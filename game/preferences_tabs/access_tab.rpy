# preferences_tabs/access_tab.rpy

screen preferences_tab_access(pref_access_yadj):
    $ tab_colors = pref_ui_tab_colors("access")

    fixed:
        xsize 1450
        ysize 740

        hbox:
            spacing 22

            vbox:
                spacing 18

                use pref_hub_panel("READABLE TEXT", "Font choice and text spacing.", 930, 382, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 12

                        hbox:
                            spacing 12
                            use pref_small_button("pref_button_default_font", Preference("font transform", None), selected=(getattr(preferences, "font_transform", None) is None), xsize=188, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_button_dejavu_sans", Preference("font transform", "dejavusans"), selected=(getattr(preferences, "font_transform", None) == "dejavusans"), xsize=188, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_button_cinzel", Preference("font transform", "cinzel"), selected=(getattr(preferences, "font_transform", None) == "cinzel"), xsize=188, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                        hbox:
                            spacing 12
                            use pref_small_button("pref_button_opendyslexic", Preference("font transform", "opendyslexic"), selected=(getattr(preferences, "font_transform", None) == "opendyslexic"), xsize=188, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_button_water_lemon", Preference("font transform", "water_lemon"), selected=(getattr(preferences, "font_transform", None) == "water_lemon"), xsize=188, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                        use pref_hub_slider_row("pref_label_text_size_scaling", Preference("font size"), style_name="pref_bar", label_width=250, slider_width=420)
                        use pref_hub_slider_row("pref_label_line_space_scaling", Preference("font line spacing"), style_name="pref_bar", label_width=250, slider_width=420)

                use pref_hub_panel("NARRATION AUDIO", "Audio behaviour while narration support runs.", 930, 246, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 12

                        if config.has_voice:
                            use pref_hub_slider_row("NARRATION VOLUME", pref_quantized_adjustment("voice volume", "voice_volume"), style_name="pref_bar", label_width=250, slider_width=420, show_percent=True)

                        use pref_hub_slider_row("LOWER GAME AUDIO DURING NARRATION", pref_quantized_adjustment("self voicing volume drop", "self_voicing_volume_drop", default=0.0), style_name="pref_bar", label_width=250, slider_width=420, show_percent=True)

            vbox:
                spacing 10

                use pref_hub_panel("CONTRAST", xsize=498, ysize=190, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 10
                        text "High-contrast text makes dialogue and labels easier to read." style "pref_label_text"
                        hbox:
                            spacing 12
                            use pref_small_button("pref_button_on", Function(pref_set_menu_high_contrast_choice, True), selected=pref_menu_high_contrast_choice(), xsize=205, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_button_off", Function(pref_set_menu_high_contrast_choice, False), selected=(not pref_menu_high_contrast_choice()), xsize=205, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                use pref_hub_panel("SCREEN READER", xsize=498, ysize=178, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 10

                        hbox:
                            spacing 12
                            use pref_small_button("pref_button_on", Preference("self voicing", "enable"), selected=getattr(preferences, "self_voicing", False), xsize=205, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_button_off", Preference("self voicing", "disable"), selected=(not getattr(preferences, "self_voicing", False)), xsize=205, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                        text "Use self-voicing for narration." style "pref_label_text"

                use pref_hub_panel("SECTION NOTES", xsize=498, ysize=170, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 8
                        text "Font changes update menus and dialogue immediately." style "pref_label_text"
                        text "Self-voicing can duck other audio while narration is active." style "pref_label_text"
