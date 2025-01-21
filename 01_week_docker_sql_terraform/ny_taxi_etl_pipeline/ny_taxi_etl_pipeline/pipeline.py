from typing import Callable, Generator, Sequence, Dict, Any
from toolz import curry, pipe, compose_left
from sqlalchemy.engine import Engine
import logging
from pathlib import Path
import pandas as pd

from .utils import log_step
from .extract import log_extract_df_iter
from .load import log_load_chunks


### EXTRACT DATA
def extract(file_path: Path) -> pd.io.parsers.TextFileReader:
    """Extract data from the given file path and return an iterator of dataframes.

    Args:
        file_path (Path): Path to the dataset file.

    Returns:
        pd.io.parsers.TextFileReader: An iterator yielding dataframes in chunks.
    """
    return log_extract_df_iter(file_path)


### TRANSFORM & PROCESS DATA
@log_step
@curry
def transform(
    transformers: Sequence[Callable[[pd.DataFrame], pd.DataFrame]],
    df_iter: Generator[pd.DataFrame, None, None],
) -> Generator[pd.DataFrame, None, None]:
    """
    Apply a sequence of transformation functions to an iterator of dataframes.

    Args:
        transformers (Sequence[Callable[[pd.DataFrame], pd.DataFrame]]):
            A list of transformation functions to apply in order.
        df_iter (Generator[pd.DataFrame, None, None]):
            A generator that yields dataframes to be transformed.

    Returns:
        Generator[pd.DataFrame, None, None]:
            A generator that yields transformed dataframes.
    """
    transform_pipeline = compose_left(*transformers)
    return (transform_pipeline(df) for df in df_iter)


### LOAD DATA TO DATABASE
@log_step
@curry
def load(table_name: str, con: Engine, df_iter: pd.io.parsers.TextFileReader) -> None:
    """
    Primary load function to manage the entire data loading process.

    Args:
        table_name (str): The name of the target database table.
        con (Engine): The database connection engine.
        df_iter (TextFileReader): A generator yielding DataFrame chunks.

    Returns:
        None
    """
    try:
        logging.info(f"Starting data load process for table '{table_name}'...")
        log_load_chunks(table_name, con, df_iter)
        logging.info(
            f"Data load process for table '{table_name}' completed successfully."
        )
    except Exception as e:
        logging.error(f"Error occurred while loading data into '{table_name}': {e}")
        raise


def etl_pipeline(
    file_path: Path,
    transformers: Sequence[Callable[[pd.DataFrame], pd.DataFrame]],
    table_name: str,
    con: Engine,
):
    """End-to-end ETL pipeline for extracting, transforming, and loading data."""
    logging.info("Starting ETL process...")
    load_func = load_func = load(table_name, con)
    transform_func = transform(transformers)
    pipe(file_path, extract, transform_func, load_func)

    logging.info("ETL process completed.")
