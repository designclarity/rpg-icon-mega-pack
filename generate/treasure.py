"""Treasure category: coins, gems, chests, keys, rings, amulets, crowns."""
import itertools
from canvas import Canvas

COIN_METS = [('gold', 'g', 'G'), ('silver', 's', 'd'), ('bronze', 'z', 'Z'),
             ('copper', 'o', 'O'), ('mithril', 'm', 'M')]


def build_coins(n=20):
    out = []
    piles = ['single', 'stack', 'pile', 'scattered']
    combos = _sample(list(itertools.product(COIN_METS, piles)), n)
    for (mname, mc, dc), pile in combos:
        cv = Canvas()
        if pile == 'single':
            cv.ellipse(8, 8, 4, 4, mc)
            cv.ellipse(8, 8, 3, 3, dc, fill=False)
            cv.set(8, 8, 'y' if mname == 'gold' else 'l')
        elif pile == 'stack':
            for i, y in enumerate((10, 8, 6)):
                cv.ellipse(8, y, 4, 2, mc)
                cv.hline(5, 11, y, dc if i else mc)
        elif pile == 'pile':
            cv.ellipse(8, 11, 6, 3, mc)
            cv.ellipse(7, 8, 4, 3, mc)
            cv.ellipse(9, 6, 3, 2, mc)
            cv.set(9, 5, 'l')
        elif pile == 'scattered':
            for dx, dy in [(-4, 2), (3, -1), (0, 4), (-1, -3), (4, 3)]:
                cv.ellipse(8 + dx, 8 + dy, 2, 2, mc)
        cv.finish()
        out.append((f"{mname}_coins_{pile}", f"{mname.capitalize()} Coins ({pile})", cv))
    return out


def _sample(combos, n):
    step = max(1, len(combos) // n)
    return combos[::step][:n]


GEM_COLORS = [('ruby', 'r', 'R'), ('sapphire', 'b', 'B'), ('emerald', 'n', 'N'),
              ('amethyst', 'p', 'P'), ('topaz', 'y', 'G'), ('aqua', 'm', 'M'),
              ('rose', 'v', 'V')]


def _gem(cv, cut, c, dc):
    if cut == 'round':
        cv.disc(8, 8, 5, c)
        cv.disc(8, 8, 3, dc)
        cv.set(6, 6, 'l'); cv.set(7, 5, 'l')
    elif cut == 'diamond':
        cv.diamond(8, 8, 5, c)
        cv.diamond(8, 8, 2, dc)
        cv.set(7, 6, 'l')
    elif cut == 'emerald':
        cv.rect(4, 6, 12, 11, c)
        cv.rect(6, 3, 10, 6, c)
        cv.hline(4, 12, 6, 'l')
    elif cut == 'triangle':
        cv.tri(8, 4, 9, 8, c, up=True)
        cv.tri(8, 5, 5, 5, 'l', up=True)
    elif cut == 'oval':
        cv.ellipse(8, 8, 4, 5, c)
        cv.ellipse(8, 8, 2, 3, dc)
        cv.set(7, 5, 'l')
    elif cut == 'hexagon':
        cv.disc(8, 8, 4, c)
        for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4)]:
            cv.set(8 + dx, 8 + dy, None)
        cv.set(6, 6, 'l')
    elif cut == 'shard':
        cv.tri(9, 3, 5, 9, c, up=True)
        cv.tri(6, 7, 4, 6, dc, up=True)
        cv.set(8, 5, 'l')


def build_gems(n=49):
    out = []
    cuts = ['round', 'diamond', 'emerald', 'triangle', 'oval', 'hexagon', 'shard']
    combos = _sample(list(itertools.product(cuts, GEM_COLORS)), n)
    for cut, (cname, c, dc) in combos:
        cv = Canvas()
        _gem(cv, cut, c, dc)
        cv.finish()
        out.append((f"{cname}_{cut}_gem", f"{cname.capitalize()} Gem ({cut})", cv))
    return out


def build_chests(n=16):
    out = []
    types = [('wooden', 'w', 'W'), ('ironbound', 'd', 'e'),
             ('golden', 'g', 'G'), ('darkwood', 'W', 'e')]
    styles = ['closed', 'open', 'locked', 'trapped']
    combos = _sample(list(itertools.product(types, styles)), n)
    for (tname, mc, dc), style in combos:
        cv = Canvas()
        if style == 'open':
            cv.rect(3, 8, 13, 13, mc)
            cv.rect(3, 3, 13, 7, dc)
            cv.rect(4, 9, 12, 12, 'e')
            cv.set(8, 9, 'y')
        else:
            cv.rect(3, 6, 13, 13, mc)
            cv.rect(3, 6, 13, 8, dc)
            cv.hline(3, 13, 6, 'l' if tname == 'golden' else mc)
            cv.rect(7, 8, 9, 11, 'g' if style == 'locked' else dc)
            if style == 'locked':
                cv.set(8, 9, 'K')
            if style == 'trapped':
                cv.set(5, 10, 'r'); cv.set(11, 10, 'r')
        cv.vline(3, 6, 13, dc)
        cv.finish()
        out.append((f"{tname}_chest_{style}", f"{tname.capitalize()} Chest ({style})", cv))
    return out


def build_keys(n=15):
    out = []
    bows = ['round', 'square', 'diamond', 'ornate', 'skull']
    teeth = ['single', 'double', 'triple']
    combos = _sample(list(itertools.product(bows, teeth)), n)
    for bow, teeth_n in combos:
        cv = Canvas()
        if bow == 'round':
            cv.disc(4, 8, 3, 'g', fill=False)
        elif bow == 'square':
            cv.rect(1, 5, 7, 11, 'g', fill=False)
        elif bow == 'diamond':
            cv.diamond(4, 8, 3, 'g', fill=False)
        elif bow == 'ornate':
            cv.disc(4, 8, 3, 'g', fill=False)
            cv.set(4, 8, 'r')
        elif bow == 'skull':
            cv.disc(4, 8, 3, 'c')
            cv.set(3, 8, 'K'); cv.set(5, 8, 'K')
        cv.hline(7, 14, 8, 'g')
        n_teeth = {'single': 1, 'double': 2, 'triple': 3}[teeth_n]
        for i in range(n_teeth):
            x = 11 + i * 2
            cv.vline(x, 8, 10, 'g')
        cv.finish()
        out.append((f"{bow}_key_{teeth_n}", f"{bow.capitalize()} Key ({teeth_n} teeth)", cv))
    return out


def build_rings(n=24):
    out = []
    bands = [('gold', 'g'), ('silver', 's'), ('bronze', 'z'), ('dark', 'e')]
    gems = [('ruby', 'r'), ('sapphire', 'b'), ('emerald', 'n'),
            ('none', None), ('diamond', 'l'), ('amethyst', 'p')]
    combos = _sample(list(itertools.product(bands, gems)), n)
    for (bname, bc), (gname, gc) in combos:
        cv = Canvas()
        cv.ellipse(8, 10, 4, 4, bc, fill=False)
        cv.ellipse(8, 10, 4, 4, bc, fill=False)
        # thicker band: two rings
        cv.ellipse(8, 10, 3, 3, bc, fill=False)
        if gc:
            cv.diamond(8, 4, 2, gc)
            cv.set(8, 3, 'l')
        cv.finish()
        g = f"_{gname}" if gname != 'none' else ""
        out.append((f"{bname}_ring{g}", f"{bname.capitalize()} Ring"
                    + (f" ({gname})" if gname != 'none' else ""), cv))
    return out


def build_amulets(n=25):
    out = []
    pendants = ['teardrop', 'circle', 'diamond', 'fang', 'coin']
    gems = [('ruby', 'r'), ('sapphire', 'b'), ('emerald', 'n'),
            ('amber', 'o'), ('amethyst', 'p')]
    combos = _sample(list(itertools.product(pendants, gems)), n)
    for pendant, (gname, gc) in combos:
        cv = Canvas()
        # chain
        for i, y in enumerate(range(2, 7)):
            cv.set(6 + (i % 2), y, 'g')
            cv.set(10 - (i % 2), y, 'g')
        if pendant == 'teardrop':
            cv.tri(8, 7, 5, 4, gc, up=True)
            cv.disc(8, 12, 2, gc)
        elif pendant == 'circle':
            cv.disc(8, 10, 3, 'g', fill=False)
            cv.disc(8, 10, 2, gc)
        elif pendant == 'diamond':
            cv.diamond(8, 10, 3, gc)
            cv.set(8, 9, 'l')
        elif pendant == 'fang':
            cv.tri(8, 13, 4, 7, 'c', up=False)
            cv.set(8, 11, gc)
        elif pendant == 'coin':
            cv.disc(8, 10, 3, 'g')
            cv.set(8, 10, gc)
        cv.finish()
        out.append((f"{pendant}_amulet_{gname}", f"{pendant.capitalize()} Amulet ({gname})", cv))
    return out


def build_crowns(n=15):
    out = []
    styles = ['royal', 'circlet', 'war', 'laurel', 'tiara']
    mats = [('gold', 'g'), ('silver', 's'), ('bronze', 'z')]
    combos = _sample(list(itertools.product(styles, mats)), n)
    for style, (mname, mc) in combos:
        cv = Canvas()
        if style == 'royal':
            cv.rect(4, 8, 12, 12, mc)
            for x in (4, 6, 8, 10, 12):
                cv.vline(x, 5, 8, mc)
                cv.set(x, 5, 'r' if x % 4 == 0 else 'b')
        elif style == 'circlet':
            cv.ellipse(8, 9, 5, 3, mc, fill=False)
            cv.set(6, 6, 'r'); cv.set(8, 6, 'b'); cv.set(10, 6, 'r')
        elif style == 'war':
            cv.rect(4, 8, 12, 12, mc)
            for x in (5, 8, 11):
                cv.tri(x, 8, 3, 4, mc, up=True)
        elif style == 'laurel':
            for i in range(7):
                x = 3 + i * 2
                y = 10 - abs(i - 3)
                cv.set(x, y, 'n')
            cv.hline(3, 13, 11, mc)
        elif style == 'tiara':
            cv.rect(5, 9, 11, 12, mc)
            cv.tri(8, 5, 4, 4, mc, up=True)
            cv.set(8, 6, 'r')
        cv.finish()
        out.append((f"{mname}_{style}_crown", f"{mname.capitalize()} {style.capitalize()} Crown", cv))
    return out


def build():
    icons = []
    icons += [("treasure/" + s, l, c) for s, l, c in build_coins()]
    icons += [("treasure/" + s, l, c) for s, l, c in build_gems()]
    icons += [("treasure/" + s, l, c) for s, l, c in build_chests()]
    icons += [("treasure/" + s, l, c) for s, l, c in build_keys()]
    icons += [("treasure/" + s, l, c) for s, l, c in build_rings()]
    icons += [("treasure/" + s, l, c) for s, l, c in build_amulets()]
    icons += [("treasure/" + s, l, c) for s, l, c in build_crowns()]
    return icons
