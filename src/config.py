import os

from .commands import *

commands = {
    "/start": command_start,
    "/webhook": command_webhook,
    "/info": command_info,
}

authorized_chats = [int(x) for x in os.environ["AUTHORIZED_CHAT_IDS"].split(",")]
auth_enabled = False
