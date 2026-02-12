# lang/en_us.rpy
# English (US) UI strings.

init -1 python:
    register_ui_lang("en_us", {
        "lang_name": "English (US)",

        # Tabs.
        "pref_tab_display": "DISPLAY",
        "pref_tab_audio": "AUDIO",
        "pref_tab_controls": "CONTROLS",
        "pref_tab_access": "ACCESS",
        "pref_tip_tab_display": "Screen mode, skip rules, and speed settings.",
        "pref_tip_tab_audio": "Mute and adjust audio levels.",
        "pref_tip_tab_controls": "Gamepad calibration and button bindings.",
        "pref_tip_tab_access": "Skip settings and transition toggles.",

        # Audio.
        "pref_label_mute_all": "MUTE ALL",
        "pref_button_muted": "MUTED",
        "pref_button_not_muted": "NOT MUTED",
        "pref_tip_muted": "Mute music, SFX, and voice.",
        "pref_tip_not_muted": "Unmute all audio channels.",
        "pref_label_music_volume": "MUSIC VOLUME",
        "pref_label_sfx_volume": "SFX VOLUME",
        "pref_label_voice_volume": "VOICE VOLUME",
        "pref_tip_music_volume": "Adjust the music channel volume.",
        "pref_tip_sfx_volume": "Adjust the sound effects volume.",
        "pref_tip_voice_volume": "Adjust the voice volume.",

        # Display.
        "pref_label_display": "DISPLAY",
        "pref_button_window": "WINDOW",
        "pref_button_fullscreen": "FULLSCREEN",
        "pref_tip_window": "Run in windowed mode.",
        "pref_tip_fullscreen": "Use fullscreen display.",
        "pref_label_skip_unseen": "SKIP UNSEEN TEXT",
        "pref_tip_skip_unseen_on": "Allow skipping text you have not read.",
        "pref_tip_skip_unseen_off": "Only skip previously seen text.",
        "pref_label_skip_after_choices": "SKIP AFTER CHOICES",
        "pref_tip_skip_after_choices_on": "Keep skipping after choices.",
        "pref_tip_skip_after_choices_off": "Stop skipping at choices.",
        "pref_label_text_speed": "TEXT SPEED",
        "pref_label_min": "MIN",
        "pref_label_max": "MAX",
        "pref_label_auto_forward": "AUTO-FORWARD DELAY",
        "pref_tip_text_speed": "Change how fast text appears.",
        "pref_tip_auto_forward": "Change the auto-forward delay.",

        # Access.
        "pref_label_skip_mode": "SKIP MODE",
        "pref_label_seen": "SEEN",
        "pref_label_all": "ALL",
        "pref_label_skip_transitions": "SKIP TRANSITIONS",
        "pref_tip_transitions_on": "Skip screen transitions.",
        "pref_tip_transitions_off": "Play screen transitions.",
        "pref_tip_font_size": "Scale the size of menu and dialogue text.",
        "pref_tip_line_spacing": "Adjust spacing between lines of text.",
        "pref_tip_self_voicing_volume": "Reduce game volume while self-voicing is active.",

        # Controls.
        "pref_button_calibrate_gamepad": "CALIBRATE GAMEPAD BUTTONS",
        "pref_tip_calibrate_gamepad": "Start the gamepad calibration flow.",
        "pref_button_change_icon_set": "CHANGE ICON SET",
        "pref_tip_change_icon_set": "Cycle the controller icon layout.",
        "pref_button_add_binding": "+",
        "pref_tip_add_binding": "Add a new binding for this action.",
        "pref_tip_remove_binding": "Remove this binding.",

        # Footer.
        "pref_button_main_menu": "MAIN MENU",
        "pref_tip_main_menu": "Return to the main menu.",
        "pref_button_back": "BACK",
        "pref_tip_back": "Return to the previous screen.",
        "pref_button_default": "DEFAULT",
        "pref_tip_default": "Reset settings to defaults.",

        # Shared toggles.
        "pref_button_on": "ON",
        "pref_button_off": "OFF",
        "pref_tip_generic_on": "Enable this option.",
        "pref_tip_generic_off": "Disable this option.",
    })
