# components/scrollbars.rpy
# Shared scrollbar styles/components for viewport/scroll areas.

style ui_vscrollbar is vbar:
    xsize gui.scrollbar_size
    bar_invert True
    # `vbar` uses top/bottom bar parts.
    top_bar Frame("gui/scrollbar/vertical_idle_bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    bottom_bar Frame("gui/scrollbar/vertical_idle_bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    hover_top_bar Frame("gui/scrollbar/vertical_hover_bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    hover_bottom_bar Frame("gui/scrollbar/vertical_hover_bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    # Thumb sprites.
    thumb Frame("gui/scrollbar/vertical_idle_thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    hover_thumb Frame("gui/scrollbar/vertical_hover_thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    # Also expose base_bar so this style can be reused with style inheritance.
    base_bar Frame("gui/scrollbar/vertical_idle_bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    hover_base_bar Frame("gui/scrollbar/vertical_hover_bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

    thumb_offset 13
    thumb_align 0.5
    top_gutter 13
    bottom_gutter 13

style ui_vscrollbar_komic is vbar:
    xsize 18
    bar_invert True
    top_bar Frame("gui/KOMIC/ScrollBars/vertical_idle_bar.png", 9, 9, 9, 9, tile=False)
    bottom_bar Frame("gui/KOMIC/ScrollBars/vertical_idle_bar.png", 9, 9, 9, 9, tile=False)
    hover_top_bar Frame("gui/KOMIC/ScrollBars/vertical_hover_bar.png", 9, 9, 9, 9, tile=False)
    hover_bottom_bar Frame("gui/KOMIC/ScrollBars/vertical_hover_bar.png", 9, 9, 9, 9, tile=False)
    thumb Frame("gui/KOMIC/ScrollBars/vertical_idle_thumb.png", 9, 9, 9, 9, tile=False)
    hover_thumb Frame("gui/KOMIC/ScrollBars/vertical_hover_thumb.png", 9, 9, 9, 9, tile=False)
    base_bar Frame("gui/KOMIC/ScrollBars/vertical_idle_bar.png", 9, 9, 9, 9, tile=False)
    hover_base_bar Frame("gui/KOMIC/ScrollBars/vertical_hover_bar.png", 9, 9, 9, 9, tile=False)
    thumb_offset 9
    thumb_align 0.5
    top_gutter 9
    bottom_gutter 9

screen ui_vscrollbar_for(viewport_id, style_name="ui_vscrollbar"):
    $ _style_name = "ui_vscrollbar_komic" if (style_name == "ui_vscrollbar" and pref_uses_komic_ui()) else style_name
    vbar value YScrollValue(viewport_id) style _style_name keyboard_focus False unscrollable gui.unscrollable
