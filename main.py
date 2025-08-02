import json

from app import display_j3j3m0Nizer

from typing import List

def load_file(file_name: str) -> any:
    """ Loads data on the specified json file name. """
    with open(fr"{file_name}", "r", encoding="utf-8") as file:
        return json.load(file)
    

def main() -> None:
    """ main terminal """
    example_list1: List[str] = load_file("./example/example_data1.json")
    example_list2: List[str] = load_file("./example/example_data2.json")
    
    display_j3j3m0Nizer(sentence = example_list1, mode = "debug")


if __name__ == "__main__":
    main()

    # * Thanks to the n#ggs and the source
    # * Jejemon Source: http://www.reyjr.com/2010/05/i-can-jejemon-write-lolz-jejejeje.html?m=1