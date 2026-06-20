################################################################################
## Initialization
################################################################################

init offset = -1


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
    timer 0.24 action SetScreenVariable("can_dismiss_line", True)
    key "dismiss" action If(can_dismiss_line, Return(), NullAction())
    $ _is_komic = pref_uses_komic_ui()
    $ _hc = pref_custom_high_contrast_enabled()
    $ _window_height = pref_dialogue_window_height()
    $ _dialogue_font = "DejaVuSans.ttf" if _is_komic else gui.text_font
    $ _name_font = "DejaVuSans.ttf" if _is_komic else gui.name_text_font
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

    window:
        id "window"
        ysize _window_height
        background pref_dialogue_window_background(width=_komic_canvas_width if _is_komic else 1526, height=_window_height)

        if _is_komic:
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
            if who is not None:
                window:
                    id "namebox"
                    style "namebox"
                    background pref_dialogue_namebox_background()
                    text who id "who"

            text what id "what":
                color pref_dialogue_text_color()
                ypos gui.dialogue_ypos
                xsize gui.dialogue_width
                size gui.text_size
                adjust_spacing False
                xpos gui.dialogue_xpos
                outlines ([ (2, "#000000d8", 0, 0) ] if _hc else [ ])

    $ _msgbox_btn_idle = "gui/hud/msgbox_btn.png"
    $ _msgbox_btn_hover = "gui/hud/msgbox_btn_hover.png" if renpy.loadable("gui/hud/msgbox_btn_hover.png") else ("gui/msgbox_btn hover.png" if renpy.loadable("gui/msgbox_btn hover.png") else _msgbox_btn_idle)
    $ _back_btn_idle = "gui/hud/back_btn.png"
    $ _back_btn_hover = "gui/hud/back_btn_hover.png" if renpy.loadable("gui/hud/back_btn_hover.png") else _back_btn_idle
    $ _bag_btn_idle = "gui/hud/Player_male_btn.png" if getattr(store, "mc_gender", "male") == "male" else "gui/hud/Player_female_btn.png"
    $ _bag_btn_hover = ("gui/hud/Player_male_btn_hover.png" if getattr(store, "mc_gender", "male") == "male" else "gui/hud/Player_female_btn_hover.png")
    $ _bag_btn_hover = _bag_btn_hover if renpy.loadable(_bag_btn_hover) else _bag_btn_idle
    $ _setting_btn_idle = "gui/hud/Settings_btn.png"
    $ _setting_btn_hover = "gui/hud/Settings_btn_hover.png" if renpy.loadable("gui/hud/Settings_btn_hover.png") else _setting_btn_idle

    fixed:
        xfill True
        yfill True

        imagebutton:
            xpos 1652
            ypos 24
            idle Transform(_bag_btn_idle, size=(101, 101))
            hover Transform(_bag_btn_hover, size=(101, 101))
            action ShowMenu("inventory_menu")

        imagebutton:
            xpos 1768
            ypos 24
            idle Transform(_setting_btn_idle, size=(101, 101))
            hover Transform(_setting_btn_hover, size=(101, 101))
            action ShowMenu("showmenu")

        if not _is_komic:
            imagebutton:
                xpos 1020
                ypos 1020
                idle Transform(_back_btn_idle, size=(27, 27))
                hover Transform(_back_btn_hover, size=(27, 27))
                insensitive Transform(_back_btn_idle, size=(27, 27))
                action If(renpy.can_rollback(), Rollback(), NullAction())

            button:
                style "msgbox_btn_button"
                xpos 1060
                ypos 1020
                xsize 98
                ysize 28
                background Transform(_msgbox_btn_idle, size=(98, 28))
                hover_background Transform(_msgbox_btn_hover, size=(98, 28))
                action Preference("auto-forward", "toggle")
                selected preferences.afm_enable
                text _("Auto") style "msgbox_btn_button_text"

            button:
                style "msgbox_btn_button"
                xpos 1170
                ypos 1020
                xsize 98
                ysize 28
                background Transform(_msgbox_btn_idle, size=(98, 28))
                hover_background Transform(_msgbox_btn_hover, size=(98, 28))
                action Skip() alternate Skip(fast=True, confirm=True)
                selected renpy.is_skipping()
                text _("Skip") style "msgbox_btn_button_text"

            button:
                style "msgbox_btn_button"
                xpos 1280
                ypos 1020
                xsize 98
                ysize 28
                background Transform(_msgbox_btn_idle, size=(98, 28))
                hover_background Transform(_msgbox_btn_hover, size=(98, 28))
                action ShowMenu('save')
                text _("Save") style "msgbox_btn_button_text"

            button:
                style "msgbox_btn_button"
                xpos 1390
                ypos 1020
                xsize 98
                ysize 28
                background Transform(_msgbox_btn_idle, size=(98, 28))
                hover_background Transform(_msgbox_btn_hover, size=(98, 28))
                action ShowMenu('load')
                text _("Load") style "msgbox_btn_button_text"

            button:
                style "msgbox_btn_button"
                xpos 1500
                ypos 1020
                xsize 98
                ysize 28
                background Transform(_msgbox_btn_idle, size=(98, 28))
                hover_background Transform(_msgbox_btn_hover, size=(98, 28))
                action HideInterface()
                text _("Hide") style "msgbox_btn_button_text"

    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


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
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Transform("gui/hud/msgbox_720p.png", size=(1526, 251), xalign=0.5, yalign=0.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height
    background Transform("gui/hud/msgbox_name_header_720p.png", size=(380, 78))
    padding gui.namebox_borders.padding

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
    color "#5f515a"

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
    $ _komic_canvas_width = 1920
    $ _komic_center_x = 960
    $ _komic_text_y = 92
    $ _komic_text_width = 1080
    $ _komic_text_size = 24
    $ _komic_text_outline = "#000000f2" if _hc else "#15394fb0"

    window:
        ysize pref_dialogue_window_height()
        background pref_dialogue_window_background(width=_komic_canvas_width if _is_komic else 1526, height=pref_dialogue_window_height())
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
            vbox:
                xanchor gui.dialogue_text_xalign
                xpos gui.dialogue_xpos
                xsize gui.dialogue_width
                ypos gui.dialogue_ypos

                text prompt style "input_prompt" color pref_dialogue_text_color()
                input id "input" color pref_dialogue_text_color()

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
    $ _choice_idle_bg = pref_button_surface(_choice_width, _choice_height, _choice_accent, _choice_selected_bg, base_color="#0c121cf2", hover_color="#131b28f4") if _hc else Transform(pref_choice_button_asset(), size=(_choice_width, _choice_height))
    $ _choice_hover_bg = pref_button_surface(_choice_width, _choice_height, _choice_accent, _choice_selected_bg, hovered=True, base_color="#0c121cf2", hover_color="#131b28f4") if _hc else Transform(pref_choice_button_asset(True), size=(_choice_width, _choice_height))
    $ _choice_text_color = pref_ui_text_color("button") if _hc else "#5f515a"
    $ _choice_text_hover = pref_ui_text_color("button_hover", _choice_accent) if _hc else "#5f515a"

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
    background Transform("gui/button/choice_label_720p.png", size=(1185, 80))
    hover_background Transform("gui/button/choice_label_hover_720p.png", size=(1185, 80))
    insensitive_background Transform("gui/button/choice_label_720p.png", size=(1185, 80))

style choice_button_text is default:
    properties gui.text_properties("choice_button")
    xalign 0.5
    yalign 0.5
    idle_color "#5f515a"
    hover_color "#5f515a"
    selected_idle_color "#5f515a"
    selected_hover_color "#5f515a"
    outlines [ ]


screen quick_menu():
    pass

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

    zorder 100
    style_prefix "auto"

    frame:
        has hbox

        text _("Auto-Forward")

        text u"\u25B8" at auto_blink(1.0) style "skip_triangle"

## This transform blinks the indicator arrow.
transform auto_blink(cycle):
    alpha 0.0
    linear 0.5 alpha 1.0
    pause 0.2
    linear 0.5 alpha 0.0
    pause (cycle - .4)
    repeat

style auto_hbox:
    spacing 9

style auto_frame:
    is empty
    ypos 15
    background Frame("#0008", 24, 8, 75, 8, tile=False)
    padding (24, 8, 75, 8)

style auto_text:
    size 24

style auto_triangle:
    is auto_text
    # This font includes the black right-pointing small triangle glyph.
    font "DejaVuSans.ttf"



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
    call screen history
    return


screen history():

    tag menu
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0):

        style_prefix "history"

        for h in _history_list:

            window:

                if gui.history_height:
                    ysize gui.history_height

                has fixed

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                text h.what:
                    style "history_text"
                    substitute False

                if h.rollback_identifier:
                    textbutton _("Rollback to Here"):
                        style "history_rollback"
                        action RollbackToIdentifier(h.rollback_identifier)

        if not _history_list:
            label _("The dialogue history is empty.")



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
