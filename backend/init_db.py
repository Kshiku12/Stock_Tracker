import psycopg2
import yfinance as yf
import numpy as np

# Database credentials for Neon PostgreSQL
PGHOST='ep-yellow-hall-a5tqvaav-pooler.us-east-2.aws.neon.tech'
PGDATABASE='neondb'
PGUSER='neondb_owner'
PGPASSWORD='npg_8RY2uXlLzwPI'

# Establish a single connection
def get_connection():
    try:
        conn = psycopg2.connect(
            host=PGHOST,
            database=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD
        )
        print("✅ Connected to Neon PostgreSQL successfully!")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to Neon PostgreSQL: {e}")
        return None

# Generic function to execute queries (INSERT, UPDATE, DELETE)
def execute_query(conn, query, params=None, fetch=False):
    with conn.cursor() as cursor:
        cursor.execute(query, params or ())
        if fetch:
            return cursor.fetchall()
        conn.commit()

# Create All 8 Tables
def create_tables(conn):
    queries = [
        """CREATE TABLE IF NOT EXISTS Stock (
            ticker VARCHAR(20) PRIMARY KEY,
            name VARCHAR(255),
            price NUMERIC(10,2)
        );""",
        
        """CREATE TABLE IF NOT EXISTS Market_Data (
            stock_ticker VARCHAR(20) PRIMARY KEY REFERENCES Stock(ticker),
            market_cap BIGINT,
            volume BIGINT,
            pe_ratio NUMERIC(10,2),
            week_52_high NUMERIC(10,2),
            week_52_low NUMERIC(10,2)
        );""",
        
        """CREATE TABLE IF NOT EXISTS Users (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            balance NUMERIC(10,2)
        );""",
        
        """CREATE TABLE IF NOT EXISTS Brokers (
            brokerage_id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            user_count INT
        );""",
        
        """CREATE TABLE IF NOT EXISTS Transactions (
            transaction_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES Users(user_id),
            stock_ticker VARCHAR(20) REFERENCES Stock(ticker),
            type VARCHAR(10),
            quantity INT,
            price NUMERIC(10,2),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""",
        
        """CREATE TABLE IF NOT EXISTS Portfolio (
            portfolio_id SERIAL PRIMARY KEY,
            user_id INT REFERENCES Users(user_id),
            stock_ticker VARCHAR(20) REFERENCES Stock(ticker),
            quantity INT,
            average_price NUMERIC(10,2)
        );""",
        
        """CREATE TABLE IF NOT EXISTS Quarterly_Financials (
            stock_ticker VARCHAR(20) REFERENCES Stock(ticker),
            eps_growth NUMERIC(10,2),
            revenue_growth NUMERIC(10,2)
        );""",
        
        """CREATE TABLE IF NOT EXISTS Yearly_Financials (
            stock_ticker VARCHAR(20) REFERENCES Stock(ticker),
            eps_growth NUMERIC(10,2),
            revenue_growth NUMERIC(10,2)
        );"""
    ]
    
    for query in queries:
        execute_query(conn, query)
    
    print("✅ All tables created successfully!")

# Fetch Stock Data from Yahoo Finance
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        history = stock.history(period="1d")

        if history.empty:
            raise ValueError("No stock history available")

        return {
            "ticker": ticker,
            "name": stock_info.get("longName", "N/A"),
            "price": float(history["Close"].iloc[-1]),
            "market_cap": float(stock_info.get("marketCap", 0)) if stock_info.get("marketCap") else 0,
            "volume": int(stock_info.get("volume", 0)) if stock_info.get("volume") else 0,
            "pe_ratio": float(stock_info.get("trailingPE", 0)) if stock_info.get("trailingPE") else 0,
            "week_52_high": float(stock_info.get("fiftyTwoWeekHigh", 0)) if stock_info.get("fiftyTwoWeekHigh") else 0,
            "week_52_low": float(stock_info.get("fiftyTwoWeekLow", 0)) if stock_info.get("fiftyTwoWeekLow") else 0
        }
    except Exception as e:
        print(f"❌ Error fetching data for {ticker}: {e}")
        return None

# Insert User
def insert_user(conn, user_id, name, balance):
    execute_query(conn, """
        INSERT INTO Users (user_id, name, balance) VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO NOTHING;
    """, (user_id, name, balance))
    print(f"✅ Inserted user: {name} (ID: {user_id})")

# Insert Stock Data
def insert_stock(conn, stock_data):
    execute_query(conn, """
        INSERT INTO Stock (ticker, name, price) VALUES (%s, %s, %s)
        ON CONFLICT (ticker) DO NOTHING;
    """, (stock_data["ticker"], stock_data["name"], stock_data["price"]))
    print(f"✅ Inserted stock: {stock_data['ticker']}")

# Insert Market Data
def insert_market_data(conn, stock_data):
    execute_query(conn, """
        INSERT INTO Market_Data (stock_ticker, market_cap, volume, pe_ratio, week_52_high, week_52_low)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (stock_ticker) DO NOTHING;
    """, (stock_data["ticker"], stock_data["market_cap"], stock_data["volume"],
          stock_data["pe_ratio"], stock_data["week_52_high"], stock_data["week_52_low"]))
    print(f"✅ Inserted market data for: {stock_data['ticker']}")

# Record Transaction
def record_transaction(conn, user_id, ticker, trans_type, qty, price):
    user_exists = execute_query(conn, "SELECT 1 FROM Users WHERE user_id = %s", (user_id,), fetch=True)
    if not user_exists:
        print(f"❌ Error: User ID {user_id} does not exist. Transaction cannot be processed.")
        return

    execute_query(conn, """
        INSERT INTO Transactions (user_id, stock_ticker, type, quantity, price, timestamp)
        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP);
    """, (user_id, ticker, trans_type, qty, price))
    print("✅ Transaction recorded!")

# Insert Portfolio Data
def insert_portfolio(conn, user_id, ticker, quantity, average_price):
    execute_query(conn, """
        INSERT INTO Portfolio (user_id, stock_ticker, quantity, average_price)
        VALUES (%s, %s, %s, %s);
    """, (user_id, ticker, quantity, average_price))
    print("✅ Portfolio updated!")