from enum import Enum


class Mode(Enum):
    WORDS = 1
    TEXT = 2
    LONGTEXT = 3

    def to_text(self):
        if self == Mode.WORDS:
            return "szavak"
        elif self == Mode.TEXT:
            return "szoveg"
        elif self == Mode.LONGTEXT:
            return "hosszu szoveg"


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

    def to_text(self):
        if self == Difficulty.EASY:
            return "konnyu"
        elif self == Difficulty.MEDIUM:
            return "kozepes"
        elif self == Difficulty.HARD:
            return "nehez"
