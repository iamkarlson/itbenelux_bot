from datetime import datetime
from unittest import TestCase

from telegram import Message, Chat

from src.handlers.messages.text_message import TextMessageHandler
from src.handlers.messages.models import SimpleResponse


class MessageHandlerTest(TestCase):
    """
    Testing all options from the options.yaml file one by one
    """

    def setUp(self):
        self.handler = TextMessageHandler(config_path="src/handlers/messages/options.yaml")

    def test_uber(self):
        uber_test_text = "в убере вроде, но тут писали, что его вроде выперли\nв общем на самом деле неизвестно"
        message = Message(text=uber_test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
        answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

        self.assertIsNotNone(answer)
        self.assertEqual("так убер же всех разогнал!", answer.data)

    def test_orevo(self):
        test_text_options = ["я ору", "бля ааааа ору"]
        for test_text in test_text_options:
            message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
            answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

            self.assertIsNotNone(answer)
            self.assertEqual("так убер же всех разогнал!", answer.data)