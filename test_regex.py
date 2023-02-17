from assets.wordle_word import WordleLetter, WordleLetterREGEX, WordleWordREGEX


def test_WordleWordREG():
    WORD_FP = r"C:\Users\Svanotte\PycharmProjects\pythonProject\assets\5_letter_words.txt"

    with open(WORD_FP, 'r') as f:
        TEXT = f.read().upper()

    FIRST = [
        WordleLetter("A", 0, 0),
        WordleLetter("R", 1, 0),
        WordleLetter("O", 2, 0),
        WordleLetter("S", 3, 0),
        WordleLetter("E", 4, 1)
    ]

    SECOND = [
        WordleLetter("T", 0, 0),
        WordleLetter("I", 1, 1),
        WordleLetter("L", 2, 0),
        WordleLetter("E", 3, 1),
        WordleLetter("D", 4, 0)
    ]

    tester = WordleWordREGEX()

    for word in [FIRST, SECOND]:
        for letter in word:
            tester.incorporate_wordleletter(letter)

        tester.compile_pattern()

        results = tester.pattern.findall(TEXT)

        results = tester.scrub_must_haves(results)

        print(tester.pattern_str)

        print(results)
        print(len(results))


def test_reject_letters():

    tester = WordleLetterREGEX()

    tester.exclude_letter("g")
    tester.exclude_letter("l")
    tester.exclude_letter("v")
    tester.exclude_letter("p")

    for letter in [chr(i).upper() for i in range(65, 91)]:
        print(letter)
        result = tester.pattern.findall(letter)
        if result:
            print(result)


test_WordleWordREG()