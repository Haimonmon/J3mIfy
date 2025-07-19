import re
from typing import List

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
      sentence = "may ! H1llo! $!n!!? okok bruhh?"
      punctuation = ["?","!"]
      detected_characters = ["@"]
      
      results = detect_punctuation(sentence, punctuation, detected_characters)
      
      for i, status in enumerate(results, start=1):
          print(f"{i}. {status}")