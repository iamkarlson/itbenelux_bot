import json
from botocore.vendored import requests
import os
import re
import random
from collections import namedtuple

import hn_top

BOT_TOKEN = os.environ["bot_token"]
URL = "https://api.telegram.org/bot{}/".format(BOT_TOKEN)
STIKER = os.environ["sticker"]
RAND_RATIO = int(os.environ["rand_ratio"])


class User(namedtuple("User", "id, is_bot, first_name, last_name")):
    # __slots__ = ()

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name
        else:
            return self.id

    def __str__(self):
        return self.full_name

    @staticmethod
    def from_dict(d):
        if d is None or ["id", "is_bot", "first_name"] > list(d.keys()):
            return None
        return User(int(d.get("id", 0)), bool(d.get("is_bot", True)), d.get("first_name"), d.get("last_name"))


def join_handler(chat_id, reply_to):
    rand = random.randint(1, 100)
    choices = ["Игорь, ты ли это?",
        "Жора, где ты был?",
        "Кем вы видите себя через 5 лет?",
        "Почему вы выбрали именно эту профессию?",
        "Чем абстрактный класс отличается от интерфейса?",
        "Вы используете стримы?",
        "Ты-то хоть 350к зарабатываешь?",
        "Как наш чат поможет добиться вам ваших целей в жизни?"]
    choice = random.choice(choices)
    send_message(choice, chat_id, reply_to)


def invite_handler(new_joiner, inviter, chat_id):
    print(new_joiner)
    send_message('Что, [%s](tg://user?id=%s), дружка своего проприетарного привел? [%s](tg://user?id=%s), что скажешь в свое оправдание?' %
                 (inviter.full_name, inviter.id, new_joiner.full_name, new_joiner.id), chat_id, None)


def send_message(text, chat_id, reply_to):
    url = URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "markdown"}
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    print(payload)
    requests.post(url, json=payload)


def send_sticker(sticker_id, chat_id, reply_to):
    print("sending sticker %s %s %s" % (sticker_id, chat_id, reply_to))
    url = URL + "sendSticker"
    payload = {"chat_id": chat_id, "sticker": sticker_id}
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    r = requests.post(url, json=payload)
    print(r.json())


def lambda_handler(event, context):
    print(event)
    body = json.loads(event["body"])
    try:
        msg = body["message"]
        inviter = User.from_dict(msg.get("from"))
        new_joiner = User.from_dict(msg.get("new_chat_participant"))
        chat_id = msg["chat"]["id"]
        # new_joiner = {id: new_joiner_id, name: new_joiner_name}
        # inviter = {id: inviter_id, name: inviter_name}
        print(inviter.id)
        if new_joiner.id != inviter.id:
            print("%s invited %s to %d" % (inviter, new_joiner, chat_id))
            invite_handler(new_joiner, inviter, chat_id)
            return {"statusCode": 200}
        elif new_joiner:
            print("%s joined to %d" % (new_joiner, chat_id))
            reply_to = body["message"]["message_id"]
            join_handler(chat_id, reply_to)
            return {"statusCode": 200}

    except Exception as e:
        print(e)

    try:
        body_message = body["message"]
    except:
        try:
            print("edited message")
            body_message = body["edited_message"]
        except:
            print("wrong message type")
            return
    try:
        chat_id = body_message["chat"]["id"]
        reply_to = body_message["message_id"]
        p = re.compile(
            r".*((\bя\b)|(\bбля\b)|([aа]{3,})).*\bор(у|ну)\b.*", re.IGNORECASE)
        message_text = (body_message["text"]).lower()
        if p.match(message_text):
            print("chat message")

            sticker_id = STIKER
            send_sticker(sticker_id, chat_id, reply_to)
            return {"statusCode": 200}


        jp = re.compile(
            r".*\b(джав(к)?(ейк)?(еечк)?(а|е|ой|у)|java)\b.*", re.IGNORECASE)
        if jp.match(message_text):
            jp_check = re.compile("так джава же говно", re.IGNORECASE)
            if not jp_check.match(message_text):
                print("chat message")
                print(RAND_RATIO)
                rand = random.randint(1, 100)
                print(rand)
                if rand < RAND_RATIO:
                    send_message("так джава же говно", chat_id, reply_to)
                    return {"statusCode": 200}
                else:
                    print("java ololo is skipped")

        news_rg = re.compile(
            r"эй ричард, как там на передовой\?", re.IGNORECASE)
        if news_rg.match(message_text):
            print("news message")
            url, text = hn_top.get_top()
            send_message("все идет по плану. новости вот читаю: [%s](%s)" % (
                text, url), chat_id, reply_to)
            return {"statusCode": 200}

        print("uber")
        uber_answer = check(
            message_text,
            r".*\b((убер(а|е|ом|у)?)|uber)\b.*",
            "так убер же всех разогнал!",
            chat_id,
            reply_to,
            RAND_RATIO,
        )
        if uber_answer["statusCode"] > 0:
            return uber_answer
        print("durak")
        durak_answer = check(
            message_text, r".*\bричард\b.*\bпочему\b.*\bты\b.*\bне\b.*", "я что, дурак?", chat_id, reply_to, 101
        )
        if durak_answer["statusCode"] > 0:
            return durak_answer

        print("rubi")
        rubi_answer = check(message_text, r".*\b(руби|ruby)\b.*",
                            "руби мёртв", chat_id, reply_to, RAND_RATIO * 2)
        if rubi_answer["statusCode"] > 0:
            return rubi_answer

        print("setevik")
        setevik_answer = check(
            message_text, r".*\b(сетевик)\b.*", "сетевик хуже фронтендера", chat_id, reply_to, RAND_RATIO * 2
        )
        if setevik_answer["statusCode"] > 0:
            return setevik_answer

        print("amen")

        amen_answer = check(
            message_text, r".*\b(б[еи]гемот?с?т?в[оаие]|б[еи]гемотт?[оаие]|б[еи]гемос?тв[оаие])\b.*", "аминь", chat_id, reply_to, RAND_RATIO * 3
        )
        if amen_answer["statusCode"] > 0:
            return amen_answer

        print("a-men")

        amen1_answer = check(
            message_text, r".*\b(б-мот|б-мотств[оаие]|б-мотт[оаие])\b.*", "ам-инь", chat_id, reply_to, RAND_RATIO * 3
        )
        if amen1_answer["statusCode"] > 0:
            return amen1_answer

        print("pizda")
        pizda_answer = check(
            message_text, r"да[.!\)]?$", "фрибэсда", chat_id, reply_to, RAND_RATIO * 3
        )
        if pizda_answer["statusCode"] > 0:
            return pizda_answer

        pizda_answer1 = check(
            message_text, r"нет[.!\)]?$", "эникейщика ответ", chat_id, reply_to, RAND_RATIO * 3
        )
        if pizda_answer1["statusCode"] > 0:
            return pizda_answer1

        print("aliexpress_answer")
        aliexpress_answer = check(
            message_text, r".*\b(али|алиекспресс?[А-я]?|алиэкспресс?[А-я]?|aliexpress|bangood)\b.*", "НЕ ПОКУПАЙ У КИТАЙЦЕВ ПОДУМОЙ", chat_id, reply_to, 101
        )
        if aliexpress_answer["statusCode"] > 0:
            return aliexpress_answer

        print("moneyz")
        moneyz_answer = check(
            message_text, r"эй ричард, мне мало платят", "а я видел [тут](https://www.levels.fyi/Salaries/Software-Engineer/Netherlands/) плотют много! обманывают наверное!", chat_id, reply_to, 101
        )
        if moneyz_answer["statusCode"] > 0:
            return moneyz_answer

        print("tier")
        tier_answer = check(
            message_text, r".*\b[чЧ]то.*\b(такое|за)\b.*\b(тир|tir|tier)[123]?\??\b.*", "В конце-концов это [про деньги](https://blog.pragmaticengineer.com/software-engineering-salaries-in-the-netherlands-and-europe/)", chat_id, reply_to, 101
        )
        if tier_answer["statusCode"] > 0:
            return tier_answer

    except Exception as e:
        print("error occurred")
        print(e)
        pass
    return {"statusCode": 200}


def check(message, regexp, answer, chat_id, reply_to, ratio):
    p_rg = re.compile(regexp, re.IGNORECASE)
    if p_rg.match(message):
        rand = random.randint(1, 100)
        if rand < ratio:
            send_message(answer, chat_id, reply_to)
            return {"statusCode": 200}
        else:
            print("ololo is skipped")
            return {"statusCode": 200}
    return {"statusCode": 0}
