# preferences_tabs/visuals_tab.rpy

screen pref_interface_panel(title, subtitle=None, xsize=400, ysize=200, accent="#d8b24f", background="#191531d2", panel_accent=None):
    $ surface_accent = panel_accent if panel_accent is not None else accent
    fixed:
        xsize xsize
        ysize ysize

        add pref_panel_surface(xsize, ysize, background, surface_accent)

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
    $ accent = theme["accent"]
    $ selected_bg = theme["selected_bg"]
    $ selected_text = theme["selected_text"]
    $ label_lines = label.split(" ") if (" " in label and xsize <= 100) else [label]
    $ text_size = 14 if len(label_lines) > 1 else (16 if (xsize <= 96 and len(label) >= 7) else 18)
    $ text_box_width = max(1, xsize - 10)
    $ text_yoffset = -1 if len(label_lines) > 1 else 0
    $ idle_surface = pref_button_surface(xsize, ysize, accent, selected_bg, base_color="#121127d0", hover_color="#1b1935f0")
    $ hover_surface = pref_button_surface(xsize, ysize, accent, selected_bg, hovered=True, base_color="#121127d0", hover_color="#1b1935f0")
    $ selected_surface = pref_button_surface(xsize, ysize, accent, selected_bg, selected=True, base_color="#121127d0", hover_color="#1b1935f0")

    button:
        selected selected
        background idle_surface
        hover_background hover_surface
        selected_background selected_surface
        selected_hover_background selected_surface
        xsize xsize
        ysize ysize
        action action

        fixed:
            xsize xsize
            ysize ysize

            vbox:
                xsize text_box_width
                xalign 0.5
                yalign 0.5
                yoffset text_yoffset
                spacing 0

                for line in label_lines:
                    text line:
                        style "pref_setting_btn_text"
                        size text_size
                        xsize text_box_width
                        color (selected_text if selected else "#edf3ff")
                        hover_color (selected_text if selected else "#ffffff")
                        xalign 0.5
                        text_align 0.5


screen pref_interface_cursor_tile(symbol, label, value, selected=False, icon=None):
    $ theme = pref_theme_palette()
    $ accent = theme["accent"]
    $ selected_text = "#f6e8f7"
    $ base_bg = "#121127d0"
    $ hover_bg = base_bg if selected else pref_color_alpha(accent, 0.12)

    button:
        background base_bg
        hover_background hover_bg
        xpadding 0
        ypadding 0
        xsize 86
        ysize 76
        action Function(pref_set_visual_value, "pref_cursor_style", value)

        fixed:
            xsize 86
            ysize 76

            if selected:
                add Solid(pref_color_alpha(accent, 0.94)) xsize 86 ysize 2
                add Solid(pref_color_alpha(accent, 0.94)) ypos 74 xsize 86 ysize 2
                add Solid(pref_color_alpha(accent, 0.94)) xsize 2 ysize 76
                add Solid(pref_color_alpha(accent, 0.94)) xpos 84 xsize 2 ysize 76

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
    $ base_bg = "#121127d0"
    $ hover_bg = base_bg if selected else pref_color_alpha(accent, 0.12)

    button:
        background base_bg
        hover_background hover_bg
        xpadding 0
        ypadding 0
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
            elif value == "komic":
                add Transform("gui/KOMIC/textbox.png", xpos=13, ypos=18, xsize=82, ysize=50)
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
            elif value == "komic":
                add Solid("#f7f0f5") xpos 12 ypos 17 xsize 10 ysize 2
                add Solid("#f7f0f5") xpos 12 ypos 17 xsize 2 ysize 10
                add Solid("#f7f0f5") xpos 86 ypos 17 xsize 10 ysize 2
                add Solid("#f7f0f5") xpos 94 ypos 17 xsize 2 ysize 10
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


screen pref_interface_slider_row(label, value):
    $ _setting_color = pref_ui_text_color("setting_label")
    $ _label_color = pref_ui_text_color("label")
    $ _percent_color = pref_ui_text_color("percent")
    hbox:
        spacing 10

        fixed:
            xsize 240
            ysize 44
            text label style "pref_setting_label" size 18 color _setting_color yalign 0.5

        fixed:
            xsize 40
            ysize 44
            text "MIN" style "pref_label_text" color _label_color xalign 1.0 yalign 0.5

        fixed:
            xsize 230
            ysize 44
            use ui_slider(value, style_name="pref_bar", xpos=0, ypos=9, xsize=230, ysize=28)

        fixed:
            xsize 40
            ysize 44
            text "MAX" style "pref_label_text" color _label_color xalign 0.0 yalign 0.5

        fixed:
            xsize 44
            ysize 44
            add pref_live_bar_percent_displayable(value, style="pref_label_text", color=_percent_color) xalign 1.0 yalign 0.5


screen preferences_tab_visuals():
    $ tab_colors = pref_ui_tab_colors("visuals")
    $ theme = pref_theme_palette()

    fixed:
        xsize 1450
        ysize 740

        hbox:
            spacing 18
            ypos 16

            vbox:
                spacing 18

                use pref_interface_panel("INTERFACE LAYOUT", "ADJUST THE LOOK AND CLARITY OF MENUS AND DIALOGUE.", 716, 360, accent=tab_colors["accent"], background=tab_colors["panel_bg"], panel_accent=theme["accent"]):
                    vbox:
                        spacing 14
                        use pref_interface_slider_row("UI OPACITY", VariableValue("persistent.pref_ui_opacity", range=1.0, step=0.1, force_step=True, action=Function(apply_visual_preferences)))
                        use pref_interface_slider_row("TEXT BOX OPACITY", VariableValue("persistent.pref_textbox_opacity", range=1.0, step=0.1, force_step=True, action=Function(apply_visual_preferences)))
                        use pref_interface_slider_row("MENU BACKGROUND DIM", VariableValue("persistent.pref_menu_background_dim", range=1.0, step=0.1, force_step=True, action=Function(apply_visual_preferences)))
                        use pref_interface_slider_row("HIGHLIGHT INTENSITY", VariableValue("persistent.pref_highlight_intensity", range=1.0, step=0.1, force_step=True, action=Function(apply_visual_preferences)))

                use pref_interface_panel("THEME ACCENT", "PERSONALISE COLOURS, GLOWS, AND INTERFACE STYLING.", 716, 354, accent=tab_colors["accent"], background=tab_colors["panel_bg"], panel_accent=theme["accent"]):
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
                            use pref_interface_option_button("GLASS", Function(pref_set_visual_value, "pref_panel_border_style", "ornate"), selected=(pref_panel_border_style_key() == "ornate"), xsize=96, ysize=40)
                            use pref_interface_option_button("GLOW", Function(pref_set_visual_value, "pref_panel_border_style", "soft_glow"), selected=(pref_panel_border_style_key() == "soft_glow"), xsize=96, ysize=40)

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

                use pref_interface_panel("CURSOR STYLE", "CHOOSE THE CURSOR APPEARANCE.", 716, 208, accent=tab_colors["accent"], background=tab_colors["panel_bg"], panel_accent=theme["accent"]):
                    hbox:
                        spacing 12
                        use pref_interface_cursor_tile(">", "ARROW", "arrow", selected=(pref_cursor_style_key() == "arrow"), icon="gui/KOMIC/Cursors/cursor_1.png")
                        use pref_interface_cursor_tile("/", "FEATHER", "feather", selected=(pref_cursor_style_key() == "feather"), icon="gui/button/test.png")
                        use pref_interface_cursor_tile("+", "STAR", "star", selected=(pref_cursor_style_key() == "star"))
                        use pref_interface_cursor_tile("o", "PAW", "paw", selected=(pref_cursor_style_key() == "paw"))
                        use pref_interface_cursor_tile(")", "MOON", "moon", selected=(pref_cursor_style_key() == "moon"))
                        use pref_interface_cursor_tile("#", "CRYSTAL", "crystal", selected=(pref_cursor_style_key() == "crystal"))

                use pref_interface_panel("DIALOGUE WINDOW STYLE", "SELECT THE APPEARANCE OF DIALOGUE WINDOWS.", 716, 264, accent=tab_colors["accent"], background=tab_colors["panel_bg"], panel_accent=theme["accent"]):
                    hbox:
                        spacing 8
                        use pref_interface_window_tile("CLASSIC", "classic", selected=(pref_dialogue_window_style_key() == "classic"))
                        use pref_interface_window_tile("KOMIC", "komic", selected=(pref_dialogue_window_style_key() == "komic"))
                        use pref_interface_window_tile("LIGHT GLASS", "bright", selected=(pref_dialogue_window_style_key() == "bright"))
                        use pref_interface_window_tile("FANTASY FRAME", "fantasy", selected=(pref_dialogue_window_style_key() == "fantasy"))
                        use pref_interface_window_tile("MINIMAL", "minimal", selected=(pref_dialogue_window_style_key() == "minimal"))

                use pref_interface_panel("SECTION NOTES", None, 716, 198, accent=tab_colors["accent"], background=tab_colors["panel_bg"], panel_accent=theme["accent"]):
                    vbox:
                        spacing 8
                        text "THESE SETTINGS ADJUST THE COLOUR ACCENTS, INTERFACE STYLE, CURSOR APPEARANCE, AND OVERALL PRESENTATION." style "pref_muted_text" color "#dce3f0" xmaximum 620
                        text "CHOOSE OPTIONS THAT BEST SUIT YOUR PREFERENCES AND ENHANCE YOUR STORY EXPERIENCE." style "pref_muted_text" color "#dce3f0" xmaximum 620
