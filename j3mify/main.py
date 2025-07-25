from .correction import best_match
from .normalization import normalization, tokenization, normal_words

from typing import Literal, List

def jejenized(sentence: str, mode: Literal["normal", "presentation", "debug"] = "debug") -> None:
    """ Converts jejemon sentence into normal sentence """
    # * NORMALIZING
    normalized_characters: str = normalization(sentence = sentence)
    
    # * TOKENIZATION
    tokenized: List[str] = tokenization(normalized_characters)

    # * FUZZY MATCH
    correct_match: List[str] = [best_match(word = word, choices = normal_words) for word in tokenized]
    
    normalized_sentence: str = " ".join(correct_match)
    
    if mode == "debug":
          print("Jejemon Sentence: ", sentence)
          print("Character Normalization: ", normalized_characters)
          print("Tokenized: ", tokenized)
          print("Normalized Sentence:", normalized_sentence)
          return " "
    
    return normalized_sentence