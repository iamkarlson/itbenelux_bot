from telegram import Message


def invite_handler(update: Message, callback):

    new_joiner = update.new_chat_members[0]
    inviter = update.from_user
    text = f"Что, [{inviter.full_name}](tg://user?id={inviter.id}), дружка своего проприетарного привел? [{new_joiner.full_name}](tg://user?id={new_joiner.id}), что скажешь в свое оправдание?"

    callback(text=text, as_new=False, parse_mode="markdown")
