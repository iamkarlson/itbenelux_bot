from telegram import Message

from .commands import *

commands = {
    "/start": command_start,
    "/webhook": command_webhook,
    "/info": command_info,
}


# Configuration is coming from "JOURNAL_FILE" env variable.

# import os
# some_service settings = os.getenv("SOME_SERVICE_SETTINGS", None)

def default_action_handler(message: Message):
    # you can put there your default action that runs when bot just receives a message with no command
    pass


# Default action is to post to journal
default_action = default_action_handler
