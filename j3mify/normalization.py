from typing import Dict, List

from .file import load_file
from .correction import re, tokenization, levenshtein


data: Dict = load_file(file_name="jejemon.json")

jejemon_dict = {k.lower(): v.lower() for k, v in data["dictionary"].items()}
subs = data["fallback_rules"]["substitutions"]
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

    # Replace leetspeak
    for k, v in subs.items():
        word = word.replace(k, v)

    word = re.sub(rf"[{''.join(strip_trailing)}]+$", "", word)

    return word


def normalization(tokenized: List[str]):
    """ Convert the word listed on array into normal word """
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
    print("Normalized:", normalization)


if __name__ == "__main__":
    jejenized(
        jeje_sentence = "mUztAh jeje"
    )
    