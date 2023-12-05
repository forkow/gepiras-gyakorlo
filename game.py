import sqlite3
import sys
import time

from gametypes import Mode, Difficulty
from math import floor

DB = sqlite3.connect("data.db")

WORDS_DIFFICULTY_TABLE = {
    Difficulty.EASY: (0, 6, 10),
    Difficulty.MEDIUM: (7, 11, 20),
    Difficulty.HARD: (12, 24, 25),
}

def start_words(difficulty: Difficulty):
    words = get_random_words(*WORDS_DIFFICULTY_TABLE[difficulty])
    padding = len(max(words, key=lambda w: len(w[0]))[0]) + 3
    typed = []
    for word, length in words:
        print(f"{word:>{padding}}   |   \x1b[0;34m", end="")
        sys.stdout.flush()
        typed_in = ""
        index = 0
        skipped = False
        print("\x1b[0;32m", end="")
        typing_start = time.time()
        while typed_in != word:
            char = sys.stdin.read(1)
            if ord(char) == 127 and index != 0: # DEL
                print(chr(8), end="") # Ctrl-H (backspace)
                print(' ', end="") # clear previous character
                print(chr(8), end="") # go back again
                sys.stdout.flush()
                typed_in = typed_in[:-1]
                index -= 1
                continue
            if ord(char) == ord('\n'):
                skipped = True
                break
            if char.isprintable():
                typed_in += char
                index += 1
                print(char, end="")
                sys.stdout.flush()
        time_to_type = time.time() - typing_start
        time_pad = padding - len(typed_in)
        typed.append((word, time_to_type, skipped))
        print(f'\x1b[0m    {round(time_to_type, 1):>{time_pad}}mp')
    print()
    total_time = sum([time for _, time, _ in typed])
    if total_time != 0:
        chars_per_second = sum([len(word) for word, _, skipped in typed if not skipped]) / total_time
    else:
        chars_per_second = 0
    skipped = len([1 for _, _, skipped in typed if skipped])
    if total_time >= 60:
        print(f"Teljes idő: {floor(total_time / 60)}p {floor(total_time%60)}mp")
    else:
        print(f"Teljes idő: {round(total_time, 1)}mp")
    print(f"Sebesség: {round(chars_per_second,1)} betu/mp")
    print(f"Kihagyott: {skipped}")


def get_random_words(min_length: int, max_length: int, count: int) -> list:
    cur = DB.execute(
        f"SELECT * FROM words WHERE length <= {max_length} AND length >= {min_length} ORDER BY random() LIMIT {count}"
    )
    rows = cur.fetchall()
    return rows
