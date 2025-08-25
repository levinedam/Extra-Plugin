from pyrogram import filters
from damMusic import app


@app.on_message(filters.command("id"))
async def get_id(client, message):
    try:
        if not message.reply_to_message and message.chat:
            await message.reply(
                f"<blockquote expandable>ᴜsᴇʀ <b>{message.from_user.first_name}'s</b> ɪᴅ ɪs <code>{message.from_user.id}</code>.\nᴛʜɪs ᴄʜᴀᴛ's ɪᴅ ɪs: <code>{message.chat.id}</code>.</blockquote>"
            )
        elif not message.reply_to_message.sticker or message.reply_to_message is None:
            if message.reply_to_message.forward_from_chat:
                await message.reply(
                    f"<blockquote expandable>Tʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ {str(message.reply_to_message.forward_from_chat.type)[9:].lower()}, {message.reply_to_message.forward_from_chat.title} ʜᴀs ᴀɴ ID ᴏғ <code>{message.reply_to_message.forward_from_chat.id}</code></blockquote>"
                )

            elif message.reply_to_message.forward_from:
                await message.reply(
                    f"<blockquote expandable>Tʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴜsᴇʀ, {message.reply_to_message.forward_from.first_name} ʜᴀs ᴀɴ ID ᴏғ <code>{message.reply_to_message.forward_from.id}</code>.</blockquote>"
                )

            elif message.reply_to_message.forward_sender_name:
                await message.reply(
                    "<blockquote>Sᴏʀʀʏ, I ɴᴇᴠᴇʀ sᴀᴡ ᴛʜᴀᴛ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ I ᴀᴍ ᴜɴᴀʙʟᴇ ᴛᴏ ғᴇᴛᴄʜ ᴛʜᴇ ID.</blockquote>"
                )
            else:
                await message.reply(
                    f"<blockquote>ᴜsᴇʀ {message.reply_to_message.from_user.first_name}'s ID ɪs <code>{message.reply_to_message.from_user.id}</code>.</blockquote>"
                )
        elif message.reply_to_message.sticker:
            if message.reply_to_message.forward_from_chat:
                await message.reply(
                    f"<blockquote expandable>Tʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ {str(message.reply_to_message.forward_from_chat.type)[9:].lower()}, {message.reply_to_message.forward_from_chat.title} ʜᴀs ᴀɴ ID ᴏғ <code>{message.reply_to_message.forward_from_chat.id}</code> \nᴀɴᴅ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ sᴛɪᴄᴋᴇʀ ID ɪs <code>{message.reply_to_message.sticker.file_id}</code></blockquote>"
                )

            elif message.reply_to_message.forward_from:
                await message.reply(
                    f"<blockquote expandable>Tʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴜsᴇʀ, {message.reply_to_message.forward_from.first_name} ʜᴀs ᴀɴ ID ᴏғ <code>{message.reply_to_message.forward_from.id}</code> \nᴀɴᴅ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ sᴛɪᴄᴋᴇʀ ID ɪs <code>{message.reply_to_message.sticker.file_id}</code>.</blockquote>"
                )

            elif message.reply_to_message.forward_sender_name:
                await message.reply(
                    "<blockquote>Sᴏʀʀʏ, I ɴᴇᴠᴇʀ sᴀᴡ ᴛʜᴀᴛ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ I ᴀᴍ ᴜɴᴀʙʟᴇ ᴛᴏ ғᴇᴛᴄʜ ᴛʜᴇ ID.</blockquote>"
                )

            else:
                await message.reply(
                    f"<blockquote expandable>ᴜsᴇʀ {message.reply_to_message.from_user.first_name}'s ID ɪs <code>{message.reply_to_message.from_user.id}</code>\n ᴀɴᴅ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ sᴛɪᴄᴋᴇʀ ID ɪs <code>{message.reply_to_message.sticker.file_id}</code>.</blockquote>"
                )
        else:
            await message.reply(
                f"<blockquote expandable>User {message.reply_to_message.from_user.first_name}'s ᴜsᴇʀ ID ɪs <code>{message.reply_to_message.from_user.id}</code>.</blockquote>"
            )
    except Exception as r:
        await message.reply(f"<blockquote>Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ɢᴇᴛᴛɪɴɢ ᴛʜᴇ ID. {r}</blockquote>")


__MODULE__ = "Usᴇʀɪᴅ"
__HELP__ = """
<blockquote>**ɪᴅ ʀᴇᴛʀɪᴇᴠᴇʀ:**

• `/id`: Retrieve user and chat IDs.</blockquote>
"""
