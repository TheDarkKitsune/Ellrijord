# preferences_tabs/access_tab.rpy

screen preferences_tab_access(pref_access_yadj):
    $ left_x = 60
    $ on_x = 650
    $ off_x = 980
    $ min_x = 650
    $ slider_x = 730
    $ max_x = 1280

    side "c r":
        viewport:
            id "pref_access_vp"
            xysize (1480, 640)
            mousewheel True
            draggable True
            yadjustment pref_access_yadj
            has vbox
            spacing 36

            fixed:
                xsize 1480
                ysize 90
                text "FONT OVERRIDE" style "pref_label":
                    xpos left_x
                    ypos 10
                fixed:
                    xpos on_x
                    ypos 0
                    use pref_small_button("DEFAULT", Preference("font transform", None), selected=(getattr(preferences, "font_transform", None) is None))
                fixed:
                    xpos off_x
                    ypos 0
                    use pref_small_button("DEJAVU SANS", Preference("font transform", "dejavusans"), selected=(getattr(preferences, "font_transform", None) == "dejavusans"))

            fixed:
                xsize 1480
                ysize 80
                fixed:
                    xpos on_x
                    ypos 0
                    use pref_small_button("OPENDYSLEXIC", Preference("font transform", "opendyslexic"), selected=(getattr(preferences, "font_transform", None) == "opendyslexic"))

            fixed:
                xsize 1480
                ysize 90
                text "TEXT SIZE SCALING" style "pref_label":
                    xpos left_x
                    ypos 10
                text "MIN" style "pref_label":
                    xpos min_x
                    ypos 10
                use ui_slider(Preference("font size"), style_name="pref_bar", xpos=slider_x, ypos=0, tooltip=L("pref_tip_font_size"))
                text "MAX" style "pref_label":
                    xpos max_x
                    ypos 10

            fixed:
                xsize 1480
                ysize 90
                text "LINE SPACE SCALING" style "pref_label":
                    xpos left_x
                    ypos 10
                text "MIN" style "pref_label":
                    xpos min_x
                    ypos 10
                use ui_slider(Preference("font line spacing"), style_name="pref_bar", xpos=slider_x, ypos=0, tooltip=L("pref_tip_line_spacing"))
                text "MAX" style "pref_label":
                    xpos max_x
                    ypos 10

            fixed:
                xsize 1480
                ysize 90
                text "HIGH CONTRAST TEXT" style "pref_label":
                    xpos left_x
                    ypos 10
                fixed:
                    xpos on_x
                    ypos 0
                    use pref_small_button("ON", Preference("high contrast text", "enable"), selected=getattr(preferences, "high_contrast_text", False))
                fixed:
                    xpos off_x
                    ypos 0
                    use pref_small_button("OFF", Preference("high contrast text", "disable"), selected=not getattr(preferences, "high_contrast_text", False))

            fixed:
                xsize 1480
                ysize 90
                text "SELF-VOICING" style "pref_label":
                    xpos left_x
                    ypos 10
                fixed:
                    xpos on_x
                    ypos 0
                    use pref_small_button("TEXT-TO-SPEECH", Preference("self voicing", "enable"), selected=getattr(preferences, "self_voicing", False))
                fixed:
                    xpos off_x
                    ypos 0
                    use pref_small_button("CLIPBOARD", Preference("clipboard voicing", "enable"), selected=getattr(preferences, "clipboard_voicing", False))

            fixed:
                xsize 1480
                ysize 90
                text "DEBUG" style "pref_label":
                    xpos left_x
                    ypos 10
                fixed:
                    xpos on_x
                    ypos 0
                    use pref_small_button("ON", Preference("debug voicing", "enable"), selected=getattr(preferences, "debug_voicing", False))
                fixed:
                    xpos off_x
                    ypos 0
                    use pref_small_button("OFF", Preference("debug voicing", "disable"), selected=not getattr(preferences, "debug_voicing", False))

            fixed:
                xsize 1480
                ysize 90
                text "VOICE VOLUME" style "pref_label":
                    xpos left_x
                    ypos 10
                text "MIN" style "pref_label":
                    xpos min_x
                    ypos 10
                use ui_slider(Preference("voice volume"), style_name="pref_bar", xpos=slider_x, ypos=0, tooltip=L("pref_tip_voice_volume"))
                text "MAX" style "pref_label":
                    xpos max_x
                    ypos 10

            fixed:
                xsize 1480
                ysize 90
                text "SELF-VOICING VOLUME DROP" style "pref_label":
                    xpos left_x
                    ypos 10
                text "MIN" style "pref_label":
                    xpos min_x
                    ypos 10
                use ui_slider(Preference("self voicing volume drop"), style_name="pref_bar", xpos=slider_x, ypos=0, tooltip=L("pref_tip_self_voicing_volume"))
                text "MAX" style "pref_label":
                    xpos max_x
                    ypos 10

        vbar value YScrollValue("pref_access_vp") keyboard_focus False
