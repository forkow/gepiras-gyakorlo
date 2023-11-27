from enum import Enum


class Mode(Enum):
    WORDS = 1
    TEXT = 2
    LONGTEXT = 3

    def to_text(self):
        if self == Mode.WORDS:
            return "Szavak"
        elif self == Mode.TEXT:
            return "Szöveg"
        elif self == Mode.LONGTEXT:
            return "Hosszú szöveg"


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

    def to_text(self):
        if self == Difficulty.EASY:
            return "Könnyű"
        elif self == Difficulty.MEDIUM:
            return "Közepes"
        elif self == Difficulty.HARD:
            return "Nehéz"
