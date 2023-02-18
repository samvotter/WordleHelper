import dataclasses
import re

from assets.wordle_word import WordleLetter
from assets.states import LetterState


@dataclasses.dataclass()
class WordleLetterRegex:
    pattern = ""
    exclude: set = dataclasses.field(default_factory=set)

    def exclude_letter(self, letter: str):
        self.exclude.add(letter)
        self.refresh_pattern()

    def refresh_pattern(self):
        str_exclude = "".join([letter for letter in self.exclude])
        self.pattern = r"[^\W" + f"{str_exclude}]"


class WordleWordREGEX:

    def __init__(self, length=5):
        """
        WordleWordRegex is a a regex pattern combining what letters a word MUST HAVE as well as the which letters it
            CANNOT HAVE, and in what position
        :param length: int - how long are the words this regex is suppose to describe?
        """
        self.letters = [WordleLetterRegex() for _ in range(length)]
        self.pattern = ""
        self.must_have = set()

    def incorporate_guess_letter(self, guess_letter: WordleLetter) -> None:
        if guess_letter.state is LetterState.GREY:
            self.consider_grey(guess_letter)
        elif guess_letter.state is LetterState.YELLOW:
            self.consider_yellow(guess_letter)
        elif guess_letter.state is LetterState.Green:
            self.consider_green(guess_letter)
        raise ValueError(f"{guess_letter.letter} has an unknown state! {guess_letter.state}")

    def consider_grey(self, guess_letter: WordleLetter):
        # letter is not in the word
        for letter in filter(lambda word_letter: word_letter.state is not LetterState.GREEN, self.letters):
            letter.exclude_letter(guess_letter.letter)

    def consider_yellow(self, guess_letter: WordleLetter):
        # letter is not in this position
        self.must_have.add(guess_letter.letter)
        self.letters[guess_letter.position].exclude_letter(guess_letter.letter)

    def consider_green(self, guess_letter: WordleLetter):
        self.letters[guess_letter.position].pattern = guess_letter.letter

    def compile_pattern(self):
        must_have = "".join(r"(?=.*" + f"{letter})" for letter in self.must_have)
        excludes = "".join([letter.pattern for letter in self.letters])
        return re.compile(must_have + excludes)
