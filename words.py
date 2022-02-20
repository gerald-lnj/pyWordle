"""Module that handles downloading and filtering of words list."""
from typing import Generator, List

import requests

CSW15_URL = "https://pages.cs.wisc.edu/~o-laughl/csw15.txt"
WORD_LIST_FILEPATH = "words.txt"


def load_words(length: int = 5) -> List[str]:
    """
    Returns list of words based on downloaded words list and length filter.
    Attempts to download word list if file is not found.

    Args:
        length (int, optional): Word length. Defaults to 5.

    Returns:
        List[str]: List of words.
    """
    try:
        words = word_generator(word_list_filepath=WORD_LIST_FILEPATH, length=length)
        return list(words)
    except FileNotFoundError as e:
        print(f"{WORD_LIST_FILEPATH} not found, downloading...")
        download_list()
        return load_words()


def download_list(url: str = CSW15_URL):
    """
    Downloads file at url and saves it to WORD_LIST_FILEPATH.

    Args:
        url (str, optional): Location of words list to download. Defaults to CSW15_URL.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(WORD_LIST_FILEPATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=512 * 1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)


def word_generator(
    word_list_filepath: str = WORD_LIST_FILEPATH, length: int = 5
) -> Generator[str, None, None]:
    """
    Memory efficient way to filter local words list by word length.

    Args:
        word_list_filepath (str, optional): Local words list file. Defaults to WORD_LIST_FILEPATH.
        length (int, optional): Word length to filter by. Defaults to 5.

    Yields:
        Generator[str, None, None]: Generator that yields words.
    """
    with open(word_list_filepath, "r") as word_list:
        for line in word_list:
            line = line.strip()
            if len(line) == length:
                yield line.upper()


if __name__ == "__main__":
    download_list()
