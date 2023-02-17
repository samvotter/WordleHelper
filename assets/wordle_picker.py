from random import choice
from os import path
from assets.wordle_word import WordleLetter


class DictionaryReader:

    def __init__(self, filepath: str):
        if not path.exists(filepath):
            raise RuntimeError(f"Could not find the provided filepath: {filepath}")
        self.filepath = filepath

    def read(self) -> list[str]:
        with open(self.filepath, 'r') as f:
            return f.read().upper().splitlines()


class WordPicker:

    def __init__(self, words: list[str]):
        self.words = words

    def random_word(self):
        return choice(self.words)

    def reset_words(self, words: list[str]):
        self.words = words


class TargetWord:

    def __init__(self, word: str):
        self._value = word

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_val: str):
        if not isinstance(new_val, str):
            raise TypeError("TargetWords must be strings")
        self._value = new_val

    def compare(self, word: str) -> WordleLetter:
        if len(word) != len(self._value):
            raise ValueError("Comparison word is not the same size as the target word.")
        for idx, letter in enumerate(word):
            state = 0
            if letter in self.value:
                state += 1
            if letter == self._value[idx]:
                state += 1
            yield WordleLetter(letter, idx, state)
