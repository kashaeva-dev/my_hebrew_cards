from django import template
import unicodedata
from itertools import accumulate

register = template.Library()


@register.filter()
def lookup(the_dict, key):
    return the_dict.get(key, '')


@register.filter()
def word_title(string):
    pattern = str(string[0]).lower()
    return string.replace(string[0], pattern)


@register.filter()
def price_format(price):
    return str('{0:,}'.format(int(price))).replace(",", " ")


@register.filter()
def pluralize_ru1(number, string):
    lst = string.split(",")
    if number % 10 == 1 and number % 100 != 11:
        return lst[0]
    elif number % 10 >= 2 and number % 10 <= 4 and number % 100 not in [11, 12, 13, 14]:
        return lst[1]
    else:
        return lst[2]


@register.filter()
def pluralize_ru2(number, string):
    lst = string.split(",")
    if number % 10 == 1 and number % 100 != 11:
        return lst[0]
    else:
        return lst[1]






@register.filter()
def letter_positions(verb):
    word = []
    for letter in verb:
        word.append(unicodedata.name(letter).split()[1])

    positions = []

    ipos = 0
    i = 0
    while i < len(word) - 1:
        if word[i] == 'LETTER':
            if word[i + 1] == 'POINT':
                positions.append(2)
                i += 2
                ipos += 1
            else:
                positions.append(1)
                i += 1
                ipos += 1
        else:
            positions[ipos - 1] += 1
            i += 1

    if word[-1] == 'LETTER':
        positions.append(1)

    return list(accumulate(positions))

@register.filter
def getSliceLetter1(positions):
    return ":".join(["0", str(positions[0])])

@register.filter
def getSliceLetter2(positions):
    return ":".join([str(positions[0]), str(positions[1])])

@register.filter
def getSliceLetter3(positions):
    return ":".join([str(positions[1]), str(positions[2])])

@register.filter
def getSliceLetter4(positions):
    return ":".join([str(positions[2]), str(positions[3])])


@register.filter
def getSliceLetter5(positions):
    if len(positions) == 5:
        return ":".join([str(positions[3]), str(positions[4])])


@register.filter
def getPlNounEnd(positions, number=2):
    return ":".join([str(positions[-(number + 1)]), '25'])


@register.filter
def getPlNounBegin(positions, number=2):
    return ":".join(['0', str(positions[-(number + 1)])])


@register.filter
def getWordFirst(words, sep=" "):
    return words.split(sep)[0]


@register.filter
def getWordSecond(words):
    return words.split()[1]


@register.filter
def getWordsNumber(words):
    return len(words.split())