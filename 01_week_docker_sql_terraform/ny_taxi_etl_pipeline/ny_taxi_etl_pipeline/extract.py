import logging
import pandas as pd
from typing import Dict, Any, Generator
from pathlib import Path


def detect_compression(file_path: Path) -> str:
    """Automatically detect the compression type based on the file extension."""
    if file_path.suffix == ".gz":
        return "gzip"
    elif file_path.suffix == ".zip":
        return "zip"
    elif file_path.suffix == ".bz2":
        return "bz2"
    else:
        return "infer"


def read_csv_in_chunks(
    file_path: Path, compression: str, chunk_size: int
) -> pd.io.parsers.TextFileReader:
    """Read CSV file in chunks using pandas"""
    return pd.read_csv(
        file_path,
        compression=compression,
        chunksize=chunk_size,
        iterator=True,
    )


def validate_dataset(file_path: Path) -> None:
    """Validate the dataset to ensure it exists and has a valid compression type."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    valid_extensions = [".csv", ".csv.gz", ".csv.zip", ".csv.bz2"]
    file_extension = "".join(file_path.suffixes)

    if file_extension not in valid_extensions:
        raise ValueError(f"Invalid file extension for dataset: {file_extension}")


def extract_df_iter(
    file_path: Path, chunk_size: int = 50000
) -> pd.io.parsers.TextFileReader:
    """Generate DataFrame chunks from the dataset"""
    validate_dataset(file_path)
    compression = detect_compression(file_path)
    return read_csv_in_chunks(file_path, compression, chunk_size)


# Logging wrapper function to handle logging externally
def log_extract_df_iter(
    file_path: Path, chunk_size: int = 50000
) -> pd.io.parsers.TextFileReader:
    """Log information and call extract_df_iter"""
    logging.info(f"Starting data extraction for {file_path}")
    try:
        yield from extract_df_iter(file_path, chunk_size)
        logging.info(f"Data extraction for {file_path} completed successfully.")
    except Exception as e:
        logging.error(f"Error during data extraction for {file_path}: {e}")
        raise
