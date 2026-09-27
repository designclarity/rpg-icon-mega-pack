"""Weapons category: swords, daggers, axes, maces, spears, bows, staves, wands.
Component-based: blade/guard/pommel/head variants x materials."""
import itertools
from canvas import Canvas, MATERIALS

BLADE_MATS = ['iron', 'steel', 'bronze', 'gold', 'mithril', 'shadow']
TRIM_MATS = {'iron': 'd', 'steel': 's', 'bronze': 'z', 'gold': 'g',
             'mithril': 'm', 'shadow': 'k'}


def _blade(cv, kind, mat, y0=1, y1=8):
    _, edge, mid, dark, light = mat
    cx = 8
    if kind == 'straight':
        cv.rect(cx - 1, y0 + 1, cx + 1, y1, mid)
        cv.vline(cx - 1, y0 + 1, y1, edge)
        cv.vline(cx, y0 + 1, y1, light)
        cv.vline(cx, y0 + 2, y1 - 1, dark)  # fuller
        cv.set(cx, y0, light)
    elif kind == 'wide':
        cv.rect(cx - 2, y0 + 1, cx + 2, y1, mid)
        cv.vline(cx - 2, y0 + 1, y1, edge)
        cv.vline(cx - 1, y0 + 1, y1, light)
        cv.vline(cx, y0 + 2, y1 - 1, dark)
        cv.rect(cx - 1, y0, cx + 1, y0, light)
    elif kind == 'rapier':
        cv.vline(cx, y0, y1, mid)
        cv.set(cx, y0, light)
        cv.rect(cx - 1, y1 - 1, cx + 1, y1, edge)
    elif kind == 'curved':
        for y in range(y0 + 1, y1 + 1):
            off = (y1 - y) // 3
            cv.hline(cx - 1 + off, cx + 1 + off, y, mid)
            cv.set(cx - 1 + off, y, edge)
        cv.set(cx + (y1 - y0 - 1) // 3, y0, light)
    elif kind == 'jagged':
        for i, y in enumerate(range(y0 + 1, y1 + 1)):
            w = 2 if i % 2 == 0 else 1
            cv.hline(cx - w, cx + w, y, mid)
            cv.set(cx - w, y, edge)
        cv.set(cx, y0, light)
    elif kind == 'short':
        cv.rect(cx - 1, y0 + 2, cx + 1, y1, mid)
        cv.vline(cx - 1, y0 + 2, y1, edge)
        cv.vline(cx, y0 + 2, y1, light)
        cv.set(cx, y0 + 1, light)
    elif kind == 'leaf':
        widths = [0, 1, 2, 2, 2, 1, 1]
        for i, y in enumerate(range(y0, y1 + 1)):
            w = widths[i % len(widths)]
            cv.hline(cx - w, cx + w, y, mid)
            if w:
                cv.set(cx - w, y, edge)
        cv.set(cx, y0, light)
    elif kind == 'serrated':
        cv.rect(cx - 1, y0 + 1, cx + 1, y1, mid)
        cv.vline(cx - 1, y0 + 1, y1, edge)
        cv.vline(cx, y0 + 1, y1, light)
        for y in range(y0 + 2, y1, 2):
            cv.set(cx + 1, y, None)  # notch on right edge
        cv.set(cx, y0, light)


def _guard(cv, kind, trim):
    if kind == 'straight':
        cv.hline(4, 12, 9, trim)
        cv.hline(5, 11, 10, trim)
    elif kind == 'curved_up':
        cv.hline(5, 11, 9, trim)
        cv.set(4, 8, trim); cv.set(12, 8, trim)
        cv.hline(5, 11, 10, trim)
    elif kind == 'curved_down':
        cv.hline(5, 11, 9, trim)
        cv.set(4, 10, trim); cv.set(12, 10, trim)
        cv.hline(6, 10, 10, trim)
    elif kind == 'round':
        cv.disc(8, 9, 2, trim)
        cv.set(8, 9, 'g' if trim != 'g' else 'y')
    elif kind == 'diamond':
        cv.diamond(8, 9, 2, trim)


def _pommel(cv, kind, trim, gem='r'):
    if kind == 'round':
        cv.disc(8, 13, 1, trim)
    elif kind == 'square':
        cv.rect(7, 13, 9, 14, trim)
    elif kind == 'spike':
        cv.tri(8, 15, 3, 3, trim, up=False)
    elif kind == 'gem':
        cv.diamond(8, 13, 2, gem)
        cv.set(8, 12, 'l')


def _grip(cv, y0=11, y1=12, c='w'):
    cv.rect(7, y0, 8, y1, c)
    cv.vline(7, y0, y1, 'W')


def sword(blade, guard, pommel, matname, dagger=False):
    cv = Canvas()
    mat = MATERIALS[matname]
    trim = TRIM_MATS[matname]
    y0, y1 = (4, 8) if dagger else (1, 8)
    _blade(cv, blade, mat, y0, y1)
    gy = y1 + 1
    # shift guard/grip/pommel down for daggers
    if dagger:
        _guard_d(cv, guard, trim, gy)
        _grip(cv, gy + 2, gy + 3)
        _pommel_d(cv, pommel, trim, gy + 4)
    else:
        _guard(cv, guard, trim)
        _grip(cv)
        _pommel(cv, pommel, trim)
    return cv.finish()


def _guard_d(cv, kind, trim, gy):
    if kind == 'straight':
        cv.hline(5, 11, gy, trim)
    elif kind == 'curved_up':
        cv.hline(6, 10, gy, trim)
        cv.set(5, gy - 1, trim); cv.set(11, gy - 1, trim)
    elif kind == 'curved_down':
        cv.hline(6, 10, gy, trim)
        cv.set(5, gy + 1, trim); cv.set(11, gy + 1, trim)
    elif kind == 'round':
        cv.disc(8, gy, 2, trim)
        cv.set(8, gy, 'g' if trim != 'g' else 'y')
    elif kind == 'diamond':
        cv.diamond(8, gy, 1, trim)
        cv.set(8, gy, 'y')


def _pommel_d(cv, kind, trim, py):
    if kind == 'round':
        cv.disc(8, py, 1, trim)
    elif kind == 'square':
        cv.rect(7, py, 9, py + 1, trim)
    elif kind == 'spike':
        cv.tri(8, py + 2, 3, 3, trim, up=False)
    elif kind == 'gem':
        cv.diamond(8, py, 1, trim)


BLADES = ['straight', 'wide', 'rapier', 'curved', 'jagged', 'short', 'leaf', 'serrated']
GUARDS = ['straight', 'curved_up', 'curved_down', 'round', 'diamond']
POMMELS = ['round', 'square', 'spike', 'gem']
DAGGER_BLADES = ['straight', 'curved', 'jagged', 'short', 'serrated']


def _sample(combos, n):
    step = max(1, len(combos) // n)
    return combos[::step][:n]


def build_swords(n=96):
    out = []
    combos = _sample(list(itertools.product(BLADES, GUARDS, POMMELS, BLADE_MATS)), n)
    for blade, guard, pommel, mat in combos:
        slug = f"{mat}_{blade}_{guard}_{pommel}_sword"
        label = f"{mat.capitalize()} {blade.capitalize()} Sword"
        out.append((slug, label, sword(blade, guard, pommel, mat)))
    return out


def build_daggers(n=48):
    out = []
    combos = _sample(list(itertools.product(DAGGER_BLADES, GUARDS, POMMELS, BLADE_MATS)), n)
    for blade, guard, pommel, mat in combos:
        slug = f"{mat}_{blade}_{guard}_{pommel}_dagger"
        label = f"{mat.capitalize()} {blade.capitalize()} Dagger"
        out.append((slug, label, sword(blade, guard, pommel, mat, dagger=True)))
    return out


def _axe_head(cv, kind, mat):
    _, edge, mid, dark, light = mat
    if kind == 'single':
        cv.rect(9, 2, 13, 6, mid)
        cv.hline(9, 13, 2, light)
        cv.vline(13, 2, 6, edge)
        cv.set(9, 6, dark); cv.set(10, 6, dark)
    elif kind == 'double':
        cv.rect(3, 2, 13, 6, mid)
        cv.hline(3, 13, 2, light)
        cv.vline(3, 2, 6, edge); cv.vline(13, 2, 6, edge)
        cv.set(8, 2, dark)
    elif kind == 'crescent':
        for y in range(2, 7):
            w = 5 - abs(y - 4)
            cv.hline(9, 9 + w, y, mid)
        cv.vline(13, 2, 6, edge)
        cv.hline(9, 12, 2, light)
    elif kind == 'bearded':
        cv.rect(9, 2, 12, 7, mid)
        cv.hline(9, 12, 2, light)
        cv.vline(12, 2, 7, edge)
        cv.set(9, 7, dark); cv.set(10, 7, dark)
    elif kind == 'pick':
        cv.hline(3, 13, 3, mid)
        cv.set(3, 3, edge); cv.set(13, 3, edge)
        cv.hline(3, 13, 4, light)
        cv.rect(7, 2, 9, 5, dark)
    elif kind == 'war':
        cv.rect(9, 2, 13, 5, mid)
        cv.hline(9, 13, 2, light)
        cv.rect(3, 3, 6, 4, dark)  # hammer back


def build_axes(n=48):
    out = []
    heads = ['single', 'double', 'crescent', 'bearded', 'pick', 'war']
    matnames = ['iron', 'steel', 'bronze', 'shadow']
    handles = [('oak', 'w'), ('wrapped', 'r'), ('long', 'W')]
    combos = _sample(list(itertools.product(heads, matnames, handles)), n)
    for head, mn, (hname, hc) in combos:
        cv = Canvas()
        hy1 = 14 if hname != 'long' else 15
        cv.vline(8, 4, hy1, 'w' if hname == 'oak' else hc)
        if hname == 'wrapped':
            for y in (7, 10, 13):
                cv.set(8, y, 'r')
        cv.set(8, 4, 't')
        _axe_head(cv, head, MATERIALS[mn])
        cv.finish()
        out.append((f"{mn}_{head}_{hname}_axe", f"{mn.capitalize()} {head.capitalize()} Axe ({hname})", cv))
    return out


def _mace_head(cv, kind, mat):
    _, edge, mid, dark, light = mat
    if kind == 'flanged':
        cv.disc(8, 3, 3, mid)
        for dx in (-2, 0, 2):
            cv.vline(8 + dx, 1, 5, edge)
        cv.set(8, 1, light)
    elif kind == 'spiked':
        cv.disc(8, 3, 2, mid)
        for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, -2), (-2, 2), (2, 2)]:
            cv.set(8 + dx, 3 + dy, edge)
        cv.set(8, 2, light)
    elif kind == 'morningstar':
        cv.disc(8, 3, 2, dark)
        for dx, dy in [(-4, 0), (4, 0), (0, -4), (-3, -3), (3, -3), (-3, 3), (3, 3)]:
            cv.set(8 + dx, 3 + dy, light)
            cv.set(8 + dx // 2, 3 + dy // 2, mid)
    elif kind == 'cube':
        cv.rect(6, 1, 10, 5, mid)
        cv.hline(6, 10, 1, light)
        cv.vline(6, 1, 5, edge)
    elif kind == 'disc':
        cv.ellipse(8, 3, 4, 2, mid)
        cv.hline(5, 11, 1, light)
    elif kind == 'hammer':
        cv.rect(4, 1, 12, 4, mid)
        cv.hline(4, 12, 1, light)
        cv.vline(4, 1, 4, edge)


def build_maces(n=36):
    out = []
    heads = ['flanged', 'spiked', 'morningstar', 'cube', 'disc', 'hammer']
    matnames = ['iron', 'steel', 'bronze']
    handles = [('oak', 'w'), ('ironshod', 'd')]
    combos = _sample(list(itertools.product(heads, matnames, handles)), n)
    for head, mn, (hname, hc) in combos:
        cv = Canvas()
        cv.vline(8, 5, 14, hc)
        cv.set(8, 5, 't')
        if hname == 'ironshod':
            cv.vline(8, 5, 14, 'd')
            cv.set(8, 8, 's'); cv.set(8, 11, 's')
        _mace_head(cv, head, MATERIALS[mn])
        cv.finish()
        out.append((f"{mn}_{head}_{hname}_mace", f"{mn.capitalize()} {head.capitalize()} Mace ({hname})", cv))
    return out


def _spear_tip(cv, kind, mat):
    _, edge, mid, dark, light = mat
    if kind == 'leaf':
        cv.tri(8, 1, 5, 4, mid, up=True)
        cv.vline(8, 1, 4, light)
    elif kind == 'diamond':
        cv.diamond(8, 2, 2, mid)
        cv.set(8, 1, light)
    elif kind == 'barbed':
        cv.tri(8, 1, 3, 4, mid, up=True)
        cv.set(6, 3, edge); cv.set(10, 3, edge)
        cv.vline(8, 1, 4, light)
    elif kind == 'trident':
        for dx in (-3, 0, 3):
            cv.vline(8 + dx, 1, 3, mid)
            cv.set(8 + dx, 1, light)
        cv.hline(5, 11, 4, dark)
    elif kind == 'pike':
        cv.vline(8, 1, 5, mid)
        cv.set(8, 1, light)
        cv.rect(7, 5, 9, 6, edge)


def build_spears(n=30):
    out = []
    tips = ['leaf', 'diamond', 'barbed', 'trident', 'pike']
    matnames = ['iron', 'steel', 'bronze']
    shafts = [('ash', 'w'), ('darkwood', 'W')]
    combos = _sample(list(itertools.product(tips, matnames, shafts)), n)
    for tip, mn, (sname, sc) in combos:
        cv = Canvas()
        cv.vline(8, 4, 14, sc)
        cv.set(8, 6, 't')
        _spear_tip(cv, tip, MATERIALS[mn])
        cv.finish()
        out.append((f"{mn}_{tip}_{sname}_spear", f"{mn.capitalize()} {tip.capitalize()} Spear ({sname})", cv))
    return out


def build_bows(n=16):
    out = []
    # (kind, limb, extra): extra in plain/nocked/wrapped/tipped
    specs = [
        ('longbow', 'w', 'plain'), ('longbow', 'W', 'nocked'),
        ('longbow', 't', 'wrapped'), ('longbow', 'w', 'tipped'),
        ('recurve', 'w', 'plain'), ('recurve', 'z', 'nocked'),
        ('recurve', 't', 'wrapped'),
        ('shortbow', 'w', 'plain'), ('shortbow', 't', 'nocked'),
        ('shortbow', 'W', 'wrapped'),
        ('crossbow', 'w', 'plain'), ('crossbow', 'd', 'nocked'),
        ('longbow', 'z', 'nocked'), ('recurve', 'w', 'tipped'),
        ('shortbow', 'z', 'plain'), ('crossbow', 'W', 'wrapped'),
    ]
    for idx, (kind, limb, extra) in enumerate(specs[:n]):
        cv = Canvas()
        if kind == 'crossbow':
            cv.hline(4, 12, 4, limb)          # prod
            cv.vline(8, 4, 13, 'W')           # stock
            cv.rect(7, 5, 9, 6, 'd')          # nut
            if extra == 'nocked':
                cv.vline(8, 1, 3, 's')
                cv.set(8, 1, 'l')
            if extra == 'wrapped':
                cv.set(8, 9, 'r'); cv.set(8, 11, 'r')
        else:
            top, bot = (2, 13) if kind == 'longbow' else ((3, 12) if kind == 'recurve' else (4, 11))
            for y in range(top, bot + 1):
                t = (y - top) / max(1, bot - top)
                x = 5 + int(3 * math_sin(t))
                cv.set(x, y, limb)
            cv.vline(5, top, bot, 'c')        # string
            if kind == 'recurve':
                cv.set(5, top, 'o'); cv.set(5, bot, 'o')
            if extra == 'tipped':
                cv.set(5, top, 'd'); cv.set(5, bot, 'd')
            if extra == 'wrapped':
                my = (top + bot) // 2
                cv.set(5, my - 1, 'r'); cv.set(5, my + 1, 'r')
            if extra == 'nocked':
                my = (top + bot) // 2
                cv.hline(5, 11, my, 'w')
                cv.set(11, my, 's')
        cv.finish()
        label = f"{kind.capitalize()} ({limb_name(limb)}, {extra})"
        out.append((f"{kind}_{limb_name(limb).lower()}_{extra}_{idx}", label, cv))
    return out


def math_sin(t):
    import math
    return math.sin(t * math.pi)


def limb_name(limb):
    return {'w': 'Oak', 'W': 'Darkwood', 't': 'Yew', 'z': 'Bronze', 'd': 'Steel'}[limb]


TOPPERS = [
    ('fire_orb', 'o'), ('frost_orb', 'b'), ('nature_orb', 'n'),
    ('shadow_orb', 'p'), ('crystal', 'm'), ('skull', 'c'),
    ('star', 'y'), ('moon', 'l'), ('flame', 'r'), ('feather', 't'),
]


def build_staves(n=30):
    out = []
    shafts = [('oak', 'w'), ('darkwood', 'W'), ('ironshod', 'd')]
    combos = _sample(list(itertools.product(shafts, TOPPERS)), n)
    for (sname, shaft), (tname, tc) in combos:
        cv = Canvas()
        cv.vline(8, 5, 14, shaft)
        cv.set(8, 5, 't' if shaft != 'd' else 's')
        if tname.endswith('orb'):
            cv.disc(8, 3, 2, tc)
            cv.set(8, 2, 'l')
        elif tname == 'crystal':
            cv.diamond(8, 3, 2, tc)
            cv.set(8, 2, 'l')
        elif tname == 'skull':
            cv.disc(8, 3, 2, tc)
            cv.set(7, 3, 'K'); cv.set(9, 3, 'K')
        elif tname == 'star':
            cv.diamond(8, 3, 2, tc)
            cv.hline(5, 11, 3, tc)
        elif tname == 'moon':
            cv.disc(8, 3, 2, tc)
            cv.disc(9, 2, 2, None)  # crescent cutout (drawn pre-outline)
            # redraw crescent manually
            cv2 = Canvas()
            cv2.disc(8, 3, 2, tc)
            for y in range(1, 6):
                for x in range(8, 12):
                    if (x - 9) ** 2 + (y - 2) ** 2 <= 4 and cv2.get(x, y):
                        cv2.set(x, y, None)
            cv.blit(cv2)
        elif tname == 'flame':
            cv.tri(8, 1, 5, 4, tc, up=True)
            cv.tri(8, 2, 3, 3, 'y', up=True)
        elif tname == 'feather':
            cv.ellipse(8, 3, 2, 3, tc)
            cv.vline(8, 1, 5, 'c')
        cv.finish()
        out.append((f"{sname}_staff_{tname}", f"{sname.capitalize()} Staff of {tname.replace('_', ' ').title()}", cv))
    return out


def build_wands(n=24):
    out = []
    shafts = [('straight', 0), ('twisted', 1), ('bent', 2), ('gnarled', 3)]
    tips = [('spark', 'y'), ('star', 'y'), ('orb', 'b'), ('crystal', 'p'),
            ('leaf', 'n'), ('ember', 'r')]
    combos = _sample(list(itertools.product(shafts, tips)), n)
    for (sname, svar), (tname, tc) in combos:
        cv = Canvas()
        for y in range(7, 15):
            if svar == 1:      # twisted: tight zigzag
                x = 8 + ((y - 7) % 2) * 2 - 1
            elif svar == 2:    # bent: kink near top
                x = 8 + (1 if y > 10 else 0)
            elif svar == 3:    # gnarled: wide zigzag + knots
                x = 8 + (2 if (y - 7) // 2 % 2 == 0 else -2)
                if (y - 7) % 4 == 3:
                    cv.set(x + 1, y, 'W')
            else:              # straight
                x = 8
            cv.set(x, y, 'W')
        cv.set(8, 7, 't')
        if tname == 'spark':
            cv.set(8, 5, tc); cv.set(7, 6, tc); cv.set(9, 6, tc); cv.set(8, 6, 'l')
        elif tname == 'star':
            cv.diamond(8, 5, 2, tc)
        elif tname == 'orb':
            cv.disc(8, 5, 2, tc); cv.set(8, 4, 'l')
        elif tname == 'crystal':
            cv.diamond(8, 5, 1, tc)
        elif tname == 'leaf':
            cv.ellipse(8, 5, 2, 2, tc)
        elif tname == 'ember':
            cv.disc(8, 5, 1, tc); cv.set(8, 5, 'o')
        cv.finish()
        out.append((f"{sname}_wand_{tname}", f"{sname.capitalize()} Wand ({tname})", cv))
    return out


def build():
    icons = []
    icons += [("weapons/" + s, l, c) for s, l, c in build_swords()]
    icons += [("weapons/" + s, l, c) for s, l, c in build_daggers()]
    icons += [("weapons/" + s, l, c) for s, l, c in build_axes()]
    icons += [("weapons/" + s, l, c) for s, l, c in build_maces()]
    icons += [("weapons/" + s, l, c) for s, l, c in build_spears()]
    icons += [("weapons/" + s, l, c) for s, l, c in build_bows()]
    icons += [("weapons/" + s, l, c) for s, l, c in build_staves()]
    icons += [("weapons/" + s, l, c) for s, l, c in build_wands()]
    return icons
