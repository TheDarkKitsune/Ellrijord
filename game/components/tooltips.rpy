# components/tooltips.rpy
# Simple mouse-follow tooltip displayable.

style ui_tooltip_frame is frame:
    background Frame("gui/btn_hover.png", 24, 24)
    padding (16, 10)

style ui_tooltip_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 20
    color "#ffffff"
    outlines [(3, "#6b3aa8", 0, 0)]


screen ui_tooltip_at(text, pos, xpad=18, ypad=18):
    zorder 200
    if text and pos:
        $ mx, my = pos
        frame:
            style "ui_tooltip_frame"
            xpos (mx + xpad)
            ypos (my + ypad)
            xanchor 0.0
            yanchor 0.0
            text text style "ui_tooltip_text"
