import logging
from sqlalchemy.engine import Engine
from toolz import curry
import pandas as pd

from .utils import log_step


@log_step
@curry
def load_to_db(table_name: str, con: Engine, if_exists: str, df: pd.DataFrame) -> None:
    """Load a single dataframe chunk into the database."""
    df.to_sql(table_name, con=con, if_exists=if_exists)


@curry
def load_chunk(
    table_name: str, con: Engine, table_created: bool, chunk: pd.DataFrame
) -> None:
    """Loads a single chunk into the database."""
    if_exists = "replace" if not table_created else "append"
    load_to_db(table_name, con, if_exists, chunk)


@log_step
@curry
def log_load_chunks(
    table_name: str, con: Engine, df_iter: pd.io.parsers.TextFileReader
) -> None:
    """Load the dataframe to the table in the connected database"""
    table_created = False
    with con.begin() as connection:
        for df in df_iter:
            logging.info(f"Table created: {table_created}")
            logging.info(f"Loading chunk of size {len(df)} rows into '{table_name}'...")

            load_chunk(
                table_name=table_name,
                con=connection,
                table_created=table_created,
                chunk=df,
            )
            table_created = True

            logging.info(f"Chunk loaded successfully into '{table_name}'.")

    logging.info(f"All chunks have been loaded into '{table_name}'.")
