"""RPG Icon Mega-Pack - canvas & palette foundation.
16x16 pixel grids, warm cohesive palette matching the Tiny Tavern /
200-icon pack aesthetic. Shapes are drawn in flat colors, then a
top-light pass adds highlights and an auto-outline pass adds the
signature dark-brown outline."""
import math
from PIL import Image

PALETTE = {
    'K': (36, 26, 18, 255),     # outline dark brown
    's': (184, 196, 204, 255),  # steel
    'l': (232, 240, 245, 255),  # steel light
    'd': (94, 107, 117, 255),   # steel dark
    'g': (232, 179, 61, 255),   # gold
    'G': (168, 116, 31, 255),   # gold dark
    'y': (250, 235, 130, 255),  # pale yellow
    'w': (138, 90, 43, 255),    # wood
    'W': (93, 58, 23, 255),     # wood dark
    't': (201, 158, 95, 255),   # leather tan
    'T': (150, 110, 60, 255),   # leather dark
    'r': (214, 64, 64, 255),    # red
    'R': (143, 36, 36, 255),    # red dark
    'o': (245, 166, 35, 255),   # orange glow
    'O': (200, 110, 20, 255),   # orange dark
    'b': (61, 125, 214, 255),   # blue
    'B': (31, 77, 143, 255),    # blue dark
    'm': (160, 225, 240, 255),  # mithril light
    'M': (95, 160, 195, 255),   # mithril dark
    'n': (95, 191, 77, 255),    # green
    'N': (47, 122, 34, 255),    # green dark
    'a': (70, 190, 175, 255),   # teal
    'A': (38, 128, 118, 255),   # teal dark
    'p': (150, 100, 220, 255),  # purple
    'P': (95, 55, 150, 255),    # purple dark
    'v': (235, 130, 180, 255),  # pink
    'V': (180, 70, 120, 255),   # pink dark
    'c': (240, 224, 184, 255),  # cream / parchment
    'C': (184, 155, 94, 255),   # parchment dark
    'k': (107, 107, 107, 255),  # gray
    'e': (38, 38, 43, 255),     # near-black
    'z': (186, 128, 62, 255),   # bronze
    'Z': (128, 82, 32, 255),    # bronze dark
    'x': (72, 58, 88, 255),     # dark violet (monster bodies)
}

# top-light pass: base color -> highlight color
LIGHT = {
    'd': 's', 's': 'l', 'G': 'g', 'W': 'w', 'T': 't', 'R': 'r',
    'O': 'o', 'B': 'b', 'M': 'm', 'N': 'n', 'A': 'a', 'P': 'p',
    'V': 'v', 'C': 'c', 'k': 's', 'Z': 'z', 'x': 'p',
}

# material sets: (name, edge, mid, dark, light)
MATERIALS = {
    'iron':     ('iron', 'd', 's', 'd', 'l'),
    'steel':    ('steel', 's', 'l', 'd', 'l'),
    'bronze':   ('bronze', 'z', 'z', 'Z', 'y'),
    'gold':     ('gold', 'g', 'g', 'G', 'y'),
    'mithril':  ('mithril', 'm', 'm', 'M', 'l'),
    'shadow':   ('shadow', 'k', 'e', 'e', 'k'),
    'wood':     ('wood', 'w', 'w', 'W', 't'),
    'leather':  ('leather', 't', 't', 'T', 'c'),
}


class Canvas:
    def __init__(self):
        self.g = [[None] * 16 for _ in range(16)]

    def inb(self, x, y):
        return 0 <= x < 16 and 0 <= y < 16

    def set(self, x, y, c):
        if self.inb(x, y) and c is not None:
            self.g[y][x] = c

    def get(self, x, y):
        if self.inb(x, y):
            return self.g[y][x]
        return None

    def hline(self, x0, x1, y, c):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            self.set(x, y, c)

    def vline(self, x, y0, y1, c):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            self.set(x, y, c)

    def rect(self, x0, y0, x1, y1, c, fill=True):
        x0, x1 = min(x0, x1), max(x0, x1)
        y0, y1 = min(y0, y1), max(y0, y1)
        if fill:
            for y in range(y0, y1 + 1):
                self.hline(x0, x1, y, c)
        else:
            self.hline(x0, x1, y0, c)
            self.hline(x0, x1, y1, c)
            self.vline(x0, y0, y1, c)
            self.vline(x1, y0, y1, c)

    def disc(self, cx, cy, r, c, fill=True):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            if fill:
                self.hline(cx - dx, cx + dx, cy + dy, c)
            else:
                self.set(cx - dx, cy + dy, c)
                self.set(cx + dx, cy + dy, c)

    def ellipse(self, cx, cy, rx, ry, c, fill=True):
        for dy in range(-ry, ry + 1):
            t = 1 - (dy * dy) / (ry * ry) if ry else 0
            dx = int(rx * math.sqrt(max(0, t)))
            if fill:
                self.hline(cx - dx, cx + dx, cy + dy, c)
            else:
                self.set(cx - dx, cy + dy, c)
                self.set(cx + dx, cy + dy, c)

    def diamond(self, cx, cy, r, c, fill=True):
        for dy in range(-r, r + 1):
            dx = r - abs(dy)
            if fill:
                self.hline(cx - dx, cx + dx, cy + dy, c)
            else:
                self.set(cx - dx, cy + dy, c)
                self.set(cx + dx, cy + dy, c)

    def tri(self, cx, y_tip, w_base, h, c, up=True):
        """Triangle with tip at (cx, y_tip), widening downward (up=True)."""
        for i in range(h):
            half = int((i + 1) * (w_base / 2) / h)
            y = y_tip + i if up else y_tip - i
            self.hline(cx - half, cx + half, y, c)

    def blit(self, other, dx=0, dy=0):
        for y in range(16):
            for x in range(16):
                c = other.g[y][x]
                if c is not None:
                    self.set(x + dx, y + dy, c)

    def flip_h(self):
        out = Canvas()
        for y in range(16):
            for x in range(16):
                out.g[y][15 - x] = self.g[y][x]
        return out

    def remap(self, mapping):
        """Return a copy with palette chars replaced per mapping dict."""
        out = Canvas()
        for y in range(16):
            for x in range(16):
                c = self.g[y][x]
                out.g[y][x] = mapping.get(c, c) if c is not None else None
        return out

    def outline(self, k='K'):
        src = [row[:] for row in self.g]
        for y in range(16):
            for x in range(16):
                if src[y][x] is not None:
                    continue
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 16 and 0 <= ny < 16 and src[ny][nx] is not None:
                            self.g[y][x] = k
                            break
                    else:
                        continue
                    break

    def toplight(self):
        for y in range(16):
            for x in range(16):
                c = self.g[y][x]
                if c is None or c == 'K' or c not in LIGHT:
                    continue
                above = self.get(x, y - 1)
                if above is None or above == 'K':
                    self.g[y][x] = LIGHT[c]

    def finish(self):
        """Apply top-light then outline. Call once per icon."""
        self.toplight()
        self.outline()
        return self

    def signature(self):
        """Exact pixel signature for duplicate detection."""
        return bytes((PALETTE[c][0] if c else 0) for row in self.g for c in row) + \
               bytes((PALETTE[c][1] if c else 0) for row in self.g for c in row) + \
               bytes((PALETTE[c][2] if c else 0) for row in self.g for c in row)

    def to_image(self, size=16):
        img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        px = img.load()
        for y in range(16):
            for x in range(16):
                c = self.g[y][x]
                if c is not None:
                    px[x, y] = PALETTE[c]
        if size != 16:
            img = img.resize((size, size), Image.NEAREST)
        return img

    def filled_count(self):
        return sum(1 for row in self.g for c in row if c is not None)
