from gametypes import Mode, Difficulty
import atexit
import game
import signal
import sys
import termios
import tty


GAMETABLE = {
    Mode.WORDS: game.start_words,
    Mode.TEXT: game.start_text,
}

TERM_OLD_ATTRS = None


def main():
    with open("banner.txt", "r") as banner:
        print(banner.read())
    global TERM_OLD_ATTRS
    TERM_OLD_ATTRS = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin, when=termios.TCSANOW)
    sys.stdin.flush()

    mode = select_mode()
    difficulty = select_difficulty()

    print(f"Mód: {mode.to_text()}")
    print(f"Nehézség: {difficulty.to_text()}")
    print()

    GAMETABLE[mode](difficulty)


def select_mode() -> Mode:
    while True:
        print("Válassz módot")
        print(f"1) Szavak")
        print(f"2) Szöveg")
        try:
            choice = int(sys.stdin.read(1))
            if choice >= 1 and choice <= 2:
                print()
                return Mode(choice)
        except ValueError:
            continue


def select_difficulty() -> Difficulty:
    while True:
        print("Válassz nehézséget")
        print(f"1) Könnyű")
        print(f"2) Közepes")
        print(f"3) Nehéz")
        try:
            choice = int(sys.stdin.read(1))
            if choice >= 1 and choice <= 3:
                print()
                return Difficulty(choice)
        except ValueError:
            continue


def exit_handler():
    print("\x1b[0m")
    try:
        if TERM_OLD_ATTRS:
            termios.tcsetattr(sys.stdin, termios.TCSANOW, TERM_OLD_ATTRS)
        sys.stdin.flush()
        sys.stdout.flush()
    except:
        pass


def ctrl_c_handler(_sig, _frm):
    exit(0)


if __name__ == '__main__':
    atexit.register(exit_handler)
    signal.signal(signal.SIGINT, ctrl_c_handler)
    main()
