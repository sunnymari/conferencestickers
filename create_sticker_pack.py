"""
Creates a Telegram sticker pack from a local PNG using the Bot API.

Setup:
    pip install requests python-dotenv

Usage:
    python create_sticker_pack.py
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # reads TELEGRAM_BOT_TOKEN from .env in this folder

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# --- fill these in ---
YOUR_TELEGRAM_USER_ID = 123456789          # get this from @userinfobot on Telegram
BOT_USERNAME = "your_bot_username_bot"     # must match the bot BotFather just registered
PACK_NAME = f"mari_summers_by_{BOT_USERNAME}"  # Telegram requires this "by_<bot>" suffix
PACK_TITLE = "Mari Summers"
STICKER_FILE = "telegram_mari_summers_sticker.png"
STICKER_EMOJI = "✨"


def create_pack():
    with open(STICKER_FILE, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/createNewStickerSet",
            data={
                "user_id": YOUR_TELEGRAM_USER_ID,
                "name": PACK_NAME,
                "title": PACK_TITLE,
                "sticker_format": "static",
                "stickers": (
                    '[{"sticker": "attach://sticker1", '
                    f'"emoji_list": ["{STICKER_EMOJI}"]}}]'
                ),
            },
            files={"sticker1": f},
        )
    result = resp.json()
    if result.get("ok"):
        print(f"Pack created: https://t.me/addstickers/{PACK_NAME}")
    else:
        print("Failed:", result)


def add_sticker(sticker_path: str, emoji: str):
    """Call this again with a new file to add more stickers to the same pack."""
    with open(sticker_path, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/addStickerToSet",
            data={
                "user_id": YOUR_TELEGRAM_USER_ID,
                "name": PACK_NAME,
                "sticker": f'{{"sticker": "attach://sticker1", "emoji_list": ["{emoji}"]}}',
            },
            files={"sticker1": f},
        )
    print(resp.json())


if __name__ == "__main__":
    create_pack()
