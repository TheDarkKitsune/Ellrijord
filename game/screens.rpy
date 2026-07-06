################################################################################
## Initialization
################################################################################

init offset = -1

init python:
    def pref_dialogue_should_center(text):
        if not text:
            return False

        plain_text = renpy.filter_text_tags(str(text), allow=[])
        plain_text = plain_text.replace("\n", " ").strip()

        if not plain_text:
            return False

        word_count = len(plain_text.split())

        return word_count <= 2

################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")

style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5

style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")

style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar ConditionSwitch("pref_uses_komic_ui()", Frame("gui/KOMIC/ScrollBars/vertical_idle_bar.png", 9, 9, 9, 9, tile=False), "True", Frame("gui/scrollbar/vertical_idle_bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile))
    hover_base_bar ConditionSwitch("pref_uses_komic_ui()", Frame("gui/KOMIC/ScrollBars/vertical_hover_bar.png", 9, 9, 9, 9, tile=False), "True", Frame("gui/scrollbar/vertical_hover_bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile))
    thumb ConditionSwitch("pref_uses_komic_ui()", Frame("gui/KOMIC/ScrollBars/vertical_idle_thumb.png", 9, 9, 9, 9, tile=False), "True", Frame("gui/scrollbar/vertical_idle_thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile))
    hover_thumb ConditionSwitch("pref_uses_komic_ui()", Frame("gui/KOMIC/ScrollBars/vertical_hover_thumb.png", 9, 9, 9, 9, tile=False), "True", Frame("gui/scrollbar/vertical_hover_thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile))

style slider:
    ysize gui.slider_size
    base_bar ConditionSwitch("pref_uses_komic_ui()", Frame("gui/KOMIC/Sliders/horizontal_idle_bar.png", 18, 14, 18, 14, tile=False), "True", Frame("gui/slider/horizontal_idle_bar.png", gui.slider_borders, tile=gui.slider_tile))
    hover_base_bar ConditionSwitch("pref_uses_komic_ui()", Frame("gui/KOMIC/Sliders/horizontal_hover_bar.png", 18, 14, 18, 14, tile=False), "True", Frame("gui/slider/horizontal_hover_bar.png", gui.slider_borders, tile=gui.slider_tile))
    thumb ConditionSwitch("pref_uses_komic_ui()", "gui/KOMIC/Sliders/horizontal_idle_thumb.png", "True", "gui/slider/horizontal_idle_thumb.png")
    hover_thumb ConditionSwitch("pref_uses_komic_ui()", "gui/KOMIC/Sliders/horizontal_hover_thumb.png", "True", "gui/slider/horizontal_hover_thumb.png")

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"

style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################

screen say(who, what):
    default can_dismiss_line = False
    default clean_quick_tab = None
    timer 0.24 action SetScreenVariable("can_dismiss_line", True)
    key "dismiss" action If(can_dismiss_line, Return(), NullAction())
    $ _is_komic = pref_uses_komic_ui()
    $ _hc = pref_custom_high_contrast_enabled()
    $ _window_width = pref_dialogue_window_width()
    $ _window_height = pref_dialogue_window_height()
    $ _dialogue_font = "DejaVuSans.ttf" if _is_komic else gui.text_font
    $ _name_font = "DejaVuSans.ttf" if _is_komic else gui.name_text_font
    $ _clean_name_left = pref_ui_asset("namebox_left", fallback="gui/clean_ui/gui/namebox_left.png")
    $ _clean_name_right = pref_ui_asset("namebox_right", fallback="gui/clean_ui/gui/namebox_right.png")
    $ _clean_side_base = pref_ui_asset("side_image_base", fallback="gui/clean_ui/gui/side_image_base.png")
    $ _clean_side_frame = pref_ui_asset("side_image_frame", fallback="gui/clean_ui/gui/side_image_frame.png")
    $ _clean_ctc = pref_ui_asset("ctc", fallback="gui/clean_ui/gui/ctc.png")
    $ _clean_quickmenu_bg = "gui/clean_ui/gui/quickmenu_ui.png"
    $ _clean_name_color = "#fffaf2" if _hc else "#ff82d7"
    $ _clean_name_outline = "#000000f6" if _hc else "#24101fb8"
    $ _clean_text_outline = "#000000f2" if _hc else "#000000b0"
    $ _center_single_word = pref_dialogue_should_center(what)
    $ _speaker_portrait = (None if _is_komic else pref_dialogue_speaker_portrait_displayable(who, size=194))
    $ _has_speaker_portrait = (_speaker_portrait is not None)
    $ _komic_canvas_width = 1920
    $ _komic_center_x = 960
    $ _komic_content_y = 40 if who is not None else 92
    $ _komic_content_spacing = 14 if who is not None else 0
    $ _komic_text_width = 1040 if who is not None else 1120
    $ _komic_text_size = 24
    $ _komic_text_yoffset = -39
    $ _komic_name_width = 720
    $ _komic_name_size = 32
    $ _komic_name_color = "#fffaf2" if _hc else "#f5fbff"
    $ _komic_text_outline = "#000000f2" if _hc else "#15394fb0"
    $ _komic_name_outline = "#000000f6" if _hc else "#102f42d8"
    $ _komic_icons_right = 1780
    $ _komic_icons_bottom = (_window_height - 18)
    $ _komic_ctc_y = (_window_height - 42)

    if _is_komic:
        window:
            id "window"
            xalign 0.5
            yalign 1.0
            ysize _window_height
            background pref_dialogue_window_background(width=_window_width, height=_window_height)

            fixed:
                xsize _komic_canvas_width
                ysize _window_height

                vbox:
                    xanchor 0.5
                    xpos _komic_center_x
                    ypos _komic_content_y
                    xsize _komic_text_width
                    spacing _komic_content_spacing

                    if who is not None:
                        text who id "who" style "komic_say_label":
                            xalign 0.5
                            xsize _komic_name_width
                            font _name_font
                            size _komic_name_size
                            color _komic_name_color
                            outlines [ (2, _komic_name_outline, 0, 0) ]

                    text what id "what" style "komic_say_dialogue":
                        xalign 0.5
                        xsize _komic_text_width
                        yoffset _komic_text_yoffset
                        font _dialogue_font
                        size _komic_text_size
                        color pref_dialogue_text_color()
                        outlines [ (2, _komic_text_outline, 0, 0) ]
                        adjust_spacing False

                hbox:
                    xanchor 1.0
                    xpos _komic_icons_right
                    yanchor 1.0
                    ypos _komic_icons_bottom
                    spacing 8

                    use komic_quick_icon_button("continue", Preference("auto-forward", "toggle"), selected=preferences.afm_enable)
                    use komic_quick_icon_button("continue", Rollback(), flipped=True, sensitive=renpy.can_rollback())
                    use komic_quick_icon_button("skip", Skip(), alternate_action=Skip(fast=True, confirm=True), selected=renpy.is_skipping())
                    use komic_quick_icon_button("save", ShowMenu("save"))
                    use komic_quick_icon_button("load", ShowMenu("load"))
                    use komic_quick_icon_button("options", ShowMenu("showmenu"))

                add Transform(pref_komic_ctc_displayable(), xalign=0.5, yanchor=1.0, ypos=_komic_ctc_y, xsize=18, ysize=36)
    else:
        frame:
            id "window"
            xalign 0.5
            style "window"

            if _has_speaker_portrait:
                fixed:
                    fit_first True
                    xanchor 0.0
                    xpos 0.33

                    vbox:
                        spacing 10

                        null height 10

                        if who is not None:
                            hbox:
                                spacing 10
                                xanchor 0.0
                                xpos 0.0

                                add Transform(_clean_name_left) yalign 0.5

                                text who id "who":
                                    font _name_font
                                    size gui.name_text_size
                                    bold True
                                    color _clean_name_color
                                    outlines [ (2, _clean_name_outline, 0, 0) ]

                                add Transform(_clean_name_right) yalign 0.5

                        text what id "what":
                            xpos 0
                            xsize 1000
                            text_align 0.0
                            yanchor 0.0
                            ypos 0
                            font _dialogue_font
                            size gui.text_size
                            color pref_dialogue_text_color()
                            adjust_spacing False
                            outlines [ (2, _clean_text_outline, 0, 0) ]

                    if not renpy.variant("small"):
                        fixed:
                            fit_first True
                            xanchor 1.0
                            xpos -30
                            ypos 20

                            add Transform(_clean_side_base, xsize=210, ysize=210)
                            add Transform(_speaker_portrait, xsize=194, ysize=194)
                            add Transform(_clean_side_frame, xsize=214, ysize=214)

            else:
                vbox:
                    spacing 20
                    xalign 0.5

                    if who is not None:
                        frame:
                            style "namebox"

                            hbox:
                                spacing 15
                                xanchor 0.0
                                xpos 0.0

                                add Transform(_clean_name_right, xzoom=-1) yalign 0.5

                                text who id "who":
                                    font _name_font
                                    size gui.name_text_size
                                    bold True
                                    color _clean_name_color
                                    outlines [ (2, _clean_name_outline, 0, 0) ]

                                add _clean_name_right yalign 0.5
                    else:
                        null height 10

                    text what id "what":
                        font _dialogue_font
                        size gui.text_size
                        color pref_dialogue_text_color()
                        adjust_spacing False
                        xalign (0.5 if _center_single_word else 0.0)
                        text_align (0.5 if _center_single_word else 0.0)
                        outlines [ (2, _clean_text_outline, 0, 0) ]

        text "▼":
            at clean_ctc_appear
            xalign 0.5
            yalign 0.955
            font "DejaVuSans.ttf"
            color "#ffffff"
            size 24
            outlines [ (1, "#00000088", 0, 0) ]

    $ _bag_btn_idle = "gui/hud/Player_male_btn.png" if getattr(store, "mc_gender", "male") == "male" else "gui/hud/Player_female_btn.png"
    $ _bag_btn_hover = ("gui/hud/Player_male_btn_hover.png" if getattr(store, "mc_gender", "male") == "male" else "gui/hud/Player_female_btn_hover.png")
    $ _bag_btn_hover = _bag_btn_hover if renpy.loadable(_bag_btn_hover) else _bag_btn_idle
    $ _bag_btn_size = 138 if getattr(store, "mc_gender", "male") != "male" else 101
    $ _bag_btn_xpos = 1615 if getattr(store, "mc_gender", "male") != "male" else 1652
    $ _bag_idle_display = Transform(_bag_btn_idle, xsize=_bag_btn_size, ysize=_bag_btn_size, fit="contain")
    $ _bag_hover_display = Transform(_bag_btn_hover, xsize=_bag_btn_size, ysize=_bag_btn_size, fit="contain")
    $ _setting_btn_idle = "gui/hud/Settings_btn.png"
    $ _setting_btn_hover = "gui/hud/Settings_btn_hover.png" if renpy.loadable("gui/hud/Settings_btn_hover.png") else _setting_btn_idle

    fixed:
        xfill True
        yfill True

        imagebutton:
            xpos _bag_btn_xpos
            ypos 6
            xsize _bag_btn_size
            ysize _bag_btn_size
            xpadding 0
            ypadding 0
            idle _bag_idle_display
            hover _bag_hover_display
            action ShowMenu("inventory_menu")

        imagebutton:
            xpos 1768
            ypos 24
            idle Transform(_setting_btn_idle, size=(101, 101))
            hover Transform(_setting_btn_hover, size=(101, 101))
            action ShowMenu("showmenu")

init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label

style window:
    xalign 0.5
    xfill True
    yfill False
    yalign gui.textbox_yalign
    xsize 1.0
    yminimum 309
    top_padding 25
    bottom_padding 70
    background Frame("gui/clean_ui/gui/textbox.png", left=0, right=0, top=100, bottom=60)

style namebox:
    xpos 0.5
    xanchor 0.5
    xsize None
    ypos 0
    ysize None
    padding gui.namebox_borders.padding
    background None

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign 0.5
    yalign 0.5
    text_align 0.5
    color "#ffffff"

style namebox_label:
    xalign 0.5
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")
    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos
    adjust_spacing False
    color "#f6f1ee"

style komic_say_label is default
style komic_say_dialogue is default
style komic_input_prompt is default

style komic_say_label:
    text_align 0.5

style komic_say_dialogue:
    text_align 0.5
    adjust_spacing False

style komic_input_prompt:
    text_align 0.5


screen input(prompt):
    style_prefix "input"
    $ _is_komic = pref_uses_komic_ui()
    $ _dialogue_font = "DejaVuSans.ttf" if _is_komic else gui.text_font
    $ _hc = pref_custom_high_contrast_enabled()
    $ _window_width = pref_dialogue_window_width()
    $ _komic_canvas_width = 1920
    $ _komic_center_x = 960
    $ _komic_text_y = 92
    $ _komic_text_width = 1080
    $ _komic_text_size = 24
    $ _komic_text_outline = "#000000f2" if _hc else "#15394fb0"

    window:
        ysize pref_dialogue_window_height()
        background pref_dialogue_window_background(width=_window_width, height=pref_dialogue_window_height())
        if _is_komic:
            fixed:
                xsize _komic_canvas_width
                ysize pref_dialogue_window_height()

                vbox:
                    xanchor 0.5
                    xpos _komic_center_x
                    ypos _komic_text_y
                    xsize _komic_text_width
                    spacing 12

                    text prompt style "komic_input_prompt":
                        color pref_dialogue_text_color()
                        font _dialogue_font
                        size _komic_text_size
                        xalign 0.5
                        outlines [ (2, _komic_text_outline, 0, 0) ]

                    input id "input":
                        color pref_dialogue_text_color()
                        font _dialogue_font
                        size _komic_text_size
                        xalign 0.5
                        xmaximum _komic_text_width
        else:
            fixed:
                xsize _window_width
                xalign 0.5
                ysize pref_dialogue_window_height()

                vbox:
                    xalign 0.5
                    ypos 48
                    spacing 18

                    text prompt:
                        style "input_prompt"
                        xalign 0.5
                        text_align 0.5
                        color pref_dialogue_text_color()
                        font _dialogue_font
                        size gui.text_size
                        outlines [ (2, "#000000b0", 0, 0) ]

                    input id "input":
                        xalign 0.5
                        xmaximum 1200
                        color pref_dialogue_text_color()
                        font _dialogue_font
                        size gui.text_size

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


screen choice(items):
    style_prefix "choice"
    $ _is_komic = pref_uses_komic_ui()
    $ _hc = pref_custom_high_contrast_enabled()
    $ _choice_width = 600 if _is_komic else 1185
    $ _choice_height = 100 if _is_komic else 80
    $ _choice_text_width = (_choice_width - 48) if _hc else (500 if _is_komic else 1000)
    $ _choice_text_size = 29 if _is_komic else gui.choice_button_text_size
    $ _choice_accent = pref_ui_tab_colors("access")["accent"]
    $ _choice_selected_bg = pref_ui_tab_colors("access")["selected_bg"]
    $ _choice_idle_bg = (
        pref_button_surface(_choice_width, _choice_height, _choice_accent, _choice_selected_bg, base_color="#0c121cf2", hover_color="#131b28f4")
        if (_is_komic and _hc) else
        (Transform(pref_choice_button_asset(), size=(_choice_width, _choice_height))
            if _is_komic else
            Transform(Frame(pref_choice_button_asset(), 35, 35), xsize=_choice_width, ysize=_choice_height))
    )
    $ _choice_hover_bg = (
        pref_button_surface(_choice_width, _choice_height, _choice_accent, _choice_selected_bg, hovered=True, base_color="#0c121cf2", hover_color="#131b28f4")
        if (_is_komic and _hc) else
        (Transform(pref_choice_button_asset(True), size=(_choice_width, _choice_height))
            if _is_komic else
            Transform(Frame(pref_choice_button_asset(True), 35, 35), xsize=_choice_width, ysize=_choice_height))
    )
    $ _choice_text_color = (
        pref_ui_text_color("button")
        if (_is_komic and _hc) else
        ("#5f515a" if _is_komic else "#f0f0f0")
    )
    $ _choice_text_hover = (
        pref_ui_text_color("button_hover", _choice_accent)
        if (_is_komic and _hc) else
        ("#5f515a" if _is_komic else "#ffffff")
    )

    vbox:
        for i in items:
            textbutton i.caption:
                action i.action
                xminimum _choice_width
                yminimum _choice_height
                background _choice_idle_bg
                hover_background _choice_hover_bg
                insensitive_background _choice_idle_bg
                selected_background _choice_hover_bg
                selected_hover_background _choice_hover_bg
                text_size _choice_text_size
                text_xalign 0.5
                text_yalign 0.5
                text_xmaximum _choice_text_width
                text_color _choice_text_color
                text_hover_color _choice_text_hover
                text_selected_color _choice_text_color
                text_selected_hover_color _choice_text_hover

style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5
    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")
    xalign 0.5
    xminimum 1185
    yminimum 80
    background Transform(Frame("gui/clean_ui/gui/button/choice_idle_background.png", 35, 35), xsize=1185, ysize=80)
    hover_background Transform(Frame("gui/clean_ui/gui/button/choice_hover_background.png", 35, 35), xsize=1185, ysize=80)
    insensitive_background Transform(Frame("gui/clean_ui/gui/button/choice_idle_background.png", 35, 35), xsize=1185, ysize=80)

style choice_button_text is default:
    properties gui.text_properties("choice_button")
    xalign 0.5
    yalign 0.5
    idle_color "#f0f0f0"
    hover_color "#ffffff"
    selected_idle_color "#f0f0f0"
    selected_hover_color "#ffffff"
    outlines [ ]


screen quick_menu():

    zorder 200
    default clean_quick_tab = None

    if quick_menu and not renpy.variant("touch"):
        if renpy.is_skipping():
            use skip_indicator
        add Transform("gui/clean_ui/gui/quickmenu_ui.png", xalign=0.5, yalign=1.0)

        vbox:
            anchor (1.0, 1.0)
            pos (0.99, 0.99)

            if clean_quick_tab:
                text clean_quick_tab:
                    style "dialogue_quick_hint"
                    xalign 1.0

            hbox:
                spacing 0
                xalign 1.0

                imagebutton auto "gui/clean_ui/gui/buttons_navigation/return_%s.png":
                    at clean_quick_menu_atl
                    hovered SetScreenVariable("clean_quick_tab", _("Back"))
                    unhovered SetScreenVariable("clean_quick_tab", None)
                    action If(renpy.can_rollback(), Rollback(), NullAction())

                imagebutton auto "gui/clean_ui/gui/buttons_navigation/skip_%s.png":
                    at clean_quick_menu_atl
                    hovered SetScreenVariable("clean_quick_tab", _("Skip"))
                    unhovered SetScreenVariable("clean_quick_tab", None)
                    action Skip()
                    alternate Skip(fast=True, confirm=True)
                    selected renpy.is_skipping()

                imagebutton auto "gui/clean_ui/gui/buttons_navigation/auto_%s.png":
                    at clean_quick_menu_atl
                    hovered SetScreenVariable("clean_quick_tab", _("Auto Forward"))
                    unhovered SetScreenVariable("clean_quick_tab", None)
                    action Preference("auto-forward", "toggle")
                    selected preferences.afm_enable

                imagebutton auto "gui/clean_ui/gui/buttons_navigation/save_%s.png":
                    at clean_quick_menu_atl
                    hovered SetScreenVariable("clean_quick_tab", _("Save"))
                    unhovered SetScreenVariable("clean_quick_tab", None)
                    action ShowMenu("save")

                imagebutton auto "gui/clean_ui/gui/buttons_navigation/qsave_%s.png":
                    at clean_quick_menu_atl
                    hovered SetScreenVariable("clean_quick_tab", _("Quick Save"))
                    unhovered SetScreenVariable("clean_quick_tab", None)
                    action QuickSave()

                imagebutton auto "gui/clean_ui/gui/buttons_navigation/load_%s.png":
                    at clean_quick_menu_atl
                    hovered SetScreenVariable("clean_quick_tab", _("Quick Load"))
                    unhovered SetScreenVariable("clean_quick_tab", None)
                    action QuickLoad()

                imagebutton auto "gui/clean_ui/gui/buttons_navigation/settings_%s.png":
                    at clean_quick_menu_atl
                    hovered SetScreenVariable("clean_quick_tab", _("Settings"))
                    unhovered SetScreenVariable("clean_quick_tab", None)
                    action ShowMenu("preferences")

init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_menu is hbox
style quick_button is default
style quick_button_text is button_text
style msgbox_quick_menu is default
style msgbox_btn_button is button
style msgbox_btn_button_text is button_text

style quick_menu:
    xalign 0.5
    yalign 1.0

style msgbox_quick_menu:
    xpos 848
    ypos 188
    spacing 13

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")

style msgbox_btn_button:
    background None
    hover_background None
    selected_background None
    insensitive_background None
    xpadding 0
    ypadding 0

style msgbox_btn_button_text:
    properties gui.text_properties("quick_button")
    xalign 0.5
    yalign 0.5
    size 28
    idle_color "#ffffff"
    hover_color "#ffffff"
    selected_idle_color "#f2df57"
    selected_hover_color "#f2df57"
    insensitive_color "#ffffff"
    outlines [ ]
    text_align 0.5

transform clean_quick_menu_atl:
    zoom 0.2

transform clean_ctc_appear:
    parallel:
        alpha 0.0
        linear 0.3 alpha 1.0
    parallel:
        yoffset 0
        ease 0.5 yoffset 10
        pause 0.1
        ease 0.1 yoffset 0
        repeat

style dialogue_quick_hint is default

style dialogue_quick_hint:
    font gui.interface_text_font
    size 22
    color "#efe7e1"
    outlines [ (1, "#000000aa", 0, 0) ]

## Auto indicator screen #######################################################
##
## This indicates that auto-forward mode is currently enabled.
##
init python:
    def auto_indicator():
        # Auto mode is on.
        if preferences.afm_enable and not renpy.get_screen("auto_indicator"):
            renpy.show_screen("auto_indicator")
        # Auto mode is off.
        elif (not preferences.afm_enable) and renpy.get_screen("auto_indicator"):
            renpy.hide_screen("auto_indicator")

    # Keep this in overlay functions so the indicator auto-updates.
    if auto_indicator not in config.overlay_functions:
        config.overlay_functions.append(auto_indicator)

screen auto_indicator():

    zorder 205
    style_prefix "auto"

    frame:
        hbox:
            spacing 5

            text _("Auto-Forward") style "auto_text"
            null width 15

            text "▸" at delayed_blink(0.0, 1.0) style "auto_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "auto_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "auto_triangle"

screen skip_indicator():

    zorder 210
    style_prefix "skip"

    frame:
        hbox:
            xanchor 1.0
            xpos 0.9
            spacing 5

            text _("Skipping") style "skip_text"
            null width 15

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"

## This transform blinks the indicator arrow.
transform auto_blink(cycle):
    alpha 0.0
    linear 0.5 alpha 1.0
    pause 0.2
    linear 0.5 alpha 0.0
    pause (cycle - .4)
    repeat

transform delayed_blink(delay, cycle):
    alpha 0.5
    pause delay

    block:
        linear 0.2 alpha 1.0
        pause 0.2
        linear 0.2 alpha 0.5
        pause (cycle - 0.4)
        repeat

style auto_hbox:
    spacing 9

style auto_frame:
    is empty
    xalign 1.0
    yanchor 1.0
    ypos 0.945
    background Frame("gui/clean_ui/gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style auto_text:
    size gui.notify_text_size
    color "#ffffff"
    outlines [ (1, "#00000088", 0, 0) ]

style auto_triangle:
    is auto_text
    font "DejaVuSans.ttf"

style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    xalign 1.0
    yanchor 1.0
    ypos 0.945
    background Frame("gui/clean_ui/gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size
    color "#ffffff"
    outlines [ (1, "#00000088", 0, 0) ]

style skip_triangle:
    font "DejaVuSans.ttf"


screen notify(message, timer=3.25):

    zorder 205
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]":
            style "notify_text"

    timer timer action Hide("notify")

transform notify_appear:
    on show:
        alpha 0.0
        linear 0.25 alpha 1.0
    on hide:
        linear 0.5 alpha 0.0

style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    xalign 0.5
    yalign 0.0
    ypos 0
    xminimum 600
    yminimum 75
    background Frame("gui/clean_ui/gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")
    text_align 0.5
    xalign 0.5
    yalign 0.5
    color "#ffffff"
    outlines [ (1, "#00000088", 0, 0) ]



################################################################################
## Main and Game Menu Screens
################################################################################

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5
        spacing gui.navigation_spacing

        if main_menu:
            textbutton _("Start") action Start()
        else:
            textbutton _("Save") action ShowMenu("save")

        textbutton _("Load") action ShowMenu("load")
        textbutton _("Preferences") action ShowMenu("preferences")

        if _in_replay:
            textbutton _("End Replay") action EndReplay(confirm=True)
        elif not main_menu:
            textbutton _("Main Menu") action MainMenu()

        textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):
            textbutton _("Quit") action Quit(confirm=not main_menu)

style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


# Old default main menu (kept, but not used)
screen main_menu_old():
    tag menu
    add gui.main_menu_background
    frame:
        style "main_menu_frame"
    use navigation

style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text



screen game_menu(title="", scroll=None, yinitial=0.0, spacing=0, can_focus=True, show_footer=True):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add pref_game_menu_background()

    frame:
        style "game_menu_outer_frame"

        hbox:
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True

                        vbox:
                            spacing spacing
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True
                        side_yfill True
                        spacing spacing
                        transclude

                else:
                    transclude

    use navigation

    if show_footer:
        textbutton _("Return"):
            style "return_button"
            action Return()

        label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")

style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style history_window is empty
style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text
style history_label is gui_label
style history_label_text is gui_label_text
style history_rollback is gui_button
style history_rollback_text is gui_button_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    ypos gui.history_name_ypos
    xanchor gui.history_name_xalign
    xsize gui.history_name_width
    xminimum gui.history_name_width
    text_align gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    xminimum gui.history_text_width
    text_align gui.history_text_xalign
    layout "subtitle"

style history_label:
    xfill True

style history_label_text:
    xalign 0.5
    text_align 0.5

style history_rollback:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos



screen about():

    tag menu

    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:
            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


label history_screen:
    return


screen history():

    tag menu
    predict False

    use game_menu(_("History")):
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 20

            label _("History is disabled."):
                xalign 0.5

            textbutton _("Return"):
                xalign 0.5
                action Return()



screen save():
    tag menu
    use file_slots(_("Save"))

screen load():
    tag menu
    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))
    $ _slot_idle_bg = Transform(pref_slot_button_asset(), size=(gui.slot_button_width, gui.slot_button_height))
    $ _slot_hover_bg = Transform(pref_slot_button_asset(True), size=(gui.slot_button_width, gui.slot_button_height))

    use game_menu(title):

        fixed:
            order_reverse True

            button:
                style "page_label"
                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"
                xalign 0.5
                yalign 0.5
                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1

                    button:
                        action FileAction(slot)
                        background _slot_idle_bg
                        hover_background _slot_hover_bg
                        selected_background _slot_hover_bg
                        selected_hover_background _slot_hover_bg
                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            vbox:
                style_prefix "page"
                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5
                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Download Sync"):
                            action DownloadSync()
                            xalign 0.5



################################################################################
## Confirm Screen
################################################################################

transform confirm_panel_enter:
    alpha 0.0
    yoffset 24
    ease 0.25 alpha 1.0 yoffset 0

style confirm_frame:
    background None
    xpadding 90
    ypadding 62

style confirm_vbox:
    spacing 34

style confirm_prompt:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 56
    color "#f7f1d6"
    outlines [(2, "#00000088", 0, 0)]
    text_align 0.5
    xalign 0.5

style confirm_hbox:
    spacing 28
    xalign 0.5

style confirm_button:
    background "#1f1a12cc"
    hover_background "#6b5520dd"
    insensitive_background "#3b3428aa"
    xpadding 34
    ypadding 14
    xminimum 260

style confirm_button_text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 44
    color "#f6ebc8"
    hover_color "#fff7da"
    insensitive_color "#b7ad93"
    outlines [(1, "#00000099", 0, 0)]
    xalign 0.5
    text_align 0.5

screen confirm(message, yes_action, no_action=None):
    if not pref_visual_bool("pref_confirm_prompts", True):
        timer 0.01 action yes_action

    modal True
    zorder 200
    style_prefix "confirm"

    $ _confirm_msg = (message or "")
    $ _confirm_bg = "gui/menu/starlit_paws.png" if "starlit paws" in _confirm_msg.lower() else "gui/menu/exit.jpg"
    add Transform(_confirm_bg, xalign=0.5, yalign=0.5, fit="contain")
    add Solid("#00000066")

    frame at confirm_panel_enter:
        style "confirm_frame"
        xalign 0.5
        yalign 0.82
        xmaximum 1500

        vbox:
            style "confirm_vbox"

            text message style "confirm_prompt"

            if no_action is None:
                textbutton _("Confirm"):
                    action yes_action
                    xalign 0.5
            else:
                hbox:
                    style "confirm_hbox"

                    textbutton _("Yes"):
                        action yes_action

                    textbutton _("No"):
                        action no_action

    key "game_menu" action (no_action if no_action is not None else yes_action)


################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style "quick_menu"
            style_prefix "quick"

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"
screen komic_quick_icon_button(icon_name, action, alternate_action=None, selected=False, xsize=50, ysize=62, flipped=False, sensitive=True):
    $ _idle = pref_komic_quick_button_asset(icon_name)
    $ _hover = pref_komic_quick_button_asset(icon_name, hovered=True)
    $ _idle_transform = Transform(_idle, xsize=xsize, ysize=ysize, fit="contain", xzoom=(-1.0 if flipped else 1.0))
    $ _hover_transform = Transform(_hover, xsize=xsize, ysize=ysize, fit="contain", xzoom=(-1.0 if flipped else 1.0))

    button:
        xpadding 0
        ypadding 0
        xsize xsize
        ysize ysize
        sensitive sensitive
        action action
        if alternate_action is not None:
            alternate alternate_action
        selected selected
        background _idle_transform
        insensitive_background _idle_transform
        hover_background _hover_transform
        selected_background _hover_transform
        selected_hover_background _hover_transform
