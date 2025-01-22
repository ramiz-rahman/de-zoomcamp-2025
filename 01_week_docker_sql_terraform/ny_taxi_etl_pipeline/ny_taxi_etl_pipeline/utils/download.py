import logging
import requests
from pathlib import Path
from typing import Optional, Tuple
from functools import partial


def create_data_directory(directory: str) -> Path:
    """Ensure the data directory exists and return its Path object."""
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_file_path(directory: Path, filename: str) -> Path:
    """Construct the full file path for the given filename."""
    return directory / filename


def file_exists(file_path: Path) -> bool:
    """Check if the given file already exists."""
    return file_path.exists()


def download_file(url: str, timeout: int) -> bytes:
    """Download the file content from the given URL."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.content


def save_file(file_path: Path, content: bytes) -> None:
    """Save the downloaded content to the specified file path."""
    file_path.write_bytes(content)


def log_and_return(value, message: str):
    """Log a message and return the value."""
    logging.info(message)
    return value


def attempt_download(url: str, timeout: int, retries: int) -> Optional[bytes]:
    """Attempt to download a file with retry logic."""
    for attempt in range(retries):
        try:
            return log_and_return(
                download_file(url, timeout),
                f"Download successful from {url} on attempt {attempt + 1}",
            )
        except requests.exceptions.RequestException as e:
            logging.warning(f"Download attempt {attempt + 1} failed: {e}")
    logging.error("Max retries reached. Download failed.")
    return None


def download_csv(
    url: str, filename: str, retries: int = 3, timeout: int = 30
) -> Optional[Path]:
    """
    Download a CSV file in a functional style.

    Args:
        url (str): The URL of the CSV file.
        filename (str): The desired filename.
        retries (int, optional): Number of retries on failure (default is 3).
        timeout (int, optional): Timeout in seconds for the request (default is 30).

    Returns:
        Optional[Path]: The path to the downloaded file, or None if download failed.
    """
    data_dir = create_data_directory("data")
    file_path = build_file_path(data_dir, filename)

    if file_exists(file_path):
        logging.info(f"File already exists: {file_path}. Skipping download.")
        return file_path

    logging.info(f"Starting download from: {url}")

    download_content = attempt_download(url, timeout, retries)

    if download_content:
        save_file(file_path, download_content)
        logging.info(f"File saved to: {file_path}")
        return file_path

    return None
