from pyrogram import filters
from damMusic import app


@app.on_message(filters.command("hastag"))
async def hastag(bot, message):

    try:
        text = message.text.split(" ", 1)[1]
        res = await utils.TheApi.gen_hashtag(text)
    except IndexError:
        return await message.reply_text("<blockquote>Example:\n\n/hastag python</blockquote>")

    await message.reply_text(f"<blockquote>ʜᴇʀᴇ ɪs ʏᴏᴜʀ  ʜᴀsᴛᴀɢ :\n<pre>{res}</pre></blockquote>", quote=True)


__MODULE__ = "Hᴀsʜᴛᴀɢ"
__HELP__ = """
<blockquote>**ʜᴀsʜᴛᴀɢ ɢᴇɴᴇʀᴀᴛᴏʀ:**

• `/hashtag [text]`: Gᴇɴᴇʀᴀᴛᴇ ʜᴀsʜᴛᴀɢs ғᴏʀ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ.</blockquote>
"""
