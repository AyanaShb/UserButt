"""Get Telegram Profile Picture and other information
and set as own profile.
Syntax: .clone @username"""
# Credits of Plugin @ViperAdnan and @mrconfused(revert)[will add sql soon]

import html
import os

from telethon.tl import functions
from telethon.tl.functions.account import (UpdateProfileRequest,UpdateUsernameRequest)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.photos import (DeletePhotosRequest,GetUserPhotosRequest,UploadProfilePhotoRequest)
from telethon.tl.types import MessageEntityMentionName,InputPhoto, MessageMediaPhoto, User, Chat

from userbot import ALIVE_NAME, CMD_HELP, DEFAULT_BIO, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "TeleBot"
DEFAULTUSERBIO = str(DEFAULT_BIO) if DEFAULT_BIO else "404: No bio found!˙"

@register(outgoing=True, pattern="^.clone(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    user_id = replied_user.user.id
    profile_pic = await event.client.download_profile_photo(
        user_id, TEMP_DOWNLOAD_DIRECTORY
    )
    first_name = html.escape(replied_user.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮"
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await event.edit("`Processing...`")
    await event.client(UpdateProfileRequest(first_name=first_name, last_name=last_name))
    await event.client(UpdateProfileRequest(about=user_bio))
    await event.client(UploadProfilePhotoRequest(await event.client.upload_file(profile_pic)))
    os.remove(profile_pic)
    await event.edit("Cloned Successfully")
    event.delete()
    event.client.send_message(event.chat_id, "Cloned Successfully", reply_to=reply_message)

@register(outgoing=True, pattern="^.revert$")
async def _(event):
    if event.fwd_from:
        return
    name = f"{DEFAULTUSER}"
    bio = f"{DEFAULTUSERBIO}"
    n = 1
    await event.edit("`Processing...`")
    pfplist = await event.client(GetUserPhotosRequest(user_id=event.from_id,offset=0,max_id=0,limit=n))
    input_photos = []
    for sep in pfplist.photos:
        input_photos.append(InputPhoto(id=sep.id,access_hash=sep.access_hash,file_reference=sep.file_reference))
    await event.client(DeletePhotosRequest(id=input_photos))
    await event.client(UpdateProfileRequest(first_name=name, last_name=""))
    await event.client(UpdateProfileRequest(about=bio))
    await event.edit("`succesfully reverted my account back`")


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id
                    or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
        return replied_user, None
    input_str = None
    try:
        input_str = event.pattern_match.group(1)
    except IndexError as e:
        return None, e
    if event.message.entities is not None:
        mention_entity = event.message.entities
        probable_user_mention_entity = mention_entity[0]
        if isinstance(probable_user_mention_entity, MessageEntityMentionName):
            user_id = probable_user_mention_entity.user_id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        try:
            user_object = await event.client.get_entity(input_str)
            user_id = user_object.id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        except Exception as e:
            return None, e
    if event.is_private:
        try:
            user_id = event.chat_id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        except Exception as e:
            return None, e
    try:
        user_object = await event.client.get_entity(int(input_str))
        user_id = user_object.id
        replied_user = await event.client(GetFullUserRequest(user_id))
        return replied_user, None
    except Exception as e:
        return None, e


CMD_HELP.update({
     "clone": ".clone <reply/@>.\
    \n**Usage: clone the replied user account.\
    \n\n.revert\
    \nUse - Reverts back to your profile which you have set in heroku.\
    "
})
