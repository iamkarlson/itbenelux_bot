from typing import List

from jellyfish import jaro_similarity
import yaml

from dataclasses import dataclass

from telegram import Message

import logging

logger = logging.getLogger(__name__)

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

    def search(self, message: str, threshold: float = 0.85) -> List[SpamWord]:
        found_words = []
        message_words = message.split()
        for word in message_words:
            for spam_word in self.words:
                similarity = jaro_similarity(word, spam_word.word)
                if similarity >= threshold:
                    logger.debug(f"Found spam word: {spam_word.word} with similarity: {similarity}")
                    found_words.append(spam_word)
        return found_words

class SpamStructureSearcher:
    """
    Class to identify suspicious formatting options that spammers typically use
    Overall, just any formatting is suspicious so we can simply count it
    """

    def search(self, message: Message) -> int:
        entities = message.entities or []

        def map_entity_type(entity):
            match entity.type:
                case 'bold':
                    return 100
                case 'italic':
                    return 100
                case 'underline':
                    return 100
                case 'mention':
                    return 200
                case 'custom_emoji':
                    return 50
                case _:
                    return 0

        return sum(map(map_entity_type, entities))

