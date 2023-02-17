"""
This module represents manually triggering game events by directly prompting the user for real-time inputs
"""
import re

from assets.wordle_picker import DictionaryReader, WordPicker, TargetWord
from assets.wordle_word import WordleWordREGEX, WordleLetter
from assets.string_analyzer import TokenAnalyzer
from assets.states import LETTER_STATES


class Game:

    _wordsize: int

    def __init__(self, filepath: str = r"5_letter_words.txt", dictionary: list[str] = None, wordsize: int = 5, target: str = None):
        """
        ManualGame prompts the user for real-time manual inputs to play the game of Wordle

        :param filepath: A filepath to a dictionary of words
        :param dictionary: A pre-composed dictionary of words
        :param wordsize: The size of words. By default, words are set to a length of 5
        """
        self.wordsize = wordsize
        if filepath:
            dictionary = DictionaryReader(filepath).read()
        if dictionary:
            dictionary = WordPicker(dictionary)
        if not self._sanitize_dictionary(dictionary.words):
            raise RuntimeError("The provided dictionary of words has words on inconsistent lengths!")
        self.dictionary = dictionary

        # the target is determined by the type of game being played
        self.target = None

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

    def compare(self, word: str, target: str = None):
        if target is None:
            target = self.target
        for result in target.compare(word):
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

    def _manual_prompt_str_letter(self):
        return input(f"Enter a {self.wordsize} letter word:").upper()

    def _manual_prompt_wordle_letters(self):
        word = []
        idx = 0
        pattern = r"^(\w)\s*(\d)"
        comp_pattern = re.compile(pattern)
        while len(word) < self.wordsize:
            letter = input(f"Enter a letter followed by its state:").upper()
            letter_result = comp_pattern.findall(letter)
            if letter_result:
                letter_val = letter_result[0][0]
                letter_state = int(letter_result[0][1])
                if int(letter_state) not in LETTER_STATES:
                    print(f"Invalid response: {letter_result[0]}\n"
                          f"Expecting:\n"
                          f"\t'a0' meaning A {LETTER_STATES[0]}\n"
                          f"\t'A1' meaning A {LETTER_STATES[1]}\n"
                          f"\t'A 2' meaning A {LETTER_STATES[2]}\n"
                          f"Try again . . .")
                else:
                    word.append(WordleLetter(letter_val, idx, letter_state))
                    idx += 1
        return word

    def solicit_text_word(self):
        word = self._manual_prompt_str_letter()
        while not self._sanitize_word(word):
            word = self._manual_prompt_str_letter()
        return [letter for letter in self.compare(word)]

    def determine_best_words(self, dictionary: list[str], n_results: int = 1):
        self.culler.compile_pattern()
        possible_words = list(filter(self.culler.pattern.findall, dictionary))
        possible_words = self.culler.scrub_must_haves(possible_words)
        self.token_analyzer.empty_tables()
        self.token_analyzer.fill_table(possible_words)
        self.token_analyzer.score_tokens(possible_words)
        best_words = self.token_analyzer.best_words(n_results)
        return possible_words, best_words

    def random_word(self):
        target = self.dictionary.random_word()
        self.target = TargetWord(target)
        print(f"Best word: {self.token_analyzer.best_words()}")
        possible_words = self.dictionary.words
        guess_result = self.solicit_text_word()
        guess_word = "".join([letter.value for letter in guess_result])
        while guess_word != self.target.value:
            for letter in guess_result:
                print(f"{letter.value}: {letter.state}", end=" ")
                self.culler.incorporate_wordleletter(letter)
            print()
            possible_words, best_word = self.determine_best_words(possible_words)
            print(f"Best word: {best_word}")
            guess_result = self.solicit_text_word()
            guess_word = "".join([letter.value for letter in guess_result])

        print("YOU WIN!!!")

    def unknown_word(self):
        possible_words = self.dictionary.words
        print(f"Total words: {len(possible_words)}")
        possible_words, best_word = self.determine_best_words(dictionary=possible_words)
        print(f"Possible words: {len(possible_words)}, {possible_words}")
        print(f"Best word: {best_word}")
        guess_result = self._manual_prompt_wordle_letters()
        guess_word = "".join([letter.value for letter in guess_result])
        print(f"guess word: {guess_word}")
        while list(best_word.values())[0] < 1:
            for letter in guess_result:
                self.culler.incorporate_wordleletter(letter)
            possible_words, best_word = self.determine_best_words(possible_words)
            print(f"Possible words: {possible_words}")
            print(f"Best word: {best_word}")
            guess_result = self._manual_prompt_wordle_letters()
            guess_word = "".join([letter.value for letter in guess_result])
            print(f"guess word: {guess_word}")
        print("YOU WIN!!!")