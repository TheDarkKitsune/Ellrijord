# custom_secrets_codes.rpy
# Standalone Secrets code-entry screen and unlock handlers.

default secrets_feedback = "Enter a secret code to unlock special content."
default persistent.secret_codes_redeemed = set()
default persistent.music_room_unlocked_keys = set()
default persistent.secret_cheats_unlocked = False

init -2 python:
    import os

    SECRET_CODE_DATA = {
        "STARFALL": {
            "title": "Secret Images Unlocked",
            "desc": "Unlocks all images from the Secret gallery tab.",
            "type": "secret_gallery",
        },
        "MELODYKEY": {
            "title": "Music Vault Unlocked",
            "desc": "Unlocks all music room tracks.",
            "type": "all_music",
        },
        "VOIDMODE": {
            "title": "Cheats Unlocked",
            "desc": "Unlocks developer cheats/features flag.",
            "type": "cheats",
        },
        "FOGRESET": {
            "title": "Image Discoveries Reset",
            "desc": "Relocks all discovered gallery images.",
            "type": "reset_gallery",
            "repeatable": True,
        },
        "MUTEVAULT": {
            "title": "Music Discoveries Reset",
            "desc": "Relocks all discovered music tracks.",
            "type": "reset_music",
            "repeatable": True,
        },
    }

    def _secret_redeemed_set():
        raw = getattr(persistent, "secret_codes_redeemed", None)
        if raw is None:
            s = set()
        else:
            try:
                s = set(raw)
            except Exception:
                s = set()
        persistent.secret_codes_redeemed = s
        return s

    def _unlock_gallery_paths(paths):
        if not paths:
            return 0

        unlocked_count = 0
        unlock_fn = getattr(renpy.store, "unlock_gallery_image", None)
        if callable(unlock_fn):
            for p in paths:
                if renpy.loadable(p):
                    unlock_fn(p)
                    unlocked_count += 1
            return unlocked_count

        # Fallback path if helper is unavailable.
        raw = getattr(persistent, "gallery_unlocked_images", None)
        try:
            s = set(raw) if raw is not None else set()
        except Exception:
            s = set()
        for p in paths:
            if renpy.loadable(p):
                s.add(p.lower())
                unlocked_count += 1
        persistent.gallery_unlocked_images = s
        renpy.save_persistent()
        return unlocked_count

    def _unlock_all_music_tracks():
        unlock_music = getattr(renpy.store, "unlock_music_track", None)
        if not callable(unlock_music):
            return 0

        exts = (".mp3", ".ogg", ".opus", ".wav", ".flac", ".m4a")
        files = [f for f in renpy.list_files() if f.startswith("audio/") and os.path.splitext(f)[1].lower() in exts]
        count = 0
        for f in files:
            unlock_music(f)
            count += 1
        return count

    def _reset_all_gallery_unlocks():
        reset_gallery = getattr(renpy.store, "reset_gallery_unlocks", None)
        if callable(reset_gallery):
            reset_gallery()
            return

        persistent.gallery_unlocked_images = set()
        renpy.save_persistent()

    def _reset_all_music_unlocks():
        reset_music = getattr(renpy.store, "reset_music_track_unlocks", None)
        if callable(reset_music):
            reset_music()
            return

        persistent.music_room_unlocked_keys = set()
        renpy.save_persistent()

    def redeem_secret_code(code_text):
        code = (code_text or "").strip().upper()
        if not code:
            renpy.store.secrets_feedback = "Please enter a code."
            renpy.restart_interaction()
            return

        data = SECRET_CODE_DATA.get(code)
        if not data:
            renpy.store.secrets_feedback = "Invalid code."
            renpy.restart_interaction()
            return

        redeemed = _secret_redeemed_set()
        repeatable = bool(data.get("repeatable", False))
        if (not repeatable) and code in redeemed:
            renpy.store.secrets_feedback = data["title"] + " (already redeemed)."
            renpy.restart_interaction()
            return

        unlock_type = data.get("type")
        if unlock_type == "secret_gallery":
            paths = list(getattr(renpy.store, "gallery_secret_images", []) or [])
            n = _unlock_gallery_paths(paths)
            renpy.store.secrets_feedback = "{}: {} image(s) unlocked.".format(data["title"], n)
        elif unlock_type == "all_music":
            n = _unlock_all_music_tracks()
            renpy.store.secrets_feedback = "{}: {} track(s) unlocked.".format(data["title"], n)
        elif unlock_type == "cheats":
            persistent.secret_cheats_unlocked = True
            renpy.save_persistent()
            renpy.store.secrets_feedback = "{}: Cheats flag enabled.".format(data["title"])
        elif unlock_type == "reset_gallery":
            _reset_all_gallery_unlocks()
            renpy.store.secrets_feedback = "{}: all gallery images relocked.".format(data["title"])
        elif unlock_type == "reset_music":
            _reset_all_music_unlocks()
            renpy.store.secrets_feedback = "{}: all music tracks relocked.".format(data["title"])
        else:
            renpy.store.secrets_feedback = "Code accepted."

        if not repeatable:
            redeemed.add(code)
            persistent.secret_codes_redeemed = redeemed
            renpy.save_persistent()
        renpy.restart_interaction()


screen secret_codes():
    tag menu
    $ mm_alt = bool(getattr(persistent, "mm_alt", False))
    default secret_code_input = ""
    $ bg = "gui/news/new_background.png" if renpy.loadable("gui/news/new_background.png") else "gui/news/news_background.png"

    add im.Scale(bg, config.screen_width, config.screen_height)

    fixed:
        xalign 0.5
        yalign 0.52
        xsize 1400
        ysize 760

        add Solid("#6b3aa8") xsize 1400 ysize 760
        add Solid("#2b2440dd") xpos 6 ypos 6 xsize 1388 ysize 748

        text "Secrets Vault":
            style "news_title"
            xpos 50
            ypos 36

        text "Type a special code to unlock hidden content.":
            style "news_body"
            xpos 50
            ypos 95
            xsize 800

        frame:
            background Solid("#1f1a33dd")
            xpos 50
            ypos 170
            xsize 860
            ysize 88
            padding (18, 14)

            fixed:
                xsize 820
                ysize 52
                clipping True

                input:
                    id "secret_code_field"
                    value ScreenVariableInputValue("secret_code_input")
                    length 50
                    default True
                    style "secret_code_input_text"
                    xpos 0
                    ypos 0
                    xsize 820

        hbox:
            xpos 50
            ypos 280
            spacing 16
            use ui_png_button("Submit", [Function(redeem_secret_code, secret_code_input), SetScreenVariable("secret_code_input", "")], zoom=0.55, text_style="ui_btn_text_small", use_alt=mm_alt)
            use ui_png_button("Back", ShowMenu("extra_menu"), zoom=0.55, text_style="ui_btn_text_small", use_alt=mm_alt)

        frame:
            background Solid("#1f1a33cc")
            xpos 50
            ypos 360
            xsize 1300
            ysize 110
            padding (16, 12)
            text secrets_feedback style "news_body" xsize 1260

        frame:
            background Solid("#1f1a33b8")
            xpos 50
            ypos 500
            xsize 1300
            ysize 220
            padding (16, 12)
            vbox:
                spacing 6
                text "Known Codes" style "news_title"

                side "c r":
                    spacing 8
                    xfill True
                    yfill True

                    viewport:
                        id "secret_codes_vp"
                        draggable True
                        mousewheel True
                        scrollbars None
                        xfill True
                        yfill True

                        vbox:
                            spacing 6
                            text "STARFALL - unlock secret gallery images" style "news_body"
                            text "MELODYKEY - unlock all music tracks" style "news_body"
                            text "VOIDMODE - unlock cheats flag" style "news_body"
                            text "FOGRESET - relock all discovered gallery images" style "news_body"
                            text "MUTEVAULT - relock all discovered music tracks" style "news_body"

                    use ui_vscrollbar_for("secret_codes_vp")


style secret_code_input_text is input:
    font "fonts/trotes/Trotes.ttf"
    size 34
    color "#ffffff"
    selected_color "#ffffff"
    selected_idle_color "#ffffff"
    selected_hover_color "#ffffff"
    hover_color "#ffffff"
    outlines [ (1, "#00000055", 0, 0) ]
