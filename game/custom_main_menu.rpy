# custom_main_menu.rpy
# Uses:
#   gui/mainmenu_bg.png
#   gui/logo.png
#   gui/btn_idle.png
#   gui/btn_hover.png

init -2 python:
    BTN_ZOOM = 0.8

    BTN_SRC_W = 534
    BTN_SRC_H = 140

    BTN_W = int(BTN_SRC_W * BTN_ZOOM)
    BTN_H = int(BTN_SRC_H * BTN_ZOOM)

    BTN_DARKEN = -0.25

    TOGGLE_ZOOM = 0.35
    TOGGLE_W = int(BTN_SRC_W * TOGGLE_ZOOM)
    TOGGLE_H = int(BTN_SRC_H * TOGGLE_ZOOM)

    # Compatibility alias in case cached bytecode references MatrixColor.
    MatrixColor = im.MatrixColor


transform logo_bob:
    yoffset -60
    linear 1.6 yoffset -70
    linear 1.6 yoffset -60
    repeat

transform btn_idle_fx:
    zoom BTN_ZOOM
    yoffset -9

transform btn_hover_fx:
    zoom BTN_ZOOM
    yoffset -9
    linear 0.08 yoffset -3
    linear 0.08 yoffset -9

style mm_btn_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 34
    color "#ffffff"
    outlines [(3, "#6b3aa8", 0, 0)]
    kerning 2
    xalign 0.5
    yalign 0.5

transform text_hover_fx:
    yoffset 0
    linear 0.08 yoffset 6
    linear 0.08 yoffset 0

transform toggle_idle_fx:
    zoom TOGGLE_ZOOM

transform toggle_hover_fx:
    zoom TOGGLE_ZOOM

style mm_toggle_text is text:
    font "fonts/trotes/Trotes.ttf"
    size 22
    color "#ffffff"
    outlines [(3, "#6b3aa8", 0, 0)]
    xalign 0.5
    yalign 0.5


# ------------------------------------------------------------
# Falling petals/leaves (put image at: gui/petal.png)
# ------------------------------------------------------------
init -2:
    transform petal_fall(xstart=0.5, t=12.0, s=0.06, r=220, drift=0.06, delay=0.0):

        xalign xstart
        yalign -0.15
        zoom s
        rotate 0

        pause delay

        parallel:
            linear t yalign 1.15

        parallel:
            linear t xalign (xstart + drift)

        parallel:
            linear t rotate r

        repeat


screen menu_petals():
    # behind UI elements in this file
    zorder 2

    add "gui/petal.png" at petal_fall(xstart=0.05, t=11.0, s=0.055, r=220,  drift=0.06, delay=0.0)
    add "gui/petal.png" at petal_fall(xstart=0.12, t=13.0, s=0.050, r=-260, drift=0.07, delay=1.0)
    add "gui/petal.png" at petal_fall(xstart=0.20, t=12.0, s=0.060, r=240,  drift=0.06, delay=2.0)
    add "gui/petal.png" at petal_fall(xstart=0.28, t=14.0, s=0.052, r=280,  drift=0.08, delay=3.0)
    add "gui/petal.png" at petal_fall(xstart=0.36, t=10.5, s=0.060, r=-230, drift=0.06, delay=0.6)
    add "gui/petal.png" at petal_fall(xstart=0.44, t=12.8, s=0.050, r=300,  drift=0.07, delay=1.7)
    add "gui/petal.png" at petal_fall(xstart=0.52, t=11.5, s=0.062, r=-280, drift=0.06, delay=2.6)
    add "gui/petal.png" at petal_fall(xstart=0.60, t=15.0, s=0.052, r=260,  drift=0.08, delay=3.6)
    add "gui/petal.png" at petal_fall(xstart=0.68, t=10.8, s=0.058, r=230,  drift=0.06, delay=1.2)
    add "gui/petal.png" at petal_fall(xstart=0.76, t=13.5, s=0.050, r=-300, drift=0.08, delay=2.2)
    add "gui/petal.png" at petal_fall(xstart=0.84, t=12.3, s=0.058, r=290,  drift=0.06, delay=3.2)
    add "gui/petal.png" at petal_fall(xstart=0.92, t=14.5, s=0.052, r=-250, drift=0.07, delay=4.0)


# --- CLIPPED button that cannot overlap others, even if hover PNG is bigger ---
screen mm_png_button(label, action, use_alt=False):
    imagebutton:
        xsize BTN_W
        ysize BTN_H
        action action
        focus_mask True

        if use_alt:
            idle Fixed(
                Transform(im.MatrixColor("gui/btn_idle.png", im.matrix.brightness(BTN_DARKEN)), zoom=BTN_ZOOM),
                Text(label, style="mm_btn_text"),
                xsize=BTN_W,
                ysize=BTN_H
            )
            hover Fixed(
                Transform(im.MatrixColor("gui/btn_hover.png", im.matrix.brightness(BTN_DARKEN)), zoom=BTN_ZOOM),
                At(Text(label, style="mm_btn_text"), text_hover_fx),
                xsize=BTN_W,
                ysize=BTN_H
            )
        else:
            idle Fixed(
                At("gui/btn_idle.png", btn_idle_fx),
                Text(label, style="mm_btn_text"),
                xsize=BTN_W,
                ysize=BTN_H
            )
            hover Fixed(
                At("gui/btn_hover.png", btn_hover_fx),
                At(Text(label, style="mm_btn_text"), text_hover_fx),
                xsize=BTN_W,
                ysize=BTN_H
            )


screen main_menu():

    tag menu

    default mm_alt = False
    default mm_track = None

    python:
        desired = "audio/Shattered_Remains.mp3" if mm_alt else "audio/Magical_Hallways.mp3"
        if mm_track != desired:
            renpy.music.play(desired, channel="music", loop=True)
            mm_track = desired

    if mm_alt:
        add im.Scale("gui/mainmenu_bg2.png", 1920, 1080)
    else:
        add im.Scale("gui/mainmenu_bg.png", 1920, 1080)

    # Petals behind logo/buttons
    use menu_petals

    fixed:

        add Transform("gui/logo.png", zoom=0.80) at logo_bob:
            xalign 0.5
            yanchor 0.0
            ypos -250

        vbox:
            xalign 0.5
            yalign 0.96
            spacing 4

            use mm_png_button("NEW GAME", Start(), use_alt=mm_alt)
            use mm_png_button("CONTINUE", ShowMenu("load"), use_alt=mm_alt)
            use mm_png_button("SETTINGS", ShowMenu("preferences"), use_alt=mm_alt)
            use mm_png_button("EXIT", Quit(confirm=True), use_alt=mm_alt)

        imagebutton:
            xsize TOGGLE_W
            ysize TOGGLE_H
            xalign 0.98
            yalign 0.98
            action ToggleScreenVariable("mm_alt")
            focus_mask True

            idle Fixed(
                At("gui/btn_idle.png", toggle_idle_fx),
                Text("BG", style="mm_toggle_text"),
                xsize=TOGGLE_W,
                ysize=TOGGLE_H
            )
            hover Fixed(
                At("gui/btn_hover.png", toggle_hover_fx),
                Text("BG", style="mm_toggle_text"),
                xsize=TOGGLE_W,
                ysize=TOGGLE_H
            )

            
