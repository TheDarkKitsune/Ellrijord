################################################################################
##
## Achievements for Ren'Py by Feniks (feniksdev.itch.io / feniksdev.com) v1.5
##
################################################################################
## This file contains code for an achievement system in Ren'Py. It is designed
## as a wrapper to the built-in achievement system, so it hooks into the
## Steam backend as well if you set up your achievement IDs the same as in
## the Steam backend.
##
## You don't have to register the achievements or anything with the backend,
## or worry about syncing - that's all automatically done for you when the
## achievements are declared and granted.
##
## To get started, declare a few achievements below. Some samples are included.
## You may also replace the `image locked_achievement` image with something
## appropriate - this image is used as the default "Locked" image for all your
## achievements unless you specify something else.
##
## Then you can make a button to go to your achievement gallery screen, e.g.
# textbutton _("Achievements") action ShowMenu("achievement_gallery")
## This will show the achievement gallery screen, declared below. You can
## further customize it however you like.
## If you click on an achievement in the gallery during development (this will
## not happen in a release build), it will toggle the achievement on/off.
## This will also let you see the achievement popup screen, similarly declared
## below. It can be customized however you like.
##
## There's also an example label you can jump to via a line like
## `jump achievement_examples` which has examples of how to grant achievements
## and track progress during gameplay.
##
## If you use this code in your projects, credit me as Feniks @ feniksdev.com
##
## Leave a comment on the tool page on itch.io or an issue on the GitHub
## if you run into any issues.
################################################################################

################################################################################
## CONFIGURATION
################################################################################
## This is a configuration value which determines whether the in-game
## achievement popup should appear when Steam is detected. Since Steam
## already has its own built-in popup, you may want to set this to False
## if you don't want to show the in-game popup alongside it.
## The in-game popup will still work on non-Steam builds, such as builds
## released DRM-free on itch.io.
define myconfig.INGAME_POPUP_WITH_STEAM = True
## The length of time the in-game popup spends hiding itself (see
## transform achievement_popout below).
define myconfig.ACHIEVEMENT_HIDE_TIME = 1.0
## True if the game should show in-game achievement popups when an
## achievement is earned. You can set this to False if you just want an
## achievement gallery screen and don't want any popups.
define myconfig.SHOW_ACHIEVEMENT_POPUPS = True
## This can be set to a sound that plays when the achievement popup appears.
## None does not play a sound.
define myconfig.ACHIEVEMENT_SOUND = None # "audio/sfx/achievement.ogg"
## If the sound plays, this sets the channel it will play on. The audio
## channel plays on the sfx mixer, and can play overlapping sounds if multiple
## achievements are earned at once.
define myconfig.ACHIEVEMENT_CHANNEL = "audio"
## This is the default name and description used for hidden achievements, unless
## you provide a more specific one. See the examples below for how to do so.
define myconfig.HIDDEN_ACHIEVEMENT_NAME = _("???{#hidden_achievement_name}")
define myconfig.HIDDEN_ACHIEVEMENT_DESCRIPTION = _("???{#hidden_achievement_description}")

## A callback, or list of callbacks, which are called when an achievement
## is granted. It is called with one argument, the achievement which
## was granted. It is only called if the achievement has not previously
## been earned. See the README for more information.
define myconfig.ACHIEVEMENT_CALLBACK = [
    ## This first example is an achievement which unlocks after two other
    ## achievements have been granted ("hidden_achievement" and
    ## "hidden_description").
    LinkedAchievement(hidden3=['hidden_achievement', 'hidden_description']),
    ## The second example is an achievement which unlocks after all achievements
    ## have been granted. This is a special case.
    LinkedAchievement(platinum_achievement='all'),
    ## You may remove these examples!
]

## This is a built-in configuration value. It will set the position of
## the Steam popup. You can change this to any of the following:
## "top_left", "top_right", "bottom_left", "bottom_right"
## You may want to use this to ensure any Steam notifications don't conflict
## with the position of the built-in notification, if you're using both.
define achievement.steam_position = None

################################################################################
## DEFINING ACHIEVEMENTS
################################################################################
## Replace this with whatever locked image you want to use as the default
## for a locked achievement.
image locked_achievement = Text("?")

################################################################################
## Start of example achievement declarations and in-game examples.
## You may remove this code down to the "End of example achievement declarations"
## comment if you don't need it - they are simply examples.
################################################################################
## Example 1 ###################################################################
## This is how you declare achievements. You will use `define` and NOT
## `default`, so you can update the achievements later (you wouldn't want the
## description to be tied to a specific save file, for example).
## The order you declare achievements in is the order they will appear in the
## achievement gallery, by default.
define sample_achievement = Achievement(
    ## The human-readable name, as it'll appear in the popup and in the gallery.
    name=_("Sample Achievement"),
    ## The id is used for Steam integration, and should match whatever ID
    ## you have set up in the Steam backend (if using).
    id="sample_achievement",
    ## Description.
    description=_("This is a sample achievement."),
    ## The image used in the popup and in the gallery once this achievement
    ## is unlocked.
    unlocked_image="gui/window_icon.png",
    ## By default all achievements use the "locked_achievement" image (declared
    ## above), but if you wanted to provide a different image, this is how
    ## you would specify it. It's used in the achievement gallery when the
    ## achievement is locked.
    locked_image="locked_achievement",
    ## All achievements are hide_name=False and hide_description=False by
    ## default, but you can change either to True to hide the name or
    ## description before the achievement is unlocked. See examples 4-7
    ## below for how to do this.
    hide_name=False,
    hide_description=False,
)
## You can grant an achievement in-game with `$ sample_achievement.grant()`

## Example 2 ###################################################################
define progress_achievement = Achievement(
    name=_("Progress Achievement"),
    id="progress_achievement",
    description=_("This is an achievement with a progress bar."),
    unlocked_image=Transform("gui/window_icon.png", matrixcolor=InvertMatrix()),
    ## To record progress, you need to specify a stat_max. This means you can
    ## show a progress bar with % completion towards the achievement. It is
    ## useful if, for example, you have an achievement counting how many
    ## chapters the player has completed which unlocks when they have seen all
    ## the chapters.
    stat_max=12,
    ## You can also provide a stat_modulo, which means the achievement is only
    ## updated in the Steam backend every time the stat reaches a multiple of
    ## the modulo.
    ## Alternatively, this system also lets you set stat_update_percent instead,
    ## so if you want it to update every 10% it progresses, you can set
    # stat_update_percent=10
    ## This is most useful for achievements with a large number of steps,
    ## like a general % completion achievement. Maybe there are 600 things to
    ## complete for the achievement, but obviously 0.1% increments are pretty
    ## meaningless so you can either set stat_modulo=6 or stat_update_percent=1
    ## and it will update Steam every 6 steps or every 1%.
    ## The in-game bar/numbers will still update every increase.
    ##
    ## This shows the progress bar in the gallery. This is True by default if
    ## you have a stat_max, but you can set it to False if you don't want to
    ## show a bar (but do want to track progress).
    show_progress_bar=True,
)
## To update progress towards completion of this achievement, you can use
# $ progress_achievement.add_progress(1)
## where 1 is how much progress is added to the stat (so, the first time it
## is called for the above example it'd be 1/12, the second it'd be 2/12, etc).
##
## Alternatively, you can directly set the progress like:
# $ progress_achievement.progress(5)
## This will directly set progress to 5, making the above example 5/12 for
## example. Alternatively, you may want to make use of the built-in "set"
## functionality, seen below.

## Example 3 ###################################################################
define set_progress_achievement = Achievement(
    name=_("Set Progress Achievement"),
    id="set_progress_achievement",
    description=_("This is an achievement with progress but no bar."),
    unlocked_image=Transform("gui/window_icon.png", matrixcolor=HueMatrix(270)),
    ## This sets a stat to progress towards
    stat_max=3,
    show_progress_bar=False, # Don't show the progress bar in the gallery
    # (though it still has a stat that it tracks)
)
## Besides the add_progress and progress methods described above, you can also
## use the add_set_progress method to add a value to a set that's tied to this
## achievement. Sets are unique - so if you try to add the same value twice, it
## only ends up in the set once. This means you don't have to check if something
## is already in the set before adding it.
## You can use this to track unique flags towards progressing this achievement.
## For example, say you add a good, bad, and neutral ending to your game.
## At those endings, you'd have one of the following lines:
## $ set_progress_achievement.add_set_progress("good_end")
## $ set_progress_achievement.add_set_progress("bad_end")
## $ set_progress_achievement.add_set_progress("neutral_end")
## When the player has seen all 3 endings, the achievement's set will have 3
## unique values in it, so the achievement will automatically unlock as soon as
## they get the third one (it doesn't matter what order they see them in).
## Note that the set is not limited to the stat_max - you could add 10 unique
## values to it, but it'll unlock the achievement after it has 3 unique values.
## This can be helpful if you have, say, 20 collectibles in your game but
## only want to require 15 of them for the achievement.
## See the example label after Example 8 for some in-script examples
## of what this might look like.

## Example 4 ###################################################################
## This achievement is "hidden", that is, its name and description appear as
## ??? in the achievement gallery until it is unlocked.
define hidden_achievement = Achievement(
    name=_("Hidden Achievement"),
    id="hidden_achievement",
    description=_("This hidden achievement hides both the name and description."),
    unlocked_image=Transform("gui/window_icon.png", matrixcolor=BrightnessMatrix(-1.0)),
    ## The important bit that hides the name and description
    hide_name=True, hide_description=True,
)

## Example 5 ###################################################################
define hidden_description = Achievement(
    name=_("Hidden Description"),
    id="hidden_description",
    description=_("This hidden achievement hides only the description."),
    unlocked_image=Transform("gui/window_icon.png", matrixcolor=SepiaMatrix()),
    hide_description=True, ## The important bit that hides only the description
)

## Example 6 ###################################################################
## This achievement unlocks automatically when the other two hidden achievements
## are unlocked. This is set up via myconfig.ACHIEVEMENT_CALLBACK earlier in
## the file.
define hidden_double_unlock = Achievement(
    name=_("You found it"),
    id="hidden3",
    description=_("This achievement unlocks automatically when the other two hidden achievements are unlocked."),
    unlocked_image=Transform("gui/window_icon.png", matrixcolor=ContrastMatrix(0.0)),
    hide_name=True, ## Hide the name
    ## Besides just setting hide_description=True to set it to "???", you can
    ## optionally provide your own custom description here, which is only
    ## shown until the achievement is unlocked (then it shows the regular
    ## description).
    hide_description=_("Try unlocking the other two hidden achievements before this one."),
)

## Example 7 ###################################################################
## This achievement has a hidden name but not a hidden description.
define hidden_name_only = Achievement(
    name=_("Hidden Name"),
    id="hidden_name_only",
    description=_("This achievement hides only the name."),
    unlocked_image=Transform("gui/window_icon.png", matrixcolor=HueMatrix(90)),
    # Use a custom name while the achievement is locked
    hide_name=_("Secret Achievement"),
    hide_description=False, # Don't hide the description
)

## Example 8 ###################################################################
## This -2 makes sure it's declared before the other achievements. This is
## so it shows up first in the list even though it's defined all the way down
## here.
define -2 all_achievements = Achievement(
    name=_("Platinum Achievement"),
    id="platinum_achievement",
    description=_("Congrats! You unlocked every achievement!"),
    unlocked_image=Transform("gui/window_icon.png", matrixcolor=BrightnessMatrix(1.0)),
    hide_description=_("Get all other achievements."),
)

## This is an example of what granting achievements and recording progress
## will look like in-script. You can remove this label if you don't need it.
label achievement_examples():
    ## For this demonstration, we reset all achievements first.
    ## Generally you wouldn't do this in-game except for testing.
    $ Achievement.reset()
    "Here are some examples of granting achievements during the game."
    $ sample_achievement.grant()
    "First up: the sample achievement."
    "Next, a progress achievement. This one needs [progress_achievement.stat_max] steps to complete. You have [progress_achievement.stat_progress] steps completed."
    menu achievement_example_add_progress:
        "You currently have [progress_achievement.stat_progress] steps completed."
        "Add 1 step":
            $ progress_achievement.add_progress(1)
            "Added 1 step. You now have [progress_achievement.stat_progress] steps completed."
            jump achievement_example_add_progress
        "Add 4 steps":
            $ progress_achievement.add_progress(4)
            "Added 4 steps. You now have [progress_achievement.stat_progress] steps completed."
            jump achievement_example_add_progress
        "Set progress to 5":
            $ progress_achievement.progress(5)
            "Set progress to 5. You now have [progress_achievement.stat_progress] steps completed. Note that you can't reverse progress - if your progress is higher than 5, it won't be reduced to 5."
            jump achievement_example_add_progress
        "Reset this achievement's progress":
            $ progress_achievement.clear()
            "Reset progress. You now have [progress_achievement.stat_progress] steps completed."
            jump achievement_example_add_progress
        "Done adding progress":
            pass
    "Note that the progress you add is {i}not{/i} rollback or repeat-safe! If you roll back, you can add more progress. You will also add more progress picking the same option multiple times."
    "We can fix that with the next type of progress progression: using sets."
    "This achievement uses a set to track unique progress towards the achievement."
    "You don't have to do anything special to use it; just set a stat_max and use the add_set_progress method."
    menu achievement_example_set_progress:
        "You currently have [set_progress_achievement.stat_progress] unique steps completed."
        "See the Good End":
            $ set_progress_achievement.add_set_progress("good_end")
            "You saw the good end! You now have [set_progress_achievement.stat_progress] unique steps completed."
            jump achievement_example_set_progress
        "See the Bad End":
            $ set_progress_achievement.add_set_progress("bad_end")
            "You saw the bad end! You now have [set_progress_achievement.stat_progress] unique steps completed."
            jump achievement_example_set_progress
        "See the Neutral End":
            $ set_progress_achievement.add_set_progress("neutral_end")
            "You saw the neutral end! You now have [set_progress_achievement.stat_progress] unique steps completed."
            jump achievement_example_set_progress
        "See the second Bad End":
            $ set_progress_achievement.add_set_progress("bad_end2")
            "You saw the second bad end! You now have [set_progress_achievement.stat_progress] unique steps completed."
            jump achievement_example_set_progress
        "Reset this achievement's progress":
            $ set_progress_achievement.clear()
        "Done adding set progress":
            pass
    "This set progress {i}is{/i} rollback safe. If you roll back or choose the same ending over and over, it will not count towards the achievement's completion multiple times."
    "Note also that there are 4 possible values that can be added to the set, but the achievement only requires 3 of them to be added to unlock."
    "The rest of the achievements are fairly straightforward to achieve."
    menu get_remaining_achievements:
        "Unlock the hidden achievement" if not hidden_achievement.has():
            $ hidden_achievement.grant()
            "You unlocked the hidden achievement!"
            jump get_remaining_achievements
        "Unlock the hidden description achievement" if not hidden_description.has():
            $ hidden_description.grant()
            "You unlocked the hidden description achievement!"
            jump get_remaining_achievements
        "Unlock the hidden name only achievement" if not hidden_name_only.has():
            $ hidden_name_only.grant()
            "You unlocked the hidden name only achievement!"
            jump get_remaining_achievements
        "Start over and reset achievement progress.":
            $ Achievement.reset()
            "All achievements have been reset. You can now start over and earn them again."
            jump achievement_examples
        "I'm done with achievements":
            "I hope this helped you understand how to use achievements in Ren'Py!"
            return
    return
################################################################################
## End of example achievement declarations and in-game examples.
################################################################################

################################################################################
## SCREENS
################################################################################
## POPUP SCREEN
################################################################################
## A screen which shows a popup for an achievement the first time
## it is obtained. You may modify this however you like.
## The relevant information is:
## a.name = the human-readable name of the achievement
## a.description = the description
## a.unlocked_image = the image of the achievement, now that it's unlocked
## a.timestamp = the time the achievement was unlocked at
screen achievement_popup(a, tag, num):

    zorder 190

    ## Allows multiple achievements to be slightly offset from each other.
    ## This number should be at least as tall as one achievement.
    default achievement_yoffset = num*170

    frame:
        style_prefix 'achieve_popup'
        ## The transform that makes it pop out
        at achievement_popout()
        ## Offsets the achievement down if there are multiple
        yoffset achievement_yoffset
        has hbox
        add a.unlocked_image:
            ## Make sure the image is within a certain size. Useful because
            ## often popups are smaller than the full gallery image.
            ## In this case it will not exceed 95 pixels tall but will retain
            ## its dimensions.
            fit "contain" ysize 95 align (0.5, 0.5)
        vbox:
            text a.name
            text a.description size 25

    ## Hide the screen after 5 seconds. You can change the time but shouldn't
    ## change the action.
    timer 5.0 action [Hide("achievement_popup"),
            Show('finish_animating_achievement', num=num, _tag=tag+"1")]

style achieve_popup_frame:
    is confirm_frame
    align (0.0, 0.0)
style achieve_popup_hbox:
    spacing 10
style achieve_popup_vbox:
    spacing 2
style achieve_popup_text:
    is text


## A transform that pops the achievement out from the left side of
## the screen and bounces it slightly into place, then does the
## reverse when the achievement is hidden.
transform achievement_popout():
    ## The `on show` event occurs when the screen is first shown.
    on show:
        ## Align it off-screen at the left. Note that no y information is
        ## given, as that is handled on the popup screen.
        xpos 0.0 xanchor 1.0
        ## Ease it on-screen
        easein_back 1.0 xpos 0.0 xanchor 0.0
    ## The `on hide, replaced` event occurs when the screen is hidden.
    on hide, replaced:
        ## Ease it off-screen again.
        ## This uses the hide time above so it supports displaying multiple
        ## achievements at once.
        easeout_back myconfig.ACHIEVEMENT_HIDE_TIME xpos 0.0 xanchor 1.0

################################################################################
## ACHIEVEMENT GALLERY SCREEN
################################################################################
## The screen displaying a list of the achievements the player has earned.
## Feel free to update the styling for this however you like; this is just one
## way to display the various information.
screen achievement_gallery():
    tag menu
    $ earned = Achievement.num_earned()
    $ total = Achievement.num_total()
    $ remaining = max(total - earned, 0)

    if renpy.loadable("gui/mainmenu_bg.png"):
        add im.Scale("gui/mainmenu_bg.png", config.screen_width, config.screen_height)
    else:
        add Solid("#111a33")

    add Solid("#080d20bb")

    text _("Achievements") style "achv_header":
        xpos 70
        ypos 52

    # Top progress summary.
    hbox:
        xpos 340
        ypos 240
        spacing 8
        text _("Got") style "achv_summary_text"
        text "* [earned]/[total]" style "achv_summary_star_text"
        text _("Achievements!") style "achv_summary_text"
        text "[remaining]" style "achv_summary_remaining_text"
        text _("more to go!") style "achv_summary_text"

    # Achievement cards + scrollbar.
    side "c r":
        xpos 250
        ypos 300
        xysize (1600, 700)

        vpgrid:
            id "achv_grid"
            cols 2
            mousewheel True
            draggable True
            pagekeys True
            xspacing 18
            yspacing 16
            xfill True
            yfill True

            for idx, a in enumerate(Achievement.all_achievements, start=1):
                button:
                    style "achv_card_button"
                    if config.developer:
                        action a.Toggle()
                    else:
                        action NullAction()

                    if a.has():
                        background Frame(Solid("#40105fdd"), 14, 14)
                        hover_background Frame(Solid("#5b1588ee"), 14, 14)
                    else:
                        background Frame(Solid("#272b35dd"), 14, 14)
                        hover_background Frame(Solid("#353b47ee"), 14, 14)

                    fixed:
                        xsize 680
                        ysize 155

                        if a.has():
                            add Solid("#5d0cd2ff") xpos 0 ypos 0 xsize 680 ysize 6
                            add Solid("#5d0cd2ff") xpos 0 ypos 149 xsize 680 ysize 6

                        fixed:
                            xpos 20
                            ypos 20
                            xysize (112, 112)
                            if a.idle_img:
                                add a.idle_img fit "contain" xysize (112, 112)
                            else:
                                text "?" xalign 0.5 yalign 0.5 size 86 color "#f2f2f2"

                        vbox:
                            xpos 150
                            ypos 24
                            spacing 8
                            if a.has():
                                text "#[idx] | [a.name]" style "achv_card_title"
                                text a.description style "achv_card_desc"
                            else:
                                text "#[idx] | ?????" style "achv_card_title"
                                text "-LOCKED ACHIEVEMENT-" style "achv_card_desc_locked"

                            if a.has() and a.timestamp:
                                text a.timestamp style "achv_card_stamp"
                            elif (not a.has()) and a.stat_max and a.show_progress_bar:
                                fixed:
                                    fit_first True
                                    bar value a.stat_progress range a.stat_max style "achv_card_bar"
                                    text "[a.stat_progress]/[a.stat_max]" style "achv_card_bar_text"

        vbar value YScrollValue("achv_grid") style "achv_vscrollbar"

    textbutton _("Close"):
        action Return()
        style "achv_close_button"
        xpos 90
        yalign 0.96

style achv_header is text:
    size 86
    color "#ef3cf3"
    outlines [(3, "#1b1232", 0, 0)]

style achv_summary_text is text:
    size 56
    color "#f1f2f7"
    outlines [(3, "#0c1020", 0, 0)]

style achv_summary_star_text is text:
    size 62
    color "#d6cf09"
    outlines [(3, "#0c1020", 0, 0)]

style achv_summary_remaining_text is text:
    size 60
    color "#ef3cf3"
    outlines [(3, "#0c1020", 0, 0)]

style achv_card_button is button:
    xsize 680
    ysize 155

style achv_card_title is text:
    size 48
    color "#f1f1f2"
    outlines [(2, "#11131a", 0, 0)]

style achv_card_desc is text:
    size 40
    color "#f0eef5"
    outlines [(2, "#11131a", 0, 0)]

style achv_card_desc_locked is text:
    size 40
    color "#c3c5cc"
    outlines [(2, "#11131a", 0, 0)]

style achv_card_stamp is text:
    size 24
    color "#c9cbda"

style achv_card_bar is bar:
    xmaximum 380
    ysize 20
    left_bar "#a83af0"
    right_bar "#4a5468"

style achv_card_bar_text is text:
    size 22
    color "#e9eaf5"
    xalign 1.0
    xpos 392
    ypos -2

style achv_vscrollbar is vscrollbar:
    xsize 18
    base_bar "#3a2462"
    thumb "#9829f1"
    hover_thumb "#bf55ff"

style achv_close_button is button:
    background None

style achv_close_button_text is text:
    size 56
    color "#d0d2dc"
    outlines [(3, "#0c1020", 0, 0)]
    hover_color "#ef3cf3"
