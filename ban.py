import asyncio
from contextlib import suppress
from string import ascii_lowercase
from typing import Union

from config import BANNED_USERS
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import (
    CallbackQuery,
    ChatPermissions,
    ChatPrivileges,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from damMusic import app
from damMusic.core.mongo import mongodb
from damMusic.misc import SUDOERS
from damMusic.utils.database import save_filter
from damMusic.utils.functions import (
    extract_user,
    extract_user_and_reason,
    time_converter,
)
from damMusic.utils.keyboard import ikb

warnsdb = mongodb.warns

__MODULE__ = "Bᴀɴ"
__HELP__ = """
<blockquote expandable>/ban - Ban A User
/sban - Delete all messages of user that sended in group and ban the user
/tban - Ban A User For Specific Time
/unban - Unban A User
/warn - Warn A User
/swarn - Delete all the message sended in group and warn the user
/rmwarns - Remove All Warning of A User
/warns - Show Warning Of A User
/kick - Kick A User
/skick - Delete the replied message kicking its sender
/purge - Purge Messages
/purge [n] - Purge "n" number of messages from replied message
/del - Delete Replied Message
/promote - Promote A Member
/fullpromote - Promote A Member With All Rights
/demote - Demote A Member
/pin - Pin A Message
/unpin - unpin a message
/unpinall - unpinall messages
/mute - Mute A User
/tmute - Mute A User For Specific Time
/unmute - Unmute A User
/zombies - Ban Deleted Accounts
/report | @admins | @admin - Report A Message To Admins.
/link - Send in Group/SuperGroup Invite Link.</blockquote>"""


async def int_to_alpha(user_id: int) -> str:
    alphabet = list(ascii_lowercase)[:10]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text


async def get_warns_count() -> dict:
    chats_count = 0
    warns_count = 0
    async for chat in warnsdb.find({"chat_id": {"$lt": 0}}):
        for user in chat["warns"]:
            warns_count += chat["warns"][user]["warns"]
        chats_count += 1
    return {"chats_count": chats_count, "warns_count": warns_count}


async def get_warns(chat_id: int) -> dict[str, int]:
    warns = await warnsdb.find_one({"chat_id": chat_id})
    if not warns:
        return {}
    return warns["warns"]


async def get_warn(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    if name in warns:
        return warns[name]


async def add_warn(chat_id: int, name: str, warn: dict):
    name = name.lower().strip()
    warns = await get_warns(chat_id)
    warns[name] = warn

    await warnsdb.update_one(
        {"chat_id": chat_id}, {"$set": {"warns": warns}}, upsert=True
    )


async def remove_warns(chat_id: int, name: str) -> bool:
    warnsd = await get_warns(chat_id)
    name = name.lower().strip()
    if name in warnsd:
        del warnsd[name]
        await warnsdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"warns": warnsd}},
            upsert=True,
        )
        return True
    return False


@app.on_message(filters.command(["kick", "skick"]) & ~filters.private & ~BANNED_USERS)
@utils.adminsOnly("can_restrict_members")
async def kickFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ")
    if user_id == app.id:
        return await message.reply_text("<blockquote>ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴍʏsᴇʟғ, ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ ɪғ ʏᴏᴜ ᴡᴀɴᴛ.</blockquote>")
    if user_id in SUDOERS:
        return await message.reply_text("<blockquote>ʏᴏᴜ ᴡᴀɴɴᴀ ᴋɪᴄᴋ ᴛʜᴇ ᴇʟᴇᴠᴀᴛᴇᴅ ᴏɴᴇ ?</blockquote>")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "<blockquote>ɪ ᴄᴀɴ'ᴛ ᴋɪᴄᴋ ᴀɴ ᴀᴅᴍɪɴ, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇs, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇs, sᴏ ᴅᴏ ɪ </blockquote>"
        )
    mention = (await app.get_users(user_id)).mention
    msg = f"""
<blockquote expandable>**ᴋɪᴄᴋᴇᴅ ᴜsᴇʀ:** {mention}
**ᴋɪᴄᴋᴇᴅ ʙʏ:** {message.from_user.mention if message.from_user else 'ᴀɴᴏɴᴍᴏᴜs'}
**ʀᴇᴀsᴏɴ:** {reason or 'ɴᴏ ʀᴇᴀsᴏɴ ᴘʀᴏᴠɪᴅᴇᴅ'}</blockquote>"""
    await message.chat.ban_member(user_id)
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg)
    await asyncio.sleep(1)
    await message.chat.unban_member(user_id)
    if message.command[0][0] == "s":
        await message.reply_to_message.delete()
        await app.delete_user_history(message.chat.id, user_id)


# Ban members


@app.on_message(
    filters.command(["ban", "sban", "tban"]) & ~filters.private & ~BANNED_USERS
)
@utils.adminsOnly("can_restrict_members")
async def banFunc(_, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text("<blockquote>I can't find that user.</blockquote>")
    if user_id == app.id:
        return await message.reply_text("<blockquote>I can't ban myself, i can leave if you want.</blockquote>")
    if user_id in SUDOERS:
        return await message.reply_text("<blockquote>You Wanna Ban The Elevated One?, RECONSIDER!</blockquote>")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "<blockquote>I can't ban an admin, You know the rules, so do i.</blockquote>"
        )

    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )

    msg = (
        f"<blockquote expandable>**Banned User:** {mention}\n"
        f"**Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n</blockquote>"
    )
    if message.command[0][0] == "s":
        await message.reply_to_message.delete()
        await app.delete_user_history(message.chat.id, user_id)
    if message.command[0] == "tban":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_ban = await time_converter(message, time_value)
        msg += f"<blockquote expandable>**Banned For:** {time_value}\n"
        if temp_reason:
            msg += f"**Reason:** {temp_reason}</blockquote>"
        with suppress(AttributeError):
            if len(time_value[:-1]) < 3:
                await message.chat.ban_member(user_id, until_date=temp_ban)
                replied_message = message.reply_to_message
                if replied_message:
                    message = replied_message
                await message.reply_text(msg)
            else:
                await message.reply_text("<blockquote>You can't use more than 99</blockquote>")
        return
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.ban_member(user_id)
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg)


# Unban members


@app.on_message(filters.command("unban") & ~filters.private & ~BANNED_USERS)
@utils.adminsOnly("can_restrict_members")
async def unban_func(_, message: Message):
    # we don't need reasons for unban, also, we
    # don't need to get "text_mention" entity, because
    # normal users won't get text_mention if the user
    # they want to unban is not in the group.
    reply = message.reply_to_message
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("<blockquote>I can't find that user.</blockquote>")

    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await message.reply_text("<blockquote>You cannot unban a channel</blockquote>")

    await message.chat.unban_member(user_id)
    umention = (await app.get_users(user_id)).mention
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(f"<blockquote>Unbanned! {umention}</blockquote>")


# Promote Members


@app.on_message(
    filters.command(["promote", "fullpromote"]) & ~filters.private & ~BANNED_USERS
)
@utils.adminsOnly("can_promote_members")
async def promoteFunc(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("<blockquote>I can't find that user.</blockquote>")

    bot = (await app.get_chat_member(message.chat.id, app.id)).privileges
    if user_id == app.id:
        return await message.reply_text("<blockquote>I can't promote myself.</blockquote>")
    if not bot:
        return await message.reply_text("<blockquote>I'm not an admin in this chat.</blockquote>")
    if not bot.can_promote_members:
        return await message.reply_text("<blockquote>I don't have enough permissions</blockquote>")

    umention = (await app.get_users(user_id)).mention

    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id=user_id,
            privileges=ChatPrivileges(
                can_change_info=bot.can_change_info,
                can_invite_users=bot.can_invite_users,
                can_delete_messages=bot.can_delete_messages,
                can_restrict_members=bot.can_restrict_members,
                can_pin_messages=bot.can_pin_messages,
                can_promote_members=bot.can_promote_members,
                can_manage_chat=bot.can_manage_chat,
                can_manage_video_chats=bot.can_manage_video_chats,
            ),
        )
        return await message.reply_text(f"<blockquote>Fully Promoted! {umention}</blockquote>")

    await message.chat.promote_member(
        user_id=user_id,
        privileges=ChatPrivileges(
            can_change_info=False,
            can_invite_users=bot.can_invite_users,
            can_delete_messages=bot.can_delete_messages,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_chat=bot.can_manage_chat,
            can_manage_video_chats=bot.can_manage_video_chats,
        ),
    )
    await message.reply_text(f"<blockquote>Promoted! {umention}</blockquote>")


# Demote Member


@app.on_message(filters.command("purge") & ~filters.private)
@utils.adminsOnly("can_delete_messages")
async def purgeFunc(_, message: Message):
    repliedmsg = message.reply_to_message
    await message.delete()

    if not repliedmsg:
        return await message.reply_text("<blockquote>Reply to a message to purge from.</blockquote>")

    cmd = message.command
    if len(cmd) > 1 and cmd[1].isdigit():
        purge_to = repliedmsg.id + int(cmd[1])
        if purge_to > message.id:
            purge_to = message.id
    else:
        purge_to = message.id

    chat_id = message.chat.id
    message_ids = []

    for message_id in range(
        repliedmsg.id,
        purge_to,
    ):
        message_ids.append(message_id)

        # Max message deletion limit is 100
        if len(message_ids) == 100:
            await app.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,  # For both sides
            )

            # To delete more than 100 messages, start again
            message_ids = []

    # Delete if any messages left
    if len(message_ids) > 0:
        await app.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )


@app.on_message(filters.command("del") & ~filters.private)
@utils.adminsOnly("can_delete_messages")
async def deleteFunc(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("<blockquote>Reply To A Message To Delete It</blockquote>")
    await message.reply_to_message.delete()
    await message.delete()


@app.on_message(filters.command("demote") & ~filters.private & ~BANNED_USERS)
@utils.adminsOnly("can_promote_members")
async def demote(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("<blockquote>I can't find that user.</blockquote>")
    if user_id == app.id:
        return await message.reply_text("<blockquote>I can't demote myself.</blockquote>")
    if user_id in SUDOERS:
        return await message.reply_text(
            "<blockquote>You wanna demote the elevated one?, RECONSIDER!</blockquote>"
        )
    try:
        member = await app.get_chat_member(message.chat.id, user_id)
        if member.status == ChatMemberStatus.ADMINISTRATOR:
            await message.chat.promote_member(
                user_id=user_id,
                privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=False,
                    can_delete_messages=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_chat=False,
                    can_manage_video_chats=False,
                ),
            )
            umention = (await app.get_users(user_id)).mention
            await message.reply_text(f"<blockquote>Demoted! {umention}</blockquote>")
        else:
            await message.reply_text("<blockquote>The person you mentioned is not an admin.</blockquote>")
    except Exception as e:
        await message.reply_text(e)


# Pin Messages


@app.on_message(filters.command(["unpinall"]) & filters.group & ~BANNED_USERS)
@utils.adminsOnly("can_pin_messages")
async def pin(_, message: Message):
    if message.command[0] == "unpinall":
        return await message.reply_text(
            "<blockquote>Aʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜɴᴘɪɴ ᴀʟʟ ᴍᴇssᴀɢᴇs?</blockquote>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ʏᴇs", callback_data="unpin_yes"),
                        InlineKeyboardButton(text="ɴᴏ", callback_data="unpin_no"),
                    ],
                ]
            ),
        )


@app.on_callback_query(filters.regex(r"unpin_(yes|no)"))
async def callback_query_handler(_, query: CallbackQuery):
    if query.data == "unpin_yes":
        await app.unpin_all_chat_messages(query.message.chat.id)
        return await query.message.edit_text("<blockquote>Aʟʟ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇs ʜᴀᴠᴇ ʙᴇᴇɴ ᴜɴᴘɪɴɴᴇᴅ.</blockquote>")
    elif query.data == "unpin_no":
        return await query.message.edit_text(
            "<blockquote>Uɴᴘɪɴ ᴏғ ᴀʟʟ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇs ʜᴀs ʙᴇᴇɴ ᴄᴀɴᴄᴇʟʟᴇᴅ.</blockquote>"
        )


@app.on_message(filters.command(["pin", "unpin"]) & ~filters.private & ~BANNED_USERS)
@utils.adminsOnly("can_pin_messages")
async def pin(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("<blockquote>Reply to a message to pin/unpin it.</blockquote>")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await message.reply_text(
            f"<blockquote>Unpinned [this]({r.link}) message.</blockquote>",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await message.reply(
        f"Pinned [this]({r.link}) message.",
        disable_web_page_preview=True,
    )
    msg = "Please check the pinned message: ~ " + f"[Check, {r.link}]"
    filter_ = dict(type="text", data=msg)
    await save_filter(message.chat.id, "~pinned", filter_)


# Mute members


@app.on_message(filters.command(["mute", "tmute"]) & ~filters.private & ~BANNED_USERS)
@utils.adminsOnly("can_restrict_members")
async def mute(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("<blockquote>I can't find that user.</blockquote>")
    if user_id == app.id:
        return await message.reply_text("<blockquote>I can't mute myself.</blockquote>")
    if user_id in SUDOERS:
        return await message.reply_text("<blockquote>You wanna mute the elevated one?, RECONSIDER!</blockquote>")
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "<blockquote>I can't mute an admin, You know the rules, so do i.</blockquote>"
        )
    mention = (await app.get_users(user_id)).mention
    keyboard = ikb({"🚨  Unmute  🚨": f"unmute_{user_id}"})
    msg = (
        f"<blockquote expandable>**Muted User:** {mention}\n"
        f"**Muted By:** {message.from_user.mention if message.from_user else 'Anon'}\n</blockquote>"
    )
    if message.command[0] == "tmute":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_mute = await time_converter(message, time_value)
        msg += f"<blockquote expandable>**Muted For:** {time_value}\n"
        if temp_reason:
            msg += f"**Reason:** {temp_reason}</blockquote>"
        try:
            if len(time_value[:-1]) < 3:
                await message.chat.restrict_member(
                    user_id,
                    permissions=ChatPermissions(),
                    until_date=temp_mute,
                )
                replied_message = message.reply_to_message
                if replied_message:
                    message = replied_message
                await message.reply_text(msg, reply_markup=keyboard)
            else:
                await message.reply_text("<blockquote>You can't use more than 99</blockquote>")
        except AttributeError:
            pass
        return
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(msg, reply_markup=keyboard)


@app.on_message(filters.command("unmute") & ~filters.private & ~BANNED_USERS)
@utils.adminsOnly("can_restrict_members")
async def unmute(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("<blockquote>I can't find that user.</blockquote>")
    await message.chat.unban_member(user_id)
    umention = (await app.get_users(user_id)).mention
    replied_message = message.reply_to_message
    if replied_message:
        message = replied_message
    await message.reply_text(f"Unmuted! {umention}")


@app.on_message(filters.command(["warn", "swarn"]) & ~filters.private & ~BANNED_USERS)
@utils.adminsOnly("can_restrict_members")
async def warn_user(_, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    chat_id = message.chat.id
    if not user_id:
        return await message.reply_text("<blockquote>ɪ ᴄᴀɴᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ</blockquote>")
    if user_id == app.id:
        return await message.reply_text("<blockquote>ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴍʏsᴇʟғ, ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ ɪғ ʏᴏᴜ ᴡᴀɴᴛ.</blockquote>")
    if user_id in SUDOERS:
        return await message.reply_text(
            "<blockquote>ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴍʏ ᴍᴀɴᴀɢᴇʀ's, ʙᴇᴄᴀᴜsᴇ ʜᴇ ᴍᴀɴᴀɢᴇ ᴍᴇ!</blockquote>"
        )
    if user_id in [
        member.user.id
        async for member in app.get_chat_members(
            chat_id=message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]:
        return await message.reply_text(
            "<blockquote>ɪ ᴄᴀɴ'ᴛ ᴡᴀʀɴ ᴀɴ ᴀᴅᴍɪɴ, ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ʀᴜʟᴇs sᴏ ᴅᴏ ɪ.</blockquote>"
        )
    user, warns = await asyncio.gather(
        app.get_users(user_id),
        get_warn(chat_id, await int_to_alpha(user_id)),
    )
    mention = user.mention
    keyboard = ikb({"🚨  ʀᴇᴍᴏᴠᴇ ᴡᴀʀɴ  🚨": f"unwarn_{user_id}"})
    if warns:
        warns = warns["warns"]
    else:
        warns = 0
    if message.command[0][0] == "s":
        await message.reply_to_message.delete()
        await app.delete_user_history(message.chat.id, user_id)
    if warns >= 2:
        await message.chat.ban_member(user_id)
        await message.reply_text(f"<blockquote>ɴᴜᴍʙᴇʀ ᴏғ ᴡᴀʀɴs ᴏғ {mention} ᴇxᴄᴇᴇᴅᴇᴅ, ʙᴀɴɴᴇᴅ!</blockquote>")
        await remove_warns(chat_id, await int_to_alpha(user_id))
    else:
        warn = {"warns": warns + 1}
        msg = f"""
<blockquote expandable>**ᴡᴀʀɴᴇᴅ ᴜsᴇʀ:** {mention}
**ᴡᴀʀɴᴇᴅ ʙʏ:** {message.from_user.mention if message.from_user else 'ᴀɴᴏɴᴍᴏᴜs'}
**ʀᴇᴀsᴏɴ :** {reason or 'ɴᴏ ʀᴇᴀsᴏɴ ᴘʀᴏᴠᴏᴅᴇᴅ'}
**ᴡᴀʀɴs:** {warns + 1}/3</blockquote>"""
        replied_message = message.reply_to_message
        if replied_message:
            message = replied_message
        await message.reply_text(msg, reply_markup=keyboard)
        await add_warn(chat_id, await int_to_alpha(user_id), warn)


@app.on_callback_query(filters.regex("unwarn_") & ~BANNED_USERS)
async def remove_warning(_, cq: CallbackQuery):
    from_user = cq.from_user
    chat_id = cq.message.chat.id
    permissions = await utils.member_permissions(chat_id, from_user.id)
    permission = "can_restrict_members"
    if permission not in permissions:
        return await cq.answer(
            "<blockquote>ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ\n"
            + f"ᴘᴇʀᴍɪssɪᴏɴ ɴᴇᴇᴅᴇᴅ: {permission}</blockquote>",
            show_alert=True,
        )
    user_id = cq.data.split("_")[1]
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if not warns or warns == 0:
        return await cq.answer("<blockquote>ᴜsᴇʀ ʜᴀs ɴᴏ ᴡᴀʀɴɪɴɢs.</blockquote>")
    warn = {"warns": warns - 1}
    await add_warn(chat_id, await int_to_alpha(user_id), warn)
    text = cq.message.text.markdown
    text = f"~~{text}~~\n\n"
    text += f"__ᴡᴀʀɴ ʀᴇᴍᴏᴠᴇᴅ ʙʏ {from_user.mention}__"
    await cq.message.edit(text)


@app.on_message(filters.command("rmwarns") & ~filters.private & ~BANNED_USERS)
@utils.adminsOnly("can_restrict_members")
async def remove_warnings(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("<blockquote>I can't find that user.</blockquote>")
    mention = (await app.get_users(user_id)).mention
    chat_id = message.chat.id
    warns = await get_warn(chat_id, await int_to_alpha(user_id))
    if warns:
        warns = warns["warns"]
    if warns == 0 or not warns:
        await message.reply_text(f"<blockquote>{mention} ʜᴀs ɴᴏ ᴡᴀʀɴɪɴɢs.</blockquote>")
    else:
        await remove_warns(chat_id, await int_to_alpha(user_id))
        await message.reply_text(f"<blockquote>ʀᴇᴍᴏᴠᴇᴅ ᴡᴀʀɴɪɴɢs ᴏғ {mention}.</blockquote>")


@app.on_message(filters.command("warns") & ~filters.private & ~BANNED_USERS)
@utils.capture_err
async def check_warns(_, message: Message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("<blockquote>ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.</blockquote>")
    warns = await get_warn(message.chat.id, await int_to_alpha(user_id))
    mention = (await app.get_users(user_id)).mention
    if warns:
        warns = warns["warns"]
    else:
        return await message.reply_text(f"<blockquote>{mention} ʜᴀs ɴᴏ ᴡᴀʀɴɪɴɢs.</blockquote>")
    return await message.reply_text(f"<blockquote>{mention} ʜᴀs {warns}/3 ᴡᴀʀɴɪɴɢs</blockquote>")


@app.on_message(filters.command("link") & ~BANNED_USERS)
@utils.adminsOnly("can_invite_users")
async def invite(_, message):
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        link = (await app.get_chat(message.chat.id)).invite_link
        if not link:
            link = await app.export_chat_invite_link(message.chat.id)
        text = f"<blockquote>ʜᴇʀᴇ's ᴛʜᴇ ɢʀᴏᴜᴘ ɪɴᴠɪᴛᴇ ʟɪɴᴋ \n\n{link}</blockquote>"
        if message.reply_to_message:
            await message.reply_to_message.reply_text(
                text, disable_web_page_preview=True
            )
        else:
            await message.reply_text(text, disable_web_page_preview=True)
