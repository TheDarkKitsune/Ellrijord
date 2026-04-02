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
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
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


screen ui_png_button(label, action, zoom=1, xsize=None, ysize=None, text_style="ui_btn_text", use_alt=False, selected=False, disabled=False, yoffset=0, hovered_action=None, unhovered_action=None, tooltip=None, button_id=None, left_icon=None, left_icon_size=None, left_icon_xpad=12, use_hover_asset=True, use_hover_bounce=True, disabled_uses_idle=False):
    $ scale = zoom * BTN_VISUAL_SCALE
    $ btn_w = int(BTN_SRC_W * scale) if xsize is None else int(xsize)
    $ btn_h = int(BTN_SRC_H * scale) if ysize is None else int(ysize)
    $ idle_disp = "gui/button/btn_idle.png"
    $ hover_disp = "gui/button/btn_hover.png"
    $ disabled_disp = "gui/button/btn_disabled.png"
    $ _disabled_render = (idle_disp if disabled_uses_idle else disabled_disp)
    $ idle_render = _disabled_render if (selected or disabled) else idle_disp
    $ hover_render = _disabled_render if (selected or disabled) else (hover_disp if use_hover_asset else idle_disp)
    $ idle_img = Transform(Frame(idle_render, BTN_BORDER_X, BTN_BORDER_Y, BTN_BORDER_X, BTN_BORDER_Y, tile=False), xsize=btn_w, ysize=btn_h)
    $ hover_img = Transform(Frame(hover_render, BTN_BORDER_X, BTN_BORDER_Y, BTN_BORDER_X, BTN_BORDER_Y, tile=False), xsize=btn_w, ysize=btn_h)
    $ disabled_img = Transform(Frame(_disabled_render, BTN_BORDER_X, BTN_BORDER_Y, BTN_BORDER_X, BTN_BORDER_Y, tile=False), xsize=btn_w, ysize=btn_h)
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
        if use_hover_bounce:
            hover Fixed(
                At(hover_img, btn_hover_fx(1.0, yoffset)),
                At(Text(label, style=text_style, xsize=btn_w, ysize=btn_h, xalign=0.5, yalign=0.5, text_align=0.5), btn_hover_fx(1.0, yoffset)),
                At(icon_disp, btn_hover_fx(1.0, yoffset)),
                xsize=btn_w,
                ysize=btn_h
            )
        else:
            hover Fixed(
                At(hover_img, btn_idle_fx(1.0, yoffset)),
                At(Text(label, style=text_style, xsize=btn_w, ysize=btn_h, xalign=0.5, yalign=0.5, text_align=0.5), btn_idle_fx(1.0, yoffset)),
                At(icon_disp, btn_idle_fx(1.0, yoffset)),
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
            Transform(icon, fit="contain", xsize=size, ysize=size, xalign=0.5, yalign=0.5),
            xsize=size,
            ysize=size
        )
        hover Fixed(
            Solid(bg),
            Transform(icon, fit="contain", xsize=size, ysize=size, xalign=0.5, yalign=0.5),
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


screen ui_news_tile_button(
    label,
    action,
    image=None,
    width=300,
    height=180,
    selected=False,
    bg="#3a3152",
    hover_bg="#4a3a6a",
    text_style="news_tile_text",
    image_xpad=0,
    image_ypad=0,
    image_mode="fit",
    image_x=0,
    image_y=0,
    image_zoom=1.0,
    image_width=None,
    image_height=None,
    image_fit="cover",
    image_xalign=0.5,
    image_yalign=0.5,
    label_band_h=48,
    label_bg="#00000022",
    use_hover_anim=False
):
    $ _label_band_h = max(0, int(label_band_h))
    $ _image_xpad = max(0, int(image_xpad))
    $ _image_ypad = max(0, int(image_ypad))
    $ _image_w = (max(1, int(image_width)) if image_width is not None else max(1, int(width - (_image_xpad * 2))))
    $ _default_image_h = max(1, int(height - _label_band_h - _image_ypad))
    $ _image_h = (max(1, int(image_height)) if image_height is not None else _default_image_h)
    $ _label_y = max(0, int(height - _label_band_h))
    button:
        xsize width
        ysize height
        action action
        selected selected
        if use_hover_anim:
            at card_interact_enabled
        background Solid(bg)
        hover_background Solid(hover_bg)

        fixed:
            xpos _image_xpad
            ypos _image_ypad
            xsize _image_w
            ysize _image_h
            clipping True
            if image and renpy.loadable(image):
                if image_mode == "manual":
                    add Transform(
                        image,
                        xoffset=int(image_x),
                        yoffset=int(image_y),
                        zoom=float(image_zoom),
                        xalign=image_xalign,
                        yalign=image_yalign
                    )
                else:
                    add Transform(image, xsize=_image_w, ysize=_image_h, fit=image_fit, xalign=image_xalign, yalign=image_yalign)
            else:
                add Solid("#ffffff18") xsize _image_w ysize _image_h

        if _label_band_h > 0:
            add Solid(label_bg) xpos 0 ypos _label_y xsize width ysize _label_band_h
        text label style text_style

