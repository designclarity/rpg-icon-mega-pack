"""UI category: hearts, mana, stars, arrows, status icons, buttons,
banners, level gems."""
import itertools
from canvas import Canvas


def _sample(combos, n):
    step = max(1, len(combos) // n)
    return combos[::step][:n]


def _heart(cv, c, style):
    if style == 'full':
        cv.disc(6, 7, 3, c)
        cv.disc(10, 7, 3, c)
        cv.tri(8, 13, 9, 6, c, up=False)
        cv.set(5, 6, 'l'); cv.set(6, 5, 'l')
    else:  # container
        cv.disc(6, 7, 3, c, fill=False)
        cv.disc(10, 7, 3, c, fill=False)
        cv.tri(8, 13, 9, 6, c, up=False)
        cv.disc(8, 8, 3, 'e')


def build_hearts(n=12):
    out = []
    colors = [('red', 'r'), ('blue', 'b'), ('green', 'n'),
              ('purple', 'p'), ('gold', 'y'), ('dark', 'x')]
    styles = ['full', 'container']
    combos = _sample(list(itertools.product(colors, styles)), n)
    for (cname, c), style in combos:
        cv = Canvas()
        _heart(cv, c, style)
        cv.finish()
        out.append((f"{cname}_heart_{style}", f"{cname.capitalize()} Heart ({style})", cv))
    return out


def build_mana(n=10):
    out = []
    colors = [('blue', 'b'), ('green', 'n'), ('purple', 'p'),
              ('red', 'r'), ('gold', 'y')]
    styles = ['drop', 'vial']
    combos = _sample(list(itertools.product(colors, styles)), n)
    for (cname, c), style in combos:
        cv = Canvas()
        if style == 'drop':
            cv.tri(8, 3, 6, 5, c, up=True)
            cv.disc(8, 10, 3, c)
            cv.set(7, 9, 'l')
        else:
            cv.rect(6, 5, 10, 12, c)
            cv.rect(7, 3, 9, 4, 'd')
            cv.vline(6, 5, 12, 'l')
        cv.finish()
        out.append((f"{cname}_mana_{style}", f"{cname.capitalize()} Mana ({style})", cv))
    return out


def build_stars(n=8):
    out = []
    colors = [('gold', 'y'), ('silver', 'l'), ('bronze', 'z'), ('red', 'r')]
    combos = _sample(list(itertools.product(colors, ['plain', 'sparkle'])), n)
    for (cname, c), variant in combos:
        cv = Canvas()
        cv.diamond(8, 8, 5, c)
        cv.hline(3, 13, 8, c)
        cv.vline(8, 3, 13, c)
        cv.set(7, 7, 'l')
        if variant == 'sparkle':
            cv.set(4, 4, 'l'); cv.set(12, 12, 'l')
        cv.finish()
        out.append((f"{cname}_star_{variant}", f"{cname.capitalize()} Star ({variant})", cv))
    return out


def build_ui_arrows(n=12):
    out = []
    dirs = ['up', 'down', 'left', 'right']
    styles = [('gold', 'g'), ('steel', 's'), ('red', 'r')]
    combos = _sample(list(itertools.product(dirs, styles)), n)
    for direction, (sname, c) in combos:
        cv = Canvas()
        if direction == 'up':
            cv.tri(8, 3, 7, 6, c, up=True)
            cv.rect(7, 8, 9, 13, c)
        elif direction == 'down':
            cv.tri(8, 13, 7, 6, c, up=False)
            cv.rect(7, 3, 9, 8, c)
        elif direction == 'left':
            for i in range(4):
                cv.vline(3 + i, 8 - i, 8 + i, c)
            cv.rect(6, 7, 13, 9, c)
        elif direction == 'right':
            cv = Canvas()
            for i in range(4):
                cv.vline(12 - i, 8 - i, 8 + i, c)
            cv.rect(3, 7, 10, 9, c)
        cv.finish()
        out.append((f"arrow_{direction}_{sname}", f"Arrow {direction.capitalize()} ({sname})", cv))
    return out


def _status(cv, kind):
    if kind == 'poison':
        cv.disc(8, 9, 5, 'n')
        cv.disc(6, 5, 2, 'n'); cv.disc(10, 4, 2, 'N')
        cv.set(6, 5, 'l'); cv.set(10, 4, 'l')
    elif kind == 'burn':
        cv.tri(8, 3, 6, 8, 'o', up=True)
        cv.tri(8, 6, 4, 5, 'y', up=True)
    elif kind == 'freeze':
        cv.diamond(8, 8, 5, 'm')
        cv.set(8, 8, 'l')
    elif kind == 'stun':
        cv.disc(8, 8, 5, 'y')
        cv.set(5, 6, 'K'); cv.set(11, 6, 'K')
        cv.set(8, 10, 'K')
    elif kind == 'shield_up':
        cv.disc(8, 8, 5, 'b')
        cv.disc(8, 8, 3, 'c')
    elif kind == 'rage':
        cv.disc(8, 8, 5, 'r')
        cv.tri(8, 4, 4, 4, 'y', up=True)
    elif kind == 'haste':
        cv.disc(8, 8, 5, 'a')
        cv.tri(9, 8, 4, 7, 'l', up=False)
    elif kind == 'curse':
        cv.disc(8, 8, 5, 'x')
        cv.set(8, 8, 'p')
    elif kind == 'charm':
        cv.disc(6, 7, 2, 'v'); cv.disc(10, 7, 2, 'v')
        cv.tri(8, 11, 6, 4, 'v', up=False)
    elif kind == 'regen':
        cv.disc(8, 8, 5, 'n')
        cv.vline(8, 5, 11, 'l'); cv.hline(5, 11, 8, 'l')
    elif kind == 'silence':
        cv.disc(8, 8, 5, 'k')
        cv.hline(4, 12, 8, 'e')
    elif kind == 'blessed':
        cv.disc(8, 8, 5, 'y')
        cv.vline(8, 5, 11, 'K'); cv.hline(5, 11, 8, 'K')


def build_status(n=12):
    out = []
    kinds = ['poison', 'burn', 'freeze', 'stun', 'shield_up', 'rage',
             'haste', 'curse', 'charm', 'regen', 'silence', 'blessed']
    for kind in _sample(kinds, n):
        cv = Canvas()
        _status(cv, kind)
        cv.finish()
        out.append((f"status_{kind}", f"Status: {kind.replace('_', ' ').title()}", cv))
    return out


def build_buttons(n=10):
    out = []
    shapes = ['round', 'square']
    colors = [('red', 'r'), ('blue', 'b'), ('green', 'n'), ('gold', 'g'), ('gray', 'k')]
    combos = _sample(list(itertools.product(shapes, colors)), n)
    for shape, (cname, c) in combos:
        cv = Canvas()
        if shape == 'round':
            cv.disc(8, 8, 5, c)
            cv.disc(8, 8, 3, 'l')
            cv.set(8, 8, c)
        else:
            cv.rect(3, 5, 13, 11, c)
            cv.rect(4, 6, 12, 10, 'l')
            cv.rect(5, 7, 11, 9, c)
        cv.finish()
        out.append((f"{shape}_button_{cname}", f"{shape.capitalize()} Button ({cname})", cv))
    return out


def build_banners(n=8):
    out = []
    colors = [('red', 'r'), ('blue', 'b'), ('green', 'n'), ('purple', 'p')]
    combos = _sample(list(itertools.product(colors, ['swallowtail', 'straight'])), n)
    for (cname, c), cut in combos:
        cv = Canvas()
        cv.vline(4, 2, 14, 'w')
        if cut == 'swallowtail':
            cv.rect(4, 2, 12, 8, c)
            cv.tri(12, 8, 3, 3, c, up=False)
            cv.set(8, 5, 'y')
        else:
            cv.rect(4, 2, 12, 7, c)
            cv.set(8, 4, 'y')
        cv.finish()
        out.append((f"{cname}_banner_{cut}", f"{cname.capitalize()} Banner ({cut})", cv))
    return out


def build_level_gems(n=8):
    out = []
    colors = [('blue', 'b'), ('green', 'n'), ('red', 'r'), ('purple', 'p')]
    combos = _sample(list(itertools.product(colors, [1, 2])), n)
    for (cname, c), pips in combos:
        cv = Canvas()
        cv.diamond(8, 8, 4, c)
        cv.set(8, 8, 'l')
        for p in range(pips):
            cv.set(7 + p, 12, 'y')
        cv.finish()
        out.append((f"{cname}_level_gem_{pips}pip", f"{cname.capitalize()} Level Gem ({pips} pip)", cv))
    return out


def build():
    icons = []
    icons += [("ui/" + s, l, c) for s, l, c in build_hearts()]
    icons += [("ui/" + s, l, c) for s, l, c in build_mana()]
    icons += [("ui/" + s, l, c) for s, l, c in build_stars()]
    icons += [("ui/" + s, l, c) for s, l, c in build_ui_arrows()]
    icons += [("ui/" + s, l, c) for s, l, c in build_status()]
    icons += [("ui/" + s, l, c) for s, l, c in build_buttons()]
    icons += [("ui/" + s, l, c) for s, l, c in build_banners()]
    icons += [("ui/" + s, l, c) for s, l, c in build_level_gems()]
    return icons
