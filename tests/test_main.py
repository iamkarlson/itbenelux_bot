import json
import os
from json import JSONDecoder
from unittest import TestCase

from telegram import Update, Bot

from src.main import handle_message

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = Bot(token=BOT_TOKEN)


class Test(TestCase):
    def test_handle_message(self):
        with open("fixtures/message.json") as f:
            test_data_raw = f.read()
            # read json from file
            test_data = JSONDecoder().decode(test_data_raw)
            print(test_data)

            update_message = Update.de_json(test_data, bot)
            handle_message(update_message.message)
            self.fail()
