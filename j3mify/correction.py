import re
from typing import List, Dict


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
    pattern = re.compile(fr"[a-zA-Z0-9']+|[{emoticon_unicodes()}]|[.,!?;\"()]", re.UNICODE, )
    return pattern.findall(sentence)


def join_punctuation(tokens: List[str], allowed_puncts: Dict[str, List[str]]) -> List[str]:
    """ Joins the tokenized puntuations """
    result = []
    i = 0

    while i < len(tokens):
        token = tokens[i]

        # If it's a word and next is punctuation
        if i + 1 < len(tokens) and tokens[i + 1] in allowed_puncts["punctuations"]:
            combined = token
            while i + 1 < len(tokens) and tokens[i + 1] in allowed_puncts["punctuations"]:
                combined += tokens[i + 1]
                i += 1
            result.append(combined)
        else:
            result.append(token)

        i += 1

    return result


def split_jejemon(word: str, variants: List[str]) -> List[str]:
    """ Splits every known jejemon alphabets """
    # * Sort the list by length to Longest to shortest
    sorted_variants: List[str] = sorted(variants, key=len, reverse=True)

    avoid_specials: List[str] = [re.escape(word.lower()) for word in sorted_variants]

    pattern: str = '|'.join(avoid_specials)
    
    return re.findall(pattern, word.lower())


def split_and_normalize_jejemon(word: str, choices: Dict[str, List[str]], threshold: float = 0.55) -> str:
    """ Breaks down a jumbled jejemon word and normalizes known parts """
    i = 0
    normalized_parts = []

    while i < len(word):
        found = False
        # * Try longest possible substrings first
        for window in range(10, 2, -1): 
            chunk = word[i:i+window]
            if not chunk:
                continue
            normalized = best_jejemon_match(chunk, choices, threshold)
            # * A change happened
            if normalized != chunk:
                normalized_parts.append(normalized)
                i += window
                found = True
                break
        if not found:
            # * If no match, keep one character and move forward
            normalized_parts.append(word[i])
            i += 1

    return "".join(normalized_parts)


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
    """ Both jaccard and levenshtein based distancing or scoring """
    lev = fuzzy_matching(a, b)
    jac = jaccard_similarity(a, b)
    return round((lev + jac) / 2, 2)


def best_normal_match(word: str, choices: List["str"], threshold: float = 0.55) -> str:
    """ identifies whats the best match on the given word with the given list of choices with possible matches """
    if word in choices:
        return word, 1

    matches = None
    best_score = -1

    for option in choices:
        score = hybrid_score(word, option.lower())
        if score >= best_score:
            matches = option
            best_score = score
            

    if best_score > threshold:
        return matches, best_score

    return word, best_score


def extract_laughs(word: str, choices: Dict[str, List[str]]) -> str:
    """ extracts only valid repeated laugh characters from a word"""
    # * reverse mapping
    all_variants = [v for lst in choices.values() for v in lst]
    all_variants.sort(key=lambda s: -len(s))

    pattern = '|'.join(re.escape(v) for v in all_variants)
    repeated_pattern = rf'((?:{pattern}){{2,}})'

    matches = re.finditer(repeated_pattern, word)

    extracted = []
    for match in matches:
        sequence = match.group(0)

        for variant in all_variants:
            count = len(re.findall(re.escape(variant), sequence))
            extracted.extend([variant] * count)

    normalized_laugh = []
    for char in extracted:
        for replacement, jejemon in choices.items():
            if char in jejemon:
                normalized_laugh.append(replacement)
    
    if not normalized_laugh:
        return word
    return "".join(normalized_laugh)


def best_jejemon_match(word: str, choices: Dict[str, List[str]], threshold: float = 0.55) -> str:
    """ corrects moderate jejemon wordings """
    for normal, jejemon in choices.items():
        matched, best_score = best_normal_match(word, jejemon)

        if matched and best_score > threshold:
            return normal

    return word


def correction(word: str, normal_choices: List[str], replacement_choices: Dict[str, List[str]], threshold: float = 0.55) -> str:
    """ just combined `best_jejemon_match` and `best_normal_match` """
    
    word = best_normal_match(
        word = word,
        choices = normal_choices,
        threshold = threshold
    )

    if word[0] not in normal_choices:
        word = split_and_normalize_jejemon(word = word[0], choices = replacement_choices["jejewords"], threshold = threshold)

        word = best_jejemon_match(
            word = word,
            choices = replacement_choices["jejewords"],
            threshold = threshold
        )

        if (word not in normal_choices) and (word not in replacement_choices["punctuations"]):
            word = extract_laughs(
                word = word,
                choices = replacement_choices["laugh"]
            )
        
        return word
    
    return word[0]


if __name__ == "__main__":
    sentence1: str = "hi po, sero!!, ustah kah na pfoe? akckuh 2h! labkckyouh!! eos po"

    tokenized =  ['hi', 'po', ',', 'sero', '!', '!', ',', 'ustah', 'kah', 'na', 'pfoe', '?', 'akckuh', '2h', '!', 'ilabkckyouh', '!', '!', 'eows', 'po', 'jejejejejejejejejje']
    choices = {
        "ako": ["aQcKuHh", "aQ"],
        "hello": ["eowz", "eEoW"],
        "love": ["lab"],
        "night": ["nayt"],
        "po": ["pfHoE", "phow", "pfoe", "poeh"],
        "to": ["2h"],
        "you": ["yuHh", "qcKyuH", "qCkyOuHh"],
        "cityhall": ["7hol"]
    }

    # token = tokenization(sentence = "like \"3owz\" its not a part of any!! ")
    # print(token)


    # matches = best_jejemon_match(
    #     word="pohw",
    #     choices=choices
    # )

    # print(matches)

    # matches = split_and_normalize_jejemon(
    #     word = "labkckyouh",
    #     choices = choices
    # )

    # print(matches)

    matches = best_normal_match(
        word="and",
        choices=["end","and"]
    )

    print(matches)
    """
    TODO: 
    * 1. Improve tokenization about identifying special characters within word or sentence
    """