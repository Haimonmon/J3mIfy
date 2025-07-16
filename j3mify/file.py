import json

from typing import List, Any, Dict

folder_directory = r"j3mify/lexicon/"

def load_file(file_name: str) -> List | Dict | Any:
    """ Loads data on the specified json file name. """
    with open(fr"{folder_directory}{file_name}", "r", encoding="utf-8") as file:
        return json.load(file)


def load_txt_file(file_name: str) -> List[str]:
    """ Loads data on the specified txt file name. """
    with open(fr"{folder_directory}{file_name}", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def save_file(file_name: str, data: Any) -> Any:
    """ Saves data on the specified json file name. """
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    pass
