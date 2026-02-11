## This file contains options that can be changed to customize your game.
##


## Basics ######################################################################

define config.name = _("Ellrijord")

define gui.show_name = True

define config.version = "1.0"


## ---------------------------------------------------------------------------
## Display / Resolution (logical render size)
## ---------------------------------------------------------------------------
define config.screen_width = 1920
define config.screen_height = 1080

# Start in fullscreen by default (recommended so you get the “F11-perfect” look).
define config.default_fullscreen = True
## ---------------------------------------------------------------------------


define gui.about = _p("""
""")


define build.name = "Ellrijord"


## Sounds and music ############################################################

define config.has_sound = True
define config.has_music = True
define config.has_voice = True

# define config.main_menu_music = "main-menu-theme.ogg"


## Transitions #################################################################

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = None


## Window management ###########################################################

## This controls dialogue window visibility (NOT OS window sizing).
define config.window = "auto"

define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)


## Preference defaults #########################################################

default preferences.text_cps = 0
default preferences.afm_time = 15


## Save directory ##############################################################

define config.save_directory = "Ellrijord-1768855811"


## Icon ########################################################################

define config.window_icon = "gui/window_icon.png"

## Build configuration #########################################################

init python:
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    build.documentation('*.html')
    build.documentation('*.txt')
