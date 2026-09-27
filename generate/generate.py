#!/usr/bin/env python3
"""RPG Icon Mega-Pack - build script.
Collects all category modules, renders every icon at 32x32 and 64x64
(nearest-neighbor from the 16x16 masters), writes category contact
sheets, a preview, a category index, and a JSON index, then runs QA.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw, ImageFont

import weapons
import armor
import potions
import magic as magic_mod
import treasure
import monsters
import items
import ui

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG = (44, 32, 22, 255)
GOLD = (232, 179, 61, 255)
CREAM = (240, 224, 184, 255)

CATEGORIES = [
    ("weapons", "Weapons", weapons),
    ("armor", "Armor", armor),
    ("potions", "Potions & Consumables", potions),
    ("magic", "Magic", magic_mod),
    ("treasure", "Treasure", treasure),
    ("monsters", "Monsters", monsters),
    ("items", "Tools & Items", items),
    ("ui", "UI Elements", ui),
]


def fonts(big=44, small=22):
    try:
        fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", big)
        fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", small)
    except OSError:
        fb = ImageFont.load_default()
        fs = ImageFont.load_default()
    return fb, fs


def short_label(label, width=20):
    base = label.split(" (")[0]
    words, lines, cur = base.split(), [], ""
    for w in words:
        if len((cur + " " + w).strip()) <= width:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:2]


def contact_sheet(slug, title, count, icons, cols=8, cell=150, icon_px=80):
    rows = (len(icons) + cols - 1) // cols
    cell_h = 165
    W = cols * cell
    H = 130 + rows * cell_h
    sheet = Image.new("RGBA", (W, H), BG)
    dr = ImageDraw.Draw(sheet)
    fb, _ = fonts()
    try:
        fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except OSError:
        fs = ImageFont.load_default()
    dr.text((W // 2, 46), title, font=fb, anchor="mm", fill=GOLD)
    dr.text((W // 2, 88), f"{count} original icons - CC0 public domain",
            font=fs, anchor="mm", fill=CREAM)
    for idx, (path, label, cv) in enumerate(icons):
        cx = (idx % cols) * cell + cell // 2
        cy = 130 + (idx // cols) * cell_h
        big = cv.to_image(icon_px)
        sheet.alpha_composite(big, (cx - icon_px // 2, cy))
        for li, line in enumerate(short_label(label)):
            dr.text((cx, cy + icon_px + 8 + li * 22), line, font=fs,
                    anchor="ma", fill=CREAM)
    return sheet.convert("RGB")


def main():
    all_icons = []  # (path, label, canvas)
    by_cat = {}
    for slug, title, mod in CATEGORIES:
        icons = mod.build()
        # strip the "cat/" prefix the modules add; we track category separately
        clean = []
        for path, label, cv in icons:
            assert path.startswith(slug + "/"), f"{path} in wrong category {slug}"
            clean.append((path.split("/", 1)[1] + ".png", label, cv))
        by_cat[slug] = (title, clean)
        all_icons.extend([(slug, p, l, c) for p, l, c in clean])

    total = len(all_icons)
    print(f"total icons: {total}")
    assert total >= 1000, f"need >=1000 icons, got {total}"

    # ---- uniqueness QA ----
    slugs = [f"{cat}/{p}" for cat, p, _, _ in all_icons]
    assert len(set(slugs)) == total, "duplicate slugs!"
    sigs = [c.signature() for _, _, _, c in all_icons]
    dup = total - len(set(sigs))
    assert dup == 0, f"{dup} duplicate pixel signatures!"
    print("QA: slugs unique, pixel signatures unique")

    # ---- render ----
    for size, dname in ((32, "png32"), (64, "png64")):
        for cat, _, _ in CATEGORIES:
            os.makedirs(os.path.join(OUT, dname, cat), exist_ok=True)
    for cat, path, label, cv in all_icons:
        img32 = cv.to_image(32)
        img64 = cv.to_image(64)
        # validate image bytes by round-tripping through PNG in memory
        for img, dname in ((img32, "png32"), (img64, "png64")):
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            chk = Image.open(buf)
            chk.load()
            assert chk.size == img.size, "round-trip size mismatch"
        img32.save(os.path.join(OUT, "png32", cat, path))
        img64.save(os.path.join(OUT, "png64", cat, path))
    print("QA: all PNGs rendered and round-trip validated")

    # ---- contact sheets per category ----
    csdir = os.path.join(OUT, "contact-sheets")
    os.makedirs(csdir, exist_ok=True)
    for slug, (title, icons) in by_cat.items():
        sheet = contact_sheet(slug, f"{title.upper()} - {len(icons)} PIXEL ICONS",
                              len(icons), [(p, l, c) for p, l, c in icons])
        sheet.save(os.path.join(csdir, f"{slug}.png"))
    print(f"wrote {len(by_cat)} category contact sheets")

    # ---- preview.png: curated 8x8 sample across categories ----
    fb, fs = fonts()
    preview = Image.new("RGBA", (1200, 1200), BG)
    dr = ImageDraw.Draw(preview)
    dr.text((600, 52), "RPG ICON MEGA-PACK", font=fb, anchor="mm", fill=GOLD)
    dr.text((600, 94), f"{total}+ original pixel-art RPG icons - CC0 public domain",
            font=fs, anchor="mm", fill=CREAM)
    sample = []
    per = 64 // len(by_cat) + 1
    for slug, (title, icons) in by_cat.items():
        step = max(1, len(icons) // per)
        sample.extend(icons[::step][:per])
    sample = sample[:64]
    cols, cell = 8, 140
    top = 130
    for idx, (p, label, cv) in enumerate(sample):
        cx = (idx % cols) * cell + 110
        cy = top + (idx // cols) * cell
        big = cv.to_image(96)
        preview.alpha_composite(big, (cx - 48, cy))
    dr.text((600, 1140), "32x32 + 64x64 PNG - transparent - game-ready",
            font=fs, anchor="mm", fill=CREAM)
    preview.convert("RGB").save(os.path.join(OUT, "preview.png"))
    print("preview.png written")

    # ---- CATEGORY-INDEX.txt ----
    with open(os.path.join(OUT, "CATEGORY-INDEX.txt"), "w") as f:
        f.write("RPG ICON MEGA-PACK - CATEGORY INDEX\n")
        f.write(f"{total} original icons\n")
        f.write("=" * 60 + "\n\n")
        for slug, (title, icons) in by_cat.items():
            f.write(f"{title} ({len(icons)}) - png32/{slug}/, png64/{slug}/\n")
            f.write("-" * 60 + "\n")
            for p, label, _ in icons:
                f.write(f"  {p[:-4]:48s} {label}\n")
            f.write("\n")

    # ---- index.json ----
    idx = {"pack": "rpg-icon-mega-pack", "total": total, "categories": {}}
    for slug, (title, icons) in by_cat.items():
        idx["categories"][slug] = {
            "title": title,
            "count": len(icons),
            "icons": [{"file": p, "label": l} for p, l, _ in icons],
        }
    with open(os.path.join(OUT, "index.json"), "w") as f:
        json.dump(idx, f, indent=1)

    # ---- final on-disk QA ----
    import glob
    f32 = glob.glob(os.path.join(OUT, "png32", "*", "*.png"))
    f64 = glob.glob(os.path.join(OUT, "png64", "*", "*.png"))
    assert len(f32) == total, f"png32 count {len(f32)} != {total}"
    assert len(f64) == total, f"png64 count {len(f64)} != {total}"
    for p in f32 + f64:  # decode EVERY png on disk
        im = Image.open(p)
        im.load()
        assert im.mode == "RGBA", p
        assert im.size in ((32, 32), (64, 64)), (p, im.size)
        Image.open(p).load()
    print(f"QA: {len(f32)} files in png32/, {len(f64)} in png64/ - all valid")
    print("BUILD OK")


if __name__ == "__main__":
    main()
