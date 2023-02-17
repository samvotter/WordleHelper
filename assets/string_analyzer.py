class TokenAnalyzer:

    def __init__(self, tokens: list[str] = None):
        self.tokens = tokens
        self.frequency_table = {}
        self.percents = {}
        self.token_scores = {}
        self.empty_tables()

    def read(self, filepath: str = None):
        with open(filepath, 'r') as f:
            self.tokens = f.read().upper().splitlines()
        self.fill_table(self.tokens)

    def set_tokens(self, tokens: list[str]):
        self.tokens = tokens

    def empty_tables(self):
        self.frequency_table    = {chr(i).upper(): 0 for i in range(65, 91)}
        self.percents           = {chr(i).upper(): 0 for i in range(65, 91)}

    def fill_table(self, tokens: list[str] = None):
        if tokens is None:
            tokens = self.tokens
        for word in tokens:
            for letter in set(word):
                self.frequency_table[letter] += 1
        total = sum(self.frequency_table.values())
        for letter in self.frequency_table:
            self.percents[letter] = self.frequency_table[letter] / total

    def score_tokens(self, tokens: list[str] = None):
        if tokens is None:
            tokens = self.tokens
        self.token_scores = {}
        for word in tokens:
            for letter in set(word):
                if word not in self.token_scores:
                    self.token_scores[word] = self.percents[letter]
                else:
                    self.token_scores[word] += self.percents[letter]

    def best_words(self, length=1) -> dict[str: int]:
        top_n_names = sorted(self.token_scores, key=self.token_scores.get, reverse=True)[:length]
        return {name: self.token_scores[name] for name in top_n_names}



