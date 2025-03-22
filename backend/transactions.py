from flask import Blueprint, request, jsonify
from database import get_connection

transactions_blueprint = Blueprint("transactions", __name__)

@transactions_blueprint.route("/buy", methods=["POST"])
def buy_stock():
    data = request.get_json()
    user_id = data.get("user_id")
    ticker = data.get("ticker")
    quantity = data.get("quantity")
    price = data.get("price")

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    with conn.cursor() as cursor:
        cursor.execute("SELECT balance FROM Users WHERE user_id = %s", (user_id,))
        balance = cursor.fetchone()[0]

        total_cost = quantity * price
        if balance < total_cost:
            return jsonify({"error": "Insufficient funds"}), 400

        cursor.execute("UPDATE Users SET balance = balance - %s WHERE user_id = %s", (total_cost, user_id))
        cursor.execute("INSERT INTO Transactions (user_id, stock_ticker, type, quantity, price) VALUES (%s, %s, %s, %s, %s)",
                       (user_id, ticker, "BUY", quantity, price))
        conn.commit()

    return jsonify({"message": "Stock purchased successfully"}), 200
