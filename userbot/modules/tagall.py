from telethon.tl.types import ChannelParticipantsAdmins
from userbot.events import register
from userbot import CMD_HELP

@register(outgoing=True, pattern="^.tagadmin$")
async def _(event):
    if event.fwd_from:
        return
    mentions = "Administrators in the chat : "
    chat = await event.get_input_chat()
    async for x in event.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    #await event.delete()


# Added to TeleBot by @its_xditya


#@telebot.on(admin_cmd(pattern=r"tagall", outgoing=True))
#@telebot.on(sudo_cmd(pattern=r"tagall", allow_sudo=True))
#async def _(event):
 #   if event.fwd_from:
  #      return
   # mentions = "Hey there!"
    #chat = await event.get_input_chat()
    #async for x in borg.iter_participants(chat, 100):
     #   mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    #await event.reply(mentions)
    #await event.delete()

 CMD_HELP.update({
    "tagall":
    "`.filters`"
    "\nUsage: Lists all active userbot filters in a chat."
    "\n\n`.filter` <keyword> <reply text> or reply to a message with .filter <keyword>"
    "\nUsage: Saves the replied message as a reply to the 'keyword'."
    "\nThe bot will reply to the message whenever 'keyword' is mentioned."
    "\nWorks with everything from files to stickers."
    "\n\n`.stop` <filter>"
    "\nUsage: Stops the specified filter."
    "\n\n`.rmbotfilters` <marie/rose>"
    "\nUsage: Removes all filters of admin bots (Currently supported: Marie, Rose and their clones.) in the chat."
})
