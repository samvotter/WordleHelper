import re


class WordleLetter:

    def __init__(self, value, place, state):
        self.value = value
        self.place = place

        self.state = state
        self._state_dict = {
            0: "Not in the word",
            1: "Not in this position",
            2: "Match"
        }


class WordleLetterREGEX:

    def __init__(self):
        self.exclude = set()
        self.pattern_str = ""
        self.pattern = None
        self.fixed = False

    def exclude_letter(self, letter: str):
        self.exclude.add(letter)
        self.compile_pattern()

    def compile_pattern(self):
        str_exclude = "".join([letter for letter in self.exclude])
        self.pattern_str = r"[^\W" + f"{str_exclude}]"
        self.pattern = re.compile(self.pattern_str)

    def set_pattern(self, pattern: str):
        self.pattern_str = pattern
        self.pattern = re.compile(pattern)
        self.fixed = True


class WordleWordREGEX:

    def __init__(self, length=5):
        self.letters = [WordleLetterREGEX() for i in range(length)]
        self.pattern_str = None
        self.pattern = None

        self._must_have = set()

        self._state_dict = {
            0: self._state_0_exclude,
            1: self._state_1_exclude,
            2: self._state_2_exclude
        }

    def incorporate_wordleletter(self, letter: WordleLetter):
        self._state_dict[letter.state](letter)

    def _state_0_exclude(self, letter: WordleLetter):
        # letter is not in the word
        for letter_reg in self.letters:
            if not letter_reg.fixed:
                letter_reg.exclude_letter(letter.value)

    def _state_1_exclude(self, letter: WordleLetter):
        # letter is not in this position
        if not self.letters[letter.place].fixed:
            self.letters[letter.place].exclude_letter(letter.value)
        self._must_have.add(letter.value)

    def _state_2_exclude(self, letter: WordleLetter):
        # letter is in this position
        self.letters[letter.place].set_pattern(letter.value)

    def compile_pattern(self):
        self.pattern_str = "".join([letter.pattern_str for letter in self.letters])
        self.pattern = re.compile(self.pattern_str)

    def scrub_must_haves(self, results: list) -> list[str]:
        if not self._must_have:
            return results

        def must_have(word: str) -> bool:
            return all([letter in word for letter in self._must_have])

        return list(filter(must_have, results))
