import re
from typing import List


def emoticon_unicodes() -> set:
    """ Gives emoticons Unicodes """
    return (
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002700-\U000027BF"  # dingbats
        "\U0001F900-\U0001F9FF"  # supplemental
        "\U0001FA70-\U0001FAFF"  # emoji v13
        "\U00002600-\U000026FF"  # misc symbols
        "\U00002B00-\U00002BFF"  # arrows and more
    )


def tokenization(sentence: str) -> List[str]:
    """ Separates word by word and put it in an array"""
    pattern = re.compile(fr"[a-zA-Z0-9']+|[{emoticon_unicodes()}]|[.,!?;]", re.UNICODE, )
    return pattern.findall(sentence)


def split_jejemon(word: str, variants: List[str]) -> List[str]:
    """ Splits every known jejemon alphabets """
    # * Sort the list by length to Longest to shortest
    sorted_variants: List[str] = sorted(variants, key=len, reverse=True)

    avoid_specials: List[str] = [re.escape(word.lower()) for word in sorted_variants]

    pattern: str = '|'.join(avoid_specials)
    
    return re.findall(pattern, word.lower())


def levenshtein(keyword1: str, keyword2: str) -> int:
    """ A function that scales the misspelled words wrongness. """
    len1 = len(keyword1)
    len2 = len(keyword2)

    dp = [[0] * (len2 + 1) for x in range(len1 + 1)]

    for i in range(len1 + 1):
        for j in range(len2 + 1):

            if i == 0:
                dp[i][j] = j

            elif j == 0:
                dp[i][j] = i

            elif keyword1[i-1] == keyword2[j-1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])

    return dp[len1][len2]


def fuzzy_matching(keyword1: str, keyword2: str) -> float:
    """ Compares the similiraties between the two words given by levenshtein """
    distance = levenshtein(keyword1=keyword1, keyword2=keyword2)
    score = 1 - (distance / max(len(keyword1), len(keyword2)))
    return round(score, 2)


def jaccard_similarity(a: str, b: str) -> float:
    """ Compares the similiraties between the two words given by levenshtein"""
    set_a = set(a)
    set_b = set(b)
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def hybrid_score(a: str, b: str) -> float:
    """ Both jaccard and levenshtein distancing """
    lev = fuzzy_matching(a, b)
    jac = jaccard_similarity(a, b)
    return round((lev + jac) / 2, 2)


def best_match(word: str, choices: List["str"], threshold: float = 0.55) -> str:
    """ identifies whats the best match on the given word with the given list of possible matches """
    if word in choices:
        return word

    matches = None
    best_score = -1

    for option in choices:
        score = hybrid_score(word, option)
        if score >= best_score:
            # matches.append(option)
            matches = option
            best_score = score

    if best_score > threshold:
        return matches

    return word


if __name__ == "__main__":  
    # ! DISCLAIMER: Nahanp kolang sa internet 💀👌✨
    word = "😜😛🥰Anong masarap na KAPE@ edi KAPEling ka samahan mopa ng DECAF DECAFapakawalan mamahalin kita i love my life because my life is you🤪😘😂🤣" 

    matches = best_match(
        word = "misyu",
        choices = ["miss you"]
    )

    print(matches)

    """
    TODO: 
    * 1. Improve tokenization about identifying special characters within word or sentence
    """