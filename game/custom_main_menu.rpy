# custom_main_menu.rpy
# Uses:
#   gui/mainmenu_bg.png
#   gui/logo.png
#   gui/btn_idle.png
#   gui/btn_hover.png

init -2 python:
    BTN_ZOOM = 1

    TOGGLE_ZOOM = 0.35

    # Compatibility alias in case cached bytecode references MatrixColor.
    MatrixColor = im.MatrixColor

    if not hasattr(persistent, "mm_alt"):
        persistent.mm_alt = False

    def toggle_mm_alt():
        persistent.mm_alt = not bool(getattr(persistent, "mm_alt", False))
        renpy.save_persistent()
        renpy.restart_interaction()


transform logo_bob:
    yoffset -60
    linear 1.6 yoffset -70
    linear 1.6 yoffset -60
    repeat

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
screen main_menu():

    tag menu

    $ mm_alt = bool(getattr(persistent, "mm_alt", False))

    python:
        desired = "audio/Shattered_Remains.mp3" if mm_alt else "audio/Magical_Hallways.mp3"
        # This block can be evaluated many times during UI interactions.
        # if_changed=True prevents music from restarting on hover/scroll/etc.
        renpy.music.play(desired, channel="music", loop=True, if_changed=True)

    if mm_alt:
        add im.Scale("gui/mainmenu_bg2.png", 1920, 1080)
    else:
        add im.Scale("gui/mainmenu_bg.png", 1920, 1080)

    # Petals behind logo/buttons
    use menu_petals

    fixed:

        add Transform("gui/logo.png") at logo_bob:
            xalign 0.5
            yanchor 0.0
            ypos 100
            xsize 600
            ysize 500

        vbox:
            xalign 0.5
            yalign 0.96
            spacing 20

            use ui_png_button(L("mm_new_game"), Start(), xsize=672, ysize=104, text_style="ui_btn_text", use_alt=mm_alt, tooltip=L("mm_tip_new_game"))
            use ui_png_button(L("mm_continue"), ShowMenu("load"), xsize=672, ysize=104, text_style="ui_btn_text", use_alt=mm_alt, tooltip=L("mm_tip_continue"))
            use ui_png_button(L("mm_settings"), ShowMenu("preferences"), xsize=672, ysize=104, text_style="ui_btn_text", use_alt=mm_alt, tooltip=L("mm_tip_settings"))
            use ui_png_button(L("mm_exit"), Quit(confirm=True), xsize=672, ysize=104, text_style="ui_btn_text", use_alt=mm_alt, tooltip=L("mm_tip_exit"))

        fixed:
            xalign 0.05
            yalign 0.95
            xsize 200
            ysize 42

            hbox:
                spacing 10
                use ui_png_button(L("mm_news"), ShowMenu("news_updates"), xsize=200, ysize=42, text_style="ui_btn_text_small", use_alt=mm_alt, left_icon="gui/news_icon.png", left_icon_size=36, left_icon_xpad=5, tooltip=L("mm_tip_news"))
                use ui_png_button(L("mm_extra"), ShowMenu("extra_menu"), xsize=200, ysize=42, text_style="ui_btn_text_small", use_alt=mm_alt, left_icon="gui/extras_icon.png", left_icon_size=30, left_icon_xpad=5, tooltip=L("mm_tip_extra"))

        fixed:
            xalign 0.95
            yalign 0.95
            xsize 200
            ysize 42

            hbox:
                spacing 10
                use ui_png_button(
                    (L("mm_light_mode") if mm_alt else L("mm_dark_mode")),
                    Function(toggle_mm_alt),
                    xsize=200,
                    ysize=42,
                    text_style="ui_btn_text_small",
                    use_alt=mm_alt,
                    left_icon=("gui/lightmode_icon.png" if mm_alt else "gui/darkmode_icon.png"),
                    left_icon_size=30,
                    left_icon_xpad=5,
                    tooltip=(L("mm_tip_light_mode") if mm_alt else L("mm_tip_dark_mode"))
                )

                    
            
