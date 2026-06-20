# preferences_tabs/audio_tab.rpy

screen preferences_tab_audio():
    $ tab_colors = pref_ui_tab_colors("audio")
    $ all_muted = is_all_muted()
    $ output_status = "AUDIO MUTED" if all_muted else "AUDIO LIVE"
    $ ducking_value = pref_quantized_adjustment("self voicing volume drop", "self_voicing_volume_drop", default=0.0)

    fixed:
        xsize 1450
        ysize 740

        hbox:
            spacing 22

            vbox:
                spacing 18

                use pref_hub_panel("MASTER MIXER", "Overall mute and per-channel balance.", 930, 392, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
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
                            use pref_hub_slider_row("pref_label_music_volume", pref_quantized_adjustment("music volume", "music_volume"), variant="fill", label_width=220, slider_width=420, dimmed=all_muted, show_percent=True)

                        use pref_hub_slider_row("AMBIENCE VOLUME", pref_ambient_adjustment(), variant="fill", label_width=220, slider_width=420, dimmed=all_muted, show_percent=True)

                        if config.has_sound:
                            use pref_hub_slider_row("pref_label_sfx_volume", pref_quantized_adjustment("sound volume", "sound_volume"), variant="fill", label_width=220, slider_width=420, dimmed=all_muted, show_percent=True)

                        if config.has_voice:
                            use pref_hub_slider_row("pref_label_voice_volume", pref_quantized_adjustment("voice volume", "voice_volume"), variant="fill", label_width=220, slider_width=420, dimmed=all_muted, show_percent=True)

                use pref_hub_panel("VOICE BALANCE", "Keep spoken dialogue clear during scenes.", 930, 222, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 12

                        hbox:
                            spacing 14

                            fixed:
                                xsize 220
                                ysize 52
                                text "VOICE DUCKING" style "pref_setting_label" yalign 0.5

                            use pref_small_button("pref_button_on", Function(ducking_value.change, ducking_value.value if ducking_value.value > 0.0 else 0.8), selected=(ducking_value.value > 0.0), xsize=180, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_button_off", Function(ducking_value.change, 0.0), selected=(ducking_value.value <= 0.0), xsize=180, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                        use pref_hub_slider_row("DUCKING STRENGTH", ducking_value, style_name="pref_bar", label_width=220, slider_width=420, dimmed=(ducking_value.value <= 0.0), show_percent=True)

                        text "Lowers background audio while voiced lines are playing." style "pref_label_text"

            vbox:
                spacing 18

                use pref_hub_panel("OUTPUT STATE", xsize=498, ysize=196, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 10
                        text output_status style "pref_section_title" color tab_colors["accent"]
                        text "Mute All controls the full mixer from the main section." style "pref_label_text"
                        text "Saved slider levels remain unchanged while muted." style "pref_label_text"

                use pref_hub_panel("PLAYBACK OPTIONS", xsize=498, ysize=294, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 12

                        hbox:
                            xfill True
                            fixed:
                                xsize 286
                                ysize 44
                                text "MUTE IN BACKGROUND" style "pref_setting_label" yalign 0.5
                            use pref_small_button(pref_bool_text(not pref_audio_bool("audio_when_unfocused", True)), Function(toggle_pref_audio_bool, "audio_when_unfocused", True), selected=(not pref_audio_bool("audio_when_unfocused", True)), xsize=120, ysize=42, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                        hbox:
                            xfill True
                            fixed:
                                xsize 286
                                ysize 44
                                text "PAUSE AUDIO ON MINIMISE" style "pref_setting_label" yalign 0.5
                            use pref_small_button(pref_bool_text(not pref_audio_bool("audio_when_minimized", True)), Function(toggle_pref_audio_bool, "audio_when_minimized", True), selected=(not pref_audio_bool("audio_when_minimized", True)), xsize=120, ysize=42, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                        hbox:
                            xfill True
                            fixed:
                                xsize 286
                                ysize 44
                                text "LOOP MUSIC" style "pref_setting_label" yalign 0.5
                            use pref_small_button(pref_bool_text(pref_loop_music_enabled()), Function(toggle_pref_loop_music), selected=pref_loop_music_enabled(), xsize=120, ysize=42, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                        text "These settings affect playback when the game is inactive or between scenes." style "pref_label_text"

                use pref_hub_panel("SECTION NOTES", xsize=498, ysize=184, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 10
                        text "Volume changes apply immediately." style "pref_label_text"
                        text "Voice ducking helps speech stand out in voiced scenes." style "pref_label_text"
                        text "Use Default to restore the original mix." style "pref_label_text"
