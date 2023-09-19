import logging
import os

import functions_framework
from flask import Request, abort
from telegram import Bot, Update, Message

from .config import commands, invite_handler, auth_enabled, authorized_chats
from .tracing.log import GCPLogger

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = Bot(token=BOT_TOKEN)

# Set the new logger class
logging.setLoggerClass(GCPLogger)

logger = logging.getLogger(__name__)


def send_back(message: Message, text):
    """
    Sends a message back to the user. Using telegram bot's sendMessage method.
    :param message: incoming telegram message
    :param text:
    :return:
    """
    bot.send_message(chat_id=message.chat_id, text=text)


def callback(text: str, as_new: bool, parse_mode: str):
    pass


def process_message(message: Message):
    """
    Command handler for telegram bot.
    Differentiates between commands, new joiners, pictures, and regular messages.
    TODO test with JSON deserialization
    """
this method was returning a string, that was send using send_back method
However, I removed this method, and now need to refactor all that shit to send in place (or somehow nicer)
    if message.text and message.text.startswith("/"):
        command_text = message.text.split("@")[0]  # Split command and bot's name
        command = commands.get(command_text)
        if command:
            return command(message)
        else:
            return "Unrecognized command"
    elif message.new_chat_members and len(message.new_chat_members) > 0:
        if len(message.new_chat_members) > 1:
            send_back(message, "Ох сколько народу-то!")
        if message.from_user.id != message.new_chat_members[0].id:
            # user invited by another user
            invite_handler(message, callback)
        else:
            # new user joined by link
            pass
    elif message.photo:
        pass
    elif message.text:
        # Regular message, needs to be answered with funny response
        pass
    else:
        # Finally we cannot recognize the message so we abort it
        # It will spam in logs, and it will fuck up the integration with webhooks.
        # TODO setup some monitoring or error handling via GCP
        raise NotImplementedError("Unsupported communication, sorry!")


def auth_check(message: Message):
    if message.chat_id in authorized_chats:
        return True
    logger.info("Unauthorized chat id")
    send_back(message, "It's not for you!")
    return False


@functions_framework.http
def handle(request: Request):
    """
    Incoming telegram webhook handler for a GCP Cloud Function.
    When request is received, body is parsed into standard telegram message model, and then forwarded to command handler.
    """
    if request.method == "GET":
        return {"statusCode": 200}
    # when post is called, parse body into standard telegram message model, and then forward to command handler
    if request.method == "POST":
        try:
            incoming_data = request.get_json()
            logger.debug(incoming_data)
            update_message = Update.de_json(incoming_data, bot)
            if auth_enabled and auth_check(update_message.message):
                process_message(update_message.message)
            return {"statusCode": 200}
        except Exception as e:
            logger.error(e)

    # Unprocessable entity
    abort(422)
