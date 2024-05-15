from datetime import datetime
from unittest import TestCase

from telegram import Message, Chat

from src.handlers.messages.text_message import TextMessageHandler
from src.handlers.messages.models import SimpleResponse, ResponseType


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
            self.assertEqual("CAADAgADxgADcQtCBUlZU0nRjfxRAg", answer.data)
            self.assertEqual(ResponseType.sticker, answer.type)
    def test_java(self):
        test_text = "я работаю на java"
        message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
        answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

        self.assertIsNotNone(answer)
        self.assertEqual("так джава же говно", answer.data)

    def test_richard_why(self):
        test_text = "ричард, почему ты не приходишь"
        message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
        answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

        self.assertIsNotNone(answer)
        self.assertEqual("я что, дурак?", answer.data)

    def test_ruby(self):
        test_text = "что думаешь про ruby?"
        message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
        answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

        self.assertIsNotNone(answer)
        self.assertEqual("руби мёртв", answer.data)

    def test_setevik(self):
        test_text = "ты же сетевик?"
        message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
        answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

        self.assertIsNotNone(answer)
        self.assertEqual("сетевик хуже фронтендера", answer.data)

    def test_begemot(self):
        test_text_options = ["бегемот", "бегемотство", "бегемотт", "бигемот", "бигемотство", "бигемотт"]
        for test_text in test_text_options:
            message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
            answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

            self.assertIsNotNone(answer, f"Failed on {test_text}")
            self.assertEqual("аминь", answer.data, f"Failed on {test_text}")

    def test_b_mot(self):
        test_text_options = ["б-мот", "б-мотство", "б-моттa"]
        for test_text in test_text_options:
            message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
            answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

            self.assertIsNotNone(answer, f"Failed on {test_text}")
            self.assertEqual("ам-инь", answer.data)

    def test_da(self):
        test_text_options = ["да.", "да!", "да)"]
        for test_text in test_text_options:
            message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
            answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

            self.assertIsNotNone(answer)
            self.assertEqual("фрибэсда", answer.data)

    def test_net(self):
        test_text_options = ["нет.", "нет)", "нет!"]
        for test_text in test_text_options:
            message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
            answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

            self.assertIsNotNone(answer)
            self.assertEqual("эникейщика ответ", answer.data)

    def test_aliexpress(self):
        test_text_options = ["на ali", "с алиэкспресса", "на aliexpress"]
        for test_text in test_text_options:
            message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
            answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

            self.assertIsNotNone(answer)
            self.assertEqual("НЕ ПОКУПАЙ У КИТАЙЦЕВ ПОДУМОЙ", answer.data)

    def test_salary(self):
        test_text = "эй ричард, мне мало платят"
        message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
        answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

        self.assertIsNotNone(answer)
        self.assertEqual(
            "а я видел [тут](https://www.levels.fyi/Salaries/Software-Engineer/Netherlands/) платят много! обманывают наверное!",
            answer.data)

    def test_tier(self):
        test_text = "что за tir?"
        message = Message(text=test_text, chat=Chat(id=1, type="test"), date=datetime.now(), message_id=1)
        answer: SimpleResponse = self.handler.handle_text_message(message, force_ratio=True)

        self.assertIsNotNone(answer)
        self.assertEqual(
            "В конце-концов это [про деньги](https://blog.pragmaticengineer.com/software-engineering-salaries-in-the-netherlands-and-europe/)",
            answer.data)
