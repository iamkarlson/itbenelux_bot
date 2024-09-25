import logging
import os

import functions_framework
from flask import Request, abort
from telegram import Bot, Update, Message
from unsync import unsync

from .config import invite_handler, authorized_chats
from .handlers.messages.stuff.aux import get_text
from .spam import SpamWordsSearcher, SpamStructureSearcher

import sentry_sdk
from sentry_sdk.integrations.gcp import GcpIntegration

from .handlers.messages.models import SimpleResponse, ResponseType
from .handlers.messages.new_chat_members import new_joiner_handler
from .handlers.messages.text_message import TextMessageHandler, logger
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

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)

# Set the new logger class
logging.setLoggerClass(GCPLogger)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
bot = Bot(token=BOT_TOKEN)

SENTRY_DSN = os.environ.get("SENTRY_DSN", "")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[GcpIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

spam_words_detector = SpamWordsSearcher("resources/trigger_words.yaml")
spam_structure_detector = SpamStructureSearcher()

SPAM_MIN_WEIGHT = 1000

text_message_handler = TextMessageHandler(config_path="resources/options.yaml")


@unsync
async def send_back(message: Message, response: SimpleResponse):
    """
    Sends a message back to the user. Using telegram bot's sendMessage method.
    :param message: incoming telegram message
    :param text:
    :return:
    @param message: OG message from telegram. it's used to get chat_id and other stuff
    @param response: indication of the responding to the user
    """
    logger.debug("Sending response")
    if response.type == ResponseType.text:
        await bot.send_message(
            chat_id=message.chat_id,
            reply_to_message_id=message.id,
            text=response.data,
            parse_mode="Markdown",
        )
    elif response.type == ResponseType.sticker:
        await bot.send_sticker(
            chat_id=message.chat_id,
            reply_to_message_id=message.id,
            sticker=response.data,
        )
    else:
        logger.error("Unsupported response type")
        raise NotImplementedError("Unsupported response type")


@unsync
async def kick(message: Message):
    """
    Function to handle spam messages. For now, it just sends a "SPAM" message as a response
    without actually kicking the user.

    :param message: incoming telegram message
    :return: None
    """
    logger.info(f"Spam detected from user: {message.from_user.username}")
    await bot.send_message(
        chat_id=message.chat_id,
        reply_to_message_id=message.id,
        text="SPAM",
        parse_mode="Markdown"
    )


def process_message(message: Message) -> (str, bool):
    """
    Command handler for telegram bot.
    Differentiates between handlers, new joiners, pictures, and regular messages.
    TODO test with JSON deserialization

    :param message: incoming telegram message
    :return: tuple from markdown response to the user and indication of replying to the message
    """

    logger.debug("Processing message")

    if message.new_chat_members and len(message.new_chat_members) > 0:
        logger.info("New user joined")
        if len(message.new_chat_members) > 1:
            return SimpleResponse(data="Ох сколько народу-то!")
        if message.from_user.id != message.new_chat_members[0].id:
            # user invited by another user
            return SimpleResponse(data=invite_handler(message))
        else:
            # new user joined by link
            return SimpleResponse(data=new_joiner_handler(message))
    elif message.photo or message.text:
        # On a regular message, needs to be answered with funny response
        # Even if it's a photo, we can still process it as a regular message based on the `caption`
        logger.info("Regular message received")
        answer = text_message_handler.handle_text_message(message)
        if answer:
            logger.debug(f"Answer: {answer.data}")
        return answer
    else:
        # Finally we cannot recognize the message so we abort it
        # It will spam in logs, and it will fuck up the integration with webhooks.
        # TODO setup some monitoring or error handling via GCP
        raise NotImplementedError("Unsupported communication, sorry!")


def auth_check(message: Message):
    if message.chat.id in authorized_chats:
        return True
    logger.info("Unauthorized chat id")
    logger.warning(
        f"User chat id: {message.chat.id} (from @{message.from_user.username})"
    )
    send_back(message, SimpleResponse(data="It's not for you!"))
    return False



def calculate_spam_words_weights(message: Message):
    """
    Function extract trigger words from the message and returns accumulative spam weights

    Trigger words are defined with weight each in TRIGGER_WORDS
    @param message:
    @return:
    """
    text = get_text(message)
    found_words = spam_words_detector.search(text)

    # Calculate the total weight of found spam words
    total_weight = sum(spam_word.weight for spam_word in found_words)

    if total_weight > 0:
        logger.warning(f"There are a few spam words found: {[spam_word.word for spam_word in found_words]}")

    return total_weight
def spam_check(message: Message):
    weights = calculate_spam_words_weights(message)
    weights += spam_structure_detector.search(message)
    #weights += calculate_user_weigths(message)
    if weights >= SPAM_MIN_WEIGHT:
        return True
    return False


@functions_framework.http
def handle(request: Request):
    """
    ================================================================================

    Incoming telegram webhook handler for a GCP Cloud Function.
    When request is received, body is parsed into standard telegram message model, and then forwarded to command handler.

    Process is the following:
    - auth_check -> chat validation
    - process_message -> make a response
    - send_back -> send a formatted response back


    The whole thing is wrapped in sentry to catch any exceptions.
    If an exception is caught, I send HTTP200 back to telegram.

    ================================================================================
    """
    if request.method == "GET":
        return {"statusCode": 200, "body": "fuck off"}
    # when post is called, parse body into standard telegram message model, and then forward to command handler
    if request.method == "POST":
        try:
            incoming_data = request.get_json()
            logger.debug(f"incoming data: {incoming_data}")
            update_message = Update.de_json(incoming_data, bot)
            message = update_message.message or update_message.edited_message
            if auth_check(message):
                is_spam = spam_check(message)
                if is_spam:
                    kick(message)
                response = process_message(message)
                if response:
                    send_back(message=message, response=response)
            return {"statusCode": 200}
        except Exception as e:
            sentry_sdk.capture_exception(e)
            logger.error("Error occurred but message wasn't processed")
            return {"statusCode": 200}

    # Unprocessable entity
    abort(422)


