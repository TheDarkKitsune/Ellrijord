# preferences_tabs/access_tab.rpy

screen preferences_tab_access(pref_access_yadj):
    fixed:
        xsize 1480
        ysize 640

        $ left_w = 360
        $ right_w = 1060
        $ row_h = 86
        $ slider_row_h = 96
        $ slider_h = 36
        $ row_gap = 20

        side "c r":
            xpos 10
            ypos 10
            xysize (1460, 620)

            controller_viewport:
                id "pref_access_vp"
                xysize (1460, 620)
                mousewheel True
                draggable True
                arrowkeys "not sticks"
                focus_scroll True
                shortcuts True
                yadjustment pref_access_yadj

                vbox:
                    spacing row_gap

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text "FONT OVERRIDE" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("DEFAULT", Preference("font transform", None), selected=(getattr(preferences, "font_transform", None) is None))
                                use pref_small_button("DEJAVU SANS", Preference("font transform", "dejavusans"), selected=(getattr(preferences, "font_transform", None) == "dejavusans"))

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("OPENDYSLEXIC", Preference("font transform", "opendyslexic"), selected=(getattr(preferences, "font_transform", None) == "opendyslexic"))

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text "TEXT SIZE SCALING" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize slider_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text "MIN" style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 700
                                    ysize slider_row_h
                                    use ui_slider(Preference("font size"), style_name="pref_bar", xpos=0, ypos=((slider_row_h - slider_h) // 2), xsize=700, ysize=slider_h, tooltip=L("pref_tip_font_size"))
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text "MAX" style "pref_setting_label" xalign 0.0 yalign 0.5

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text "LINE SPACE SCALING" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize slider_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text "MIN" style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 700
                                    ysize slider_row_h
                                    use ui_slider(Preference("font line spacing"), style_name="pref_bar", xpos=0, ypos=((slider_row_h - slider_h) // 2), xsize=700, ysize=slider_h, tooltip=L("pref_tip_line_spacing"))
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text "MAX" style "pref_setting_label" xalign 0.0 yalign 0.5

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text "HIGH CONTRAST TEXT" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("ON", Preference("high contrast text", "enable"), selected=getattr(preferences, "high_contrast_text", False))
                                use pref_small_button("OFF", Preference("high contrast text", "disable"), selected=not getattr(preferences, "high_contrast_text", False))

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text "SELF-VOICING" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("TEXT-TO-SPEECH", Preference("self voicing", "enable"), selected=getattr(preferences, "self_voicing", False))
                                use pref_small_button("CLIPBOARD", Preference("clipboard voicing", "enable"), selected=getattr(preferences, "clipboard_voicing", False))

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text "DEBUG" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("ON", Preference("debug voicing", "enable"), selected=getattr(preferences, "debug_voicing", False))
                                use pref_small_button("OFF", Preference("debug voicing", "disable"), selected=not getattr(preferences, "debug_voicing", False))

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text "VOICE VOLUME" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize slider_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text "MIN" style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 700
                                    ysize slider_row_h
                                    use ui_slider(Preference("voice volume"), style_name="pref_bar", xpos=0, ypos=((slider_row_h - slider_h) // 2), xsize=700, ysize=slider_h, tooltip=L("pref_tip_voice_volume"))
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text "MAX" style "pref_setting_label" xalign 0.0 yalign 0.5

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text "SELF-VOICING VOLUME DROP" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize slider_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text "MIN" style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 700
                                    ysize slider_row_h
                                    use ui_slider(Preference("self voicing volume drop"), style_name="pref_bar", xpos=0, ypos=((slider_row_h - slider_h) // 2), xsize=700, ysize=slider_h, tooltip=L("pref_tip_self_voicing_volume"))
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text "MAX" style "pref_setting_label" xalign 0.0 yalign 0.5

            use ui_vscrollbar_for("pref_access_vp")
