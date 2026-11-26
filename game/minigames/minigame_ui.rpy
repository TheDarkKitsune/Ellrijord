# Shared temporary skin primitives, independent of any minigame rules.

init -2 python:
    ELL_MINIGAME_UI_DIR = "images/minigames/memory/ui/"

    def ell_minigame_ui(name):
        return ELL_MINIGAME_UI_DIR + name + ".png"


style ell_minigame_body is text:
    font "DejaVuSans.ttf"
    size 23
    color "#FFF1DB"

style ell_memory_caption is ell_minigame_body:
    size 17
    color "#A58AC5"
    kerning 1.2

style ell_minigame_title is inv_title:
    color "#FFF1DB"
    outlines [(1, "#30243E", 0, 1)]

style ell_minigame_button_text is ell_minigame_body:
    size 21
    color "#FFF1DB"
    hover_color "#ffffff"
    insensitive_color "#a798af"


transform ell_minigame_button_hover:
    on idle:
        ease 0.15 yoffset 0
    on hover:
        ease 0.15 yoffset -3



screen ell_minigame_button(caption, action, icon=None, width=280, height=64, button_id=None, disabled=False):
    button at ell_minigame_button_hover:
        if button_id is not None:
            id button_id
        xysize (width, height)
        padding (18, 10)
        background Frame(ell_minigame_ui("button"), 36, 36)
        hover_background Frame(ell_minigame_ui("button_hover"), 36, 36)
        insensitive_background Frame(ell_minigame_ui("button_disabled"), 36, 36)
        sensitive not disabled
        action action
        hbox:
            align (0.5, 0.5)
            spacing 12
            if icon:
                add Transform(ell_minigame_ui("icon_" + icon), xysize=(32, 32)) yalign 0.5
            text caption style "ell_minigame_button_text" yalign 0.5


screen ell_minigame_icon_button(icon, action, tip, button_id):
    button at ell_minigame_button_hover:
        id button_id
        xysize (58, 58)
        padding (11, 11)
        background Frame(ell_minigame_ui("button"), 36, 36)
        hover_background Frame(ell_minigame_ui("button_hover"), 36, 36)
        tooltip tip
        alt tip
        action action
        add Transform(ell_minigame_ui("icon_" + icon), xysize=(36, 36))


