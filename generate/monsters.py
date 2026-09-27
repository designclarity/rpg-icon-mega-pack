"""Monsters category: slimes, skulls, bats, eyes, ghosts, spiders,
dragon eggs, tentacles, wisps."""
import itertools
from canvas import Canvas

SLIME_COLORS = [('green', 'n', 'N'), ('blue', 'b', 'B'), ('red', 'r', 'R'),
                ('purple', 'p', 'P'), ('gold', 'y', 'G'), ('shadow', 'x', 'e'),
                ('frost', 'm', 'M'), ('lava', 'o', 'R')]


def build_slimes(n=16):
    out = []
    faces = ['happy', 'angry']
    combos = _sample(list(itertools.product(SLIME_COLORS, faces)), n)
    for (cname, c, dc), face in combos:
        cv = Canvas()
        cv.ellipse(8, 10, 6, 4, c)
        cv.ellipse(8, 10, 6, 4, dc, fill=False)
        cv.set(5, 7, 'l'); cv.set(6, 6, 'l')
        if face == 'happy':
            cv.set(6, 10, 'K'); cv.set(10, 10, 'K')
            cv.hline(7, 9, 11, 'K')
        else:
            cv.set(6, 9, 'K'); cv.set(10, 9, 'K')
            cv.hline(6, 7, 8, 'K'); cv.hline(9, 10, 8, 'K')
        cv.finish()
        out.append((f"{cname}_slime_{face}", f"{cname.capitalize()} Slime ({face})", cv))
    return out


def _sample(combos, n):
    step = max(1, len(combos) // n)
    return combos[::step][:n]


def _skull(cv, kind, bone):
    dark = 'K'
    if kind == 'human':
        cv.disc(8, 7, 4, bone)
        cv.rect(6, 10, 10, 13, bone)
        cv.set(6, 8, dark); cv.set(10, 8, dark)
        cv.set(8, 9, dark)
        cv.vline(7, 11, 12, dark); cv.vline(9, 11, 12, dark)
    elif kind == 'horned':
        cv.disc(8, 8, 4, bone)
        cv.tri(4, 7, 3, 4, 'c', up=False)
        cv.tri(12, 7, 3, 4, 'c', up=False)
        cv.set(6, 8, dark); cv.set(10, 8, dark)
        cv.set(8, 10, dark)
    elif kind == 'beast':
        cv.ellipse(8, 8, 5, 4, bone)
        cv.set(5, 7, dark); cv.set(11, 7, dark)
        cv.tri(8, 12, 4, 3, bone, up=False)
    elif kind == 'small':
        cv.disc(8, 8, 3, bone)
        cv.set(7, 8, dark); cv.set(9, 8, dark)
        cv.set(8, 9, dark)
    elif kind == 'cracked':
        cv.disc(8, 7, 4, bone)
        cv.set(6, 8, dark); cv.set(10, 8, dark)
        for y in range(4, 9):
            cv.set(8 + (y % 2), y, dark)


def build_skulls(n=15):
    out = []
    kinds = ['human', 'horned', 'beast', 'small', 'cracked']
    bones = [('bone', 'c'), ('dark', 'k'), ('mossy', 'n')]
    combos = _sample(list(itertools.product(kinds, bones)), n)
    for kind, (bname, bc) in combos:
        cv = Canvas()
        _skull(cv, kind, bc)
        cv.finish()
        out.append((f"{bname}_skull_{kind}", f"{bname.capitalize()} Skull ({kind})", cv))
    return out


def build_bats(n=8):
    out = []
    colors = [('brown', 'T'), ('black', 'e'), ('red', 'R'), ('purple', 'P')]
    poses = ['up', 'down']
    combos = _sample(list(itertools.product(colors, poses)), n)
    for (cname, c), pose in combos:
        cv = Canvas()
        cv.disc(8, 8, 2, c)
        cv.set(7, 8, 'r'); cv.set(9, 8, 'r')
        if pose == 'up':
            cv.tri(3, 8, 5, 6, c, up=True)
            cv.tri(13, 8, 5, 6, c, up=True)
        else:
            cv.tri(3, 8, 5, 6, c, up=False)
            cv.tri(13, 8, 5, 6, c, up=False)
        cv.finish()
        out.append((f"{cname}_bat_{pose}", f"{cname.capitalize()} Bat (wings {pose})", cv))
    return out


def build_eyes(n=12):
    out = []
    colors = [('red', 'r'), ('blue', 'b'), ('green', 'n'),
              ('purple', 'p'), ('gold', 'y'), ('shadow', 'x')]
    combos = _sample(list(itertools.product(colors, ['round', 'slit'])), n)
    for (cname, c), pupil in combos:
        cv = Canvas()
        cv.ellipse(8, 8, 5, 4, 'c')
        cv.disc(8, 8, 2, c)
        if pupil == 'round':
            cv.set(8, 8, 'K')
        else:
            cv.vline(8, 6, 10, 'K')
        cv.set(7, 7, 'l')
        cv.set(3, 5, 'c'); cv.set(13, 5, 'c'); cv.set(3, 11, 'c'); cv.set(13, 11, 'c')
        cv.finish()
        out.append((f"floating_eye_{cname}_{pupil}", f"Floating Eye ({cname}, {pupil} pupil)", cv))
    return out


def build_ghosts(n=8):
    out = []
    colors = [('white', 'c'), ('blue', 'm'), ('green', 'n'), ('purple', 'p')]
    faces = ['boo', 'wail']
    combos = _sample(list(itertools.product(colors, faces)), n)
    for (cname, c), face in combos:
        cv = Canvas()
        cv.tri(8, 3, 7, 6, c, up=True)
        cv.rect(5, 8, 11, 12, c)
        for x in range(5, 12, 2):
            cv.set(x, 13, None)
        # wavy bottom
        for x in (5, 7, 9, 11):
            cv.set(x, 12, c)
        if face == 'boo':
            cv.set(6, 8, 'K'); cv.set(10, 8, 'K')
            cv.set(8, 10, 'K')
        else:
            cv.set(6, 8, 'K'); cv.set(10, 8, 'K')
            cv.ellipse(8, 10, 1, 2, 'K')
        cv.finish()
        out.append((f"{cname}_ghost_{face}", f"{cname.capitalize()} Ghost ({face})", cv))
    return out


def build_spiders(n=8):
    out = []
    colors = [('black', 'e'), ('red', 'R'), ('purple', 'P'), ('brown', 'W')]
    combos = _sample(list(itertools.product(colors, ['marked', 'plain'])), n)
    for (cname, c), variant in combos:
        cv = Canvas()
        cv.ellipse(8, 9, 3, 3, c)
        cv.disc(8, 5, 2, c)
        cv.set(7, 5, 'r'); cv.set(9, 5, 'r')
        for j, y in enumerate((6, 8, 10)):
            cv.set(4 - j, y, c); cv.set(12 + j, y, c)
        if variant == 'marked':
            cv.set(8, 9, 'r')
        cv.finish()
        out.append((f"{cname}_spider_{variant}", f"{cname.capitalize()} Spider ({variant})", cv))
    return out


def build_eggs(n=12):
    out = []
    colors = [('green', 'n'), ('blue', 'b'), ('red', 'r'),
              ('purple', 'p'), ('gold', 'y'), ('shadow', 'x')]
    patterns = ['spotted', 'zigzag']
    combos = _sample(list(itertools.product(colors, patterns)), n)
    for (cname, c), pattern in combos:
        cv = Canvas()
        cv.ellipse(8, 9, 4, 5, c)
        cv.set(6, 6, 'l')
        if pattern == 'spotted':
            cv.set(7, 8, 'K'); cv.set(10, 10, 'K'); cv.set(8, 12, 'K')
        else:
            for x in range(5, 12):
                cv.set(x, 9 + (x % 2), 'K')
        cv.finish()
        out.append((f"{cname}_dragon_egg_{pattern}", f"{cname.capitalize()} Dragon Egg ({pattern})", cv))
    return out


def build_tentacles(n=8):
    out = []
    colors = [('purple', 'P'), ('green', 'N'), ('red', 'R'), ('blue', 'B')]
    combos = _sample(list(itertools.product(colors, ['curl_left', 'curl_right'])), n)
    for (cname, c), direction in combos:
        cv = Canvas()
        for y in range(4, 14):
            x = 8 + (y - 9) // 2
            cv.hline(x - 1, x + 1, y, c)
        cv.set(6, 4, c)
        for y in range(6, 13, 2):
            cv.set(8 + (y - 9) // 2, y, 'v')
        if direction == 'curl_right':
            cv = cv.flip_h()
        cv.finish()
        out.append((f"{cname}_tentacle_{direction}", f"{cname.capitalize()} Tentacle ({direction.replace('_', ' ')})", cv))
    return out


def build_wisps(n=10):
    out = []
    colors = [('blue', 'b'), ('green', 'n'), ('purple', 'p'), ('gold', 'y'), ('red', 'r')]
    combos = _sample(list(itertools.product(colors, ['trail', 'no_trail'])), n)
    for (cname, c), variant in combos:
        cv = Canvas()
        cv.disc(8, 8, 3, c)
        cv.set(7, 7, 'l'); cv.set(8, 6, 'l')
        if variant == 'trail':
            cv.tri(8, 13, 4, 4, c, up=False)
        else:
            cv.set(8, 12, c); cv.set(8, 13, c)
        cv.set(8, 3, c)
        cv.finish()
        out.append((f"{cname}_wisp_{variant}", f"{cname.capitalize()} Wisp ({variant.replace('_', ' ')})", cv))
    return out


def build():
    icons = []
    icons += [("monsters/" + s, l, c) for s, l, c in build_slimes()]
    icons += [("monsters/" + s, l, c) for s, l, c in build_skulls()]
    icons += [("monsters/" + s, l, c) for s, l, c in build_bats()]
    icons += [("monsters/" + s, l, c) for s, l, c in build_eyes()]
    icons += [("monsters/" + s, l, c) for s, l, c in build_ghosts()]
    icons += [("monsters/" + s, l, c) for s, l, c in build_spiders()]
    icons += [("monsters/" + s, l, c) for s, l, c in build_eggs()]
    icons += [("monsters/" + s, l, c) for s, l, c in build_tentacles()]
    icons += [("monsters/" + s, l, c) for s, l, c in build_wisps()]
    return icons
