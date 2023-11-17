from itertools import islice
from math import ceil, sqrt
import sqlite3
from hyphen import Hyphenator

hyphenator = Hyphenator("hu_HU")

KEY_MAP = {
    "a": (3, 0),
    "s": (2, 0),
    "d": (1, 0),
    "f": (0, 0),
    "g": (-1, 0),

    "q": (3.5, 1),
    "w": (2.5, 1),
    "e": (1.5, 1),
    "r": (0.5, 1),
    "t": (-0.5, 1),

    "0": (5, 2),
    "1": (4, 2),
    "2": (3, 2),
    "3": (2, 2),
    "4": (1, 2),
    "5": (0, 2),

    "í": (3.5, -1),
    "y": (2.5, -1),
    "x": (1.5, -1),
    "c": (0.5, -1),
    "v": (-0.5, -1),


    "ű": (5, 0),
    "á": (4, 0),
    "é": (3, 0),
    "l": (2, 0),
    "k": (1, 0),
    "j": (0, 0),
    "h": (-1, 0),

    "ú": (5.5, 1),
    "ő": (4.5, 1),
    "p": (3.5, 1),
    "o": (2.5, 1),
    "i": (1.5, 1),
    "u": (0.5, 1),
    "z": (-0.5, 1),

    "6": (0, 2),
    "7": (1, 2),
    "8": (2, 2),
    "9": (3, 2),
    "ö": (4, 2),
    "ü": (5, 2),
    "ó": (6, 2),

    "Shift": (5.5, -1),
    "-": (4.5, -1),
    ".": (3.5, -1),
    ",": (2.5, -1),
    "m": (1.5, -1),
    "n": (0.5, -1),
    "b": (-0.5, -1),
}


def to_key(key: str) -> str:
    if key == '?' or key == ';':
        return ','
    elif key == ':':
        return '.'
    elif key == '_' or key == '*':
        return '-'
    return key.lower()


def load_words(word_file: str) -> list[str]:
    words = []
    with open(word_file, "r") as file:
        for word in file.readlines():
            words.append(word.strip())
    return words


def is_valid_word(word: str) -> bool:
    if word.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-')):
        return False
    if word.endswith('-'):
        return False
    for char in word:
        if (to_key(char) not in KEY_MAP.keys()) or char in "?!.":
            return False
    return True and not word.startswith('-')


def window(seq, n=2):
    """Returns a sliding window (of width n) over data from the iterable"""
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def key_side(key: str) -> int:
    if key in "012345qwertasdfgíyxcv":
        return 0
    elif key in "6789öüózuiopőúhjkléáűbnm,.-":
        return 1


def calculate_key_distance(fromm: str, to: str, last_keys_on_sides: (str, str)) -> float:
    to_side = key_side(to)
    if key_side(fromm) == key_side(to):
        dist_x = abs(KEY_MAP[fromm][0] - KEY_MAP[to][0])
        dist_y = abs(KEY_MAP[fromm][1] - KEY_MAP[to][1])
    else:
        fromm = last_keys_on_sides[to_side]
        dist_x = abs(KEY_MAP[fromm][0] - KEY_MAP[to][0])
        dist_y = abs(KEY_MAP[fromm][1] - KEY_MAP[to][1])
    return sqrt(dist_x ** 2 + dist_y ** 2)


def calculate_word_length(word: str, last_letter: str = None) -> int:
    if last_letter:
        word = last_letter + word

    total_distance = 0
    last_keys_on_sides = ["f", "j"]
    for (char1, char2) in window(word):
        total_distance += calculate_key_distance(to_key(char1), to_key(char2), last_keys_on_sides)
        key2_side = key_side(to_key(char2))
        last_keys_on_sides[key2_side] = to_key(char2)
    return total_distance


def contains_swear(word: str) -> bool:
    bad = [
        "fasz",
        "picsa",
        "picsá",
        "geci",
        "kurva",
        "kurvá",
        "idióta",
        "idiótá",
        "agyhalott",
        "segg",
        "pénis",
        "anyád",
        "aberrá",
        "bassz",
        "basz",
        "sperm",
        ]
    for b in bad:
        if b in word:
            return True
    return False


def syll_join(sylls: list[str]) -> str:
    prefix_hyphen = False
    result = ""
    for syll in sylls:
        if prefix_hyphen:
            result += '-'
            prefix_hyphen = False
        if syll == '-':
            prefix_hyphen = True
        else:
            result += syll
        result += '-'
    return result

db = sqlite3.connect("../words.db")
words = load_words("hu.txt")

db.execute("CREATE TABLE words(word TEXT, length REAL, hyphenated TEXT)")

for word in words:
    if not is_valid_word(word) or contains_swear(word):
        continue
    hyphenated = syll_join(hyphenator.syllables(word))
    length = round(calculate_word_length(word))
    db.execute(f"INSERT INTO words VALUES (?,?,?)", (word, length, hyphenated))

db.commit()
db.close()
