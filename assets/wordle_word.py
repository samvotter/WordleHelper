import dataclasses

from assets.states import LetterState


@dataclasses.dataclass(frozen=True, order=True)
class WordleLetter:
    letter: str
    position: int
    state: LetterState


@dataclasses.dataclass(frozen=True, order=True)
class WordleWord:
    letters: list[WordleLetter] = dataclasses.field(default_factory=list)