from math import sqrt
from itertools import islice

_KEY_MAP = {
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

def _to_key(key: str) -> str:
    if key == '?' or key == ';':
        return ','
    elif key == ':':
        return '.'
    elif key == '_' or key == '*':
        return '-'
    return key.lower()

def _window(seq, n=2):
    """Returns a sliding window (of width n) over data from the iterable"""
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def _key_side(key: str) -> int:
    if key in "012345qwertasdfgíyxcv":
        return 0
    elif key in "6789öüózuiopőúhjkléáűbnm,.-":
        return 1

def _calculate_key_distance(fromm: str, to: str, last_keys_on_sides: (str, str)) -> float:
    if _key_side(fromm) == _key_side(to):
        dist_x = abs(_KEY_MAP[fromm][0] - _KEY_MAP[to][0])
        dist_y = abs(_KEY_MAP[fromm][1] - _KEY_MAP[to][1])
    else:
        fromm = last_keys_on_sides[_key_side(to)]
        dist_x = abs(_KEY_MAP[fromm][0] - _KEY_MAP[to][0])
        dist_y = abs(_KEY_MAP[fromm][1] - _KEY_MAP[to][1])
    return sqrt(dist_x ** 2 + dist_y ** 2)

def calculate_word_length(word: str, last_letter: str = None) -> int:
    if last_letter:
        word = last_letter + word

    total_distance = 0
    last_keys_on_sides = ["f", "j"]
    for (char1, char2) in _window(word):
        total_distance += _calculate_key_distance(_to_key(char1), _to_key(char2), last_keys_on_sides)
        key2_side = _key_side(_to_key(char2))
        last_keys_on_sides[key2_side] = _to_key(char2)
    return total_distance
