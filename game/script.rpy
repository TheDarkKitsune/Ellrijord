# game/script.rpy

# Intro illustration placeholders (replace these with your real image paths).
default page1 = "gui/intro/page1.png"
default page2 = "gui/intro/page2.png"
default page3 = "gui/intro/page3.png"
default page4 = "gui/intro/page4.png"
default page5 = "gui/intro/page5.png"
default page6 = "gui/intro/page6.png"

# Intro voice placeholders (replace these with your real audio paths).
default audio1 = "audio/intro/audio1.ogg"
default audio2 = "audio/intro/audio2.ogg"
default audio3 = "audio/intro/audio3.ogg"
default audio4 = "audio/intro/audio4.ogg"
default audio5 = "audio/intro/audio5.ogg"
default audio6 = "audio/intro/audio6.ogg"

# Optional title transition music placeholder.
default title_music = "audio/intro/title_transition.ogg"

# Trim transparent borders from intro art (fraction of image size).
# Increase these if the image still shows empty transparent space.
default intro_trim_left = 0.10
default intro_trim_right = 0.10
default intro_trim_top = 0.04
default intro_trim_bottom = 0.04

init python:
    def play_intro_voice(path):
        if path and renpy.loadable(path):
            renpy.music.play(path, channel="voice", loop=False)
        else:
            renpy.music.stop(channel="voice", fadeout=0.2)

    def intro_display(path):
        if (not path) or (not renpy.loadable(path)):
            return Solid("#000")

        w, h = renpy.image_size(path)
        x0 = int(w * intro_trim_left)
        y0 = int(h * intro_trim_top)
        x1 = int(w * (1.0 - intro_trim_right))
        y1 = int(h * (1.0 - intro_trim_bottom))

        cw = max(1, x1 - x0)
        ch = max(1, y1 - y0)

        return Transform(
            LiveCrop((x0, y0, cw, ch), path),
            xysize=(config.screen_width, config.screen_height),
            fit="contain",
            xalign=0.5,
            yalign=0.5
        )

label start:

    window show

    # Page 1: The Golden Age
    scene expression intro_display(page1)
    with dissolve

    $ play_intro_voice(audio1)
    "Once upon a time, beneath the eternal embrace of the World Tree Yggdrasil, there bloomed a realm of pure wonder: Ellrijord."
    "Here, the kemonomimi thrived in harmony. Catfolk leaped through treetops, foxes wove clever tales by firelight, and all bowed to their benevolent ruler, Lady Aurora, whose heart shone brighter than the stars."
    "{i}Fade to shimmering light...{/i}"

    # Page 2: The Shadow Awakens
    scene expression intro_display(page2)
    with dissolve

    $ play_intro_voice(audio2)
    "But one fateful day, a void of pure evil spilled from the cosmos. It was a darkness without form or mercy - a corrupting blight that twisted all it touched."
    "Fields withered to ash. Joy turned to screams. The once-vibrant world began to crumble under its icy grasp."
    "{i}Darkness creeps in...{/i}"

    # Page 3: The Fall of Aurora
    scene expression intro_display(page3)
    with dissolve

    $ play_intro_voice(audio3)
    "Worst of all, the evil claimed Lady Aurora. Her pure soul shattered, reforming into the tyrannical Lady Ender - ruler of the Dark Void."
    "With a heart of endless night, she decreed: Defy her, and perish. Submit, and serve eternally as her thralls. Blood stained the realms, chains bound the free."
    "{i}Screen cracks with void energy...{/i}"

    # Page 4: Flames of Ruin
    scene expression intro_display(page4)
    with dissolve

    $ play_intro_voice(audio4)
    "Ellrijord burned. Millions fell to blade or bondage. Yet in the heart of despair, a flicker of hope endured."
    "A band of brave kemonomimi souls fled through a desperate rift, carrying the last embers of their world's light. They escaped the void's clutches... but to where?"
    "{i}Portal swirls open...{/i}"

    # Page 5: Sanctuary in the Stars
    scene expression intro_display(page5)
    with dissolve

    $ play_intro_voice(audio5)
    "They emerged into Midgard - the realm mortals call Earth."
    "Humans, sensing their plight, opened their hearts and homes. \"You are safe here,\" they vowed. Alliances formed in secrecy, guardians against the shadows that might follow."
    "{i}Lights of the city flicker warmly...{/i}"

    # Page 6: Echoes of Destiny
    scene expression intro_display(page6)
    with dissolve

    $ play_intro_voice(audio6)
    "Which brings us... to now."
    "Whispers of the void stir once more. Lady Ender's gaze turns to Earth. Will you reclaim the light? Or let darkness claim all realms?"
    "{i}Your story begins...{/i}"

    # Title screen transition.
    $ renpy.music.stop(channel="voice", fadeout=0.3)
    if renpy.loadable(title_music):
        play music title_music fadein 1.0

    scene black
    with fade
    centered "{size=68}{b}Ellrijord: Void's Embrace{/b}{/size}\n\n{size=42}Press Start{/size}"

    return
