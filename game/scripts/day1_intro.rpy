# day1_intro.rpy
# Ellrijord: Tales of Light and Void
# Day 1 - Bedroom, Breakfast, School, Evening, Day 2 Handoff
# Continuity: Hana and older survivors remember Ellrijord firsthand. The
# protagonist was very young when the family left; Tsuki was born in Midgard.
# The protagonist starts at 17, approaching 18; Tsuki is 15, turning 16 later.
# The family reached Midgard about 15.5 years ago, when the protagonist was
# roughly 2.5. Tsuki was born shortly afterwards. Exact birthdays remain open.
# Akari's early impressions can resemble childhood memories. Her first dream
# hints at another viewpoint; the source and limits of this ability stay
# unrevealed, and Hana does not identify it as a power in these scenes.

default ell_day = 1
default ell_time_of_day = "morning"
default bedroom_clothes_taken = False
default day1_uniform_added_to_inventory = False
default day1_breakfast_topics_seen = set()
default day1_plushie_system_introduced = False
default day1_lunch_companion = None
default day1_class_focus = None
default day1_akari_glimpse_seen = False
default day1_akari_hana_talk_seen = False
default day1_akari_dream_seen = False
default persistent.picture_frames_found = set()
default persistent.plushies_found = set()
default persistent.first_plush_found = False
default persistent.tsuki_first_plush_reaction_seen = False

init -10 python:
    def day1_ensure_characters():
        s = renpy.store
        C = renpy.store.Character

        if not hasattr(s, "narrator"):
            s.narrator = C(None)
        if not hasattr(s, "mc"):
            s.mc = C("[mc_first_name]")

        if not hasattr(s, "tsuki_unknown"):
            s.tsuki_unknown = C("???", color="#d8c4ff")
        if not hasattr(s, "tsuki"):
            s.tsuki = C("Tsuki", color="#d8c4ff")
        if not hasattr(s, "hana"):
            s.hana = C("Hana", color="#f4b6c2")

        if not hasattr(s, "aria"):
            s.aria = C("Aria", color="#d8c4ff")
        if not hasattr(s, "poko"):
            s.poko = C("Poko", color="#ff9a76")
        if not hasattr(s, "mimi"):
            s.mimi = C("Mimi", color="#ffd6f1")

        if not hasattr(s, "kuroe"):
            s.kuroe = C("Kuroe", color="#6c6cff")
        if not hasattr(s, "sakura"):
            s.sakura = C("Sakura", color="#ffb7d5")
        if not hasattr(s, "rika"):
            s.rika = C("Rika", color="#c88cff")

        if not hasattr(s, "ell_teacher"):
            s.ell_teacher = C("Teacher", color="#c7b7d9")

    def day1_unlock_picture_frame(frame_id, gallery_image_path):
        found = getattr(persistent, "picture_frames_found", set())
        try:
            found = set(found)
        except Exception:
            found = set()

        if frame_id in found:
            return False

        found.add(frame_id)
        persistent.picture_frames_found = found
        persistent.secret_unlocked = True

        if "ell_accept_quest" in globals():
            ell_accept_quest("picture_frames_25")
        if "ell_sync_collectible_quests" in globals():
            ell_sync_collectible_quests()

        if "unlock_gallery_image" in globals():
            unlock_gallery_image(gallery_image_path)

        if "picture_frame_hunter_25" in globals():
            try:
                picture_frame_hunter_25.add_set_progress(frame_id)
            except Exception:
                pass

        renpy.save_persistent()
        return True

    def day1_unlock_plushie(plushie_id, gallery_image_path=None):
        found = getattr(persistent, "plushies_found", set())
        try:
            found = set(found)
        except Exception:
            found = set()

        if plushie_id in found:
            return False

        found.add(plushie_id)
        persistent.plushies_found = found
        persistent.secret_unlocked = True

        if "ell_sync_collectible_quests" in globals():
            ell_sync_collectible_quests()

        if len(found) == 1:
            persistent.first_plush_found = True

        if gallery_image_path and "unlock_gallery_image" in globals():
            unlock_gallery_image(gallery_image_path)

        renpy.save_persistent()
        return True

    def day1_show_ui_popup(title, subtitle="", body=""):
        renpy.call_screen("day1_game_ui_popup", title=title, subtitle=subtitle, body=body)


label day1_opening:
    $ day1_ensure_characters()
    $ ell_day = 1
    $ ell_time_of_day = "morning"
    $ bedroom_clothes_taken = False
    $ day1_breakfast_topics_seen = set()
    $ day1_plushie_system_introduced = False
    $ day1_lunch_companion = None
    $ day1_class_focus = None
    $ day1_akari_glimpse_seen = False
    $ day1_akari_hana_talk_seen = False
    $ day1_akari_dream_seen = False

    stop music fadeout 1.0
    scene black with fade

    $ _day1_music = None
    if renpy.loadable("audio/bgm/morning_theme.ogg"):
        $ _day1_music = "audio/bgm/morning_theme.ogg"
    elif renpy.loadable("audio/converted/Cherry Blossom.wav"):
        $ _day1_music = "audio/converted/Cherry Blossom.wav"
    if _day1_music:
        play music _day1_music fadein 2.0

    tsuki_unknown "Wake up already!"
    tsuki_unknown "Come on, [mc_first_name]! You're going to be late for school if you don't get up!"
    tsuki_unknown "Mom said if you miss the first day, she's blaming me too, so move!"

    narrator "A familiar voice cuts through the warmth of sleep."

    if mc_gender == "male":
        mc "Tsk... five more minutes..."
    else:
        mc "Mmgh... just five more minutes..."

    tsuki_unknown "Nope."
    tsuki_unknown "Absolutely not."
    tsuki_unknown "You said that yesterday, and the day before that."

    narrator "The mattress dips slightly."

    if renpy.loadable("scenes/wakeup.png"):
        scene expression "scenes/wakeup.png" with dissolve
    elif renpy.has_image("wakeup"):
        scene wakeup with dissolve
    elif renpy.has_image("bedroom_morning"):
        scene bedroom_morning with dissolve
    elif renpy.has_image("bg morning_city"):
        scene bg morning_city with dissolve
    elif renpy.loadable("gui/menu/mainmenu_bg.png"):
        scene expression im.Scale("gui/menu/mainmenu_bg.png", config.screen_width, config.screen_height) with dissolve
    else:
        scene black with dissolve

    narrator "By the time I force my eyes open, Tsuki is already standing over me with the sort of smug expression only a younger sister can perfect."

    if renpy.loadable("scenes/arms_crossed.png"):
        scene expression "scenes/arms_crossed.png" with dissolve
    elif renpy.has_image("arms_crossed"):
        scene arms_crossed with dissolve

    if mc_gender == "male":
        narrator "Tsuki folds her arms, tail flicking with impatient energy."
    else:
        narrator "Tsuki folds her arms, trying and failing to hide how pleased she is with herself."

    tsuki "Finally."
    if renpy.loadable("scenes/arms_crossed_after.png"):
        scene expression "scenes/arms_crossed_after.png" with dissolve
    elif renpy.has_image("arms_crossed_after"):
        scene arms_crossed_after with dissolve
    tsuki "Good morning, sleepyhead."
    tsuki "Your clothes are on the dresser."
    tsuki "Get dressed, then come out. Breakfast is ready."
    tsuki "And hurry. First day is a bad time to make an entrance as the late one."

    if mc_gender == "male":
        mc "You say that like you didn't come in here just to bully me awake."
    else:
        mc "You sound way too happy about this."

    tsuki "Because I am."
    tsuki "Anyway, get moving."

    if renpy.loadable("scenes/turnaround.png"):
        scene expression "scenes/turnaround.png" with dissolve
    elif renpy.has_image("turnaround"):
        scene turnaround with dissolve

    narrator "She turns toward the door, then pauses."

    tsuki "Oh, and don't just lay there staring into space."
    if renpy.loadable("scenes/moving.png"):
        scene expression "scenes/moving.png" with dissolve
    elif renpy.has_image("moving"):
        scene moving with dissolve
    tsuki "Grab the clothes first."

    hide tsuki with dissolve

    if renpy.loadable("scenes/doorway.png"):
        scene expression "scenes/doorway.png" with dissolve
    elif renpy.has_image("doorway"):
        scene doorway with dissolve

    $ renpy.pause(0.4)

    if renpy.loadable("scenes/tsukigone.png"):
        scene expression "scenes/tsukigone.png" with dissolve
    elif renpy.has_image("tsukigone"):
        scene tsukigone with dissolve

    narrator "The room settles into a quiet morning stillness."

    jump day1_bedroom_pnc


label day1_bedroom_pnc:
    $ renpy.choice_for_skipping()
    if renpy.is_skipping():
        $ renpy.stop_skipping()
    call screen bedroom_day1_screen
    return


screen bedroom_day1_screen():
    tag room
    modal True
    on "show" action Function(renpy.stop_skipping)

    $ _is_komic = pref_uses_komic_ui()
    $ _bedroom_map = (
        "gui/maps/collectibles_gone.png"
        if (bedroom_clothes_taken and "cat_plush_1" in set(getattr(persistent, "plushies_found", set())) and renpy.loadable("gui/maps/collectibles_gone.png"))
        else ("gui/maps/bedroom2.png" if bedroom_clothes_taken else "gui/maps/bedroom1.png")
    )
    $ _has_bedroom_map = renpy.loadable(_bedroom_map)
    $ _cat_plush_found = "cat_plush_1" in set(getattr(persistent, "plushies_found", set()))
    $ _room_button_width = 600 if _is_komic else 760
    $ _room_button_height = 64 if _is_komic else 48
    $ _room_button_text_size = 24 if _is_komic else 33
    $ _room_button_idle = (
        Transform(pref_choice_button_asset(), size=(_room_button_width, _room_button_height))
        if _is_komic else
        Transform(Frame("gui/clean_ui/gui/button/choice_idle_background.png", 35, 35), xsize=_room_button_width, ysize=_room_button_height)
    )
    $ _room_button_hover = (
        Transform(pref_choice_button_asset(True), size=(_room_button_width, _room_button_height))
        if _is_komic else
        Transform(Frame("gui/clean_ui/gui/button/choice_hover_background.png", 35, 35), xsize=_room_button_width, ysize=_room_button_height)
    )
    $ _room_button_text_color = pref_dialogue_text_color() if _is_komic else "#f0f0f0"
    $ _room_button_text_hover = pref_dialogue_text_color() if _is_komic else "#ffffff"
    $ _room_panel_bg = Solid("#00000044") if _is_komic else Solid("#00000088")

    if _has_bedroom_map:
        add _bedroom_map

        imagemap:
            ground _bedroom_map
            hover _bedroom_map

            hotspot (520, 360, 260, 240) action [Function(renpy.stop_skipping), Jump("day1_dresser")]
            hotspot (0, 240, 240, 500) action [Function(renpy.stop_skipping), Jump("day1_bedroom_door")]
            hotspot (1250, 300, 420, 420) action [Function(renpy.stop_skipping), Jump("day1_bed")]
            hotspot (260, 760, 360, 220) action [Function(renpy.stop_skipping), Jump("day1_desk")]
            hotspot (1570, 360, 90, 120) action [Function(renpy.stop_skipping), Jump("day1_secret_picture1")]

            if day1_plushie_system_introduced and bedroom_clothes_taken and not _cat_plush_found:
                hotspot (860, 400, 70, 180) action [Function(renpy.stop_skipping), Jump("day1_secret_plushie1")]

        vbox:
            xalign 0.5
            yalign 0.6
            xsize _room_button_width
            spacing 6

            textbutton "Dresser":
                action [Function(renpy.stop_skipping), Jump("day1_dresser")]
                xfill True
                ysize _room_button_height
                background _room_button_idle
                hover_background _room_button_hover
                text_size _room_button_text_size
                text_color _room_button_text_color
                text_hover_color _room_button_text_hover
                text_xalign 0.5

            textbutton "Door":
                action [Function(renpy.stop_skipping), Jump("day1_bedroom_door")]
                xfill True
                ysize _room_button_height
                background _room_button_idle
                hover_background _room_button_hover
                text_size _room_button_text_size
                text_color _room_button_text_color
                text_hover_color _room_button_text_hover
                text_xalign 0.5

            textbutton "Bed":
                action [Function(renpy.stop_skipping), Jump("day1_bed")]
                xfill True
                ysize _room_button_height
                background _room_button_idle
                hover_background _room_button_hover
                text_size _room_button_text_size
                text_color _room_button_text_color
                text_hover_color _room_button_text_hover
                text_xalign 0.5

            textbutton "Desk":
                action [Function(renpy.stop_skipping), Jump("day1_desk")]
                xfill True
                ysize _room_button_height
                background _room_button_idle
                hover_background _room_button_hover
                text_size _room_button_text_size
                text_color _room_button_text_color
                text_hover_color _room_button_text_hover
                text_xalign 0.5

    elif renpy.has_image("bedroom_morning"):
        add "bedroom_morning"

        imagemap:
            ground "bedroom_morning"
            hover "bedroom_morning"

            hotspot (520, 360, 260, 240) action [Function(renpy.stop_skipping), Jump("day1_dresser")]
            hotspot (0, 240, 240, 500) action [Function(renpy.stop_skipping), Jump("day1_bedroom_door")]
            hotspot (1250, 300, 420, 420) action [Function(renpy.stop_skipping), Jump("day1_bed")]
            hotspot (260, 760, 360, 220) action [Function(renpy.stop_skipping), Jump("day1_desk")]
            hotspot (1570, 360, 90, 120) action [Function(renpy.stop_skipping), Jump("day1_secret_picture1")]

            if day1_plushie_system_introduced and bedroom_clothes_taken and not _cat_plush_found:
                hotspot (860, 400, 70, 180) action [Function(renpy.stop_skipping), Jump("day1_secret_plushie1")]
    else:
        if renpy.loadable("gui/menu/mainmenu_bg.png"):
            add im.Scale("gui/menu/mainmenu_bg.png", config.screen_width, config.screen_height)
        else:
            add Solid("#101018")

        frame:
            xalign 0.5
            yalign 0.5
            xpadding 30
            ypadding 30
            background _room_panel_bg

            vbox:
                spacing 12
                text "Bedroom Actions"
                textbutton "Dresser":
                    action [Function(renpy.stop_skipping), Jump("day1_dresser")]
                    xsize _room_button_width
                    ysize _room_button_height
                    background _room_button_idle
                    hover_background _room_button_hover
                    text_size _room_button_text_size
                    text_color _room_button_text_color
                    text_hover_color _room_button_text_hover
                    text_xalign 0.5
                textbutton "Door":
                    action [Function(renpy.stop_skipping), Jump("day1_bedroom_door")]
                    xsize _room_button_width
                    ysize _room_button_height
                    background _room_button_idle
                    hover_background _room_button_hover
                    text_size _room_button_text_size
                    text_color _room_button_text_color
                    text_hover_color _room_button_text_hover
                    text_xalign 0.5
                textbutton "Bed":
                    action [Function(renpy.stop_skipping), Jump("day1_bed")]
                    xsize _room_button_width
                    ysize _room_button_height
                    background _room_button_idle
                    hover_background _room_button_hover
                    text_size _room_button_text_size
                    text_color _room_button_text_color
                    text_hover_color _room_button_text_hover
                    text_xalign 0.5
                textbutton "Desk":
                    action [Function(renpy.stop_skipping), Jump("day1_desk")]
                    xsize _room_button_width
                    ysize _room_button_height
                    background _room_button_idle
                    hover_background _room_button_hover
                    text_size _room_button_text_size
                    text_color _room_button_text_color
                    text_hover_color _room_button_text_hover
                    text_xalign 0.5


screen day1_secret_discovered_popup(image_path, message="You've discovered a secret."):
    modal True
    zorder 300
    key "dismiss" action Return()
    key "game_menu" action Return()

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 18

        if image_path and renpy.loadable(image_path):
            add Transform(image_path, fit="contain", xalign=0.5, yalign=0.5, xsize=760, ysize=760)

        text "[message]":
            xalign 0.5
            size 52
            color "#f8f8f8"
            outlines [(2, "#000000cc", 0, 0)]

        textbutton "Continue":
            xalign 0.5
            background None
            hover_background None
            text_size 44
            text_color "#f8f8f8"
            text_outlines [(2, "#000000cc", 0, 0)]
            action Return()


screen day1_game_ui_popup(title, subtitle="", body=""):
    modal True
    zorder 350

    add Solid("#00000088")

    fixed:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 375

        if renpy.loadable("gui/clean_ui/gui/quests.png"):
            add Transform("gui/clean_ui/gui/quests.png", xsize=900, ysize=375)
        else:
            add Solid("#111111ee") xsize 900 ysize 375

        vbox:
            xalign 0.5
            ypos 40
            xsize 640
            spacing 16

            text "[title]":
                xalign 0.5
                text_align 0.5
                size 26
                color "#ddd3c4"
                kerning 2
                outlines [(1, "#000000aa", 0, 0)]

            if subtitle:
                text "[subtitle]":
                    xalign 0.5
                    text_align 0.5
                    size 40
                    color "#f7f2eb"
                    outlines [(2, "#000000bb", 0, 0)]
            else:
                text "[title]":
                    xalign 0.5
                    text_align 0.5
                    size 40
                    color "#f7f2eb"
                    outlines [(2, "#000000bb", 0, 0)]

        if body:
            text "[body]":
                xalign 0.5
                ypos 156
                xsize 560
                text_align 0.5
                font "DejaVuSans.ttf"
                size 23
                line_spacing 8
                color "#ddd7d0"
                outlines [(1, "#00000088", 0, 0)]

        textbutton "Continue":
            xalign 0.5
            ypos 305
            xsize 270
            ysize 54
            background Transform(Frame("gui/clean_ui/gui/button/choice_idle_background.png", 35, 35), xsize=270, ysize=54)
            hover_background Transform(Frame("gui/clean_ui/gui/button/choice_hover_background.png", 35, 35), xsize=270, ysize=54)
            insensitive_background Transform(Frame("gui/clean_ui/gui/button/choice_idle_background.png", 35, 35), xsize=270, ysize=54)
            text_size 26
            text_color "#f0f0f0"
            text_hover_color "#ffffff"
            text_xalign 0.5
            text_yalign 0.5
            action Return()


label day1_dresser:
    if renpy.loadable("scenes/dresser.png"):
        scene expression "scenes/dresser.png"
    elif renpy.loadable("gui/maps/dresser.png"):
        scene expression "gui/maps/dresser.png"
    elif renpy.has_image("dresser"):
        scene dresser

    if not bedroom_clothes_taken:
        narrator "A neat pile of clothes sits on the dresser."
        narrator "Tsuki wasn't kidding. She really did set everything out for me."

        menu:
            "Take the clothes":
                $ bedroom_clothes_taken = True
                if "inventory" in globals() and not day1_uniform_added_to_inventory:
                    $ inventory.add_item("uniform_top", notify=False)
                    $ inventory.add_item("uniform_skirt", notify=False)
                    $ inventory.add_item("uniform_shoes", notify=False)
                    if "pm_notify" in globals():
                        $ pm_notify("Added School Uniform.", sound_type="success")
                    $ day1_uniform_added_to_inventory = True
                if renpy.loadable("scenes/pickup.png"):
                    scene expression "scenes/pickup.png"
                elif renpy.loadable("gui/maps/pickup.png"):
                    scene expression "gui/maps/pickup.png"
                elif renpy.has_image("pickup"):
                    scene pickup
                narrator "I pick up the folded clothes."
                $ renpy.pause(0.6)
                if renpy.loadable("scenes/pickedup.png"):
                    scene expression "scenes/pickedup.png"
                elif renpy.loadable("gui/maps/pickedup.png"):
                    scene expression "gui/maps/pickedup.png"
                elif renpy.has_image("pickedup"):
                    scene pickedup
                narrator "Might as well get changed before she comes back to drag me out herself."

                if mc_gender == "male":
                    narrator "Uniform, undershirt, everything I need for the day."
                else:
                    narrator "Uniform, ribbon, everything set out properly and annoyingly neatly."

                if renpy.loadable("scenes/dresser2.png"):
                    scene expression "scenes/dresser2.png"
                elif renpy.loadable("gui/maps/dresser2.png"):
                    scene expression "gui/maps/dresser2.png"
                elif renpy.has_image("dresser2"):
                    scene dresser2
                narrator "At least someone in this house has their life together."
                jump day1_changed

            "Leave them there":
                narrator "Yeah... no."
                narrator "I'm not getting out of this room in pajamas."
                jump day1_bedroom_pnc
    else:
        if renpy.loadable("scenes/dresser2.png"):
            scene expression "scenes/dresser2.png"
        elif renpy.loadable("gui/maps/dresser2.png"):
            scene expression "gui/maps/dresser2.png"
        elif renpy.has_image("dresser2"):
            scene dresser2
        narrator "The dresser is clear now."
        narrator "No more excuses."
        jump day1_bedroom_pnc


label day1_changed:
    scene black
    if renpy.loadable("scenes/dressed.png"):
        scene expression "scenes/dressed.png"
    elif renpy.loadable("gui/maps/dressed.png"):
        scene expression "gui/maps/dressed.png"
    elif renpy.has_image("dressed"):
        scene dressed
    narrator "A few minutes later, I'm dressed and a little more awake."
    narrator "The uniform still feels strange after the break."
    narrator "But today starts whether I'm ready or not."

    jump day1_bedroom_pnc


label day1_bedroom_door:
    if not bedroom_clothes_taken:
        if renpy.loadable("scenes/onsiedoor.png"):
            scene expression "scenes/onsiedoor.png"
        elif renpy.loadable("gui/maps/onesiedoor.png"):
            scene expression "gui/maps/onesiedoor.png"
        elif renpy.has_image("onsiedoor"):
            scene onsiedoor
        narrator "I should probably get dressed first."
        narrator "Tsuki would never let me hear the end of it if I walked out like this."
        jump day1_bedroom_pnc
    else:
        if renpy.loadable("scenes/uniformdoor.png"):
            scene expression "scenes/uniformdoor.png"
        elif renpy.loadable("gui/maps/uniformdoor.png"):
            scene expression "gui/maps/uniformdoor.png"
        elif renpy.has_image("uniformdoor"):
            scene uniformdoor
        narrator "Time to face the rest of the morning."
        scene black with fade
        jump day1_living_room


label day1_bed:
    if renpy.loadable("gui/maps/bed.png"):
        scene expression "gui/maps/bed.png"
    elif renpy.has_image("bed"):
        scene bed

    if not bedroom_clothes_taken:
        narrator "The bed looks far too inviting."
        narrator "Tempting... but if I lie back down, I'm finished."
    else:
        narrator "I've already gotten this far."
        narrator "Going back to bed now would be a tragic misuse of effort."
    jump day1_bedroom_pnc


label day1_desk:
    if renpy.loadable("scenes/desk.png"):
        scene expression "scenes/desk.png"
    elif renpy.loadable("gui/maps/desk.png"):
        scene expression "gui/maps/desk.png"
    elif renpy.has_image("desk"):
        scene desk

    if not bedroom_clothes_taken:
        narrator "My desk."
        narrator "A battlefield of books, notes, and unfinished intentions."
        narrator "No time for that. Clothes first."
    else:
        narrator "No time to sit around this morning."
        narrator "School first. Regret everything later."
    jump day1_bedroom_pnc


label day1_secret_picture1:
    $ _picture1_path = "secrets/Picture Frames/picture1.png"
    $ _already_found = "picture1" in set(getattr(persistent, "picture_frames_found", set()))

    if renpy.loadable("gui/maps/bedroom2.png") and bedroom_clothes_taken:
        scene expression "gui/maps/bedroom2.png"
    elif renpy.loadable("gui/maps/bedroom1.png"):
        scene expression "gui/maps/bedroom1.png"

    if _already_found:
        narrator "It's the same tiny photo frame."
        jump day1_bedroom_pnc

    $ day1_unlock_picture_frame("picture1", _picture1_path)

    call screen day1_secret_discovered_popup(_picture1_path, "You've discovered a secret.")

    jump day1_bedroom_pnc


label day1_secret_plushie1:
    $ _plushie_found = "cat_plush_1" in set(getattr(persistent, "plushies_found", set()))
    $ _plushie_path = "secrets/plushies/kittycat_plush.png"

    if _plushie_found:
        jump day1_bedroom_pnc

    if not day1_plushie_system_introduced:
        jump day1_bedroom_pnc

    if renpy.loadable("gui/maps/collectibles_gone.png") and bedroom_clothes_taken:
        scene expression "gui/maps/collectibles_gone.png"
    elif renpy.loadable("gui/maps/bedroom2.png") and bedroom_clothes_taken:
        scene expression "gui/maps/bedroom2.png"
    elif renpy.loadable("gui/maps/bedroom1.png"):
        scene expression "gui/maps/bedroom1.png"

    narrator "Wait..."
    narrator "Is that one of Tsuki's plushies?"
    narrator "A small cat plush is tucked away near the wardrobe."
    narrator "Looks like she wasn't kidding about hiding them everywhere."

    $ day1_unlock_plushie("cat_plush_1", _plushie_path)

    call screen day1_game_ui_popup(
        title="PLUSHIE FOUND",
        subtitle="Tsuki's Cat Plush",
        body="You found one of Tsuki's lost plushies."
    )

    jump day1_bedroom_pnc


label day1_living_room:
    if renpy.loadable("scenes/Hallway.png"):
        scene expression im.Scale("scenes/Hallway.png", config.screen_width, config.screen_height) with dissolve
        pause 1.1

    if renpy.loadable("scenes/Hallway2.png"):
        scene expression im.Scale("scenes/Hallway2.png", config.screen_width, config.screen_height) with dissolve
        pause 1.1

    if renpy.loadable("scenes/Kitchen_open.png"):
        scene expression im.Scale("scenes/Kitchen_open.png", config.screen_width, config.screen_height) with dissolve
        pause 1.1

    narrator "The smell of breakfast reaches me before I even make it fully into the room."

    if renpy.loadable("scenes/hana.png"):
        scene expression im.Scale("scenes/hana.png", config.screen_width, config.screen_height) with dissolve
    elif renpy.has_image("living_room_morning"):
        scene living_room_morning with dissolve
    elif renpy.has_image("bg morning_city"):
        scene bg morning_city with dissolve
    elif renpy.loadable("gui/menu/mainmenu_bg.png"):
        scene expression im.Scale("gui/menu/mainmenu_bg.png", config.screen_width, config.screen_height) with dissolve
    else:
        scene black with dissolve

    if renpy.has_image("hana neutral") and not renpy.loadable("scenes/hana.png"):
        show hana neutral at left
    if renpy.has_image("tsuki happy"):
        show tsuki happy at right

    hana "There you are."
    hana "I was starting to think we'd have to send Tsuki back in with a bucket of cold water."

    if mc_gender == "male":
        mc "That would've been a war crime."
    else:
        if renpy.loadable("scenes/hana2.png"):
            scene expression im.Scale("scenes/hana2.png", config.screen_width, config.screen_height) with dissolve
        mc "I'm pretty sure that counts as child abuse."

    if renpy.loadable("scenes/worth it.png"):
        scene expression im.Scale("scenes/worth it.png", config.screen_width, config.screen_height) with dissolve
    tsuki "Worth it."

    if renpy.loadable("scenes/hana.png"):
        scene expression im.Scale("scenes/hana.png", config.screen_width, config.screen_height) with dissolve
    hana "Now Sit down at the table the pair of you. I'll bring your breakfast over."

    if renpy.loadable("scenes/table.png"):
        scene expression im.Scale("scenes/table.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.35, hard=True)
    if renpy.loadable("scenes/table2.png"):
        scene expression im.Scale("scenes/table2.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.35, hard=True)
    if renpy.loadable("scenes/table3.png"):
        scene expression im.Scale("scenes/table3.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.35, hard=True)
    if renpy.loadable("scenes/table4.png"):
        scene expression im.Scale("scenes/table4.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.35, hard=True)

    if renpy.loadable("scenes/food.png"):
        scene expression im.Scale("scenes/food.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.35, hard=True)
    if renpy.loadable("scenes/food2.png"):
        scene expression im.Scale("scenes/food2.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.35, hard=True)
    if renpy.loadable("scenes/food3.png"):
        scene expression im.Scale("scenes/food3.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.35, hard=True)
    if renpy.loadable("scenes/food4.png"):
        scene expression im.Scale("scenes/food4.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.35, hard=True)
    if renpy.loadable("scenes/food5.png"):
        scene expression im.Scale("scenes/food5.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.35, hard=True)
    if renpy.loadable("scenes/food6.png"):
        scene expression im.Scale("scenes/food6.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.5, hard=True)

    if renpy.loadable("scenes/sit.png"):
        scene expression im.Scale("scenes/sit.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.35, hard=True)
    if renpy.loadable("scenes/sit2.png"):
        scene expression im.Scale("scenes/sit2.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.35, hard=True)
    if renpy.loadable("scenes/sit4.png"):
        scene expression im.Scale("scenes/sit4.png", config.screen_width, config.screen_height) with dissolve

    narrator "Mum brings the food over to us, sets everything down, and then takes her seat beside Tsuki."
    narrator "For one ordinary moment, the morning feels almost too peaceful."

    if renpy.has_image("tsuki happy"):
        hide tsuki
    if renpy.has_image("tsuki neutral"):
        show tsuki neutral at right

    if renpy.loadable("scenes/talk.png"):
        scene expression im.Scale("scenes/talk.png", config.screen_width, config.screen_height) with dissolve
    hana "First day back always feels longer than it is."
    hana "You'll be fine."

    if mc_gender == "male":
        if renpy.loadable("scenes/talk2.png"):
            scene expression im.Scale("scenes/talk2.png", config.screen_width, config.screen_height) with dissolve
        mc "That's easy for you to say."
    else:
        if renpy.loadable("scenes/talk2.png"):
            scene expression im.Scale("scenes/talk2.png", config.screen_width, config.screen_height) with dissolve
        mc "You say that like I don't remember how chaotic this school gets."

    if renpy.loadable("scenes/talk.png"):
        scene expression im.Scale("scenes/talk.png", config.screen_width, config.screen_height) with dissolve
    hana "And yet, you always come back in one piece."
    hana "Usually."

    if renpy.loadable("scenes/talk3.png"):
        scene expression im.Scale("scenes/talk3.png", config.screen_width, config.screen_height) with dissolve
    tsuki "Barely."

    if mc_gender == "male":
        if renpy.loadable("scenes/talk4.png"):
            scene expression im.Scale("scenes/talk4.png", config.screen_width, config.screen_height) with dissolve
        mc "I don't need commentary from the peanut gallery."
    else:
        if renpy.loadable("scenes/talk4.png"):
            scene expression im.Scale("scenes/talk4.png", config.screen_width, config.screen_height) with dissolve
        mc "You're enjoying this far too much."

    if renpy.loadable("scenes/talk5.png"):
        scene expression im.Scale("scenes/talk5.png", config.screen_width, config.screen_height) with dissolve
    tsuki "A little."

    if renpy.loadable("scenes/eat.png"):
        scene expression im.Scale("scenes/eat.png", config.screen_width, config.screen_height) with dissolve
    narrator "The two of us start eating."
    if renpy.loadable("scenes/eating.png"):
        scene expression im.Scale("scenes/eating.png", config.screen_width, config.screen_height) with dissolve
    narrator "Tsuki picks at her breakfast with that half-distracted, half-alert energy she always has in the morning."
    if renpy.loadable("scenes/eating2.png"):
        scene expression im.Scale("scenes/eating2.png", config.screen_width, config.screen_height) with dissolve
    narrator "Mum watches us with the kind of quiet smile that makes the whole room feel warmer."

    if renpy.loadable("scenes/eating3.png"):
        scene expression im.Scale("scenes/eating3.png", config.screen_width, config.screen_height) with dissolve
    narrator "For a few minutes, breakfast takes over the conversation."
    if renpy.loadable("scenes/eating4.png"):
        scene expression im.Scale("scenes/eating4.png", config.screen_width, config.screen_height) with dissolve
    narrator "The clink of cutlery, Hana's soft reminders, and Tsuki's occasional complaints fill the room."

    scene black with fade
    $ renpy.pause(0.6)

    narrator "A little while later..."

    if renpy.loadable("scenes/finish.png"):
        scene expression im.Scale("scenes/finish.png", config.screen_width, config.screen_height) with dissolve
    narrator "Breakfast is finished, and the morning feels a little less rushed."
    if renpy.loadable("scenes/finish2.png"):
        scene expression im.Scale("scenes/finish2.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.9, hard=True)

    if renpy.loadable("scenes/finish.png"):
        scene expression im.Scale("scenes/finish.png", config.screen_width, config.screen_height) with dissolve
        $ renpy.pause(0.7, hard=True)

    if renpy.loadable("scenes/hana_to_mc.png"):
        scene expression im.Scale("scenes/hana_to_mc.png", config.screen_width, config.screen_height) with dissolve
    hana "You'll be seeing Aria, Poko, and Mimi again today, won't you?"

    if mc_gender == "male":
        if renpy.loadable("scenes/mc_to_both.png"):
            scene expression im.Scale("scenes/mc_to_both.png", config.screen_width, config.screen_height) with dissolve
        mc "Yeah."
        mc "The usual trio."
    else:
        if renpy.loadable("scenes/mc_to_both.png"):
            scene expression im.Scale("scenes/mc_to_both.png", config.screen_width, config.screen_height) with dissolve
        mc "Yeah."
        mc "The usual trio."

    if renpy.loadable("scenes/tsuki_to_mc.png"):
        scene expression im.Scale("scenes/tsuki_to_mc.png", config.screen_width, config.screen_height) with dissolve
    tsuki "Poko's the loud one, right?"

    if mc_gender == "male":
        if renpy.loadable("scenes/mc_to_both.png"):
            scene expression im.Scale("scenes/mc_to_both.png", config.screen_width, config.screen_height) with dissolve
        mc "That's one way to describe her."
    else:
        if renpy.loadable("scenes/mc_to_both.png"):
            scene expression im.Scale("scenes/mc_to_both.png", config.screen_width, config.screen_height) with dissolve
        mc "That's one way to describe her."

    if renpy.loadable("scenes/tsuki_to_mc.png"):
        scene expression im.Scale("scenes/tsuki_to_mc.png", config.screen_width, config.screen_height) with dissolve
    tsuki "And Mimi's the pretty one everyone gets nervous around?"

    if renpy.loadable("scenes/hana_to_tsuki.png"):
        scene expression im.Scale("scenes/hana_to_tsuki.png", config.screen_width, config.screen_height) with dissolve
    hana "Tsuki."

    if renpy.loadable("scenes/tsuki_to_hana.png"):
        scene expression im.Scale("scenes/tsuki_to_hana.png", config.screen_width, config.screen_height) with dissolve
    tsuki "What? I'm right."

    if renpy.loadable("scenes/finish.png"):
        scene expression im.Scale("scenes/finish.png", config.screen_width, config.screen_height) with dissolve
    narrator "I can already feel where this is going."

    if renpy.loadable("scenes/hana_to_mc.png"):
        scene expression im.Scale("scenes/hana_to_mc.png", config.screen_width, config.screen_height) with dissolve
    hana "And for Year 2, you'll have Kuroe, Sakura, and Rika around too."

    if mc_gender == "male":
        if renpy.loadable("scenes/mc_to_both.png"):
            scene expression im.Scale("scenes/mc_to_both.png", config.screen_width, config.screen_height) with dissolve
        mc "Rika being there still feels weird."
        mc "Having your younger cousin at school should not feel this threatening."
    else:
        if renpy.loadable("scenes/mc_to_both.png"):
            scene expression im.Scale("scenes/mc_to_both.png", config.screen_width, config.screen_height) with dissolve
        mc "Rika being in the same school now still feels strange."
        mc "She's definitely going to cause trouble."

    if renpy.loadable("scenes/tsuki_to_mc.png"):
        scene expression im.Scale("scenes/tsuki_to_mc.png", config.screen_width, config.screen_height) with dissolve
    tsuki "She's family."
    tsuki "Causing trouble is basically tradition."

    if renpy.loadable("scenes/hana_to_tsuki.png"):
        scene expression im.Scale("scenes/hana_to_tsuki.png", config.screen_width, config.screen_height) with dissolve
    hana "Just make sure you all look after one another."

    if renpy.loadable("scenes/mc_to_both.png"):
        scene expression im.Scale("scenes/mc_to_both.png", config.screen_width, config.screen_height) with dissolve
    narrator "I nod, though with this group, 'normal' is probably already out of reach."

    $ day1_breakfast_topics_seen = set()

    while len(day1_breakfast_topics_seen) < 3:
        menu:
            "Talk about Aria" if "aria" not in day1_breakfast_topics_seen:
                $ day1_breakfast_topics_seen.add("aria")
                mc "Aria's probably going to act like she runs the entire school."
                if renpy.loadable("scenes/tsuki_to_mc.png"):
                    scene expression im.Scale("scenes/tsuki_to_mc.png", config.screen_width, config.screen_height) with dissolve
                tsuki "Doesn't she?"
                if renpy.loadable("scenes/hana_to_tsuki.png"):
                    scene expression im.Scale("scenes/hana_to_tsuki.png", config.screen_width, config.screen_height) with dissolve
                hana "Only in her own head."
                if renpy.loadable("scenes/mc_to_both.png"):
                    scene expression im.Scale("scenes/mc_to_both.png", config.screen_width, config.screen_height) with dissolve
                narrator "Even so, Aria has a way of drawing attention without trying."

            "Talk about Poko" if "poko" not in day1_breakfast_topics_seen:
                $ day1_breakfast_topics_seen.add("poko")
                mc "If Poko's in a good mood, the whole hallway will know in five seconds."
                if renpy.loadable("scenes/tsuki_to_mc.png"):
                    scene expression im.Scale("scenes/tsuki_to_mc.png", config.screen_width, config.screen_height) with dissolve
                tsuki "And if she's in a bad mood?"
                if renpy.loadable("scenes/mc_to_both.png"):
                    scene expression im.Scale("scenes/mc_to_both.png", config.screen_width, config.screen_height) with dissolve
                mc "Then the whole building will know."
                narrator "Loud, fiery, impossible to ignore. That's Poko."

            "Talk about Mimi" if "mimi" not in day1_breakfast_topics_seen:
                $ day1_breakfast_topics_seen.add("mimi")
                mc "Mimi's the dangerous one."
                if renpy.loadable("scenes/tsuki_to_mc.png"):
                    scene expression im.Scale("scenes/tsuki_to_mc.png", config.screen_width, config.screen_height) with dissolve
                tsuki "Dangerous?"
                if renpy.loadable("scenes/mc_to_both.png"):
                    scene expression im.Scale("scenes/mc_to_both.png", config.screen_width, config.screen_height) with dissolve
                mc "The elegant kind."
                if renpy.loadable("scenes/hana_to_mc.png"):
                    scene expression im.Scale("scenes/hana_to_mc.png", config.screen_width, config.screen_height) with dissolve
                hana "Be nice."
                if renpy.loadable("scenes/mc_to_both.png"):
                    scene expression im.Scale("scenes/mc_to_both.png", config.screen_width, config.screen_height) with dissolve
                narrator "Mimi never needs to raise her voice to take control of a conversation."

    if persistent.first_plush_found and not persistent.tsuki_first_plush_reaction_seen:
        tsuki "Wait."
        tsuki "You actually found one already?"

        if mc_gender == "male":
            mc "The cat plush by the wardrobe?"
        else:
            mc "The little cat plush hidden near the wardrobe?"

        tsuki "Yeah!"
        tsuki "That's one of mine!"
        tsuki "I thought that one was gone forever..."

        hana "So she really had hidden them all over the place."

        tsuki "I told you!"

        narrator "Tsuki smiles in that bright, unguarded way she only shows when something genuinely matters to her."

        tsuki "Keep looking, okay?"
        tsuki "There should still be more of them out there."

        $ persistent.tsuki_first_plush_reaction_seen = True
        $ renpy.save_persistent()

    if not day1_plushie_system_introduced:
        if renpy.loadable("scenes/plush_quest/quest.png"):
            scene expression im.Scale("scenes/plush_quest/quest.png", config.screen_width, config.screen_height) with dissolve
        tsuki "Oh! Wait."
        if renpy.loadable("scenes/plush_quest/quest2.png"):
            scene expression im.Scale("scenes/plush_quest/quest2.png", config.screen_width, config.screen_height) with dissolve
        tsuki "I almost forgot."

        if mc_gender == "male":
            if renpy.loadable("scenes/plush_quest/quest3.png"):
                scene expression im.Scale("scenes/plush_quest/quest3.png", config.screen_width, config.screen_height) with dissolve
            mc "That already sounds dangerous."
        else:
            if renpy.loadable("scenes/plush_quest/quest3.png"):
                scene expression im.Scale("scenes/plush_quest/quest3.png", config.screen_width, config.screen_height) with dissolve
            mc "That already sounds like trouble."

        if renpy.loadable("scenes/plush_quest/quest2.png"):
            scene expression im.Scale("scenes/plush_quest/quest2.png", config.screen_width, config.screen_height) with dissolve
        tsuki "It's not dangerous."
        if renpy.loadable("scenes/plush_quest/quest2.png"):
            scene expression im.Scale("scenes/plush_quest/quest2.png", config.screen_width, config.screen_height) with dissolve
        tsuki "It's important."

        if renpy.loadable("scenes/plush_quest/quest4.png"):
            scene expression im.Scale("scenes/plush_quest/quest4.png", config.screen_width, config.screen_height) with dissolve
        hana "That usually means it's dangerous."

        if renpy.loadable("scenes/plush_quest/quest5.png"):
            scene expression im.Scale("scenes/plush_quest/quest5.png", config.screen_width, config.screen_height) with dissolve
        tsuki "Mum!"

        if renpy.loadable("scenes/plush_quest/quest6.png"):
            scene expression im.Scale("scenes/plush_quest/quest6.png", config.screen_width, config.screen_height) with dissolve
        narrator "Tsuki suddenly leans forward across the table."

        if renpy.loadable("scenes/plush_quest/quest7.png"):
            scene expression im.Scale("scenes/plush_quest/quest7.png", config.screen_width, config.screen_height) with dissolve
        tsuki "You haven't seen any of my plushies around the house, have you?"

        if renpy.loadable("scenes/plush_quest/quest8.png"):
            scene expression im.Scale("scenes/plush_quest/quest8.png", config.screen_width, config.screen_height) with dissolve
        mc "Your plushies?"

        if renpy.loadable("scenes/plush_quest/quest7.png"):
            scene expression im.Scale("scenes/plush_quest/quest7.png", config.screen_width, config.screen_height) with dissolve
        tsuki "Yeah."
        tsuki "The little cat ones."
        tsuki "And the fox one."
        tsuki "And the moon one."
        tsuki "And the-"

        if renpy.loadable("scenes/plush_quest/quest8.png"):
            scene expression im.Scale("scenes/plush_quest/quest8.png", config.screen_width, config.screen_height) with dissolve
        mc "How many plushies did you lose?"

        if renpy.loadable("scenes/plush_quest/quest7.png"):
            scene expression im.Scale("scenes/plush_quest/quest7.png", config.screen_width, config.screen_height) with dissolve
        tsuki "I didn't lose them!"
        tsuki "They just... relocated."

        if renpy.loadable("scenes/plush_quest/quest9.png"):
            scene expression im.Scale("scenes/plush_quest/quest9.png", config.screen_width, config.screen_height) with dissolve
        hana "Somehow into places no one can reach."

        if renpy.loadable("scenes/plush_quest/quest7.png"):
            scene expression im.Scale("scenes/plush_quest/quest7.png", config.screen_width, config.screen_height) with dissolve
        tsuki "Exactly."

        if renpy.loadable("scenes/plush_quest/quest10.png"):
            scene expression im.Scale("scenes/plush_quest/quest10.png", config.screen_width, config.screen_height) with dissolve
        narrator "Tsuki puffs her cheeks in protest."

        if renpy.loadable("scenes/plush_quest/quest7.png"):
            scene expression im.Scale("scenes/plush_quest/quest7.png", config.screen_width, config.screen_height) with dissolve
        tsuki "I hid them around the house a while ago."
        tsuki "But now I can't remember where half of them are."

        if mc_gender == "male":
            if renpy.loadable("scenes/plush_quest/quest8.png"):
                scene expression im.Scale("scenes/plush_quest/quest8.png", config.screen_width, config.screen_height) with dissolve
            mc "So you're asking me to go plushie hunting."
        else:
            if renpy.loadable("scenes/plush_quest/quest8.png"):
                scene expression im.Scale("scenes/plush_quest/quest8.png", config.screen_width, config.screen_height) with dissolve
            mc "So I'm being recruited as your plushie detective."

        if renpy.loadable("scenes/plush_quest/quest11.png"):
            scene expression im.Scale("scenes/plush_quest/quest11.png", config.screen_width, config.screen_height) with dissolve
        tsuki "Yes."

        if mc_gender == "male":
            if renpy.loadable("scenes/plush_quest/quest8.png"):
                scene expression im.Scale("scenes/plush_quest/quest8.png", config.screen_width, config.screen_height) with dissolve
            mc "Why me?"
        else:
            if renpy.loadable("scenes/plush_quest/quest8.png"):
                scene expression im.Scale("scenes/plush_quest/quest8.png", config.screen_width, config.screen_height) with dissolve
            mc "And why exactly me?"

        if renpy.loadable("scenes/plush_quest/quest7.png"):
            scene expression im.Scale("scenes/plush_quest/quest7.png", config.screen_width, config.screen_height) with dissolve
        tsuki "Because you leave your room sometimes."

        if mc_gender == "male":
            if renpy.loadable("scenes/plush_quest/quest8.png"):
                scene expression im.Scale("scenes/plush_quest/quest8.png", config.screen_width, config.screen_height) with dissolve
            mc "Rude."
        else:
            if renpy.loadable("scenes/plush_quest/quest8.png"):
                scene expression im.Scale("scenes/plush_quest/quest8.png", config.screen_width, config.screen_height) with dissolve
            mc "Wow. Rude."

        if renpy.loadable("scenes/plush_quest/quest7.png"):
            scene expression im.Scale("scenes/plush_quest/quest7.png", config.screen_width, config.screen_height) with dissolve
        tsuki "Also because I know you'll find them eventually."
        tsuki "You always poke around everywhere."

        if renpy.loadable("scenes/plush_quest/quest8.png"):
            scene expression im.Scale("scenes/plush_quest/quest8.png", config.screen_width, config.screen_height) with dissolve
        narrator "She's not wrong."

        if renpy.loadable("scenes/plush_quest/quest7.png"):
            scene expression im.Scale("scenes/plush_quest/quest7.png", config.screen_width, config.screen_height) with dissolve
        tsuki "If you see any while you're exploring places..."
        tsuki "Can you grab them for me?"
        tsuki "Please?"

        menu:
            "Sure, I'll keep an eye out.":
                if renpy.loadable("scenes/plush_quest/quest8.png"):
                    scene expression im.Scale("scenes/plush_quest/quest8.png", config.screen_width, config.screen_height) with dissolve
                mc "Fine."
                mc "If I spot any plushies hiding around, I'll pick them up."
                if renpy.loadable("scenes/plush_quest/quest12.png"):
                    scene expression im.Scale("scenes/plush_quest/quest12.png", config.screen_width, config.screen_height) with dissolve
                tsuki "Yay!"
                tsuki "I knew you'd help!"
            "You're really making me your plushie detective.":
                if renpy.loadable("scenes/plush_quest/quest8.png"):
                    scene expression im.Scale("scenes/plush_quest/quest8.png", config.screen_width, config.screen_height) with dissolve
                mc "So this is official now?"
                mc "I'm your plushie detective?"
                tsuki "Correct."
                if renpy.loadable("scenes/plush_quest/quest13.png"):
                    scene expression im.Scale("scenes/plush_quest/quest13.png", config.screen_width, config.screen_height) with dissolve
                tsuki "Congratulations on your promotion."

        if renpy.loadable("scenes/plush_quest/quest9.png"):
            scene expression im.Scale("scenes/plush_quest/quest9.png", config.screen_width, config.screen_height) with dissolve
        hana "Just try not to tear the house apart while you're looking."

        if renpy.loadable("scenes/plush_quest/quest7.png"):
            scene expression im.Scale("scenes/plush_quest/quest7.png", config.screen_width, config.screen_height) with dissolve
        tsuki "And if you find them..."
        tsuki "Bring them back to me!"

        if renpy.loadable("scenes/plush_quest/quest13.png"):
            scene expression im.Scale("scenes/plush_quest/quest13.png", config.screen_width, config.screen_height) with dissolve
        narrator "Tsuki beams proudly."

        $ day1_plushie_system_introduced = True

        if "ell_accept_quest" in globals():
            $ ell_accept_quest("tsuki_lost_plushies")
        if "ell_sync_collectible_quests" in globals():
            $ ell_sync_collectible_quests()

        call screen day1_game_ui_popup(
            title="NEW QUEST OBTAINED",
            subtitle="Tsuki's Lost Plushies",
            body="Hidden plushies are scattered across different locations. Keep an eye out while exploring and collect them when you find them."
        )

    if renpy.loadable("scenes/plush_quest/quest4.png"):
        scene expression im.Scale("scenes/plush_quest/quest4.png", config.screen_width, config.screen_height) with dissolve
    hana "Alright, you two. Finish getting ready. You don't want to rush the walk there."

    if renpy.loadable("scenes/breakfast_end.png"):
        scene expression im.Scale("scenes/breakfast_end.png", config.screen_width, config.screen_height) with dissolve
    narrator "With breakfast over and the morning conversation behind us, it's finally time to head out."

    scene black with fade
    narrator "A few minutes later..."

    if renpy.loadable("scenes/leaving.png"):
        scene expression im.Scale("scenes/leaving.png", config.screen_width, config.screen_height) with dissolve
    tsuki "Try not to embarrass yourself on day one."

    if mc_gender == "male":
        if renpy.loadable("scenes/leaving2.png"):
            scene expression im.Scale("scenes/leaving2.png", config.screen_width, config.screen_height) with dissolve
        mc "I'll do my worst."
    else:
        if renpy.loadable("scenes/leaving2.png"):
            scene expression im.Scale("scenes/leaving2.png", config.screen_width, config.screen_height) with dissolve
        mc "No promises."

    if renpy.loadable("scenes/leaving3.png"):
        scene expression im.Scale("scenes/leaving3.png", config.screen_width, config.screen_height) with dissolve
    hana "Have a good day, both of you."

    scene black with fade
    narrator "And just like that, the first day begins."

    jump day1_school_gate


# -----------------------------------------------------------------------------
# DAY 1: SCHOOL AND EVENING (STORY-LED INTRODUCTION)
# -----------------------------------------------------------------------------
# Day 1 intentionally stays linear. Small dialogue choices provide flavour, but
# all six school characters are introduced before class. Free exploration and
# Mini Tsuki's UI tutorial belong to Day 2 and are not implemented here.
#
# If you have custom scene renders, name them to match the optional assets
# below, or ask Codex to replace these candidate paths with your actual renders.
# Missing optional renders fall back safely to the project's main menu image,
# rather than causing a missing-image error.

init -10 python:
    def day1_optional_background(*candidates):
        for path in candidates:
            if renpy.loadable(path):
                return im.Scale(path, config.screen_width, config.screen_height)
        if renpy.loadable("gui/menu/mainmenu_bg.png"):
            return im.Scale("gui/menu/mainmenu_bg.png", config.screen_width, config.screen_height)
        return Solid("#191723")


label day1_school_gate:
    # WALK TO SCHOOL: no map or free-roam screen on Day 1.
    if renpy.has_image("school_walk_morning"):
        scene school_walk_morning with dissolve
    else:
        scene expression day1_optional_background("scenes/school_walk.png", "scenes/walk_to_school.png", "scenes/morning_street.png") with dissolve

    narrator "The morning air is cool enough to wake me up properly. Almost."
    narrator "Tsuki walks a few steps ahead, her bag bouncing against her side."

    tsuki "You're walking awfully slowly for someone who was nearly late."
    mc "I was perfectly on time until you started giving orders."
    tsuki "Oh? So waking you up was a mistake?"
    mc "I didn't say that."
    tsuki "Good. Because I'd happily let you sleep through the bell tomorrow."
    mc "You'd last about thirty seconds before coming to bother me."
    tsuki "...That's not the point!"

    narrator "We pass the little shops opening for the day. A few neighbours wave as students hurry along the pavement."
    narrator "Human voices mingle with the familiar sight of ears and tails beneath school coats."
    narrator "It's the kind of everyday scene I barely notice anymore."

    tsuki "Hey. Are you even listening?"
    mc "Something about you being the most generous little sister in Midgard?"
    tsuki "The {i}most{/i} generous. Don't forget it."
    mc "I'll have it engraved on a plaque."
    tsuki "Make it a big one."

    narrator "An old shop sign catches the morning sun. Its painted branches remind me of the stories Mum tells us about Ellrijord."
    narrator "To her, those places are memories. I was so young when we left that it's hard to tell what I remember myself and what I know from her stories."
    narrator "Sometimes there's sunlight through enormous branches, or a tune I can't quite finish. Nothing stays long enough to make a whole picture."
    narrator "Tsuki was born here in Midgard. She's only ever known Ellrijord through the people who remember it."

    tsuki "You're doing that thinking thing again."
    if mc_gender == "male":
        mc "Didn't know I was allowed to do that before first period."
    else:
        mc "Someone has to do it for both of us."
    tsuki "Rude!"
    narrator "She sticks her tongue out before turning back towards the road."

    if renpy.has_image("school_gate_morning"):
        scene school_gate_morning with dissolve
    else:
        scene expression day1_optional_background("scenes/school_gate.png", "scenes/school_gate_morning.png", "scenes/school_walk.png") with dissolve

    narrator "At last, the school gates come into view."
    narrator "Students stream through in little groups, trading holiday stories and complaints about the new term."

    tsuki "Right! I have places to be and people to impress."
    mc "Mostly people to annoy."
    tsuki "It's called having a social life. Try it sometime."
    mc "I'll put it on the list."
    tsuki "See you after school! And don't forget what you promised me!"
    narrator "She gives me an enthusiastic wave before disappearing into the crowd."
    narrator "The lost plushies. Right. She really is going to hold me to that."

    if mc_gender == "male":
        narrator "Another school year. Let's see how long it takes for things to get complicated."
    else:
        narrator "Same school, same morning rush. Somehow it still feels like a fresh start."

    jump day1_school_intro_hub


label day1_school_intro_hub:
    # Deliberately linear: both groups receive a Day 1 introduction.
    jump day1_intro_year3


label day1_intro_year3:
    if renpy.has_image("school_courtyard_morning"):
        scene school_courtyard_morning with dissolve
    else:
        scene expression day1_optional_background("scenes/school_courtyard.png", "scenes/school_gate.png") with dissolve

    narrator "I haven't even reached the main building when a familiar voice calls out."
    poko "Well, well! Look who survived the first morning!"

    if renpy.has_image("aria neutral"):
        show aria neutral at left
    if renpy.has_image("poko grin"):
        show poko grin at center
    if renpy.has_image("mimi smile"):
        show mimi smile at right

    narrator "Aria. Poko. Mimi."
    narrator "The Year 3 trio has a presence that makes the crowd around them feel just a little more alive."
    narrator "Even among the students arriving for class, they're difficult to miss."

    mc "Good morning to you too, Poko."
    poko "You're welcome! I was going to send a rescue team if you didn't show up."
    aria "You were going to finish telling us about your holiday, actually."
    poko "I can do two things!"
    mimi "That's quite an ambitious claim this early in the morning."
    poko "Mimi! You're supposed to be on my side!"

    narrator "Aria smiles as Poko throws her hands up in protest."
    narrator "Mimi, meanwhile, seems perfectly at ease despite the number of students greeting her on their way past."

    aria "It's good to see you again, [mc_first_name]. How was your morning?"
    menu:
        "Tsuki made sure I was awake.":
            mc "Loud. Tsuki took personal responsibility for getting me out of bed."
            poko "Ha! I knew I liked that kid."
            aria "She means well. Usually."
        "Surprisingly peaceful, all things considered.":
            mc "Not bad, actually. Breakfast with Mum and Tsuki was nice."
            mimi "That sounds like a lovely way to start the term."
            poko "You're making the rest of us look unprepared."

    aria "I found an old photo of Poppy and Gizmo this morning."
    poko "The birthday cake one?"
    aria "Gizmo had frosting everywhere. Poppy was trying to help."
    mc "And getting covered in it herself?"
    aria "Naturally. I miss that little team."

    narrator "Poppy and Gizmo passed away years ago, but I still remember birthdays like that."
    narrator "Aria smiles at the memory. For a moment, we let the morning bustle fill the quiet."

    aria "Anyway. New term. Any grand plans?"

    mimi "I'm looking forward to seeing what this term brings."
    poko "You mean you're looking forward to being top of the class again."
    mimi "Those aren't mutually exclusive."
    narrator "Mimi answers so sweetly that Poko doesn't seem to realise she's been teased until a moment later."

    narrator "A warning chime sounds from inside the building."
    aria "We'd better get moving."
    poko "Already? It's barely morning!"
    mimi "That is generally when the first bell rings."
    mc "You two never change."
    poko "And you'd miss me terribly if I did!"

    narrator "We head inside together before the corridor splits us in different directions."
    jump day1_intro_year2


label day1_intro_year2:
    if renpy.has_image("school_hallway_morning"):
        scene school_hallway_morning with dissolve
    else:
        scene expression day1_optional_background("scenes/school_hallway.png", "scenes/school_corridor.png") with dissolve

    narrator "A burst of familiar laughter reaches me from farther down the hallway."

    if renpy.has_image("kuroe neutral"):
        show kuroe neutral at left
    if renpy.has_image("sakura smile"):
        show sakura smile at center
    if renpy.has_image("rika grin"):
        show rika grin at right

    rika "There you are!"
    narrator "My younger cousin Rika appears in front of me before I can pretend I haven't heard her."
    rika "I was starting to think you'd got lost on the way here!"
    mc "Good morning to you too, Rika."
    rika "You're welcome!"

    sakura "Morning, [mc_first_name]. It's nice having everyone back."
    mc "Morning, Sakura."
    kuroe "We're not even through the first day. Give it time."
    sakura "Kuroe..."
    kuroe "I'm joking. Mostly."

    narrator "Kuroe's attention drifts towards a noticeboard near the stairs."
    narrator "Among the club notices is a faded poster showing an illustration of Yggdrasil."
    kuroe "They're putting up the old-world history display again."
    rika "Oh no. That look means she's found another mystery."
    kuroe "It's not a mystery just because you don't want to read about it."
    rika "See? Definitely a mystery."

    sakura "I think it'll be interesting. There are still so many stories about Ellrijord that never made it into the books."
    kuroe "Exactly. And the versions that did aren't always the same."
    narrator "For a moment, Kuroe looks far more serious than she did a second ago."

    mc "Sounds like you've already got your first project of the term."
    kuroe "Maybe."
    rika "Which means we'll all get dragged into it eventually."
    mc "I was afraid you'd say that."
    sakura "It might be fun!"

    narrator "The bell rings properly this time."
    sakura "We should get to class!"
    rika "Race you!"
    kuroe "No running in the halls."
    rika "You sound just like a teacher!"
    narrator "Rika darts away with Sakura following at a more sensible pace."
    narrator "Kuroe takes one last look at the poster before turning towards her classroom."

    narrator "Six familiar faces, and the day has barely begun."
    jump day1_class_intro


label day1_class_intro:
    if renpy.has_image("classroom_morning"):
        scene classroom_morning with dissolve
    else:
        scene expression day1_optional_background("scenes/classroom.png", "scenes/classroom_morning.png") with dissolve

    narrator "I reach my classroom just before the door closes."
    narrator "Chairs scrape against the floor as everyone settles in, and the last few conversations fade away."

    ell_teacher "Good morning, everyone. Welcome back."
    ell_teacher "I hope you've all had a good break, because we have plenty to cover this term."
    narrator "A handful of students groan. The teacher pretends not to hear them."
    ell_teacher "We'll begin with something familiar: the history shared by Midgard and Ellrijord."

    narrator "An illustration appears at the front of the room: the enormous branching form of Yggdrasil."
    ell_teacher "Many of your parents and grandparents remember Ellrijord as the home they left behind."
    ell_teacher "Some of you were very young when your families came to Midgard. Others were born here and know Ellrijord through the stories you've been told."
    ell_teacher "If you do have memories of Ellrijord, however fragmented, they belong to this history too."
    ell_teacher "The same history can look very different depending on who tells it. That's worth remembering."

    narrator "I glance at the drawing."
    narrator "Mum remembers a home. I have a few uncertain impressions, tangled up with stories I've heard all my life."
    narrator "Seeing it reduced to a drawing on the classroom wall still feels strange."

    if mc_gender == "female":
        call day1_akari_first_glimpse

    menu:
        "Pay close attention to the lesson.":
            $ day1_class_focus = "history"
            narrator "I open my notebook and copy down the title."
            mc "(Might as well start the term properly.)"
            ell_teacher "Good. We'll be revisiting these ideas throughout the year."
        "Let my thoughts wander for a moment.":
            $ day1_class_focus = "daydream"
            narrator "Outside the window, a breeze stirs the branches of a nearby tree."
            mc "(All this talk about other worlds before lunch...)"
            ell_teacher "[mc_first_name]? Still with us?"
            mc "Yes! Sorry."
            narrator "A couple of classmates try not to laugh."

    narrator "The morning passes in a blur of introductions, timetables and the first pages of new notebooks."
    narrator "By the time the lunch bell rings, my head is full of names, dates and enough reminders to last the week."

    jump day1_lunch


label day1_akari_first_glimpse:
    narrator "For a heartbeat, the branches in the drawing seem to move."
    narrator "There's sunlight between them. Someone is humming nearby, too softly for me to catch the tune."
    narrator "I blink. The drawing is still. The classroom is full of the scratch of pens."
    mc "(Was that something I remembered?)"
    narrator "I glance around. No one else seems to have noticed anything."
    $ day1_akari_glimpse_seen = True
    return


label day1_lunch:
    $ ell_time_of_day = "midday"
    if renpy.has_image("school_courtyard_morning"):
        scene school_courtyard_morning with dissolve
    else:
        scene expression day1_optional_background("scenes/school_lunch.png", "scenes/school_courtyard.png", "scenes/school_cafeteria.png") with dissolve

    narrator "Lunch turns the quiet courtyard into a chorus of voices."
    narrator "There are familiar faces scattered across the tables, and more than one group waves me over."
    narrator "I have time to sit with one group properly before the bell."

    # This affects only Day 1's extra dialogue. Everyone has already appeared.
    menu:
        "Spend lunch with Aria, Poko and Mimi.":
            $ day1_lunch_companion = "year3"
            jump day1_lunch_year3
        "Spend lunch with Kuroe, Sakura and Rika.":
            $ day1_lunch_companion = "year2"
            jump day1_lunch_year2


label day1_lunch_year3:
    narrator "I make my way over to Aria, Poko and Mimi."
    poko "Excellent choice! We were just deciding who's the most prepared for the new term."
    mc "And let me guess. You voted for yourself?"
    poko "Obviously."
    mimi "You forgot your timetable this morning."
    poko "Details!"
    aria "I had to lend her a pen as well."
    poko "Betrayal. From both sides."

    narrator "Mimi laughs and moves her bag aside so I can sit."
    mimi "It's nice having everyone back together. The holidays were strangely quiet."
    aria "You say that, but I saw how many messages you sent."
    mimi "I said {i}strangely{/i} quiet, not completely quiet."

    poko "Anyway, big plans for the term?"
    mc "Surviving it seems like a reasonable start."
    aria "Aim a little higher."
    mc "Surviving with good grades?"
    aria "Much better."

    narrator "The three of them fall into an easy argument about which club will be the busiest this year."
    narrator "I find myself smiling more than I expected."
    jump day1_lunch_finish


label day1_lunch_year2:
    narrator "I head towards Kuroe, Sakura and Rika."
    rika "Aha! I knew you'd come over!"
    mc "You were waving both arms at me. It was difficult not to notice."
    sakura "We saved you a space."
    kuroe "Rika was about to claim it for her bag."
    rika "My bag has feelings!"

    narrator "Sakura passes me a napkin before Rika can steal the last seat."
    sakura "So, how was your first lesson?"
    mc "Already got a history lecture."
    kuroe "About Ellrijord?"
    mc "Of course you'd ask that."
    kuroe "I saw the display poster earlier. I'd like to know where they got some of those records."
    rika "See? A whole term of mystery investigations."
    sakura "That doesn't sound too bad."
    mc "Remind me not to volunteer for anything before I've had lunch."

    narrator "Rika starts telling us a wildly exaggerated story about her morning."
    narrator "Kuroe corrects half the details. Sakura tries, unsuccessfully, to keep a straight face."
    narrator "It's hard not to feel at home with them."
    jump day1_lunch_finish


label day1_lunch_finish:
    narrator "Soon enough, the bell sounds and lunch comes to an end."
    narrator "I take one last look around the courtyard before heading back inside."
    narrator "It's only the first day, but the school already feels lively again."
    jump day1_afternoon_classes


label day1_afternoon_classes:
    $ ell_time_of_day = "afternoon"
    if renpy.has_image("classroom_morning"):
        scene classroom_morning with dissolve
    else:
        scene expression day1_optional_background("scenes/classroom_afternoon.png", "scenes/classroom.png") with dissolve

    narrator "The afternoon is less memorable: more introductions, a few classroom rules, and a timetable I already know I'll misplace."
    ell_teacher "Before you go, remember that the clubs and noticeboards will have their updated schedules posted tomorrow."
    ell_teacher "And please try to arrive on time from now on."
    narrator "A few people glance in my direction. I decide not to take that personally."

    narrator "When the final bell finally rings, the classroom comes back to life."
    narrator "Bags zip shut. Chairs scrape back. Someone cheers a little too loudly."
    mc "(One day down.)"
    jump day1_after_school


label day1_after_school:
    if renpy.has_image("school_gate_afternoon"):
        scene school_gate_afternoon with dissolve
    elif renpy.has_image("school_gate_morning"):
        scene school_gate_morning with dissolve
    else:
        scene expression day1_optional_background("scenes/school_gate_afternoon.png", "scenes/school_gate.png") with dissolve

    narrator "Outside, the afternoon sun stretches long shadows across the school entrance."
    narrator "I catch glimpses of the others leaving in different directions."

    poko "See you tomorrow! Don't forget how lucky you are to know me!"
    aria "Ignore her. Get home safely, okay?"
    mimi "See you soon, [mc_first_name]."
    narrator "Farther down the path, Rika waves so enthusiastically that Sakura has to tug her away from the crowd."
    rika "Bye!"
    sakura "See you tomorrow!"
    kuroe "Take care."

    narrator "A little farther along, Tsuki emerges from the remaining students, looking far too pleased with herself."
    tsuki "There you are!"
    mc "Did you spend the whole afternoon rehearsing that entrance?"
    tsuki "Maybe. How was your first day?"
    menu:
        "Better than I expected.":
            mc "Pretty good, actually. It was nice seeing everyone."
            tsuki "Aww. Look at you being all sentimental."
        "Exhausting. I deserve a medal.":
            mc "I survived. There should be some kind of reward."
            tsuki "I'll consider giving you a sticker."
    tsuki "Come on, then. Mum'll want to hear all about it."

    if renpy.has_image("school_walk_afternoon"):
        scene school_walk_afternoon with dissolve
    else:
        scene expression day1_optional_background("scenes/walk_home.png", "scenes/school_walk.png", "scenes/morning_street.png") with dissolve

    narrator "We head home together, taking the familiar streets at an easier pace than we managed this morning."
    tsuki "Don't think I've forgotten about the plushies, by the way."
    mc "I had a feeling you might mention them."
    tsuki "Just keeping my very reliable assistant informed."
    mc "Assistant? Since when was that my official job title?"
    tsuki "Since breakfast. No take-backs!"

    narrator "The afternoon light catches the windows of the shops as we pass."
    narrator "For a moment, the branches painted on the old sign look almost like the ones from our history lesson."
    narrator "Then Tsuki starts complaining about homework, and the thought slips away."
    jump day1_evening_home


label day1_evening_home:
    $ ell_time_of_day = "evening"
    if renpy.has_image("living_room_evening"):
        scene living_room_evening with dissolve
    else:
        scene expression day1_optional_background("scenes/living_room_evening.png", "scenes/Kitchen_open.png", "scenes/Hallway.png") with dissolve

    narrator "By the time we get home, the house feels wonderfully quiet."
    hana "Welcome back, you two! How was school?"
    tsuki "I was brilliant, obviously."
    hana "Of course you were. And [mc_first_name]?"
    mc "I made it through the first day."
    hana "That's a good start."

    narrator "We talk for a while about teachers, new timetables and the familiar faces we ran into."
    narrator "Tsuki adds unnecessary dramatic details to practically every story. Mum pretends not to notice."

    hana "Now that the term's started, you'll have a little more freedom in the afternoons. Just be sensible about where you go, and let me know if you'll be late."
    tsuki "See? Even Mum thinks you need looking after."
    mc "That applies to you too, Tsuki."
    tsuki "I choose not to hear that."

    narrator "The rest of the evening passes easily. Dinner, a few things to put away, and the familiar comfort of being home."
    if mc_gender == "female" and day1_akari_glimpse_seen:
        call day1_akari_hana_memories
    narrator "Eventually, I excuse myself and head back to my room."
    jump day1_night


label day1_akari_hana_memories:
    narrator "Tsuki heads upstairs to unpack her bag. I linger at the table while Mum gathers the last plates."
    mc "Mum? How old was I when we left Ellrijord?"
    hana "About two and a half. We reached Midgard a little over fifteen years ago."
    hana "Tsuki was born not long after we settled here. Why do you ask?"
    mc "We were looking at a picture of Yggdrasil in class. For a second, I could almost see sunlight through the branches."
    mc "And someone humming. Then it was gone."
    narrator "Mum sets the plates down and takes the chair beside me."
    hana "I used to hum to you when you were little. I still did after we came here."
    mc "So it could be a real memory?"
    hana "It could be. I can't tell from that alone."
    mc "I wish I remembered more than little pieces."
    hana "I can tell you what I remember. But you don't have to force your own memories to match mine."
    mc "What if it was just something I dreamed?"
    hana "Then you can tell me about that too."
    narrator "She rests her hand over mine. I hadn't realised how tightly I'd been holding the edge of the table."
    mc "Thanks, Mum."
    hana "Any time."
    $ day1_akari_hana_talk_seen = True
    return


label day1_night:
    $ ell_time_of_day = "night"
    if renpy.has_image("bedroom_night"):
        scene bedroom_night with dissolve
    else:
        scene expression day1_optional_background("scenes/bedroom_night.png", "gui/maps/bedroom_night.png", "gui/maps/bedroom2.png") with dissolve

    narrator "My room is quiet again."
    narrator "This morning, I could barely get out of bed. Now the entire first day feels like a collection of moments passing through my head."
    narrator "Tsuki's threats. Mum's smile. Aria, Poko and Mimi laughing in the courtyard. Rika calling to me down the hallway."
    narrator "And that old picture of Yggdrasil on the classroom wall."

    narrator "I set my bag aside and glance towards the window."
    narrator "Beyond the rooftops, the sky has darkened to a deep blue."
    narrator "For the briefest moment, a pale shimmer seems to flicker between the clouds."
    narrator "I blink, and it's gone."

    mc "(Probably just tired.)"
    narrator "Still, I can't quite forget it."

    tsuki "[mc_first_name]? Are you still awake?"
    mc "Barely."
    tsuki "Good. I just wanted to say... don't forget my plushies tomorrow, okay?"
    mc "You came all the way here to remind me?"
    tsuki "Maybe. Goodnight!"
    narrator "Her footsteps retreat down the hallway before I can answer."
    mc "Goodnight, Tsuki."

    narrator "Somewhere between the familiar warmth of home and the questions left unanswered by the day, sleep finally catches up with me."
    scene black with fade
    if mc_gender == "female":
        call day1_akari_first_dream
    narrator "And just like that, Day 1 comes to an end."

    jump day1_end_of_intro


label day1_akari_first_dream:
    narrator "At first, there is only the tune from earlier. A few notes, then a gap."
    narrator "Sunlight moves over bark beneath my hand. The branches stretch far above me."
    narrator "I look down. The hand resting against the tree is larger than mine, the fingers unfamiliar."
    narrator "Behind me, a little girl calls for her mum."
    narrator "I start to turn, but the scene breaks apart before I can see her."
    mc "(Whose hands were those?)"
    narrator "For an instant, I'm almost awake. Then the last of the image slips away and sleep draws me under again."
    $ day1_akari_dream_seen = True
    return


label day1_end_of_intro:
    # The wake-up tutorial and exploration loop live in day2_intro.rpy.
    $ ell_day = 2
    $ ell_time_of_day = "morning"
    if renpy.has_label("day2_opening"):
        jump expression "day2_opening"

    # Safe fallback if this script is used without the Day 2 files.
    return
