# components/buttons.rpy
# Shared PNG button styles, transforms, and screen helpers.

init -2 python:
    BTN_SRC_W = 534
    BTN_SRC_H = 140
    BTN_DARKEN = -0.25


transform btn_idle_fx(z=1.0, y=-9):
    zoom z
    yoffset y

transform btn_hover_fx(z=1.0, y=-9):
    zoom z
    yoffset y
    linear 0.08 yoffset (y + 6)
    linear 0.08 yoffset y

transform text_hover_fx:
    yoffset 0
    linear 0.08 yoffset 6
    linear 0.08 yoffset 0


style ui_btn_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 34
    color "#ffffff"
    outlines [(3, "#6b3aa8", 0, 0)]
    kerning 2
    xalign 0.5
    yalign 0.5

style ui_btn_text_tab is ui_btn_text:
    size 26

style ui_btn_text_small is ui_btn_text:
    size 22


screen ui_png_button(label, action, zoom=0.8, text_style="ui_btn_text", use_alt=False, selected=False, yoffset=-9, hovered_action=None, unhovered_action=None, tooltip=None):
    $ btn_w = int(BTN_SRC_W * zoom)
    $ btn_h = int(BTN_SRC_H * zoom)
    $ idle_disp = im.MatrixColor("gui/btn_idle.png", im.matrix.brightness(BTN_DARKEN)) if use_alt else "gui/btn_idle.png"
    $ hover_disp = im.MatrixColor("gui/btn_hover.png", im.matrix.brightness(BTN_DARKEN)) if use_alt else "gui/btn_hover.png"
    $ idle_render = hover_disp if selected else idle_disp
    $ hover_actions = ([hovered_action] if hovered_action is not None else [])
    $ unhover_actions = ([unhovered_action] if unhovered_action is not None else [])

    imagebutton:
        xsize btn_w
        ysize btn_h
        action action
        selected selected
        focus_mask True
        if tooltip:
            tooltip tooltip
        hovered hover_actions
        unhovered unhover_actions

        idle Fixed(
            At(idle_render, btn_idle_fx(zoom, yoffset)),
            Text(label, style=text_style),
            xsize=btn_w,
            ysize=btn_h
        )
        hover Fixed(
            At(hover_disp, btn_hover_fx(zoom, yoffset)),
            At(Text(label, style=text_style), text_hover_fx),
            xsize=btn_w,
            ysize=btn_h
        )
