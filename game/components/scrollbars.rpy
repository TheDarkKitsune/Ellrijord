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

screen ui_vscrollbar_for(viewport_id, style_name="ui_vscrollbar"):
    vbar value YScrollValue(viewport_id) style style_name keyboard_focus False unscrollable gui.unscrollable
