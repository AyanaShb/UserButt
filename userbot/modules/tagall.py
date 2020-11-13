from telethon.tl.types import ChannelParticipantsAdmins
from userbot.events import register
from userbot import CMD_HELP, bot

@register(outgoing=True, pattern="^.tagadmin$")
async def _(event):
    if event.fwd_from:
        return
    mentions = "Administrators in chat : "
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    #await event.delete()


@register(outgoing=True, pattern="^.tagall$")
async def _(event):
    if event.fwd_from:
        return
    mentions = "Hey there!"
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, 200000):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()
    
CMD_HELP.update({
    "tagall":
    "`.tagadmin`"
    "\nUsage: Lists all admin in a chat."
    "\n\n`.tagall`"
    "\nUsage: Lists all member in a chat."
})
