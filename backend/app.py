from flask import Flask
from flask_cors import CORS
from auth import auth_blueprint
from stock import stock_blueprint
from transactions import transactions_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(stock_blueprint, url_prefix="/stock")
app.register_blueprint(transactions_blueprint, url_prefix="/transactions")

if __name__ == "__main__":
    app.run(debug=True)
