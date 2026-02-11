# components/tooltips.rpy
# Simple mouse-follow tooltip displayable.

style ui_tooltip_frame is frame:
    background Frame("gui/btn_hover.png", 24, 24)
    padding (16, 10)

style ui_tooltip_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 13
    color "#ffffff"
    outlines [(2, "#6b3aa8", 0, 0)]

init -2 python:
    def get_focus_rect():
        try:
            focus = renpy.display.focus.get_focused()
            if focus is None:
                return None
            f_widget = getattr(focus, "widget", None)
            f_arg = getattr(focus, "arg", getattr(focus, "argument", None))
            for item in renpy.display.focus.focus_list:
                if getattr(item, "widget", None) is f_widget:
                    item_arg = getattr(item, "arg", getattr(item, "argument", None))
                    if f_arg is None or item_arg == f_arg:
                        return (item.x, item.y, item.w, item.h)
        except Exception:
            return None
        return None

    def get_rect_at_pos(x, y):
        try:
            for item in renpy.display.focus.focus_list:
                if x >= item.x and x <= (item.x + item.w) and y >= item.y and y <= (item.y + item.h):
                    return (item.x, item.y, item.w, item.h)
        except Exception:
            return None
        return None


screen ui_tooltip_from_rect(text, rect, ypad=12):
    layer "overlay"
    zorder 200

    if rect:
        timer 0.02 repeat True action NullAction()
        $ rx, ry, rw, rh = rect
        $ rx = int(rx)
        $ ry = int(ry)
        $ rw = int(rw)
        $ rh = int(rh)
        frame:
            background Frame("gui/textbox.png", 20, 20)
            xpos rx
            ypos (ry + rh + ypad)
            xsize rw
            padding (16, 8)
            if text:
                text text style "ui_tooltip_text" xmaximum (rw - 32) text_align 0.5
