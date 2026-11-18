"""news-image-20261118 entry: hand in one image that sums up the world's news
of Wednesday 18 November 2026.

The image is the entry.png beside this file — a 1024x1024 poster drawn
programmatically (Pillow) from the day's reporting: the Shenzhen APEC
arrivals ahead of the first Trump-Xi-Putin trilateral as the lead, with the
US-Iran strikes in the Gulf, Ukraine's strike on the Crimea bridge, the US
losing measles-elimination status, the magnitude 6.0 Papua New Guinea
earthquake, the Knesset speaker vote and the trillion-dollar chemicals
report around it, under the day's full date. This program copies it to
/output/entry.png, as the starter's main.ts does. Pure Python standard
library, deterministic.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

MAX_BYTES = 1_048_576  # the gate's 1 MiB cap
MAX_SIDE = 1024        # the gate's 1024-by-1024 cap


def check_image(data: bytes) -> None:
    """Refuse to hand in an image the gate would mark invalid."""
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        width, height = struct.unpack(">II", data[16:24])  # the IHDR's first two fields
    elif data.startswith(b"\xff\xd8\xff"):
        width = height = 0  # a JPEG's dimensions sit in a later segment; the shipped file is a PNG
    else:
        raise ValueError("entry.png is neither a PNG nor a JPEG")
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"entry.png is {width}x{height}, over the 1024x1024 cap")


def main() -> None:
    data = (HERE / "entry.png").read_bytes()
    check_image(data)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUTPUT_DIR / "entry.png")


if __name__ == "__main__":
    main()
