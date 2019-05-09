import json
from botocore.vendored import requests
import os
import re
import random

import hn_top

BOT_TOKEN = os.environ['bot_token']
URL = "https://api.telegram.org/bot{}/".format(BOT_TOKEN)
STIKER = os.environ['sticker']
BATKO_STIKER = os.environ['batko_sticker']
RAND_RATIO = int(os.environ['rand_ratio'])


def join_handler(chat_id, reply_to):
    send_message("Игорь, ты ли это?", chat_id, reply_to)


def send_message(text, chat_id, reply_to):
    url = URL + "sendMessage"
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'markdown'}
    if reply_to:
        payload['reply_to_message_id'] = reply_to
    requests.post(url, json=payload)


def send_sticker(sticker_id, chat_id, reply_to):
    print("sending sticker %s %s %s" % (sticker_id, chat_id, reply_to))
    url = URL + "sendSticker"
    payload = {'chat_id': chat_id, 'sticker': sticker_id}
    if reply_to:
        payload['reply_to_message_id'] = reply_to
    r = requests.post(url, json=payload)
    print(r.json())


def lambda_handler(event, context):
    message = json.loads(event['body'])
    print(message)
    try:
        if message['message']['new_chat_participant']['id']:
            print('new member')
            chat_id = message['message']['chat']['id']
            reply_to = message['message']['message_id']
            join_handler(chat_id, reply_to)
            return {'statusCode': 200}
    except:
        pass

    try:
        body_message = message['message']
    except:
        try:
            print("edited message")
            body_message = message['edited_message']
        except:
            print("wrong message type")
            return
    try:
        p = re.compile(
            r".*((\bя\b)|(\bбля\b)|([aа]{3,})).*\bор(у|ну)\b.*", re.IGNORECASE)
        message_text = (body_message['text']).lower()
        if p.match(message_text):
            print("chat message")
            chat_id = body_message['chat']['id']
            reply_to = body_message['message_id']

            sticker_id = STIKER
            send_sticker(sticker_id, chat_id, reply_to)
            return {'statusCode': 200}
        bp = re.compile(r".*\bя белорус\b.*", re.IGNORECASE)
        if bp.match(message_text):
            print("chat message")
            chat_id = body_message['chat']['id']
            reply_to = body_message['message_id']

            sticker_id = BATKO_STIKER
            send_sticker(sticker_id, chat_id, reply_to)
            return {'statusCode': 200}
        jp = re.compile(
            r".*\b(джав(к)?(ейк)?(еечк)?(а|е|ой|у)|java)\b.*", re.IGNORECASE)
        if jp.match(message_text):
            jp_check = re.compile("так джава же говно", re.IGNORECASE)
            if not jp_check.match(message_text):
                print("chat message")
                chat_id = body_message['chat']['id']
                reply_to = body_message['message_id']
                print(RAND_RATIO)
                rand = random.randint(1, 100)
                print(rand)
                if rand < RAND_RATIO:
                    send_message("так джава же говно", chat_id, reply_to)
                else:
                    print("java ololo is skipped")

                return {'statusCode': 200}
        news_rg = re.compile(
            r"эй ричард, как там на передовой?", re.IGNORECASE)
        if news_rg.match(message_text):
            print("news message")
            chat_id = body_message['chat']['id']
            reply_to = body_message['message_id']
            url, text = hn_top.get_top()
            send_message("все идет по плану. новости вот читаю: [%s](%s)" % (
                text, url), chat_id, reply_to)

        u_rg = re.compile(
            r".*\b((убер(а|е|ом|у)?)|uber)\b.*", re.IGNORECASE)
        if u_rg.match(message_text):
            print("chat message")
            chat_id = body_message['chat']['id']
            reply_to = body_message['message_id']
            print(RAND_RATIO)
            rand = random.randint(1, 100)
            print(rand)
            if rand < RAND_RATIO:
                send_message("Ехал убер через убер, видит убер в убер убер", chat_id, reply_to)
            else:
                print("uber ololo is skipped")

            return {'statusCode': 200}
        print("debug")
        p_rg = re.compile(r".*\bричард\b.*\bпочему\b.*\bты\b.*\bне\b.*", re.IGNORECASE)
        if p_rg.match(message_text):
            print("pochemu message")
            chat_id = body_message['chat']['id']
            reply_to = body_message['message_id']
            send_message("я что, дурак?", chat_id, reply_to)
            return {'statusCode': 200}
    except Exception as e:
        print("error")
        print(e)

        pass
    return {'statusCode': 200}
