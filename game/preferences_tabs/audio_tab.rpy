# preferences_tabs/audio_tab.rpy

screen preferences_tab_audio():
    vbox:
        spacing 26

        hbox:
            spacing 18
            text L("pref_label_mute_all") style "pref_label"
            use pref_small_button("pref_button_muted", Function(set_all_mute, True), selected=is_all_muted(), tooltip_key="pref_tip_muted")
            use pref_small_button("pref_button_not_muted", Function(set_all_mute, False), selected=not is_all_muted(), tooltip_key="pref_tip_not_muted")

        if config.has_music:
            vbox:
                spacing 8
                text L("pref_label_music_volume") style "pref_label"
                use ui_slider(Preference("music volume"), style_name="pref_bar", tooltip=L("pref_tip_music_volume"))

        if config.has_sound:
            vbox:
                spacing 8
                text L("pref_label_sfx_volume") style "pref_label"
                use ui_slider(Preference("sound volume"), style_name="pref_bar", tooltip=L("pref_tip_sfx_volume"))

        if config.has_voice:
            vbox:
                spacing 8
                text L("pref_label_voice_volume") style "pref_label"
                use ui_slider(Preference("voice volume"), style_name="pref_bar", tooltip=L("pref_tip_voice_volume"))
