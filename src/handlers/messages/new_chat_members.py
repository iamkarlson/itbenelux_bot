import random

from telegram import Message


def invite_handler(update: Message):
    new_joiner = update.new_chat_members[0]
    inviter = update.from_user
    text = f"Что, [{inviter.full_name}](tg://user?id={inviter.id}), дружка своего проприетарного привел? [{new_joiner.full_name}](tg://user?id={new_joiner.id}), что скажешь в свое оправдание?"

    return text


def new_joiner_handler(update: Message):
    choices = [
        "Игорь, ты ли это?",
        "Жора, где ты был?",
        "Кем вы видите себя через 5 лет?",
        "Почему вы выбрали именно эту профессию?",
        "Чем абстрактный класс отличается от интерфейса?",
        "Вы используете стримы?",
        "Ты то хоть 350к зарабатываешь?",
        "Как наш чат поможет добиться вам ваших целей в жизни?",
    ]
    choice = random.choice(choices)
    return choice
