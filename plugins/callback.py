import os
import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from .commands import start, BATCH
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *

@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m):
    await m.answer()

    # help text
    help_text = """**You need Help?? 🧐**

★ **Just Send me the Files I will Store File and give you Shareable Link.**

**You Can Use me in Channel too 😉**

★ **Make me Admin in your Channel with Edit Permission. Thats Enough Now Continue Uploading Files in Channel I Will Edit all Posts and add shareable Link URL Buttons**

**How to Enable Uploader Details in Caption**

★ **Use /mode Command to Change and Also you Can Use `/mode channel_id` to Control Caption for Channel Message.**"""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('Home 🏕', callback_data='home'),
            InlineKeyboardButton('About 📕', callback_data='about')
        ],
        [
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]
    ]

    # editing as help message
    await m.message.edit(
        text=help_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@Client.on_callback_query(filters.regex('^close$'))
async def close_cb(c, m):
    await m.message.delete()
    await m.message.reply_to_message.delete()


@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m):
    await m.answer()
    owner = await c.get_users(int(OWNER_ID))
    bot = await c.get_me()

    # about text
    about_text = f"""--**My Details :**--

🤖 𝐌𝐲 𝐍𝐚𝐦𝐞 : **{bot.mention(style='md')}**
    
📝 𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞 : **[Python 3](https://www.python.org/)**

🧰 𝐅𝐫𝐚𝐦𝐞𝐰𝐨𝐫𝐤 : **[Pyrogram](https://github.com/pyrogram/pyrogram)**

👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 : **{owner.mention(style='md')}**

📢 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 : **[HMTD Links](https://t.me/HMTD_Links)**

👥 𝐆𝐫𝐨𝐮𝐩 : **[HMTD Discussion Group](https://t.me/HMTD_Discussion_Group)**

🌐𝐒𝐨𝐮𝐫𝐜𝐞 𝐂𝐨𝐝𝐞 : **[Press Me 🥰](https://bit.ly/3z0Vckn)**
"""

    # creating buttons
    buttons = [
        [
            InlineKeyboardButton('Home 🏕', callback_data='home'),
            InlineKeyboardButton('Help 💡', callback_data='help')
        ],
        [
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]
    ]

    # editing message
    await m.message.edit(
        text=about_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex('^home$'))
async def home_cb(c, m):
    await m.answer()
    await start(c, m, cb=True)


@Client.on_callback_query(filters.regex('^done$'))
async def done_cb(c, m):
    BATCH.remove(m.from_user.id)
    c.cancel_listener(m.from_user.id)
    await m.message.delete()


@Client.on_callback_query(filters.regex('^delete'))
async def delete_cb(c, m):
    await m.answer()
    cmd, msg_id = m.data.split("+")
    chat_id = m.from_user.id if not DB_CHANNEL_ID else int(DB_CHANNEL_ID)
    message = await c.get_messages(chat_id, int(msg_id))
    await message.delete()
    await m.message.edit("**Deleted Files Successfully 👨‍✈️**")
