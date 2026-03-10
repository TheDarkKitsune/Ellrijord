# dlc_scripts/summer_festival_dlc.rpy
# Summer Festival DLC entry label.

label dlc_summer_festival_start:
    scene black with fade

    $ persistent.last_played_dlc = "summer_festival_dlc"
    $ _dlc_route = ""
    $ _dlc_confession_variant = ""

    "Summer Festival DLC"
    "A one-night side story opens as lanterns brighten the academy streets."
    "Yukata fabric rustles in the summer wind, and the crowd buzzes with anticipation."
    "Tonight should be simple: food stalls, games, and laughter."
    "But beneath the celebration, a faint anomaly trembles at the edge of the sky."

    jump dlc_summer_festival_select


label dlc_summer_festival_select:
    scene black with dissolve

    "Who will you spend the festival night with?"
    menu:
        "Reina Takamine":
            jump dlc_summer_festival_reina
        "Mimi Usagiyama":
            jump dlc_summer_festival_mimi
        "Poko Kazunami":
            jump dlc_summer_festival_poko


label dlc_summer_festival_reina:
    $ _dlc_route = "Reina Takamine"
    scene black with dissolve

    "Reina waits near the shrine gate, posture perfectly composed despite her summer yukata."
    "\"You are late by ninety seconds,\" she says, then quietly adds, \"...I am glad you came.\""

    menu:
        "Start with the goldfish stand":
            "Reina tries to stay serious while you fail spectacularly at scooping goldfish."
            "By the third attempt, she laughs under her breath and takes the net from your hand."
        "Start with festival food":
            "You share grilled skewers while Reina critiques each stall like a tactical operation."
            "When sauce lands on your sleeve, she wipes it away before noticing how close she is."

    "As evening deepens, a soft ripple passes through the lantern light."
    "For a heartbeat, the crowd goes quiet, as if listening to something very far away."
    "\"The same sensation...\" Reina whispers. \"The Void is near, but weak.\""

    menu:
        "Fireworks confession (gentle)":
            $ _dlc_confession_variant = "gentle"
            "Under the first burst of fireworks, you tell Reina that being beside her feels like finding steady ground."
            "She exhales, eyes reflecting gold and violet. \"Then stay. I don't want to stand alone anymore.\""
        "Fireworks confession (bold)":
            $ _dlc_confession_variant = "bold"
            "As fireworks split the sky, you take Reina's hand and tell her plainly: you want her, no half-steps."
            "Her fingers tighten around yours. \"Then don't let go,\" she says, voice unsteady for once."

    jump dlc_summer_festival_epilogue


label dlc_summer_festival_mimi:
    $ _dlc_route = "Mimi Usagiyama"
    scene black with dissolve

    "Mimi appears in a pastel yukata, clutching a festival fan like a shield."
    "\"I-I practiced saying hi without stuttering,\" she says. \"I still failed, though...\""

    menu:
        "Play ring toss together":
            "Mimi misses every throw until you guide her wrist."
            "She finally lands one and beams like she just won the whole festival."
        "Visit the mask stall":
            "You help Mimi pick a fox mask. She insists you wear a matching one."
            "When you turn back, she is already smiling, calmer than before."

    "Near the forest path, lantern shadows distort for an instant."
    "A distant hum brushes your thoughts, then vanishes like a dream on waking."
    "Mimi grips your sleeve. \"That feeling again... but if you're here, I can handle it.\""

    menu:
        "Fireworks confession (gentle)":
            $ _dlc_confession_variant = "gentle"
            "As fireworks bloom overhead, you promise Mimi you will always meet her halfway, no matter how hard the fear gets."
            "Her eyes shine. \"Then I'll keep trying... because I want a future with you.\""
        "Fireworks confession (bold)":
            $ _dlc_confession_variant = "bold"
            "With the sky alight, you tell Mimi you are done pretending your feelings are subtle."
            "She blushes, then nods with surprising resolve. \"Okay... then be mine tonight.\""

    jump dlc_summer_festival_epilogue


label dlc_summer_festival_poko:
    $ _dlc_route = "Poko Kazunami"
    scene black with dissolve

    "Poko arrives late, balancing three candied apples and wearing a yukata she claims is \"tactically optimized for chaos.\""
    "\"Date rule number one,\" she declares. \"If it's not fun, we are doing it wrong.\""

    menu:
        "Challenge her at festival games":
            "Poko talks big, loses immediately, then accuses the game booth of conspiracy."
            "You both end up laughing so hard the vendor gives you a pity prize."
        "Follow her to the hidden photo spots":
            "Poko drags you through side paths to \"secret vantage points.\""
            "Half the route is nonsense, but the final view over the lantern-lit city is perfect."

    "At the edge of the avenue, the neon signs flicker in sync, then stop."
    "For one strange second, Poko's usual grin fades."
    "\"Yeah... that's Void static,\" she murmurs. \"Let's keep moving before it grows teeth.\""

    menu:
        "Fireworks confession (gentle)":
            $ _dlc_confession_variant = "gentle"
            "You tell Poko that even when everything is absurd, she makes the world feel lighter."
            "She looks away, smiling. \"Careful. Keep saying things like that and I'll believe you.\""
        "Fireworks confession (bold)":
            $ _dlc_confession_variant = "bold"
            "When fireworks burst overhead, you pull Poko close and tell her you want every future festival with her."
            "She blinks, stunned, then grins. \"Deal. But next time I pick the games.\""

    jump dlc_summer_festival_epilogue


label dlc_summer_festival_epilogue:
    scene black with dissolve

    "Route Completed: [_dlc_route]"
    "Confession Variant: [_dlc_confession_variant]"
    "The summer night closes with laughter, sparks, and a lingering hint that the Void is not done with you yet."

    menu:
        "Play another heroine route":
            jump dlc_summer_festival_select
        "Exit DLC":
            jump _main_menu
