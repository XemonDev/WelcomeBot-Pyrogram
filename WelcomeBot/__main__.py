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
        if cur.execute("SELECT * FROM welcome").fetchone()['welcome_status'] == 'on' and message.chat.id in CHATS:
            if message.from_user.id == message.new_chat_members[0].id:
                return await func(client, message)

    return decorator
def pro(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if cur.execute("SELECT * FROM welcome").fetchone()['profile_status'] == 'on' and message.chat.id in CHATS:
            return await func(client, message)

    return decorator

@app.on_message(filters.regex(r"^welcome (on|off)") & filters.group)
@admin_only
async def wlc(app: Client, msg: Message):
    CMD = msg.matches[0].group(1)
    status = cur.execute("SELECT * FROM welcome").fetchone()['welcome_status']
    if CMD != status:
        if CMD.lower() == 'on':
            cur.execute("UPDATE welcome SET welcome_status = 'on'")
            db.commit()
            await msg.reply('خوش امدگویی خودکار فعال شد')
        elif CMD.lower() == 'off':
            cur.execute("UPDATE welcome SET welcome_status = 'off'")
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
@app.on_message(filters.regex(r"^profile (on|off)") & filters.group)
@admin_only
async def profile(app: Client, msg: Message):
    CMD = msg.matches[0].group(1)
    status = cur.execute("SELECT * FROM welcome").fetchone()['profile_status']
    if CMD != status:
        if CMD.lower() == 'on':
            cur.execute("UPDATE welcome SET profile_status = 'on'")
            db.commit()
            await msg.reply('حالت اصل خودکار فعال شد')
        elif CMD.lower() == 'off':
            cur.execute("UPDATE welcome SET profile_status = 'off'")
            db.commit()
            await msg.reply('حالت اصل خودکار خاموش شد')
        else:
            pass
    else:
        Cmds = {
            "on": "روشن",
            "off": "خاموش"
        }
        await msg.reply(f'حالت اصل خودکار از قبل {Cmds[CMD]} بود')
@app.on_message(filters.command(['setp','تنظیم اصل'],['','/','!','#']) & filters.reply & filters.group)
async def set_profile(app: Client, msg: Message):
    reply = msg.reply_to_message
    t = reply.from_user.is_bot
    if reply.text is not None:
        if reply.from_user is not None:
            if t == False:
                if len(reply.text) < 20:
                    cur.execute("SELECT * FROM profile WHERE id = '%s'" % str(reply.from_user.id))
                    user = cur.fetchone()
                    if user is None:
                        cur.execute("INSERT INTO profile(id,profile) VALUES(%s,'%s')" % (str(reply.from_user.id),reply.text))
                        db.commit()
                    elif user is not None:
                        cur.execute("UPDATE profile SET profile = '%s' WHERE id = '%s'" % (reply.text,str(reply.from_user.id)))
                        db.commit()
                    await msg.reply("اصل کاربر ثبت شد")
                    
                
        
@app.on_message(filters.new_chat_members & filters.group)
@welcome_on
async def joined(app: Client, msg: Message):
    welcome = cur.execute("SELECT * FROM welcome").fetchone()['welcome']
    if welcome is not None:
        await msg.reply(str(welcome))
@app.on_message(filters.group & filters.reply & filters.command(['اصل بده','asl bede','asl'],[""]))
@pro
async def prf(app: Client,message: Message):
    cur.execute("SELECT * FROM profile WHERE id = '%s'" % message.reply_to_message.from_user.id)
    user = cur.fetchone()
    if user is not None:
        await message.reply("● اصل کاربر:\n%s" % user['profile'])
app.start()
idle()
