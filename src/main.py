import logging
import os

import functions_framework
from flask import Request, abort
from telegram import Bot, Update, Message

from .config import commands, invite_handler, auth_enabled, authorized_chats
from .handlers.messages.new_chat_members import new_joiner_handler
from .models import SimpleResponse, ResponseType
from .tracing.log import GCPLogger

"""

This is the main entry point for the telegram bot.
I want to keep this file as clean as possible, so I will try to move all the logic to other files.

What can be done here:
- parse incoming message
- check if it is a command
- check if it is a new user
- check if it is a picture
- check if it is a regular message
- check if it is a reply
- check if it is a forwarded message
- check if it is a sticker
- check if it is a video
- check if it is a voice message


"""

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = Bot(token=BOT_TOKEN)

# Set the new logger class
logging.setLoggerClass(GCPLogger)

logger = logging.getLogger(__name__)


def send_back(message: Message, response: SimpleResponse):
    """
    Sends a message back to the user. Using telegram bot's sendMessage method.
    :param message: incoming telegram message
    :param text:
    :return:
    @param message: OG message from telegram. it's used to get chat_id and other stuff
    @param response: indication of the responding to the user
    """
    if response.type == ResponseType.text:
        bot.send_message(chat_id=message.chat_id, text=response.data)
    elif response.type == ResponseType.sticker:
        bot.send_sticker(chat_id=message.chat_id, sticker=response.data)
    else:
        raise NotImplementedError("Unsupported response type")

def process_message(message: Message) -> (str, bool):
    """
    Command handler for telegram bot.
    Differentiates between handlers, new joiners, pictures, and regular messages.
    TODO test with JSON deserialization

    :param message: incoming telegram message
    :return: tuple from markdown response to the user and indication of replying to the message
    """

    if message.text and message.text.startswith("/"):
        command_text = message.text.split("@")[0]  # Split command and bot's name
        command = commands.get(command_text)
        if command:
            return SimpleResponse(data=command(message))
        else:
            return SimpleResponse(data="Unrecognized command")
    elif message.new_chat_members and len(message.new_chat_members) > 0:
        if len(message.new_chat_members) > 1:
            return SimpleResponse(data="Ох сколько народу-то!")
        if message.from_user.id != message.new_chat_members[0].id:
            # user invited by another user
            return SimpleResponse(data=invite_handler(message))
        else:
            # new user joined by link
            return SimpleResponse(data=new_joiner_handler(message))
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
    send_back(message, SimpleResponse(data="It's not for you!"))
    return False


@functions_framework.http
def handle(request: Request):
    """
    Incoming telegram webhook handler for a GCP Cloud Function.
    When request is received, body is parsed into standard telegram message model, and then forwarded to command handler.
    """
    if request.method == "GET":
        return {"statusCode": 200, "body": "fuck off"}
    # when post is called, parse body into standard telegram message model, and then forward to command handler
    if request.method == "POST":
        try:
            incoming_data = request.get_json()
            logger.debug(incoming_data)
            update_message = Update.de_json(incoming_data, bot)
            if auth_enabled and auth_check(update_message.message):
                response = process_message(update_message.message)
                send_back(message=update_message.message, response=response)
            return {"statusCode": 200}
        except Exception as e:
            logger.error(e)

    # Unprocessable entity
    abort(422)
