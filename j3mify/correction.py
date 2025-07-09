import re
from typing import List


def tokenization(sentence: str) -> List[str]:
    """ Separates word by word and put it in an array"""
    pattern = re.compile(r"\w+(?:-\w+)*|'[a-z]+|[^\w\s]", re.IGNORECASE)
    return pattern.findall(sentence)


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


if __name__ == "__main__":  
    # ! DISCLAIMER: Nahanp kolang sa internet 💀👌✨
    word = "😜😛🥰Anong masarap na KAPE@ edi KAPEling ka samahan mopa ng DECAF DECAFapakawalan mamahalin kita i love my life because my life is you🤪😘😂🤣" 

    print(tokenization(sentence = word))

    """
    TODO: 
    * 1. Improve tokenization about identifying special characters within word or sentence
    """