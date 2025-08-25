from pyrogram import enums, filters
from damMusic import app


@app.on_message(filters.command("removephoto"))
@utils.adminsOnly("can_change_info")
async def deletechatphoto(_, message):

    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("<blockquote>**ᴘʀᴏᴄᴇssɪɴɢ....**</blockquote>")
    admin_check = await app.get_chat_member(chat_id, user_id)
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("<blockquote>**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴ ɢʀᴏᴜᴘs !**</blockquote>")
    try:
        if admin_check.privileges.can_change_info:
            await app.delete_chat_photo(chat_id)
            await msg.edit(
                "<blockquote>**ɢʀᴏᴜᴘs  ᴘʀᴏғɪʟᴇ ᴘʜᴏᴛᴏ ʀᴇᴍᴏᴠᴇᴅ  !\nʙʏ** {}</blockquote>".format(
                    message.from_user.mention
                )
            )
    except BaseException:
        await msg.edit(
            "<blockquote>**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ʀᴇᴍᴏᴠᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ !</blockquote>**"
        )


@app.on_message(filters.command("setphoto"))
@utils.adminsOnly("can_change_info")
async def setchatphoto(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("<blockquote>ᴘʀᴏᴄᴇssɪɴɢ...</blockquote>")
    admin_check = await app.get_chat_member(chat_id, user_id)
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("<blockquote>`ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴ ɢʀᴏᴜᴘs !`</blockquote>")
    elif not reply:
        await msg.edit("<blockquote>**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ᴅᴏᴄᴜᴍᴇɴᴛ.**</blockquote>")
    elif reply:
        try:
            if admin_check.privileges.can_change_info:
                photo = await reply.download()
                await message.chat.set_photo(photo=photo)
                await msg.edit_text(
                    "<blockquote>**ɴᴇᴡ ɢʀᴏᴜᴘ ᴘʀᴏғɪʟᴇ ᴘʜᴏᴛᴏ ᴄʜᴀɴɢᴇᴅ !\nʙʏ** {}</blockquote>".format(
                        message.from_user.mention
                    )
                )
            else:
                await msg.edit("<blockquote>**sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ᴘʜᴏᴛᴏ !**</blockquote>")

        except BaseException:
            await msg.edit(
                "<blockquote>**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ !**</blockquote>"
            )


@app.on_message(filters.command("settitle"))
@utils.adminsOnly("can_change_info")
async def setgrouptitle(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("<blockquote>ᴘʀᴏᴄᴇssɪɴɢ...</blockquote>")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("<blockquote>**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴ ɢʀᴏᴜᴘs !**</blockquote>")
    elif reply:
        try:
            title = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_title(title)
                await msg.edit(
                    "<blockquote>**ɴᴇᴡ ɢʀᴏᴜᴘ ɴᴀᴍᴇ ᴄʜᴀɴɢᴇᴅ !\nʙʏ** {}</blockquote>".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "<blockquote>ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ **ᴄʜᴀɴɢᴇ ɪɴғᴏ** ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ !</blockquote>"
            )
    elif len(message.command) > 1:
        try:
            title = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_title(title)
                await msg.edit(
                    "<blockquote>**ɴᴇᴡ ɢʀᴏᴜᴘ ɴᴀᴍᴇ ᴄʜᴀɴɢᴇᴅ !\nʙʏ** {}</blockquote>".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "<blockquote>**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ !**</blockquote>"
            )

    else:
        await msg.edit(
            "<blockquote>**ʏᴏᴜ ɴᴇᴇᴅ ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ **</blockquote>"
        )


@app.on_message(filters.command(["setdiscription", "setdesc"]))
@utils.adminsOnly("can_change_info")
async def setg_discription(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("<blockquote>**ᴘʀᴏᴄᴇssɪɴɢ...**</blockquote>")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("<blockquote>**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴ ɢʀᴏᴜᴘs!**</blockquote>")
    elif reply:
        try:
            discription = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit(
                    "<blockquote>**ɴᴇᴡ ᴅɪsᴄʀɪᴘᴛɪᴏɴ ᴏғ ɢʀᴏᴜᴘ ᴄʜᴀɴɢᴇᴅ!**\nʙʏ {}</blockquote>".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "<blockquote>**ᴛʜᴇ ᴜsᴇʀ ᴍᴜsᴛ ʜᴀᴠᴇ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛɪᴏɴ!**</blockquote>"
            )
    elif len(message.command) > 1:
        try:
            discription = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit(
                    "<blockquote>**ɴᴇᴡ ᴅɪsᴄʀɪᴘᴛɪᴏɴ ᴏғ ɢʀᴏᴜᴘ ᴄʜᴀɴɢᴇᴅ!**\nʙʏ {}</blockquote>".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "<blockquote>**ᴛʜᴇ ᴜsᴇʀ ᴍᴜsᴛ ʜᴀᴠᴇ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛɪᴏɴ!**</blockquote>"
            )
    else:
        await msg.edit(
            "<blockquote>**ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛᴏɴ!</blockquote>**"
        )
