from datetime import datetime

from telegram import Message, Chat

from src.handlers.messages.text_message import TextMessageHandler
from src.handlers.messages.models import SimpleResponse

from unittest import TestCase
from src.handlers.messages.stuff.hn_top import HackerNewsAction


class TestHackerNewsAction(TestCase):

    def setUp(self):

        self.hna = HackerNewsAction()


    def test_get_hh_top_story_link(self):

        url, text = self.hna.get_hn_top_story_link()
        self.assertTrue(url.startswith("http"))
        self.assertTrue(len(text) > 0)
        print(url, text)


class MessageHandlerTest(TestCase):
    """
    Testing all options from the options.yaml file one by one
    """

    def setUp(self):
        self.handler = TextMessageHandler(config_path="src/handlers/messages/options.yaml")

    def test_hacker_news(self):
        test_text = "эй ричард, как там на передовой?"
        message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
        answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

        self.assertIsNotNone(answer)
        self.assertIn("все идет по плану. новости вот читаю:", answer.data)

