# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
"""Userbot help command"""

import asyncio

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.help(?: |$)(.*)")
async def help(event):
    """For .help command"""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            msg = await event.edit(str(CMD_HELP[args]))
        else:
            msg = await event.edit("Please specify a valid module name.")
    else:
        numb = 1
        string = "**Usage:** `.help` <module name>\n\n"
        for i in sorted(CMD_HELP):
            string += str(numb) + "• " + str(i) + "\n"
            numb = numb + 1
        msg = await event.edit(string)
    await asyncio.sleep(45)
    try:
        await msg.delete()
    except BaseException:
        return  # just in case if msg deleted first
