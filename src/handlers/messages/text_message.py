import logging
import random
import re

import yaml
from telegram import Message

from .models import ResponseType, SimpleResponse
from .stuff import hn_top

hn_top_action = hn_top.HackerNewsAction()

logger = logging.getLogger(__name__)

class TextMessageHandler:

    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            self.options = yaml.safe_load(f)

    def check(self, message, opt, force_ratio) -> SimpleResponse | None:
        regexp = opt['regexp']
        answer = opt['answer']
        ratio = opt['ratio']

        p_rg = re.compile(regexp, re.IGNORECASE)
        if p_rg.match(message):
            rand = random.randint(1, 100)

            if 'extra' in opt and opt['extra'] == 'hn_top':
                extra_data = hn_top_action.get_hn_top_story_link()
                answer = answer.format(*extra_data) if extra_data else "I'm so sorry but I'm lost"

            if rand < ratio or force_ratio:
                return SimpleResponse(data=answer)
            else:
                logger.warning(f"{answer} is skipped")
                return None

    def handle_text_message(self, update: Message, force_ratio: bool = False) -> SimpleResponse:
        try:
            message_text = update.text.lower()

            for opt in self.options:
                answer = self.check(
                    message_text,
                    opt,
                    force_ratio

                )
                if answer:
                    if 'type' in opt:
                        answer.type = ResponseType[opt['type']]
                    return answer
        except Exception as e:
            logger.error("error occurred")
            print(e)


if __name__ == "__main__":
    # Test the function here, if needed
    pass
