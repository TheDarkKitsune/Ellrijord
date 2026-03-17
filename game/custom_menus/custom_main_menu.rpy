# custom_main_menu.rpy
# Uses:
#   gui/mainmenu_bg.png
#   gui/logo.png
#   gui/btn_idle.png
#   gui/btn_hover.png

default persistent.mm_mode = "light"
default persistent.mm_alt = False
default main_menu_last_announced_track = None
default main_menu_force_announce_track = None

init -2 python:
    BTN_ZOOM = 1

    TOGGLE_ZOOM = 0.35

    # Social links shown on main menu (left of mode toggle).
    SOCIAL_URL_ITCH = "https://enderfall.itch.io/"
    SOCIAL_URL_DISCORD = "https://discord.gg/YxXJpZK7nv"
    SOCIAL_URL_PATREON = "https://www.patreon.com/c/EnderFall/home"
    SOCIAL_URL_WEBSITE = "https://www.enderfall.co.uk/"

    # Compatibility alias in case cached bytecode references MatrixColor.
    MatrixColor = im.MatrixColor

    if not hasattr(persistent, "mm_mode"):
        persistent.mm_mode = "dark" if bool(getattr(persistent, "mm_alt", False)) else "light"

    if getattr(persistent, "mm_mode", "light") not in ("light", "dark", "twilight"):
        persistent.mm_mode = "light"

    persistent.mm_alt = (persistent.mm_mode != "light")

    def get_main_menu_mode():
        mode = getattr(persistent, "mm_mode", "light")
        if mode not in ("light", "dark", "twilight"):
            mode = "dark" if bool(getattr(persistent, "mm_alt", False)) else "light"
            persistent.mm_mode = mode
        persistent.mm_alt = (mode != "light")
        return mode

    def is_main_menu_alt():
        return get_main_menu_mode() != "light"

    def get_track_for_mode(mode):
        if mode == "twilight":
            if renpy.loadable("audio/unspoken_language.wav"):
                return "audio/unspoken_language.wav"
            if renpy.loadable("audio/rooftop_universe.wav"):
                return "audio/rooftop_universe.wav"
            return "audio/academy_window.wav"
        if mode == "dark":
            if renpy.loadable("audio/rooftop_universe.wav"):
                return "audio/rooftop_universe.wav"
            return "audio/academy_window.wav"
        if renpy.loadable("audio/academy_window.wav"):
            return "audio/academy_window.wav"
        return "audio/rooftop_universe.wav"

    def get_main_menu_track():
        return get_track_for_mode(get_main_menu_mode())

    def get_main_menu_bg_path():
        mode = get_main_menu_mode()
        if mode == "dark":
            preferred = "gui/mainmenu_bg2.png"
        elif mode == "twilight":
            preferred = "gui/mainmenu_bg3.png"
        else:
            preferred = "gui/mainmenu_bg.png"

        if renpy.loadable(preferred):
            return preferred
        return "gui/window_icon.png"

    def get_main_menu_toggle_label():
        mode = get_main_menu_mode()
        if mode == "light":
            return L("mm_light_mode")
        if mode == "dark":
            return L("mm_dark_mode")
        return L("mm_twilight_mode")

    def get_main_menu_toggle_tooltip():
        mode = get_main_menu_mode()
        if mode == "light":
            return L("mm_tip_dark_mode")
        if mode == "dark":
            return L("mm_tip_twilight_mode")
        return L("mm_tip_light_mode")

    def get_main_menu_current_mode_label():
        mode = get_main_menu_mode()
        if mode == "dark":
            return L("mm_dark_mode")
        if mode == "twilight":
            return L("mm_twilight_mode")
        return L("mm_light_mode")

    def get_main_menu_current_track_label():
        mode = get_main_menu_mode()
        if mode == "dark":
            return "Shattered Remains"
        if mode == "twilight":
            return "Unspoken Language"
        return "Magical Hallways"

    def get_track_label_from_path(path):
        if path == "audio/unspoken_language.wav":
            return "Unspoken Language"
        if path == "audio/rooftop_universe.wav":
            return "Rooftop Universe"
        if path == "audio/academy_window.wav":
            return "Academy Window"
        return str(path)

    def get_main_menu_now_playing_text(path):
        return "Now Playing: {0}".format(get_track_label_from_path(path))

    def get_main_menu_toggle_icon():
        mode = get_main_menu_mode()
        if mode == "light":
            return "gui/lightmode_icon.png"
        return "gui/darkmode_icon.png"

    def cycle_main_menu_mode():
        modes = ("light", "dark", "twilight")
        current = get_main_menu_mode()
        idx = modes.index(current)
        next_mode = modes[(idx + 1) % len(modes)]
        next_track = get_track_for_mode(next_mode)
        persistent.mm_mode = next_mode
        persistent.mm_alt = (next_mode != "light")
        renpy.music.play(next_track, channel="music", loop=True, if_changed=True, fadeout=0.0, fadein=0.0)
        main_menu_force_announce_track = next_track
        main_menu_last_announced_track = None
        renpy.save_persistent()
        renpy.restart_interaction()

# Backward-compat alias.
    def toggle_mm_alt():
        cycle_main_menu_mode()

style main_menu_social_caption is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 14
    color "#f4eaff"
    outlines [(2, "#2a1a44", 0, 0)]


transform logo_bob:
    yoffset -60
    linear 1.6 yoffset -70
    linear 1.6 yoffset -60
    repeat

transform main_menu_now_playing_fade:
    alpha 0.0
    linear 0.25 alpha 1.0
    pause 3.0
    linear 0.7 alpha 0.0

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


screen main_menu_now_playing(text):
    zorder 150
    text text at main_menu_now_playing_fade:
        style "ui_tooltip_text"
        xpos 30
        ypos 24
    timer 4.0 action Hide("main_menu_now_playing")


# --- CLIPPED button that cannot overlap others, even if hover PNG is bigger ---
screen main_menu():

    tag menu

    $ mm_mode = get_main_menu_mode()
    $ mm_alt = is_main_menu_alt()

    python:
        desired = get_main_menu_track()
        # This block can be evaluated many times during UI interactions.
        # if_changed=True prevents music from restarting on hover/scroll/etc.
        renpy.music.play(desired, channel="music", loop=True, if_changed=True, fadeout=0.0, fadein=0.0)
        announce_track = main_menu_force_announce_track if main_menu_force_announce_track is not None else desired
        if main_menu_last_announced_track != announce_track:
            renpy.hide_screen("main_menu_now_playing")
            renpy.show_screen("main_menu_now_playing", text=get_main_menu_now_playing_text(announce_track))
            main_menu_last_announced_track = announce_track
            main_menu_force_announce_track = None
        # Mark currently playing main-menu track as discovered for the music room.
        if "unlock_music_track" in globals():
            unlock_music_track(desired)

    add im.Scale(get_main_menu_bg_path(), 1920, 1080)

    # Petals behind logo/buttons (light mode only).
    if mm_mode == "light":
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
            spacing 8

            use ui_png_button(L("mm_new_game"), Start(), xsize=640, ysize=94, text_style="ui_btn_text", use_alt=mm_alt, tooltip=L("mm_tip_new_game"))
            use ui_png_button(L("mm_continue"), ShowMenu("load"), xsize=640, ysize=94, text_style="ui_btn_text", use_alt=mm_alt, tooltip=L("mm_tip_continue"))
            use ui_png_button(L("mm_settings"), ShowMenu("preferences"), xsize=640, ysize=94, text_style="ui_btn_text", use_alt=mm_alt, tooltip=L("mm_tip_settings"))
            use ui_png_button(L("mm_exit"), Quit(confirm=True), xsize=640, ysize=94, text_style="ui_btn_text", use_alt=mm_alt, tooltip=L("mm_tip_exit"))

        fixed:
            xalign 0.05
            yalign 0.95
            xsize 220
            ysize 48

            hbox:
                spacing 8
                use ui_png_button(L("mm_news"), ShowMenu("news_updates"), xsize=220, ysize=48, text_style="ui_btn_text_small", use_alt=mm_alt, left_icon="gui/news_icon.png", left_icon_size=36, left_icon_xpad=5, tooltip=L("mm_tip_news"))
                use ui_png_button(L("mm_extra"), ShowMenu("extra_menu"), xsize=220, ysize=48, text_style="ui_btn_text_small", use_alt=mm_alt, left_icon="gui/extras_icon.png", left_icon_size=30, left_icon_xpad=5, tooltip=L("mm_tip_extra"))

        fixed:
            xalign 0.95
            yalign 0.95
            xsize 220
            ysize 48

            hbox:
                spacing 12
                use ui_png_button(
                    get_main_menu_toggle_label(),
                    Function(cycle_main_menu_mode),
                    xsize=220,
                    ysize=48,
                    text_style="ui_btn_text_small",
                    use_alt=mm_alt,
                    left_icon=get_main_menu_toggle_icon(),
                    left_icon_size=30,
                    left_icon_xpad=5
                )

        # Social buttons: placed to the left of the mode toggle.
        fixed:
            xalign 0.87
            xoffset -25
            yalign 0.97
            xsize 420
            ysize 78

            hbox:
                spacing 10

                vbox:
                    spacing 2
                    use ui_rect_icon_button("gui/logos/itch_logo.png", OpenURL(SOCIAL_URL_ITCH), size=62, bg="#0000", hover_overlay="#ffffff22", tooltip="itch.io")
                    text "ITCH.IO" style "main_menu_social_caption" xalign 0.5

                vbox:
                    spacing 2
                    use ui_rect_icon_button("gui/logos/discord_logo.png", OpenURL(SOCIAL_URL_DISCORD), size=62, bg="#0000", hover_overlay="#ffffff22", tooltip="discord")
                    text "DISCORD" style "main_menu_social_caption" xalign 0.5

                vbox:
                    spacing 2
                    use ui_rect_icon_button("gui/logos/patreon_logo.png", OpenURL(SOCIAL_URL_PATREON), size=62, bg="#0000", hover_overlay="#ffffff22", tooltip="patreon")
                    text "PATREON" style "main_menu_social_caption" xalign 0.5

                vbox:
                    spacing 2
                    use ui_rect_icon_button("gui/logos/enderfall_logo.png", OpenURL(SOCIAL_URL_WEBSITE), size=62, bg="#0000", hover_overlay="#ffffff22", tooltip="website")
                    text "WEBSITE" style "main_menu_social_caption" xalign 0.5
