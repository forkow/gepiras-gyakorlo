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

PHRASES_DIFFICULTY_TABLE = {
    Difficulty.EASY: (1, 10),
    Difficulty.MEDIUM: (2, 15),
    Difficulty.HARD: (3, 20),
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
                if index >= len(word) or word[index] != char:
                    print("\x1b[0;31m", end="")
                else:
                    print("\x1b[0;32m", end="")
                typed_in += char
                index += 1
                print(char, end="")
                sys.stdout.flush()
        time_to_type = time.time() - typing_start
        time_pad = padding - len(typed_in)
        typed.append((word, time_to_type, skipped))
        time_color = "\x1b[0;31m" if skipped else "\x1b[0;32m"
        print(f'{time_color}    {round(time_to_type, 1):>{time_pad}}mp', end="")
        print("\x1b[0m")
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


def start_text(difficulty: Difficulty):
    phrases = get_random_phrases(*PHRASES_DIFFICULTY_TABLE[difficulty])
    padding_left = 5
    padding_right = len(max(phrases, key=lambda p: len(p[0]))[0]) + 5
    typed = []
    for phrase, in phrases:
        print(f"{' '*padding_left}{phrase}")
        print(f"{' '*padding_left}{'-'*len(phrase)}")
        print(' '*padding_left, end="")
        sys.stdout.flush()
        typed_in = ""
        index = 0
        skipped = False
        typing_start = time.time()
        while typed_in != phrase:
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
                if index >= len(phrase) or phrase[index] != char:
                    print("\x1b[0;31m", end="")
                else:
                    print("\x1b[0;32m", end="")
                typed_in += char
                index += 1
                print(char, end="")
                sys.stdout.flush()
        time_to_type = time.time() - typing_start
        time_pad = padding_right - len(typed_in)
        word_count = phrase.count(' ') + 1
        words_per_minute = word_count / (time_to_type / 60)
        typed.append((phrase, time_to_type, words_per_minute, skipped))
        time_color = "\x1b[0;31m" if skipped else "\x1b[0;32m"
        print(f"{time_color}{round(time_to_type, 1):>{time_pad}}")
        print("\x1b[0m")
    print()
    total_time = sum([time for _, time, _, _ in typed])
    skipped = len([1 for _, _, _, skipped in typed if skipped])
    if total_time >= 60:
        print(f"Teljes idő: {floor(total_time / 60)}p {floor(total_time%60)}mp")
    else:
        print(f"Teljes idő: {round(total_time, 1)}mp")
    words_per_minute_all = [wpm for _, _, wpm, skipped in typed if not skipped]
    if len(words_per_minute_all):
        wpm_average = sum(words_per_minute_all)/len(words_per_minute_all)
        print(f"Sebesség: {round(wpm_average, 1)} szó/perc")
    skipped = len([1 for _, _, _, skipped in typed if skipped])
    print(f"Kihagyott: {skipped}")


def get_random_words(min_length: int, max_length: int, count: int) -> list:
    cursor = DB.cursor()
    cursor.execute(f"SELECT * FROM words WHERE length <= {max_length} AND length >= {min_length} ORDER BY random() LIMIT {count}")
    return cursor.fetchall()


def get_random_phrases(difficulty: int, count: int) -> list:
    cursor = DB.cursor()
    cursor.execute(f"SELECT text FROM phrases WHERE difficulty = {difficulty} ORDER BY RANDOM() LIMIT {count}")
    return cursor.fetchall()
