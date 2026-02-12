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

transform text_idle_fx(y=-9, adjust=6):
    yoffset (y + adjust)

transform text_hover_fx(y=-9, adjust=6):
    yoffset (y + adjust)
    linear 0.08 yoffset (y + adjust + 6)
    linear 0.08 yoffset (y + adjust)


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


screen ui_png_button(label, action, zoom=0.8, text_style="ui_btn_text", use_alt=False, selected=False, disabled=False, yoffset=-9, hovered_action=None, unhovered_action=None, tooltip=None, button_id=None):
    $ btn_w = int(BTN_SRC_W * zoom)
    $ btn_h = int(BTN_SRC_H * zoom)
    $ text_adjust = int(round(11 * (zoom / 0.8)))
    # Ren'Py 8.5 matrixcolor is incompatible with legacy im.matrix objects.
    # Keep alt mode stable by using the same assets unless dedicated dark PNGs are added.
    $ idle_disp = "gui/btn_idle.png"
    $ hover_disp = "gui/btn_hover.png"
    $ disabled_disp = "gui/btn_disabled.png"
    $ idle_render = disabled_disp if selected else idle_disp
    $ hover_render = disabled_disp if selected else hover_disp
    $ hover_actions = ([hovered_action] if hovered_action is not None else [])
    $ unhover_actions = ([unhovered_action] if unhovered_action is not None else [])

    imagebutton:
        if button_id is not None:
            id button_id
        xsize btn_w
        ysize btn_h
        action action
        selected selected
        sensitive (not disabled)
        focus_mask True
        if tooltip:
            tooltip tooltip
        hovered hover_actions
        unhovered unhover_actions

        idle Fixed(
            At(idle_render, btn_idle_fx(zoom, yoffset)),
            At(
                Text(label, style=text_style, xsize=btn_w, ysize=btn_h, xalign=0.5, yalign=0.5, text_align=0.5),
                text_idle_fx(yoffset, text_adjust)
            ),
            xsize=btn_w,
            ysize=btn_h
        )
        hover Fixed(
            At(hover_render, btn_hover_fx(zoom, yoffset)),
            At(
                Text(label, style=text_style, xsize=btn_w, ysize=btn_h, xalign=0.5, yalign=0.5, text_align=0.5),
                text_hover_fx(yoffset, text_adjust)
            ),
            xsize=btn_w,
            ysize=btn_h
        )
        insensitive Fixed(
            At(disabled_disp, btn_idle_fx(zoom, yoffset)),
            At(
                Text(label, style=text_style, xsize=btn_w, ysize=btn_h, xalign=0.5, yalign=0.5, text_align=0.5),
                text_idle_fx(yoffset, text_adjust)
            ),
            xsize=btn_w,
            ysize=btn_h
        )


screen ui_rect_icon_button(icon, action, size=68, bg="#2a2836", hover_overlay="#f003", tooltip=None, hovered_action=None, unhovered_action=None, button_id=None):
    $ _hover_actions = ([hovered_action] if hovered_action is not None else [])
    $ _unhover_actions = ([unhovered_action] if unhovered_action is not None else [])
    imagebutton:
        if button_id is not None:
            id button_id
        xysize (size, size)
        action action
        if tooltip:
            tooltip tooltip
        hovered _hover_actions
        unhovered _unhover_actions

        idle Fixed(
            Solid(bg),
            Transform(icon, xysize=(size, size)),
            xsize=size,
            ysize=size
        )
        hover Fixed(
            Solid(bg),
            Transform(icon, xysize=(size, size)),
            Solid(hover_overlay),
            xsize=size,
            ysize=size
        )


screen ui_rect_text_button(label, action, width=68, height=68, bg="#2a2836", hover_bg="#ff8335", text_style="pref_setting_btn_text", tooltip=None, hovered_action=None, unhovered_action=None, button_id=None):
    $ _hover_actions = ([hovered_action] if hovered_action is not None else [])
    $ _unhover_actions = ([unhovered_action] if unhovered_action is not None else [])
    imagebutton:
        if button_id is not None:
            id button_id
        xysize (width, height)
        action action
        if tooltip:
            tooltip tooltip
        hovered _hover_actions
        unhovered _unhover_actions

        idle Fixed(
            Solid(bg),
            Text(label, style=text_style, xsize=width, ysize=height, xalign=0.5, yalign=0.5, text_align=0.5),
            xsize=width,
            ysize=height
        )
        hover Fixed(
            Solid(hover_bg),
            Text(label, style=text_style, xsize=width, ysize=height, xalign=0.5, yalign=0.5, text_align=0.5),
            xsize=width,
            ysize=height
        )


screen ui_news_tile_button(label, action, image=None, width=300, height=180, selected=False, bg="#3a3152", hover_bg="#4a3a6a", text_style="news_tile_text"):
    button:
        xsize width
        ysize height
        action action
        selected selected
        background Solid(bg)
        hover_background Solid(hover_bg)

        if image and renpy.loadable(image):
            add Transform(image, xsize=(width - 16), ysize=(height - 50), fit="cover", xalign=0.5, yalign=0.15)
        else:
            add Solid("#ffffff18") xsize (width - 40) ysize (height - 60) xalign 0.5 yalign 0.35

        text label style text_style
