# preferences_tabs/visuals_tab.rpy

screen pref_interface_panel(title, subtitle=None, xsize=400, ysize=200, accent="#d8b24f", background="#191531d2"):
    $ bg = "#11152ad8"
    $ shell_border = "#6e6ca540"
    $ shell_fill = "#26295724"

    fixed:
        xsize xsize
        ysize ysize

        add Solid(shell_fill) xpos 0 ypos 0 xsize xsize ysize ysize
        add Solid(shell_border) xpos 0 ypos 0 xsize xsize ysize 1
        add Solid(shell_border) xpos 0 ypos (ysize - 1) xsize xsize ysize 1
        add Solid(shell_border) xpos 0 ypos 0 xsize 1 ysize ysize
        add Solid(shell_border) xpos (xsize - 1) ypos 0 xsize 1 ysize ysize

        add Solid("#9d8cff10") xpos 1 ypos 1 xsize (xsize - 2) ysize (ysize - 2)

        add Solid(bg) xpos 12 ypos 12 xsize (xsize - 24) ysize (ysize - 24)
        add Solid("#d8b24f33") xpos 12 ypos 12 xsize (xsize - 24) ysize 1
        add Solid("#d8b24f22") xpos 12 ypos (ysize - 13) xsize (xsize - 24) ysize 1

        vbox:
            xpos 32
            ypos 24
            xsize (xsize - 64)
            spacing 8

            text title style "pref_section_title" color accent
            if subtitle:
                text subtitle style "pref_label_text" color "#d5dcef"
            add Solid(accent + "66") xsize (xsize - 64) ysize 2
            transclude


screen pref_interface_option_button(label, action, selected=False, xsize=120, ysize=44):
    $ theme = pref_theme_palette()
    $ selected_bg = theme["selected_bg"]
    $ selected_text = theme["selected_text"]

    button:
        background "#121127d0"
        hover_background "#1b1935f0"
        xsize xsize
        ysize ysize
        action action

        fixed:
            xsize xsize
            ysize ysize

            if selected:
                add Solid(pref_color_alpha(selected_bg, 0.86)) xsize xsize ysize ysize

            text label:
                style "pref_setting_btn_text"
                color (selected_text if selected else "#edf3ff")
                hover_color "#ffffff"
                xalign 0.5
                yalign 0.5
                text_align 0.5


screen pref_interface_cursor_tile(symbol, label, value, selected=False, icon=None):
    $ theme = pref_theme_palette()
    $ accent = theme["accent"]
    $ selected_text = "#f6e8f7"

    button:
        background "#121127d0"
        hover_background pref_color_alpha(accent, 0.12)
        xsize 86
        ysize 76
        action Function(pref_set_visual_value, "pref_cursor_style", value)

        fixed:
            xsize 86
            ysize 76

            add Solid("#0b10263e") xpos 6 ypos 6 xsize 74 ysize 64

            if selected:
                add Solid(pref_color_alpha(accent, 0.94)) xsize 86 ysize 2
                add Solid(pref_color_alpha(accent, 0.94)) ypos 74 xsize 86 ysize 2
                add Solid(pref_color_alpha(accent, 0.94)) xsize 2 ysize 76
                add Solid(pref_color_alpha(accent, 0.94)) xpos 84 xsize 2 ysize 76
                add Solid(pref_color_alpha(accent, 0.08)) xpos 3 ypos 3 xsize 80 ysize 70

            if icon:
                add Transform(icon, fit="contain", xsize=34, ysize=34, xalign=0.5, ypos=8)
            else:
                text symbol:
                    style "pref_section_title"
                    size 30
                    color (selected_text if selected else accent)
                    xalign 0.5
                    ypos 6
                    text_align 0.5

            text label:
                style "pref_label_text"
                size 12
                color (selected_text if selected else "#edf3ff")
                xalign 0.5
                ypos 52
                text_align 0.5


screen pref_interface_window_tile(label, value, selected=False):
    $ theme = pref_theme_palette()
    $ accent = theme["accent"]
    $ selected_text = "#f6e8f7"

    button:
        background "#121127d0"
        hover_background pref_color_alpha(accent, 0.12)
        xsize 108
        ysize 122
        action Function(pref_set_visual_value, "pref_dialogue_window_style", value)

        fixed:
            xsize 108
            ysize 122

            add Solid("#0b10263e") xpos 8 ypos 10 xsize 92 ysize 72

            if selected:
                add Solid(pref_color_alpha(accent, 0.94)) xsize 108 ysize 2
                add Solid(pref_color_alpha(accent, 0.94)) ypos 120 xsize 108 ysize 2
                add Solid(pref_color_alpha(accent, 0.94)) xsize 2 ysize 122
                add Solid(pref_color_alpha(accent, 0.94)) xpos 106 xsize 2 ysize 122
                add Solid(pref_color_alpha(accent, 0.08)) xpos 3 ypos 3 xsize 102 ysize 116

            if value == "classic":
                add Solid("#202338") xpos 13 ypos 18 xsize 82 ysize 50
                add Solid("#d8b24f") xpos 13 ypos 18 xsize 82 ysize 2
                add Solid("#d8b24f") xpos 13 ypos 66 xsize 82 ysize 2
                add Solid("#d8b24f") xpos 13 ypos 18 xsize 2 ysize 50
                add Solid("#d8b24f") xpos 93 ypos 18 xsize 2 ysize 50
            elif value == "soft":
                add Solid("#2b2c41") xpos 13 ypos 18 xsize 82 ysize 50
                add Solid("#f0eff61c") xpos 18 ypos 23 xsize 72 ysize 40
                add Solid("#7f869f") xpos 13 ypos 18 xsize 82 ysize 2
            elif value == "bright":
                add Solid("#ddd7d1") xpos 13 ypos 18 xsize 82 ysize 50
                add Solid("#f6f1eb") xpos 18 ypos 23 xsize 72 ysize 40
                add Solid("#d8b24f") xpos 13 ypos 18 xsize 82 ysize 2
                add Solid("#d8b24f") xpos 13 ypos 66 xsize 82 ysize 2
            elif value == "fantasy":
                add Solid("#2c1f45") xpos 13 ypos 18 xsize 82 ysize 50
                add Solid("#d39bd2") xpos 13 ypos 18 xsize 82 ysize 2
                add Solid("#9c7cff88") xpos 13 ypos 65 xsize 82 ysize 3
                add Solid("#e8c9ff44") xpos 16 ypos 22 xsize 76 ysize 1
            elif value == "minimal":
                add Solid("#303247") xpos 13 ypos 18 xsize 82 ysize 50
                add Solid("#ffffff12") xpos 13 ypos 18 xsize 82 ysize 1
                add Solid("#9c7cff66") xpos 13 ypos 65 xsize 82 ysize 3

            if value == "classic":
                add Solid("#d8b24f") xpos 12 ypos 17 xsize 10 ysize 2
                add Solid("#d8b24f") xpos 12 ypos 17 xsize 2 ysize 10
                add Solid("#d8b24f") xpos 86 ypos 17 xsize 10 ysize 2
                add Solid("#d8b24f") xpos 94 ypos 17 xsize 2 ysize 10
                add Solid("#d8b24f") xpos 12 ypos 59 xsize 10 ysize 2
                add Solid("#d8b24f") xpos 12 ypos 51 xsize 2 ysize 10
                add Solid("#d8b24f") xpos 86 ypos 59 xsize 10 ysize 2
                add Solid("#d8b24f") xpos 94 ypos 51 xsize 2 ysize 10
            elif value == "soft":
                add Solid("#7f869f") xpos 12 ypos 17 xsize 10 ysize 2
                add Solid("#7f869f") xpos 12 ypos 17 xsize 2 ysize 10
                add Solid("#7f869f") xpos 86 ypos 17 xsize 10 ysize 2
                add Solid("#7f869f") xpos 94 ypos 17 xsize 2 ysize 10
            elif value == "bright":
                add Solid("#efe3be") xpos 12 ypos 17 xsize 10 ysize 2
                add Solid("#efe3be") xpos 12 ypos 17 xsize 2 ysize 10
                add Solid("#efe3be") xpos 86 ypos 17 xsize 10 ysize 2
                add Solid("#efe3be") xpos 94 ypos 17 xsize 2 ysize 10
            elif value == "fantasy":
                add Solid("#d39bd2") xpos 12 ypos 17 xsize 10 ysize 2
                add Solid("#d39bd2") xpos 12 ypos 17 xsize 2 ysize 10
                add Solid("#d39bd2") xpos 86 ypos 17 xsize 10 ysize 2
                add Solid("#d39bd2") xpos 94 ypos 17 xsize 2 ysize 10
            elif value == "minimal":
                add Solid("#c5bfd6") xpos 13 ypos 18 xsize 82 ysize 1

            text label:
                style "pref_label_text"
                size 12
                color (selected_text if selected else "#edf3ff")
                xalign 0.5
                ypos 90
                text_align 0.5


screen pref_interface_slider_row(label, value, value_text):
    hbox:
        spacing 10

        fixed:
            xsize 240
            ysize 44
            text label style "pref_setting_label" size 18 yalign 0.5

        fixed:
            xsize 40
            ysize 44
            text "MIN" style "pref_label_text" xalign 1.0 yalign 0.5

        fixed:
            xsize 230
            ysize 44
            use ui_slider(value, style_name="pref_bar", xpos=0, ypos=9, xsize=230, ysize=28)

        fixed:
            xsize 40
            ysize 44
            text "MAX" style "pref_label_text" xalign 0.0 yalign 0.5

        fixed:
            xsize 44
            ysize 44
            text value_text style "pref_label_text" color "#f1d08a" xalign 1.0 yalign 0.5


screen preferences_tab_visuals():
    $ tab_colors = pref_tab_colors("visuals")
    $ theme = pref_theme_palette()

    fixed:
        xsize 1450
        ysize 740

        hbox:
            xpos 1034
            ypos 0
            spacing 10
            text "SETTINGS ARE SAVED AUTOMATICALLY" style "pref_label_text" color "#f5f1e7"
            text "v" style "pref_section_title" size 20 color tab_colors["accent"] ypos -1

        hbox:
            spacing 18
            ypos 16

            vbox:
                spacing 18

                use pref_interface_panel("INTERFACE LAYOUT", "ADJUST THE LOOK AND CLARITY OF MENUS AND DIALOGUE.", 716, 360, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 14
                        use pref_interface_slider_row("UI OPACITY", PersistentFloatAdjustment("pref_ui_opacity", 0.80), pref_visual_percent("pref_ui_opacity"))
                        use pref_interface_slider_row("TEXT BOX OPACITY", PersistentFloatAdjustment("pref_textbox_opacity", 0.80), pref_visual_percent("pref_textbox_opacity"))
                        use pref_interface_slider_row("MENU BACKGROUND DIM", PersistentFloatAdjustment("pref_menu_background_dim", 0.60), pref_visual_percent("pref_menu_background_dim"))
                        use pref_interface_slider_row("HIGHLIGHT INTENSITY", PersistentFloatAdjustment("pref_highlight_intensity", 0.70), pref_visual_percent("pref_highlight_intensity"))

                use pref_interface_panel("THEME ACCENT", "PERSONALIZE COLOURS, GLOWS, AND INTERFACE STYLING.", 716, 354, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 16

                        hbox:
                            spacing 10
                            fixed:
                                xsize 222
                                ysize 40
                                text "ACCENT COLOUR" style "pref_setting_label" size 19 color "#f0f4ff" yalign 0.5
                            use pref_interface_option_button("GOLD", Function(pref_set_visual_value, "pref_theme_accent", "gold"), selected=(pref_theme_accent_key() == "gold"), xsize=72, ysize=40)
                            use pref_interface_option_button("VIOLET", Function(pref_set_visual_value, "pref_theme_accent", "violet"), selected=(pref_theme_accent_key() == "violet"), xsize=84, ysize=40)
                            use pref_interface_option_button("BLUE", Function(pref_set_visual_value, "pref_theme_accent", "blue"), selected=(pref_theme_accent_key() == "blue"), xsize=72, ysize=40)
                            use pref_interface_option_button("MINT", Function(pref_set_visual_value, "pref_theme_accent", "mint"), selected=(pref_theme_accent_key() == "mint"), xsize=72, ysize=40)
                            use pref_interface_option_button("ROSE", Function(pref_set_visual_value, "pref_theme_accent", "rose"), selected=(pref_theme_accent_key() == "rose"), xsize=72, ysize=40)

                        hbox:
                            spacing 10
                            fixed:
                                xsize 222
                                ysize 40
                                text "BUTTON GLOW" style "pref_setting_label" size 19 color "#f0f4ff" yalign 0.5
                            use pref_interface_option_button("LOW", Function(pref_set_visual_value, "pref_button_glow", "low"), selected=(pref_button_glow_key() == "low"), xsize=96, ysize=40)
                            use pref_interface_option_button("MEDIUM", Function(pref_set_visual_value, "pref_button_glow", "medium"), selected=(pref_button_glow_key() == "medium"), xsize=96, ysize=40)
                            use pref_interface_option_button("HIGH", Function(pref_set_visual_value, "pref_button_glow", "high"), selected=(pref_button_glow_key() == "high"), xsize=96, ysize=40)

                        hbox:
                            spacing 10
                            fixed:
                                xsize 222
                                ysize 40
                                text "PANEL BORDER STYLE" style "pref_setting_label" size 19 color "#f0f4ff" yalign 0.5
                            use pref_interface_option_button("SIMPLE", Function(pref_set_visual_value, "pref_panel_border_style", "simple"), selected=(pref_panel_border_style_key() == "simple"), xsize=96, ysize=40)
                            use pref_interface_option_button("ORNATE", Function(pref_set_visual_value, "pref_panel_border_style", "ornate"), selected=(pref_panel_border_style_key() == "ornate"), xsize=96, ysize=40)
                            use pref_interface_option_button("SOFT GLOW", Function(pref_set_visual_value, "pref_panel_border_style", "soft_glow"), selected=(pref_panel_border_style_key() == "soft_glow"), xsize=96, ysize=40)

                        hbox:
                            spacing 10
                            fixed:
                                xsize 222
                                ysize 40
                                text "SELECTED HIGHLIGHT STYLE" style "pref_setting_label" size 19 color "#f0f4ff" yalign 0.5
                            use pref_interface_option_button("FILL", Function(pref_set_visual_value, "pref_selected_highlight_style", "fill"), selected=(pref_selected_highlight_style_key() == "fill"), xsize=96, ysize=40)
                            use pref_interface_option_button("OUTLINE", Function(pref_set_visual_value, "pref_selected_highlight_style", "outline"), selected=(pref_selected_highlight_style_key() == "outline"), xsize=96, ysize=40)
                            use pref_interface_option_button("GLOW", Function(pref_set_visual_value, "pref_selected_highlight_style", "glow"), selected=(pref_selected_highlight_style_key() == "glow"), xsize=96, ysize=40)

            vbox:
                spacing 18

                use pref_interface_panel("CURSOR STYLE", "CHOOSE THE CURSOR APPEARANCE.", 716, 196, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    hbox:
                        spacing 12
                        use pref_interface_cursor_tile(">", "ARROW", "arrow", selected=(pref_cursor_style_key() == "arrow"))
                        use pref_interface_cursor_tile("/", "FEATHER", "feather", selected=(pref_cursor_style_key() == "feather"), icon="gui/button/test.png")
                        use pref_interface_cursor_tile("+", "STAR", "star", selected=(pref_cursor_style_key() == "star"))
                        use pref_interface_cursor_tile("o", "PAW", "paw", selected=(pref_cursor_style_key() == "paw"))
                        use pref_interface_cursor_tile(")", "MOON", "moon", selected=(pref_cursor_style_key() == "moon"))
                        use pref_interface_cursor_tile("#", "CRYSTAL", "crystal", selected=(pref_cursor_style_key() == "crystal"))

                use pref_interface_panel("DIALOGUE WINDOW STYLE", "SELECT THE APPEARANCE OF DIALOGUE WINDOWS.", 716, 264, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    hbox:
                        spacing 8
                        use pref_interface_window_tile("CLASSIC", "classic", selected=(pref_visual_value("pref_dialogue_window_style", "classic") == "classic"))
                        use pref_interface_window_tile("DARK GLASS", "soft", selected=(pref_visual_value("pref_dialogue_window_style", "classic") == "soft"))
                        use pref_interface_window_tile("LIGHT GLASS", "bright", selected=(pref_visual_value("pref_dialogue_window_style", "classic") == "bright"))
                        use pref_interface_window_tile("FANTASY FRAME", "fantasy", selected=(pref_visual_value("pref_dialogue_window_style", "classic") == "fantasy"))
                        use pref_interface_window_tile("MINIMAL", "minimal", selected=(pref_visual_value("pref_dialogue_window_style", "classic") == "minimal"))

                use pref_interface_panel("SECTION NOTES", None, 716, 198, accent=tab_colors["accent"], background=tab_colors["panel_bg"]):
                    vbox:
                        spacing 8
                        text "THESE SETTINGS ADJUST THE COLOUR ACCENTS, INTERFACE STYLE, CURSOR APPEARANCE, AND OVERALL PRESENTATION." style "pref_muted_text" color "#dce3f0" xmaximum 620
                        text "CHOOSE OPTIONS THAT BEST SUIT YOUR PREFERENCES AND ENHANCE YOUR STORY EXPERIENCE." style "pref_muted_text" color "#dce3f0" xmaximum 620
