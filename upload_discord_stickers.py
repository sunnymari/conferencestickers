"""
Upload Mari Summers stickers to a Discord server.

Discord has no shareable public pack like Telegram. Stickers live on a
server (5 free slots, more with boosts). You also need Manage Expressions.

    python prepare_stickers.py
    python upload_discord_stickers.py

Needs DISCORD_BOT_TOKEN and DISCORD_GUILD_ID in .env. The bot must be in
that server with Create Expressions / Manage Expressions.

If you don't want a bot, upload the PNGs in stickers/discord/ by hand:
Server Settings → Stickers → Upload (exactly 320×320 PNG, under 512KB).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

from prepare_stickers import prepare

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
API = "https://discord.com/api/v10"


def require_creds() -> tuple[str, str]:
    token = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
    guild = os.environ.get("DISCORD_GUILD_ID", "").strip()
    if not token or not guild:
        sys.exit(
            "Discord stickers are ready in stickers/discord/ (320×320 PNG).\n"
            "To upload from this script, add DISCORD_BOT_TOKEN and DISCORD_GUILD_ID to .env.\n"
            "Or upload those PNGs in Discord: Server Settings → Stickers."
        )
    return token, guild


def existing_names(token: str, guild: str) -> set[str]:
    resp = requests.get(
        f"{API}/guilds/{guild}/stickers",
        headers={"Authorization": f"Bot {token}"},
        timeout=30,
    )
    if resp.status_code != 200:
        sys.exit(f"Could not list stickers ({resp.status_code}): {resp.text}")
    return {s["name"] for s in resp.json()}


def upload(token: str, guild: str, prepared: list[dict]) -> None:
    have = existing_names(token, guild)
    for item in prepared:
        if item["discord_name"] in have:
            print(f"skip {item['discord_name']} (already on the server)")
            continue
        with item["discord"].open("rb") as f:
            resp = requests.post(
                f"{API}/guilds/{guild}/stickers",
                headers={"Authorization": f"Bot {token}"},
                data={
                    "name": item["discord_name"],
                    "description": item["description"],
                    "tags": item["discord_tags"],
                },
                files={"file": (item["discord"].name, f, "image/png")},
                timeout=60,
            )
        if resp.status_code in (200, 201):
            print(f"uploaded {item['discord_name']}")
        else:
            print(f"failed {item['discord_name']} ({resp.status_code}): {resp.text}")


def main() -> None:
    token, guild = require_creds()
    prepared = prepare()
    upload(token, guild, prepared)


if __name__ == "__main__":
    main()
