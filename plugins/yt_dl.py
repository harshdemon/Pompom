import sys, time, os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.utils import download_progress_hook, get_thumbnail_url, run_async, ytdl_downloads, progress_for_pyrogram
from youtube_dl import DownloadError
import youtube_dl
import requests
import uuid
from config import Config

active_list = []
queue_links = {}
index = 0


async def down_multiple(bot, update, link_msg):
    global index
    user_id = update.from_user.id
    msg = await update.message.reply_text(f"**{index+1}. Link:-** {queue_links[user_id][index]}\n\nDownloading... Please Have Patience\n 𝙇𝙤𝙖𝙙𝙞𝙣𝙜...", disable_web_page_preview=True)

    # Set options for youtube-dl
    thumbnail = get_thumbnail_url(queue_links[user_id][index])
    ytdl_opts = {
        'format': 'best',
        'progress_hooks': [lambda d: download_progress_hook(d, msg, queue_links[user_id][index])],
    }
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        try:
            await run_async(ydl.download, [queue_links[user_id][index]])
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
                if thumbnail:
                    await bot.send_video(chat_id=update.from_user.id, video=f"{file}", thumb=thumbnail_filename, caption=f"**📁 File Name:- `{file}`\n\nHere Is your Requested Video 🔥**\n\nPowered By - @{Config.BOT_USERNAME}", progress=progress_for_pyrogram, progress_args=("\n⚠️ Please Wait...\n\n**Uploading Started...**", msg, time.time()))
                    os.remove(f"{file}")
                    os.remove(thumbnail_filename)
                    break
                else:
                    await bot.send_video(chat_id=update.from_user.id, video=f"{file}", caption=f"**📁 File Name:- `{file}`\n\nHere Is your Requested Video 🔥**\n\nPowered By - @{Config.BOT_USERNAME}", progress=progress_for_pyrogram, progress_args=("\n⚠️ Please Wait...\n\n**Uploading Started...**", msg, time.time()))
                    os.remove(f"{file}")
            except Exception as e:
                print("⚠️  ERROR:- ", e)
                break
        else:
            continue

    await msg.delete()
    
    if queue_links[user_id][index] == queue_links[user_id][len(queue_links[user_id])-1]:
        queue_links.pop(user_id)
        index = 0
        try:
            await update.message.reply_text(f"ALL LINKS DOWNLOADED SUCCESSFULLY ✅",  reply_to_message_id=link_msg.id)
            active_list.remove(user_id)
            return
        except:
            await update.message.reply_text(f"ALL LINKS DOWNLOADED SUCCESSFULLY ✅")
            active_list.remove(user_id)

    else:
        index += 1
        await down_multiple(bot, update, queue_links[user_id][index])
        

@Client.on_message(filters.regex(pattern=r"https://\S+"))
async def handle_yt_dl(bot: Client, cmd: Message):
    await cmd.reply_text("**Do you want to download this file ?**", reply_to_message_id=cmd.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔻 Download 🔻', callback_data='http_link')], [InlineKeyboardButton('🖇️ Add Multiple Links 🖇️', callback_data='multiple_http_link')]]))


@Client.on_callback_query(filters.regex('^http_link'))
async def handle_single_download(bot: Client, update: CallbackQuery):
    user_id = update.from_user.id

    if user_id in active_list:
        await update.message.edit("Sorry! You can download only one video at a time")
        return
    else:
        active_list.append(user_id)

    http_link = update.message.reply_to_message.text
    await ytdl_downloads(bot, update, http_link)
    active_list.remove(user_id)
    

@Client.on_callback_query(filters.regex('^multiple_http_link'))
async def handle_multiple_download(bot: Client, update: CallbackQuery):
    http_link = update.message.reply_to_message.text
    
    user_id = update.from_user.id

    if user_id in active_list:
        await update.message.edit("Sorry! You can download only one video at a time")
        return
    else:
        active_list.append(user_id)

    try:
        global queue_links
        user_id = update.from_user.id

        if user_id not in queue_links:
            queue_links.update({user_id: [http_link]})
            await update.message.delete()
            while True:
                link = await bot.ask(chat_id=user_id, text="🔗Send Link to add it to queue 🔗\n\nUse /done when you're done adding links to queue.", filters=filters.text, reply_to_message_id=update.message.id)

                if str(link.text).startswith("https"):
                    queue_links[user_id].append(link.text)
                    await update.message.reply_text("Successfully Added To Queue ✅", reply_to_message_id=link.id)

                elif link.text == "/done":
                    user = queue_links[user_id]
                    links = ""
                    for idx, link in enumerate(user):
                        links += f"{(idx+1)}. `{link}`\n"

                    links_msg = await update.message.reply_text(f"👤 <code>{update.from_user.first_name}</code>\n\n {links}")
                    break

                else:
                    await update.answer("⚠️ Please Send Valid Link !")
                    continue

        await update.message.reply_text("Downloading Started ✅\n\nPlease have patience while it's downloading it may take sometimes...")

        if user_id in queue_links:
            try:
                await down_multiple(bot, update, links_msg)
            except Exception as e:
                print('Error on line {}'.format(
                    sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
