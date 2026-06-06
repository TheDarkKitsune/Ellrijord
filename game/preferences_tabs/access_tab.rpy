# preferences_tabs/access_tab.rpy

screen preferences_tab_access(pref_access_yadj):
    $ tab_colors = pref_tab_colors("access")

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

                use pref_hub_panel("VOICE MIX", "Audio behavior while self-voicing runs.", 930, 246, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 12

                        if config.has_voice:
                            use pref_hub_slider_row("pref_label_voice_volume", Preference("voice volume"), style_name="pref_bar", label_width=250, slider_width=420)

                        use pref_hub_slider_row("pref_label_self_voicing_volume_drop", Preference("self voicing volume drop"), style_name="pref_bar", label_width=250, slider_width=420)

            vbox:
                spacing 18

                use pref_hub_panel("CONTRAST", xsize=498, ysize=168, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 10
                        text "High-contrast text makes dialogue and labels easier to read." style "pref_label_text"
                        hbox:
                            spacing 12
                            use pref_small_button("pref_button_on", Preference("high contrast text", "enable"), selected=getattr(preferences, "high_contrast_text", False), xsize=205, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_button_off", Preference("high contrast text", "disable"), selected=(not getattr(preferences, "high_contrast_text", False)), xsize=205, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                use pref_hub_panel("SCREEN READER", xsize=498, ysize=228, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 10

                        hbox:
                            spacing 12
                            use pref_small_button("pref_button_text_to_speech", Preference("self voicing", "enable"), selected=getattr(preferences, "self_voicing", False), xsize=205, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_button_clipboard", Preference("clipboard voicing", "enable"), selected=getattr(preferences, "clipboard_voicing", False), xsize=205, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                        hbox:
                            spacing 12
                            use pref_small_button("pref_button_on", Preference("debug voicing", "enable"), selected=getattr(preferences, "debug_voicing", False), xsize=205, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])
                            use pref_small_button("pref_button_off", Preference("debug voicing", "disable"), selected=(not getattr(preferences, "debug_voicing", False)), xsize=205, ysize=50, accent=tab_colors["accent"], selected_bg=tab_colors["selected_bg"], selected_text=tab_colors["selected_text"])

                        text "Use self-voicing for narration. Clipboard and debug are optional tools." style "pref_label_text"

                use pref_hub_panel("PREVIEW", xsize=498, ysize=160, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    frame:
                        background pref_surface_color(tab_colors["well_bg"], "well")
                        xsize 454
                        ysize 60
                        xpadding 16
                        ypadding 8

                        text "Aa Bb Cc 123" style "pref_section_title" color tab_colors["accent"]

                    text "Font: [pref_font_label()]" style "pref_label_text"

                use pref_hub_panel("SECTION NOTES", xsize=498, ysize=120, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 8
                        text "Font changes update menus and dialogue immediately." style "pref_label_text"
                        text "Self-voicing can duck other audio while narration is active." style "pref_label_text"
