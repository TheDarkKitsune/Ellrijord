# custom_preferences.rpy
# Minimal stub to avoid legacy pref_tab crashes while focusing on News screen.

screen preferences():
    tag menu

    add "gui/game_menu.png"

    frame:
        background Solid("#2b2440")
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 320
        padding (30, 24)

        vbox:
            spacing 16
            text "Preferences are temporarily disabled." style "ui_btn_text"
            text "Use the cloud icon on the main menu for News." style "ui_btn_text_small"
            use ui_png_button("BACK", Return(), zoom=0.6, text_style="ui_btn_text_small")
