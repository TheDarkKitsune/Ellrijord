# game/script.rpy

default intro_story_video = "Story.webm"

init python:
    def resolve_story_video(base_name):
        candidates = [
            base_name,
            "movies/" + base_name,
            "video/" + base_name,
            "gui/intro/" + base_name,
        ]
        exts = [".webm", ".mp4", ".ogv", ".mkv", ".avi"]

        for c in candidates:
            if renpy.loadable(c):
                return c
            for ext in exts:
                p = c + ext
                if renpy.loadable(p):
                    return p
        return None


screen intro_press_any_to_continue():
    modal True
    key "dismiss" action Return()
    key "mouseup_1" action Return()
    key "K_RETURN" action Return()
    key "K_SPACE" action Return()

    if renpy.loadable("gui/Start.png"):
        add im.Scale("gui/Start.png", config.screen_width, config.screen_height)
    else:
        add Solid("#000000")

    text "Press any button to continue":
        style "ui_btn_text"
        xalign 0.5
        yalign 0.92
        size 46

label start:
    window hide
    scene black
    with dissolve

    $ _story_video = resolve_story_video(intro_story_video)
    if _story_video:
        $ renpy.movie_cutscene(_story_video)
    else:
        scene black
        centered "Video not found: [intro_story_video]"
    call screen intro_press_any_to_continue

    return
