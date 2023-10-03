import random
import re
import yaml
from telegram import Message
from src.models import ResponseType, SimpleResponse
from src.stuff import hn_top


def check(message, regexp, answer, ratio):
    p_rg = re.compile(regexp, re.IGNORECASE)
    if p_rg.match(message):
        rand = random.randint(1, 100)
        if rand < ratio:
            return SimpleResponse(data=answer)
        else:
            print(f"{answer} is skipped")
            return None


def handle_text_message(update: Message):
    try:
        message_text = update.text.lower()

        with open("options.yaml", "r") as f:
            options = yaml.safe_load(f)

        for opt in options:
            extra_data = None
            if 'extra' in opt and opt['extra'] == 'hn_top':
                extra_data = hn_top.get_top()
            answer = check(
                message_text,
                opt["regexp"],
                opt.get("answer", "").format(*extra_data) if extra_data else opt.get("answer", ""),
                opt["ratio"]
            )
            if answer:
                if 'type' in opt:
                    answer.type = ResponseType[opt['type']]
                return answer
    except Exception as e:
        print("error occurred")
        print(e)


if __name__ == "__main__":
    # Test the function here, if needed
    pass
