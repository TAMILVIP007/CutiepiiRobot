IBM_WATSON_CRED_URL = "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/bd6b59ba-3134-4dd4-aff2-49a79641ea15"
IBM_WATSON_CRED_PASSWORD = "UQ1MtTzZhEsMGK094klnfa-7y_4MCpJY1yhd52MXOo3Y"
url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"

import re
import emoji
import aiohttp
import requests

from google_trans_new import google_translator
from pyrogram import filters

from Cutiepii_Robot import BOT_ID
from Cutiepii_Robot.modules.mongo.chatbot import add_chat, get_session, remove_chat
from Cutiepii_Robot.functions.pluginhelpers import admins_only, edit_or_reply
from Cutiepii_Robot import pgram as Cutiepii

translator = google_translator()


def extract_emojis(s):
    return "".join(c for c in s if c in emoji.UNICODE_EMOJI)


async def fetch(url):
    try:
        async with aiohttp.Timeout(10.0):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    try:
                        data = await resp.json()
                    except:
                        data = await resp.text()
            return data
    except:
        print("AI response Timeout")
        return


cutiepii_chats = []
en_chats = []

@Cutiepii.on_message(
    filters.command("chatbot") & ~filters.edited & ~filters.bot & ~filters.private
)
@admins_only
async def hmm(_, message):
    global cutiepii_chats
    if len(message.command) != 2:
        await message.reply_text(
            "I only recognize `/chatbot on` and /chatbot `off only`"
        )
        message.continue_propagation()
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    if status in ["ON", "on", "On"]:
        lel = await edit_or_reply(message, "`Processing...`")
        lol = add_chat(int(message.chat.id))
        if not lol:
            await lel.edit("Cutiepii AI Already Activated In This Chat")
            return
        await lel.edit(
            f"Cutiepii AI Successfully Added For Users In The Chat {message.chat.id}"
        )

    elif status in ["OFF", "off", "Off"]:
        lel = await edit_or_reply(message, "`Processing...`")
        Escobar = remove_chat(int(message.chat.id))
        if not Escobar:
            await lel.edit("Cutiepii AI Was Not Activated In This Chat")
            return
        await lel.edit(
            f"Cutiepii AI Successfully Deactivated For Users In The Chat {message.chat.id}"
        )

    elif status in ["EN", "en", "english"]:
        if chat_id not in en_chats:
            en_chats.append(chat_id)
            await message.reply_text("English AI chat Enabled!")
            return
        await message.reply_text("AI Chat Is Already Disabled.")
        message.continue_propagation()
    else:
        await message.reply_text(
            "I only recognize `/chatbot on` and /chatbot `off only`"
        )


@Cutiepii.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.edited
    & ~filters.via_bot
    & ~filters.forwarded,
    group=2,
)
async def hmm(client, message):
    if not get_session(int(message.chat.id)):
        return
    if not message.reply_to_message:
        return
    try:
        senderr = message.reply_to_message.from_user.id
    except:
        return
    if senderr != BOT_ID:
        return
    msg = message.text
    chat_id = message.chat.id
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    if chat_id in en_chats:
        test = msg
        test = test.replace("Cutiepii", "Aco")
        test = test.replace("Cutiepii", "Aco")
        URL = "https://api.affiliateplus.xyz/api/chatbot?message=hi&botname=@Cutiepii_Robot&ownername=@Awesome_Rj"

        try:
            r = requests.request("GET", url=URL)
        except:
            return

        try:
            result = r.json()
        except:
            return

        pro = result["message"]
    else:
        u = msg.split()
        emj = extract_emojis(msg)
        msg = msg.replace(emj, "")
        if (
            [(k) for k in u if k.startswith("@")]
            and [(k) for k in u if k.startswith("#")]
            and [(k) for k in u if k.startswith("/")]
            and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
        ):

            h = " ".join(filter(lambda x: x[0] != "@", u))
            km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
            tm = km.split()
            jm = " ".join(filter(lambda x: x[0] != "#", tm))
            hm = jm.split()
            rm = " ".join(filter(lambda x: x[0] != "/", hm))
        elif [(k) for k in u if k.startswith("@")]:

            rm = " ".join(filter(lambda x: x[0] != "@", u))
        elif [(k) for k in u if k.startswith("#")]:
            rm = " ".join(filter(lambda x: x[0] != "#", u))
        elif [(k) for k in u if k.startswith("/")]:
            rm = " ".join(filter(lambda x: x[0] != "/", u))
        elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
            rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
        else:
            rm = msg
            # print (rm)
        try:
            lan = translator.detect(rm)
        except:
            return
        test = rm
        if "en" not in lan and lan != "":
            try:
                test = translator.translate(test, lang_tgt="en")
            except:
                return
        # test = emoji.demojize(test.strip())

        # Kang with the credits bitches @InukaASiTH
        test = test.replace("Cutiepii", "Aco")
        test = test.replace("Cutiepii", "Aco")
        URL = f"https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@Cutiepii_Robot&ownername=@Awesome_Rj"
        try:
            r = requests.request("GET", url=URL)
        except:
            return

        try:
            result = r.json()
        except:
            return
        pro = result["message"]
        if "en" not in lan and lan != "":
            try:
                pro = translator.translate(pro, lang_tgt=lan[0])
            except:
                return
    try:
        await Cutiepii.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


@Cutiepii.on_message(
    filters.text & filters.private & ~filters.edited & filters.reply & ~filters.bot
)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
    except:
        return
    test = rm
    if "en" not in lan and lan != "":
        try:
            test = translator.translate(test, lang_tgt="en")
        except:
            return

    # test = emoji.demojize(test.strip())

    # Kang with the credits bitches @InukaASiTH
    test = test.replace("Cutiepii", "Aco")
    test = test.replace("Cutiepii", "Aco")
    URL = f"https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@Cutiepii_Robot&ownername=@Awesome_Rj"
    try:
        r = requests.request("GET", url=URL)
    except:
        return

    try:
        result = r.json()
    except:
        return

    pro = result["message"]
    if "en" not in lan and lan != "":
        pro = translator.translate(pro, lang_tgt=lan[0])
    try:
        await Cutiepii.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


@Cutiepii.on_message(
    filters.regex("Cutiepii|Cutiepii|Cutiepii|Cutiepii|Cutiepii")
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded
    & ~filters.reply
    & ~filters.channel
    & ~filters.edited
)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
    except:
        return
    test = rm
    if "en" not in lan and lan != "":
        try:
            test = translator.translate(test, lang_tgt="en")
        except:
            return

    # test = emoji.demojize(test.strip())

    # Kang with the credits bitches @InukaASiTH
    test = test.replace("Cutiepii", "Aco")
    test = test.replace("Cutiepii", "Aco")
    URL = f"https://api.affiliateplus.xyz/api/chatbot?message={test}&botname=@Cutiepii_Robot&ownername=@Awesome_Rj"
    try:
        r = requests.request("GET", url=URL)
    except:
        return

    try:
        result = r.json()
    except:
        return
    pro = result["message"]
    if "en" not in lan and lan != "":
        try:
            pro = translator.translate(pro, lang_tgt=lan[0])
        except Exception:
            return
    try:
        await Cutiepii.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


__help__ = """
<b> Chatbot </b>
Cutiepii AI 3.0 IS THE ONLY AI SYSTEM WHICH CAN DETECT & REPLY UPTO 200 LANGUAGES
  • /chatbot [ON/OFF]: Enables and disables AI Chat mode (EXCLUSIVE)
  • /chatbot EN : Enables English only chatbot
 
"""

__mod_name__ = "AI"
