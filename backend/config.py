import os

class Config:
    PGHOST = os.getenv("PGHOST", "ep-yellow-hall-a5tqvaav-pooler.us-east-2.aws.neon.tech")
    PGDATABASE = os.getenv("PGDATABASE", "neondb")
    PGUSER = os.getenv("PGUSER", "neondb_owner")
    PGPASSWORD = os.getenv("PGPASSWORD", "npg_8RY2uXlLzwPI")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Change this in production
