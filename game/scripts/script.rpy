# game/script.rpy

default intro_story_video = "Story.webm"
default run_ui_test_demo = True
default mc_profile_done = False

default mc_first_name = "Feniks"
# Keep this as your fixed family/last name.
default mc_last_name = "Kuzunoha"

default mc_gender = "male"
default mc_pronoun_subject = "he"
default mc_pronoun_object = "him"
default mc_pronoun_subject_cap = "He"
default mc_pronoun_object_cap = "Him"
default persistent.last_played_dlc = ""

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
        # Reset first name to the selected character's default until player types a custom one.
        s.mc_first_name = "Akari" if s.mc_gender == "female" else "Kaito"
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
        s.mc_last_name = "Kuzunoha"
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
    $ _typed_name = (mc_first_name or "").strip()
    $ _female_display_name = _typed_name if (mc_gender == "female" and _typed_name) else "Akari"
    $ _male_display_name = _typed_name if (mc_gender == "male" and _typed_name) else "Kaito"

    if renpy.loadable("gui/mainmenu_bg.png"):
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    else:
        add Solid("#1f1f26")
    add Solid("#01061166")

    text "Choose Your Name":
        font "fonts/cinzel/Cinzel-Bold.otf"
        xalign 0.5
        ypos 38
        size 72
        color "#ffffff"
        outlines [(2, "#1f2635cc", 0, 0)]

    text "Select your protagonist":
        font "fonts/cinzel/Cinzel-Bold.otf"
        xalign 0.5
        ypos 126
        size 36
        color "#d7dfef"
        outlines [(1, "#1f2635cc", 0, 0)]

    hbox:
        xalign 0.5
        yalign 0.5
        spacing 50

        fixed:
            xsize 430
            ysize 760

            button:
                background None
                hover_background None
                xfill True
                yfill True
                action Function(set_mc_gender, "female")
                hovered SetScreenVariable("hovered_gender", "female")
                unhovered SetScreenVariable("hovered_gender", None)

                if renpy.loadable("gui/Akari.png"):
                    if mc_gender == "female":
                        add Transform("gui/Akari.png", crop=(793, 251, 198, 698), fit="contain", xalign=0.5, yalign=0.5, xsize=418, ysize=748, xoffset=-3, matrixcolor=TintMatrix("#ba7dff")) at profile_glow_pulse
                        add Transform("gui/Akari.png", crop=(793, 251, 198, 698), fit="contain", xalign=0.5, yalign=0.5, xsize=418, ysize=748, xoffset=3, matrixcolor=TintMatrix("#ba7dff")) at profile_glow_pulse
                        add Transform("gui/Akari.png", crop=(793, 251, 198, 698), fit="contain", xalign=0.5, yalign=0.5, xsize=418, ysize=748, yoffset=-3, matrixcolor=TintMatrix("#ba7dff")) at profile_glow_pulse
                        add Transform("gui/Akari.png", crop=(793, 251, 198, 698), fit="contain", xalign=0.5, yalign=0.5, xsize=418, ysize=748, yoffset=3, matrixcolor=TintMatrix("#ba7dff")) at profile_glow_pulse

                    add Transform("gui/Akari.png", crop=(793, 251, 198, 698), fit="contain", xalign=0.5, yalign=0.5, xsize=418, ysize=748):
                        alpha (1.0 if (mc_gender == "female" or female_hovered) else 0.62)
                        zoom (1.00 if female_hovered else 0.96)

                    if mc_gender == "female":
                        add Transform(Solid("#f6ceff"), xpos=92, ypos=168, xsize=6, ysize=6) at profile_sparkle_rise_a
                        add Transform(Solid("#d98cff"), xpos=120, ypos=236, xsize=5, ysize=5) at profile_sparkle_rise_b
                        add Transform(Solid("#ffe6ff"), xpos=334, ypos=210, xsize=4, ysize=4) at profile_sparkle_rise_c
                        add Transform(Solid("#cf8dff"), xpos=308, ypos=152, xsize=6, ysize=6) at profile_sparkle_rise_b
                elif renpy.loadable("gui/mc_female.png"):
                    if mc_gender == "female":
                        add Transform("gui/mc_female.png", fit="cover", xalign=0.5, yalign=0.5, xsize=418, ysize=748, xoffset=-3, matrixcolor=TintMatrix("#ba7dff")) at profile_glow_pulse
                        add Transform("gui/mc_female.png", fit="cover", xalign=0.5, yalign=0.5, xsize=418, ysize=748, xoffset=3, matrixcolor=TintMatrix("#ba7dff")) at profile_glow_pulse
                        add Transform("gui/mc_female.png", fit="cover", xalign=0.5, yalign=0.5, xsize=418, ysize=748, yoffset=-3, matrixcolor=TintMatrix("#ba7dff")) at profile_glow_pulse
                        add Transform("gui/mc_female.png", fit="cover", xalign=0.5, yalign=0.5, xsize=418, ysize=748, yoffset=3, matrixcolor=TintMatrix("#ba7dff")) at profile_glow_pulse

                    add Transform("gui/mc_female.png", fit="cover", xalign=0.5, yalign=0.5, xsize=418, ysize=748):
                        alpha (1.0 if (mc_gender == "female" or female_hovered) else 0.62)
                        zoom (1.03 if female_hovered else 1.0)

                    if mc_gender == "female":
                        add Transform(Solid("#f6ceff"), xpos=92, ypos=168, xsize=6, ysize=6) at profile_sparkle_rise_a
                        add Transform(Solid("#d98cff"), xpos=120, ypos=236, xsize=5, ysize=5) at profile_sparkle_rise_b
                        add Transform(Solid("#ffe6ff"), xpos=334, ypos=210, xsize=4, ysize=4) at profile_sparkle_rise_c
                        add Transform(Solid("#cf8dff"), xpos=308, ypos=152, xsize=6, ysize=6) at profile_sparkle_rise_b
                else:
                    text "FEMALE" at Transform(alpha=(1.0 if (mc_gender == "female" or female_hovered) else 0.45)):
                        style "ui_btn_text"
                        xalign 0.5
                        yalign 0.5
                        size 52
                        color "#d9ecff"
                        outlines [ (2, "#203f67", 0, 0) ]

            vbox:
                xalign 0.5
                yalign 1.0
                yoffset 132
                spacing 2

                text "[_female_display_name] [mc_last_name]":
                    font "fonts/cinzel/Cinzel-Bold.otf"
                    size 52
                    xalign 0.5
                    at Transform(alpha=(1.0 if mc_gender == "female" else 0.72))
                    color ("#ffd77f" if (mc_gender == "female" or female_hovered) else "#dbe5f2")
                    outlines [(2, "#11161fbb", 0, 0)]

                text "She / Her":
                    font "fonts/cinzel/Cinzel-Bold.otf"
                    size 42
                    xalign 0.5
                    at Transform(alpha=(1.0 if mc_gender == "female" else 0.66))
                    color ("#ffe59a" if (mc_gender == "female" or female_hovered) else "#cbd5e3")
                    outlines [(1, "#11161fbb", 0, 0)]

        vbox:
            xsize 520
            spacing 14
            yalign 0.5

            fixed:
                xalign 0.5
                xsize 560
                ysize 420

                add Solid("#7ea9e0cc") xsize 560 ysize 420
                add Solid("#102447d8") xpos 3 ypos 3 xsize 554 ysize 414
                add Solid("#c9dcff14") xpos 22 ypos 20 xsize 516 ysize 372

                vbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 16
                    xsize 500

                    fixed:
                        xalign 0.5
                        xsize 500
                        ysize 96
                        add Solid("#7ea9e0dd") xsize 500 ysize 96
                        add Solid("#122a51ee") xpos 3 ypos 3 xsize 494 ysize 90

                        input:
                            value VariableInputValue("mc_first_name", returnable=False)
                            length 20
                            xalign 0.5
                            yalign 0.5
                            font "fonts/cinzel/Cinzel-Bold.otf"
                            size 68
                            color "#ffffff"
                            outlines [(2, "#1f2635cc", 0, 0)]

                    text "Family Name":
                        font "fonts/cinzel/Cinzel-Bold.otf"
                        xalign 0.5
                        size 54
                        color "#f2dfad"
                        outlines [(1, "#1f2635cc", 0, 0)]

                    text "[mc_last_name]":
                        font "fonts/cinzel/Cinzel-Bold.otf"
                        xalign 0.5
                        size 60
                        color "#ffffff"
                        outlines [(2, "#1f2635cc", 0, 0)]

            textbutton "Confirm":
                xalign 0.5
                xsize 420
                ysize 92
                action [Function(finalize_mc_profile), SetVariable("mc_profile_done", True), Return(True)]
                text_style "ui_btn_text"
                background "#7ea9e0dd"
                hover_background "#95bdf0f0"
                text_color "#0f2445"
                text_outlines [ (1, "#d5e8ff", 0, 0) ]
                text_xalign 0.5

        fixed:
            xsize 430
            ysize 760

            button:
                background None
                hover_background None
                xfill True
                yfill True
                action Function(set_mc_gender, "male")
                hovered SetScreenVariable("hovered_gender", "male")
                unhovered SetScreenVariable("hovered_gender", None)

                if renpy.loadable("gui/Kaito.png"):
                    if mc_gender == "male":
                        add Transform("gui/Kaito.png", fit="contain", xalign=0.5, yalign=0.5, xsize=418, ysize=748, xoffset=-3, matrixcolor=TintMatrix("#7fb8ff")) at profile_glow_pulse
                        add Transform("gui/Kaito.png", fit="contain", xalign=0.5, yalign=0.5, xsize=418, ysize=748, xoffset=3, matrixcolor=TintMatrix("#7fb8ff")) at profile_glow_pulse
                        add Transform("gui/Kaito.png", fit="contain", xalign=0.5, yalign=0.5, xsize=418, ysize=748, yoffset=-3, matrixcolor=TintMatrix("#7fb8ff")) at profile_glow_pulse
                        add Transform("gui/Kaito.png", fit="contain", xalign=0.5, yalign=0.5, xsize=418, ysize=748, yoffset=3, matrixcolor=TintMatrix("#7fb8ff")) at profile_glow_pulse

                    add Transform("gui/Kaito.png", fit="contain", xalign=0.5, yalign=0.5, xsize=418, ysize=748):
                        alpha (1.0 if (mc_gender == "male" or male_hovered) else 0.62)
                        zoom (1.00 if male_hovered else 0.96)
                elif renpy.loadable("gui/mc_male.png"):
                    if mc_gender == "male":
                        add Transform("gui/mc_male.png", fit="contain", xalign=0.5, yalign=1.0, xsize=390, ysize=730, xoffset=-3, matrixcolor=TintMatrix("#7fb8ff")) at profile_glow_pulse
                        add Transform("gui/mc_male.png", fit="contain", xalign=0.5, yalign=1.0, xsize=390, ysize=730, xoffset=3, matrixcolor=TintMatrix("#7fb8ff")) at profile_glow_pulse
                        add Transform("gui/mc_male.png", fit="contain", xalign=0.5, yalign=1.0, xsize=390, ysize=730, yoffset=-3, matrixcolor=TintMatrix("#7fb8ff")) at profile_glow_pulse
                        add Transform("gui/mc_male.png", fit="contain", xalign=0.5, yalign=1.0, xsize=390, ysize=730, yoffset=3, matrixcolor=TintMatrix("#7fb8ff")) at profile_glow_pulse

                    add Transform("gui/mc_male.png", fit="contain", xalign=0.5, yalign=1.0, xsize=390, ysize=730):
                        alpha (1.0 if (mc_gender == "male" or male_hovered) else 0.62)
                        zoom (1.03 if male_hovered else 1.0)
                else:
                    text "MALE" at Transform(alpha=(1.0 if (mc_gender == "male" or male_hovered) else 0.45)):
                        style "ui_btn_text"
                        xalign 0.5
                        yalign 0.5
                        size 52
                        color "#d9ecff"
                        outlines [ (2, "#203f67", 0, 0) ]

            vbox:
                xalign 0.5
                yalign 1.0
                yoffset 132
                spacing 2

                text "[_male_display_name] [mc_last_name]":
                    font "fonts/cinzel/Cinzel-Bold.otf"
                    size 52
                    xalign 0.5
                    at Transform(alpha=(1.0 if mc_gender == "male" else 0.72))
                    color ("#ffd77f" if (mc_gender == "male" or male_hovered) else "#ced8e6")
                    outlines [(2, "#11161fbb", 0, 0)]

                text "He / Him":
                    font "fonts/cinzel/Cinzel-Bold.otf"
                    size 42
                    xalign 0.5
                    at Transform(alpha=(1.0 if mc_gender == "male" else 0.66))
                    color ("#ffe59a" if (mc_gender == "male" or male_hovered) else "#cbd5e3")
                    outlines [(1, "#11161fbb", 0, 0)]


transform profile_glow_pulse:
    alpha 0.14
    linear 0.9 alpha 0.34
    linear 0.9 alpha 0.14
    repeat

transform profile_sparkle_rise_a:
    alpha 0.0
    pause 0.0
    linear 0.22 alpha 0.75
    linear 1.2 yoffset -28 alpha 0.0
    pause 0.8
    repeat

transform profile_sparkle_rise_b:
    alpha 0.0
    pause 0.45
    linear 0.24 alpha 0.72
    linear 1.3 yoffset -34 alpha 0.0
    pause 0.7
    repeat

transform profile_sparkle_rise_c:
    alpha 0.0
    pause 0.82
    linear 0.24 alpha 0.68
    linear 1.15 yoffset -24 alpha 0.0
    pause 0.9
    repeat

label start:
    window hide
    scene black
    with dissolve
    $ mc_last_name = "Kuzunoha"

    $ _story_video = resolve_story_video(intro_story_video)
    if _story_video:
        $ renpy.movie_cutscene(_story_video)
    else:
        scene black
        centered "Video not found: [intro_story_video]"
    call screen intro_press_any_to_continue
    if not mc_profile_done:
        call screen mc_profile_setup
    if run_ui_test_demo and renpy.has_label("ui_test_demo"):
        call ui_test_demo

    if mc_gender == "female":
        call female_route_start
    else:
        call male_route_start

    return
