import pytest
import re
import enum


class TestWords(enum.StrEnum):
    HELLO = "hello"
    RABBIT = "rabbit"
    THERE = "there"
    WONT = "wont"
    FIFTEEN = "fifteen"
    PORRIDGE = "porridge"
    SLIMER = "slimer"
    JAZZY = "jazzy"
    QUILL = "quill"
    WALLET = "wallet"


@pytest.mark.parametrize(
    "include, exclude, expected", [
        ("e", "f", [TestWords.HELLO, TestWords.THERE, TestWords.PORRIDGE, TestWords.SLIMER, TestWords.WALLET]),
        ("a", "el", [TestWords.RABBIT, TestWords.JAZZY, TestWords.WALLET]),
        ("to", "", [TestWords.WONT])
    ]
)
def test_must_include_x_but_not_y(include, exclude, expected):
    must_have = "".join(r"(?=.*" + f"{letter})" for letter in include)
    pattern = re.compile(must_have + r"[^\W" + f"{exclude}]")
    results = list(filter(lambda word: pattern.match(word), list(TestWords)))
    print(results)
    assert results == expected
