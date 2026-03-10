# dlc_scripts/starlit_paws_dlc.rpy
# Starlit Paws DLC (Aria + MC)

# ============================================================
# PERSISTENT / STATE
# ============================================================
default persistent.starlit_paws_unlocked = False
default persistent.starlit_paws_complete = False
default persistent.starlit_paws_secret_seen = False
default persistent.starlit_paws_all_pawprints = False
default starlit_paws_pawprints = 0

# ============================================================
# CHARACTERS
# ============================================================
define mc = Character("[mc_first_name]")
define aria = Character("Aria", color="#d8c4ff")
define poppy = Character("Poppy", color="#ffd6f1")
define gizmo = Character("Gizmo", color="#ffd89c")
define narrator = Character(None)

# ============================================================
# MUSIC
# ============================================================
define audio.little_lights = "audio/Dlc_Tracks/Starlit_Paws_Dlc/Little_Lights.wav"
define audio.small_celebration = "audio/Dlc_Tracks/Starlit_Paws_Dlc/A_Small_Celebration.wav"
define audio.sunlight_between_leaves = "audio/Dlc_Tracks/Starlit_Paws_Dlc/Sunlight_Between_Leaves.wav"
define audio.memories_in_a_box = "audio/Dlc_Tracks/Starlit_Paws_Dlc/Memories_in_a_Box.wav"
define audio.where_starlight_sleeps = "audio/Dlc_Tracks/Starlit_Paws_Dlc/Where_Starlight_Sleeps.wav"

# Fallback mappings for cues that do not yet have separate files.
define audio.two_candles = "audio/Dlc_Tracks/Starlit_Paws_Dlc/A_Small_Celebration.wav"
define audio.watching_the_sky = "audio/Dlc_Tracks/Starlit_Paws_Dlc/Where_Starlight_Sleeps.wav"
define audio.still_walking_with_you = "audio/Dlc_Tracks/Starlit_Paws_Dlc/Little_Lights.wav"

# ============================================================
# AMBIENCE / SFX
# ============================================================
define audio.wind_soft = "audio/Ambience/Wind Soft.wav"
define audio.city_ambience = "audio/Ambience/City_Ambience.mp3"
define audio.page_turn = "audio/Ambience/Page_Turn.wav"
define audio.candle_light = "audio/Ambience/Candle_Light.wav"
define audio.dream_chime = "audio/Ambience/Dream_Chime.wav"

# Optional extra ambience for the dream meadow.
# If you do not have this file yet, either add it later or comment out the play/stop lines below.
define audio.dream_meadow_ambience = "audio/Ambience/Dream_Meadow_Ambience.wav"

init -2 python:
    try:
        renpy.music.register_channel("ambient", "sfx", True, True)
    except Exception:
        pass

# ============================================================
# DLC START
# ============================================================
label dlc_starlit_paws_start:
    $ persistent.last_played_dlc = "starlit_paws_dlc"
    $ persistent.starlit_paws_unlocked = True

    stop ambient fadeout 1.0
    stop music fadeout 1.0
    scene bg rooftop_twilight with fade
    $ unlock_music_track("audio/Dlc_Tracks/Starlit_Paws_Dlc/Little_Lights.wav")
    play music little_lights volume 0.55 fadein 2.0
    play ambient wind_soft volume 0.20 fadein 2.0 loop

    narrator "The rooftop was quieter than usual."
    narrator "The city below still hummed with life, but up here, everything felt far away."
    narrator "And Aria-"
    narrator "-sat alone near the fence, holding two tiny wrapped packages in her lap."

    show aria soft at center with dissolve

    mc "There you are."
    aria "...Hey."
    mc "You disappeared after class."
    aria "I know. Sorry."
    mc "You've been doing that a lot lately."
    aria "Have I?"
    mc "Aria."

    show aria smile
    aria "Okay... maybe a little."

    mc "What's with the secret packages?"

    show aria neutral
    aria "You noticed those first?"
    mc "I notice everything."
    aria "That sounds vaguely threatening."
    mc "It was meant to sound cool."

    show aria laugh
    aria "It didn't."

    narrator "She laughed, but only for a moment. The smile faded just as quickly as it came."

    mc "Something's on your mind."
    aria "...Tomorrow's their birthday."

    stop music fadeout 1.0
    play music memories_in_a_box volume 0.55 fadein 2.0

    mc "Poppy and Gizmo."
    aria "Yeah."
    aria "I kept thinking maybe I'd be better about it this year."
    aria "Not sad, exactly. Just... steadier."
    mc "And are you?"

    show aria sad
    aria "A little."
    aria "But it still feels strange."
    aria "Every year I always knew what I'd do."
    aria "Cake. Candles. One present each, even if they pretended they only cared about stealing each other's."
    aria "Gizmo would act like he was too cool for it, then pout if his ribbon looked smaller."
    aria "Poppy would hug everyone before she opened anything."

    mc "That sounds exactly like them."

    show aria soft
    aria "It is."
    aria "I can still picture it all so clearly."
    aria "The frosting on their faces. The noise. The way they'd run circles around the apartment like tiny storms."

    pause 0.5

    aria "After Ellrijord fell..."
    aria "I didn't think life would ever feel warm again."
    aria "We were so young. We barely understood what we'd lost, only that it hurt."
    aria "Then they were born."
    aria "And suddenly this broken little life in Midgard felt... full."

    mc "They did that."

    show aria tear
    aria "They were everything to me."
    aria "I know that probably sounds dramatic, but-"
    mc "It doesn't."
    mc "Not when it's true."

    narrator "Aria lowered her eyes to the packages in her hands."

    aria "I used to think I was protecting them."
    aria "But honestly..."
    aria "They were protecting me too."

    menu:
        "How should MC respond?"
        "Sit beside her quietly.":
            $ rooftop_choice = "quiet"
            mc "...Come here."
            narrator "I sat beside her, close enough that our shoulders touched."
            aria "Thank you."
        "Gently tease her to lighten the mood.":
            $ rooftop_choice = "tease"
            mc "You mean those two menace-gremlins saved you through sheer chaos?"
            show aria laugh
            aria "Menace-gremlins is generous, honestly."
            aria "They weaponized cuteness."
        "Take her hand.":
            $ rooftop_choice = "hand"
            narrator "I reached for her hand, and after only a second, she let me take it."
            mc "You don't have to carry this by yourself."
            aria "...I know."

    show aria soft
    mc "What are the packages?"
    aria "Birthday ribbons."
    aria "I know it's silly."
    mc "It's not silly."
    aria "I was going to leave them with the cake tomorrow."
    aria "Just... something small. Something that says I remembered."

    mc "Then let me help."
    aria "Help?"
    mc "Tomorrow. We do it properly."
    mc "Cake, candles, ribbons, whatever you want."
    mc "A whole day."

    show aria surprised
    aria "You really don't mind?"
    mc "Aria."
    mc "It's them. Of course I don't mind."

    show aria smile
    aria "...Okay."
    aria "But you have to promise not to laugh at me if I get sentimental."
    mc "No promises."
    show aria laugh
    aria "Terrible answer."

    narrator "For the first time that evening, her smile stayed."
    narrator "The wind carried the last gold of sunset across the rooftop, soft and fleeting."
    narrator "Tomorrow would hurt a little."
    narrator "But it would also matter."

    jump dlc_starlit_paws_bakery

# ============================================================
# BIRTHDAY ERRAND DAY
# ============================================================
label dlc_starlit_paws_bakery:
    scene bg city_street_day with fade
    stop music fadeout 1.0
    stop ambient fadeout 1.0
    $ unlock_music_track("audio/Dlc_Tracks/Starlit_Paws_Dlc/A_Small_Celebration.wav")
    play music small_celebration volume 0.55 fadein 2.0
    play ambient city_ambience volume 0.25 fadein 2.0 loop

    narrator "The next day arrived clear and bright."
    narrator "Aria met me outside the bakery with her hands tucked into her sleeves and a look that was trying very hard to be composed."

    show aria smile at center with dissolve

    mc "You're early."
    aria "You're later than me by three minutes, so technically I win."
    mc "Was this a competition?"
    aria "Everything is a competition if Gizmo taught me anything."
    mc "Fair."

    scene bg bakery_day with dissolve
    narrator "The bell above the door chimed as we stepped inside. Sweet warmth wrapped around us instantly."

    aria "We always got the same kind."
    mc "Half strawberry, half chocolate."
    aria "You remembered."
    mc "Poppy liked strawberry. Gizmo liked chocolate."
    mc "And then they'd mix them together and act like that was the plan all along."

    show aria laugh
    aria "Exactly."

    narrator "She ordered the cake softly, carefully, as if saying it out loud made the tradition real again."

    aria "Do you remember the year Gizmo tried to blow out both candles before we even finished singing?"
    mc "He inhaled frosting and still claimed victory."
    aria "He absolutely did."
    mc "And Poppy cried because she thought that meant the birthday was ruined."
    aria "Until you put whipped cream on your nose and distracted her."
    mc "A heroic act."
    aria "A ridiculous one."

    show aria soft
    aria "They loved you, you know."
    mc "I loved them too."

    narrator "Aria went quiet then, fingertips resting against the cake box once it was set in front of us."

    aria "Sometimes I'm afraid I'll remember the pain of missing them more clearly than I remember the sound of them laughing."

    menu:
        "Response"
        "Then we spend today remembering the laughter.":
            $ bakery_choice = "laughter"
            mc "Then that's what today is for."
            mc "Not just missing them. Remembering them properly."
        "Tell me another story about them.":
            $ bakery_choice = "story"
            mc "Then tell me another story."
            mc "The more you tell me, the less room the silence gets."
        "You don't lose them by loving them.":
            $ bakery_choice = "love"
            mc "Love doesn't erase the hurt."
            mc "But it doesn't erase them either."

    show aria smile
    aria "...You always know what to say."
    mc "That is deeply untrue, but I appreciate the confidence."

    narrator "She laughed under her breath and took the cake carefully into her arms like it was something precious."

    jump dlc_starlit_paws_toyshop

label dlc_starlit_paws_toyshop:
    scene bg city_street_day with dissolve
    narrator "Our second stop was a small toy shop tucked between a florist and a stationery store."
    narrator "Aria slowed before the window."

    show aria soft at center with dissolve
    mc "You found something."
    aria "Maybe."

    scene bg toyshop_day with dissolve
    narrator "Inside, hanging near the register, were two tiny plush cat keychains."
    narrator "One pale and sleepy-looking. One bright-eyed and mischievous."

    aria "...That's almost unfair."
    mc "They do look familiar."
    aria "Poppy and Gizmo, if they'd been turned into souvenirs."

    narrator "She picked them up with absurd care, brushing a thumb over each tiny stitched face."

    aria "One for Poppy. One for Gizmo."
    aria "And... one for you."

    mc "Me?"
    aria "You're part of this too."
    aria "So you have to carry one."

    menu:
        "Which keychain does MC take?"
        "Take Poppy's keychain.":
            $ keychain_choice = "poppy"
            mc "Then I'm on Team Poppy."
            aria "Soft choice. Very you."
        "Take Gizmo's keychain.":
            $ keychain_choice = "gizmo"
            mc "I'll take Gizmo. Someone has to manage his chaos."
            aria "Bold of you to assume that's possible."
        "Let Aria choose for you.":
            $ keychain_choice = "aria_pick"
            mc "You choose."
            aria "...Then this one."
            narrator "She placed the keychain in my hand with a small smile."

    mc "I'll guard it with my life."
    aria "Gizmo would definitely try to steal yours on principle."
    mc "And Poppy?"
    aria "She'd probably curl up beside it like it was part of the family already."

    show aria laugh
    aria "They really were impossible."
    mc "You say that like you didn't adore them."
    aria "I adored them because they were impossible."

    narrator "At the counter, Aria hesitated before adding a pair of tiny blue ribbons to the purchase."

    mc "More ribbons?"
    aria "For the candles."
    aria "Poppy liked anything pretty. Gizmo liked pretending he didn't care, then stealing hers if his looked boring."
    mc "Naturally."

    jump dlc_starlit_paws_park

label dlc_starlit_paws_park:
    scene bg park_afternoon with fade
    stop music fadeout 1.0
    $ unlock_music_track("audio/Dlc_Tracks/Starlit_Paws_Dlc/Sunlight_Between_Leaves.wav")
    play music sunlight_between_leaves volume 0.55 fadein 2.0
    # Keeping city ambience off here lets the scene breathe more naturally.

    narrator "By the time we reached the park, the afternoon had softened into gold."
    narrator "Children's voices drifted across the paths. Leaves shimmered in the breeze."

    show aria soft at center with dissolve

    aria "They used to race to that tree first."
    mc "The one Gizmo wasn't supposed to climb?"
    aria "The very same."
    mc "And yet he always climbed it."
    aria "With the confidence of someone who had never once considered consequences."

    narrator "Aria smiled toward the tree, then turned to a sunlit patch of grass."

    aria "Poppy loved spots like this."
    aria "She'd find the warmest patch of sunlight in any room and settle there like she'd been personally invited by the universe."

    narrator "She stepped into the light and sat down, hugging her knees loosely."

    mc "Reenacting the scene?"
    aria "Maybe."
    aria "You can sit too, you know."

    narrator "I sat beside her. For a while, neither of us said anything."
    narrator "The silence wasn't empty. It was full of things we both remembered."

    aria "They were the first people who made Midgard feel like home."
    aria "Not because they understood what we'd lost. They didn't. They were born here."
    aria "But because they made me want to stay."
    aria "To build something. To protect something."

    mc "You did."
    aria "We did."

    show aria sad
    aria "I used to watch them sleeping and think..."
    aria "If the world ever tries to take this from me too, I'll fight it with everything I have."
    aria "That sounds dramatic, doesn't it?"
    mc "No. It sounds like love."

    narrator "She lowered her head slightly, hiding a smile."

    aria "Gizmo always acted brave when he scraped his knees."
    aria "He'd wobble around, lip trembling, then say he was fine because Poppy was watching."
    aria "And Poppy would cry harder than he did."
    mc "She was the gentlest of the two."
    aria "Mm."
    aria "She was the kind of gentle that made people soften around her without meaning to."
    aria "Even Gizmo. Especially Gizmo."

    narrator "A beat passed."

    aria "Sometimes I still expect to hear them running down the hallway at home."
    aria "Or arguing over who gets the bigger slice of cake."
    aria "Or climbing into bed when they were supposed to be asleep."
    aria "Is that strange?"

    menu:
        "Response"
        "No. I still expect it too.":
            $ park_choice = "too"
            mc "No."
            mc "Honestly... sometimes I still expect it too."
        "It means they're still part of your life.":
            $ park_choice = "part"
            mc "It just means they still belong in your world."
        "I think that kind of love leaves echoes.":
            $ park_choice = "echoes"
            mc "I think some love is loud enough to echo for a long time."

    show aria tear
    aria "...I like that."
    aria "Echoes."

    narrator "She leaned her head lightly against my shoulder."
    narrator "The sunlight shifted around us, warm and fleeting, like a memory choosing to stay a little longer."

    jump dlc_starlit_paws_snackstall

label dlc_starlit_paws_snackstall:
    scene bg city_street_day with dissolve
    stop music fadeout 1.0
    play music small_celebration volume 0.55 fadein 2.0
    play ambient city_ambience volume 0.25 fadein 1.5 loop

    narrator "We stopped for snacks on the way back."
    narrator "Aria ordered something sweet, then immediately guarded it with both hands."

    show aria smile at center with dissolve

    mc "Defensive posture. Interesting."
    aria "Years of conditioning."
    mc "Against Gizmo?"
    aria "Against Gizmo specifically."
    aria "He could appear from nowhere if he smelled sugar."

    narrator "I looked left, then right, then dramatically positioned myself between her and the street."

    mc "Don't worry. I'll protect the snack."
    show aria laugh
    aria "You look ridiculous."
    mc "I look vigilant."
    aria "You look like you're preparing to duel a child."
    mc "A child with no moral boundaries."

    narrator "Aria laughed-really laughed this time, the kind that bent her shoulders and brightened her whole face."
    narrator "The sound caught me off guard with how badly I'd missed hearing it."

    aria "He would've loved that."
    mc "I know."

    pause 0.5

    show aria soft
    aria "Thank you."
    mc "For what?"
    aria "For not trying to make today less important than it is."
    aria "For not acting like I should be over it just because time passed."
    mc "That was never going to happen."
    aria "I know."
    aria "That's why I asked you to come."

    narrator "She said it so simply that it took a second to settle in my chest."
    narrator "Not as a grand confession. Just as something true."

    jump dlc_starlit_paws_photo_box

# ============================================================
# PHOTO BOX
# ============================================================
label dlc_starlit_paws_photo_box:
    scene bg aria_apartment_evening with fade
    stop ambient fadeout 1.0
    stop music fadeout 1.0
    $ unlock_music_track("audio/Dlc_Tracks/Starlit_Paws_Dlc/Memories_in_a_Box.wav")
    play music memories_in_a_box volume 0.55 fadein 2.0

    narrator "Evening painted the apartment in amber by the time we returned."
    narrator "Aria set the cake carefully on the table, then disappeared into her room for a moment."
    narrator "When she came back, she was carrying a small wooden box."

    show aria soft at center with dissolve

    mc "That looks important."
    aria "It is."
    aria "I haven't opened it in a while."

    narrator "She sat down beside me and placed the box between us."
    narrator "Inside were photos, folded drawings, ribbons, and tiny keepsakes saved with impossible care."

    play sound page_turn volume 0.80

    aria "This one was their fourth birthday."
    narrator "In the photo, Poppy was smiling so hard her eyes were almost closed. Gizmo was mid-motion, clearly trying to swipe frosting before anyone noticed."

    mc "Evidence of criminal intent."
    aria "And yet no jury would convict him."

    narrator "She lifted another photo."
    play sound page_turn volume 0.80
    pause 0.25

    aria "This was the park. The tree incident."
    mc "He climbed it, fell halfway down, then insisted the branch had attacked him."
    aria "He was deeply offended."

    narrator "Aria laughed softly, then unfolded a child's drawing done in bright, uneven crayon."
    play sound page_turn volume 0.80

    aria "He made this."
    mc "That's definitely supposed to be us."
    aria "It is."
    mc "Why am I taller than everybody else by an entire building?"
    aria "Artistic interpretation."
    mc "And why does Gizmo have what appears to be a sword?"
    aria "That might be a balloon."
    mc "It is absolutely not a balloon."

    show aria laugh
    aria "He said he drew all of us under the stars so we'd never get lost."

    narrator "The smile on her face faded into something quieter."

    show aria sad
    aria "They looked up to us so much."
    aria "Sometimes that scared me."
    mc "Scared you?"
    aria "I was still figuring out how to be okay myself."
    aria "We both were."
    aria "And they thought I could do anything."
    aria "Protect them from anything."

    mc "You gave them love. Safety. Home."
    mc "That matters more than being perfect."

    aria "I know."
    aria "But sometimes I still wonder if I did enough."

    menu:
        "Response"
        "They never doubted you.":
            $ box_choice = "doubted"
            mc "They adored you, Aria."
            mc "They never doubted for a second that you were their safe place."
        "You were their whole world too.":
            $ box_choice = "whole_world"
            mc "You say they were everything to you."
            mc "You were everything to them too."
        "Love isn't measured by how long you get.":
            $ box_choice = "measured"
            mc "You don't measure love by how long you get someone."
            mc "You measure it by how fully you gave it."

    show aria tear
    aria "...You always make it sound easier to breathe."

    narrator "She reached deeper into the box and took out two tiny bracelets made of thread and plastic beads."

    aria "They made these for me."
    aria "Well... 'made' is generous. Poppy actually made hers. Gizmo mostly tangled string and declared it art."
    mc "Iconic, honestly."
    aria "I still kept both."

    narrator "Aria held them against her palm as if weighing memory itself."

    aria "Do you know what I'm most afraid of?"
    mc "What?"
    aria "Forgetting something small."
    aria "Not the big things. Not birthdays or laughter or the way Gizmo ran too fast around corners."
    aria "I'm afraid of forgetting the tiny things."
    aria "How Poppy's voice sounded when she got sleepy."
    aria "The exact shape of Gizmo's grin right before he did something awful."
    aria "The way they'd lean on me when they were tired."

    mc "Then let's write them down."

    show aria surprised
    aria "Write them down?"
    mc "Tonight. After the candles."
    mc "Every little thing you can remember."
    mc "Not because you have to prove you loved them."
    mc "Just so the memories have somewhere to rest."

    show aria soft
    aria "...That's a really good idea."
    aria "I hate how often that happens."
    mc "Natural talent."

    narrator "She bumped her shoulder against mine lightly."

    jump dlc_starlit_paws_rooftop_night

# ============================================================
# ROOFTOP NIGHT
# ============================================================
label dlc_starlit_paws_rooftop_night:
    scene bg rooftop_night with fade
    stop ambient fadeout 1.0
    stop music fadeout 1.0
    play music two_candles volume 0.50 fadein 2.0
    play ambient wind_soft volume 0.20 fadein 2.0 loop

    narrator "Night settled over the city by the time we returned to the rooftop."
    narrator "Aria carried the cake. I carried the little bag with the ribbons, matches, and keychains."
    narrator "Above us, the sky was deep and endless."

    show aria soft at center with dissolve

    narrator "She set the cake between us and carefully fixed two candles into the frosting."
    narrator "One tied with a pale ribbon. The other with a bright one."

    play sound candle_light
    pause 0.4

    aria "There."
    mc "Looks official."
    aria "It does, doesn't it?"

    narrator "The tiny flames flickered in the wind, stubborn and warm."

    aria "Every year they'd try to blow out each other's candle first."
    mc "Competitive even in birthday etiquette."
    aria "Especially in birthday etiquette."

    mc "Do we reenact it?"
    aria "Obviously."

    narrator "We leaned in at the same time, each aiming for the other candle just to hear her laugh when we failed."

    show aria laugh
    aria "You cheated!"
    mc "You started first."
    aria "I absolutely did not."
    mc "There are no witnesses."
    aria "There are two very judgmental ghosts of birthday chaos witnessing everything."

    narrator "We tried again, this time properly. Together."
    narrator "The candles went out in a single breath."

    pause 1.0

    show aria tear
    aria "Happy birthday, Poppy."
    aria "Happy birthday, Gizmo."

    narrator "Her voice didn't break. Somehow that made it hurt more."

    aria "I hope wherever you are feels warm."
    aria "I hope there's sunlight for Poppy and too many things to climb for Gizmo."
    aria "I hope you know I never stopped loving you."

    pause 0.5

    aria "When Ellrijord disappeared... I thought we lost our home."
    aria "But you two gave me another one."
    aria "You weren't warriors. You weren't chosen by prophecy."
    aria "You were just my little siblings."
    aria "And you meant everything to me."

    narrator "She closed her eyes for a moment, fingers tightening around the keychain in her hand."

    aria "If I ever forget your voices..."

    stop music fadeout 1.0
    play music little_lights volume 0.55 fadein 2.0

    menu:
        "What does MC say?"
        "Then I'll help you remember.":
            $ night_choice = "remember"
            mc "Then I'll help you remember."
            mc "Every story. Every habit. Every ridiculous little thing."
        "You remember them because you loved them.":
            $ night_choice = "loved"
            mc "You remember them because you loved them."
            mc "That kind of love doesn't disappear."
        "They're part of who you are.":
            $ night_choice = "part_of_you"
            mc "They're woven into you, Aria."
            mc "You'd have to forget yourself first."

    narrator "Aria looked at me for a long time, eyes bright with reflected city lights."

    aria "They were my light after the void."
    aria "And now..."
    aria "So are you."

    narrator "The words landed quietly, without ceremony, and hit harder because of it."

    menu:
        "MC reacts"
        "Pull her into an embrace.":
            $ confession_choice = "embrace"
            narrator "I pulled her gently into my arms. She exhaled against my shoulder like she'd been holding that breath for years."
            mc "I'm here."
        "Rest your forehead against hers.":
            $ confession_choice = "forehead"
            narrator "I leaned close until our foreheads touched, the city and stars blurring at the edges."
            mc "Then I'm not going anywhere."
        "Hold her hand and stay with her in the silence.":
            $ confession_choice = "silence"
            narrator "I took her hand and held it between both of mine, saying nothing for a moment because nothing felt big enough."
            mc "I know."

    show aria soft
    aria "Stay a little longer?"
    mc "As long as you want."

    narrator "So we sat beneath the night sky with the empty candles, the half-eaten cake, and the kind of silence that only exists between people who trust each other completely."
    narrator "Eventually, when the air turned colder, we went home."

    jump dlc_starlit_paws_memory_journal

# ============================================================
# MEMORY JOURNAL
# ============================================================
label dlc_starlit_paws_memory_journal:
    scene bg aria_apartment_evening with dissolve
    stop ambient fadeout 1.0
    stop music fadeout 1.0
    play music memories_in_a_box volume 0.55 fadein 2.0

    narrator "Before sleeping, Aria opened a notebook and wrote for a long time."
    narrator "I stayed with her while she filled page after page with little memories."

    show aria soft at center with dissolve

    aria "Poppy hummed when she was sleepy."
    aria "Not a song. Just... little sounds."
    mc "Write it down."
    aria "Gizmo always stole the first bite, no matter whose plate it was."
    mc "Especially write that down."
    aria "Poppy squeezed my hand three times when she wanted attention."
    mc "That's devastatingly adorable."
    aria "Gizmo grinned right before every terrible decision."
    mc "Somehow I can picture it perfectly."

    narrator "The pages filled. The room grew softer."

    aria "Thank you for staying."
    mc "You don't have to thank me for this."
    aria "I know."
    aria "I still want to."

    narrator "At some point, the pen slipped from her fingers."
    narrator "She fell asleep with her head on my shoulder, the notebook open in her lap, memory and exhaustion finally giving way to rest."

    stop ambient fadeout 1.0
    stop music fadeout 2.0
    scene black with dissolve
    pause 1.0

    narrator "That night, Aria dreamed."

    jump dlc_starlit_paws_dream

# ============================================================
# DREAM MEADOW
# ============================================================
label dlc_starlit_paws_dream:
    # Small silence before the transition makes the dream feel more cinematic.
    scene black
    pause 1.0
    play sound dream_chime volume 0.60
    scene bg dream_meadow with fade
    $ unlock_music_track("audio/Dlc_Tracks/Starlit_Paws_Dlc/Where_Starlight_Sleeps.wav")
    play ambient dream_meadow_ambience volume 0.20 fadein 2.0 loop
    pause 0.3
    play music where_starlight_sleeps volume 0.55 fadein 3.0

    narrator "A meadow stretched beneath a twilight sky vast enough to hold two worlds at once."
    narrator "The grass glowed softly at the edges. Starlight clung to every blade."
    narrator "Somewhere nearby, laughter rang out."

    show aria surprised at center with dissolve
    aria "...Hello?"

    narrator "She turned toward the sound."

    show poppy child at left with dissolve
    show gizmo child at right with dissolve

    poppy "Aria!"
    gizmo "You're late!"

    # A brief dip here lets the reunion land harder.
    stop music fadeout 0.5
    pause 0.8
    play music where_starlight_sleeps volume 0.55 fadein 1.5

    narrator "They collided with her all at once."
    narrator "Poppy clung to her middle, nearly in tears from happiness. Gizmo wrapped both arms around her and pretended he wasn't emotional at all."

    show aria tear
    aria "Poppy... Gizmo..."
    poppy "You remembered!"
    gizmo "Obviously she remembered. It's our birthday."
    poppy "I know, but still!"

    aria "I-"
    aria "I missed you so much."

    poppy "We know."
    gizmo "A lot. Like, a dramatic amount."
    aria "You're one to talk."
    gizmo "I'm very cool and composed."
    poppy "He cried the last time we saw a pretty cloud."
    gizmo "That cloud looked important."

    narrator "Aria laughed through tears, and the sound seemed to make the whole meadow brighter."

    aria "You're exactly the same."
    gizmo "Of course we are."
    poppy "Come on!"

    narrator "They grabbed her hands and pulled her forward through the glowing grass."
    narrator "The meadow unfolded like a memory made kinder than reality."

    narrator "They ran together beneath the stars."
    narrator "Gizmo darted ahead, climbing a low stone just because it was there. Poppy stopped every few steps to pick glowing flowers and tuck them behind Aria's ear."

    aria "This place..."
    poppy "Pretty, right?"
    gizmo "I picked the climbing rocks."
    poppy "I picked the flowers."
    gizmo "We both picked the sky."

    aria "It's beautiful."

    narrator "A little farther ahead, someone else stood waiting."

    mc "Took you long enough."
    gizmo "Hey! You made it too."
    poppy "Good."
    poppy "You still taking care of our sister?"

    mc "I'm trying."
    gizmo "Try harder."
    mc "Rude."
    poppy "He means thank you. Probably."
    gizmo "I absolutely did not say that."

    show aria laugh
    aria "You two are impossible."
    gizmo "And yet beloved."
    aria "Annoyingly so."

    narrator "They spent what felt like hours in that meadow, though dream-time had no real shape."
    narrator "Poppy braided little flowers into Aria's hair. Gizmo challenged the MC to a race he immediately cheated in."
    narrator "For a little while, the ache of missing them disappeared into simple joy."

    narrator "Eventually, they all settled in the grass beneath the open sky."

    poppy "Look."

    narrator "High above, new stars gathered themselves into shape."
    narrator "Two tiny constellations."
    narrator "Paw prints."

    aria "...Oh."
    gizmo "Told you the sky was good."
    poppy "So if you ever look up and miss us too much..."
    poppy "We're still there."

    aria "I don't want to forget you."

    poppy "You won't."
    gizmo "And even if you forget something small, that's okay."
    gizmo "You loved us. That part matters more."

    aria "I still hear you sometimes."
    aria "In little things."
    poppy "Good."
    gizmo "That means we're doing our job."

    mc "Your job?"
    gizmo "Watching the brat."
    aria "I called you that."
    gizmo "We learned from the best."

    narrator "Poppy scooted closer and rested her head against Aria's shoulder."

    poppy "Don't be sad all the time, okay?"
    poppy "It's okay to smile when you think of us."
    poppy "That doesn't mean you loved us less."

    aria "...Okay."

    narrator "The wind changed. The meadow shimmered. Somewhere far off, dawn began touching the horizon."

    show aria tear
    aria "Do you have to go?"

    gizmo "Not really."
    gizmo "But you have to wake up."
    poppy "We'll still be here. Just differently."

    aria "I love you."
    poppy "We know."
    gizmo "Love you too. Obviously."

    narrator "They stood and took a few steps back, still smiling."

    poppy "Happy birthday to us."
    gizmo "Try not to cry too much after this."
    aria "No promises."

    narrator "They laughed and turned toward the horizon, where the twilight melted into silver light."
    narrator "Not disappearing. Not lost."
    narrator "Just becoming part of something larger and gentle and endless."

    scene bg dream_meadow with dissolve
    narrator "For one last moment, the paw-print constellations shone overhead."

    stop ambient fadeout 2.0
    stop music fadeout 3.0
    scene black with dissolve
    pause 2.0

    jump dlc_starlit_paws_morning

# ============================================================
# MORNING ENDING
# ============================================================
label dlc_starlit_paws_morning:
    scene bg morning_city with fade
    play music still_walking_with_you volume 0.55 fadein 2.0

    narrator "Aria woke in the pale gold of morning."
    narrator "The notebook was still open beside her. The wooden box still sat on the table."
    narrator "For the first time in days, her chest felt light."

    show aria soft at center with dissolve

    mc "Morning."
    aria "Morning."
    mc "You look like you actually slept."
    aria "I did."
    aria "I had a dream."
    mc "A good one?"

    show aria smile
    aria "Yeah."
    aria "A really good one."

    narrator "She picked up the two plush keychains and clipped them carefully to her bag."

    aria "There."
    mc "Permanent addition?"
    aria "Definitely."
    aria "They're still coming with me."
    aria "Just... in a different way."

    mc "I think they'd like that."
    aria "I think so too."

    narrator "She looked up toward the morning sky, eyes soft with something gentler than grief."

    aria "I thought remembering them would always hurt the same way."
    aria "But maybe..."
    aria "Maybe it can be warm too."

    mc "It can."

    narrator "Aria slipped her hand into mine."

    aria "Thank you."
    aria "For yesterday. For all of it."
    mc "Always."

    show aria soft
    aria "Whenever things feel heavy again..."
    aria "I'm going to remember that meadow."
    aria "The flowers. The stupid climbing rocks. The sky."
    mc "The brat cats."
    show aria laugh
    aria "The brat cats."

    narrator "She leaned lightly against my shoulder as the city slowly woke around us."
    narrator "Above the rooftops, the sky stretched clear and wide."
    narrator "And somewhere, beyond sight but not beyond reach, small lights endured."

    $ persistent.starlit_paws_complete = True
    stop music fadeout 2.0

    narrator "Ending Reached: Starlit Paws"
    narrator "Achievement Unlocked: The Brat Cats"

    if persistent.starlit_paws_all_pawprints:
        jump dlc_starlit_paws_secret_epilogue
    else:
        return

# ============================================================
# SECRET EPILOGUE
# ============================================================
label dlc_starlit_paws_secret_epilogue:
    scene bg secret_meadow with fade
    play music watching_the_sky volume 0.55 fadein 2.0
    play ambient dream_meadow_ambience volume 0.18 fadein 2.0 loop

    narrator "Night returned in a place beyond ordinary distance."
    narrator "The meadow lay quiet beneath a blanket of stars."

    show poppy child at left with dissolve
    show gizmo child at right with dissolve

    gizmo "She cried again."
    poppy "Only a little."
    gizmo "Still counts."
    poppy "She always worries too much."
    gizmo "That's because she loves us."

    narrator "They looked up. In the stars above, a faint shimmer showed Aria and the MC walking together through the city below."

    gizmo "Looks like she's doing okay."
    poppy "She always will."

    poppy "We'll stay right here."
    gizmo "Yeah. Watching the brat."
    poppy "She called us that."
    gizmo "We improved it."

    narrator "They lay back in the glowing grass, hands behind their heads, the paw-print constellations bright overhead."

    gizmo "Think she knows?"
    poppy "I think she does."

    poppy "Happy birthday to us."
    gizmo "Best one yet."

    narrator "The camera rose slowly toward the sky."
    narrator "The two constellations shone brighter for one last moment before settling into the stars above Midgard forever."

    $ persistent.starlit_paws_secret_seen = True
    narrator "Achievement Unlocked: Starlit Guardians"
    stop ambient fadeout 2.0
    stop music fadeout 3.0
    return
