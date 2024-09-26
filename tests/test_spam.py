import unittest
from datetime import datetime
from unittest.mock import patch

from telegram import Message, Chat

from src.spam import SpamWordsSearcher, SpamWord, SpamStructureSearcher


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
        self.assertEqual(2, len(found_words))
        first_word = any(word.word == "зaрaботок" for word in found_words)


        self.assertTrue(first_word, "Word 'заработок' not found in the list")
        self.assertTrue(any(word.word == "предложение" for word in found_words))

    def test_search_false_alarm(self):
        update =  {'message_id': 627965, 'from': {'id': 449647384, 'is_bot': False, 'first_name': 'Tim', 'username': 'zeehond'}, 'chat': {'id': -1001235860760, 'title': 'it talks Paesi Bassi, Belgio, Lussemburgo - buoni espatriati', 'username': 'ITBenelux', 'type': 'supergroup'}, 'date': 1727358993, 'text': 'у меня тоже, причём идея его поставить пришла именно из-за машинки )\n\nну Rocket в инструкции пишет что не надо декальцинировать\nставьте ontharder и молитесь'}
        message = Message.de_json(update, None)
        found_words = self.searcher.search(message.text)
        self.assertIsInstance(found_words, list)
        self.assertEqual(len(found_words), 0)


class TestSpamStructureSearcher(unittest.TestCase):

    def setUp(self):
        self.searcher = SpamStructureSearcher()

    def test_search_no_entities(self):
        message = Message(message_id=1, date=datetime.now(), chat=Chat(id=1, type="test"),
                          text="This is a test message.")
        entities = self.searcher.search(message)
        self.assertEqual(0, entities)

    def test_search_a_lot_of_entities(self):
        update = {'message_id': 363, 'from': {'id': 107262564, 'is_bot': False,
                                              'first_name': 'ᛃᛟᚺᚾ ᚠᚨcᛖᛚᛖᛊᛊ ᛞᛟᛖ',
                                              'username': 'IamKarlson',
                                              'language_code': 'en',
                                              'is_premium': True},
                  'chat': {'id': -1001672520725,
                           'title': 'никого TATATTATA test',
                           'type': 'supergroup'}, 'date': 1727284790,
                  'text': '🅰️🅱️🔤🔡🔚\nBaкaнcuя для aктuвныx!\nHyжны людu, кoтopыe yвepeннo paбoтaют c тeлeфoнoм. \nBoзpacт oт 🔞 . \n3apa6oтoк — oт 100$ в день, дeньгu cpaзy пo фaктy. \nБeз нapyшeнuй зaкoнa u вcякoй epyнды. \nO6yчeнue u дeтaлu пo ccылкe\n➡️@SpamAccount',
                  'entities': [
                      {'offset': 0, 'length': 3, 'type': 'custom_emoji', 'custom_emoji_id': '5440385956597218145'},
                      {'offset': 3, 'length': 3, 'type': 'custom_emoji', 'custom_emoji_id': '5438251082973203261'},
                      {'offset': 6, 'length': 2, 'type': 'custom_emoji', 'custom_emoji_id': '5440447185650991182'},
                      {'offset': 8, 'length': 2, 'type': 'custom_emoji', 'custom_emoji_id': '5440821620899858547'},
                      {'offset': 10, 'length': 2, 'type': 'custom_emoji', 'custom_emoji_id': '5440885676042108150'},
                      {'offset': 13, 'length': 22, 'type': 'bold'},
                      {'offset': 13, 'length': 22, 'type': 'underline'},
                      {'offset': 88, 'length': 7, 'type': 'underline'},
                      {'offset': 99, 'length': 2, 'type': 'custom_emoji', 'custom_emoji_id': '5348485489097717994'},
                      {'offset': 105, 'length': 4, 'type': 'underline'},
                      {'offset': 109, 'length': 5, 'type': 'underline'},
                      {'offset': 109, 'length': 1, 'type': 'italic'},
                      {'offset': 157, 'length': 20, 'type': 'underline'},
                      {'offset': 197, 'length': 1, 'type': 'italic'},
                      {'offset': 224, 'length': 2, 'type': 'custom_emoji', 'custom_emoji_id': '5215695279377884733'},
                      {'offset': 226, 'length': 16, 'type': 'mention'}]}
        message = Message.de_json(update, None)
        weight = self.searcher.search(message)
        # 7 emojis, 4 underlines, 2 italics, 1 mention
        # 10*7 + 50*4 + 50*2 + 100*1
        self.assertEqual(1350, weight)

    def test_search_false_alarm(self):
        update =  {'message_id': 627965, 'from': {'id': 449647384, 'is_bot': False, 'first_name': 'Tim', 'username': 'zeehond'}, 'chat': {'id': -1001235860760, 'title': 'it talks Paesi Bassi, Belgio, Lussemburgo - buoni espatriati', 'username': 'ITBenelux', 'type': 'supergroup'}, 'date': 1727358993, 'text': 'у меня тоже, причём идея его поставить пришла именно из-за машинки )\n\nну Rocket в инструкции пишет что не надо декальцинировать\nставьте ontharder и молитесь'}
        message = Message.de_json(update, None)
        weight = self.searcher.search(message)
        # 7 emojis, 4 underlines, 2 italics, 1 mention
        # 10*7 + 50*4 + 50*2 + 100*1
        self.assertEqual(0, weight)


if __name__ == '__main__':
    unittest.main()
