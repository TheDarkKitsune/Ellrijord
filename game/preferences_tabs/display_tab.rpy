# preferences_tabs/display_tab.rpy

screen preferences_tab_display():
    default pref_display_yadj = ui.adjustment()

    fixed:
        xsize 1480
        ysize 640

        $ left_w = 360
        $ right_w = 1060
        $ row_h = 78
        $ slider_row_h = 96
        $ row_gap = 20
        $ slider_block_w = 760

        side "c r":
            xysize (1460, 620)

            viewport:
                id "pref_display_vp"
                xysize (1460, 620)
                mousewheel True
                draggable True
                yadjustment pref_display_yadj

                hbox:
                    spacing 28

                    vbox:
                        xsize left_w
                        spacing row_gap

                        fixed:
                            xsize left_w
                            ysize row_h
                            text L("pref_label_display") style "pref_setting_label" yalign 0.5

                        fixed:
                            xsize left_w
                            ysize row_h
                            text L("pref_label_skip_unseen") style "pref_setting_label" yalign 0.5

                        fixed:
                            xsize left_w
                            ysize row_h
                            text L("pref_label_skip_after_choices") style "pref_setting_label" yalign 0.5

                        fixed:
                            xsize left_w
                            ysize row_h
                            text "LANGUAGE" style "pref_setting_label" yalign 0.5

                        fixed:
                            xsize left_w
                            ysize slider_row_h
                            text L("pref_label_text_speed") style "pref_setting_label" yalign 0.5

                        fixed:
                            xsize left_w
                            ysize slider_row_h
                            text L("pref_label_auto_forward") style "pref_setting_label" yalign 0.5

                    vbox:
                        xsize right_w
                        spacing row_gap

                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("pref_button_window", Preference("display", "window"), selected=not preferences.fullscreen, tooltip_key="pref_tip_window")
                                use pref_small_button("pref_button_fullscreen", Preference("display", "fullscreen"), selected=preferences.fullscreen, tooltip_key="pref_tip_fullscreen")

                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("pref_button_on", SetField(preferences, "skip_unseen", True), selected=preferences.skip_unseen, tooltip_key="pref_tip_skip_unseen_on")
                                use pref_small_button("pref_button_off", SetField(preferences, "skip_unseen", False), selected=not preferences.skip_unseen, tooltip_key="pref_tip_skip_unseen_off")

                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("pref_button_on", SetField(preferences, "skip_after_choices", True), selected=preferences.skip_after_choices, tooltip_key="pref_tip_skip_after_choices_on")
                                use pref_small_button("pref_button_off", SetField(preferences, "skip_after_choices", False), selected=not preferences.skip_after_choices, tooltip_key="pref_tip_skip_after_choices_off")

                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("ENGLISH (US)", Function(set_ui_lang, "en_us"), selected=get_ui_lang() == "en_us")
                                use pref_small_button("ESPANOL (ES)", Function(set_ui_lang, "es_es"), selected=get_ui_lang() == "es_es")

                        fixed:
                            xsize right_w
                            ysize slider_row_h
                            hbox:
                                xpos (right_w - slider_block_w)
                                spacing 14
                                fixed:
                                    xsize 100
                                    ysize slider_row_h
                                    text L("pref_label_min") style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 560
                                    ysize slider_row_h
                                    use ui_slider(Preference("text speed"), style_name="pref_bar", xpos=0, xsize=560, ysize=88, tooltip=L("pref_tip_text_speed"))
                                fixed:
                                    xsize 72
                                    ysize slider_row_h
                                    text L("pref_label_max") style "pref_setting_label" xalign 1.0 yalign 0.5

                        fixed:
                            xsize right_w
                            ysize slider_row_h
                            hbox:
                                xpos (right_w - slider_block_w)
                                spacing 14
                                fixed:
                                    xsize 100
                                    ysize slider_row_h
                                    text L("pref_label_min") style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 560
                                    ysize slider_row_h
                                    use ui_slider(Preference("auto-forward time"), style_name="pref_bar", xpos=0, xsize=560, ysize=88, tooltip=L("pref_tip_auto_forward"))
                                fixed:
                                    xsize 72
                                    ysize slider_row_h
                                    text L("pref_label_max") style "pref_setting_label" xalign 1.0 yalign 0.5

            vbar value YScrollValue("pref_display_vp") keyboard_focus False
