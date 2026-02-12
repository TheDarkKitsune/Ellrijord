# preferences_tabs/audio_tab.rpy

screen preferences_tab_audio():
    default pref_audio_yadj = ui.adjustment()

    fixed:
        xsize 1480
        ysize 640

        $ left_w = 360
        $ right_w = 1060
        $ row_h = 86
        $ slider_row_h = 96
        $ row_gap = 20

        side "c r":
            xpos 10
            ypos 10
            xysize (1460, 620)

            viewport:
                id "pref_audio_vp"
                xysize (1460, 620)
                mousewheel True
                draggable True
                yadjustment pref_audio_yadj

                vbox:
                    spacing row_gap

                    hbox:
                        spacing 28
                        fixed:
                            xsize left_w
                            ysize row_h
                            text L("pref_label_mute_all") style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize right_w
                            ysize row_h
                            hbox:
                                xalign 1.0
                                spacing 12
                                use pref_small_button("pref_button_muted", Function(set_all_mute, True), selected=is_all_muted(), tooltip_key="pref_tip_muted")
                                use pref_small_button("pref_button_not_muted", Function(set_all_mute, False), selected=not is_all_muted(), tooltip_key="pref_tip_not_muted")

                    if config.has_music:
                        hbox:
                            spacing 28
                            fixed:
                                xsize left_w
                                ysize row_h
                                text L("pref_label_music_volume") style "pref_setting_label" yalign 0.5
                            fixed:
                                xsize right_w
                                ysize row_h
                                use ui_slider(Preference("music volume"), variant="fill", xpos=(right_w - 700), xsize=700, ysize=36, tooltip=L("pref_tip_music_volume"))

                    if config.has_sound:
                        hbox:
                            spacing 28
                            fixed:
                                xsize left_w
                                ysize row_h
                                text L("pref_label_sfx_volume") style "pref_setting_label" yalign 0.5
                            fixed:
                                xsize right_w
                                ysize row_h
                                use ui_slider(Preference("sound volume"), style_name="pref_bar", xpos=(right_w - 700), xsize=700, ysize=36, tooltip=L("pref_tip_sfx_volume"))

                    if config.has_voice:
                        hbox:
                            spacing 28
                            fixed:
                                xsize left_w
                                ysize row_h
                                text L("pref_label_voice_volume") style "pref_setting_label" yalign 0.5
                            fixed:
                                xsize right_w
                                ysize row_h
                                use ui_slider(Preference("voice volume"), style_name="pref_bar", xpos=(right_w - 700), xsize=700, ysize=36, tooltip=L("pref_tip_voice_volume"))

            vbar value YScrollValue("pref_audio_vp") keyboard_focus False
