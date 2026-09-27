# RPG Icon Mega-Pack

**1,262 original fantasy pixel-art RPG icons — CC0 public domain.**

A complete, game-ready icon library for RPGs, roguelikes, dungeon crawlers,
idle games, and tabletop companions. Every icon ships as a transparent PNG
in two resolutions: **32x32** and **64x64**.

## Contents

| Folder           | What it is                                         |
|------------------|----------------------------------------------------|
| `png32/`         | 1,262 icons at 32x32 px (transparent PNG)          |
| `png64/`         | 1,262 icons at 64x64 px (transparent PNG)          |
| `contact-sheets/`| 8 per-category preview sheets + `preview.png`      |
| `CATEGORY-INDEX.txt` | Full list of every icon, grouped by category   |
| `index.json`     | Machine-readable index: filename, label, category  |

## Categories (1,262 icons total)

- **Weapons** (317) — swords, axes, bows, daggers, spears, staffs, maces, wands, hammers, crossbows
- **Armor** (161) — shields, helmets, chestplates, boots, gauntlets, pauldrons, belts, cloaks
- **Potions & Consumables** (174) — potion flasks, vials, elixirs, food, herbs
- **Magic** (147) — runes, orbs, scrolls, spellbooks, crystals
- **Treasure** (164) — coins, gems, chests, keys, rings, amulets, crowns
- **Monsters** (97) — slimes, skulls, bats, eyes, ghosts, spiders, dragon eggs, tentacles, wisps
- **Tools & Items** (122) — lanterns, tools, maps, compasses, bombs, arrows, vessels, camp gear, instruments, tomes, candles
- **UI Elements** (80) — hearts, mana, stars, arrows, status effects, buttons, banners, level gems

## How to use

1. Copy the `png32/` or `png64/` folders into your project.
2. File names are slugs, e.g. `steel_knight_helmet.png`, `healing_potion_flask.png`.
3. Use `index.json` to load icons by category at runtime (Unity, Godot, web, etc.).

Pixel art is authored on a 16x16 grid and exported with nearest-neighbor
scaling, so icons stay crisp at any multiple of 16.

## License

**CC0 1.0 Universal — public domain.** Use the icons in commercial games,
free games, videos, streams, and merchandise. No attribution required
(though it's appreciated). See `LICENSE-CC0.txt`.

## How these were made

These icons were **AI-assisted**: a program (included in the `generate/`
folder of the source project) authored each icon on a 16x16 pixel grid,
applied a consistent palette and dark-brown outline, and exported
nearest-neighbor PNGs at 32x32 and 64x64. Every design is original —
no third-party art, sprites, or IP were used. Automated QA verified that
all 1,262 icons are unique pixel artworks with no duplicates, and every
PNG was decoded and validated.

## Quality notes (honest)

- Icons are clean, readable pixel art in a consistent style — verified
  by automated checks and spot-checked visually by category sheet.
- A few abstract icons (runes, status effects, some tools) are stylized
  by design; they read best at 32px and above.
- No human hand-cleaning pass was performed on every icon; the pack is
  sold as-is under CC0.
