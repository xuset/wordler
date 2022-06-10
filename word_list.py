def load_words(file):
    return [line for line in (line.strip() for line in file) if line.isalpha()]


answers = load_words(open("wordle_oracle.txt", "r"))

dictionary = load_words(open("wordle_dictionary.txt"))