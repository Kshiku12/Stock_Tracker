from flask import Blueprint, jsonify
import yfinance as yf

stock_blueprint = Blueprint("stock", __name__)

@stock_blueprint.route("/<ticker>", methods=["GET"])
def get_stock(ticker):
    stock = yf.Ticker(ticker)
    stock_info = stock.info

    return jsonify({
        "ticker": ticker,
        "name": stock_info.get("longName", "N/A"),
        "price": stock_info.get("regularMarketPrice", 0),
        "market_cap": stock_info.get("marketCap", 0)
    })
