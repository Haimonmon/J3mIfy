from .correction import correction, join_punctuation, tokenization
from .normalization import normalization, normal_words, substitutes

from typing import Literal, List

def jejenized(sentence: str, mode: Literal["normal", "presentation", "debug"] = None) -> None:
    """ Converts jejemon sentence into normal sentence """
    # * NORMALIZING
    normalized_characters: str = normalization(sentence)

    # * TOKENIZATION
    tokenized: List[str] = tokenization(normalized_characters)

    # * FUZZY MATCH
    correct_match: List[str] = [correction(word, normal_words, substitutes) for word in tokenized]
    correct_match = join_punctuation(correct_match, substitutes)

    normalized_sentence: str = " ".join(correct_match)
    
    if mode == "debug":
          print("Jejemon Sentence: ", sentence)
          print("Character Normalization: ", normalized_characters)
          print("Tokenized: ", tokenized)
          print("Normalized Sentence:", normalized_sentence)
          return " "
    
    return normalized_sentence

if __name__ == "__main__":
     pass

     """
     TODO: Bugs Encounter
     
     1. ending jejemon punctuation like @ and ! at the end of word can be possible normalized, like: origam! and tax! to origami and taxi
     2. sandwich emoticon need to be remove , as it cuts off words like good (emoji) night
     3. improve normalization
     ! 4. 22o should be output "totoo", apply this with numbers like 130130 ,is for B*BO ( Just Censored ) [HARDCODED]
     * 5, 3owz need to be convert to hello , especially on hard jejemon [HARDCODED]
     6. 4 can be "for" and "A" Needs to be fixed
     """
