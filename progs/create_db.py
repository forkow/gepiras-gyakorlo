import os
import sqlite3
import keycalc

from os import path
from sys import argv

if len(argv) < 2:
    print(f"usage: {argv[0]} <data_dir> [db_path=data.db]")
    exit(1)

DATA_DIR = argv[1]
DB_PATH = (argv[2] if len(argv) >= 3 else "data.db")

def main():
    db = sqlite3.connect(DB_PATH)
    create_words_table(db)
    create_phrases_table(db)
    db.commit()
    db.close()

def load_words(path):
    words = []
    with open(path, "r") as words_file:
        for word in words_file.read().splitlines():
            words.append(word)
    return words

def create_words_table(db):
    words = load_words(path.join(DATA_DIR, "hu.txt"))
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS words")
    cursor.execute("CREATE TABLE words(word TEXT, length INTEGER)")
    for word in words:
        length = round(keycalc.calculate_word_length(word))
        cursor.execute("INSERT INTO words VALUES (?,?)", (word, length))

def create_phrases_table(db):
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS phrases")
    cursor.execute("CREATE TABLE phrases(text TEXT, difficulty INTEGER)")
    for difficulty in range(1, 4):
        with open(path.join(DATA_DIR, f"ph{difficulty}.txt")) as phrases_file:
            for phrase in phrases_file.read().splitlines():
                cursor.execute("INSERT INTO phrases VALUES (?,?)", (phrase, difficulty))

if __name__ == "__main__":
    main()
