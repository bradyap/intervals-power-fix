import os
import shutil
from dotenv import load_dotenv


def get_api_key() -> str:
    """Gets Intervals API key from environment variable.

    :raises ValueError: If the API key is not found in environment variables
    :return: The Intervals API key
    :rtype: str
    """
    load_dotenv()

    api_key = os.getenv('INTERVALS_API_KEY')

    if api_key:
        print("API key loaded.")
    else:
        raise ValueError(
            "API key not found. Please set it in Settings -> Set API Key.")

    return api_key


def set_api_key(api_key: str) -> None:
    """Sets Intervals API key in environment variable. Creates .env file if it doesn't exist.

    :param api_key: The Intervals API key to set
    :type api_key: str
    """

    with open('.env', 'w') as f:
        f.write(f'INTERVALS_API_KEY={api_key}')


def find_replace(fpath: str, find_replace: dict[str, str]) -> None:
    """Does find/replace on a file for a given set of values.

    :param fpath: Path to the file
    :type fpath: str
    :param find_replace: Dict where keys are what to find, values are what to replace with
    :type find_replace: dict[str, str]
    """
    with open(fpath, 'r') as f:
        csv_data = f.read()

    for k, v in find_replace.items():
        csv_data = csv_data.replace(k, v)

    with open(fpath, 'w') as f:
        f.write(csv_data)


def rmr(wdpath: str) -> None:
    """Deletes folder and all contents.

    :param wdpath: Path to the folder
    :type wdpath: str
    """
    if os.path.exists(wdpath):
        try:
            shutil.rmtree(wdpath)
        except Exception as e:
            print(f"Failed to delete folder: {e}")
    else:
        print(f"Folder not found: {wdpath}")
