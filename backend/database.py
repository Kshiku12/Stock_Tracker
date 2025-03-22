import psycopg2
from config import Config

def get_connection():
    try:
        conn = psycopg2.connect(
            host=Config.PGHOST,
            database=Config.PGDATABASE,
            user=Config.PGUSER,
            password=Config.PGPASSWORD
        )
        return conn
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None
