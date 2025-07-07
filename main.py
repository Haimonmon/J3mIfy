import json
import re

with open("jejemon.json", "r", encoding="utf-8") as f:
    data = json.load(f)

jejemon_dict = {k.lower(): v.lower() for k, v in data["dictionary"].items()}
subs = data["fallback_rules"]["substitutions"]
strip_trailing = data["fallback_rules"]["strip_trailing"]
remove_repeats = data["fallback_rules"]["remove_repeated_letters"]
custom_subs = data["fallback_rules"]["custom_substitutions"]

def fallback_pattern(word):
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

def normalize_jejemon(tokens: str):
    normalized = []
    for word in tokens:
        cleaned = word.lower()
        if cleaned in jejemon_dict:
            normalized.append(jejemon_dict[cleaned])
        else:
            normalized.append(fallback_pattern(cleaned))
    return " ".join(normalized)

def simple_word_tokenize(text):
    pattern = re.compile(r"\w+(?:-\w+)*|'[a-z]+|[^\w\s]", re.IGNORECASE)
    return pattern.findall(text)

def main():
    text = input("Enter Jejemon text: ")
    tokens = simple_word_tokenize(text)
    print("Original Tokens:", tokens)
    print("Normalized:", normalize_jejemon(tokens))

if __name__ == "__main__":
    main()