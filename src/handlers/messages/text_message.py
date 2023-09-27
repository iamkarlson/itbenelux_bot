import re
import random

from telegram import Message


def handle_text_message(update: Message):
    try:
        chat_id = update.chat_id
        reply_to = update.message_id
        p = re.compile(
            r".*((\bя\b)|(\bбля\b)|([aа]{3,})).*\bор(у|ну)\b.*", re.IGNORECASE
        )
        message_text = (update["text"]).lower()
        if p.match(message_text):
            print("chat message")

            sticker_id = OREVO_STICKER
            send_sticker(sticker_id, chat_id, reply_to)
            return {"statusCode": 200}

        jp = re.compile(
            r".*\b(джав(к)?(ейк)?(еечк)?(а|е|ой|у)|java)\b.*", re.IGNORECASE
        )
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

        news_rg = re.compile(r"эй ричард, как там на передовой\?", re.IGNORECASE)
        if news_rg.match(message_text):
            print("news message")
            url, text = hn_top.get_top()
            send_message(
                "все идет по плану. новости вот читаю: [%s](%s)" % (text, url),
                chat_id,
                reply_to,
            )
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
            message_text,
            r".*\bричард\b.*\bпочему\b.*\bты\b.*\bне\b.*",
            "я что, дурак?",
            chat_id,
            reply_to,
            101,
        )
        if durak_answer["statusCode"] > 0:
            return durak_answer

        print("rubi")
        rubi_answer = check(
            message_text,
            r".*\b(руби|ruby)\b.*",
            "руби мёртв",
            chat_id,
            reply_to,
            RAND_RATIO * 2,
        )
        if rubi_answer["statusCode"] > 0:
            return rubi_answer

        print("setevik")
        setevik_answer = check(
            message_text,
            r".*\b(сетевик)\b.*",
            "сетевик хуже фронтендера",
            chat_id,
            reply_to,
            RAND_RATIO * 2,
        )
        if setevik_answer["statusCode"] > 0:
            return setevik_answer

        print("amen")

        amen_answer = check(
            message_text,
            r".*\b(б[еи]гемот?с?т?в[оаие]|б[еи]гемотт?[оаие]|б[еи]гемос?тв[оаие])\b.*",
            "аминь",
            chat_id,
            reply_to,
            RAND_RATIO * 3,
        )
        if amen_answer["statusCode"] > 0:
            return amen_answer

        print("a-men")

        amen1_answer = check(
            message_text,
            r".*\b(б-мот|б-мотств[оаие]|б-мотт[оаие])\b.*",
            "ам-инь",
            chat_id,
            reply_to,
            RAND_RATIO * 3,
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
            message_text,
            r"нет[.!\)]?$",
            "эникейщика ответ",
            chat_id,
            reply_to,
            RAND_RATIO * 3,
        )
        if pizda_answer1["statusCode"] > 0:
            return pizda_answer1

        print("aliexpress_answer")
        aliexpress_answer = check(
            message_text,
            r".*\b(али|алиекспресс?[А-я]?|алиэкспресс?[А-я]?|aliexpress|bangood)\b.*",
            "НЕ ПОКУПАЙ У КИТАЙЦЕВ ПОДУМОЙ",
            chat_id,
            reply_to,
            101,
        )
        if aliexpress_answer["statusCode"] > 0:
            return aliexpress_answer

        print("moneyz")
        moneyz_answer = check(
            message_text,
            r"эй ричард, мне мало платят",
            "а я видел [тут](https://www.levels.fyi/Salaries/Software-Engineer/Netherlands/) плотют много! обманывают наверное!",
            chat_id,
            reply_to,
            101,
        )
        if moneyz_answer["statusCode"] > 0:
            return moneyz_answer

        print("tier")
        tier_answer = check(
            message_text,
            r".*\b[чЧ]то.*\b(такое|за)\b.*\b(тир|tir|tier)[123]?\??\b.*",
            "В конце-концов это [про деньги](https://blog.pragmaticengineer.com/software-engineering-salaries-in-the-netherlands-and-europe/)",
            chat_id,
            reply_to,
            101,
        )
        if tier_answer["statusCode"] > 0:
            return tier_answer

    except Exception as e:
        print("error occurred")
        print(e)
        pass
    return {"statusCode": 200}

