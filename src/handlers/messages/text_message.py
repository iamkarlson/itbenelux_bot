import random
import re

from telegram import Message

from src.models import ResponseType, SimpleResponse
from src.settings import settings
from src.stuff import hn_top


def check(message, regexp, answer, ratio):
    p_rg = re.compile(regexp, re.IGNORECASE)
    if p_rg.match(message):
        rand = random.randint(1, 100)
        if rand < ratio:
            return SimpleResponse(data=answer)
        else:
            print("ololo is skipped")
            return None


def handle_text_message(update: Message):
    try:
        message_text = update.text.lower()

        news_rg = re.compile(r"эй ричард, как там на передовой\?", re.IGNORECASE)
        if news_rg.match(message_text):
            print("news message")
            url, text = hn_top.get_top()
            return SimpleResponse(data="все идет по плану. новости вот читаю: [%s](%s)" % (text, url))

        kto_to_oret = re.compile(
            r".*((\bя\b)|(\bбля\b)|([aа]{3,})).*\bор(у|ну)\b.*", re.IGNORECASE
        )
        if kto_to_oret.match(message_text):
            print("oret chat message")
            sticker_id = settings.orevo_sticker
            return SimpleResponse(data=sticker_id, type=ResponseType.sticker)

        java_answer = check(
            message_text,
            r".*\b(джав(к)?(ейк)?(еечк)?(а|е|ой|у)|java)\b.*",
            "так джава же говно",
            settings.rand_ratio,
        )
        if java_answer:
            return SimpleResponse(data="так джава же говно")

        print("uber")
        uber_answer = check(
            message_text,
            r".*\b((убер(а|е|ом|у)?)|uber)\b.*",
            "так убер же всех разогнал!",
            settings.rand_ratio,
        )
        if uber_answer:
            return uber_answer

        print("durak")
        durak_answer = check(
            message_text,
            r".*\bричард\b.*\bпочему\b.*\bты\b.*\bне\b.*",
            "я что, дурак?",
            101,
        )
        if durak_answer:
            return durak_answer

        print("rubi")
        rubi_answer = check(
            message_text,
            r".*\b(руби|ruby)\b.*",
            "руби мёртв",
            settings.rand_ratio * 2,
        )
        if rubi_answer:
            return rubi_answer

        print("setevik")
        setevik_answer = check(
            message_text,
            r".*\b(сетевик)\b.*",
            "сетевик хуже фронтендера",
            settings.rand_ratio * 2,
        )
        if setevik_answer:
            return setevik_answer

        print("amen")

        amen_answer = check(
            message_text,
            r".*\b(б[еи]гемот?с?т?в[оаие]|б[еи]гемотт?[оаие]|б[еи]гемос?тв[оаие])\b.*",
            "аминь",
            settings.rand_ratio * 3,
        )
        if amen_answer:
            return amen_answer

        print("a-men")

        amen1_answer = check(
            message_text,
            r".*\b(б-мот|б-мотств[оаие]|б-мотт[оаие])\b.*",
            "ам-инь",
            settings.rand_ratio * 3,
        )
        if amen1_answer:
            return amen1_answer

        print("pizda")
        pizda_answer = check(
            message_text, r"да[.!\)]?$", "фрибэсда", settings.rand_ratio * 3
        )
        if pizda_answer:
            return pizda_answer

        pizda_answer1 = check(
            message_text,
            r"нет[.!\)]?$",
            "эникейщика ответ",
            settings.rand_ratio * 3,
        )
        if pizda_answer1:
            return pizda_answer1

        print("aliexpress_answer")
        aliexpress_answer = check(
            message_text,
            r".*\b(али|алиекспресс?[А-я]?|алиэкспресс?[А-я]?|aliexpress|bangood)\b.*",
            "НЕ ПОКУПАЙ У КИТАЙЦЕВ ПОДУМОЙ",
            101,
        )
        if aliexpress_answer:
            return aliexpress_answer

        print("moneyz")
        moneyz_answer = check(
            message_text,
            r"эй ричард, мне мало платят",
            "а я видел [тут](https://www.levels.fyi/Salaries/Software-Engineer/Netherlands/) плотют много! обманывают наверное!",
            101,
        )
        if moneyz_answer:
            return moneyz_answer

        print("tier")
        tier_answer = check(
            message_text,
            r".*\b[чЧ]то.*\b(такое|за)\b.*\b(тир|tir|tier)[123]?\??\b.*",
            "В конце-концов это [про деньги](https://blog.pragmaticengineer.com/software-engineering-salaries-in-the-netherlands-and-europe/)",
            101,
        )
        if tier_answer:
            return tier_answer

    except Exception as e:
        print("error occurred")
        print(e)
