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
                            text L("pref_label_font_override") style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("pref_button_default_font", Preference("font transform", None), selected=(getattr(preferences, "font_transform", None) is None), tooltip_key="pref_tip_default_font")
                                use pref_small_button("pref_button_dejavu_sans", Preference("font transform", "dejavusans"), selected=(getattr(preferences, "font_transform", None) == "dejavusans"), tooltip_key="pref_tip_dejavu_sans")

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
                                use pref_small_button("pref_button_opendyslexic", Preference("font transform", "opendyslexic"), selected=(getattr(preferences, "font_transform", None) == "opendyslexic"), tooltip_key="pref_tip_opendyslexic")

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text L("pref_label_text_size_scaling") style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize slider_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text L("pref_label_min") style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 700
                                    ysize slider_row_h
                                    use ui_slider(Preference("font size"), style_name="pref_bar", xpos=0, ypos=((slider_row_h - slider_h) // 2), xsize=700, ysize=slider_h, tooltip=L("pref_tip_font_size"))
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text L("pref_label_max") style "pref_setting_label" xalign 0.0 yalign 0.5

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text L("pref_label_line_space_scaling") style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize slider_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text L("pref_label_min") style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 700
                                    ysize slider_row_h
                                    use ui_slider(Preference("font line spacing"), style_name="pref_bar", xpos=0, ypos=((slider_row_h - slider_h) // 2), xsize=700, ysize=slider_h, tooltip=L("pref_tip_line_spacing"))
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text L("pref_label_max") style "pref_setting_label" xalign 0.0 yalign 0.5

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text L("pref_label_high_contrast_text") style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("pref_button_on", Preference("high contrast text", "enable"), selected=getattr(preferences, "high_contrast_text", False), tooltip_key="pref_tip_high_contrast_on")
                                use pref_small_button("pref_button_off", Preference("high contrast text", "disable"), selected=not getattr(preferences, "high_contrast_text", False), tooltip_key="pref_tip_high_contrast_off")

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text L("pref_label_self_voicing") style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("pref_button_text_to_speech", Preference("self voicing", "enable"), selected=getattr(preferences, "self_voicing", False), tooltip_key="pref_tip_text_to_speech")
                                use pref_small_button("pref_button_clipboard", Preference("clipboard voicing", "enable"), selected=getattr(preferences, "clipboard_voicing", False), tooltip_key="pref_tip_clipboard_voicing")

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text L("pref_label_debug") style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("pref_button_on", Preference("debug voicing", "enable"), selected=getattr(preferences, "debug_voicing", False), tooltip_key="pref_tip_debug_on")
                                use pref_small_button("pref_button_off", Preference("debug voicing", "disable"), selected=not getattr(preferences, "debug_voicing", False), tooltip_key="pref_tip_debug_off")

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text L("pref_label_voice_volume") style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize slider_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text L("pref_label_min") style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 700
                                    ysize slider_row_h
                                    use ui_slider(Preference("voice volume"), style_name="pref_bar", xpos=0, ypos=((slider_row_h - slider_h) // 2), xsize=700, ysize=slider_h, tooltip=L("pref_tip_voice_volume"))
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text L("pref_label_max") style "pref_setting_label" xalign 0.0 yalign 0.5

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text L("pref_label_self_voicing_volume_drop") style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize slider_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text L("pref_label_min") style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 700
                                    ysize slider_row_h
                                    use ui_slider(Preference("self voicing volume drop"), style_name="pref_bar", xpos=0, ypos=((slider_row_h - slider_h) // 2), xsize=700, ysize=slider_h, tooltip=L("pref_tip_self_voicing_volume"))
                                fixed:
                                    xsize 60
                                    ysize slider_row_h
                                    text L("pref_label_max") style "pref_setting_label" xalign 0.0 yalign 0.5

            use ui_vscrollbar_for("pref_access_vp")
