# day1_intro.rpy
# Ellrijord: Tales of Light and Void
# Day 1 Opening - Bedroom -> Living Room -> First School Arrival

default ell_day = 1
default ell_time_of_day = "morning"
default bedroom_clothes_taken = False
default day1_uniform_added_to_inventory = False
default day1_breakfast_topics_seen = set()
default day1_plushie_system_introduced = False
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

        if not hasattr(s, "tsuki"):
            s.tsuki = C("Tsuki", color="#d8c4ff")
        if not hasattr(s, "hana"):
            s.hana = C("Hana", color="#f4b6c2")

        if not hasattr(s, "aria"):
            s.aria = C("Aria", color="#d8c4ff")
        if not hasattr(s, "poko"):
            s.poko = C("Poko", color="#ff9a76")
        if not hasattr(s, "reina"):
            s.reina = C("Reina", color="#ffd6f1")

        if not hasattr(s, "kuroe"):
            s.kuroe = C("Kuroe", color="#6c6cff")
        if not hasattr(s, "sakura"):
            s.sakura = C("Sakura", color="#ffb7d5")
        if not hasattr(s, "rika"):
            s.rika = C("Rika", color="#c88cff")

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

    stop music fadeout 1.0
    scene black with fade

    $ _day1_music = None
    if renpy.loadable("audio/bgm/morning_theme.ogg"):
        $ _day1_music = "audio/bgm/morning_theme.ogg"
    elif renpy.loadable("audio/converted/Cherry Blossom.wav"):
        $ _day1_music = "audio/converted/Cherry Blossom.wav"
    if _day1_music:
        play music _day1_music fadein 2.0

    tsuki "Wake up already!"
    tsuki "Come on, [mc_first_name]! You're going to be late for school if you don't get up!"
    tsuki "Mom said if you miss the first day, she's blaming me too, so move!"

    narrator "A familiar voice cuts through the warmth of sleep."

    if mc_gender == "male":
        mc "Tsk... five more minutes..."
    else:
        mc "Mmgh... just five more minutes..."

    tsuki "Nope."
    tsuki "Absolutely not."
    tsuki "You said that yesterday, and the day before that."

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
    $ _room_button_idle = Transform(pref_choice_button_asset(), size=(_room_button_width, _room_button_height)) if _is_komic else Solid("#141414c8")
    $ _room_button_hover = Transform(pref_choice_button_asset(True), size=(_room_button_width, _room_button_height)) if _is_komic else Solid("#2a2a2ae0")
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

    frame:
        xalign 0.5
        yalign 0.5
        xsize 980
        ypadding 28
        xpadding 36
        if renpy.loadable("gui/collectibles/collectible_panel_720p.png"):
            background Frame("gui/collectibles/collectible_panel_720p.png", 40, 40)
        else:
            background Solid("#111111ee")

        vbox:
            spacing 14
            xalign 0.5
            yalign 0.5

            text "[title]":
                xalign 0.5
                text_align 0.5
                size 54
                color "#f8f8f8"
                outlines [(2, "#000000cc", 0, 0)]

            if subtitle:
                text "[subtitle]":
                    xalign 0.5
                    text_align 0.5
                    size 40
                    color "#ffdca8"
                    outlines [(2, "#000000cc", 0, 0)]

            if body:
                fixed:
                    xalign 0.5
                    xsize 760
                    ysize 210

                    if renpy.loadable("gui/collectibles/collectible_body_720p.png"):
                        add Transform("gui/collectibles/collectible_body_720p.png", fit="contain", xsize=760, ysize=210):
                            xalign 0.5
                            yalign 0.5

                    text "[body]":
                        xalign 0.5
                        yalign 0.5
                        text_align 0.5
                        size 26
                        color "#6f6267"
                        outlines [(1, "#f6efe4", 0, 0)]
                        xmaximum 620

            null height 10

            if renpy.loadable("gui/collectibles/collectible_button_720p.png"):
                fixed:
                    xalign 0.5
                    xsize 320
                    ysize 96
                    yoffset -12

                    imagebutton:
                        idle Transform("gui/collectibles/collectible_button_720p.png", fit="contain", xsize=320, ysize=96)
                        if renpy.loadable("gui/collectibles/collectible_button_hover_720p.png"):
                            hover Transform("gui/collectibles/collectible_button_hover_720p.png", fit="contain", xsize=320, ysize=96)
                        else:
                            hover Transform("gui/collectibles/collectible_button_720p.png", fit="contain", xsize=320, ysize=96)
                        xalign 0.5
                        yalign 0.5
                        action Return()

                    text "Continue":
                        xalign 0.5
                        yalign 0.5
                        size 26
                        color "#ffffff"
                        outlines [(2, "#7c655c", 0, 0)]
            else:
                textbutton "Continue":
                    xalign 0.5
                    ysize 54
                    xpadding 28
                    ypadding 10
                    background Solid("#2a2a2ae0")
                    hover_background Solid("#454545ee")
                    text_size 34
                    text_color "#f8f8f8"
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
    hana "You'll be seeing Aria, Poko, and Reina again today, won't you?"

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
    tsuki "And Reina's the pretty one everyone gets nervous around?"

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

            "Talk about Reina" if "reina" not in day1_breakfast_topics_seen:
                $ day1_breakfast_topics_seen.add("reina")
                mc "Reina's the dangerous one."
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
                narrator "Reina never needs to raise her voice to take control of a conversation."

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


label day1_school_gate:
    if renpy.has_image("school_gate_morning"):
        scene school_gate_morning with dissolve
    elif renpy.has_image("bg city_street_day"):
        scene bg city_street_day with dissolve
    elif renpy.loadable("gui/menu/mainmenu_bg.png"):
        scene expression im.Scale("gui/menu/mainmenu_bg.png", config.screen_width, config.screen_height) with dissolve
    else:
        scene black with dissolve

    narrator "The school stands ahead of us, just as familiar and imposing as ever."
    narrator "Students move in clumps across the grounds, conversations blending into one constant wave of noise."

    if mc_gender == "male":
        narrator "Another year."
        narrator "Another chance for everything to change."
    else:
        narrator "Same gates. Same uniforms."
        narrator "But something about today feels different."

    narrator "Somewhere in this crowd are the people who will shape the days to come."
    narrator "Upperclassmen. Friends. Trouble."
    narrator "Maybe all three at once."

    jump day1_school_intro_hub


label day1_school_intro_hub:
    narrator "The morning bell hasn't rung yet."
    narrator "There's still a little time before classes start."

    menu:
        "Look for the Year 3s":
            jump day1_intro_year3
        "Look for the Year 2s":
            jump day1_intro_year2
        "Head toward class":
            jump day1_class_intro


label day1_intro_year3:
    if renpy.has_image("school_courtyard_morning"):
        scene school_courtyard_morning with dissolve
    elif renpy.has_image("bg city_street_day"):
        scene bg city_street_day with dissolve
    elif renpy.loadable("gui/menu/mainmenu_bg.png"):
        scene expression im.Scale("gui/menu/mainmenu_bg.png", config.screen_width, config.screen_height) with dissolve
    else:
        scene black with dissolve

    narrator "It doesn't take long to spot them."

    if renpy.has_image("aria neutral"):
        show aria neutral at left
    if renpy.has_image("poko grin"):
        show poko grin at center
    if renpy.has_image("reina smile"):
        show reina smile at right

    narrator "Aria. Poko. Reina."
    narrator "The Year 3 trio has presence in a way that makes the air around them feel just a little more charged."
    narrator "Even among the crowd gathering before class, they stand out effortlessly."

    poko "Well, well."
    poko "Look who survived morning."

    reina "You say that as though it was ever in doubt."

    aria "First day nerves suit you less than you'd think."

    if mc_gender == "male":
        mc "Good morning to you too."
    else:
        mc "Wow. You really came ready to attack before first period."

    narrator "And just like that, the day starts moving."

    jump day1_end_of_intro


label day1_intro_year2:
    if renpy.has_image("school_hallway_morning"):
        scene school_hallway_morning with dissolve
    elif renpy.has_image("bg city_street_day"):
        scene bg city_street_day with dissolve
    elif renpy.loadable("gui/menu/mainmenu_bg.png"):
        scene expression im.Scale("gui/menu/mainmenu_bg.png", config.screen_width, config.screen_height) with dissolve
    else:
        scene black with dissolve

    narrator "A familiar cluster of voices pulls my attention down the hall."

    if renpy.has_image("kuroe neutral"):
        show kuroe neutral at left
    if renpy.has_image("sakura smile"):
        show sakura smile at center
    if renpy.has_image("rika grin"):
        show rika grin at right

    narrator "Kuroe. Sakura. Rika."
    narrator "The Year 2 group somehow manages to feel both approachable and dangerous at the same time."

    rika "There you are!"
    rika "I was starting to think you'd gotten lost before the year even started."

    if mc_gender == "male":
        mc "You're way too confident for someone who's still younger than me."
    else:
        mc "And you're way too pleased with yourself this early."

    sakura "It's nice to see everyone again."
    kuroe "More or less."

    narrator "So much for easing into the day."

    jump day1_end_of_intro


label day1_class_intro:
    if renpy.has_image("classroom_morning"):
        scene classroom_morning with dissolve
    elif renpy.has_image("bg bakery_day"):
        scene bg bakery_day with dissolve
    elif renpy.loadable("gui/menu/mainmenu_bg.png"):
        scene expression im.Scale("gui/menu/mainmenu_bg.png", config.screen_width, config.screen_height) with dissolve
    else:
        scene black with dissolve

    narrator "Might as well head in before the real chaos starts."
    narrator "Once class begins, there'll be no slowing the day down."

    jump day1_end_of_intro


label day1_end_of_intro:
    scene black with fade
    narrator "Day 1 opening complete."
    return
