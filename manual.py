"""
This module represents manually triggering game events by directly prompting the user for real-time inputs
"""

from assets.wordle_picker import DictionaryReader, WordPicker, TargetWord
from assets.wordle_word import WordleWordREGEX
from assets.string_analyzer import TokenAnalyzer


class ManualGame:

    def __init__(self, filepath: str = None, dictionary: list[str] = None, wordsize: int = 5, target: str = None):
        """
        ManualGame prompts the user for real-time manual inputs to play the game of Wordle

        :param filepath: A filepath to a dictionary of words
        :param dictionary: A pre-composed dictionary of words
        :param wordsize: The size of words. By default, words are set to a length of 5
        """
        self._wordsize = wordsize
        if filepath:
            dictionary = DictionaryReader(filepath).read()
        if dictionary:
            dictionary = WordPicker(dictionary)
        if not self._sanitize_dictionary(dictionary.words):
            raise RuntimeError("The provided dictionary of words has words on inconsistent lengths!")
        self.dictionary = dictionary
        if not target:
            target = self.dictionary.random_word()
        self.target = TargetWord(target)

        # these attributes are used to cheat at the game
        self.culler = WordleWordREGEX()
        self.token_analyzer = TokenAnalyzer(self.dictionary.words)
        self.token_analyzer.fill_table()
        self.token_analyzer.score_tokens()

    @property
    def wordsize(self):
        return self._wordsize

    @wordsize.setter
    def wordsize(self, new_value):
        if not isinstance(new_value, int):
            raise TypeError("Wordsize must be a positive int.")
        if new_value <= 0:
            raise ValueError("Wordsize must be a positive int.")
        self._wordsize = new_value

    def compare(self, word: str):
        for result in self.target.compare(word):
            yield result

    def _sanitize_dictionary(self, dictionary: list[str]):
        return all([self._sanitize_word(word) for word in dictionary])

    def _sanitize_word(self, word: str):
        if not word.isalpha():
            print(f"{word} is not a word.")
            return False
        if len(word) != self.wordsize:
            print(f"{word} is not {self.wordsize} letters.")
            return False
        return True

    def _sanitize_target(self, word: str):
        if self._sanitize_word(word):
            return word in self.dictionary
        return False

    def _manual_prompt(self):
        return input(f"Enter a {self.wordsize} letter word:").upper()

    def solicit_word(self):
        word = self._manual_prompt()
        while not self._sanitize_word(word):
            word = self._manual_prompt()
        return [letter for letter in self.compare(word)]

    def play(self):
        print(f"Best word: {self.token_analyzer.best_words()}")
        possible_words = self.dictionary.words
        guess_result = self.solicit_word()
        while "".join(letter.value for letter in guess_result) != self.target.value:
            for letter in guess_result:
                print(f"{letter.value}: {letter.state}", end=" ")
                self.culler.incorporate_wordleletter(letter)
            print()
            self.culler.compile_pattern()
            possible_words = list(filter(self.culler.pattern.findall, possible_words))
            possible_words = self.culler.scrub_must_haves(possible_words)
            self.token_analyzer.empty_tables()
            self.token_analyzer.fill_table(possible_words)
            self.token_analyzer.score_tokens(possible_words)
            print(f"Best word: {self.token_analyzer.best_words()}")
            guess_result = self.solicit_word()

        print("YOU WIN!!!")


thing = ManualGame(filepath=r"assets\5_letter_words.txt")
thing.play()




