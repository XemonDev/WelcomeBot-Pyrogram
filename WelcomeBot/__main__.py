from pyrogram import Client, filters, idle
from pyrogram.types import Message
from typing import Callable
from pyrogram.client import Client
from WelcomeBot.config import API_HASH, API_ID, SESSION_STRING, SUDO_USERS, CHATS

import sqlite3
db = sqlite3.connect('welcome.db', check_same_thread=False)
db.row_factory = sqlite3.Row
cur = db.cursor()
app = Client(SESSION_STRING, API_ID, API_HASH)


def admin_only(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS and message.chat.id in CHATS:
            return await func(client, message)

    return decorator


def welcome_on(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if cur.execute("SELECT * FROM welcome").fetchone()['status'] == 'on' and message.chat.id in CHATS:
            return await func(client, message)

    return decorator


@app.on_message(filters.regex(r"^welcome (on|off)") & filters.group)
@admin_only
async def wlc(app: Client, msg: Message):
    CMD = msg.matches[0].group(1)
    status = cur.execute("SELECT * FROM welcome").fetchone()['status']
    if CMD != status:
        if CMD.lower() == 'on':
            cur.execute("UPDATE welcome SET status = 'on'")
            db.commit()
            await msg.reply('خوش امدگویی خودکار فعال شد')
        elif CMD.lower() == 'off':
            cur.execute("UPDATE welcome SET status = 'off'")
            db.commit()
            await msg.reply('خوش امدگویی خودکار خاموش شد')
        else:
            pass
    else:
        Cmds = {
            "on": "روشن",
            "off": "خاموش"
        }
        await msg.reply(f'خوش امدگویی خودکار از قبل {Cmds[CMD]} بود')


@app.on_message(filters.regex(r"setwelcome (\w.*)") & filters.group)
@admin_only
async def set_welcome(app: Client, msg: Message):
    wlc = msg.matches[0].group(1)
    if len(wlc) <= 70:
        cur.execute("UPDATE welcome SET welcome = '%s'" % wlc)
        db.commit()
        await msg.reply('متن خوش امدگویی به تنظیم شد:\n%s' % wlc)


@app.on_message(filters.new_chat_members & filters.group)
@welcome_on
async def joined(app: Client, msg: Message):
    welcome = cur.execute("SELECT * FROM welcome").fetchone()['welcome']
    if welcome is not None:
        await msg.reply(str(welcome))

app.start()
idle()
