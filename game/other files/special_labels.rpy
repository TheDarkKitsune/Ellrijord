## Special Labels ##############################################################
##
## These are special labels that Ren'Py automatically recognizes if they
## are included with the game. Read more here:
## https://www.renpy.org/doc/html/label.html#special-labels
##

## Splash Screen ###############################################################
##
## Put the splash screen code here. It runs when the game is launched.
##
screen press_any_button():
    add "#292835"
    label _("Press any button") at gentle_flash style 'press_any'
    ## This a special version of the EventListener class which will
    ## end the interaction when a button is pressed.
    add pad_config.PRESS_ANYTHING

style press_any:
    is gui_label
    xcenter 0.5 ycenter 0.8
    xfill True
    background "#0005"
    ypadding 25
style press_any_text:
    is gui_label_text
    xalign 0.5 text_align 0.5 yalign 0.5

## A transform which becomes semi-transparent and opaque in a loop.
transform gentle_flash:
    alpha 1.0
    pause 1.0
    ease 2.0 alpha 0.3
    ease 2.0 alpha 1.0
    pause 1.0
    repeat

label splashscreen():
    ## With controller support, it's good to have a "press any button" screens
    ## to start, so we know the player is using a controller.
    ## This lets Ren'Py set up default_focus as well.
    call screen press_any_button
    return

## After Load ##################################################################
##
## Adjust any variables etc in the after_load label
## Also consider: define config.after_load_callbacks = [ ... ]
##
label after_load():
    return

## Before Main Menu ############################################################
##
## This label is called before the main menu is displayed when the game is
## started up or the game is restarted.
## Here, it is used to ensure the previous focus while on the main menu is
## reset.
##
label before_main_menu():
    $ pad_config.clear_managed_focus("main_menu")
    return