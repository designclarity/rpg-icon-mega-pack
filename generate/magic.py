"""Magic category: runes, orbs, scrolls, spellbooks, crystals."""
import itertools
from canvas import Canvas

RUNE_COLORS = [('ember', 'o'), ('frost', 'b'), ('venom', 'n'),
               ('shadow', 'p'), ('storm', 'm'), ('blood', 'r')]


def _rune_symbol(cv, symbol, c):
    if symbol == 'cross':
        cv.vline(8, 4, 12, c); cv.hline(5, 11, 8, c)
    elif symbol == 'x':
        for i in range(-3, 4):
            cv.set(8 + i, 8 + i, c); cv.set(8 + i, 8 - i, c)
    elif symbol == 'triangle':
        cv.tri(8, 4, 7, 8, c, up=True)
    elif symbol == 'square':
        cv.rect(5, 5, 11, 11, c, fill=False)
    elif symbol == 'zigzag':
        for i, y in enumerate(range(5, 12)):
            cv.set(5 + (i % 4 if i % 8 < 4 else 3 - i % 4), y, c)
    elif symbol == 'dots':
        for dx in (-2, 0, 2):
            for dy in (-2, 0, 2):
                cv.set(8 + dx, 8 + dy, c)
    elif symbol == 'star':
        cv.diamond(8, 8, 3, c)
        cv.hline(4, 12, 8, c)
    elif symbol == 'diamond':
        cv.diamond(8, 8, 3, c, fill=False)
        cv.set(8, 8, c)
    elif symbol == 'wave':
        for x in range(4, 13):
            import math
            cv.set(x, 8 + int(2 * math.sin((x - 4) / 8 * 6.28)), c)
    elif symbol == 'fork':
        cv.vline(8, 8, 12, c)
        cv.vline(6, 4, 8, c); cv.vline(10, 4, 8, c)
        cv.hline(6, 10, 8, c)
    elif symbol == 'spiral':
        cv.disc(8, 8, 3, c, fill=False)
        cv.disc(8, 8, 1, c)
        cv.set(11, 8, c)
    elif symbol == 'eye':
        cv.ellipse(8, 8, 4, 2, c, fill=False)
        cv.set(8, 8, c)


def build_runes(n=60):
    out = []
    symbols = ['cross', 'x', 'triangle', 'square', 'zigzag', 'dots',
               'star', 'diamond', 'wave', 'fork', 'spiral', 'eye']
    combos = _sample(list(itertools.product(symbols, RUNE_COLORS)), n)
    for symbol, (cname, c) in combos:
        cv = Canvas()
        cv.disc(8, 8, 6, 'k')
        cv.disc(8, 8, 6, 'e')
        cv.disc(8, 8, 5, 'k')
        _rune_symbol(cv, symbol, c)
        cv.finish()
        out.append((f"{cname}_rune_{symbol}", f"{cname.capitalize()} Rune ({symbol})", cv))
    return out


def _sample(combos, n):
    step = max(1, len(combos) // n)
    return combos[::step][:n]


def build_orbs(n=16):
    out = []
    colors = [('fire', 'o'), ('frost', 'b'), ('nature', 'n'), ('shadow', 'p'),
              ('arcane', 'm'), ('holy', 'y'), ('blood', 'r'), ('storm', 'a')]
    styles = ['plain', 'swirl']
    combos = _sample(list(itertools.product(colors, styles)), n)
    for (cname, c), style in combos:
        cv = Canvas()
        cv.disc(8, 8, 5, c)
        cv.set(6, 6, 'l'); cv.set(7, 5, 'l')
        if style == 'swirl':
            for dx, dy in ((1, -2), (2, 0), (1, 2), (-1, 2), (-2, 0), (-1, -2)):
                cv.set(8 + dx, 8 + dy, 'l')
        cv.finish()
        out.append((f"{cname}_orb_{style}", f"{cname.capitalize()} Orb ({style})", cv))
    return out


def build_scrolls(n=20):
    out = []
    styles = ['open', 'rolled', 'tied', 'torn', 'ancient']
    seals = [('wax_red', 'r'), ('wax_blue', 'b'), ('gold', 'g'), ('none', None)]
    combos = _sample(list(itertools.product(styles, seals)), n)
    for style, (sname, sc) in combos:
        cv = Canvas()
        if style == 'open':
            cv.rect(3, 5, 13, 11, 'c')
            cv.vline(3, 5, 11, 'C'); cv.vline(13, 5, 11, 'C')
            cv.hline(5, 11, 7, 'C'); cv.hline(5, 11, 9, 'C')
        elif style == 'rolled':
            cv.rect(3, 6, 13, 10, 'c')
            cv.ellipse(3, 8, 2, 2, 'C')
            cv.ellipse(13, 8, 2, 2, 'C')
        elif style == 'tied':
            cv.rect(5, 4, 11, 12, 'c')
            cv.hline(5, 11, 8, 'r')
            cv.set(8, 8, 'R')
        elif style == 'torn':
            cv.rect(3, 5, 13, 11, 'c')
            for x in range(4, 13, 2):
                cv.set(x, 11, None)
        elif style == 'ancient':
            cv.rect(3, 5, 13, 11, 'C')
            cv.hline(4, 12, 5, 't')
            cv.set(6, 8, 'W'); cv.set(10, 9, 'W')
        if sc:
            cv.disc(8, 8, 1, sc)
        cv.finish()
        out.append((f"{style}_scroll_{sname}", f"{style.capitalize()} Scroll ({sname.replace('_', ' ')})", cv))
    return out


def build_spellbooks(n=21):
    out = []
    covers = [('crimson', 'R'), ('azure', 'B'), ('emerald', 'N'),
              ('violet', 'P'), ('obsidian', 'e'), ('parchment', 'C'),
              ('teal', 'A')]
    emblems = ['star', 'moon', 'eye']
    combos = _sample(list(itertools.product(covers, emblems)), n)
    for (cname, cc), emblem in combos:
        cv = Canvas()
        cv.rect(4, 3, 12, 13, cc)
        cv.vline(4, 3, 13, 'K')
        cv.vline(5, 3, 13, 'c')  # pages edge
        cv.rect(4, 3, 5, 13, 'c')
        if emblem == 'star':
            cv.diamond(9, 8, 2, 'y')
        elif emblem == 'moon':
            cv.disc(9, 8, 2, 'l')
            cv.disc(10, 7, 2, cc)
        elif emblem == 'eye':
            cv.ellipse(9, 8, 2, 1, 'l')
            cv.set(9, 8, 'K')
        cv.finish()
        out.append((f"{cname}_spellbook_{emblem}", f"{cname.capitalize()} Spellbook ({emblem})", cv))
    return out


def build_crystals(n=30):
    out = []
    shapes = ['shard', 'cluster', 'prism', 'geode', 'obelisk']
    colors = [('ruby', 'r'), ('sapphire', 'b'), ('emerald', 'n'),
              ('amethyst', 'p'), ('topaz', 'y'), ('aqua', 'm')]
    combos = _sample(list(itertools.product(shapes, colors)), n)
    for shape, (cname, c) in combos:
        cv = Canvas()
        if shape == 'shard':
            cv.tri(8, 2, 6, 10, c, up=True)
            cv.vline(8, 3, 10, 'l')
        elif shape == 'cluster':
            cv.tri(6, 6, 5, 8, c, up=True)
            cv.tri(10, 4, 5, 10, c, up=True)
            cv.tri(8, 8, 4, 6, 'l', up=True)
        elif shape == 'prism':
            cv.diamond(8, 8, 4, c)
            cv.vline(8, 5, 11, 'l')
        elif shape == 'geode':
            cv.disc(8, 9, 5, 'k')
            cv.disc(8, 9, 3, c)
            cv.set(7, 8, 'l')
        elif shape == 'obelisk':
            cv.rect(6, 6, 10, 13, c)
            cv.tri(8, 2, 4, 4, c, up=True)
            cv.vline(7, 6, 12, 'l')
        cv.finish()
        out.append((f"{cname}_crystal_{shape}", f"{cname.capitalize()} Crystal ({shape})", cv))
    return out


def build():
    icons = []
    icons += [("magic/" + s, l, c) for s, l, c in build_runes()]
    icons += [("magic/" + s, l, c) for s, l, c in build_orbs()]
    icons += [("magic/" + s, l, c) for s, l, c in build_scrolls()]
    icons += [("magic/" + s, l, c) for s, l, c in build_spellbooks()]
    icons += [("magic/" + s, l, c) for s, l, c in build_crystals()]
    return icons
