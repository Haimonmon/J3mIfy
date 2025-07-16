from typing import Dict, List, Set

from .file import load_file, load_txt_file
from .correction import re, tokenization, levenshtein, best_match

data: Dict = load_file(file_name="jejemon.json")

strip_trailing = data["fallback_rules"]["strip_trailing"]
remove_repeats = data["fallback_rules"]["remove_repeated_letters"]
custom_subs = data["fallback_rules"]["custom_substitutions"]

substitutes: Dict[str, Dict[str, List[str]]] = load_file(file_name="character.json")["jejemon_alphabet"]
normal_words: List[str] = load_txt_file(file_name="words.txt")




def is_punctuation(char: str) -> bool:
     pass


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


def replace_variants(word: str, normal: str, detected_variants: List[str]) -> str:
    for variant in detected_variants:
        if variant in word:
            word = word.replace(variant, normal, 1)
    return word


def normalize_characters(word: str) -> str:
    """ Change each character into normal ones """
    # * Will be using this using scoring
    word = word.lower()

    common_substitute_match: Dict = {}

    for normal, variants in substitutes.items():
            detected_jeje_char: List[str] = tokenize_jeje_letters(word = word.lower(), variants = variants)

            if detected_jeje_char:
                replacement: str = word
                i = 0
                while i < len(variants):
                    detected_jeje_char = tokenize_jeje_letters(word = replacement, variants = variants)

                    if not detected_jeje_char or i == len(variants) - 1:
                        word = replacement
                        break

                    variant: str = variants[i]

                    # print(word, "-> ", variants, "- ", variant)
                    # print("Current Word: ", word)
                    # print("Current variant: ", variant)
                    # print("Current variants lists: ", variants)
            
                    replacement = replace_variants(word = replacement, normal = normal, detected_variants = detected_jeje_char)

                    # print("Replacement:", replacement)
                    # print("Detected jejemon Characters:", detected_jeje_char)
                    # print()
                    i += 1
                
                    # common_substitute_match[normal] = best_match(word = word, choices = normal_words)

    # print(common_substitute_match)
    return word


def normalization(sentence: str) -> str:
    """  Checks possible patterns """
    sentence = sentence.lower()

    # * Remove long repeated letters
    if remove_repeats:
        # * Removes multiple Characters inside of the word like: boook -> book
        sentence = re.sub(r'(.)\1{2,}', r'\1\1', sentence)
        # * Removes multiple and double characters at the end of the word like: boookss -> books
        sentence = re.sub(r'(.)\1$', r'\1', sentence)

    sentence: str = normalize_characters(sentence)

    # sentence = re.sub(rf"[{''.join(strip_trailing)}]+$", "", sentence)

    return sentence


def jejenized(jeje_sentence: str) -> None:
    """ Converts jejemon sentence into normal sentence """
    normalized_characters: str = normalization(sentence = jeje_sentence)
    tokenized: List[str] = tokenization(normalized_characters)

    correct_match: List[str] = [best_match(word = word, choices = normal_words) for word in tokenized]

    print("Jejemon Sentence: ", jeje_sentence)
    print("Character Normalization: ", normalized_characters)
    print("Tokenized: ", tokenized)
    print("Normalized:", " ".join(correct_match))


if __name__ == "__main__":
    # jejenized(
    #     jeje_sentence = "muztAhh"
    # )

    # print(normalize_characters("mUztAhh"))
    setence1: str = "H1ndI p0 4kO nA9s45al1tA nA9t4typ3 p0 4kooo"

    sentence2: str = "muuzt4hH"

    jejenized(jeje_sentence = setence1)
    # dictionary = ['z', 's', 'x', 'zz', "ah"]

    # print(correct_match)

    # tokenized: List[str] = tokenize_jeje_letters(word = word2, variants = dictionary)
    # print(tokenized)