import j3mify as jeje

def main():
    """ main terminal 💀👌🥐✨ """
    text = input("Enter Jejemon text: ")
    tokens = jeje.tokenization(text)
    print("Original Tokens:", tokens)
    print("Normalized:", jeje.normalization(tokens))

if __name__ == "__main__":
    main()