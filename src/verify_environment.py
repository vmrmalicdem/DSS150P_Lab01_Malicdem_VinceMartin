"""
Task 1.3 - Verify the local environment by connecting to PostgreSQL
and confirming basic queries run successfully.

Run this AFTER `docker compose up -d` has started the postgres container.
"""

from sqlalchemy import create_engine, text

CONNECTION_STRING = "postgresql+psycopg2://dss150p:dss150p_lab@localhost:5433/dss150p_lab"


def main() -> None:
    engine = create_engine(CONNECTION_STRING)

    with engine.connect() as conn:
        version = conn.execute(text("SELECT version();")).scalar()
        current_db = conn.execute(text("SELECT current_database();")).scalar()

        print("=== PostgreSQL Connection Test ===")
        print("Server version:", version)
        print("Current database:", current_db)
        print("Connection: SUCCESS")


if __name__ == "__main__":
    main()
