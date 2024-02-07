import asyncio
import os
import sys
import time
import uuid
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from youtube_dl import DownloadError
import youtube_dl
from config import Config
from helper.utils import (
    download_progress_hook,
    get_thumbnail_url,
    ytdl_downloads,
    get_porn_thumbnail_url,
    progress_for_pyrogram,
)


class Downloader:
    def __init__(self):
        self.queue_links = {}

    async def download_multiple(self, bot, update, link_msg):
        user_id = update.from_user.id

        for index, link in enumerate(self.queue_links[user_id]):

            msg = await update.message.reply_text(
                f"**{index+1}. Link:-** {link}\n\nDownloading... Please Have Patience\n 𝙇𝙤𝙖𝙙𝙞𝙣𝙜...",
                disable_web_page_preview = True
            )

            # Set options for youtube-dl
            if str(self.queue_links[user_id][index]).startswith("https://www.pornhub"):
                thumbnail = get_porn_thumbnail_url(
                    self.queue_links[user_id][index])
            else:
                thumbnail = get_thumbnail_url(self.queue_links[user_id][index])

            ytdl_opts = {
                'format': 'best',
                'progress_hooks': [lambda d: download_progress_hook(d, msg, self.queue_links[user_id][index])],
            }
            loop = asyncio.get_event_loop()

            with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
                try:
                    await loop.run_in_executor(None, ydl.download, [self.queue_links[user_id][index]])
                except DownloadError:
                    await msg.edit("Sorry, There was a problem with that particular video")
                    return

            # Generate a unique filename for the thumbnail
            unique_id = uuid.uuid4().hex
            if thumbnail:
                thumbnail_filename = f"p_hub_thumbnail_{unique_id}.jpg"

                # Download the thumbnail image
                response = requests.get(thumbnail)
                if response.status_code == 200:
                    with open(thumbnail_filename, 'wb') as f:
                        f.write(response.content)

            await msg.edit("⚠️ Please Wait...\n\n**Trying to Upload....**")

            for file in os.listdir('.'):
                if file.endswith(".mp4") or file.endswith('.mkv'):
                    try:
                        await self.send_video(bot, update, file, thumbnail_filename, msg)
                        break
                    except Exception as e:
                        await msg.edit("⚠️  ERROR:- ", e)
                        break
                else:
                    continue

            await msg.delete()
        try:
            return await update.message.reply_text(f"ALL LINKS DOWNLOADED SUCCESSFULLY ✅",  reply_to_message_id=link_msg.id)
        except:
            await update.message.reply_text(f"ALL LINKS DOWNLOADED SUCCESSFULLY ✅")

    async def send_video(self, bot, update, file, thumbnail_filename, msg):
        user_id = update.from_user.id
        if thumbnail_filename:
            await bot.send_video(
                chat_id=user_id,
                video=file,
                thumb=thumbnail_filename,
                caption=f"**📁 File Name:- `{file}`\n\nHere Is your Requested Video 🔥**\n\nPowered By - @{Config.BOT_USERNAME}",
                progress=progress_for_pyrogram,
                progress_args=(
                    "\n⚠️ Please Wait...\n\n**Uploading Started...**", msg, time.time())
            )
            os.remove(thumbnail_filename)
        else:
            await bot.send_video(
                chat_id=user_id,
                video=file,
                caption=f"**📁 File Name:- `{file}`\n\nHere Is your Requested Video 🔥**\n\nPowered By - @{Config.BOT_USERNAME}",
                progress=progress_for_pyrogram,
                progress_args=(
                    "\n⚠️ Please Wait...\n\n**Uploading Started...**", msg, time.time())
            )
        os.remove(file)


downloader = Downloader()


@Client.on_message(filters.regex(pattern=r"(?=.*https://)(?!.*\bmega\b).*"))
async def handle_yt_dl(bot: Client, cmd: Message):
    await cmd.reply_text("**Do you want to download this file ?**", reply_to_message_id=cmd.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔻 Download 🔻', callback_data='http_link')], [InlineKeyboardButton('🖇️ Add Multiple Links 🖇️', callback_data='multiple_http_link')]]))


@Client.on_callback_query(filters.regex('^http_link'))
async def handle_single_download(bot: Client, update: CallbackQuery):
    http_link = update.message.reply_to_message.text
    await ytdl_downloads(bot, update, http_link)


@Client.on_callback_query(filters.regex('^multiple_http_link'))
async def handle_multiple_download(bot: Client, update: CallbackQuery):
    http_link = update.message.reply_to_message.text

    user_id = update.from_user.id
    try:
        global queue_links
        user_id = update.from_user.id

        if user_id not in downloader.queue_links:
            downloader.queue_links.update({user_id: [http_link]})
            await update.message.delete()
            while True:
                link = await bot.ask(chat_id=user_id, text="🔗Send Link to add it to queue 🔗\n\nUse /done when you're done adding links to queue.", filters=filters.text, reply_to_message_id=update.message.id)

                if str(link.text).startswith("https"):
                    downloader.queue_links[user_id].append(link.text)
                    await update.message.reply_text("Successfully Added To Queue ✅", reply_to_message_id=link.id)
                elif link.text == "/done":
                    user = downloader.queue_links[user_id]
                    links = ""
                    for idx, link in enumerate(user):
                        links += f"{(idx+1)}. `{link}`\n"

                    links_msg = await update.message.reply_text(f"👤 <code>{update.from_user.first_name}</code>\n\n {links}")
                    break
                elif link.text == "/clear":
                    downloader.queue_links.pop(user_id)
                    await update.message.reply_text("Successfully Cleared ✅")
                    break
                else:
                    await update.answer("⚠️ Please Send Valid Link !")
                    continue

        await update.message.reply_text("Downloading Started ✅\n\nPlease have patience while it's downloading it may take sometimes...")

        if user_id in downloader.queue_links:
            try:
                await downloader.download_multiple(bot, update, links_msg)
            except Exception as e:
                print('Error on line {}'.format(
                    sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
