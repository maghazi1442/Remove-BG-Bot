# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by Annajiyah Media Center

import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API = os.environ["REMOVEBG_API"]
IMG_PATH = "./DOWNLOADS"

FayasNoushad = Client(
    "Remove Background Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
)

START_TEXT = """
بسم الله الرحمن الرحيم
Selamat bergabung ikhwah fillah {},saya bot penghapus latar belakang gambar. Kirimi saya gambar maka Saya akan membantu menghapus latar belakang semampu saya.

"""
HELP_TEXT = """
- Kirimkan gambar ke bot ini
- Saya akan membantu menghapus latar belakang
- Saya akan mengirim foto tanpa latar belakang

"Jangan Lupa Untuk Mendoakan Kemenangan Islam Dan Kaum Muslimin"

Dibuat Oleh : #Annajiyah_Media_Center
"""
ABOUT_TEXT = """
- **Bot :** `Penghapus Background Bot`


"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('channel', url='https://t.me/+SanO-EuVn-NjODQx'),
        InlineKeyboardButton('contact', url='http://t.me/Annajiyahmediacenter0')
        ],[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ERROR_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Join Updates Channel', url='https://t.me/+SanO-EuVn-NjODQx')
        ]]
    )

@FayasNoushad.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()

@FayasNoushad.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )

@FayasNoushad.on_message(filters.private & (filters.photo | filters.document))
async def remove_background(bot, update):
    if not API:
        await update.reply_text(
            text="Error :- Remove BG Api is error",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )
        return
    await update.reply_chat_action("typing")
    message = await update.reply_text(
        text="Bismillah Sedang Proses",
        quote=True,
        disable_web_page_preview=True
    )
    if (update and update.media and (update.photo or (update.document and "image" in update.document.mime_type))):
        file_name = IMG_PATH + "/" + str(update.from_user.id) + "/" + "image.jpg"
        new_file_name = IMG_PATH + "/" + str(update.from_user.id) + "/" + "no_bg.png"
        await update.download(file_name)
        await message.edit_text(
            text="Gambar selesai di hapus dan ikhwah dapat mendownloadnya..",
            disable_web_page_preview=True
        )
        try:
            new_image = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": open(file_name, "rb")},
                data={"size": "auto"},
                headers={"X-Api-Key": API}
            )
            if new_image.status_code == 200:
                with open(f"{new_file_name}", "wb") as image:
                    image.write(new_image.content)
            else:
                await update.reply_text(
                    text="API is error.",
                    quote=True,
                    reply_markup=ERROR_BUTTONS
                )
                return
            await update.reply_chat_action("upload_photo")
            await update.reply_document(
                document=new_file_name,
                quote=True
            )
            await message.delete()
            try:
                os.remove(file_name)
            except:
                pass
        except Exception as error:
            print(error)
            await message.edit_text(
                text="Something went wrong! May be API limits.",
                disable_web_page_preview=True,
                reply_markup=ERROR_BUTTONS
            )
    else:
        await message.edit_text(
            text="Media not supported",
            disable_web_page_preview=True,
            reply_markup=ERROR_BUTTONS
        )

FayasNoushad.run()
