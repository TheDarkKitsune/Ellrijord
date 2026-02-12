# preferences_tabs/display_tab.rpy

screen preferences_tab_display():
    fixed:
        xsize 1480
        ysize 640

        $ left_x = 80
        $ on_x = 620
        $ off_x = 860
        $ min_x = 620
        $ slider_x = 700
        $ max_x = 1280

        $ row_y = 30
        text L("pref_label_display") style "pref_label":
            xpos left_x
            ypos row_y
        fixed:
            xpos on_x
            ypos (row_y - 8)
            use pref_small_button("pref_button_window", Preference("display", "window"), selected=not preferences.fullscreen, tooltip_key="pref_tip_window")
        fixed:
            xpos off_x
            ypos (row_y - 8)
            use pref_small_button("pref_button_fullscreen", Preference("display", "fullscreen"), selected=preferences.fullscreen, tooltip_key="pref_tip_fullscreen")

        $ row_y = 150
        text L("pref_label_skip_unseen") style "pref_label":
            xpos left_x
            ypos row_y
        fixed:
            xpos on_x
            ypos (row_y - 8)
            use pref_small_button("pref_button_on", SetField(preferences, "skip_unseen", True), selected=preferences.skip_unseen, tooltip_key="pref_tip_skip_unseen_on")
        fixed:
            xpos off_x
            ypos (row_y - 8)
            use pref_small_button("pref_button_off", SetField(preferences, "skip_unseen", False), selected=not preferences.skip_unseen, tooltip_key="pref_tip_skip_unseen_off")

        $ row_y = 270
        text L("pref_label_skip_after_choices") style "pref_label":
            xpos left_x
            ypos row_y
        fixed:
            xpos on_x
            ypos (row_y - 8)
            use pref_small_button("pref_button_on", SetField(preferences, "skip_after_choices", True), selected=preferences.skip_after_choices, tooltip_key="pref_tip_skip_after_choices_on")
        fixed:
            xpos off_x
            ypos (row_y - 8)
            use pref_small_button("pref_button_off", SetField(preferences, "skip_after_choices", False), selected=not preferences.skip_after_choices, tooltip_key="pref_tip_skip_after_choices_off")

        $ row_y = 340
        text "LANGUAGE" style "pref_label":
            xpos left_x
            ypos row_y
        text get_ui_lang_label(get_ui_lang()) style "pref_label":
            xpos min_x
            ypos row_y
        fixed:
            xpos on_x
            ypos (row_y - 8)
            use pref_small_button("ENGLISH (US)", Function(set_ui_lang, "en_us"), selected=get_ui_lang() == "en_us")
        fixed:
            xpos off_x
            ypos (row_y - 8)
            use pref_small_button("ESPANOL (ES)", Function(set_ui_lang, "es_es"), selected=get_ui_lang() == "es_es")

        $ row_y = 410
        text L("pref_label_text_speed") style "pref_label":
            xpos left_x
            ypos row_y
        text L("pref_label_min") style "pref_label":
            xpos min_x
            ypos row_y
        use ui_slider(Preference("text speed"), style_name="pref_bar", xpos=slider_x, ypos=(row_y - 8), tooltip=L("pref_tip_text_speed"))
        text L("pref_label_max") style "pref_label":
            xpos max_x
            ypos row_y

        $ row_y = 540
        text L("pref_label_auto_forward") style "pref_label":
            xpos left_x
            ypos row_y
        text L("pref_label_min") style "pref_label":
            xpos min_x
            ypos row_y
        use ui_slider(Preference("auto-forward time"), style_name="pref_bar", xpos=slider_x, ypos=(row_y - 8), tooltip=L("pref_tip_auto_forward"))
        text L("pref_label_max") style "pref_label":
            xpos max_x
            ypos row_y
