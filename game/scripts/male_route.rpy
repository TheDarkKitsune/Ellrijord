label male_route_start:
    $ route_char = Character("[mc_first_name]")
    $ narrator_char = Character(None)

    window show
    if renpy.loadable("gui/mainmenu_bg.png"):
        scene expression im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    else:
        scene black
    with dissolve

    narrator_char "TEST: You are now on the MALE route."
    route_char "Alright, let's test this branch."
    route_char "My name is [mc_first_name]."
    route_char "Pronoun check: [mc_pronoun_subject_cap]/[mc_pronoun_object_cap]."

    route_char "How should this route start?"
    menu:
        "Confident intro.":
            route_char "I step forward and take the lead."
        "Calm intro.":
            route_char "I take a breath and move carefully."

    route_char "Male route test complete."

    return
