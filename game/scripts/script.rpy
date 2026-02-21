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
    default hovered_gender = None

    $ female_hovered = hovered_gender == "female"
    $ male_hovered = hovered_gender == "male"

    if renpy.loadable("gui/mainmenu_bg.png"):
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    else:
        add Solid("#1f1f26")
    add Solid("#010611a8")

    hbox:
        xalign 0.5
        yalign 0.5
        spacing 50

        frame:
            xsize 430
            ysize 760
            padding (6, 6)
            background Frame(
                Solid("#a9d4ff" if female_hovered else ("#8fc3ff" if mc_gender == "female" else "#6ea3e8")),
                10,
                10
            )

            fixed:
                xfill True
                yfill True
                button:
                    background "#03102a"
                    hover_background "#0a1a3d"
                    xfill True
                    yfill True
                    action Function(set_mc_gender, "female")
                    hovered SetScreenVariable("hovered_gender", "female")
                    unhovered SetScreenVariable("hovered_gender", None)

                    if renpy.loadable("gui/mc_female.png"):
                        add Transform("gui/mc_female.png", fit="contain", xalign=0.5, yalign=1.0, xsize=390, ysize=730):
                            alpha (1.0 if (mc_gender == "female" or female_hovered) else 0.45)
                            zoom (1.03 if female_hovered else 1.0)
                    else:
                        add Solid("#03102a")
                        text "FEMALE" at Transform(alpha=(1.0 if (mc_gender == "female" or female_hovered) else 0.45)):
                            style "ui_btn_text"
                            xalign 0.5
                            yalign 0.5
                            size 52
                            color "#d9ecff"
                            outlines [ (2, "#203f67", 0, 0) ]

        vbox:
            xsize 520
            spacing 24
            yalign 0.5

            text "FIRST NAME":
                style "ui_btn_text"
                xalign 0.5
                size 86
                color "#d7ebff"
                outlines [ (3, "#1f3e66", 0, 0) ]

            frame:
                xalign 0.5
                xsize 470
                ysize 88
                background "#08132acc"
                padding (20, 16)

                input:
                    value VariableInputValue("mc_first_name", returnable=False)
                    length 20
                    xalign 0.5
                    yalign 0.5
                    font "fonts/trotes/Trotes.ttf"
                    size 56
                    color "#e7f4ff"
                    outlines [ (2, "#1b3458", 0, 0) ]

            text "Click a character portrait to choose":
                style "ui_btn_text"
                xalign 0.5
                size 34
                color "#c7ddf8"
                outlines [ (2, "#1e3a60", 0, 0) ]

            text "[mc_pronoun_subject_cap]/[mc_pronoun_object_cap]":
                style "ui_btn_text"
                xalign 0.5
                size 44
                color "#d8ecff"
                outlines [ (2, "#1d3a61", 0, 0) ]

            text "Family Name: [mc_last_name]":
                style "ui_btn_text"
                xalign 0.5
                size 34
                color "#c7ddf8"
                outlines [ (2, "#1d395f", 0, 0) ]

            textbutton "CONFIRM":
                xalign 0.5
                xsize 360
                ysize 96
                action [Function(finalize_mc_profile), SetVariable("mc_profile_done", True), Return(True)]
                text_style "ui_btn_text"
                background "#0f254ddd"
                hover_background "#255195"
                text_color "#dff0ff"
                text_outlines [ (3, "#2a4d7a", 0, 0) ]
                text_xalign 0.5

        frame:
            xsize 430
            ysize 760
            padding (6, 6)
            background Frame(
                Solid("#a9d4ff" if male_hovered else ("#8fc3ff" if mc_gender == "male" else "#6ea3e8")),
                10,
                10
            )

            fixed:
                xfill True
                yfill True
                button:
                    background "#03102a"
                    hover_background "#0a1a3d"
                    xfill True
                    yfill True
                    action Function(set_mc_gender, "male")
                    hovered SetScreenVariable("hovered_gender", "male")
                    unhovered SetScreenVariable("hovered_gender", None)

                    if renpy.loadable("gui/mc_male.png"):
                        add Transform("gui/mc_male.png", fit="contain", xalign=0.5, yalign=1.0, xsize=390, ysize=730):
                            alpha (1.0 if (mc_gender == "male" or male_hovered) else 0.45)
                            zoom (1.03 if male_hovered else 1.0)
                    else:
                        add Solid("#03102a")
                        text "MALE" at Transform(alpha=(1.0 if (mc_gender == "male" or male_hovered) else 0.45)):
                            style "ui_btn_text"
                            xalign 0.5
                            yalign 0.5
                            size 52
                            color "#d9ecff"
                            outlines [ (2, "#203f67", 0, 0) ]

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

    if mc_gender == "female":
        call female_route_start
    else:
        call male_route_start

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
