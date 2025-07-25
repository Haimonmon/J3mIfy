from typing import Dict, List, Set, Literal
import re

from .file import load_file, load_txt_file
from .punctuation import detect_punctuation, remove_unnecessary_punctutation
from .correction import tokenization, split_jejemon,  best_match

data: Dict = load_file(file_name="jejemon.json")
remove_repeats = data["fallback_rules"]["remove_repeated_letters"]

substitutes: Dict[str, Dict[str, List[str]]] = load_file(file_name = "character.json")
normal_words: List[str] = load_txt_file(file_name="words.txt")


def replace_variants(sentence: str, normal: str, detected_variants: List[str]) -> str:
    # ? Temporary solution
    punctuation_detector: List[str] = detect_punctuation(
          sentence = sentence, 
          punctuation_chars = substitutes["punctuations"], 
          detected_characters = detected_variants
    )
    #print(sentence)
    #print(normal)
    #print(punctuation_detector)
    #print()
    for index, variant in enumerate(detected_variants):
        if variant in sentence:
            if punctuation_detector[index] == "not punctuation":
                  sentence = sentence.replace(variant, normal, 1)
            else:
                  continue
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


def number_repetition_replacer(match):
    """
    Used by expand_number_repetition to expand patterns like 'naka2tawa' to 'nakakatawa'.
    """
    before = match.group(1)
    after = match.group(2)
    return before + before + after
def two_replacer(match):
    before = match.group(1) or ""
    digits = match.group(2)
    after = match.group(3) or ""

    count_2s = digits.count("2")
    candidates = []

    if count_2s == 1:
        if before == "" and after:
            candidates.extend(["tu" + after, "to" + after])
        elif before and after:
            candidates.extend([before + "tu" + after, before + "to" + after])
        elif before and not after:
            candidates.append(before + "to")
        elif not before and not after:
            candidates.append("to")
    elif count_2s == 2:
        if before and after:
            candidates.append(before + "to" + after)
        elif not before and after:
            # This handles 22o → totoo
            candidates.append("to" * 2 + after)

    for candidate in candidates:
        if candidate in normal_words:
            return candidate

    return candidates[0] if candidates else "to"




def expand_number_repetition(sentence: str) -> str:
    # Repeat previous syllable (nakakatawa, natutulog)
    sentence = re.sub(r'([a-zA-Z]{2})2([a-zA-Z]+)', number_repetition_replacer, sentence)

    # Covers standalone, start, middle, and double 2
    psentence = re.sub(r'\b([a-zA-Z]*?)(2{1,2})([a-zA-Z]*?)\b', two_replacer, sentence)

    return psentence

def normalization(sentence: str) -> str:
    """  Checks possible patterns """
    sentence = sentence.lower()
    sentence = expand_number_repetition(sentence)  # <-- Call the new function here

    sentence = remove_unnecessary_punctutation(sentence, substitutes = substitutes)
    # * Remove long repeated letters
    if remove_repeats:
        # * Removes multiple Characters inside of the word like: boook -> book
        sentence = re.sub(r'([^!?\.])\1{2,}', r'\1\1', sentence)
        # * Removes multiple and double characters at the end of the word like: boookss -> books
        sentence = re.sub(r'([^!?\.])\1$', r'\1', sentence)
        
    sentence = normalize_characters(sentence = sentence, substitute = "emoticons") 

    #print(sentence)
    
    sentence = normalize_characters(sentence = sentence, substitute = "alphabets")
    
    # print(sentence)
    # sentence = re.sub(rf"[{''.join(strip_trailing)}]+$", "", sentence)
    return sentence


if __name__ == "__main__":
    # jejenized(
    #     jeje_sentence = "muztAhh"
    # )

    # print(normalize_characters("mUztAhh"))
    setence1: str = "H1ndI p0 4kO nA9s45al1tA nA9t4typ3 p0 4kooo"

    sentence2: str = "muuzt4hH"

    # jejenized(jeje_sentence = setence1)
    # dictionary = ['z', 's', 'x', 'zz', "ah"]

    # print(correct_match)

    # tokenized: List[str] = tokenize_jeje_letters(word = word2, variants = dictionary)
    # print(tokenized)