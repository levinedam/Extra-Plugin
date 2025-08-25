import random

from pyrogram import filters
from damMusic import app


def get_random_message(love_percentage):
    if love_percentage <= 30:
        return random.choice(
            [
                "<blockquote>Love is in the air but needs a little spark.</blockquote>",
                "A good start but there's room to grow.",
                "<blockquote>It's just the beginning of something beautiful.</blockquote>",
            ]
        )
    elif love_percentage <= 70:
        return random.choice(
            [
                "<blockquote>A strong connection is there. Keep nurturing it.</blockquote>",
                "<blockquote>You've got a good chance. Work on it.</blockquote>",
                "<blockquote>Love is blossoming, keep going.</blockquote>",
            ]
        )
    else:
        return random.choice(
            [
                "<blockquote>Wow! It's a match made in heaven!</blockquote>",
                "<blockquote>Perfect match! Cherish this bond.</blockquote>",
                "<blockquote>Destined to be together. Congratulations!</blockquote>",
            ]
        )


@app.on_message(filters.command("love", prefixes="/"))
async def love_command(client, message):
    command, *args = message.text.split(" ")
    if len(args) >= 2:
        name1 = args[0].strip()
        name2 = args[1].strip()

        love_percentage = random.randint(10, 100)
        love_message = get_random_message(love_percentage)

        response = f"{name1}💕 + {name2}💕 = {love_percentage}%\n\n{love_message}"
    else:
        response = "<blockquote>Please enter two names after /love command.</blockquote>"

    await app.send_message(message.chat.id, response)


__MODULE__ = "Lᴏᴠᴇ"
__HELP__ = """
<blockquote>**ʟᴏᴠᴇ ᴄᴀʟᴄᴜʟᴀᴛᴏʀ:**

• `/love [name1] [name2]`: Cᴀʟᴄᴜʟᴀᴛᴇs ᴛʜᴇ ᴘᴇʀᴄᴇɴᴛᴀɢᴇ ᴏғ ʟᴏᴠᴇ ʙᴇᴛᴡᴇᴇɴ ᴛᴡᴏ ᴘᴇᴏᴘʟᴇ.</blockquote>
"""
