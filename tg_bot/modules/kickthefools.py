from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (
    ChatBannedRights,
    UserStatusLastMonth,
    UserStatusLastWeek,
)

from tg_bot.events import register


@register(pattern="^/kickthefools")
async def _(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not event.chat.admin_rights.ban_users:
        return
    if not admin and not creator:
        await event.reply("I am not admin here !")
        return
    c = 0
    kick_rights = ChatBannedRights(until_date=None, view_messages=True)
    await event.reply("Searching Participant Lists...")
    async for i in event.client.iter_participants(event.chat_id):

        if isinstance(i.status, UserStatusLastMonth):
            status = await event.client(
                EditBannedRequest(event.chat_id, i, kick_rights)
            )
            if not status:
                return
            c += 1

        if isinstance(i.status, UserStatusLastWeek):
            status = await event.client(
                EditBannedRequest(event.chat_id, i, kick_rights)
            )
            if not status:
                return
            c += 1

    required_string = "Successfully Kicked **{}** users"
    await event.reply(required_string.format(c))
