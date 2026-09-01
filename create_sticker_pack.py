"""
Create (or update) the Mari Summers Telegram sticker pack.

Needs TELEGRAM_BOT_TOKEN in .env. Optional TELEGRAM_USER_ID; if omitted,
the script uses the last person who sent /start to the bot.

    python prepare_stickers.py
    python create_sticker_pack.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

from prepare_stickers import prepare

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

PACK_TITLE = "Mari Summers"


def api(token: str, method: str, **kwargs) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    resp = requests.post(url, timeout=60, **kwargs)
    data = resp.json()
    return data


def require_token() -> str:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token or token == "your_bot_token_here":
        sys.exit("Set TELEGRAM_BOT_TOKEN in .env (from @BotFather).")
    return token


def bot_username(token: str) -> str:
    me = api(token, "getMe")
    if not me.get("ok"):
        sys.exit(f"getMe failed: {me}")
    username = me["result"]["username"]
    print(f"Bot: @{username}")
    return username


def resolve_user_id(token: str) -> int:
    raw = os.environ.get("TELEGRAM_USER_ID", "").strip()
    if raw:
        return int(raw)

    updates = api(token, "getUpdates", data={"timeout": 0})
    if not updates.get("ok"):
        sys.exit(f"getUpdates failed: {updates}")
    user_ids = []
    for update in updates.get("result", []):
        msg = update.get("message") or update.get("edited_message") or {}
        from_user = msg.get("from") or {}
        if from_user.get("id") and not from_user.get("is_bot"):
            user_ids.append(from_user["id"])
    if user_ids:
        user_id = user_ids[-1]
        print(f"Using Telegram user id {user_id} from the last message to the bot.")
        return user_id

    sys.exit(
        "No TELEGRAM_USER_ID in .env, and nobody has messaged the bot yet.\n"
        "Open Telegram, send /start to your bot, then run this script again.\n"
        "Or paste your numeric id from @userinfobot into TELEGRAM_USER_ID in .env."
    )


def pack_name(username: str) -> str:
    return f"MariSummers_by_{username}"


def build_files_and_stickers(prepared: list[dict]) -> tuple[dict, list[dict]]:
    files = {}
    stickers = []
    for i, item in enumerate(prepared, start=1):
        attach = f"sticker{i}"
        files[attach] = (f"{item['slug']}.png", item["telegram"].read_bytes(), "image/png")
        stickers.append(
            {
                "sticker": f"attach://{attach}",
                "format": "static",
                "emoji_list": [item["emoji"]],
                "keywords": item["keywords"],
            }
        )
    return files, stickers


def create_or_update(token: str, user_id: int, name: str, prepared: list[dict]) -> None:
    existing = api(token, "getStickerSet", data={"name": name})
    files, stickers = build_files_and_stickers(prepared)

    if existing.get("ok"):
        count = len(existing["result"].get("stickers") or [])
        print(f"Pack already exists with {count} sticker(s). Adding any new ones.")
        for i, sticker in enumerate(stickers, start=1):
            attach = f"sticker{i}"
            result = api(
                token,
                "addStickerToSet",
                data={
                    "user_id": user_id,
                    "name": name,
                    "sticker": json.dumps(
                        {
                            "sticker": f"attach://{attach}",
                            "format": sticker["format"],
                            "emoji_list": sticker["emoji_list"],
                            "keywords": sticker["keywords"],
                        }
                    ),
                },
                files={attach: files[attach]},
            )
            if result.get("ok"):
                print(f"  added {files[attach][0]}")
            else:
                print(f"  skip {files[attach][0]}: {result.get('description')}")
        return

    result = api(
        token,
        "createNewStickerSet",
        data={
            "user_id": user_id,
            "name": name,
            "title": PACK_TITLE,
            "sticker_type": "regular",
            "stickers": json.dumps(stickers),
        },
        files=files,
    )
    if not result.get("ok"):
        sys.exit(f"createNewStickerSet failed: {result}")
    print("Pack created.")


def main() -> None:
    token = require_token()
    username = bot_username(token)
    user_id = resolve_user_id(token)
    name = pack_name(username)
    prepared = prepare()
    create_or_update(token, user_id, name, prepared)
    print(f"Add the pack: https://t.me/addstickers/{name}")


if __name__ == "__main__":
    main()
