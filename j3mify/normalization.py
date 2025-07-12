from typing import Dict, List, Set

from .file import load_file
from .correction import re, tokenization, levenshtein, best_match

data: Dict = load_file(file_name="jejemon.json")

strip_trailing = data["fallback_rules"]["strip_trailing"]
remove_repeats = data["fallback_rules"]["remove_repeated_letters"]
custom_subs = data["fallback_rules"]["custom_substitutions"]

def fallback_pattern(word: str) -> str:
    """  Checks possible patterns """
    word = word.lower()

    for sub in custom_subs:
        word = re.sub(sub["pattern"], sub["replace"], word)

    # Remove long repeated letters
    if remove_repeats:
        word = re.sub(r'(.)\1{2,}', r'\1', word)

    word: str = normalize_characters(word)

    word = re.sub(rf"[{''.join(strip_trailing)}]+$", "", word)

    return word


def replace_character(word:str, index: int, replacement: str) -> None:
    """ Replace a character on string at a specific index """
    word_characters: List[str] = list(word)
    word_characters[index] = replacement
    return "".join(word_characters)


def tokenize_jeje_letters(word: str, variants: List[str]) -> List[str]:
    """ Splits every known jejemon alphabets """  
    # * Sort the list by length to Longest to shortest
    sorted_variants: List[str] = sorted(variants, key = len, reverse = True)
    
    avoid_specials: List[str] = [re.escape(word.lower()) for word in sorted_variants]

    pattern: str = '|'.join(avoid_specials)

    return re.findall(pattern, word.lower())


def normalize_characters(word: str) -> str:
    """ Change each character into normal ones """
    substitutes: Dict[str, Dict[str, List[str]]] = load_file(file_name="character.json")["jejemon_alphabet"]

    # * Will be using this using scoring
    common_substitute_match: Dict = {}

    word_letters_index: int = 0
    while word_letters_index < len(word):
        current_word_letter: str = word[word_letters_index]

        for normal , variants in substitutes.items():
            for variant in variants:
                if current_word_letter == variant:
                    word = replace_character(word = word, index = word_letters_index, replacement = normal)

     
        word_letters_index += 1
    
    print(common_substitute_match)
    return word


def normalization(tokenized: List[str]):
    """ Convert the word listed on array into normal word """
    jejemon_dict = {k.lower(): v.lower() for k, v in data["dictionary"].items()}

    normalized = []

    for word in tokenized:
        cleaned = word.lower()
        if cleaned in jejemon_dict:
            normalized.append(jejemon_dict[cleaned])
        else:
            normalized.append(fallback_pattern(cleaned))
    return " ".join(normalized)


def jejenized(jeje_sentence: str) -> None:
    """ Converts jejemon sentence into normal sentence """
    tokenized = tokenization(jeje_sentence)
    normalized = normalization(tokenized = tokenized)

    print("Original Tokens:", tokenized)
    print("Normalized:", normalized)


if __name__ == "__main__":
    # jejenized(
    #     jeje_sentence = "mUztAhh jejejeje"
    # )

    # print(normalize_characters("mUztAhh"))
    word: str = "Helopo^^.\\/\\/ hahahahaha"
    dictionary = ["He", "Lop", "o", "aba", "k", "^^", "\\/\\/","ha"]

    tokenized: List[str] = tokenize_jeje_letters(word = word, variants = dictionary)
    print(tokenized)
    