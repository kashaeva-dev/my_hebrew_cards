import unicodedata


def only_letters(word):
    new_word = ""
    for letter in word:
        if letter == " ":
            new_word += letter
        elif unicodedata.name(letter).split()[1] == 'LETTER':
            new_word += letter
    return new_word