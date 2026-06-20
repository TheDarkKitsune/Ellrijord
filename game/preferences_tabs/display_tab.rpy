# preferences_tabs/display_tab.rpy

screen preferences_tab_display():
    $ tab_colors = pref_ui_tab_colors("display")
    $ preview_line = "The next line arrives at your chosen pace."

    fixed:
        xsize 1450
        ysize 740

        hbox:
            spacing 22

            vbox:
                spacing 18

                use pref_hub_panel("DISPLAY MODE", "Choose how the game window is shown.", 694, 190, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    hbox:
                        spacing 14
                        use pref_small_button("pref_button_window", Preference("display", "window"), selected=(not preferences.fullscreen), xsize=300, ysize=52, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                        use pref_small_button("pref_button_fullscreen", Preference("display", "fullscreen"), selected=preferences.fullscreen, xsize=300, ysize=52, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                use pref_hub_panel("SKIP OPTIONS", "Set how skipping behaves during story scenes.", 694, 228, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 16

                        hbox:
                            spacing 14
                            fixed:
                                xsize 210
                                ysize 52
                                text pref_L("pref_label_skip_unseen") style "pref_setting_label" yalign 0.5
                            use pref_small_button("pref_button_on", SetField(preferences, "skip_unseen", True), selected=preferences.skip_unseen, xsize=152, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_button_off", SetField(preferences, "skip_unseen", False), selected=(not preferences.skip_unseen), xsize=152, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                        hbox:
                            spacing 14
                            fixed:
                                xsize 210
                                ysize 52
                                text pref_L("pref_label_skip_after_choices") style "pref_setting_label" yalign 0.5
                            use pref_small_button("pref_button_on", SetField(preferences, "skip_after_choices", True), selected=preferences.skip_after_choices, xsize=152, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_button_off", SetField(preferences, "skip_after_choices", False), selected=(not preferences.skip_after_choices), xsize=152, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                use pref_hub_panel("TEXT PACE", "Tune dialogue speed and auto-forward timing.", 694, 236, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 12
                        use pref_hub_slider_row("pref_label_text_speed", Preference("text speed"), label_width=220, slider_width=300)
                        use pref_hub_slider_row("pref_label_auto_forward", Preference("auto-forward time"), label_width=220, slider_width=300)

            vbox:
                spacing 18

                use pref_hub_panel("LANGUAGE", "Switch the interface language.", 734, 220, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 12

                        hbox:
                            spacing 12
                            use pref_small_button("pref_lang_en_gb", Function(set_ui_lang, "en_gb"), selected=(get_ui_lang() == "en_gb"), xsize=210, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_lang_es_es", Function(set_ui_lang, "es_es"), selected=(get_ui_lang() == "es_es"), xsize=210, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_lang_fr_fr", Function(set_ui_lang, "fr_fr"), selected=(get_ui_lang() == "fr_fr"), xsize=210, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                        hbox:
                            spacing 12
                            use pref_small_button("pref_lang_de_de", Function(set_ui_lang, "de_de"), selected=(get_ui_lang() == "de_de"), xsize=210, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_lang_pt_br", Function(set_ui_lang, "pt_br"), selected=(get_ui_lang() == "pt_br"), xsize=210, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                use pref_hub_panel("LIVE PREVIEW", xsize=734, ysize=258, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    $ mode_name = "Fullscreen" if preferences.fullscreen else "Window"
                    $ skip_text = "Unread text can be skipped." if preferences.skip_unseen else "Unread text stops skip."
                    $ choice_text = "Skipping continues after choices." if preferences.skip_after_choices else "Choices stop at choices."

                    frame:
                        background pref_surface_color(tab_colors["well_bg"], "well")
                        xsize 690
                        ysize 118
                        xpadding 18
                        ypadding 12

                        vbox:
                            spacing 6
                            text mode_name style "pref_section_title" color tab_colors["accent"]
                            add pref_preview_displayable(preview_line, style="pref_body_text", size=20)

                    text skip_text style "pref_muted_text"
                    text choice_text style "pref_muted_text"

                use pref_hub_panel("SECTION NOTES", "What changes here affect.", 734, 196, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 10
                        text "Display Mode changes the window style used by the game." style "pref_muted_text"
                        text "Skip Options control unread text and choice behaviour." style "pref_muted_text"
                        text "Text Pace sets dialogue speed and auto-forward timing." style "pref_muted_text"
