from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from database import get_connection

bcrypt = Bcrypt()
auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Users (name, balance) VALUES (%s, %s) RETURNING user_id", (name, 10000))
        user_id = cursor.fetchone()[0]
        conn.commit()

    return jsonify({"message": "User created successfully", "user_id": user_id}), 201

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    with conn.cursor() as cursor:
        cursor.execute("SELECT user_id, password FROM Users WHERE name = %s", (name,))
        user = cursor.fetchone()

    if not user or not bcrypt.check_password_hash(user[1], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user[0])
    return jsonify({"token": token, "user_id": user[0]}), 200
