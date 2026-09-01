"""Resize source Mari Summers art for Telegram and Discord.

Telegram static stickers: PNG, longest side exactly 512px, transparent.
Discord custom stickers: PNG, exactly 320x320, transparent, max 512KB.
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "imessage_stickers" / "StickerPackExtension" / "Stickers"
TELEGRAM_DIR = ROOT / "stickers" / "telegram"
DISCORD_DIR = ROOT / "stickers" / "discord"

STICKERS = [
    {
        "source": "Sticker1.png",
        "slug": "mari_badge",
        "emoji": "🏝️",
        "keywords": ["mari", "badge", "conference"],
        "discord_name": "mari_badge",
        "discord_tags": "island",
        "description": "Mari Summers conference badge",
    },
    {
        "source": "Sticker2.png",
        "slug": "mari_summers",
        "emoji": "✨",
        "keywords": ["mari", "summers", "name"],
        "discord_name": "mari_summers",
        "discord_tags": "sparkles",
        "description": "Mari Summers nameplate sticker",
    },
    {
        "source": "Sticker3.png",
        "slug": "mari_lookback",
        "emoji": "💖",
        "keywords": ["mari", "look", "heart"],
        "discord_name": "mari_lookback",
        "discord_tags": "heart",
        "description": "Mari Summers looking back",
    },
]


def fit_max_side(im: Image.Image, max_side: int) -> Image.Image:
    w, h = im.size
    if max(w, h) == max_side:
        return im
    if w >= h:
        size = (max_side, max(1, round(h * max_side / w)))
    else:
        size = (max(1, round(w * max_side / h)), max_side)
    return im.resize(size, Image.Resampling.LANCZOS)


def pad_square(im: Image.Image, size: int) -> Image.Image:
    fitted = fit_max_side(im, size)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x = (size - fitted.width) // 2
    y = (size - fitted.height) // 2
    canvas.paste(fitted, (x, y), fitted)
    return canvas


def save_png(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, format="PNG", optimize=True)
    size = path.stat().st_size
    if size > 512 * 1024:
        raise SystemExit(f"{path.name} is {size} bytes; Discord/Telegram limit is 512KB")


def prepare() -> list[dict]:
    TELEGRAM_DIR.mkdir(parents=True, exist_ok=True)
    DISCORD_DIR.mkdir(parents=True, exist_ok=True)
    prepared = []
    for item in STICKERS:
        src = SOURCE_DIR / item["source"]
        im = Image.open(src).convert("RGBA")
        tg_path = TELEGRAM_DIR / f"{item['slug']}.png"
        dc_path = DISCORD_DIR / f"{item['slug']}.png"
        save_png(fit_max_side(im, 512), tg_path)
        save_png(pad_square(im, 320), dc_path)
        prepared.append({**item, "telegram": tg_path, "discord": dc_path})
        print(f"{item['slug']}: telegram {Image.open(tg_path).size} {tg_path.stat().st_size}B, discord {Image.open(dc_path).size} {dc_path.stat().st_size}B")
    return prepared


if __name__ == "__main__":
    prepare()
