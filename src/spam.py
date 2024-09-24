from typing import List

from fuzzywuzzy import fuzz
import yaml

from dataclasses import dataclass

@dataclass
class SpamWord:
    word: str
    weight: int

@dataclass
class SpamWordsList:
    words: List[SpamWord]


class SpamWordsSearcher:
    """
    Class to parse trigger words from resources/trigger_words.yaml
    and search for them in the incoming messages

    Trigger words are defined as dictionary like:
    words:
    - word: заработок
      weight: 300
    - word: предложение
      weight: 200

    To make it easier, there's a data class that parses this shit
    """


    def __init__(self, path: str):
        self.path = path
        self.words = self._load_words()

    def _load_words(self) -> List[SpamWord]:
        with open(self.path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            return [SpamWord(word=item['word'], weight=item['weight']) for item in data['words']]

    def search(self, message: str) -> List[SpamWord]:
        found_words = []
        for spam_word in self.words:
            if self.check_word(message, spam_word.word):
                found_words.append(spam_word)
        return found_words


    def check_word(self, message: str, spam_word: str, threshold: int = 80) -> bool:
        similarity = fuzz.partial_ratio(spam_word, message)
        return similarity >= threshold