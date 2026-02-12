# components/sliders.rpy
# Shared slider styles/components.

transform ui_slider_thumb_fx:
    zoom 0.4
    yoffset 0

style ui_slider_bar is slider:
    xsize 200
    ysize 36
    base_bar Frame("gui/slider/horizontal_idle_bar.png", 32,18,32,18, tile=gui.slider_tile)
    hover_base_bar Frame("gui/slider/horizontal_hover_bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb At("gui/slider/horizontal_idle_thumb.png", ui_slider_thumb_fx)
    hover_thumb At("gui/slider/horizontal_idle_thumb.png", ui_slider_thumb_fx)
    thumb_offset (21, 21)

screen ui_slider(value, style_name="ui_slider_bar", xpos=None, ypos=None, xsize=None, ysize=None, tooltip=None, hovered_action=None, unhovered_action=None):
    $ _hover = hovered_action
    $ _unhover = unhovered_action
    $ _can_tip = hasattr(renpy.store, "set_pref_tooltip") and hasattr(renpy.store, "clear_pref_tooltip")
    if tooltip is not None and _can_tip:
        if _hover is None:
            $ _hover = Function(renpy.store.set_pref_tooltip, tooltip)
        if _unhover is None:
            $ _unhover = Function(renpy.store.clear_pref_tooltip)

    bar value value style style_name:
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
