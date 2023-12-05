from gametypes import Mode, Difficulty
import sqlite3
import sys


DB = sqlite3.connect("data.db")

WORDS_DIFFICULTY_TABLE = {
    Difficulty.EASY: (0, 6, 10),
    Difficulty.MEDIUM: (7, 10, 20),
    Difficulty.HARD: (12, 24, 25),
}


def start_words(difficulty: Difficulty):
    words = get_random_words(*WORDS_DIFFICULTY_TABLE[difficulty])
    padding = len(max(words, key=lambda w: len(w[0]))[0]) + 3

    # need this to be able to `continue` from the inner while loop
    outer_continue = False
    
    for word, length, hyphenated, syllable_count in words:
        if outer_continue:
            outer_continue = False
            continue
        print(f"{word:>{padding}}   |   \x1b[0;34m", end="")
        sys.stdout.flush()
        typed_in = ""
        index = 0
        print("\x1b[0;32m", end="")
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
                outer_continue = True
                break
            if char.isprintable():
                typed_in += char
                index += 1
                print(char, end="")
                sys.stdout.flush()
        print('\x1b[0m')


def get_random_words(min_length: int, max_length: int, count: int) -> list:
    cur = DB.execute(
        f"SELECT * FROM words WHERE length <= {max_length} AND length >= {min_length} ORDER BY random() LIMIT {count}"
    )
    rows = cur.fetchall()
    return rows
