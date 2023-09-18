import logging
import os

import functions_framework
from flask import Request, abort
from telegram import Bot, Update, Message

from .config import default_action, commands
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


def handle_message(message: Message):
    """
    Handles incoming telegram message.
    :param message: incoming telegram message
    :return:
    """
    response = process_message(message)
    if response:
        send_back(message, response)
    else:
        send_back(message, "I don't understand")


def process_message(message: Message):
    """
    Command handler for telegram bot.
    Differentiates between commands, new joiners, pictures, and regular messages.
    """
    # Check if the message is a command
    if message.text and message.text.startswith("/"):
        command_text = message.text.split("@")[0]  # Split command and bot's name
        command = commands.get(command_text)
        if command:
            return command(message)
        else:
            return "Unrecognized command"
    elif message.new_chat_members:
        pass
    elif message.photo:
        pass
    else:
        return process_non_command(message)


def process_non_command(message: Message):
    # Your code here to process non-command messages
    if default_action(message):
        logger.info("Added to journal!")
        return "Added to journal!"
    else:
        return "Failed to add to journal."


authorized_chats = [int(x) for x in os.environ["AUTHORIZED_CHAT_IDS"].split(",")]


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
            if auth_check(update_message.message):
                handle_message(update_message.message)
            return {"statusCode": 200}
        except Exception as e:
            logger.error(e)

    # Unprocessable entity
    abort(422)
