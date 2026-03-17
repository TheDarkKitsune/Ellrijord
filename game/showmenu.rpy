################################################################################
# ELLRIJORD - CUSTOM SHOWMENU / PAUSE MENU
################################################################################

transform showmenu_panel_enter:
    alpha 0.0
    xoffset -30
    ease 0.25 alpha 1.0 xoffset 0

transform showmenu_button_hover:
    on idle:
        alpha 0.96
    on hover:
        alpha 1.0
        ease 0.12


style showmenu_frame:
    background "#0b1020cc"
    xpadding 38
    ypadding 32

style showmenu_vbox:
    spacing 12

style showmenu_title:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 42
    color "#f3f6ff"
    outlines [(2, "#7c8cff88", 0, 0)]
    xalign 0.5

style showmenu_subtitle:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 20
    color "#cfd8ffcc"
    xalign 0.5

style showmenu_button:
    background None
    hover_background "#ffffff10"
    xpadding 12
    ypadding 8
    xfill True

style showmenu_button_text:
    font "fonts/cinzel/Cinzel-Bold.otf"
    size 30
    color "#dfe7ff"
    hover_color "#ffffff"
    selected_color "#ffffff"
    outlines [(1, "#4a5fcf88", 0, 0)]


screen showmenu():
    modal True

    frame at showmenu_panel_enter:
        style "showmenu_frame"
        xalign 0.5
        yalign 0.5
        xmaximum 520

        vbox:
            style "showmenu_vbox"

            text _("PAUSE MENU") style "showmenu_title"
            text _("Ellrijord: Tales Of Light And Void") style "showmenu_subtitle"

            null height 10

            textbutton _("Return to Game"):
                style "showmenu_button"
                text_style "showmenu_button_text"
                at showmenu_button_hover
                action Hide("showmenu")

            textbutton _("Save Game"):
                style "showmenu_button"
                text_style "showmenu_button_text"
                at showmenu_button_hover
                action ShowMenu("save")

            textbutton _("Load Game"):
                style "showmenu_button"
                text_style "showmenu_button_text"
                at showmenu_button_hover
                action ShowMenu("load")

            if renpy.has_screen("codex"):
                textbutton _("Codex / References"):
                    style "showmenu_button"
                    text_style "showmenu_button_text"
                    at showmenu_button_hover
                    action ShowMenu("codex")

            textbutton _("Inventory"):
                style "showmenu_button"
                text_style "showmenu_button_text"
                at showmenu_button_hover
                action ShowMenu("inventory_menu")

            textbutton _("Settings"):
                style "showmenu_button"
                text_style "showmenu_button_text"
                at showmenu_button_hover
                action ShowMenu("preferences")

            textbutton _("Main Menu"):
                style "showmenu_button"
                text_style "showmenu_button_text"
                at showmenu_button_hover
                action MainMenu(confirm=True)

            if renpy.variant("pc"):
                textbutton _("Quit"):
                    style "showmenu_button"
                    text_style "showmenu_button_text"
                    at showmenu_button_hover
                    action Quit(confirm=True)

    key "game_menu" action Hide("showmenu")


init -10 python:
    # Make Esc/right-click open this as an overlay over the current scene.
    config.game_menu_action = Show("showmenu")
