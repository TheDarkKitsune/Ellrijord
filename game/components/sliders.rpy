# components/sliders.rpy
# Shared slider styles/components.

init -2 python:
    UI_SLIDER_THUMB_W = 36
    UI_SLIDER_THUMB_H = 36
    UI_SLIDER_THUMB_YOFFSET = 0

style ui_slider_bar is slider:
    xsize 200
    ysize 36
    base_bar Frame("gui/slider/horizontal_idle_bar.png", gui.slider_borders, tile=gui.slider_tile)
    hover_base_bar Frame("gui/slider/horizontal_hover_bar.png", gui.slider_borders, tile=gui.slider_tile)
    # Render a bar patch behind the thumb so transparent thumb pixels don't punch holes.
    thumb Fixed(
        Transform("gui/slider/horizontal_idle_thumb.png", xsize=UI_SLIDER_THUMB_W, ysize=UI_SLIDER_THUMB_H),
        xsize=UI_SLIDER_THUMB_W,
        ysize=UI_SLIDER_THUMB_H
    )
    hover_thumb Fixed(
        Transform("gui/slider/horizontal_hover_thumb.png", xsize=UI_SLIDER_THUMB_W, ysize=UI_SLIDER_THUMB_H),
        xsize=UI_SLIDER_THUMB_W,
        ysize=UI_SLIDER_THUMB_H
    )
    thumb_offset 18
    thumb_align 0.5
    right_gutter 18
    left_gutter 18

style ui_slider_bar_komic is slider:
    xsize 200
    ysize 36
    base_bar Frame("gui/KOMIC/Sliders/horizontal_idle_bar.png", 18, 14, 18, 14, tile=False)
    hover_base_bar Frame("gui/KOMIC/Sliders/horizontal_hover_bar.png", 18, 14, 18, 14, tile=False)
    thumb Fixed(
        Transform("gui/KOMIC/Sliders/horizontal_idle_thumb.png", xsize=15, ysize=38),
        xsize=15,
        ysize=38
    )
    hover_thumb Fixed(
        Transform("gui/KOMIC/Sliders/horizontal_hover_thumb.png", xsize=15, ysize=38),
        xsize=15,
        ysize=38
    )
    thumb_offset 7
    thumb_align 0.5
    right_gutter 8
    left_gutter 8

style ui_slider_bar_fill is ui_slider_bar:
    left_bar Frame("gui/slider/horizontal_fill_bar.png", gui.slider_borders, tile=gui.slider_tile)
    right_bar Frame("gui/slider/horizontal_idle_bar.png", gui.slider_borders, tile=gui.slider_tile)
    hover_left_bar Frame("gui/slider/horizontal_fill_hover_bar.png", gui.slider_borders, tile=gui.slider_tile)
    hover_right_bar Frame("gui/slider/horizontal_hover_bar.png", gui.slider_borders, tile=gui.slider_tile)

style ui_slider_bar_fill_komic is ui_slider_bar_komic:
    left_bar Frame("gui/KOMIC/Sliders/horizontal_idle_bar.png", 18, 14, 18, 14, tile=False)
    right_bar Frame("gui/KOMIC/Sliders/horizontal_idle_bar.png", 18, 14, 18, 14, tile=False)
    hover_left_bar Frame("gui/KOMIC/Sliders/horizontal_hover_bar.png", 18, 14, 18, 14, tile=False)
    hover_right_bar Frame("gui/KOMIC/Sliders/horizontal_hover_bar.png", 18, 14, 18, 14, tile=False)

style ui_slider_bar_contrast is slider:
    xsize 200
    ysize 36
    base_bar Frame(Solid("#3d4a60"), 6, 6, 6, 6, tile=False)
    hover_base_bar Frame(Solid("#4b5971"), 6, 6, 6, 6, tile=False)
    thumb Fixed(
        Transform(Solid("#fff8df"), xsize=24, ysize=38),
        Transform(Solid("#0d1117"), xpos=2, ypos=2, xsize=20, ysize=34),
        Transform(Solid("#fff8df"), xpos=8, ypos=6, xsize=8, ysize=26),
        xsize=24,
        ysize=38
    )
    hover_thumb Fixed(
        Transform(Solid("#ffffff"), xsize=24, ysize=38),
        Transform(Solid("#0d1117"), xpos=2, ypos=2, xsize=20, ysize=34),
        Transform(Solid("#ffffff"), xpos=8, ypos=6, xsize=8, ysize=26),
        xsize=24,
        ysize=38
    )
    thumb_offset 12
    thumb_align 0.5
    right_gutter 12
    left_gutter 12

style ui_slider_bar_fill_contrast is ui_slider_bar_contrast:
    left_bar Frame(Solid("#ffe07f"), 6, 6, 6, 6, tile=False)
    right_bar Frame(Solid("#485871"), 6, 6, 6, 6, tile=False)
    hover_left_bar Frame(Solid("#fff1ba"), 6, 6, 6, 6, tile=False)
    hover_right_bar Frame(Solid("#586986"), 6, 6, 6, 6, tile=False)

screen ui_slider(value, style_name=None, variant="default", xpos=None, ypos=None, xsize=None, ysize=None, tooltip=None, hovered_action=None, unhovered_action=None, button_id=None, use_controller_bar=False):
    $ _style_name = style_name
    if _style_name is None:
        $ _style_name = "ui_slider_bar_fill" if variant == "fill" else "ui_slider_bar"
    if pref_custom_high_contrast_enabled():
        $ _style_name = {
            "pref_bar": "ui_slider_bar_fill_contrast",
            "ui_slider_bar": "ui_slider_bar_contrast",
            "ui_slider_bar_fill": "ui_slider_bar_fill_contrast",
            "ui_slider_bar_komic": "ui_slider_bar_fill_contrast",
            "ui_slider_bar_fill_komic": "ui_slider_bar_fill_contrast",
        }.get(_style_name, _style_name)
    elif pref_uses_komic_ui():
        $ _style_name = {
            "pref_bar": "ui_slider_bar_fill_komic",
            "ui_slider_bar": "ui_slider_bar_komic",
            "ui_slider_bar_fill": "ui_slider_bar_fill_komic",
        }.get(_style_name, _style_name)

    $ _hover = hovered_action
    $ _unhover = unhovered_action
    $ _can_tip = hasattr(renpy.store, "set_pref_tooltip") and hasattr(renpy.store, "clear_pref_tooltip")
    if tooltip is not None and _can_tip:
        if _hover is None:
            $ _hover = Function(renpy.store.set_pref_tooltip, tooltip)
        if _unhover is None:
            $ _unhover = Function(renpy.store.clear_pref_tooltip)

    $ _is_adjustment = hasattr(value, "value") and hasattr(value, "change") and hasattr(value, "range")

    if use_controller_bar:
        if _is_adjustment:
            controller_bar adjustment value style _style_name:
                if button_id is not None:
                    id button_id
                if xpos is not None:
                    xpos xpos
                if ypos is not None:
                    ypos ypos
                if xsize is not None:
                    xsize xsize
                if ysize is not None:
                    ysize ysize
                if _hover is not None:
                    hovered _hover
                if _unhover is not None:
                    unhovered _unhover
        else:
            controller_bar value value style _style_name:
                if button_id is not None:
                    id button_id
                if xpos is not None:
                    xpos xpos
                if ypos is not None:
                    ypos ypos
                if xsize is not None:
                    xsize xsize
                if ysize is not None:
                    ysize ysize
                if _hover is not None:
                    hovered _hover
                if _unhover is not None:
                    unhovered _unhover
    else:
        if _is_adjustment:
            bar adjustment value style _style_name:
                if button_id is not None:
                    id button_id
                if xpos is not None:
                    xpos xpos
                if ypos is not None:
                    ypos ypos
                if xsize is not None:
                    xsize xsize
                if ysize is not None:
                    ysize ysize
                if _hover is not None:
                    hovered _hover
                if _unhover is not None:
                    unhovered _unhover
        else:
            bar value value style _style_name:
                if button_id is not None:
                    id button_id
                if xpos is not None:
                    xpos xpos
                if ypos is not None:
                    ypos ypos
                if xsize is not None:
                    xsize xsize
                if ysize is not None:
                    ysize ysize
                if _hover is not None:
                    hovered _hover
                if _unhover is not None:
                    unhovered _unhover
