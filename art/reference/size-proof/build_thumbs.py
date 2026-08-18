#!/usr/bin/env python3
"""Build consistently framed, same-background thumbs for the size-proof page."""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image

SRC = Path("/Users/jacobroecker/code/waloyo/art/reference/size-proof/stills")
OUT = Path("/Users/jacobroecker/code/waloyo/art/reference/size-proof/thumbs")
OUT.mkdir(parents=True, exist_ok=True)

# Light field so earth-tone figures keep contrast at icon size.
# Not parchment texture — a flat cream, same on every still.
FIELD = (247, 242, 232, 255)

STILLS = [
    "warrior-front.jpg",
    "warrior-front-anime.jpg",
    "warrior-front-mace.jpg",
    "warrior-front-macuahuitl.jpg",
    "settler-front.jpg",
    "settler-front-anime.jpg",
]

# Headroom / side / foot as a fraction of the figure bbox.
# Larger slots get more air above the head; tokens get packed.
SLOTS = {
    320: dict(head=0.16, side=0.10, foot=0.07),
    256: dict(head=0.12, side=0.08, foot=0.06),
    100: dict(head=0.07, side=0.06, foot=0.05),
    64: dict(head=0.05, side=0.05, foot=0.04),
    32: dict(head=0.04, side=0.04, foot=0.03),
}


def dist2(a, b) -> int:
    return sum((x - y) * (x - y) for x, y in zip(a, b))


def edge_swatches(rgb: Image.Image, n: int = 24) -> list[tuple[int, int, int]]:
    w, h = rgb.size
    pts = []
    for i in range(n):
        t = i / max(n - 1, 1)
        pts.append((int(t * (w - 1)), 0))
        pts.append((int(t * (w - 1)), h - 1))
        pts.append((0, int(t * (h - 1))))
        pts.append((w - 1, int(t * (h - 1))))
    return [rgb.getpixel(p)[:3] for p in pts]


def is_field_color(rgb: tuple[int, int, int], swatches: list[tuple[int, int, int]]) -> bool:
    r, g, b = rgb
    mx, mn = max(r, g, b), min(r, g, b)
    # Flattened checkerboard: light, almost no chroma
    if mx > 200 and (mx - mn) < 28:
        return True
    # Near any sampled edge / parchment / peach
    return any(dist2(rgb, s) <= 48 * 48 for s in swatches)


def alpha_from_edges(im: Image.Image) -> Image.Image:
    """Flood from the frame edge through field colors; leftover is the figure."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    pix = rgb.load()
    swatches = edge_swatches(rgb)
    seen = bytearray(w * h)
    q = deque()

    def push(x: int, y: int) -> None:
        i = y * w + x
        if seen[i]:
            return
        if not is_field_color(pix[x, y], swatches):
            return
        seen[i] = 1
        q.append((x, y))

    for x in range(w):
        push(x, 0)
        push(x, h - 1)
    for y in range(h):
        push(0, y)
        push(w - 1, y)

    while q:
        x, y = q.popleft()
        if x > 0:
            push(x - 1, y)
        if x + 1 < w:
            push(x + 1, y)
        if y > 0:
            push(x, y - 1)
        if y + 1 < h:
            push(x, y + 1)

    # Soft edge: field-colored pixels next to figure become transparent too
    alpha = Image.new("L", (w, h), 255)
    ap = alpha.load()
    for y in range(h):
        row = y * w
        for x in range(w):
            if seen[row + x]:
                ap[x, y] = 0
            elif is_field_color(pix[x, y], swatches):
                # interior holes in cloth stay; only fade near already-cleared field
                nfield = 0
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and seen[ny * w + nx]:
                        nfield += 1
                if nfield:
                    ap[x, y] = 0
    return alpha


def figure_bbox(alpha: Image.Image, threshold: int = 16) -> tuple[int, int, int, int]:
    a = alpha.point(lambda v: 255 if v > threshold else 0)
    box = a.getbbox()
    if box is None:
        return (0, 0) + alpha.size
    return box


def framed_square(im: Image.Image, alpha: Image.Image, slot: int) -> Image.Image:
    spec = SLOTS[slot]
    l, t, r, b = figure_bbox(alpha)
    fw, fh = r - l, b - t
    head = int(fh * spec["head"])
    side = int(max(fw, fh) * spec["side"])
    foot = int(fh * spec["foot"])
    l2 = l - side
    r2 = r + side
    t2 = t - head
    b2 = b + foot
    # Square: grow the short axis. Extra height goes to headroom; extra width is even.
    bw, bh = r2 - l2, b2 - t2
    if bh > bw:
        extra = bh - bw
        l2 -= extra // 2
        r2 += extra - extra // 2
    elif bw > bh:
        extra = bw - bh
        t2 -= extra  # keep feet, add air above
    # Paste onto a canvas large enough, then crop the square
    rgba = im.convert("RGBA")
    rgba.putalpha(alpha)
    canvas_w = max(r2, rgba.size[0]) - min(l2, 0) + 8
    canvas_h = max(b2, rgba.size[1]) - min(t2, 0) + 8
    ox, oy = max(0, -l2), max(0, -t2)
    field = Image.new("RGBA", (canvas_w, canvas_h), FIELD)
    field.alpha_composite(rgba, (ox, oy))
    crop = (ox + l2, oy + t2, ox + r2, oy + b2)
    # clamp
    cw, ch = field.size
    x0, y0, x1, y1 = crop
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(cw, x1), min(ch, y1)
    tile = field.crop((x0, y0, x1, y1))
    if tile.size[0] != tile.size[1]:
        side_px = max(tile.size)
        sq = Image.new("RGBA", (side_px, side_px), FIELD)
        sq.paste(tile, ((side_px - tile.size[0]) // 2, side_px - tile.size[1]))
        tile = sq
    return tile.resize((slot, slot), Image.Resampling.LANCZOS)


def main() -> None:
    for name in STILLS:
        im = Image.open(SRC / name)
        print("mask", name, im.size)
        alpha = alpha_from_edges(im)
        stem = Path(name).stem
        alpha.save(OUT / f"{stem}-mask.png")
        for slot in SLOTS:
            tile = framed_square(im, alpha, slot)
            out = OUT / f"{stem}-{slot}.png"
            tile.save(out, "PNG")
            print(" ", out.name, tile.size)


if __name__ == "__main__":
    main()
