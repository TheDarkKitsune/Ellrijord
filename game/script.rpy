# game/script.rpy

default intro_story_video = "Story.webm"
default run_ui_test_demo = True
default mc_profile_done = False

default mc_first_name = "Feniks"
# Keep this as your fixed family/last name.
default mc_last_name = "Dev"

default mc_gender = "male"
default mc_pronoun_subject = "he"
default mc_pronoun_object = "him"
default mc_pronoun_subject_cap = "He"
default mc_pronoun_object_cap = "Him"

init python:
    def resolve_story_video(base_name):
        candidates = [
            base_name,
            "movies/" + base_name,
            "video/" + base_name,
            "gui/intro/" + base_name,
        ]
        exts = [".webm", ".mp4", ".ogv", ".mkv", ".avi"]

        for c in candidates:
            if renpy.loadable(c):
                return c
            for ext in exts:
                p = c + ext
                if renpy.loadable(p):
                    return p
        return None

    def set_mc_gender(gender):
        s = renpy.store
        s.mc_gender = "female" if gender == "female" else "male"
        if s.mc_gender == "female":
            s.mc_pronoun_subject = "she"
            s.mc_pronoun_object = "her"
            s.mc_pronoun_subject_cap = "She"
            s.mc_pronoun_object_cap = "Her"
        else:
            s.mc_pronoun_subject = "he"
            s.mc_pronoun_object = "him"
            s.mc_pronoun_subject_cap = "He"
            s.mc_pronoun_object_cap = "Him"

    def finalize_mc_profile():
        s = renpy.store
        n = (s.mc_first_name or "").strip()
        s.mc_first_name = n if n else "Feniks"
        set_mc_gender(s.mc_gender)


screen intro_press_any_to_continue():
    modal True
    key "dismiss" action Return()
    key "mouseup_1" action Return()
    key "K_RETURN" action Return()
    key "K_SPACE" action Return()

    if renpy.loadable("gui/Start.png"):
        add im.Scale("gui/Start.png", config.screen_width, config.screen_height)
    else:
        add Solid("#000000")

    text "Press any button to continue":
        style "ui_btn_text"
        xalign 0.5
        yalign 0.92
        size 46


screen mc_profile_setup():
    modal True

    if renpy.loadable("gui/mainmenu_bg.png"):
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    else:
        add Solid("#1f1f26")
    add Solid("#00000080")

    hbox:
        xalign 0.5
        yalign 0.5
        spacing 50

        frame:
            xsize 430
            ysize 760
            background Frame(Solid("#8e68d8"), 10, 10)

            fixed:
                xfill True
                yfill True
                if renpy.loadable("gui/mc_female.png"):
                    add Transform("gui/mc_female.png", fit="contain", xalign=0.5, yalign=1.0, xsize=390, ysize=730):
                        alpha (1.0 if mc_gender == "female" else 0.45)
                else:
                    add Solid("#8e68d8")
                    text "FEMALE" at Transform(alpha=(1.0 if mc_gender == "female" else 0.45)):
                        xalign 0.5
                        yalign 0.5
                        size 52
                        color "#ffffff"
                        outlines [ (2, "#00000066", 0, 0) ]

        vbox:
            xsize 520
            spacing 24
            yalign 0.5

            text "NAME":
                xalign 0.5
                size 86
                color "#ffffff"
                outlines [ (3, "#00000080", 0, 0) ]

            frame:
                xalign 0.5
                xsize 470
                ysize 88
                background "#151515cc"
                padding (20, 16)

                input:
                    value VariableInputValue("mc_first_name", returnable=False)
                    length 20
                    xalign 0.5
                    yalign 0.5
                    size 56
                    color "#ffffff"
                    outlines [ (2, "#00000066", 0, 0) ]

            text "GENDER":
                xalign 0.5
                size 80
                color "#ffffff"
                outlines [ (3, "#00000080", 0, 0) ]

            textbutton "Male":
                xalign 0.5
                xsize 470
                ysize 92
                action Function(set_mc_gender, "male")
                selected (mc_gender == "male")
                text_size 56
                text_xalign 0.5
                background "#ffffffff"
                selected_background "#bfe8ff"
                text_color "#111111"

            textbutton "Female":
                xalign 0.5
                xsize 470
                ysize 92
                action Function(set_mc_gender, "female")
                selected (mc_gender == "female")
                text_size 56
                text_xalign 0.5
                background "#111111cc"
                selected_background "#7d5be0"
                text_color "#ffffff"

            text "[mc_pronoun_subject_cap]/[mc_pronoun_object_cap]":
                xalign 0.5
                size 44
                color "#e6e6e6"
                outlines [ (2, "#00000080", 0, 0) ]

            text "Family Name: [mc_last_name]":
                xalign 0.5
                size 34
                color "#e6e6e6"
                outlines [ (2, "#00000066", 0, 0) ]

            textbutton "CONFIRM":
                xalign 0.5
                xsize 360
                ysize 96
                action [Function(finalize_mc_profile), SetVariable("mc_profile_done", True), Return(True)]
                text_style "ui_btn_text"
                background "#221f2ecc"
                hover_background "#4f3b80"
                text_xalign 0.5

        frame:
            xsize 430
            ysize 760
            background Frame(Solid("#333340"), 10, 10)

            fixed:
                xfill True
                yfill True
                if renpy.loadable("gui/mc_male.png"):
                    add Transform("gui/mc_male.png", fit="contain", xalign=0.5, yalign=1.0, xsize=390, ysize=730):
                        alpha (1.0 if mc_gender == "male" else 0.45)
                else:
                    add Solid("#333340")
                    text "MALE" at Transform(alpha=(1.0 if mc_gender == "male" else 0.45)):
                        xalign 0.5
                        yalign 0.5
                        size 52
                        color "#ffffff"
                        outlines [ (2, "#00000066", 0, 0) ]

label start:
    window hide
    scene black
    with dissolve

    $ _story_video = resolve_story_video(intro_story_video)
    if _story_video:
        $ renpy.movie_cutscene(_story_video)
    else:
        scene black
        centered "Video not found: [intro_story_video]"
    call screen intro_press_any_to_continue
    if not mc_profile_done:
        call screen mc_profile_setup
    if run_ui_test_demo:
        call ui_test_demo

    return


label ui_test_demo:
    $ test_char = Character("[mc_first_name] [mc_last_name]")

    window show

    if renpy.loadable("gui/mainmenu_bg.png"):
        scene expression im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    else:
        scene black

    with dissolve

    test_char "Would you like to... come to my house?"

    menu:
        "Yes.":
            test_char "[mc_pronoun_subject_cap] said yes. This is a test line so you can check textbox spacing and button visibility."
        "No, I think another time.":
            test_char "No worries. This is still the same UI test branch."

    test_char "Open the game menu here to test settings styling as well."

    return
