# components/buttons.rpy
# Shared PNG button styles, transforms, and screen helpers.

init -2 python:
    BTN_SRC_W = 168
    BTN_SRC_H = 26
    BTN_VISUAL_SCALE = 4
    BTN_HOVER_BOUNCE = 4
    BTN_BORDER_X = 10
    BTN_BORDER_Y = 13


transform btn_idle_fx(z=1.0, y=0):
    zoom z
    yoffset y

transform btn_hover_fx(z=1.0, y=0, bounce=BTN_HOVER_BOUNCE):
    zoom z
    yoffset y
    linear 0.08 yoffset (y + bounce)
    linear 0.08 yoffset y


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


screen ui_png_button(label, action, zoom=1, xsize=None, ysize=None, text_style="ui_btn_text", use_alt=False, selected=False, disabled=False, yoffset=0, hovered_action=None, unhovered_action=None, tooltip=None, button_id=None, left_icon=None, left_icon_size=None, left_icon_xpad=12):
    $ scale = zoom * BTN_VISUAL_SCALE
    $ btn_w = int(BTN_SRC_W * scale) if xsize is None else int(xsize)
    $ btn_h = int(BTN_SRC_H * scale) if ysize is None else int(ysize)
    $ idle_disp = "gui/btn_idle.png"
    $ hover_disp = "gui/btn_hover.png"
    $ disabled_disp = "gui/btn_disabled.png"
    $ idle_render = disabled_disp if (selected or disabled) else idle_disp
    $ hover_render = disabled_disp if (selected or disabled) else hover_disp
    $ idle_img = Transform(Frame(idle_render, BTN_BORDER_X, BTN_BORDER_Y, BTN_BORDER_X, BTN_BORDER_Y, tile=False), xsize=btn_w, ysize=btn_h)
    $ hover_img = Transform(Frame(hover_render, BTN_BORDER_X, BTN_BORDER_Y, BTN_BORDER_X, BTN_BORDER_Y, tile=False), xsize=btn_w, ysize=btn_h)
    $ disabled_img = Transform(Frame(disabled_disp, BTN_BORDER_X, BTN_BORDER_Y, BTN_BORDER_X, BTN_BORDER_Y, tile=False), xsize=btn_w, ysize=btn_h)
    $ hover_actions = ([hovered_action] if hovered_action is not None else [])
    $ unhover_actions = ([unhovered_action] if unhovered_action is not None else [])
    $ icon_sz = int(left_icon_size) if left_icon_size is not None else int(btn_h * 0.62)
    $ icon_x = int(left_icon_xpad)
    $ icon_y = int((btn_h - icon_sz) / 2)
    $ icon_disp = Transform(left_icon, xsize=icon_sz, ysize=icon_sz, xpos=icon_x, ypos=icon_y) if left_icon is not None else Null(width=0, height=0)

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
            At(idle_img, btn_idle_fx(1.0, yoffset)),
            At(Text(label, style=text_style, xsize=btn_w, ysize=btn_h, xalign=0.5, yalign=0.5, text_align=0.5), btn_idle_fx(1.0, yoffset)),
            At(icon_disp, btn_idle_fx(1.0, yoffset)),
            xsize=btn_w,
            ysize=btn_h
        )
        hover Fixed(
            At(hover_img, btn_hover_fx(1.0, yoffset)),
            At(Text(label, style=text_style, xsize=btn_w, ysize=btn_h, xalign=0.5, yalign=0.5, text_align=0.5), btn_hover_fx(1.0, yoffset)),
            At(icon_disp, btn_hover_fx(1.0, yoffset)),
            xsize=btn_w,
            ysize=btn_h
        )
        insensitive Fixed(
            At(disabled_img, btn_idle_fx(1.0, yoffset)),
            At(Text(label, style=text_style, xsize=btn_w, ysize=btn_h, xalign=0.5, yalign=0.5, text_align=0.5), btn_idle_fx(1.0, yoffset)),
            At(icon_disp, btn_idle_fx(1.0, yoffset)),
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
