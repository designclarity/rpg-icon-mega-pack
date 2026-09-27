"""Tools & items: lights, ropes, maps, compasses, bombs, arrows,
digging tools, vessels, camp gear, instruments, books, candles."""
import itertools
from canvas import Canvas


def _sample(combos, n):
    step = max(1, len(combos) // n)
    return combos[::step][:n]


def _light(cv, kind):
    if kind == 'lantern_square':
        cv.rect(5, 5, 11, 12, 'W')
        cv.rect(6, 6, 10, 11, 'o')
        cv.rect(6, 6, 10, 7, 'y')
        cv.hline(5, 11, 4, 'd')
        cv.set(8, 3, 'd')
    elif kind == 'lantern_round':
        cv.disc(8, 9, 4, 'W')
        cv.disc(8, 9, 3, 'o')
        cv.set(7, 8, 'y')
        cv.rect(6, 3, 10, 5, 'd')
    elif kind == 'torch':
        cv.vline(8, 7, 14, 'w')
        cv.tri(8, 2, 5, 5, 'o', up=True)
        cv.tri(8, 4, 3, 3, 'y', up=True)
    elif kind == 'candle_cluster':
        for x, h in ((5, 5), (8, 8), (11, 6)):
            cv.vline(x, 12 - h, 12, 'c')
            cv.set(x, 11 - h, 'y')
        cv.ellipse(8, 13, 5, 1, 'g')
    elif kind == 'oil_lamp':
        cv.ellipse(8, 10, 4, 3, 'z')
        cv.vline(11, 8, 9, 'Z')
        cv.set(12, 7, 'y')
    elif kind == 'brazier':
        cv.tri(8, 12, 7, 4, 'd', up=False)
        cv.ellipse(8, 8, 4, 2, 'e')
        cv.tri(8, 4, 4, 4, 'o', up=True)
    elif kind == 'chandelier':
        cv.hline(4, 12, 6, 'g')
        cv.vline(8, 2, 6, 'g')
        for x in (5, 8, 11):
            cv.set(x, 5, 'y')
    elif kind == 'glowstone':
        cv.diamond(8, 9, 4, 'm')
        cv.set(7, 8, 'l')
    elif kind == 'firefly_jar':
        cv.ellipse(8, 9, 4, 4, 'c')
        cv.rect(6, 4, 10, 5, 'w')
        cv.set(7, 8, 'y'); cv.set(10, 10, 'y'); cv.set(8, 11, 'y')
    elif kind == 'moon_lantern':
        cv.disc(8, 9, 4, 'l')
        cv.rect(6, 3, 10, 5, 'd')
        cv.hline(4, 12, 13, 'd')


def build_lights(n=16):
    out = []
    kinds = ['lantern_square', 'lantern_round', 'torch', 'candle_cluster',
             'oil_lamp', 'brazier', 'chandelier', 'glowstone',
             'firefly_jar', 'moon_lantern']
    combos = _sample(list(itertools.product(kinds, ['lit', 'unlit'])), n)
    for kind, state in combos:
        cv = Canvas()
        _light(cv, kind)
        if state == 'unlit':
            cv = cv.remap({'y': 'k', 'o': 'd', 'l': 's'})
        cv.finish()
        out.append((f"{kind}_{state}", f"{kind.replace('_', ' ').title()} ({state})", cv))
    return out


def _tool(cv, kind):
    if kind == 'rope_coil':
        cv.ellipse(8, 9, 5, 4, 't')
        cv.ellipse(8, 9, 3, 2, 'T')
        cv.set(12, 5, 't')
    elif kind == 'grappling_hook':
        cv.vline(8, 3, 10, 'd')
        for dx in (-3, 3):
            cv.vline(8 + dx, 8, 12, 'd')
            cv.set(8 + dx, 12, 's')
        cv.hline(5, 11, 8, 'd')
    elif kind == 'chain':
        for y in range(3, 14, 2):
            cv.ellipse(8, y, 2, 1, 's')
    elif kind == 'net':
        for x in range(3, 14, 3):
            cv.vline(x, 4, 12, 't')
        for y in range(4, 13, 3):
            cv.hline(3, 13, y, 't')
    elif kind == 'pulley':
        cv.disc(8, 8, 4, 'w', fill=False)
        cv.disc(8, 8, 2, 'd')
        cv.vline(8, 2, 4, 'd')
    elif kind == 'hook':
        cv.vline(8, 3, 9, 'd')
        cv.disc(8, 11, 2, 'd', fill=False)
        cv.set(10, 11, 's')
    elif kind == 'shackle':
        cv.ellipse(8, 7, 3, 3, 'd', fill=False)
        cv.rect(5, 9, 11, 12, 'd')
    elif kind == 'winch':
        cv.rect(4, 6, 12, 10, 'w')
        cv.disc(8, 8, 2, 'd')
        cv.vline(12, 8, 12, 'd')


def build_tools(n=12):
    out = []
    kinds = ['rope_coil', 'grappling_hook', 'chain', 'net',
             'pulley', 'hook', 'shackle', 'winch']
    combos = _sample(list(itertools.product(kinds, ['standard', 'dark_iron'])), n)
    for kind, variant in combos:
        cv = Canvas()
        _tool(cv, kind)
        if variant == 'dark_iron':
            cv = cv.remap({'w': 'W', 't': 'T', 's': 'd', 'd': 'e', 'c': 'C'})
        cv.finish()
        out.append((f"{kind}_{variant}", f"{kind.replace('_', ' ').title()} ({variant.replace('_', ' ')})", cv))
    return out


def build_maps(n=10):
    out = []
    kinds = ['scroll_map', 'folded_map', 'treasure_map', 'world_map', 'dungeon_map']
    combos = _sample(list(itertools.product(kinds, ['marked', 'plain'])), n)
    for kind, variant in combos:
        cv = Canvas()
        cv.rect(3, 4, 13, 12, 'c')
        cv.vline(3, 4, 12, 'C')
        if kind == 'scroll_map':
            cv.vline(2, 3, 13, 'w'); cv.vline(14, 3, 13, 'w')
        elif kind == 'folded_map':
            cv.vline(8, 4, 12, 'C')
        elif kind == 'treasure_map':
            cv.hline(4, 9, 10, 'R')
            cv.set(5, 6, 'b')
        elif kind == 'world_map':
            cv.ellipse(7, 8, 3, 2, 'n')
            cv.ellipse(11, 9, 2, 1, 'n')
        elif kind == 'dungeon_map':
            cv.rect(5, 6, 11, 10, 'e', fill=False)
            cv.hline(5, 8, 8, 'e')
        if variant == 'marked':
            cv.set(10, 7, 'r'); cv.set(11, 8, 'r'); cv.set(10, 9, 'r'); cv.set(9, 8, 'r')
        cv.finish()
        out.append((f"{kind}_{variant}", f"{kind.replace('_', ' ').title()} ({variant})", cv))
    return out


def _needle(cv, angle):
    # 6 distinct needle rotations
    if angle == 0:      # N-S
        cv.vline(8, 4, 12, 'r'); cv.set(8, 4, 'R')
    elif angle == 1:    # NE-SW
        for i in range(5):
            cv.set(8 + i, 4 + i, 'r'); cv.set(8 - i, 12 - i, 'c')
        cv.set(12, 8, 'R')
    elif angle == 2:    # E-W
        cv.hline(4, 12, 8, 'r'); cv.set(12, 8, 'R')
    elif angle == 3:    # SE-NW
        for i in range(5):
            cv.set(8 + i, 12 - i, 'r'); cv.set(8 - i, 4 + i, 'c')
        cv.set(12, 8, 'R')
    elif angle == 4:    # NNE-SSW (steep diag)
        for i in range(5):
            cv.set(9 + i // 2, 4 + i, 'r'); cv.set(7 - i // 2, 12 - i, 'c')
    elif angle == 5:    # NNW-SSE
        for i in range(5):
            cv.set(7 - i // 2, 4 + i, 'r'); cv.set(9 + i // 2, 12 - i, 'c')


def build_compasses(n=6):
    out = []
    for i in range(n):
        cv = Canvas()
        cv.disc(8, 8, 5, 'g')
        cv.disc(8, 8, 4, 'c')
        _needle(cv, i)
        cv.set(8, 8, 'K')
        for dx, dy in [(-5, 0), (5, 0), (0, -5), (0, 5)]:
            cv.set(8 + dx, 8 + dy, 'K')
        cv.finish()
        out.append((f"compass_{i}", f"Compass (variant {i + 1})", cv))
    return out


def _bomb(cv, kind):
    if kind == 'round_bomb':
        cv.disc(8, 10, 4, 'e')
        cv.set(6, 8, 'k')
        cv.vline(10, 4, 6, 't')
        cv.set(10, 3, 'o')
    elif kind == 'dynamite':
        for x in (6, 8, 10):
            cv.vline(x, 6, 12, 'r')
            cv.set(x, 6, 'c')
        cv.hline(6, 10, 5, 't')
        cv.set(8, 4, 'o')
    elif kind == 'powder_keg':
        cv.ellipse(8, 10, 4, 4, 'w')
        cv.hline(4, 12, 10, 'd')
        cv.set(8, 5, 't')
    elif kind == 'grenade':
        cv.disc(8, 10, 3, 'n')
        cv.rect(7, 5, 9, 7, 'd')
        cv.set(10, 5, 'd')
    elif kind == 'firecracker':
        cv.vline(8, 5, 13, 'r')
        cv.set(8, 4, 'y')
        cv.hline(6, 10, 9, 'G')
    elif kind == 'smoke_bomb':
        cv.disc(8, 10, 3, 'k')
        cv.disc(9, 6, 2, 'c')
        cv.disc(6, 4, 1, 'c')
    elif kind == 'bomb_bundle':
        for dx, dy in [(-3, 2), (3, 2), (0, -1)]:
            cv.disc(8 + dx, 10 + dy, 2, 'e')
        cv.vline(8, 3, 6, 't')
        cv.set(8, 2, 'o')
    elif kind == 'big_keg':
        cv.ellipse(8, 10, 5, 5, 'w')
        cv.hline(3, 13, 8, 'd'); cv.hline(3, 13, 12, 'd')
        cv.set(8, 4, 'r')
    elif kind == 'powder_horn':
        cv.tri(10, 6, 6, 8, 't', up=False)
        cv.rect(4, 8, 7, 10, 'd')
        cv.set(12, 9, 'o')
    elif kind == 'land_mine':
        cv.ellipse(8, 10, 5, 3, 'd')
        for x in (4, 8, 12):
            cv.set(x, 6, 's')
        cv.set(8, 7, 'r')


def build_bombs(n=10):
    out = []
    kinds = ['round_bomb', 'dynamite', 'powder_keg', 'grenade', 'firecracker',
             'smoke_bomb', 'bomb_bundle', 'big_keg', 'powder_horn', 'land_mine']
    for kind in _sample(kinds, n):
        cv = Canvas()
        _bomb(cv, kind)
        cv.finish()
        out.append((f"{kind}", f"{kind.replace('_', ' ').title()}", cv))
    return out


def _arrow(cv, kind):
    if kind == 'arrow':
        cv.hline(2, 12, 8, 'w')
        cv.tri(14, 8, 3, 4, 's', up=False)
        cv.tri(2, 8, 3, 4, 'r', up=True)
    elif kind == 'bolt':
        cv.hline(3, 12, 8, 'd')
        cv.set(13, 8, 'l')
        cv.set(2, 8, 'c')
    elif kind == 'fire_arrow':
        cv.hline(2, 11, 8, 'w')
        cv.tri(13, 8, 3, 5, 'o', up=False)
        cv.set(13, 8, 'y')
    elif kind == 'frost_arrow':
        cv.hline(2, 11, 8, 'w')
        cv.diamond(13, 8, 2, 'm')
    elif kind == 'quiver':
        cv.tri(8, 12, 5, 8, 'T', up=False)
        cv.hline(5, 11, 4, 't')
        cv.vline(7, 1, 4, 'w'); cv.vline(9, 1, 4, 'w')
        cv.set(7, 1, 's'); cv.set(9, 1, 's')
    elif kind == 'bundle':
        for dx in (-2, 0, 2):
            cv.vline(8 + dx, 3, 13, 'w')
            cv.set(8 + dx, 3, 's')
        cv.hline(5, 11, 8, 't')
    elif kind == 'long_arrow':
        cv.hline(1, 12, 8, 'w')
        cv.tri(14, 8, 3, 4, 's', up=False)
        cv.set(1, 8, 'b')
    elif kind == 'barbed_arrow':
        cv.hline(2, 11, 8, 'w')
        cv.tri(13, 8, 3, 4, 'd', up=False)
        cv.set(11, 7, 'd'); cv.set(11, 9, 'd')
    elif kind == 'hunting_arrow':
        cv.hline(2, 12, 8, 'w')
        cv.tri(14, 8, 3, 4, 'n', up=False)
        cv.tri(2, 8, 3, 4, 'n', up=True)
    elif kind == 'war_bolt':
        cv.hline(3, 11, 8, 'W')
        cv.tri(13, 8, 3, 5, 'd', up=False)
        cv.set(3, 8, 'r')
    elif kind == 'javelin':
        cv.vline(8, 2, 12, 'w')
        cv.tri(8, 2, 3, 4, 's', up=True)
        cv.set(8, 13, 'r')
    elif kind == 'quiver_full':
        cv.tri(8, 13, 6, 9, 'T', up=False)
        cv.hline(4, 12, 5, 't')
        for x in (6, 8, 10):
            cv.vline(x, 1, 5, 'w')
            cv.set(x, 1, 's')
    elif kind == 'signal_arrow':
        cv.hline(2, 11, 8, 'w')
        cv.diamond(13, 8, 2, 'r')
        cv.set(13, 8, 'y')
    elif kind == 'blunt_arrow':
        cv.hline(2, 11, 8, 'w')
        cv.disc(13, 8, 2, 't')
        cv.tri(2, 8, 3, 4, 'b', up=True)


def build_arrows(n=14):
    out = []
    kinds = ['arrow', 'bolt', 'fire_arrow', 'frost_arrow', 'quiver', 'bundle',
             'long_arrow', 'barbed_arrow', 'hunting_arrow', 'war_bolt',
             'javelin', 'quiver_full', 'signal_arrow', 'blunt_arrow']
    for kind in _sample(kinds, n):
        cv = Canvas()
        _arrow(cv, kind)
        cv.finish()
        out.append((f"{kind}", f"{kind.replace('_', ' ').title()}", cv))
    return out


def _dig(cv, kind, handle):
    hc = 'w' if handle == 'oak' else 'W'
    if kind == 'pickaxe':
        cv.vline(8, 5, 14, hc)
        cv.hline(3, 13, 4, 'd')
        cv.set(3, 5, 's'); cv.set(13, 5, 's')
    elif kind == 'shovel':
        cv.vline(8, 3, 9, hc)
        cv.ellipse(8, 11, 2, 3, 'd')
        cv.set(8, 9, 's')
    elif kind == 'hoe':
        cv.vline(8, 4, 14, hc)
        cv.hline(8, 12, 5, 'd')
        cv.vline(12, 5, 7, 'd')
    elif kind == 'sickle':
        cv.vline(8, 7, 14, hc)
        for x in range(8, 14):
            cv.set(x, 7 - (x - 8) // 2, 's')
    elif kind == 'trowel':
        cv.vline(8, 9, 14, hc)
        cv.tri(8, 3, 4, 6, 's', up=True)


def build_digging(n=10):
    out = []
    kinds = ['pickaxe', 'shovel', 'hoe', 'sickle', 'trowel']
    combos = _sample(list(itertools.product(kinds, ['oak', 'darkwood'])), n)
    for kind, handle in combos:
        cv = Canvas()
        _dig(cv, kind, handle)
        cv.finish()
        out.append((f"{kind}_{handle}", f"{kind.replace('_', ' ').title()} ({handle})", cv))
    return out


def _vessel(cv, kind):
    if kind == 'bucket':
        cv.tri(8, 12, 7, 6, 'w', up=False)
        cv.hline(4, 12, 6, 'b')
        cv.set(8, 3, 'd')
    elif kind == 'tankard':
        cv.rect(5, 6, 10, 13, 'w')
        cv.rect(10, 8, 13, 12, 'W', fill=False)
    elif kind == 'bowl':
        cv.ellipse(8, 9, 5, 3, 't')
        cv.ellipse(8, 8, 5, 2, 'c')
    elif kind == 'plate':
        cv.ellipse(8, 9, 6, 2, 'c')
        cv.ellipse(8, 9, 4, 1, 'C')
    elif kind == 'waterskin':
        cv.ellipse(8, 10, 3, 4, 'T')
        cv.vline(8, 4, 6, 'W')
        cv.set(8, 8, 't')
    elif kind == 'barrel':
        cv.ellipse(8, 9, 4, 5, 'w')
        cv.hline(4, 12, 7, 'd'); cv.hline(4, 12, 11, 'd')


def build_vessels(n=10):
    out = []
    kinds = ['bucket', 'tankard', 'bowl', 'plate', 'waterskin', 'barrel']
    combos = _sample(list(itertools.product(kinds, ['full', 'empty'])), n)
    for kind, state in combos:
        cv = Canvas()
        _vessel(cv, kind)
        if state == 'full':
            if kind == 'bucket':
                cv.hline(5, 11, 7, 'b')
            elif kind == 'tankard':
                cv.rect(5, 6, 10, 8, 'y')   # foam head
                cv.set(7, 7, 'l')
            elif kind == 'bowl':
                cv.ellipse(8, 8, 4, 1, 'r')
            elif kind == 'plate':
                cv.ellipse(8, 9, 3, 1, 't')
            elif kind == 'waterskin':
                cv.set(8, 6, 'b')
            elif kind == 'barrel':
                cv.set(8, 5, 'y')
        cv.finish()
        out.append((f"{kind}_{state}", f"{kind.replace('_', ' ').title()} ({state})", cv))
    return out


def _camp(cv, kind):
    if kind == 'tent':
        cv.tri(8, 4, 9, 9, 't', up=True)
        cv.tri(8, 9, 4, 4, 'e', up=True)
    elif kind == 'bedroll':
        cv.ellipse(8, 10, 5, 3, 'r')
        cv.ellipse(8, 10, 5, 3, 'R', fill=False)
        cv.hline(4, 12, 10, 't')
    elif kind == 'campfire':
        for dx in (-3, 3):
            cv.vline(8 + dx, 10, 12, 'w')
        cv.tri(8, 5, 5, 5, 'o', up=True)
        cv.tri(8, 7, 3, 3, 'y', up=True)
    elif kind == 'banner':
        cv.vline(5, 3, 13, 'w')
        cv.rect(5, 3, 12, 9, 'b')
        cv.tri(12, 9, 3, 3, 'b', up=False)
        cv.set(8, 6, 'y')
    elif kind == 'crate':
        cv.rect(4, 7, 12, 13, 'w')
        cv.hline(4, 12, 7, 'W'); cv.hline(4, 12, 13, 'W')
        cv.vline(8, 7, 13, 'W')


def build_camp(n=10):
    out = []
    kinds = ['tent', 'bedroll', 'campfire', 'banner', 'crate']
    combos = _sample(list(itertools.product(kinds, ['day', 'night'])), n)
    for kind, time in combos:
        cv = Canvas()
        _camp(cv, kind)
        if time == 'night':
            cv = cv.remap({'t': 'T', 'c': 'C', 'r': 'R', 'b': 'B', 'w': 'W',
                           'y': 'G', 'o': 'O', 'e': 'e'})
            cv.set(3, 2, 'l'); cv.set(13, 3, 'l')
        cv.finish()
        out.append((f"{kind}_{time}", f"{kind.replace('_', ' ').title()} ({time})", cv))
    return out


def _instrument(cv, kind):
    if kind == 'lute':
        cv.disc(7, 10, 3, 'w')
        cv.vline(10, 4, 8, 'W')
        cv.set(10, 4, 't')
    elif kind == 'horn':
        cv.tri(11, 8, 6, 6, 'y', up=False)
        cv.set(5, 8, 'G')
    elif kind == 'drum':
        cv.ellipse(8, 7, 4, 2, 'c')
        cv.rect(4, 7, 12, 12, 'r')
        cv.vline(4, 7, 12, 'R')
    elif kind == 'flute':
        cv.vline(8, 4, 13, 'z')
        for y in (7, 9, 11):
            cv.set(8, y, 'K')
    elif kind == 'harp':
        cv.tri(8, 4, 6, 9, 'g', up=True)
        for x in (6, 8, 10):
            cv.vline(x, 6, 11, 'c')


def build_instruments(n=8):
    out = []
    kinds = ['lute', 'horn', 'drum', 'flute', 'harp']
    combos = _sample(list(itertools.product(kinds, ['notes', 'silent'])), n)
    for kind, sound in combos:
        cv = Canvas()
        _instrument(cv, kind)
        if sound == 'notes':
            cv.set(12, 3, 'c'); cv.set(13, 5, 'c'); cv.set(11, 2, 'c')
        cv.finish()
        out.append((f"{kind}_{sound}", f"{kind.replace('_', ' ').title()} ({sound})", cv))
    return out


def build_books(n=8):
    out = []
    colors = [('red', 'R'), ('blue', 'B'), ('green', 'N'), ('purple', 'P')]
    combos = _sample(list(itertools.product(colors, ['closed', 'open'])), n)
    for (cname, c), state in combos:
        cv = Canvas()
        if state == 'closed':
            cv.rect(4, 4, 11, 12, c)
            cv.rect(4, 4, 5, 12, 'c')
            cv.hline(7, 10, 8, 'g')
        else:
            cv.rect(2, 5, 7, 12, 'c')
            cv.rect(9, 5, 14, 12, 'c')
            cv.rect(2, 5, 3, 12, c)
            cv.rect(13, 5, 14, 12, c)
            cv.hline(4, 6, 8, 'K'); cv.hline(10, 12, 8, 'K')
        cv.finish()
        out.append((f"{cname}_tome_{state}", f"{cname.capitalize()} Tome ({state})", cv))
    return out


def build_candles(n=8):
    out = []
    combos = _sample(list(itertools.product([5, 8, 11], [5, 7, 9])), n)
    for i, (x, h) in enumerate(combos):
        cv = Canvas()
        cv.vline(x, 12 - h, 12, 'c')
        cv.set(x, 11 - h, 'y')
        cv.set(x, 10 - h, 'o')
        cv.ellipse(8, 13, 4, 1, 'g')
        cv.finish()
        out.append((f"candle_{i}", f"Candle (variant {i + 1})", cv))
    return out


def build():
    icons = []
    icons += [("items/" + s, l, c) for s, l, c in build_lights()]
    icons += [("items/" + s, l, c) for s, l, c in build_tools()]
    icons += [("items/" + s, l, c) for s, l, c in build_maps()]
    icons += [("items/" + s, l, c) for s, l, c in build_compasses()]
    icons += [("items/" + s, l, c) for s, l, c in build_bombs()]
    icons += [("items/" + s, l, c) for s, l, c in build_arrows()]
    icons += [("items/" + s, l, c) for s, l, c in build_digging()]
    icons += [("items/" + s, l, c) for s, l, c in build_vessels()]
    icons += [("items/" + s, l, c) for s, l, c in build_camp()]
    icons += [("items/" + s, l, c) for s, l, c in build_instruments()]
    icons += [("items/" + s, l, c) for s, l, c in build_books()]
    icons += [("items/" + s, l, c) for s, l, c in build_candles()]
    return icons
