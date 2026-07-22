#!/usr/bin/env python3
"""Create placeholder PNGs for missing Lovable __l5e assets."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

try:
    from PIL import Image, ImageDraw

    HAS_PIL = True
except Exception:
    HAS_PIL = False


def write_png(path: Path, w: int, h: int, rgba_fn) -> int:
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w):
            raw.extend(rgba_fn(x, y))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    data = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return len(data)


def main() -> None:
    print("HAS_PIL", HAS_PIL)
    targets = [
        (
            Path(
                r"E:/hermes/projects/bomb-defuser-site/__l5e/assets-v1/"
                r"368c6919-1b6a-4306-9501-b851af42c43e/raiku-logo.png"
            ),
            512,
            512,
            "logo",
        ),
        (
            Path(
                r"E:/hermes/projects/bomb-defuser-site/__l5e/assets-v1/"
                r"2a6b1b52-819a-4bad-8256-fe17ae1690f4/mascot-coding.png"
            ),
            768,
            768,
            "coding",
        ),
        (
            Path(
                r"E:/hermes/projects/bomb-defuser-site/__l5e/assets-v1/"
                r"89dbcd9a-ab31-4142-a833-ba2e2c49aa14/mascot-sleep.png"
            ),
            768,
            768,
            "sleep",
        ),
    ]

    if HAS_PIL:
        for path, w, h, kind in targets:
            img = Image.new("RGBA", (w, h), (10, 14, 12, 255))
            d = ImageDraw.Draw(img)
            green = (0, 255, 136, 255)
            dark = (6, 20, 14, 255)
            d.rounded_rectangle(
                [20, 20, w - 20, h - 20], radius=40, fill=dark, outline=green, width=6
            )
            if kind == "logo":
                d.ellipse(
                    [w // 2 - 120, h // 2 - 140, w // 2 + 120, h // 2 + 100],
                    fill=(20, 30, 24, 255),
                    outline=green,
                    width=8,
                )
                d.rectangle(
                    [w // 2 - 20, h // 2 - 170, w // 2 + 20, h // 2 - 130], fill=green
                )
                d.text((w // 2 - 70, h // 2 + 120), "RAIKU", fill=green)
            elif kind == "coding":
                d.ellipse(
                    [w // 2 - 160, h // 2 - 180, w // 2 + 160, h // 2 + 140],
                    fill=(30, 50, 40, 255),
                    outline=green,
                    width=6,
                )
                d.text((w // 2 - 90, h // 2 - 20), "</>", fill=green)
                d.text((w // 2 - 110, h // 2 + 160), "CODING", fill=green)
            else:
                d.ellipse(
                    [w // 2 - 160, h // 2 - 180, w // 2 + 160, h // 2 + 140],
                    fill=(30, 40, 50, 255),
                    outline=(120, 180, 255, 255),
                    width=6,
                )
                d.text((w // 2 - 80, h // 2 - 10), "zzz", fill=(180, 220, 255, 255))
                d.text((w // 2 - 90, h // 2 + 160), "SLEEP", fill=(180, 220, 255, 255))
            img.save(path, "PNG")
            print("PIL", path.name, path.stat().st_size)
    else:
        for path, w, h, kind in targets:

            def fn(x, y, kind=kind, w=w, h=h):
                r, g, b, a = 8, 16, 12, 255
                if x < 12 or y < 12 or x >= w - 12 or y >= h - 12:
                    return (0, 255, 136, 255)
                cx, cy = w // 2, h // 2
                dx, dy = x - cx, y - cy
                if dx * dx + dy * dy < (min(w, h) // 3) ** 2:
                    if kind == "sleep":
                        return (40, 60, 90, 255)
                    return (20, 40, 30, 255)
                if kind == "logo" and abs(x - cx) < 16 and cy - 160 < y < cy - 100:
                    return (0, 255, 136, 255)
                return (r, g, b, a)

            n = write_png(path, w, h, fn)
            print("RAW", path.name, n)

    for path, _, _, _ in targets:
        print(path.name, path.read_bytes()[:8])


if __name__ == "__main__":
    main()
