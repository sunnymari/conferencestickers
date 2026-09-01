# conferencestickers
On a budget but want to pass out stickers for your next conference ? This repo has the solution !!!!!

Mari Summers stickers for iMessage, Telegram, and Discord, generated from the same three PNGs.

## Telegram
```bash
pip install -r requirements.txt
python prepare_stickers.py
python create_sticker_pack.py
```
Needs `TELEGRAM_BOT_TOKEN` in `.env`. Send `/start` to your bot once (or set `TELEGRAM_USER_ID`). Pack files land in `stickers/telegram/` (longest side 512px).

## Discord
Discord stickers live on a server (not a public pack link). Upload-ready files are in `stickers/discord/` — exact 320×320 PNG, under 512KB.

- Manual: Server Settings → Stickers → Upload
- Or set `DISCORD_BOT_TOKEN` and `DISCORD_GUILD_ID` in `.env` and run `python upload_discord_stickers.py`

## iMessage
Open `imessage_stickers/MariSummersStickers.xcodeproj` in Xcode.
