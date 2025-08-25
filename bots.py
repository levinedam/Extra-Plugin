from pyrogram import enums, filters


@app.on_message(filters.command("bots") & filters.group)
async def bots(client, message):
    bot_list = []
    async for bot in app.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.BOTS
    ):
        bot_list.append(bot.user)

    total_bots = len(bot_list)
    if total_bots == 0:
        await message.reply_text("<blockquote>There are no bots in this group.</blockquote>")
        return

    header = f"**🤖 Bot List in {message.chat.title}**\n\n"
    bot_lines = "\n".join(
        [f"{i + 1}. @{bot.username}" for i, bot in enumerate(bot_list)]
    )
    footer = f"<blockquote>\n\n**Total Number of Bots:** {total_bots}</blockquote>"

    result_text = header + bot_lines + footer
    await app.send_message(message.chat.id, result_text)


@app.on_message(filters.command(["staff", "staffs"]) & filters.group)
async def staffs(client, message):
    owner_list = []
    admin_list = []

    async for member in app.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        staff = member.user
        staff_name = f"{staff.first_name} {staff.last_name or ''}".strip()
        staff_username = f"@{staff.username}" if staff.username else "No Username"

        if member.status == enums.ChatMemberStatus.OWNER:
            custom_title = member.custom_title if member.custom_title else "Owner"
            owner_list.append(f"{staff_name} ({staff_username}) - {custom_title}")
        elif member.status == enums.ChatMemberStatus.ADMINISTRATOR:
            custom_title = member.custom_title if member.custom_title else "Admin"
            admin_list.append(f"{staff_name} ({staff_username}) - {custom_title}")

    total_owners = len(owner_list)
    total_admins = len(admin_list)

    result_text = ""

    if total_owners > 0:
        result_text += "<blockquote>**👑 Owner(s)**\n"
        result_text += (
            "\n".join([f"{i + 1}: {owner}" for i, owner in enumerate(owner_list)])
            + "\n\n</blockquote>"
        )
    else:
        result_text += "<blockquote>**👑 Owner(s)**\nNo owner found.\n\n</blockquote>"

    if total_admins > 0:
        result_text += "<blockquote>**👮‍♂️ Admin(s)**\n"
        result_text += (
            "\n".join([f"{i + 1}: {admin}" for i, admin in enumerate(admin_list)])
            + "\n</blockquote>"
        )
    else:
        result_text += "<blockquote>**👮‍♂️ Admin(s)**\nNo admins found.\n</blockquote>"

    await app.send_message(message.chat.id, result_text)


__MODULE__ = "Bots"
__HELP__ = """
<blockquote>• /bots - Get a list of bots in the group.
• /staffs - Get a list of staff members (owners & admins) in the group.</blockquote>
"""
