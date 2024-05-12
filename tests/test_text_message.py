from datetime import datetime
from unittest import TestCase

from telegram import Update, Message, Chat

from src.handlers.messages.text_message import TextMessageHandler


class MessageHandlerTest(TestCase):
    """
    Testing all options from the options.yaml file one by one
    """

    def setUp(self):
        self.handler = TextMessageHandler(config_path="src/handlers/messages/options.yaml")

    def test_orevo(self):
        message = Message(text="orevo", chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)

        self.assertEqual(
            "так убер же всех разогнал!",
            self.handler.handle_text_message(message)
        )
