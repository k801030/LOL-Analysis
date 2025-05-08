class TypoCorrector:
    typo_map = {
        "FiddleSticks": "Fiddlesticks",
        "TOP": "top",
        "JUNGLE": "jg",
        "MIDDLE": "mid",
        "BOTTOM": "bot",
        "UTILITY": "sup",
    }

    @staticmethod
    def correct(word):
        """
        Correct a single word based on predefined typo mappings.
        """
        return TypoCorrector.typo_map.get(word, word)
