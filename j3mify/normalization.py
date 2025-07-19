from typing import Dict, List, Set, Literal

from .file import load_file, load_txt_file
from .punctuation import detect_punctuation
from .correction import re, tokenization, split_jejemon,  best_match

data: Dict = load_file(file_name="jejemon.json")
remove_repeats = data["fallback_rules"]["remove_repeated_letters"]

substitutes: Dict[str, Dict[str, List[str]]] = load_file(file_name = "character.json")
normal_words: List[str] = load_txt_file(file_name="words.txt")

# * Allowed for sandwich ruling
allowed_punctuations: List[str] = ["!","@","'"]

def apply_sandwich_ruling(sentence: str, allowed: list, not_allowed: list) -> str:
    def replacer(match):
        punct = match.group(1)
        if punct in allowed:
            return punct  # * keep it
        
        if punct in not_allowed:
            return ""  # * mark it for removal
            
    pattern = re.compile(r'(?<=\w)([^\w\s])(?=\w)')
    return pattern.sub(replacer, sentence)


def get_allowed_punctuations() -> None:
      pass


def remove_unnecessary_punctutation(sentence: str) -> str:
     # * Real Punctuations
     punctuations: List[str] = substitutes["punctuations"]
      
     sentence = apply_sandwich_ruling(sentence = sentence, allowed = allowed_punctuations, not_allowed = punctuations)
     return sentence
     
     
def replace_variants(sentence: str, normal: str, detected_variants: List[str]) -> str:
    for variant in detected_variants:
        if variant in sentence:
            sentence = sentence.replace(variant, normal, 1)
    return sentence


def normalize_characters(sentence: str, substitute: Literal["alphabets","emoticons"]) -> str:
    """ Change each character into normal ones """
    if not substitute or substitute not in ["alphabets","emoticons"]:
    	return
    
    sentence = sentence.lower()

    common_substitute_match: Dict = {}

    for normal, variants in substitutes[substitute].items():
            detected_jeje_char: List[str] = split_jejemon(word = sentence.lower(), variants = variants)

            if detected_jeje_char:
                replacement: str = sentence
                i = 0
                while i < len(variants):
                    detected_jeje_char = split_jejemon(word = replacement, variants = variants)
                    
                    variant: str = variants[i]
                    
                    replacement = replace_variants(sentence = replacement, normal = normal, detected_variants = detected_jeje_char)
                    
                    if not detected_jeje_char or i == len(variants) - 1:
                        sentence = replacement
                        break
                    i += 1
                    # common_substitute_match[normal] = best_match(word = word, choices = normal_words)
    return sentence


def normalization(sentence: str) -> str:
    """  Checks possible patterns """
    sentence = sentence.lower()
    
    sentence = remove_unnecessary_punctutation(sentence)
    # * Remove long repeated letters
    if remove_repeats:
        # * Removes multiple Characters inside of the word like: boook -> book
        sentence = re.sub(r'([^!?\.])\1{2,}', r'\1\1', sentence)
        # * Removes multiple and double characters at the end of the word like: boookss -> books
        sentence = re.sub(r'([^!?\.])\1$', r'\1', sentence)
        
    sentence = normalize_characters(sentence = sentence, substitute = "emoticons") 
    
    sentence = normalize_characters(sentence = sentence, substitute = "alphabets")

    # sentence = re.sub(rf"[{''.join(strip_trailing)}]+$", "", sentence)
    return sentence


def jejenized(sentence: str, mode: Literal["normal", "presentation", "debug"] = None) -> None:
    """ Converts jejemon sentence into normal sentence """
    normalized_characters: str = normalization(sentence = sentence)
    # tokenized: List[str] = tokenization(normalized_characters)

    # correct_match: List[str] = [best_match(word = word, choices = normal_words) for word in tokenized]
    
    # normalized_sentence: str = " ".join(correct_match)
    
    if mode == "normal":
          print("Jejemon Sentence: ", sentence)
          # print("Character Normalization: ", normalized_characters)
          # print("Tokenized: ", tokenized)
          print("Normalized Sentence:", normalized_sentence)
          return " "
    
    return normalized_characters
          

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