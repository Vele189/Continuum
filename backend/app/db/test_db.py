from sqlalchemy import text
from app.db.session import engine

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ PostgreSQL connection successful:", result.scalar())
    except Exception as e:
        print("❌ PostgreSQL connection failed:", e)

if __name__ == "__main__":
    test_connection()
