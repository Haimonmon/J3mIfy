import json
import re

# Load JSON dictionary and fallback rules
with open("jejemon.json", "r", encoding="utf-8") as f:
    data = json.load(f)

jejemon_dict = {k.lower(): v.lower() for k, v in data["dictionary"].items()}
subs = data["fallback_rules"]["substitutions"]
strip_trailing = data["fallback_rules"]["strip_trailing"]
remove_repeats = data["fallback_rules"]["remove_repeated_letters"]

def fallback_pattern(word):
    word = word.lower()

    # Remove long repeated letters
    if remove_repeats:
        word = re.sub(r'(.)\1{2,}', r'\1', word)

    # Replace leetspeak
    for k, v in subs.items():
        word = word.replace(k, v)

    word = re.sub(rf"[{''.join(strip_trailing)}]+$", "", word)

    return word

def normalize_jejemon(tokens):
    normalized = []
    for word in tokens:
        cleaned = word.lower()
        if cleaned in jejemon_dict:
            normalized.append(jejemon_dict[cleaned])
        else:
            normalized.append(fallback_pattern(cleaned))
    return normalized

def simple_word_tokenize(text):
    return re.findall(r"\b\w+\b|'\w+", text.lower())

def main():
    text = input("Enter Jejemon text: ")
    tokens = simple_word_tokenize(text)
    print("Original Tokens:", tokens)
    print("Normalized:", normalize_jejemon(tokens))

if __name__ == "__main__":
    main()