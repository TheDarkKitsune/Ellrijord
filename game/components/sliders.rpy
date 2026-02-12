# components/sliders.rpy
# Shared slider styles/components.

init -2 python:
    UI_SLIDER_THUMB_W = 22
    UI_SLIDER_THUMB_H = 30
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

style ui_slider_bar_fill is ui_slider_bar:
    left_bar Frame("gui/slider/horizontal_fill_bar.png", gui.slider_borders, tile=gui.slider_tile)
    right_bar Frame("gui/slider/horizontal_idle_bar.png", gui.slider_borders, tile=gui.slider_tile)
    hover_left_bar Frame("gui/slider/horizontal_fill_hover_bar.png", gui.slider_borders, tile=gui.slider_tile)
    hover_right_bar Frame("gui/slider/horizontal_hover_bar.png", gui.slider_borders, tile=gui.slider_tile)

screen ui_slider(value, style_name=None, variant="default", xpos=None, ypos=None, xsize=None, ysize=None, tooltip=None, hovered_action=None, unhovered_action=None):
    $ _style_name = style_name
    if _style_name is None:
        $ _style_name = "ui_slider_bar_fill" if variant == "fill" else "ui_slider_bar"

    $ _hover = hovered_action
    $ _unhover = unhovered_action
    $ _can_tip = hasattr(renpy.store, "set_pref_tooltip") and hasattr(renpy.store, "clear_pref_tooltip")
    if tooltip is not None and _can_tip:
        if _hover is None:
            $ _hover = Function(renpy.store.set_pref_tooltip, tooltip)
        if _unhover is None:
            $ _unhover = Function(renpy.store.clear_pref_tooltip)

    controller_bar value value style _style_name:
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
