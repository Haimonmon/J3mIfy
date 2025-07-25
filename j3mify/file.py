import os
import json
import asyncio
import aiofiles

from typing import List, Any, Dict
from collections import defaultdict

directory = r"j3mify/lexicon/"

LIST_SIZE: int = 5000

alphabet: List[str] = [
    "a", "b", "c", "d", "e",
    "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o",
    "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y",
    "z"
]

def load_file(file_name: str) -> List | Dict | Any:
    """ Loads data on the specified json file name. """
    with open(fr"{directory}{file_name}", "r", encoding="utf-8") as file:
        return json.load(file)


def load_txt_file(file_name: str) -> List[str]:
    """ Loads data on the specified txt file name. """
    with open(fr"{directory}{file_name}", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def save_file(file_name: str, data: Any) -> Any:
    """ Saves data on the specified json file name. """
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


def create_file(directory: str, file_name: str) -> bool:
      """ Creates a specified file with its file name and designated directrory """
      os.makedirs(directory, exist_ok = True)
      file_path = os.path.join(directory, file_name)
      
      if os.path.exists(file_path):
            return False

      with open(file_path, "w") as f:
            pass 
      return True
 
 
def create_folder(directory_name: str) -> bool:
      """ Creates a folder by its given name. """
      if not os.path.exists(directory_name):
            os.makedirs(directory_name, exist_ok=True)
            return True
      return False

      
# * Word File sorter
def group_words_by_letter(words: List[str]) -> Dict[str, List[str]]:
      """ Grouped the list of words by their designated Alphabet, creates a dictionary """
      grouped = defaultdict(list)
      for word in words:
            if not word:
                  continue
            
            letter = word[0].lower()
            if letter not in alphabet:
                  continue
            
            if LIST_SIZE and len(grouped[letter]) < LIST_SIZE:
                  grouped[word[0].lower()].append(word)
      return grouped


async def write_words_to_file(letter: str, words: List[str], directory: str, semaphore: asyncio.Semaphore):
      async with semaphore:
            file_name = f"{letter.upper()}{letter.lower()}.txt"
            file_path = os.path.join(directory, file_name)
            os.makedirs(directory, exist_ok=True)

            async with aiofiles.open(file_path, mode='w', encoding='utf-8') as f:
                  await f.write('\n'.join(words))
            print(f"✓ {file_name}: {len(words): ,} words written.")
        
        
async def organize_data(file_name: str, saving_directory: str, task_limit: int = 3) -> None:
      """ Gets data and sorts out alphabetically """
      unorganized_data: List[str] = load_txt_file(file_name)
      
      folder_created: bool = create_folder(saving_directory)
      for letter in alphabet:
            file_created: bool = create_file(directory = saving_directory, file_name = f"{letter.upper()}{letter.lower()}.txt")
            
      grouped: Dict[str, List[str]] = group_words_by_letter(unorganized_data)
      
      semaphore = asyncio.Semaphore(task_limit)
      
      tasks = [
            write_words_to_file(letter, grouped[letter], saving_directory, semaphore)
            for letter in grouped
      ] 
      
      await asyncio.gather(*tasks)
      print(f"✓ Data has been organized on {saving_directory} directory. \n")   
      
      
if __name__ == "__main__":
      # * Source: https://github.com/dwyl/english-words
      english_source: str = f"source/English-wordlist.txt"
      english_directory: str = f"{directory}/english-dictionary"
      
      asyncio.run(organize_data(
            file_name = english_source,
            saving_directory = english_directory
      ))
      
      # * Source: https://github.com/AustinZuniga/Filipino-wordlist/blob/master/Filipino-wordlist.txt
      tagalog_source: str = "source/tagalog_dict.txt"
      tagalog_directory: str = f"{directory}/tagalog-dictionary"

      asyncio.run(organize_data(
            file_name = tagalog_source,
            saving_directory = tagalog_directory
      ))
