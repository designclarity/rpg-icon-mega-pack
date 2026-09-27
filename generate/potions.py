"""Potions & consumables: potion bottles x liquids x stoppers, food,
herbs, elixirs."""
import itertools
from canvas import Canvas

LIQUIDS = [
    ('healing', 'r'), ('mana', 'b'), ('poison', 'n'), ('shadow', 'p'),
    ('fire', 'o'), ('frost', 'm'), ('nature', 'a'), ('love', 'v'),
    ('holy', 'y'), ('stamina', 'O'),
]
LIQUID_DARK = {'r': 'R', 'b': 'B', 'n': 'N', 'p': 'P', 'o': 'O', 'm': 'M',
               'a': 'A', 'v': 'V', 'y': 'G', 'O': 'R'}


def _bottle_body(cv, shape, liquid):
    lc = liquid
    dc = LIQUID_DARK[liquid]
    if shape == 'flask':
        cv.disc(8, 10, 4, lc)
        cv.disc(8, 10, 4, dc)  # placeholder replaced below
        cv.disc(8, 10, 4, lc)
        cv.vline(7, 3, 6, 'c'); cv.vline(9, 3, 6, 'c')
        # shade lower half
        for y in range(11, 14):
            for x in range(4, 13):
                if cv.get(x, y) == lc:
                    cv.set(x, y, dc)
    elif shape == 'tall_vial':
        cv.rect(6, 6, 10, 13, lc)
        cv.vline(6, 6, 13, dc)
        cv.rect(7, 3, 9, 5, 'c')
    elif shape == 'square_bottle':
        cv.rect(5, 7, 11, 13, lc)
        cv.rect(7, 4, 9, 6, 'c')
        cv.vline(5, 7, 13, dc)
        cv.hline(5, 11, 7, 'l')
    elif shape == 'gourd':
        cv.disc(8, 11, 3, lc)
        cv.disc(8, 6, 2, lc)
        cv.vline(7, 3, 4, 'c'); cv.vline(9, 3, 4, 'c')
    elif shape == 'teardrop':
        cv.tri(8, 4, 7, 6, lc, up=True)
        cv.disc(8, 11, 3, lc)
    elif shape == 'wide_jar':
        cv.ellipse(8, 10, 5, 4, lc)
        cv.rect(6, 4, 10, 6, 'c')
        cv.hline(4, 12, 8, dc)
    elif shape == 'phial':
        cv.rect(7, 8, 9, 13, lc)
        cv.vline(7, 8, 13, dc)
        cv.rect(7, 5, 9, 7, 'c')
    elif shape == 'round_belly':
        cv.disc(8, 10, 5, lc)
        cv.vline(7, 2, 5, 'c'); cv.vline(9, 2, 5, 'c')
        for y in range(11, 15):
            for x in range(3, 14):
                if cv.get(x, y) == lc:
                    cv.set(x, y, dc)
    # bubbles
    cv.set(7, 11, 'l'); cv.set(9, 9, 'l')


def _stopper(cv, kind, shape):
    if kind == 'cork':
        if shape in ('tall_vial', 'phial'):
            cv.rect(7, 2, 9, 4, 't')
        else:
            cv.rect(7, 1, 9, 3, 't')
    elif kind == 'cap':
        if shape in ('tall_vial', 'phial'):
            cv.rect(6, 2, 10, 4, 'd')
        else:
            cv.rect(6, 1, 10, 3, 'd')
    # 'open' -> nothing


def build_potions(n=110):
    out = []
    shapes = ['flask', 'tall_vial', 'square_bottle', 'gourd', 'teardrop',
              'wide_jar', 'phial', 'round_belly']
    stoppers = ['cork', 'cap', 'open']
    combos = _sample(list(itertools.product(shapes, LIQUIDS, stoppers)), n)
    for shape, (lname, lc), stopper in combos:
        cv = Canvas()
        _bottle_body(cv, shape, lc)
        _stopper(cv, stopper, shape)
        cv.finish()
        st = f"_{stopper}" if stopper != 'open' else ""
        out.append((f"{lname}_potion_{shape}{st}",
                    f"{lname.capitalize()} Potion ({shape.replace('_', ' ')}{', ' + stopper if stopper != 'open' else ''})",
                    cv))
    return out


def _sample(combos, n):
    step = max(1, len(combos) // n)
    return combos[::step][:n]


def _food(cv, kind):
    if kind == 'bread':
        cv.ellipse(8, 9, 5, 3, 't')
        cv.set(6, 8, 'c'); cv.set(10, 8, 'c')
    elif kind == 'meat':
        cv.ellipse(7, 9, 3, 3, 'r')
        cv.vline(11, 5, 12, 'c'); cv.vline(12, 5, 12, 'c')
        cv.set(7, 8, 'R')
    elif kind == 'apple':
        cv.disc(8, 9, 3, 'r')
        cv.vline(8, 4, 6, 'W')
        cv.ellipse(10, 5, 2, 1, 'n')
    elif kind == 'cheese':
        cv.tri(8, 5, 9, 7, 'y', up=True)
        cv.set(7, 9, 'G'); cv.set(9, 8, 'G')
    elif kind == 'fish':
        cv.ellipse(7, 8, 4, 2, 'b')
        cv.tri(12, 8, 3, 5, 'b', up=False)
        cv.set(5, 8, 'K')
    elif kind == 'mushroom':
        cv.ellipse(8, 6, 4, 3, 'r')
        cv.rect(7, 8, 9, 12, 'c')
        cv.set(6, 5, 'c'); cv.set(10, 5, 'c')
    elif kind == 'pie':
        cv.tri(8, 6, 8, 6, 't', up=True)
        cv.set(8, 7, 'r')
    elif kind == 'carrot':
        cv.tri(8, 12, 4, 8, 'o', up=False)
        cv.tri(8, 4, 4, 3, 'n', up=True)
    elif kind == 'cake':
        cv.rect(4, 8, 12, 12, 'v')
        cv.rect(4, 7, 12, 8, 'c')
        cv.set(8, 5, 'r')
    elif kind == 'egg':
        cv.ellipse(8, 9, 3, 4, 'c')
        cv.set(8, 9, 'y')
    elif kind == 'berries':
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (-1, 2), (1, 2)]:
            cv.disc(8 + dx, 9 + dy, 1, 'P')
        cv.vline(8, 4, 6, 'N')
    elif kind == 'drumstick':
        cv.ellipse(7, 10, 3, 2, 'T')
        cv.vline(11, 6, 9, 'c')
        cv.set(7, 10, 't')


def build_food(n=24):
    out = []
    kinds = ['bread', 'meat', 'apple', 'cheese', 'fish', 'mushroom', 'pie',
             'carrot', 'cake', 'egg', 'berries', 'drumstick']
    variants = ['fresh', 'cooked']
    combos = _sample(list(itertools.product(kinds, variants)), n)
    for kind, var in combos:
        cv = Canvas()
        _food(cv, kind)
        if var == 'cooked':
            # sear marks + darker roast tone on every cooked item
            cv = cv.remap({'t': 'T', 'c': 'C', 'r': 'R', 'n': 'N', 'y': 'G',
                           'b': 'B', 'v': 'V', 'o': 'O'})
            cv.set(6, 5, 'O')
            cv.set(10, 4, 'c')
        cv.finish()
        out.append((f"{kind}_{var}", f"{kind.capitalize()} ({var})", cv))
    return out


def _herb(cv, kind):
    if kind == 'sprig':
        cv.vline(8, 5, 13, 'N')
        for y in (6, 9, 12):
            cv.set(6, y, 'n'); cv.set(10, y, 'n')
    elif kind == 'flower':
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            cv.disc(8 + dx, 8 + dy, 1, 'v')
        cv.set(8, 8, 'y')
        cv.vline(8, 10, 13, 'N')
    elif kind == 'root':
        cv.tri(8, 12, 4, 6, 't', up=False)
        cv.set(7, 9, 'T')
    elif kind == 'bluecap':
        cv.ellipse(8, 6, 3, 2, 'b')
        cv.rect(7, 8, 9, 12, 'c')
    elif kind == 'glowshroom':
        cv.ellipse(8, 6, 3, 2, 'm')
        cv.rect(7, 8, 9, 12, 'c')
        cv.set(8, 5, 'l')
    elif kind == 'thorn':
        cv.vline(8, 4, 13, 'N')
        cv.set(6, 7, 'N'); cv.set(10, 9, 'N')
        cv.set(8, 4, 'r')
    elif kind == 'moss':
        cv.ellipse(8, 11, 5, 2, 'N')
        cv.set(6, 10, 'n'); cv.set(10, 10, 'n')
    elif kind == 'sunpetal':
        for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3)]:
            cv.set(8 + dx, 7 + dy, 'y')
        cv.set(8, 7, 'o')
        cv.vline(8, 9, 13, 'N')


def build_herbs(n=16):
    out = []
    kinds = ['sprig', 'flower', 'root', 'bluecap', 'glowshroom', 'thorn', 'moss', 'sunpetal']
    combos = _sample(list(itertools.product(kinds, ['sprout', 'mature'])), n)
    for kind, stage in combos:
        cv = Canvas()
        _herb(cv, kind)
        if stage == 'mature':
            # extra foliage marks a mature plant
            cv.set(5, 5, 'n'); cv.set(11, 5, 'n'); cv.set(8, 2, 'n')
        cv.finish()
        out.append((f"herb_{kind}_{stage}", f"{kind.replace('_', ' ').title()} Herb ({stage})", cv))
    return out


def build_elixirs(n=24):
    out = []
    shapes = ['slim', 'bulb', 'twin', 'hourglass']
    combos = _sample(list(itertools.product(shapes, LIQUIDS)), n)
    for shape, (lname, lc) in combos:
        cv = Canvas()
        dc = LIQUID_DARK[lc]
        if shape == 'slim':
            cv.rect(7, 4, 9, 13, lc)
            cv.vline(7, 4, 13, dc)
            cv.rect(7, 2, 9, 3, 'd')
        elif shape == 'bulb':
            cv.disc(8, 11, 3, lc)
            cv.rect(7, 4, 9, 8, lc)
            cv.vline(7, 4, 8, dc)
            cv.rect(7, 2, 9, 3, 'g')
        elif shape == 'twin':
            cv.rect(5, 6, 7, 13, lc)
            cv.rect(9, 6, 11, 13, lc)
            cv.hline(5, 11, 5, 'd')
        elif shape == 'hourglass':
            cv.tri(8, 4, 6, 4, lc, up=True)
            cv.tri(8, 12, 6, 4, lc, up=False)
        cv.set(8, 10, 'l')
        cv.finish()
        out.append((f"{lname}_elixir_{shape}", f"{lname.capitalize()} Elixir ({shape})", cv))
    return out


def build():
    icons = []
    icons += [("potions/" + s, l, c) for s, l, c in build_potions()]
    icons += [("potions/" + s, l, c) for s, l, c in build_food()]
    icons += [("potions/" + s, l, c) for s, l, c in build_herbs()]
    icons += [("potions/" + s, l, c) for s, l, c in build_elixirs()]
    return icons
