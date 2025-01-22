from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
import logging


def get_db_engine(user: str, password: str, host: str, port: int, db: str) -> Engine:
    """
    Create a PostgreSQL database connection engine.

    Args:
        user (str): Database username.
        password (str): Database password.
        host (str): Database host (e.g., 'localhost' or an IP address).
        port (int): Port number to connect to the database.
        db (str): Name of the database.

    Returns:
        Engine: SQLAlchemy Engine object for interacting with the database.

    Raises:
        ValueError: If any required parameter is missing or invalid.
        Exception: If the connection fails.
    """
    if not all([user, password, host, port, db]):
        raise ValueError("All database connection parameters must be provided.")

    try:
        logging.info(f"Attempting to connect to the database at {host}:{port}/{db}")

        db_url = URL.create(
            drivername="postgresql",
            username=user,
            password=password,
            host=host,
            port=port,
            database=db,
        )

        engine = create_engine(db_url)

        # Try connecting to ensure the credentials are correct
        with engine.connect() as connection:
            logging.info("Database connection established successfully.")

        return engine

    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        raise
