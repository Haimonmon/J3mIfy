from .correction import correction, join_punctuation, tokenization
from .normalization import normalization, normal_words, substitutes

from typing import Literal, List, Dict, Any

def j3j3niZ3d(sentence: str, mode: Literal["presentation", "debug"] = None) -> Dict[str, str] | str:
    """ Converts jejemon sentence into normal sentence """
    if not sentence:
         return 
    
    # * NORMALIZING
    normalized_characters: str = normalization(sentence)

    # * TOKENIZATION
    tokenized: List[str] = tokenization(normalized_characters)

    # * FUZZY MATCH
    correct_match: List[str] = [correction(word, normal_words, substitutes) for word in tokenized]
    correct_match = join_punctuation(correct_match, substitutes)

    normalized_sentence: str = " ".join(correct_match)
    
    if mode == "debug":
          return {
               "original_sentence": sentence,
               "character_normalization": normalized_characters,
               "tokenization": tokenized,
               "normalized_sentence": normalized_sentence
          }
    if mode == "presentation":
         return {
              "original_sentence": sentence,
              "normalized_sentence": normalized_sentence
         }

    
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
