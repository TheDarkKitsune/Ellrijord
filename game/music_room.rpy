################################################################################
## MUSIC ROOM DECLARATION
################################################################################
init python:
    import os

    if not hasattr(persistent, "music_room_unlocked_keys") or persistent.music_room_unlocked_keys is None:
        persistent.music_room_unlocked_keys = set()

    def _get_music_unlocked_set():
        """
        Return a safe set for unlocked music keys, normalizing old/bad data.
        """
        raw = getattr(persistent, "music_room_unlocked_keys", None)
        if raw is None:
            unlocked = set()
        else:
            try:
                unlocked = set(raw)
            except Exception:
                unlocked = set()
        if raw is None or raw is not unlocked:
            persistent.music_room_unlocked_keys = unlocked
        return unlocked

    def music_track_key(path_or_name):
        """
        Normalize a track path or name into a stable unlock key.
        """
        base = os.path.splitext(os.path.basename(path_or_name))[0]
        return base.lower()

    # Per-track unlock hints shown while a track is still locked.
    MUSIC_TRACK_HINTS = {
        "academy_window": "Hint: Main Menu (Light mode).",
        "rooftop_universe": "Hint: Main Menu (Dark mode).",
        "unspoken_language": "Hint: Main Menu (Twilight mode).",
    }

    def music_track_hint(path_or_name):
        key = music_track_key(path_or_name)
        return MUSIC_TRACK_HINTS.get(key, "Hint: Discover this track during story/events.")

    def music_track_artist(path_or_name, fallback_artist=None):
        key = music_track_key(path_or_name)
        normalized = str(path_or_name).replace("\\", "/").lower()
        if normalized.startswith("audio/dlc_tracks/"):
            return "Ellrijord OST"
        if key in (
            "magical_hallways",
            "shattered_remains",
            "academy_window",
            "rooftop_universe",
            "unspoken_language",
        ):
            return "Ellrijord OST"
        if fallback_artist == "Aelx Coldfire Music":
            return "Alex Coldfire Music"
        return fallback_artist or "Unknown Artist"

    def music_track_category(song_or_path):
        try:
            path = song_or_path.path
        except Exception:
            path = str(song_or_path)

        normalized = path.replace("\\", "/").lower()
        key = music_track_key(path)

        if key in (
            "magical_hallways",
            "shattered_remains",
            "academy_window",
            "rooftop_universe",
            "unspoken_language",
        ):
            return "menu"

        if normalized.startswith("audio/dlc_tracks/"):
            return "dlc"

        return "story"

    def music_track_category_label(category):
        if category == "menu":
            return "Menu"
        if category == "dlc":
            return "DLC"
        return "Story"

    def music_room_filtered_tracklist(mr, category):
        tracks = mr.get_tracklist(all_tracks=True)
        return [song for song in tracks if music_track_category(song) == category]

    def music_track_unlocked(key):
        """
        Returns True if a music track key is unlocked in persistent data.
        """
        unlocked = _get_music_unlocked_set()
        return key in unlocked

    def unlock_music_track(path_or_name):
        """
        Unlock a music track by filename or path.
        Example: unlock_music_track("audio/Magical_Hallways.mp3")
                 unlock_music_track("Magical_Hallways")
        """
        key = music_track_key(path_or_name)
        unlocked = _get_music_unlocked_set()
        if key not in unlocked:
            unlocked.add(key)
            persistent.music_room_unlocked_keys = unlocked
            renpy.save_persistent()

    def reset_music_track_unlocks():
        """
        Relock all music tracks.
        """
        persistent.music_room_unlocked_keys = set()
        renpy.save_persistent()
    #################### STEP 1: Set up the music room.
    ## You can make multiple music rooms consisting of different sets of tracks,
    ## if you so desire, or use one music room for all your music. You only need
    ## to pass in the name of the ExtendedMusicRoom object you set up here to
    ## the music room screens below.

    ## You can pass any of the following arguments to ExtendedMusicRoom:
    ## channel: The channel to play the music on. Defaults to 'music'.
    ## fadeout: The time in seconds to fade out the old song when changing
    ##          tracks. Defaults to 0.0 (no fade).
    ## fadein: The time in seconds to fade in the new song when changing tracks.
    ##         Defaults to 0.0 (no fade).
    ## loop: Whether to loop the music when reaching the end of the track list.
    ##       Defaults to True and can be toggled in the music room with a
    ##       button.
    ## single_track: If True, only a single track will loop. Defaults to False
    ##               and can be toggled in the music room with a button.
    ## shuffle: Whether to shuffle the tracks or play them in default order.
    ##          Defaults to False and can be toggled in the music room with a
    ##          button.
    ## stop_action: A screen action to run when the music stops. Defaults to
    ##              None, so no action is run.
    ## alphabetical : If True, the tracks will be sorted alphabetically.
    ##                If False, the default, they will be arranged in the order
    ##                they are added to the music room in.
    music_room = ExtendedMusicRoom(channel='music', fadeout=0.0, fadein=0.0,
        loop=True, single_track=False, shuffle=False, stop_action=None,
        alphabetical=True)

    ## This sets up a default art image for all tracks in this room which aren't
    ## given a more specific one. This default art is 600x600, but several
    ## layouts resize it. It should typically be square.
    music_room.default_art = "gui/music_room/cover_art.webp"

    ## Auto-register all music files in game/audio.
    ## This makes new tracks appear in the music gallery without extra edits.
    track_exts = (".mp3", ".ogg", ".opus", ".wav", ".flac", ".m4a")
    all_audio_files = [
        f for f in renpy.list_files()
        if f.startswith("audio/")
        and "/ambience/" not in f.lower()
        and os.path.splitext(f)[1].lower() in track_exts
    ]

    # Keep one file per track name, preferring converted assets when present.
    def _audio_rank(path):
        # Highest priority first:
        # 1) audio/converted/*  (Ren'Py-safe converted WAVs)
        # 2) mp3/ogg/opus
        # 3) wav/flac/m4a
        ext = os.path.splitext(path)[1].lower()
        in_converted = path.startswith("audio/converted/")
        if in_converted:
            return (0, path.lower())
        if ext in (".mp3", ".ogg", ".opus"):
            return (1, path.lower())
        return (2, path.lower())

    chosen_by_base = {}
    paths_by_base = {}
    for f in sorted(all_audio_files, key=_audio_rank):
        base = os.path.splitext(os.path.basename(f))[0]
        key = base.lower()
        if key not in paths_by_base:
            paths_by_base[key] = []
        paths_by_base[key].append(f)
        if key not in chosen_by_base:
            chosen_by_base[key] = f

    for base_key in sorted(chosen_by_base.keys()):
        f = chosen_by_base[base_key]
        base = os.path.splitext(os.path.basename(f))[0]
        pretty = base.replace("_", " ")
        artist_name = music_track_artist(f, "Alex Coldfire Music")

        # Locked until manually unlocked by script via unlock_music_track(...).
        unlock_condition = "music_track_unlocked({})".format(repr(base_key))

        music_room.add(
            name=_(pretty),
            path=f,
            artist=artist_name,
            art=None,
            description=_("Soundtrack track."),
            unlock_condition=unlock_condition,
        )


################################################################################
## CONFIGURATION VALUES
################################################################################
## Set this to True if you want to unlock all tracks in the music room during
## development. Set it to False to test the unlock conditions. Tracks will
## automatically obey unlock rules in a distribution regardless of the value
## of this configuration variable.
define myconfig.UNLOCK_TRACKS_FOR_DEVELOPMENT = False

################################################################################
## IMAGES & DEFINITIONS
################################################################################
## These colours are used by the colorize_button transform in the screens below
## to colorize the default music controls. You can change these if you want to
## use the provided images, or simply supply your own and remove the lines
## `at colorize_button` from the screen below.
define MUSIC_ROOM_IDLE_COLOR = "#ff8335"
define MUSIC_ROOM_HOVER_COLOR = "#f93c3e"
define MUSIC_ROOM_SELECTED_IDLE_COLOR = "#ff8335"
define MUSIC_ROOM_SELECTED_HOVER_COLOR = "#f93c3e"
define MUSIC_ROOM_INSENSITIVE_COLOR = "#888"

## Here are the default buttons used for the music controls below. You can
## update these or replace them.
image play_button = "gui/music_room/play.webp"
image pause_button = "gui/music_room/pause.webp"
image next_button = "gui/music_room/next.webp"
image prev_button = Transform("gui/music_room/next.webp", xzoom=-1.0)
image repeat_all_button = "gui/music_room/repeat all.webp"
## Note that this image is just a foreground on top of the repeat_all button!
image repeat_one_button = "gui/music_room/repeat 1.webp"
image shuffle_button = "gui/music_room/shuffle.webp"
image back_10_button = "gui/music_room/back_10.webp"
image forward_10_button = "gui/music_room/forward_10.webp"

## The "audio level" bars. These are optional to show next to the currently
## playing song. There are four bars that randomly change height.
define AUDIO_BAR_HEIGHT = 30
define AUDIO_BAR_WIDTH = 8
image audio_bar = Transform(MUSIC_ROOM_HOVER_COLOR,
    xysize=(AUDIO_BAR_WIDTH, AUDIO_BAR_HEIGHT))
transform audio_bar_move():
    yzoom renpy.random.random() ## Start at a random height
    block:
        ## Choose a random height to be
        choice:
            ease 0.2 yzoom 1.0
        choice:
            ease 0.2 yzoom 0.2
        choice:
            ease 0.2 yzoom 0.8
        choice:
            ease 0.2 yzoom 0.0
        choice:
            ease 0.2 yzoom 0.5
        repeat
## The final audio bars image, with four bars that randomly change height.
image audio_bars = HBox(
    At('audio_bar', audio_bar_move),
    At('audio_bar', audio_bar_move),
    At('audio_bar', audio_bar_move),
    At('audio_bar', audio_bar_move),
    yalign=1.0, ysize=AUDIO_BAR_HEIGHT,
)

################################################################################
## TRANSFORMS
################################################################################
## A transform that makes it easier to apply colours to the various buttons.
## The default images are black, so it uses ColorizeMatrix to colorize them.
## The colours are defined at the top of the file.
transform colorize_button(idle=MUSIC_ROOM_IDLE_COLOR,
        hover=MUSIC_ROOM_HOVER_COLOR,
        selected_idle=MUSIC_ROOM_SELECTED_IDLE_COLOR,
        selected_hover=MUSIC_ROOM_SELECTED_HOVER_COLOR,
        insensitive=MUSIC_ROOM_INSENSITIVE_COLOR):
    matrixcolor ColorizeMatrix(insensitive, "#fff")
    on idle:
        matrixcolor ColorizeMatrix(idle, "#fff")
    on hover:
        matrixcolor ColorizeMatrix(hover, "#fff")
    on insensitive:
        matrixcolor ColorizeMatrix(insensitive, "#fff")
    on selected_idle:
        matrixcolor ColorizeMatrix(selected_idle, "#fff")
    on selected_hover:
        matrixcolor ColorizeMatrix(selected_hover, "#fff")

## A simple transform to easily resize buttons. Used by some layouts.
transform zoom_button(z):
    zoom z

default mr_layout_open = False

## A screen that's only for development; allows you to try out the different
## layouts on each music room template. You can remove it and references to it
## once you've picked a layout.
screen select_music_room_layout(mr, **properties):
    frame:
        style_prefix 'mr_layout'
        properties properties
        has vbox
        xalign 0.5
        spacing 6

        text "LAYOUT SELECT":
            style "mr_layout_title_text"
            xalign 0.5

        add Solid("#9e87dc") xalign 0.5 xsize 300 ysize 2

        null height 6

        textbutton "Layout 1":
            action ShowMenu("music_room3", mr=mr)
            xminimum 300
        textbutton "Layout 2":
            action ShowMenu("music_room2", mr=mr)
            xminimum 300
        textbutton "Layout 3":
            action ShowMenu("music_room", mr=mr)
            xminimum 300
        textbutton "Layout 4":
            action ShowMenu("music_room4", mr=mr)
            xminimum 300
        textbutton "Layout 5":
            action ShowMenu("music_room5", mr=mr)
            xminimum 300
style mr_layout_frame:
    background "#1a1730"
    xpadding 12
    ypadding 10
style mr_layout_dropdown_frame:
    background "#120f24f0"
    xpadding 6
    ypadding 6
style mr_layout_button:
    background "#2a2540"
    hover_background "#39305a"
    selected_background "#5a4489"
    xpadding 12
    ypadding 8
style mr_layout_button_text:
    hover_color "#d9ccff"
    selected_color "#f0c676"
    idle_color "#f1effa"
    insensitive_color "#666"
    size 22
style mr_layout_title_text is text:
    color "#e4d6ff"
    size 44
    font "fonts/cinzel/Cinzel-Bold.otf"

################################################################################
## SCREENS - VERSION 1
################################################################################
## Note! This music room gets passed in an ExtendedMusicRoom object as declared
## earlier. If you wanted to have multiple music rooms, you would need to
## declare multiple ExtendedMusicRoom objects, and you would pass those into
## the music_room screen to use.
screen music_room(mr):

    tag menu

    ## Needed to have easy access to information on the currently playing song.
    ## Required for ALL music rooms!
    ## If you'd like to begin the music room without any songs playing, remove
    ## this line and include the following three lines:
    # on 'show' action Stop(mr.channel)
    # on 'replace' action Stop(mr.channel)
    # default current_track = None
    ## Setting current_track to mr.get_current_song() as seen here will make it
    ## pick out whichever song is currently playing (e.g. the main menu track).
    default current_track = mr.get_current_song()
    default category_filter = "menu"
    default category_open = False

    style_prefix "music_room"

    add "#292835" ## The background image

    ## To return to the main menu
    textbutton _("Return") action Return() align (0.0, 1.0) text_size 40:
        left_margin 25 bottom_margin 25

    ## Buttons to go to the different layouts. Remove once you've decided
    ## on which layout to use.
    use select_music_room_layout(mr, left_margin=200, align=(0.0, 1.0))

    ## The track list. These are displayed either in the order they were added
    ## to the music room in or in alphabetical order, depending on whether
    ## alphabetical sorting was turned on or not. You can arrange this however
    ## you like, with whichever information you like!
    frame:
        style_prefix 'track_list'
        xsize 750 left_margin 25 top_margin 25
        vbox:
            spacing 8
            hbox:
                spacing 10
                text _("Category") style "track_list_text" yalign 0.5
                textbutton music_track_category_label(category_filter):
                    style "track_list_category_button"
                    action ToggleScreenVariable("category_open")
            if category_open:
                frame:
                    style "track_list_category_dropdown_frame"
                    has vbox
                    spacing 2
                    textbutton _("MENU   *"):
                        style "track_list_category_option_button"
                        action [SetScreenVariable("category_filter", "menu"), SetScreenVariable("category_open", False)]
                    textbutton _("STORY  *"):
                        style "track_list_category_option_button"
                        action [SetScreenVariable("category_filter", "story"), SetScreenVariable("category_open", False)]
                    textbutton _("DLC    *"):
                        style "track_list_category_option_button"
                        action [SetScreenVariable("category_filter", "dlc"), SetScreenVariable("category_open", False)]
            viewport:
                mousewheel True scrollbars "vertical" draggable True
                has vbox
                label _("Track List") style "music_room_title"
                ## get_tracklist takes one argument, all_tracks. If all_tracks is
                ## True, it shows all tracks, including locked ones (which will be
                ## shown grayed out). If all_tracks is False, it only shows unlocked
                ## tracks.
                for num, song in enumerate(music_room_filtered_tracklist(mr, category_filter)):
                    button:
                        action mr.Play(song.path)
                        sensitive (not song.locked)
                        has hbox
                        fixed:
                            if song is current_track:
                                ## If the song is currently playing, add a bit of
                                ## flair with some audio bars.
                                add Transform('audio_bars', ysize=30, xalign=0.5,
                                    yzoom=-1.0, yalign=0.55)
                            else:
                                ## The track number. +1 is because enumerate starts
                                ## at 0 instead of 1.
                                text str(num+1) align (0.5, 0.55)
                        vbox:
                            spacing 4
                            ## Track info
                            if song.locked:
                                label _("Locked Track")
                                text _(music_track_hint(song.path))
                            else:
                                label song.name
                                text music_track_artist(song.path, song.artist)

    ## This holds the album art, song title, artist, music bar, and music
    ## controls. You may adjust this however you wish! The important part
    ## is generally the actions on the buttons, and the music bar is special
    ## so you can click it to seek in the song.
    frame:
        right_margin 45 background None
        xalign 1.0 yalign 0.0
        has vbox
        if current_track:
            add current_track.art xalign 0.5 ysize 440 fit "contain"
            text current_track.name
            text music_track_artist(current_track.path, current_track.artist)
            ## Include more fields if you like e.g.
            # text current_track.description
        else:
            ## To maintain sizing, the default art is shown at alpha 0.0.
            ## You can also just include it without the alpha 0.0 to display
            ## it regardless of whether a track is playing or not.
            add mr.default_art xalign 0.5 alpha 0.0 ysize 440 fit "contain"
            text "" # This represents the space taken up by the song title
            text _("No song playing")

        hbox:
            spacing 8
            ## This fixed (and the duration one below it) ensure that the
            ## pos and duration text don't change size as the text updates
            ## (which could move the hbox around since it's center-aligned).
            fixed:
                yfit True xsize 100
                add mr.get_pos(style="music_room_pos")
            ## This makes a special music bar which shows the current position
            ## of the song, and also allows you to click the bar to skip around.
            ## It takes the same style properties as a regular bar, and in this
            ## case even gets the style "music_room_bar" because of the style
            ## prefix.
            ## It needs to be passed the music room - in our case, that's
            ## `room mr` because the music room is passed in as "mr".
            music_bar room mr
            ## Again, this fixed helps keep the hbox from changing size.
            fixed:
                yfit True xsize 100
                add mr.get_duration(style="music_room_duration")

        ## This contains the music controls. You can remove whichever ones
        ## you don't need.
        hbox:
            ################## Back 10 seconds button ##################
            imagebutton:
                idle "back_10_button"
                ## This automatically colorizes the button. If you are supplying
                ## your own images, you can remove any `at` ATL transforms to
                ## these buttons.
                at colorize_button()
                action mr.AdjustTrackPos(-10)
            ################## Shuffle button ##################
            imagebutton:
                idle "shuffle_button"
                at colorize_button(MUSIC_ROOM_INSENSITIVE_COLOR, MUSIC_ROOM_IDLE_COLOR)
                action mr.ToggleShuffle()
            ################## Previous, play/pause, next buttons ##################
            imagebutton:
                idle "prev_button"
                at colorize_button()
                action mr.Previous()
            imagebutton:
                at colorize_button()
                idle "pause_button" hover "pause_button"
                selected_idle "play_button" selected_hover "play_button"
                action mr.PlayAction()
            imagebutton:
                idle "next_button"
                at colorize_button()
                action mr.Next()
            ################## Repeat all, repeat one buttons ##################
            imagebutton:
                at colorize_button(idle=MUSIC_ROOM_INSENSITIVE_COLOR,
                    hover=MUSIC_ROOM_IDLE_COLOR)
                idle "repeat_all_button"
                if mr.single_track:
                    foreground "repeat_one_button"
                action mr.CycleLoop()
            ################## Forward 10 seconds button ##################
            imagebutton:
                idle "forward_10_button"
                at colorize_button()
                action mr.AdjustTrackPos(10)

################################################################################
## Styles for Music Room 1
################################################################################
style music_room_vbox:
    ycenter 0.5 spacing 25
style music_room_frame:
    background "#21212d"
    yalign 0.5 xalign 0.0
    left_margin 25 padding (25, 25)
style music_room_text:
    color "#fff"
    xalign 0.5
style music_room_title:
    background None xalign 0.5 bottom_padding 15
style music_room_title_text:
    font gui.name_text_font
    size 50 color "#ff8335" xalign 0.5
style music_room_hbox:
    spacing 50 xalign 0.5 yalign 1.0
style music_room_image_button:
    align (0.5, 0.5)
style music_room_bar:
    xsize 700 xalign 0.5 ysize 38
    right_bar "#21212d"
    left_bar "#fc5f39"
style music_room_pos:
    color "#fff" xalign 0.5 adjust_spacing False
style music_room_duration:
    color "#fff" xalign 0.5 adjust_spacing False

################################################################################
## Styles for the track list, shared generally by the other rooms.
################################################################################
style track_list_frame:
    background "#21212d"
    yalign 0.0 xalign 0.0
    padding (25, 25)
style track_list_viewport:
    xfill False yfill False ymaximum config.screen_height-200
style track_list_side:
    spacing 20
style track_list_vbox:
    spacing 0
style track_list_button:
    right_padding 45
    background Transform("#ff8335", ysize=2, yalign=1.0)
    hover_foreground "#fff1"
    ypadding 15 xfill True
style track_list_hbox:
    xalign 0.0 spacing 18
style track_list_fixed:
    xsize 45 ysize 45 yalign 0.5
style track_list_text:
    color "#bfbfb9"
    insensitive_color "#666"
style track_list_label:
    background None padding (2, 0)
style track_list_label_text:
    color "#f7f7ed" hover_color "#f93c3e" selected_color "#ff8335"
    insensitive_color "#666"
style track_list_vscrollbar:
    thumb "#fc5f39" base_bar "#292835"
style track_list_category_button is button:
    background "#2f2f45"
    hover_background "#3e3e63"
    selected_background "#45456d"
    xpadding 12
    ypadding 6
style track_list_category_button_text is text:
    color "#f7f7ed"
    hover_color "#f93c3e"
    size 22
style track_list_category_dropdown_frame is frame:
    background "#141422dd"
    xpadding 6
    ypadding 6
style track_list_category_option_button is button:
    background "#2f2f45"
    hover_background "#3e3e63"
    selected_background "#45456d"
    xpadding 12
    ypadding 6
style track_list_category_option_button_text is text:
    color "#f7f7ed"
    hover_color "#f93c3e"
    size 22

################################################################################
## SCREENS - VERSION 2
################################################################################
screen music_room2(mr):
    tag menu

    default current_track = mr.get_current_song()
    default category_filter = "menu"
    default category_open = False

    add "#292835" ## The background image

    ## Buttons to go to the different layouts. Remove once you've decided
    ## on which layout to use.
    use select_music_room_layout(mr, yalign=1.0, bottom_margin=100)

    ## To return to the main menu
    textbutton _("Return") action Return() align (0.0, 1.0) text_size 40:
        left_margin 25 bottom_margin 25

    ## If you'd like to use a sidebar with this layout, you will need to indent
    ## everything in this vbox one level right and include:
    ##
    # use game_menu(_("Music Room")):
    ##
    ## See music_room3 for code you can use if you have Easy Ren'Py GUI with
    ## a sidebar.
    vbox:
        style_prefix 'music_room2' first_spacing 52
        hbox:
            ## The track list. These are displayed either in the order they
            ## were added to the music room in or in alphabetical order,
            ## depending on whether alphabetical sorting was turned on or not.
            ## You can arrange this however you like, with whichever information
            ## you like!
            frame:
                style_prefix 'track_list'
                ## If you want this to accommodate a sidebar, set the xsize
                ## smaller e.g. xsize config.screen_width-1050
                xsize config.screen_width-700
                ysize config.screen_height-250
                vbox:
                    spacing 8
                    hbox:
                        spacing 10
                        text _("Category") style "track_list_text" yalign 0.5
                        textbutton music_track_category_label(category_filter):
                            style "track_list_category_button"
                            action ToggleScreenVariable("category_open")
                    if category_open:
                        frame:
                            style "track_list_category_dropdown_frame"
                            has vbox
                            spacing 2
                            textbutton _("MENU   *"):
                                style "track_list_category_option_button"
                                action [SetScreenVariable("category_filter", "menu"), SetScreenVariable("category_open", False)]
                            textbutton _("STORY  *"):
                                style "track_list_category_option_button"
                                action [SetScreenVariable("category_filter", "story"), SetScreenVariable("category_open", False)]
                            textbutton _("DLC    *"):
                                style "track_list_category_option_button"
                                action [SetScreenVariable("category_filter", "dlc"), SetScreenVariable("category_open", False)]
                    viewport:
                        mousewheel True scrollbars "vertical" draggable True
                        has vbox
                        label _("Track List") style "music_room_title" xalign 0.5
                        for num, song in enumerate(music_room_filtered_tracklist(mr, category_filter)):
                            button:
                                action mr.Play(song.path)
                                sensitive (not song.locked)
                                has hbox
                                fixed:
                                    if song is current_track:
                                        ## If the song is currently playing, add a
                                        ## bit of flair with some audio bars.
                                        add Transform('audio_bars', ysize=30,
                                            xalign=0.5, yzoom=-1.0, yalign=0.55)
                                    else:
                                        ## The track number
                                        text str(num+1) align (0.5, 0.55)
                                vbox:
                                    spacing 4
                                    ## Track info
                                    if song.locked:
                                        label _("Locked Track")
                                        text _(music_track_hint(song.path))
                                    else:
                                        label song.name
                                        text music_track_artist(song.path, song.artist)
            vbox:
                yalign 0.0
                if current_track:
                    add current_track.art xalign 0.5 xsize 550 fit "contain"
                    label current_track.name
                    text music_track_artist(current_track.path, current_track.artist)
                else:
                    add mr.default_art xalign 0.5 xsize 550 fit "contain"
                    label _("No song playing")

        ## The music controls
        ## This contains the music controls. You can remove whichever ones
        ## you don't need.
        hbox:
            spacing 45
            ################## Back 10 seconds button ##################
            imagebutton:
                idle "back_10_button"
                at colorize_button()
                action mr.AdjustTrackPos(-10)
            ################## Shuffle button ##################
            imagebutton:
                idle "shuffle_button"
                at colorize_button(MUSIC_ROOM_INSENSITIVE_COLOR, MUSIC_ROOM_IDLE_COLOR)
                action mr.ToggleShuffle()
            ################## Previous, play/pause, next buttons ##################
            imagebutton:
                idle "prev_button"
                at colorize_button(), zoom_button(0.65)
                action mr.Previous()
            imagebutton:
                at colorize_button(), zoom_button(0.35)
                idle "pause_button" hover "pause_button"
                selected_idle "play_button" selected_hover "play_button"
                action mr.PlayAction()
            imagebutton:
                idle "next_button"
                at colorize_button(), zoom_button(0.65)
                action mr.Next()
            ################## Repeat all, repeat one buttons ##################
            imagebutton:
                at colorize_button(idle=MUSIC_ROOM_INSENSITIVE_COLOR,
                    hover=MUSIC_ROOM_IDLE_COLOR)
                idle "repeat_all_button"
                if mr.single_track:
                    foreground "repeat_one_button"
                action mr.CycleLoop()
            ################## Forward 10 seconds button ##################
            imagebutton:
                idle "forward_10_button"
                at colorize_button()
                action mr.AdjustTrackPos(10)

        hbox:
            spacing 8
            ## This fixed (and the duration one below it) ensure that the
            ## pos and duration text don't change as the text updates (which
            ## could move the hbox around since it's changing size).
            fixed:
                yfit True xsize 100
                add mr.get_pos(style="music_room_pos")
            ## This makes a special music bar which shows the current position
            ## of the song, and also allows you to click the bar to skip around.
            ## It takes the same style properties as a regular bar, and in this
            ## case even gets the style "music_room_bar" because of the style
            ## prefix.
            music_bar room mr
            fixed:
                yfit True xsize 100
                add mr.get_duration(style="music_room_duration")
            ################## Music volume bar ##################
            null width 40
            imagebutton:
                idle "gui/music_room/volume.webp"
                at colorize_button(), zoom_button(0.45)
                hovered CaptureFocus("volume_slider_drop")
                action CaptureFocus("volume_slider_drop")

    ## This shows a volume bar popup when the volume control button is hovered
    ## or pressed.
    if GetFocusRect("volume_slider_drop"):
        default hide_volume = False
        nearrect:
            focus "volume_slider_drop" prefer_top True
            button:
                modal True
                action NullAction()
                hovered SetScreenVariable('hide_volume', False)
                unhovered SetScreenVariable('hide_volume', True)
                background None xpadding 65 top_padding 40
                bottom_padding 90 yoffset 75
                xalign 0.5 yalign 1.0
                vbar value MixerValue(mr.channel) xysize (25, 200):
                    xalign 0.5 top_bar "#21212d" thumb None
                    hovered SetScreenVariable('hide_volume', False)
                    bottom_bar "#fc5f39"
        if hide_volume:
            timer 1.0 action [ClearFocus("volume_slider_drop"),
                SetScreenVariable('hide_volume', False)]

################################################################################
## Styles for Music Room 2
################################################################################
style music_room2_vbox:
    xalign 0.5 spacing 20 yalign 0.5
style music_room2_hbox:
    spacing 15 xalign 0.5
style music_room2_image_button:
    align (0.5, 0.5)
style music_room2_bar:
    xsize 1050 xalign 0.5 ysize 38
    right_bar "#21212d"
    left_bar "#fc5f39"
style music_room2_slider:
    xsize 200 xalign 0.5 ysize 25 yalign 0.5
    right_bar "#21212d"
    left_bar "#fc5f39"
    thumb None
style music_room2_label:
    background None xalign 0.0
style music_room2_label_text:
    color "#f7f7ed"
style music_room2_text:
    color "#bfbfb9"

################################################################################
## SCREENS - VERSION 3
################################################################################
screen music_room3(mr):

    tag menu

    ## Needed to have easy access to information on the currently playing song.
    ## Required for ALL music rooms!
    default current_track = mr.get_current_song()
    default category_filter = "menu"
    default category_open = False

    style_prefix "music_room3"

    add HBox(Transform("#1a1730", xsize=350), "#1a1630b2") # Background

    # Left sidebar category controls.
    fixed:
        xpos 0
        ypos 0
        xsize 350
        ysize config.screen_height

        frame:
            style "music_room3_sidebar_panel"
            xfill True
            yfill True

            vbox:
                xfill True
                spacing 14
                text _("CATEGORY"):
                    style "music_room3_sidebar_title"
                    xalign 0.5

                add Solid("#9e87dc") xalign 0.5 xsize 300 ysize 2

                null height 8

                button:
                    style "music_room3_category_row"
                    selected (category_filter == "menu")
                    action SetScreenVariable("category_filter", "menu")
                    fixed:
                        xfill True
                        ysize 52
                        text _("MENU"):
                            style "music_room3_category_row_text"
                            xalign 0.0
                            yalign 0.5
                        text "*":
                            style "music_room3_category_row_star"
                            xalign 0.97
                            yalign 0.5

                button:
                    style "music_room3_category_row"
                    selected (category_filter == "story")
                    action SetScreenVariable("category_filter", "story")
                    fixed:
                        xfill True
                        ysize 52
                        text _("STORY"):
                            style "music_room3_category_row_text"
                            xalign 0.0
                            yalign 0.5
                        text "*":
                            style "music_room3_category_row_star"
                            xalign 0.97
                            yalign 0.5

                button:
                    style "music_room3_category_row"
                    selected (category_filter == "dlc")
                    action SetScreenVariable("category_filter", "dlc")
                    fixed:
                        xfill True
                        ysize 52
                        text _("DLC"):
                            style "music_room3_category_row_text"
                            xalign 0.0
                            yalign 0.5
                        text "*":
                            style "music_room3_category_row_star"
                            xalign 0.97
                            yalign 0.5

                null height 10
                add Solid("#9e87dc") xalign 0.5 xsize 300 ysize 2
                null height 10
                use select_music_room_layout(mr)
                null height 10
                add Solid("#9e87dc") xalign 0.5 xsize 300 ysize 2
                null yfill True
                textbutton _("RETURN"):
                    style "music_room3_sidebar_return_button"
                    action ShowMenu("extra_menu")

    ############################################################################
    ## If you have a standard Ren'Py UI sidebar, you can use this:
    ##
    # use game_menu(_("Music Room")):
    ##
    ## Otherwise, if you're using my Easy Ren'Py GUI (https://feniksdev.itch.io/easy-renpy-gui)
    ## you can use this:
    ##
    fixed:
        yfill True
        xsize config.screen_width-420
        align (1.0, 0.5)
    ##
    ############################################################################

        frame:
            style_prefix 'music_room3_list'
            xfill True top_margin 25 yfill True bottom_margin 220
            vbox:
                spacing 8
                text _("TRACK LIST"):
                    style "music_room3_list_label_text"
                    color "#ffffff"
                    xalign 0.5
                    text_align 0.5
                viewport:
                    mousewheel True scrollbars "vertical" draggable True
                    has vbox
                    ## get_tracklist takes one argument, all_tracks. If all_tracks is
                    ## True, it shows all tracks, including locked ones (which will be
                    ## shown grayed out). If all_tracks is False, it only shows unlocked
                    ## tracks.
                    for num, song in enumerate(music_room_filtered_tracklist(mr, category_filter)):
                        button:
                            action mr.Play(song.path)
                            sensitive (not song.locked)
                            has hbox
                            fixed:
                                if song is current_track:
                                    ## If the song is currently playing, add a bit of
                                    ## flair with some audio bars.
                                    add Transform('audio_bars', ysize=30, xalign=0.5,
                                        yzoom=-1.0, yalign=0.55)
                                else:
                                    ## The track number. +1 is because enumerate starts
                                    ## at 0 instead of 1.
                                    text str(num+1) align (0.5, 0.55)
                            add song.art ysize 100 fit "contain"
                            vbox:
                                spacing 4
                                ## Track info
                                if song.locked:
                                    label _("Locked Track")
                                    text _(music_track_hint(song.path))
                                else:
                                    label song.name
                                    text music_track_artist(song.path, song.artist)

        ## This holds the album art, song title, artist, music bar, and music
        ## controls. You may adjust this however you wish! The important part
        ## is generally the actions on the buttons, and the music bar is special
        ## so you can click it to seek in the song.
        frame:
            style_prefix 'musicroom3'
            has hbox
            xalign 0.5 yalign 0.5
            if current_track:
                add current_track.art ysize 150 fit "contain"
            else:
                add mr.default_art ysize 150 fit "contain"
            vbox:
                xsize 250
                if current_track:
                    text current_track.name
                    text music_track_artist(current_track.path, current_track.artist) color "#c9c3dc"
                else:
                    text _("No song playing")

            null width 10

            vbox:
                yalign 0.5 spacing 15
                hbox:
                    xalign 0.5 spacing 30
                    ################## Shuffle button ##################
                    imagebutton:
                        idle "shuffle_button"
                        at colorize_button(
                            idle="#6b657a",
                            hover="#b39df0",
                            selected_idle="#8c78c9",
                            selected_hover="#b39df0",
                            insensitive="#6b657a"), zoom_button(0.6)
                        action mr.ToggleShuffle()
                    ############ Previous, play/pause, next buttons ############
                    imagebutton:
                        idle "prev_button"
                        at colorize_button(
                            idle="#8c78c9",
                            hover="#b39df0",
                            selected_idle="#8c78c9",
                            selected_hover="#b39df0",
                            insensitive="#6b657a"), zoom_button(0.4)
                        action mr.Previous()
                    imagebutton:
                        at colorize_button(
                            idle="#8c78c9",
                            hover="#b39df0",
                            selected_idle="#8c78c9",
                            selected_hover="#b39df0",
                            insensitive="#6b657a"), zoom_button(0.25)
                        idle "pause_button" hover "pause_button"
                        selected_idle "play_button" selected_hover "play_button"
                        action mr.PlayAction()
                    imagebutton:
                        idle "next_button"
                        at colorize_button(
                            idle="#8c78c9",
                            hover="#b39df0",
                            selected_idle="#8c78c9",
                            selected_hover="#b39df0",
                            insensitive="#6b657a"), zoom_button(0.4)
                        action mr.Next()
                    ################## Repeat all, repeat one buttons ##################
                    imagebutton:
                        at colorize_button(
                            idle="#6b657a",
                            hover="#b39df0",
                            selected_idle="#8c78c9",
                            selected_hover="#b39df0",
                            insensitive="#6b657a"), zoom_button(0.6)
                        idle "repeat_all_button"
                        if mr.single_track:
                            foreground "repeat_one_button"
                        action mr.CycleLoop()

                ################## Music Bar ##################
                hbox:
                    spacing 8
                    fixed:
                        yfit True xsize 100
                        add mr.get_pos(style="music_room_pos")
                    music_bar room mr
                    fixed:
                        yfit True xsize 100
                        add mr.get_duration(style="music_room_duration")

            add "gui/music_room/volume.webp" zoom 0.45 yalign 0.5:
                matrixcolor ColorizeMatrix("#b39df0", "#fff")

            bar value MixerValue(mr.channel) xysize (150, 25):
                xalign 0.5 right_bar "#221b35" thumb None yalign 0.5
                left_bar "#8c78c9"


    ## Buttons to go to the different layouts. Remove once you've decided
    ## on which layout to use.

style musicroom3_frame:
    yalign 1.0 xalign 0.5 xfill True ysize 200
    background Frame(
        Fixed(
            Transform("#8c78c9", xysize=(100, 100)),
            Transform("#2a2540", xysize=(90, 90), align=(0.5, 0.5)),
            xysize=(100, 100)
        ), 10, 10
    )

style musicroom3_hbox:
    spacing 20
style musicroom3_image_button:
    yalign 0.5
style musicroom3_bar:
    ysize 25 xsize 480
    yalign 0.5
    right_bar "#221b35" thumb None
    left_bar "#8c78c9"
style musicroom3_text:
    yalign 0.5 size 25 color "#f1effa"
style musicroom3_vbox:
    yalign 0.5

style music_room3_list_frame is track_list_frame:
    background "#1a1730d6"
style music_room3_list_viewport is track_list_viewport
style music_room3_list_viewport:
    ymaximum config.screen_height-300
style music_room3_list_side is track_list_side
style music_room3_list_vbox is track_list_vbox
style music_room3_list_button is track_list_button:
    background Transform("#8c78c9", ysize=2, yalign=1.0)
    hover_foreground "#b39df022"
style music_room3_list_hbox is track_list_hbox
style music_room3_list_fixed is track_list_fixed
style music_room3_list_text is track_list_text:
    color "#ffffff"
style music_room3_list_label is track_list_label:
    background None
style music_room3_list_label_text is track_list_label_text:
    color "#ffffff"
    hover_color "#b39df0"
    selected_color "#8c78c9"
    insensitive_color "#666"
style music_room3_list_vscrollbar is track_list_vscrollbar:
    thumb "#8c78c9"
    base_bar "#2a2540"
style music_room3_category_button is button:
    background "#2a2540"
    hover_background "#39305a"
    selected_background "#4a3a74"
    xpadding 12
    ypadding 6
style music_room3_category_button_text is text:
    color "#f1effa"
    hover_color "#b39df0"
    size 22
style music_room3_category_dropdown_frame is frame:
    background "#17142bdc"
    xpadding 6
    ypadding 6
style music_room3_category_option_button is button:
    background Frame(Solid("#231c3a"), 10, 10)
    hover_background Frame(Solid("#31264d"), 10, 10)
    selected_background Frame(Solid("#4f3b79"), 10, 10)
    xpadding 22
    ypadding 12
    xfill True
    top_margin 6
style music_room3_category_option_button_text is text:
    color "#ffffff"
    hover_color "#ffffff"
    selected_color "#ffffff"
    size 34
    font "fonts/cinzel/Cinzel-Bold.otf"
    xalign 0.0

style music_room3_sidebar_panel is frame:
    background Solid("#1a1730")
    xpadding 16
    ypadding 18

style music_room3_sidebar_title is text:
    color "#e4d6ff"
    size 52
    font "fonts/cinzel/Cinzel-Bold.otf"
    text_align 0.5

style music_room3_sidebar_divider is text:
    color "#d6a76f"
    size 24
    font "fonts/cinzel/Cinzel-Bold.otf"

style music_room3_category_row is button:
    background Frame(Solid("#231c3a"), 10, 10)
    hover_background Frame(Solid("#31264d"), 10, 10)
    selected_background Frame(Solid("#5a4489"), 10, 10)
    xfill True
    xpadding 22
    ypadding 8
    top_margin 6

style music_room3_category_row_text is text:
    color "#ffffff"
    hover_color "#ffffff"
    selected_color "#ffffff"
    size 34
    font "fonts/cinzel/Cinzel-Bold.otf"

style music_room3_category_row_star is text:
    color "#f2e6cf"
    hover_color "#ffd9a0"
    selected_color "#ffffff"
    size 30
    font "fonts/cinzel/Cinzel-Bold.otf"

style music_room3_sidebar_return_button is button:
    background Frame(Solid("#231c3a"), 10, 10)
    hover_background Frame(Solid("#31264d"), 10, 10)
    selected_background Frame(Solid("#5a4489"), 10, 10)
    xfill True
    xpadding 22
    ypadding 10
    bottom_margin 8

style music_room3_sidebar_return_button_text is text:
    color "#ffffff"
    hover_color "#ffd9a0"
    size 32
    font "fonts/cinzel/Cinzel-Bold.otf"
    xalign 0.5

################################################################################
## SCREENS - VERSION 4
################################################################################
screen music_room4(mr):
    tag menu

    default current_track = mr.get_current_song()
    default category_filter = "menu"
    default category_open = False

    add Solid("#090b2acc")
    add Solid("#2a31581c")

    textbutton _("Return"):
        action Return()
        xalign 0.97
        yalign 0.04
        text_size 32

    textbutton "|||":
        action NullAction()
        xpos 18
        ypos 10
        text_size 30
        background None

    # Top tabs
    hbox:
        xalign 0.5
        ypos 36
        spacing 70
        text _("Image Gallery") color "#bfc1d7" size 46
        text _("* Music Room") color "#efe3a7" size 46

    # Left artwork/title panel
    frame:
        background Solid("#000742dd")
        xpos 90
        ypos 220
        xsize 650
        ysize 420
        padding (12, 12)

        fixed:
            add Solid("#f2e8b0") xsize 626 ysize 396
            add Solid("#000742") xpos 6 ypos 6 xsize 614 ysize 384
            if current_track:
                add current_track.art xalign 0.5 yalign 0.5 fit "contain" xsize 420 ysize 260
            else:
                text "♪" xalign 0.5 yalign 0.5 size 220 color "#efe3a7"

    text (current_track.name if current_track else _("Track Title")):
        xpos 280
        ypos 676
        size 54
        color "#c8c6df"

    # Right track list
    side "c r":
        xpos 920
        ypos 205
        xysize (860, 620)

        vbox:
            spacing 10

            hbox:
                spacing 10
                text "Category" size 26 color "#bfc1d7" yalign 0.5
                textbutton music_track_category_label(category_filter):
                    style "track_list_category_button"
                    action ToggleScreenVariable("category_open")

            if category_open:
                frame:
                    style "track_list_category_dropdown_frame"
                    has vbox
                    spacing 2
                    textbutton _("MENU   *"):
                        style "track_list_category_option_button"
                        action [SetScreenVariable("category_filter", "menu"), SetScreenVariable("category_open", False)]
                    textbutton _("STORY  *"):
                        style "track_list_category_option_button"
                        action [SetScreenVariable("category_filter", "story"), SetScreenVariable("category_open", False)]
                    textbutton _("DLC    *"):
                        style "track_list_category_option_button"
                        action [SetScreenVariable("category_filter", "dlc"), SetScreenVariable("category_open", False)]

            viewport:
                id "music_room4_vp"
                mousewheel True
                draggable True
                scrollbars "vertical"
                has vbox
                spacing 16

                for num, song in enumerate(music_room_filtered_tracklist(mr, category_filter)):
                    button:
                        action mr.Play(song.path)
                        sensitive (not song.locked)
                        xsize 790
                        ysize 88
                        background Frame(Solid("#000742"), 22, 22)
                        hover_background Frame(Solid("#0f1460"), 22, 22)
                        selected_background Frame(Solid("#101873"), 22, 22)

                        fixed:
                            add Solid("#efe3a7") xsize 790 ysize 88
                            add Solid("#000742") xpos 6 ypos 6 xsize 778 ysize 76
                            if song.locked:
                                text _(music_track_hint(song.path)) xalign 0.5 yalign 0.5 size 26 color "#868aaa"
                            else:
                                text song.name xalign 0.5 yalign 0.5 size 42 color ("#d9def2" if song is current_track else "#868aaa")
                            text "*" xpos 22 yalign 0.5 size 32 color "#efe3a7"
                            text "*" xalign 0.97 yalign 0.5 size 32 color "#efe3a7"

        vbar value YScrollValue("music_room4_vp") style "track_list_vscrollbar"

    # Bottom controls/progress
    fixed:
        xpos 80
        ypos 860
        xsize 1700
        ysize 170

        hbox:
            spacing 22
            ypos 24
            textbutton "<<" action mr.Previous() text_size 58 background None
            textbutton (">" if current_track else ">") action mr.PlayAction() text_size 58 background None
            textbutton ">>" action mr.Next() text_size 58 background None

        fixed:
            xpos 360
            ypos 86
            xsize 1260
            ysize 36
            music_bar room mr

    # Layout picker for development/testing.
    use select_music_room_layout(mr, align=(0.5, 1.0), bottom_margin=20)

################################################################################
## SCREENS - VERSION 5
################################################################################
screen music_room5(mr):
    tag menu
    default current_track = mr.get_current_song()
    default category_filter = "menu"
    default category_open = False
    default hovered_track_path = None

    if renpy.loadable("gui/mainmenu_bg3.png"):
        add im.Scale("gui/mainmenu_bg3.png", config.screen_width, config.screen_height)
    elif renpy.loadable("gui/mainmenu_bg2.png"):
        add im.Scale("gui/mainmenu_bg2.png", config.screen_width, config.screen_height)
    elif renpy.loadable("gui/mainmenu_bg.png"):
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    else:
        add Solid("#120f22")

    add Solid("#07060c99")
    add Solid("#2b1d3a36")

    fixed:
        xalign 0.5
        yalign 0.5
        xsize 1580
        ysize 990

        add Frame(Solid("#291f40d8"), 18, 18) xysize (1580, 990)
        add Frame(Solid("#8f5f2f4a"), 16, 16) xpos 8 ypos 8 xysize (1564, 974)
        add Frame(Solid("#100d1fd8"), 14, 14) xpos 16 ypos 16 xysize (1548, 958)
        add Solid("#0b0918ad") xpos 28 ypos 28 xsize 1524 ysize 934

        # Header row.
        fixed:
            xpos 40
            ypos 42
            xsize 1500
            ysize 72

            hbox:
                spacing 14
                yalign 0.5
                text _("CATEGORY"):
                    color "#a8a0b9"
                    size 40
                    font "fonts/cinzel/Cinzel-Bold.otf"
                    yalign 0.5
                textbutton music_track_category_label(category_filter):
                    action ToggleScreenVariable("category_open")
                    background Frame(Solid("#2a1c33f0"), 6, 6)
                    hover_background Frame(Solid("#3b2948f0"), 6, 6)
                    xpadding 16
                    ypadding 7
                    text_color "#f4d8aa"
                    text_hover_color "#ffd78a"
                    text_size 34
                    text_font "fonts/cinzel/Cinzel-Bold.otf"
                    yalign 0.5

        if category_open:
            frame:
                xpos 220
                ypos 118
                background Frame(Solid("#120d1bf2"), 8, 8)
                xpadding 8
                ypadding 8

                has vbox
                spacing 4

                textbutton _("MENU   *"):
                    action [SetScreenVariable("category_filter", "menu"), SetScreenVariable("category_open", False)]
                    background Frame(Solid("#2f2438"), 6, 6)
                    hover_background Frame(Solid("#4a3658"), 6, 6)
                    xpadding 14
                    ypadding 6
                    text_color "#f4d8aa"
                    text_hover_color "#ffd78a"
                    text_size 30
                    text_font "fonts/cinzel/Cinzel-Bold.otf"
                textbutton _("STORY  *"):
                    action [SetScreenVariable("category_filter", "story"), SetScreenVariable("category_open", False)]
                    background Frame(Solid("#2f2438"), 6, 6)
                    hover_background Frame(Solid("#4a3658"), 6, 6)
                    xpadding 14
                    ypadding 6
                    text_color "#f4d8aa"
                    text_hover_color "#ffd78a"
                    text_size 30
                    text_font "fonts/cinzel/Cinzel-Bold.otf"
                textbutton _("DLC    *"):
                    action [SetScreenVariable("category_filter", "dlc"), SetScreenVariable("category_open", False)]
                    background Frame(Solid("#2f2438"), 6, 6)
                    hover_background Frame(Solid("#4a3658"), 6, 6)
                    xpadding 14
                    ypadding 6
                    text_color "#f4d8aa"
                    text_hover_color "#ffd78a"
                    text_size 30
                    text_font "fonts/cinzel/Cinzel-Bold.otf"

        # Main track table.
        fixed:
            xpos 40
            ypos 128
            xsize 1500
            ysize 590

            add Frame(Solid("#211a32d6"), 10, 10) xysize (1500, 590)
            add Frame(Solid("#915d2e3d"), 8, 8) xpos 2 ypos 2 xysize (1496, 586)
            add Solid("#0f0d1d88") xpos 10 ypos 10 xsize 1478 ysize 568

            side "c r":
                xfill True
                yfill True

                viewport:
                    id "music_room5_vp"
                    xysize (1460, 568)
                    mousewheel True
                    draggable True
                    scrollbars None
                    has vbox
                    spacing 2

                    for num, song in enumerate(music_room_filtered_tracklist(mr, category_filter), start=1):
                        $ row_active = (song is current_track and not song.locked)
                        $ row_hovered = (hovered_track_path == song.path)
                        $ row_title_color = "#ffd7a0" if row_active else ("#f9f1e4" if row_hovered else "#f3eadb")
                        $ row_sub_color = "#f4c884" if row_active else ("#cfc0a8" if row_hovered else "#b9b0c7")
                        $ is_placeholder_art = (song.art == mr.default_art)

                        button:
                            action mr.Play(song.path)
                            hovered SetScreenVariable("hovered_track_path", song.path)
                            unhovered SetScreenVariable("hovered_track_path", None)
                            sensitive (not song.locked)
                            xsize 1460
                            ysize 112
                            background (Frame(Solid("#85532640"), 8, 8) if row_active else Frame(Solid("#00000020"), 8, 8))
                            hover_background Frame(Solid("#ffb45a0d"), 8, 8)
                            selected_background Frame(Solid("#8553264e"), 8, 8)

                            fixed:
                                if row_active:
                                    add Solid("#ffd08b12") xsize 1460 ysize 112
                                    add Solid("#ffb45a40") xsize 1460 ysize 1
                                    add Solid("#ffb45a40") ypos 111 xsize 1460 ysize 1
                                    add Solid("#ffb45a40") xsize 1 ysize 112
                                    add Solid("#ffb45a40") xpos 1459 xsize 1 ysize 112
                                    add Solid("#ffad44") xsize 5 ysize 112
                                    add Solid("#ff9f2f") xsize 1460 ysize 2
                                    add Solid("#ff9f2f") ypos 110 xsize 1460 ysize 2
                                elif row_hovered:
                                    add Solid("#ffb45a0d") xsize 1460 ysize 112
                                    add Solid("#d2a35c88") xsize 2 ysize 112
                                    add Solid("#71563466") ypos 111 xsize 1460 ysize 1
                                else:
                                    add Solid("#5f4a301e") ypos 111 xsize 1460 ysize 1

                                text str(num):
                                    xpos 14
                                    yalign 0.5
                                    color "#e2c4a0"
                                    size 48
                                    font "fonts/cinzel/Cinzel-Bold.otf"

                                fixed:
                                    xpos 52
                                    yalign 0.5
                                    xsize 148
                                    ysize 90
                                    add Frame(Solid("#b88a3d88"), 6, 6) xysize (148, 90)
                                    add Solid("#100d1fd8") xpos 1 ypos 1 xsize 146 ysize 88
                                    if song.locked:
                                        text _("LOCKED"):
                                            xalign 0.5
                                            yalign 0.5
                                            color "#877f9d"
                                            size 24
                                            font "fonts/cinzel/Cinzel-Bold.otf"
                                    else:
                                        if is_placeholder_art:
                                            add song.art xalign 0.5 yalign 0.5 fit "contain" xsize 122 ysize 74 alpha 0.78
                                            text "*" xalign 0.92 yalign 0.12 color "#f4c884" size 16
                                        else:
                                            add song.art xalign 0.5 yalign 0.5 fit "contain" xsize 138 ysize 82

                                if song.locked:
                                    text _("Locked Track"):
                                        xpos 224
                                        ypos 18
                                        color "#a9a0bc"
                                        size 52
                                        font "fonts/cinzel/Cinzel-Bold.otf"
                                    text _(music_track_hint(song.path)):
                                        xpos 224
                                        ypos 64
                                        color "#857e96"
                                        size 34
                                        font "fonts/cinzel/Cinzel-Bold.otf"
                                else:
                                    text song.name:
                                        xpos 224
                                        ypos 18
                                        color row_title_color
                                        size 58
                                        font "fonts/cinzel/Cinzel-Bold.otf"
                                    text music_track_artist(song.path, song.artist):
                                        xpos 224
                                        ypos 64
                                        color row_sub_color
                                        size 42
                                        font "fonts/cinzel/Cinzel-Bold.otf"
                                    if row_active:
                                        text _("* currently playing *"):
                                            xpos 224
                                            ypos 94
                                            color "#f2bc6a"
                                            size 28
                                            font "fonts/cinzel/Cinzel-Bold.otf"

                vbar:
                    value YScrollValue("music_room5_vp")
                    style "music_room5_vscrollbar"
                    yfill True

        # Divider ornament.
        text "──────── ✦ ────────":
            xalign 0.5
            ypos 724
            color "#d9a85f"
            size 40
            font "fonts/cinzel/Cinzel-Bold.otf"

        # Bottom player panel.
        fixed:
            xpos 40
            ypos 760
            xsize 1500
            ysize 188

            add Frame(Solid("#211a32be"), 12, 12) xysize (1500, 188)
            add Frame(Solid("#9e67343e"), 10, 10) xpos 2 ypos 2 xysize (1496, 184)
            add Solid("#0e0c1b7d") xpos 10 ypos 10 xsize 1480 ysize 168
            add Solid("#f4ca8f0f") xpos 18 ypos 18 xsize 1464 ysize 1

            frame:
                background Frame(Solid("#b88a3d66"), 6, 6)
                xpos 22
                ypos 20
                xsize 140
                ysize 140
                add Solid("#100d1fcc") xpos 1 ypos 1 xsize 138 ysize 138
                if current_track:
                    add current_track.art xalign 0.5 yalign 0.5 fit "contain" xsize 126 ysize 126
                else:
                    add music_room.default_art xalign 0.5 yalign 0.5 fit "contain" xsize 126 ysize 126

            vbox:
                xpos 182
                ypos 36
                spacing 6
                text (current_track.name if current_track else _("No Song Playing")):
                    color "#f0c676"
                    size 58
                    font "fonts/cinzel/Cinzel-Bold.otf"
                text (music_track_artist(current_track.path, current_track.artist) if current_track else _("Unknown Artist")):
                    color "#c4b7a1"
                    size 44
                    font "fonts/cinzel/Cinzel-Bold.otf"

            hbox:
                xpos 920
                ypos 50
                spacing 26
                imagebutton:
                    idle "shuffle_button"
                    at colorize_button(idle="#f2b86a", hover="#ff922d"), zoom_button(0.5)
                    action mr.ToggleShuffle()
                imagebutton:
                    idle "prev_button"
                    at colorize_button(idle="#f2b86a", hover="#ff922d"), zoom_button(0.38)
                    action mr.Previous()
                fixed:
                    xsize 86
                    ysize 72
                    text "●":
                        xalign 0.5
                        yalign 0.5
                        color "#ff963c33"
                        size 92
                        font "DejaVuSans.ttf"
                    text "●":
                        xalign 0.5
                        yalign 0.5
                        color "#ff963c66"
                        size 68
                        font "DejaVuSans.ttf"
                    imagebutton:
                        idle "pause_button"
                        hover "pause_button"
                        selected_idle "play_button"
                        selected_hover "play_button"
                        at colorize_button(idle="#f2b86a", hover="#ff922d"), zoom_button(0.34)
                        align (0.5, 0.5)
                        action mr.PlayAction()
                imagebutton:
                    idle "next_button"
                    at colorize_button(idle="#f2b86a", hover="#ff922d"), zoom_button(0.38)
                    action mr.Next()
                imagebutton:
                    idle "repeat_all_button"
                    if mr.single_track:
                        foreground "repeat_one_button"
                    at colorize_button(idle="#f2b86a", hover="#ff922d"), zoom_button(0.5)
                    action mr.CycleLoop()

            fixed:
                style_prefix "music_room5"
                xpos 760
                ypos 112
                xsize 560
                ysize 34
                music_bar room mr

            fixed:
                xpos 670
                ypos 108
                xsize 80
                ysize 34
                add mr.get_pos(style="music_room5_pos")

            fixed:
                xpos 1328
                ypos 108
                xsize 80
                ysize 34
                add mr.get_duration(style="music_room5_duration")

            add "gui/music_room/volume.webp" xpos 1365 ypos 58 zoom 0.4:
                matrixcolor ColorizeMatrix("#f2b86a", "#fff")

            bar value MixerValue(mr.channel) xpos 1420 ypos 76 xysize (66, 26):
                right_bar "#261e34"
                left_bar "#ff9f3a"
                thumb None

    textbutton _("Return"):
        action Return()
        xalign 0.035
        ypos 24
        background None
        text_color "#e8d8c0"
        text_hover_color "#ffca79"
        text_size 36
        text_font "fonts/cinzel/Cinzel-Bold.otf"

    use select_music_room_layout(mr, xpos=1550, ypos=24)

style music_room5_bar is music_room_bar:
    xsize 560
    ysize 24
    right_bar "#2a1f2d"
    left_bar Fixed(
        Transform("#e6b35a", alpha=0.96),
        Transform("#ff9a2f", alpha=0.34),
    )
    thumb None

style music_room5_pos is music_room_pos:
    color "#e8d7be"

style music_room5_duration is music_room_duration:
    color "#e8d7be"

style music_room5_vscrollbar is vscrollbar:
    xsize 12
    base_bar Frame(Solid("#2a1f2d"), 6, 6)
    thumb Frame(Solid("#d89b3c"), 6, 6)
    hover_thumb Frame(Solid("#eab35a"), 6, 6)


