"""Build the temporary memory-game skin; never writes original game artwork.

The plush atlas was made with imagegen. This script only extracts and sizes its
sprites, fits the existing cat plush, and draws deterministic UI geometry.
Run manually, before replacing these temporary assets with commissioned art.
"""

from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'game/images/minigames/memory'
GOLD = '#E4C575'
PLUM = '#30243E'
LAVENDER = '#A58AC5'
CREAM = '#FFF1DB'
PINK = '#E7A9BC'
SCALE = 3


def canvas(size):
    return Image.new('RGBA', tuple(n * SCALE for n in size))


def rounded(draw, bounds, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(tuple(int(v * SCALE) for v in bounds), int(radius * SCALE), fill=fill, outline=outline, width=max(1, int(width * SCALE)))


def line(draw, points, fill=GOLD, width=1):
    draw.line([(int(x * SCALE), int(y * SCALE)) for x, y in points], fill=fill, width=max(1, int(width * SCALE)))


def star(draw, x, y, radius, color=GOLD):
    points = []
    for i in range(8):
        angle = i * math.pi / 4 - math.pi / 2
        r = radius if i % 2 == 0 else radius * .25
        points.append(((x + math.cos(angle) * r) * SCALE, (y + math.sin(angle) * r) * SCALE))
    draw.polygon(points, fill=color)


def moon(image, center, radius, color=GOLD):
    # Draw into its own alpha layer; cutting the crescent does not erase the UI.
    layer = Image.new('RGBA', image.size)
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse(tuple(int(v * SCALE) for v in (x - radius, y - radius, x + radius, y + radius)), fill=color)
    d.ellipse(tuple(int(v * SCALE) for v in (x - radius * .18, y - radius * 1.12, x + radius * 1.42, y + radius * .48)), fill=(0, 0, 0, 0))
    image.alpha_composite(layer)


def save(image, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.resize((image.width // SCALE, image.height // SCALE), Image.Resampling.LANCZOS).save(path)


def gradient(size, top, bottom):
    image = canvas(size)
    d = ImageDraw.Draw(image)
    a, b = tuple(bytes.fromhex(top.lstrip('#'))), tuple(bytes.fromhex(bottom.lstrip('#')))
    for y in range(image.height):
        t = y / max(1, image.height - 1)
        d.line((0, y, image.width, y), fill=tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3)) + (255,))
    return image


def card_textures():
    folder = DEST / 'tsuki_plushies'
    for front in (True, False):
        im = canvas((400, 560))
        d = ImageDraw.Draw(im)
        rounded(d, (13, 16, 387, 547), 27, '#1c1326a0')
        rounded(d, (10, 8, 390, 539), 25, CREAM if front else '#493459', GOLD, 2)
        rounded(d, (21, 20, 379, 527), 18, outline='#ceb57b' if front else '#A58AC5', width=1)
        rounded(d, (28, 27, 372, 520), 14, outline='#e7d4b4' if front else '#765882', width=.6)
        if front:
            # Delicate printed stars and a label baseline leave space for art.
            for x, y in ((48, 55), (352, 55), (48, 487), (352, 487)):
                star(d, x, y, 6, '#cfb376')
            line(d, ((88, 466), (170, 466)), '#dcc395')
            line(d, ((230, 466), (312, 466)), '#dcc395')
            moon(im, (200, 466), 9, '#bc9862')
        else:
            for x, y, r in ((80, 100, 6), (310, 110, 10), (92, 414, 10), (315, 438, 6), (100, 208, 4), (308, 324, 5), (200, 88, 9), (200, 459, 9)):
                star(d, x, y, r)
            d.ellipse((84*SCALE, 153*SCALE, 316*SCALE, 385*SCALE), outline='#9b7cae', width=2*SCALE)
            d.ellipse((91*SCALE, 160*SCALE, 309*SCALE, 378*SCALE), outline='#765882', width=SCALE)
            moon(im, (195, 269), 75)
            d = ImageDraw.Draw(im)
            star(d, 254, 223, 18, CREAM)
            star(d, 270, 282, 9)
            # Top and bottom corner flourishes.
            for y, direction in ((55, 1), (493, -1)):
                line(d, ((53, y+direction*22), (53, y), (112, y)), width=1)
                line(d, ((347, y+direction*22), (347, y), (288, y)), width=1)
                star(d, 53, y, 4)
                star(d, 347, y, 4)
        save(im, folder / ('front.png' if front else 'back.png'))
    for name, colour in (('highlight', (228, 197, 117, 230)), ('incorrect', (226, 89, 105, 235))):
        outline = canvas((400, 560))
        rounded(ImageDraw.Draw(outline), (10, 8, 390, 539), 25, outline=colour, width=5)
        glow = outline.filter(ImageFilter.GaussianBlur(5 * SCALE))
        glow.alpha_composite(outline)
        save(glow, folder / (name + '.png'))


def panel(path, fill, radius=22, width=2):
    im = canvas((160, 160))
    d = ImageDraw.Draw(im)
    rounded(d, (4, 4, 156, 156), radius, fill, '#E4C575b0', width)
    rounded(d, (9, 9, 151, 151), max(3, radius-5), outline='#A58AC530', width=1)
    save(im, path)


def ui_assets():
    folder = DEST / 'ui'
    panel(folder / 'panel.png', '#30243Ef5')
    panel(folder / 'dialogue.png', '#21192ded')
    panel(folder / 'stat.png', '#45344fee', radius=18, width=1)
    panel(folder / 'button.png', '#544068', radius=24, width=2)
    panel(folder / 'button_hover.png', '#745a8a', radius=24, width=2)
    panel(folder / 'button_disabled.png', '#3b3045', radius=24, width=1)
    mask = canvas((160, 160))
    rounded(ImageDraw.Draw(mask), (0, 0, 160, 160), 14, '#ffffff')
    save(mask, folder / 'portrait_mask.png')
    for name in ('restart', 'instructions', 'exit', 'save', 'menu', 'play', 'moon', 'clock', 'pairs', 'trophy'):
        im = canvas((64, 64))
        d = ImageDraw.Draw(im)
        if name == 'moon':
            moon(im, (30, 33), 20)
            star(d, 49, 18, 6)
        elif name == 'clock':
            d.ellipse((11*SCALE,11*SCALE,53*SCALE,53*SCALE), outline=GOLD, width=3*SCALE)
            line(d, ((32,20),(32,33),(42,39)), width=3)
        elif name == 'pairs':
            rounded(d, (10,18,35,52), 4, outline=GOLD, width=2)
            rounded(d, (28,10,53,44), 4, '#544068', GOLD, 2)
            star(d, 41, 27, 6)
        elif name == 'trophy':
            d.polygon([(21*SCALE,13*SCALE),(43*SCALE,13*SCALE),(39*SCALE,35*SCALE),(32*SCALE,40*SCALE),(25*SCALE,35*SCALE)], fill=GOLD)
            line(d, ((32,39),(32,49)), width=3)
            line(d, ((22,51),(42,51)), width=3)
            line(d, ((21,19),(13,19),(14,30),(25,35)), width=2)
            line(d, ((43,19),(51,19),(50,30),(39,35)), width=2)
        elif name == 'restart':
            d.arc((12*SCALE,12*SCALE,52*SCALE,52*SCALE), 35, 310, fill=GOLD, width=3*SCALE)
            d.polygon([(46*SCALE,8*SCALE),(50*SCALE,26*SCALE),(34*SCALE,21*SCALE)], fill=GOLD)
        elif name == 'instructions':
            rounded(d, (11,11,53,53), 8, outline=GOLD, width=2)
            d.ellipse((30*SCALE,19*SCALE,34*SCALE,23*SCALE), fill=GOLD)
            line(d, ((32,29),(32,44)), width=3)
        elif name == 'exit':
            line(d, ((31,12),(15,12),(15,52),(31,52)), width=3)
            line(d, ((29,32),(53,32),(44,23)), width=3)
            line(d, ((53,32),(44,41)), width=3)
        elif name == 'save':
            rounded(d, (12,11,52,53), 5, outline=GOLD, width=2)
            rounded(d, (21,13,43,28), 2, outline=GOLD, width=2)
            rounded(d, (21,37,43,51), 2, outline=GOLD, width=2)
        elif name == 'menu':
            for y in (19,32,45):
                line(d, ((16,y),(48,y)), width=3)
        else:
            d.polygon([(23*SCALE,15*SCALE),(49*SCALE,32*SCALE),(23*SCALE,49*SCALE)], fill=GOLD)
        save(im, folder / ('icon_' + name + '.png'))
    # A quiet, intentionally unobtrusive plum/lavender surface for the game UI.
    im = gradient((1920, 1080), '#30243E', '#1e1729')
    decor = canvas((1920, 1080))
    d = ImageDraw.Draw(decor)
    for bounds, color in (((-300,-450,950,700),'#A58AC522'),((1200,300,2300,1500),'#A58AC51c')):
        d.ellipse(tuple(int(n*SCALE) for n in bounds), fill=color)
    decor = decor.filter(ImageFilter.GaussianBlur(80*SCALE))
    im.alpha_composite(decor)
    d = ImageDraw.Draw(im)
    rng = random.Random(23)
    for _ in range(65):
        x, y = rng.randrange(35,1885), rng.randrange(25,1055)
        star(d,x,y,rng.choice((1,1,2,3)), '#E4C57545')
    rounded(d, (24,24,1896,1056), 30, outline='#E4C57560', width=1)
    line(d, ((64,111),(550,111)), '#E4C57545')
    line(d, ((1370,111),(1856,111)), '#E4C57545')
    save(im, folder / 'background.png')


def illustrations():
    folder = DEST / 'tsuki_plushies/illustrations'
    folder.mkdir(parents=True, exist_ok=True)
    atlas = Image.open(ROOT / 'tools/assets/memory/plush_atlas.png').convert('RGBA')
    sprites = []
    cat = Image.open(ROOT / 'game/secrets/plushies/kittycat_plush.png').convert('RGBA')
    sprites.append(cat.crop(cat.getbbox()))
    for index in range(14):
        x, y = index % 4, index // 4
        sprite = atlas.crop((x*atlas.width//4, y*atlas.height//4, (x+1)*atlas.width//4, (y+1)*atlas.height//4))
        sprites.append(sprite.crop(sprite.getbbox()))
    for index, sprite in enumerate(sprites, 1):
        sprite.thumbnail((292,354), Image.Resampling.LANCZOS)
        target = Image.new('RGBA', (400,560))
        target.alpha_composite(sprite, ((400-sprite.width)//2, 91+(354-sprite.height)//2))
        target.save(folder / ('plush_{:02d}.png'.format(index)))


if __name__ == '__main__':
    card_textures()
    ui_assets()
    illustrations()
    print('Temporary skin written to', DEST)
