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
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

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

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"

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


screen input(prompt):
    style_prefix "input"

    window:
        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action

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
            textbutton _("History") action ShowMenu("history")
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
        add gui.game_menu_background

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
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text



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



screen save():
    tag menu
    use file_slots(_("Save"))

screen load():
    tag menu
    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

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
