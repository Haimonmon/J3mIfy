import re
from typing import List, Dict

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


def remove_unnecessary_punctutation(sentence: str, substitutes: Dict[str, Dict[str, List[str]]]) -> str:
     # * Real Punctuations
     punctuations: List[str] = substitutes["punctuations"]
      
     sentence = apply_sandwich_ruling(sentence = sentence, allowed = allowed_punctuations, not_allowed = punctuations)
     return sentence
     
     
def detect_punctuation(sentence: str, punctuation_chars: List[str], detected_characters: List[str]) -> List[str]:
    char_positions = {char: [m.start() for m in re.finditer(re.escape(char), sentence)] for char in punctuation_chars}

    punctuation_set = set()
    punct_group = "".join(re.escape(p) for p in punctuation_chars)
    clusters = list(re.finditer(rf"[{punct_group}]+", sentence))

    for cluster in clusters:
        # print(cluster)
        start, end = cluster.start(), cluster.end()
        if start > 0 and re.match(r'\w', sentence[start - 1]) and (end == len(sentence) or not re.match(r'\w', sentence[end])):
            punctuation_set.update(range(start, end))

    results = []
    char_index_tracker = {char: 0 for char in punctuation_chars}

    for char in detected_characters:
        if char in punctuation_chars:
            idx_list = char_positions[char]
            char_idx = char_index_tracker[char]
            #* print(char)
            if char_idx < len(idx_list):
                pos = idx_list[char_idx]
                label = "punctuation" if pos in punctuation_set else "not punctuation"
                results.append(label)
                char_index_tracker[char] += 1
            else:
                results.append("not punctuation")
        else:
            results.append("not punctuation")

    return results
    
    
if __name__ == "__main__":
      sentence = "! have a $!n????? and mama and yah and do'g hahahahahahahaha!!!!"
      punctuation = ["?","!"]
      detected_characters = ["!","!"]
      
      results = detect_punctuation(sentence, punctuation, detected_characters)
      
      for i, status in enumerate(results, start=1):
          print(f"{i}. {status}")