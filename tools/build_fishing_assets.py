"""Rebuild the original procedural fishing sprites; never edits lake paintings.

Requires Pillow only when rebuilding assets. Runtime has no added dependency.
All figures are drawn at 3x resolution with alpha and antialiased on export.
"""
from pathlib import Path
import math
import random
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "game/images/minigames/fishing"
S = 3
INK = "#253a50"
GOLD = "#e4c575"


def make(size):
    return Image.new("RGBA", (size[0] * S, size[1] * S))


def poly(im, points, fill, outline=INK, width=2):
    d = ImageDraw.Draw(im)
    pts = [(int(x * S), int(y * S)) for x, y in points]
    d.polygon(pts, fill=fill)
    if outline:
        d.line(pts + [pts[0]], fill=outline, width=width * S, joint="curve")


def line(im, points, fill, width=2):
    ImageDraw.Draw(im).line([(int(x*S), int(y*S)) for x, y in points], fill=fill, width=width*S, joint="curve")


def ellipse(im, box, fill, outline=None, width=2):
    ImageDraw.Draw(im).ellipse(tuple(int(v*S) for v in box), fill=fill, outline=outline, width=width*S)


def arc(im, box, start, end, fill, width=2):
    ImageDraw.Draw(im).arc(tuple(int(v*S) for v in box), start, end, fill=fill, width=width*S)


def save(im, folder, name):
    out = DEST / folder / (name + ".png")
    out.parent.mkdir(parents=True, exist_ok=True)
    im.resize((im.width // S, im.height // S), Image.Resampling.LANCZOS).save(out)


def gradient_body(im, box, top, bottom):
    mask = Image.new("L", im.size)
    ImageDraw.Draw(mask).ellipse(tuple(int(v*S) for v in box), fill=255)
    layer = Image.new("RGBA", im.size)
    d = ImageDraw.Draw(layer)
    a, b = tuple(bytes.fromhex(top.lstrip("#"))), tuple(bytes.fromhex(bottom.lstrip("#")))
    for y in range(int(box[1]*S), int(box[3]*S)+1):
        t = (y/S-box[1])/(box[3]-box[1])
        c = tuple(int(x+(z-x)*t) for x,z in zip(a,b)) + (255,)
        d.line([(0,y),(im.width,y)],fill=c)
    im.alpha_composite(Image.composite(layer, Image.new("RGBA",im.size), mask))
    ellipse(im, box, None, INK)


def fish(name, palette, pattern=None):
    top, belly, fin = palette
    im = make((320, 180))
    # Layered fan tail, dorsal and ventral fins with fine rays.
    poly(im, [(91,84),(22,35),(36,91),(20,146),(98,112)], fin)
    for end in [(27,43),(37,70),(32,115),(25,138)]:
        line(im,[(94,99),end],top,1)
    poly(im, [(109,58),(130,18),(157,31),(181,17),(204,58)],fin)
    poly(im, [(136,118),(159,158),(185,133),(216,148),(222,119)],fin)
    gradient_body(im,(77,48,282,135),top,belly)
    for row in range(3):
        for col in range(6):
            x=105+col*20+(row%2)*8
            y=66+row*18
            arc(im,(x,y,x+22,y+19),10,140,top,1)
    if pattern == "koi":
        for box in [(110,54,151,85),(177,90,220,129),(225,57,261,82)]:
            ellipse(im,box,fin)
    if pattern == "moss":
        for x,y in [(112,65),(149,61),(173,70),(128,85),(201,62)]:
            ellipse(im,(x,y,x+12,y+7),"#739268")
    if pattern == "silver":
        line(im,[(98,95),(200,89),(263,93)],"#e1fdff",4)
        for x in range(125,225,20):
            ellipse(im,(x,65,x+4,69),"#395b82")
    if pattern == "crystal":
        for x in (112,153,194):
            poly(im,[(x,60),(x+8,24),(x+23,55)],"#c3f9ff", "#5fa9bd",1)
    if pattern == "moon":
        poly(im,[(90,87),(25,14),(53,76),(39,102),(25,165),(96,113)],"#cbd7ff","#758dc6")
        arc(im,(164,62,206,106),40,290,"#fff5d6",7)
        ellipse(im,(180,66,205,92),top)
    if pattern == "fire":
        for pts in [[(80,85),(12,13),(33,73),(7,87),(48,104)],[(82,106),(6,149),(49,137),(35,173),(111,121)]]:
            poly(im,pts,"#9ff7eb","#3ba5c4")
        for x,y in [(110,71),(155,64),(185,86),(132,111),(215,107)]:
            ellipse(im,(x,y,x+12,y+6),"#ffdb9b")
    poly(im,[(162,95),(195,104),(171,132),(152,112)],fin)
    line(im,[(168,103),(173,122)],belly,1)
    arc(im,(215,67,249,125),95,265,top,2)
    ellipse(im,(244,70,262,91),"#fff7df",INK,1)
    ellipse(im,(252,75,261,87),"#172945")
    ellipse(im,(252,76,255,80),"#ffffff")
    arc(im,(267,97,286,112),85,220,INK,1)
    line(im,[(104,60),(151,56),(183,59)],"#ffffff99",2)
    save(im,"fish",name)
    silhouette=Image.new("RGBA",im.size,"#20253d")
    silhouette.putalpha(im.getchannel("A"))
    save(silhouette,"silhouettes",name)


def leviathan():
    im=make((540,260))
    poly(im,[(179,135),(18,49),(67,127),(13,214),(200,172)],"#5b4f96")
    poly(im,[(187,84),(229,16),(259,57),(313,7),(332,67),(393,31),(405,103)],"#8473b7")
    poly(im,[(223,174),(242,248),(290,204),(339,245),(368,180)],"#655591")
    gradient_body(im,(120,75,491,197),"#46467e","#b7a6d3")
    for x in range(170,407,34):
        arc(im,(x,107,x+35,155),15,155,"#8d80b4",2)
    poly(im,[(393,99),(420,24),(430,89)],"#d9d2ec")
    poly(im,[(436,95),(474,39),(471,111)],"#d9d2ec")
    poly(im,[(301,156),(367,223),(377,166)],"#9483bc")
    ellipse(im,(448,110,473,129),"#b5ffec",INK)
    ellipse(im,(463,112,469,126),"#17474b")
    line(im,[(474,154),(510,151),(519,173),(491,186)],"#dbc6f4",3)
    line(im,[(494,173),(521,189),(527,177)],"#97e9e9",2)
    for x,y in [(160,130),(209,154),(260,120),(328,136),(374,108)]:
        ellipse(im,(x,y,x+6,y+5),"#91f9e6")
    save(im,"fish","void_leviathan")
    sil=Image.new("RGBA",im.size,"#17102d"); sil.putalpha(im.getchannel("A"))
    save(sil,"silhouettes","void_leviathan")


def hazards():
    im=make((160,160))
    poly(im,[(45,19),(107,23),(101,85),(131,107),(145,112),(143,139),(30,141),(29,113),(53,94)],"#886455")
    poly(im,[(45,19),(107,23),(108,44),(44,43)],"#bb9872")
    poly(im,[(28,129),(144,127),(146,144),(27,146)],"#413f49")
    for y in (56,68,80): line(im,[(77,y),(98,y+2)],"#d5bf8d",2)
    ellipse(im,(41,100,57,111),"#5c6c58")
    save(im,"hazards","boot")
    im=make((270,110))
    poly(im,[(15,74),(19,54),(123,43),(174,12),(187,19),(161,43),(248,31),(260,53),(163,66),(112,76),(73,97),(60,86),(79,73)],"#8d765d")
    line(im,[(25,62),(119,55),(187,48),(247,42)],"#c5a582",2)
    line(im,[(122,56),(174,25)],"#604d47",2)
    for x in (50,99,207): arc(im,(x,48,x+22,70),10,260,"#5d5148",2)
    save(im,"hazards","branch")
    im=make((180,140))
    for side in (-1,1):
        for i in range(3):
            line(im,[(90+side*35,85),(90+side*(60+i*5),85+i*10),(90+side*76,115+i*4)],"#bd6d57",6)
        line(im,[(90+side*38,69),(90+side*65,45)],"#cb775c",7)
        ellipse(im,(90+side*65-19,17,90+side*65+19,57),"#e3a276",INK)
        poly(im,[(90+side*65,12),(90+side*65-3,36),(90+side*65+12,19)],"#203c4b",None)
    gradient_body(im,(42,49,138,105),"#c26c55","#edbc86")
    for x in (66,105):
        line(im,[(x,62),(x,40)],"#cb9977",6)
        ellipse(im,(x-8,31,x+7,47),"#fff4da",INK,1)
        ellipse(im,(x-3,34,x+3,43),INK)
    save(im,"hazards","crab")
    im=make((145,210))
    for i in range(5):
        x=30+i*20
        points=[(72,196),(x,152),(x+15,110),(x-9,72),(x+12,15+i*8)]
        line(im,points,"#254f55",13)
        line(im,points,"#79a58a",7)
    save(im,"hazards","weeds")
    im=make((300,120))
    poly(im,[(88,53),(20,17),(38,65),(17,104),(91,83)],"#737b67")
    poly(im,[(120,43),(156,9),(182,44)],"#8e9b73")
    poly(im,[(78,48),(200,36),(281,54),(284,68),(236,78),(198,93),(77,85)],"#879677")
    poly(im,[(202,63),(284,62),(268,78),(224,80)],"#3b424a")
    for x in range(224,276,12): poly(im,[(x,65),(x+5,75),(x+8,65)],"#eee5c4",None)
    ellipse(im,(235,44,246,55),"#efcb69",INK,1)
    ellipse(im,(240,46,244,53),INK)
    save(im,"hazards","pike")
    im=make((300,120))
    points=[(15+i*6,61+math.sin(i*.17)*20) for i in range(44)]
    line(im,points,"#253b53",35)
    line(im,points,"#678ba0",26)
    line(im,[(x,y+8) for x,y in points],"#c8d2b1",5)
    ellipse(im,(255,31,292,70),"#658ca0",INK)
    ellipse(im,(276,40,285,49),"#fce58c")
    for x in (63,139,211): poly(im,[(x,31),(x+9,43),(x+4,55),(x+20,41)],"#ffef91",None)
    save(im,"hazards","eel")
    im=make((140,175))
    glow=make((140,175)); ellipse(glow,(13,22,128,143),"#956bff66")
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(14*S)))
    poly(im,[(70,13),(102,47),(116,92),(97,125),(82,151),(72,125),(49,153),(48,127),(28,104),(25,78),(45,45)],"#8b7dbd","#c4b2f2")
    poly(im,[(72,41),(91,73),(92,104),(72,120),(49,102),(47,75)],"#c3c9ee",None)
    ellipse(im,(53,77,65,86),"#29234f"); ellipse(im,(80,77,92,86),"#29234f")
    save(im,"hazards","wisp")


def gear_and_effects():
    im=make((300,150))
    points=[(9,140),(64,101),(124,66),(181,39),(240,22),(293,20)]
    line(im,points,"#352e3f",9); line(im,points,"#cf9a68",5)
    line(im,[(8,141),(57,108)],"#6c4547",12)
    for x,y in points[1:]: ellipse(im,(x-4,y-2,x+4,y+9),"#d5ccad",INK,1)
    ellipse(im,(47,111,72,136),"#cbb777",INK,2)
    ellipse(im,(53,117,66,130),"#5a5360")
    save(im,"gear","rod")
    im=make((40,58))
    arc(im,(6,22,33,52),0,188,"#233e53",6)
    arc(im,(6,22,33,52),0,188,"#d6ebe4",3)
    line(im,[(32,35),(32,5)],"#d6ebe4",3)
    poly(im,[(6,38),(9,26),(15,35)],"#d6ebe4",None)
    ellipse(im,(27,1,37,11),None,"#e5efdf",2)
    save(im,"gear","hook")
    im=make((64,70))
    ellipse(im,(7,14,58,64),"#d1ab6f",INK)
    poly(im,[(17,19),(14,8),(31,15),(47,7),(45,20)],"#ded6a4")
    line(im,[(18,23),(47,23)],"#8d7355",3)
    arc(im,(19,31,43,52),5,330,"#e89489",5)
    save(im,"gear","bait")
    im=make((40,40)); ellipse(im,(4,4,35,35),"#baf6ee10","#c5fff47c",1)
    arc(im,(9,8,30,29),190,260,"#e8ffffd0",2); save(im,"effects","bubble")
    im=make((70,70)); poly(im,[(35,3),(42,27),(67,35),(42,42),(35,67),(27,43),(3,35),(27,27)],"#f6e2a4",None)
    save(im,"effects","spark")
    im=make((150,100))
    for x,y,r in [(20,47,7),(49,16,5),(113,25,6),(132,62,5),(82,7,4)]: ellipse(im,(x-r,y-r,x+r,y+r),"#dcfff1aa")
    arc(im,(27,42,124,90),180,360,"#d6fff1cc",4)
    arc(im,(15,55,137,98),185,355,"#92e8e5aa",2)
    save(im,"effects","catch")


def panels():
    for name,size in [("hud",(900,112)),("notice",(800,65))]:
        im=make(size);d=ImageDraw.Draw(im)
        box=(2*S,2*S,(size[0]-2)*S,(size[1]-2)*S)
        d.rounded_rectangle(box,24*S,fill="#251f36ed",outline=GOLD,width=2*S)
        d.rounded_rectangle((8*S,8*S,(size[0]-8)*S,(size[1]-8)*S),19*S,outline="#78617b",width=S)
        save(im,"ui",name)
    im=make((240,200))
    poly(im,[(27,29),(115,20),(215,38),(211,169),(120,159),(27,174)],"#513d66")
    poly(im,[(38,37),(119,29),(120,151),(37,162)],"#f4e4c1")
    poly(im,[(121,30),(204,46),(200,158),(121,151)],"#e7d4ac")
    line(im,[(120,30),(120,152)],"#b69a72",2)
    ellipse(im,(57,59,99,106),"#69a7a0",INK,1)
    poly(im,[(60,78),(45,64),(47,96),(65,89)],"#69a7a0")
    ellipse(im,(87,73,92,78),INK)
    for y in (117,129,141): line(im,[(51,y),(106,y-4)],"#bba37e",2)
    for y in (66,84,102,120,138): line(im,[(136,y),(185,y+7)],"#bba37e",2)
    poly(im,[(169,36),(184,39),(182,94),(174,86),(166,91)],"#b7778f")
    save(im,"ui","journal")


def main():
    for name,palette,pattern in [
        ("goldenfin",("#db923f","#fff1ac","#efbf65"),None),
        ("silverstream_trout",("#6689ad","#e6f3ee","#8c9fb7"),"silver"),
        ("mossback_carp",("#557a67","#d8d8a8","#8da27a"),"moss"),
        ("sunset_koi",("#e3b095","#ffedce","#c96c72"),"koi"),
        ("crystal_perch",("#6aafbc","#e1fafa","#b9e2ec"),"crystal"),
        ("moonfin",("#8a97cb","#f1ebff","#c3c7e8"),"moon"),
        ("foxfire_koi",("#416e98","#b0dbdf","#6dcece"),"fire"),
    ]: fish(name,palette,pattern)
    leviathan(); hazards(); gear_and_effects(); panels()
    # Existing inventory API resolves species IDs to these standard icon paths.
    icons=ROOT/"game/gui/inventory_system/icons"
    for path in (DEST/"fish").glob("*.png"):
        out=icons/path.name
        if not out.exists():
            with Image.open(path) as image:
                icon=Image.new("RGBA",(128,128)); image.thumbnail((122,110),Image.Resampling.LANCZOS)
                icon.alpha_composite(image,((128-image.width)//2,(128-image.height)//2));icon.save(out)
    print("Fishing sprites, silhouettes, gear, effects and panels built.")


if __name__ == "__main__": main()
