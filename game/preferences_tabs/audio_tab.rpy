# preferences_tabs/audio_tab.rpy

screen preferences_tab_audio():
    $ tab_colors = pref_tab_colors("audio")
    $ all_muted = is_all_muted()
    $ output_status = "AUDIO MUTED" if all_muted else "AUDIO LIVE"

    fixed:
        xsize 1450
        ysize 740

        hbox:
            spacing 22

            vbox:
                spacing 18

                use pref_hub_panel("MASTER MIXER", "Overall mute and per-channel balance.", 930, 390, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 14

                        hbox:
                            spacing 14
                            fixed:
                                xsize 220
                                ysize 52
                                text pref_L("pref_label_mute_all") style "pref_setting_label" yalign 0.5
                            use pref_small_button("pref_button_muted", Function(set_all_mute, True), selected=all_muted, xsize=180, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_button_not_muted", Function(set_all_mute, False), selected=(not all_muted), xsize=210, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                        if config.has_music:
                            use pref_hub_slider_row("pref_label_music_volume", Preference("music volume"), variant="fill", label_width=220, slider_width=420, dimmed=all_muted)

                        if config.has_sound:
                            use pref_hub_slider_row("pref_label_sfx_volume", Preference("sound volume"), variant="fill", label_width=220, slider_width=420, dimmed=all_muted)

                        if config.has_voice:
                            use pref_hub_slider_row("pref_label_voice_volume", Preference("voice volume"), variant="fill", label_width=220, slider_width=420, dimmed=all_muted)

                use pref_hub_panel("SOUNDSTAGE", "How each channel shapes the scene.", 930, 150, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 8
                        text "Music shapes ambience, SFX adds feedback, and voice keeps spoken scenes clear." style "pref_label_text"
                        text "Your mix carries across menus and story scenes." style "pref_label_text"

            vbox:
                spacing 18

                use pref_hub_panel("OUTPUT STATE", xsize=498, ysize=176, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 10
                        text output_status style "pref_section_title" color tab_colors["accent"]
                        text "Mute All controls the full mixer from the main section on the left." style "pref_label_text"
                        text "The sliders stay saved even while output is muted." style "pref_label_text"

                use pref_hub_panel("CHANNEL GUIDE", xsize=498, ysize=228, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 10

                        if config.has_music:
                            text "Music Volume" style "pref_setting_label" color tab_colors["accent"]
                            text "Background tracks and ambient layers." style "pref_label_text"

                        if config.has_sound:
                            text "SFX Volume" style "pref_setting_label" color tab_colors["accent"]
                            text "Interface cues and world interactions." style "pref_label_text"

                        if config.has_voice:
                            text "Voice Volume" style "pref_setting_label" color tab_colors["accent"]
                            text "Spoken dialogue playback." style "pref_label_text"

                use pref_hub_panel("SAVED LEVELS", xsize=498, ysize=104, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 6
                        hbox:
                            xfill True
                            text "Music" style "pref_label_text"
                            text "[pref_audio_percent('music_volume')]" style "pref_label_text" xalign 1.0
                        hbox:
                            xfill True
                            text "SFX" style "pref_label_text"
                            text "[pref_audio_percent('sound_volume')]" style "pref_label_text" xalign 1.0
                        hbox:
                            xfill True
                            text "Voice" style "pref_label_text"
                            text "[pref_audio_percent('voice_volume')]" style "pref_label_text" xalign 1.0
