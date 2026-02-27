# custom_credits_menu.rpy
# Standalone credits board screen used by Extras -> Credits.

default credits_entries = [
    {"role": "BGM", "name": "@AlterClad", "avatar": None, "details": "Add contributor details here."},
    {"role": "BGM", "name": "@AlissOnTheMoon", "avatar": None, "details": "Add contributor details here."},
    {"role": "BGM", "name": "@MetalWeebcore", "avatar": None, "details": "Add contributor details here."},
    {"role": "BGM", "name": "@alorem123", "avatar": None, "details": "Add contributor details here."},
    {"role": "LOGO", "name": "@Erminael", "avatar": None, "details": "Add contributor details here."},
    {"role": "LORE", "name": "@EdmundKinoko", "avatar": None, "details": "Add contributor details here."},
    {"role": "OVERLAYS", "name": "@feyakun", "avatar": None, "details": "Add contributor details here."},
    {"role": "ALERTS", "name": "@MaroWeber", "avatar": None, "details": "Add contributor details here."},
    {"role": "BG", "name": "@minhanmaghikoa", "avatar": None, "details": "Add contributor details here."},
    {"role": "ENDING", "name": "@YorshCP", "avatar": None, "details": "Add contributor details here."},
    {"role": "ENDING", "name": "@awa_ben_0521", "avatar": None, "details": "Add contributor details here."},
    {"role": "LORE", "name": "@hitorinee_", "avatar": None, "details": "Add contributor details here."},
    {"role": "LORE", "name": "@Nyao__", "avatar": None, "details": "Add contributor details here."},
    {"role": "LORE", "name": "@nymphedahlia", "avatar": None, "details": "Add contributor details here."},
    {"role": "END", "name": "@Hectyne", "avatar": None, "details": "Add contributor details here."},
    {"role": "END", "name": "@mifflue", "avatar": None, "details": "Add contributor details here."},
    {"role": "STINGER", "name": "@alderwicked", "avatar": None, "details": "Add contributor details here."},
    {"role": "CHAT CSS", "name": "@touru9Klub", "avatar": None, "details": "Add contributor details here."},
    {"role": "MAMA", "name": "@shiino_2256", "avatar": None, "details": "Add contributor details here."},
    {"role": "PAPA", "name": "@Spiral_Hero", "avatar": None, "details": "Add contributor details here."},
    
]

init -2 python:
    CREDITS_AVATAR_SEEDS = [
        "gui/news_icon.png",
        "gui/window_icon.png",
    ]

    def _credits_avatar_pool():
        pool = [p for p in CREDITS_AVATAR_SEEDS if renpy.loadable(p)]
        if not pool:
            pool = ["gui/window_icon.png"]
        return pool


style credits_header_text is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 86
    color "#ffffff"
    outlines [(4, "#5f2d96", 0, 0)]

style credits_role_text is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 24
    color "#dff3ff"
    outlines [(2, "#203b67", 0, 0)]
    text_align 0.5

style credits_name_text is text:
    font "fonts/cinzel_decorative/CinzelDecorative-Bold.otf"
    size 24
    color "#ffd8ff"
    outlines [(2, "#55286d", 0, 0)]
    text_align 0.5


screen credits_entry_card(entry, idx, avatar_pool, ring_image):
    $ avatar = (entry.get("avatar") if entry.get("avatar") and renpy.loadable(entry.get("avatar")) else avatar_pool[idx % len(avatar_pool)])

    fixed:
        xysize (250, 180)
        clipping True

        text entry.get("role", "ROLE"):
            style "credits_role_text"
            xalign 0.5
            ypos -6
            xsize 250

        fixed:
            xysize (122, 122)
            xalign 0.5
            ypos 30
            clipping True
            add Solid("#68d3ff") xysize (122, 122)
            add Solid("#285ea9") xpos 4 ypos 4 xysize (114, 114)
            add Transform(avatar, fit="contain", xsize=84, ysize=84, xpos=19, ypos=19)
            add Solid("#9be5ff55") xysize (122, 122)
            if ring_image:
                add Transform(ring_image, fit="contain", xsize=122, ysize=122, xalign=0.5, yalign=0.5)

        text entry.get("name", "@credit"):
            style "credits_name_text"
            xalign 0.5
            ypos 152
            xsize 250


screen extra_credits_board():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))
    $ ring_image = ("gui/peaceful_vn_ui/render/png/round avatatr frame.png" if renpy.loadable("gui/peaceful_vn_ui/render/png/round avatatr frame.png") else ("gui/peaceful_vn_ui/render/png/avatar frame 2.png" if renpy.loadable("gui/peaceful_vn_ui/render/png/avatar frame 2.png") else None))
    $ avatar_pool = _credits_avatar_pool()
    $ credits_cols = 5
    $ credits_rows = [credits_entries[i:i + credits_cols] for i in range(0, len(credits_entries), credits_cols)]
    $ news_bg = "gui/news/new_background.png" if renpy.loadable("gui/news/new_background.png") else "gui/news/news_background.png"

    add im.Scale(news_bg, config.screen_width, config.screen_height)

    fixed:
        xalign 0.5
        yalign 1.19
        xsize 1820
        ysize 930

        # Tighter inner credits panel around the 5-column grid.
        add Solid("#6b3aa8") xpos 210 ypos 104 xsize 1400 ysize 664
        add Solid("#2b2440cc") xpos 216 ypos 110 xsize 1388 ysize 652

        text L("extra_credits"):
            style "credits_header_text"
            xalign 0.5
            ypos -56

        side "c r":
            xpos 216
            ypos 136
            xsize 1368
            ysize 568
            spacing 8

            viewport id "credits_vp":
                mousewheel True
                draggable True
                scrollbars None
                pagekeys True
                xsize 1338
                ysize 568

                vbox:
                    spacing 14
                    for row_i, row_items in enumerate(credits_rows):
                        hbox:
                            spacing 18
                            for col_i, entry in enumerate(row_items):
                                $ idx = row_i * credits_cols + col_i
                                fixed:
                                    xysize (250, 180)
                                    use credits_entry_card(entry, idx, avatar_pool, ring_image)
                                    button:
                                        background None
                                        hover_background Solid("#7edcff33")
                                        xpos 64
                                        ypos 30
                                        xsize 122
                                        ysize 122
                                        action Show("extra_credits_detail", entry_index=idx)
                            for _pad in range(credits_cols - len(row_items)):
                                null width 250

            vbar:
                value YScrollValue("credits_vp")
                style "ui_vscrollbar"
                keyboard_focus False
                unscrollable gui.unscrollable

    hbox:
        xalign 0.5
        yalign 0.95
        spacing 18
        use ui_png_button(L("pref_button_back"), ShowMenu("extra_menu"), zoom=0.60, text_style="ui_btn_text_small", use_alt=mm_alt)


screen extra_credits_detail(entry_index):
    modal True
    zorder 220
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))
    $ valid_index = (entry_index >= 0 and entry_index < len(credits_entries))
    $ entry = (credits_entries[entry_index] if valid_index else {"role": "CREDITS", "name": "@credit", "details": "No details found."})
    $ role_title = entry.get("role", "CREDITS").replace("\n", " ")
    $ details_text = entry.get("details", "Add contributor details here.")

    add Solid("#0008")

    key "dismiss" action Hide("extra_credits_detail")
    key "game_menu" action Hide("extra_credits_detail")
    key "rollback" action Hide("extra_credits_detail")

    frame:
        background Solid("#2b2440")
        xalign 0.5
        yalign 0.5
        xsize 980
        ysize 560
        padding (30, 24)

        vbox:
            spacing 18
            text "[role_title] - [entry.get('name', '@credit')]" style "news_title"

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                xsize 920
                ysize 390
                text details_text style "news_body" xsize 900

            hbox:
                xalign 1.0
                use ui_png_button(L("news_close"), Hide("extra_credits_detail"), zoom=0.55, text_style="ui_btn_text_small", use_alt=mm_alt)

