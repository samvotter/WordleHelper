import dataclasses


@dataclasses.dataclass()
class CharacterOccurrenceTable:
    frequency: dict[str, int] = dataclasses.field(default_factory=dict, init=False)
    percent: dict[str, float] = dataclasses.field(default_factory=dict, init=False)

    def _calculate_percent(self):
        total = sum(self.frequency.values())
        if total == 0:
            return
        self.percent = {letter: value / total for letter, value in self.frequency}

    def count_frequency(self, tokens: set[str]):
        for token in tokens:
            for letter in token:
                self.frequency[letter] += 1
        self._calculate_percent()


@dataclasses.dataclass()
class TokenAnalyzer:

    tokens: set[str] = dataclasses.field(default_factory=set)

    def include_latter(self, letter: str) -> set[str]:
        return set(filter(lambda word: letter in word, self.tokens))

    def exclude_letter(self, letter: str) -> set[str]:
        return set(filter(lambda word: letter not in word, self.tokens))

    @staticmethod
    def score_tokens(tokens: set[str]) -> dict[str, float]:
        distribution = CharacterOccurrenceTable()
        distribution.count_frequency(tokens)
        return {token: sum([distribution.percent[letter] for letter in token]) for token in tokens}

    def best_words(self, tokens: set[str], length=1) -> dict[str: int]:
        token_scores = self.score_tokens(tokens)
        top_n_names = sorted(token_scores, key=token_scores.get, reverse=True)[:length]
        return {name: token_scores[name] for name in top_n_names}
