from .correction import best_match
from .file import load_file, save_file
from .normalization import normalization, tokenization, normal_words, List

from typing import Literal

def jejenized(sentence: str, mode: Literal["normal", "presentation", "debug"] = None) -> None:
    """ Converts jejemon sentence into normal sentence """
    normalized_characters: str = normalization(sentence = sentence)
    tokenized: List[str] = tokenization(normalized_characters)

    correct_match: List[str] = [best_match(word = word, choices = normal_words) for word in tokenized]
    
    normalized_sentence: str = " ".join(correct_match)
    
    if mode == "normal":
          print("Jejemon Sentence: ", sentence)
          # print("Character Normalization: ", normalized_characters)
          # print("Tokenized: ", tokenized)
          print("Normalized Sentence:", normalized_sentence)
          return " "
    
    return normalized_sentence