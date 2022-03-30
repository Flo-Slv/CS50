from cs50 import get_string


# Main function.
def main():
    text = get_string("Text: ")

    # Count number of letters.
    l = count_letters(text)

    # Count number of words.
    w = count_words(text)

    # Count number of sentences.
    s = count_sentences(text)

    # Average letters per 100 words.
    L = (l / float(w)) * 100

    # Average sentences per 100 words.
    S = (s / float(w)) * 100

    # Formula.
    index = round(0.0588 * float(L) - 0.296 * float(S) - 15.8)

    # Results.
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


# Function letters.
def count_letters(text):
    letters = 0

    for i in range(0, len(text)):
        char = ord(text[i])

        if (char >= 65 and char <= 90) or (char >= 97 and char <= 122):
            letters += 1

    return letters


# Function words.
def count_words(text):
    # Text is starting with one word.
    words = 1
    space = chr(32)

    for i in range(0, len(text)):
        if text[i] == space:
            words += 1

    return words


# Funtion sentences.
def count_sentences(text):
    sentences = 0

    for i in range(0, len(text)):
        char = ord(text[i])

        if char == 33 or char == 46 or char == 63:
            sentences += 1

    return sentences


main()
