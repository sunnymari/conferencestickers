# ✨BALLING ON A BUDGET✨

How I built Starcove Studios Roblox #RDC networking kit for $0

One of the most important lessons that shaped how I approach engineering didn't come from a computer science class or an engineering class.

It came from macroeconomics.

"We live in a society with infinite wants but limited resources."

That quote stuck with me, and it still shapes how I approach my work today.

In the gaming community, handing out swag and stickers is a huge part of the culture. It's how you meet people, how you're remembered, how you build community. But the Starcove Studios team is balling on a budget, so I asked myself:

How do I make stickers and business cards fun and engaging without spending a dollar on them?

The answer: make them virtual. ALL FREE.

Here's how it works:

1. HiHello is my actual digital business card, name, title, contact info, links. The QR code on my printed card and badge points here. This is the universal piece, it works for literally anyone regardless of what apps they use.

2. iMessage and Telegram are the two virtual sticker delivery systems, each one a different way for someone to get my "Mari Summers" character sticker onto their phone, native to whichever platform they already use.

The relationship between them matters. The sticker isn't a replacement for the business card, it's a memorable, shareable extension of it.

3. Someone scans the HiHello QR code to save my actual contact details, then separately adds the sticker because it's fun and keeps my name and brand visible in their chats long after the conference ends.

They each do a different job: HiHello is "here's how to actually reach me," and the stickers are "here's a piece of my brand that sticks around."

No print costs. No design agency. Just infinite wants, limited resources, and a little creativity.

If you're at RDC and want the sticker, come find me. I'll drop it in your DMs on the spot.

## Grab the stickers

**Telegram pack (scan or tap):** [https://t.me/addstickers/MariSummers_by_starcove_mari_bot](https://t.me/addstickers/MariSummers_by_starcove_mari_bot)

**QR code** (print this for the conference table):
[stickers/telegram/mari-summers-addstickers-qr.png](https://github.com/sunnymari/conferencestickers/blob/main/stickers/telegram/mari-summers-addstickers-qr.png)

Direct download: [raw PNG](https://raw.githubusercontent.com/sunnymari/conferencestickers/main/stickers/telegram/mari-summers-addstickers-qr.png)

Discord upload files: [stickers/discord/](https://github.com/sunnymari/conferencestickers/tree/main/stickers/discord)

## Build it yourself

Mari Summers stickers for iMessage, Telegram, and Discord, generated from the same three PNGs.

### Telegram
```bash
pip install -r requirements.txt
python prepare_stickers.py
python create_sticker_pack.py
```
Needs `TELEGRAM_BOT_TOKEN` in `.env`. Send `/start` to your bot once (or set `TELEGRAM_USER_ID`). Pack files land in `stickers/telegram/` (longest side 512px).

### Discord
Discord stickers live on a server (not a public pack link). Upload-ready files are in `stickers/discord/` — exact 320×320 PNG, under 512KB.

- Manual: Server Settings → Stickers → Upload
- Or set `DISCORD_BOT_TOKEN` and `DISCORD_GUILD_ID` in `.env` and run `python upload_discord_stickers.py`

### iMessage
Open `imessage_stickers/MariSummersStickers.xcodeproj` in Xcode.
