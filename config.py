import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "")  # ⚠️ Required
    API_HASH  = os.environ.get("API_HASH", "") # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") # ⚠️ Required
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "") # ⚠️ Required
   
    # database config
    DB_URL  = os.environ.get("mongodb+srv://Krishna:pss968048@cluster0.4rfuzro.mongodb.net/?retryWrites=true&w=majority","")  # ⚠️ Required
 
    # other configs
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    TG_MAX_SIZE = 2040108421
    BOT_UPTIME  = time.time()
    START_PIC   = os.environ.get("START_PIC", "")
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '').split()] # ⚠️ Required
    FORCE_SUB_TEXT = os.environ.get('FORCE_SUB_TEXT', "**Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ ᴏᴜʀ Bᴀᴄᴋ-ᴜᴘ ᴄʜᴀɴɴᴇʟ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ sᴏ ʏᴏᴜ ᴅᴏɴ'ᴛ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇ...\n\nIғ ʏᴏᴜ ᴡᴀɴᴛ ᴛʜᴇ ғɪʟᴇ, ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ '❆ Jᴏɪɴ Oᴜʀ Bᴀᴄᴋ-Uᴘ Cʜᴀɴɴᴇʟ ❆' ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴀɴᴅ ᴊᴏɪɴ ᴏᴜʀ ʙᴀᴄᴋ-ᴜᴘ ᴄʜᴀɴɴᴇʟ, ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ '↻ Tʀʏ Aɢᴀɪɴ' ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ...\n\nTʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇs...**")
    FORCE_SUB = os.environ.get('https://t.me/NDA_BATCH_FREE', '') # ⚠️ Required
    AUTH_CHANNEL = int(FORCE_SUB) if FORCE_SUB and id_pattern.search(
    FORCE_SUB) else None
    LOG_CHANNEL = int(os.environ.get("https://t.me/NDA_BATCH_FREE", "")) # ⚠️ Required

    
    # Mega User Account ⚠️ Only Set When you have Pro or Enterprise Mega Account
    MEGA_EMAIL = os.environ.get("MEGA_EMAIL")
    MEGA_PASSWORD = os.environ.get("MEGA_PASSWORD")

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))



class Txt(object):
    # part of text configuration
    START_TXT = """<b>Hello {} 👋,
━━━━━━━━━━━━━━━━━━━━━
Tʜɪs Bᴏᴛ Cᴀɴ Sᴇᴀʀᴄʜ PᴏʀɴHᴜʙ
Vɪᴅᴇᴏs & Dᴏᴡɴʟᴏᴀᴅ Tʜᴇᴍ Fᴏʀ Yᴏᴜ

Cᴀɴ Aʟsᴏ Dᴏᴡɴʟᴏᴀᴅ Fɪʟᴇs ᴛʜʀᴏᴜɢʜ
Lɪɴᴋ ᴏғ Mᴇɢᴀ & YᴏᴜTᴜʙᴇ
━━━━━━━━━━━━━━━━━━━━━
⚠️Tʜᴇ Bᴏᴛ Cᴏɴᴛᴀɪɴs 𝟷𝟾+ Cᴏɴᴛᴇɴᴛ
Sᴏ Kɪɴᴅʟʏ Aᴄᴄᴇss ɪᴛ ᴡɪᴛʜ Yᴏᴜʀ ᴏᴡɴ
Rɪsᴋ. Cʜɪʟᴅʀᴇɴ Pʟᴇᴀsᴇ Sᴛᴀʏ Aᴡᴀʏ."
Wᴇ ᴅᴏɴ'ᴛ ɪɴᴛᴇɴᴅ ᴛᴏ sᴘʀᴇᴀᴅ Pøʀɴᴏ-
-ɢʀᴀᴘʜʏ ʜᴇʀᴇ.  Iᴛ's Jᴜsᴛ ᴀ ʙᴏᴛ ғᴏʀ ᴀ"
ᴘᴜʀᴘᴏsᴇ ᴀs ᴍᴀɴʏ ᴏғ ᴛʜᴇᴍ ᴡᴀɴᴛᴇᴅ."
━━━━━━━━━━━━━━━━━━━━━
Click The Buttons Below To Search
"""

    ABOUT_TXT = """<b>╭───────────⍟
├🤖 ᴍy ɴᴀᴍᴇ : {}
├👨‍💻 Nᴇᴛᴡᴏʀᴋ : <a href=https://t.me/EquinoxNetwork>Eǫᴜɪɴᴏx Tᴇᴀᴍ</a>
├👑Cʜᴀᴛ Gʀᴏᴜᴘ : <a href=https://t.me/Equinox_Chats>Eǫᴜɪɴᴏx~Cʜᴀᴛs</a> 
├☃️ Sᴜᴘᴘᴏʀᴛ  : <a href=https://t.me/equinoxSupport>•Sᴜᴘᴘᴏʀᴛ•</a>
├📕 Lɪʙʀᴀʀy : <a href=https://github.com/pyrogram>Pyʀᴏɢʀᴀᴍ</a>
├✏️ Oᴡɴᴇʀ : <a href=https://t.me/Harshu_xd1>•Oᴡɴᴇʀ•</a>
├💾 Mʏ Dᴇᴠ: <a href=https://t.me/NomoreTymWaste>»PᴀPᴀ«</a>
├🌀 Eǫᴜɪɴᴏx Bᴏᴛs : <a href=https://t.me/Equinoxbots>Bᴏᴛs Hᴜʙ </a>
╰───────────────⍟ """

    HELP_TXT = """
Tʜɪs Bᴏᴛ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ Tᴏ Dᴏᴡɴʟᴏᴀᴅ Fᴏʟʟᴏᴡɪɴɢ Fɪʟᴇ ᴛʜʀᴏᴜɢʜ ʟɪɴᴋs:

⊚ YouTube
⊚ Mega
⊚ PornHub

❗ 𝗔𝗻𝘆 𝗢𝘁𝗵𝗲𝗿 𝗛𝗲𝗹𝗽 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 :- <a href=https://t.me/EquinoxSupport>•𝐄𝐐𝐔𝐈𝐍𝐎𝐗</a>
"""


    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""

