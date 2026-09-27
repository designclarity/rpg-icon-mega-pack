"""Armor category: shields, helmets, chestplates, boots, gauntlets,
pauldrons, belts, cloaks."""
import itertools
from canvas import Canvas, MATERIALS

SHIELD_MATS = ['iron', 'steel', 'bronze']


def _shield_shape(cv, shape, mat):
    _, edge, mid, dark, light = mat
    if shape == 'round':
        cv.disc(8, 8, 6, mid)
        cv.disc(8, 8, 4, dark)
        cv.disc(8, 8, 2, mid)
    elif shape == 'heater':
        # triangle-ish heater shield
        for i in range(9):
            w = 5 - i // 2
            cv.hline(8 - w, 8 + w, 4 + i, mid)
        cv.hline(3, 13, 4, light)
    elif shape == 'kite':
        for i in range(11):
            w = 4 - abs(i - 3)
            cv.hline(8 - w, 8 + w, 3 + i, mid)
        cv.vline(8, 3, 13, light)
    elif shape == 'tower':
        cv.rect(5, 3, 11, 13, mid)
        cv.rect(5, 3, 11, 13, dark, fill=False)
        cv.rect(6, 4, 10, 12, mid)
        cv.vline(6, 4, 12, light)
    elif shape == 'buckler':
        cv.disc(8, 8, 4, mid)
        cv.disc(8, 8, 2, dark)
        cv.set(8, 8, light)
    elif shape == 'oval':
        cv.ellipse(8, 8, 4, 6, mid)
        cv.ellipse(8, 8, 2, 4, dark)
    elif shape == 'diamond':
        cv.diamond(8, 8, 6, mid)
        cv.diamond(8, 8, 3, dark)


def _shield_emblem(cv, emblem, shape):
    ec = 'r'
    if emblem == 'cross':
        cv.vline(8, 4, 12, ec); cv.hline(5, 11, 8, ec)
    elif emblem == 'chevron':
        for i in range(3):
            cv.hline(8 - 3 + i, 8 + 3 - i, 6 + i, ec)
    elif emblem == 'stripe':
        cv.hline(4, 12, 8, ec); cv.hline(4, 12, 9, 'R')
    elif emblem == 'circle':
        cv.disc(8, 8, 2, ec, fill=False)
    elif emblem == 'skull':
        cv.disc(8, 8, 2, 'c')
        cv.set(7, 8, 'K'); cv.set(9, 8, 'K')
    elif emblem == 'star':
        cv.diamond(8, 8, 2, 'y')
    # 'none' -> nothing


def build_shields(n=72):
    out = []
    shapes = ['round', 'heater', 'kite', 'tower', 'buckler', 'oval', 'diamond']
    emblems = ['none', 'cross', 'chevron', 'stripe', 'circle', 'skull', 'star']
    combos = _sample(list(itertools.product(shapes, emblems, SHIELD_MATS)), n)
    for shape, emblem, mn in combos:
        cv = Canvas()
        _shield_shape(cv, shape, MATERIALS[mn])
        _shield_emblem(cv, emblem, shape)
        # boss
        cv.disc(8, 8, 1, 'd' if mn != 'bronze' else 'Z')
        cv.finish()
        el = f"_{emblem}" if emblem != 'none' else ""
        out.append((f"{mn}_{shape}{el}_shield",
                    f"{mn.capitalize()} {shape.capitalize()} Shield"
                    + (f" ({emblem})" if emblem != 'none' else ""), cv))
    return out


def _sample(combos, n):
    step = max(1, len(combos) // n)
    return combos[::step][:n]


def _helmet(cv, kind, mat):
    _, edge, mid, dark, light = mat
    if kind == 'knight':
        cv.rect(4, 4, 12, 12, mid)
        cv.hline(4, 12, 4, light)
        cv.hline(4, 12, 10, 'e')   # visor slit
        cv.vline(4, 4, 12, edge)
    elif kind == 'nasal':
        cv.rect(5, 4, 11, 11, mid)
        cv.hline(5, 11, 4, light)
        cv.vline(8, 7, 11, dark)   # nasal guard
    elif kind == 'viking':
        cv.rect(5, 5, 11, 12, mid)
        cv.hline(5, 11, 5, light)
        cv.tri(4, 8, 3, 4, 'c', up=False)   # horns
        cv.tri(12, 8, 3, 4, 'c', up=False)
    elif kind == 'hood':
        cv.tri(8, 3, 9, 6, 'T', up=True)
        cv.ellipse(8, 10, 3, 3, 'e')
    elif kind == 'crown':
        cv.rect(4, 8, 12, 12, 'g')
        for x in (4, 6, 8, 10, 12):
            cv.vline(x, 5, 8, 'g')
            cv.set(x, 5, 'y')
        cv.hline(4, 12, 12, 'G')
    elif kind == 'circlet':
        cv.ellipse(8, 9, 5, 3, 'g', fill=False)
        cv.set(8, 6, 'r')
    elif kind == 'mage_hat':
        cv.tri(9, 1, 7, 8, 'P', up=True)
        cv.ellipse(8, 10, 5, 2, 'P')
        cv.set(6, 9, 'p')
    elif kind == 'kettle':
        cv.ellipse(8, 7, 5, 3, mid)
        cv.hline(3, 13, 8, edge)
        cv.hline(3, 13, 4, light)


def build_helmets(n=24):
    out = []
    mat_kinds = ['knight', 'nasal', 'viking', 'kettle']      # use material
    fixed_kinds = ['hood', 'crown', 'circlet', 'mage_hat']   # material-agnostic
    matnames = ['iron', 'steel', 'bronze']
    combos = _sample(list(itertools.product(mat_kinds, matnames)), n)
    for kind, mn in combos:
        cv = Canvas()
        _helmet(cv, kind, MATERIALS[mn])
        cv.finish()
        out.append((f"{mn}_{kind}_helmet", f"{mn.capitalize()} {kind.replace('_', ' ').title()} Helmet", cv))
    for kind in fixed_kinds:
        cv = Canvas()
        _helmet(cv, kind, MATERIALS['iron'])
        cv.finish()
        out.append((f"{kind}_helmet", f"{kind.replace('_', ' ').title()} Helmet", cv))
    return out


def _chestplate(cv, kind, mat):
    _, edge, mid, dark, light = mat
    if kind == 'cuirass':
        cv.rect(4, 3, 12, 12, mid)
        cv.vline(5, 3, 12, light)
        cv.vline(4, 3, 12, edge)
        cv.hline(4, 12, 7, dark)
    elif kind == 'chainmail':
        cv.rect(4, 3, 12, 12, 'k')
        for y in range(3, 13, 2):
            for x in range(4, 13, 2):
                cv.set(x, y, 's')
        cv.vline(4, 3, 12, edge)
    elif kind == 'plate':
        cv.rect(4, 3, 12, 12, mid)
        for y in (5, 8, 11):
            cv.hline(4, 12, y, dark)
        cv.vline(5, 3, 12, light)
    elif kind == 'leather':
        cv.rect(4, 3, 12, 12, 't')
        cv.vline(5, 3, 12, 'c')
        cv.hline(4, 12, 7, 'T')
        cv.set(8, 7, 'g')
    elif kind == 'robes':
        cv.tri(8, 3, 9, 10, 'P', up=True)
        cv.vline(8, 3, 12, 'p')


def build_chestplates(n=20):
    out = []
    mat_kinds = ['cuirass', 'chainmail', 'plate']
    fixed_kinds = ['leather', 'robes']
    matnames = ['iron', 'steel', 'bronze', 'mithril']
    combos = _sample(list(itertools.product(mat_kinds, matnames)), n)
    for kind, mn in combos:
        cv = Canvas()
        _chestplate(cv, kind, MATERIALS[mn])
        cv.finish()
        out.append((f"{mn}_{kind}_chestplate", f"{mn.capitalize()} {kind.capitalize()} Chestplate", cv))
    for kind in fixed_kinds:
        cv = Canvas()
        _chestplate(cv, kind, MATERIALS['iron'])
        cv.finish()
        out.append((f"{kind}_chestplate", f"{kind.capitalize()} Chestplate", cv))
    return out


def _boots(cv, kind, mat):
    _, edge, mid, dark, light = mat
    if kind == 'boot':
        cv.rect(6, 4, 9, 10, 't')
        cv.rect(4, 10, 11, 13, 't')
        cv.hline(4, 11, 13, 'T')
    elif kind == 'greave':
        cv.rect(6, 4, 10, 13, mid)
        cv.vline(6, 4, 13, light)
        cv.hline(6, 10, 8, dark)
    elif kind == 'sabaton':
        cv.rect(6, 4, 9, 9, mid)
        cv.tri(8, 9, 7, 5, mid, up=False)
        cv.hline(5, 11, 10, light)
    elif kind == 'shoe':
        cv.ellipse(8, 11, 4, 2, 'T')
        cv.rect(6, 8, 10, 11, 't')


def build_boots(n=16):
    out = []
    mat_kinds = ['greave', 'sabaton']
    fixed_kinds = ['boot', 'shoe']
    matnames = ['iron', 'steel', 'bronze', 'leather']
    combos = _sample(list(itertools.product(mat_kinds, matnames)), n)
    for kind, mn in combos:
        cv = Canvas()
        _boots(cv, kind, MATERIALS[mn])
        cv.finish()
        out.append((f"{mn}_{kind}", f"{mn.capitalize()} {kind.capitalize()}", cv))
    for kind in fixed_kinds:
        cv = Canvas()
        _boots(cv, kind, MATERIALS['iron'])
        cv.finish()
        out.append((f"{kind}", f"{kind.capitalize()}", cv))
    return out


def _gauntlet(cv, kind, mat):
    _, edge, mid, dark, light = mat
    if kind == 'mitten':
        cv.ellipse(8, 8, 3, 4, mid)
        cv.set(8, 5, light)
    elif kind == 'plate':
        cv.rect(5, 4, 11, 12, mid)
        for y in (6, 9):
            cv.hline(5, 11, y, dark)
        cv.vline(5, 4, 12, light)
    elif kind == 'glove':
        cv.rect(5, 5, 11, 12, 't')
        for x in (6, 8, 10):
            cv.vline(x, 5, 8, 'T')
    elif kind == 'clawed':
        cv.ellipse(8, 9, 3, 3, mid)
        for x in (6, 8, 10):
            cv.tri(x, 12, 2, 3, 'l', up=False)


def build_gauntlets(n=16):
    out = []
    mat_kinds = ['mitten', 'plate', 'clawed']
    fixed_kinds = ['glove']
    matnames = ['iron', 'steel', 'bronze', 'leather']
    combos = _sample(list(itertools.product(mat_kinds, matnames)), n)
    for kind, mn in combos:
        cv = Canvas()
        _gauntlet(cv, kind, MATERIALS[mn])
        cv.finish()
        out.append((f"{mn}_{kind}_gauntlet", f"{mn.capitalize()} {kind.capitalize()} Gauntlet", cv))
    for kind in fixed_kinds:
        cv = Canvas()
        _gauntlet(cv, kind, MATERIALS['iron'])
        cv.finish()
        out.append((f"{kind}_gauntlet", f"{kind.capitalize()} Gauntlet", cv))
    return out


def build_pauldrons(n=12):
    out = []
    kinds = ['round', 'spiked', 'layered']
    matnames = ['iron', 'steel', 'bronze', 'gold']
    combos = _sample(list(itertools.product(kinds, matnames)), n)
    for kind, mn in combos:
        cv = Canvas()
        mat = MATERIALS[mn]
        _, edge, mid, dark, light = mat
        if kind == 'round':
            cv.ellipse(8, 7, 5, 4, mid)
            cv.set(8, 4, light)
        elif kind == 'spiked':
            cv.ellipse(8, 8, 5, 3, mid)
            for x in (4, 8, 12):
                cv.tri(x, 5, 2, 4, light, up=True)
        elif kind == 'layered':
            for i, y in enumerate((4, 7, 10)):
                cv.ellipse(8, y, 5 - i, 2, mid if i % 2 == 0 else dark)
        cv.finish()
        out.append((f"{mn}_{kind}_pauldron", f"{mn.capitalize()} {kind.capitalize()} Pauldron", cv))
    return out


def build_belts(n=12):
    out = []
    buckles = ['square', 'round', 'skull', 'gem']
    straps = ['brown', 'black', 'red']
    combos = _sample(list(itertools.product(buckles, straps)), n)
    strap_c = {'brown': 'T', 'black': 'e', 'red': 'R'}
    for buckle, strap in combos:
        cv = Canvas()
        cv.hline(2, 14, 8, strap_c[strap])
        cv.hline(2, 14, 7, 't' if strap != 'black' else 'k')
        if buckle == 'square':
            cv.rect(6, 6, 10, 10, 'g', fill=False)
        elif buckle == 'round':
            cv.disc(8, 8, 2, 'g', fill=False)
            cv.set(8, 8, 'y')
        elif buckle == 'skull':
            cv.disc(8, 8, 2, 'c')
            cv.set(7, 8, 'K'); cv.set(9, 8, 'K')
        elif buckle == 'gem':
            cv.diamond(8, 8, 2, 'r')
        cv.finish()
        out.append((f"{strap}_{buckle}_belt", f"{strap.capitalize()} Belt ({buckle} buckle)", cv))
    return out


def build_cloaks(n=12):
    out = []
    styles = ['traveler', 'royal', 'hooded']
    colors = ['red', 'blue', 'green', 'purple']
    col_c = {'red': 'r', 'blue': 'b', 'green': 'n', 'purple': 'p'}
    col_d = {'red': 'R', 'blue': 'B', 'green': 'N', 'purple': 'P'}
    combos = _sample(list(itertools.product(styles, colors)), n)
    for style, color in combos:
        cv = Canvas()
        c, d = col_c[color], col_d[color]
        if style == 'traveler':
            cv.tri(8, 3, 9, 11, c, up=True)
            cv.vline(8, 3, 13, d)
        elif style == 'royal':
            cv.tri(8, 3, 11, 11, c, up=True)
            cv.tri(8, 3, 5, 11, 'y', up=True)
        elif style == 'hooded':
            cv.tri(8, 2, 7, 6, d, up=True)
            cv.tri(8, 6, 9, 8, c, up=True)
        cv.finish()
        out.append((f"{color}_{style}_cloak", f"{color.capitalize()} {style.capitalize()} Cloak", cv))
    return out


def build():
    icons = []
    icons += [("armor/" + s, l, c) for s, l, c in build_shields()]
    icons += [("armor/" + s, l, c) for s, l, c in build_helmets()]
    icons += [("armor/" + s, l, c) for s, l, c in build_chestplates()]
    icons += [("armor/" + s, l, c) for s, l, c in build_boots()]
    icons += [("armor/" + s, l, c) for s, l, c in build_gauntlets()]
    icons += [("armor/" + s, l, c) for s, l, c in build_pauldrons()]
    icons += [("armor/" + s, l, c) for s, l, c in build_belts()]
    icons += [("armor/" + s, l, c) for s, l, c in build_cloaks()]
    return icons
