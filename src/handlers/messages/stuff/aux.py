import logging

from telegram import Message

logger = logging.getLogger(__name__)

def get_text(message: Message) -> str:
    if message.text:
        message_text = message.text.lower()
    elif message.caption:
        message_text = message.caption.lower()
    else:
        logger.error("No text in the message")
        raise ValueError("No text in the message")
    return message_text
