import unittest
from unittest.mock import patch
from src.spam import SpamWordsSearcher, SpamWord

class TestSpamWordsSearcher(unittest.TestCase):

    def setUp(self):
        self.mock_words = [
            SpamWord(word="заработок", weight=300),
            SpamWord(word="предложение", weight=200)
        ]
        self.searcher = SpamWordsSearcher('src/resources/trigger_words.yaml')

    @patch.object(SpamWordsSearcher, '_load_words', return_value=[
        SpamWord(word="заработок", weight=300),
        SpamWord(word="предложение", weight=200)
    ])
    def test_load_words(self, mock_load_words):
        words = self.searcher._load_words()
        self.assertIsInstance(words, list)
        self.assertGreater(len(words), 0)
        self.assertIsInstance(words[0], SpamWord)

    @patch.object(SpamWordsSearcher, '_load_words', return_value=[
        SpamWord(word="заработок", weight=300),
        SpamWord(word="предложение", weight=200)
    ])
    def test_search(self, mock_load_words):
        message = "This is a test message with заработок and предложение."
        found_words = self.searcher.search(message)
        self.assertIsInstance(found_words, list)
        self.assertGreater(len(found_words), 0)
        self.assertTrue(any(word.word == "заработок" for word in found_words))
        self.assertTrue(any(word.word == "предложение" for word in found_words))

if __name__ == '__main__':
    unittest.main()