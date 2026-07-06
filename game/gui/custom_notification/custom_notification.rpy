init python:
    def pm_notify(message, sound_type="default"):
        sound_map = {
            "default": "gui/custom_notification/notification.mp3",
            "error": "gui/custom_notification/error.mp3",
            "success": "gui/custom_notification/success.mp3",
            "remove": "gui/custom_notification/remove.mp3",
        }

        sound_path = sound_map.get(sound_type, sound_map["default"])
        if renpy.loadable(sound_path):
            renpy.sound.play(sound_path)

        renpy.hide_screen("custom_notification")
        renpy.notify(message)


screen custom_notification(message, sound_type="default"):
    zorder 250
    $ notification_path = "gui/custom_notification/images/gui/Notification.png"
    $ has_notification_art = renpy.loadable(notification_path)

    if has_notification_art:
        $ bar_width = 760
        $ bar_height = 110

        fixed:
            xsize bar_width
            ysize bar_height
            xalign 0.5
            ypos 46

            add Transform(
                notification_path,
                crop=(0, 75, 481, 70),
                fit="contain",
                xsize=bar_width,
                ysize=bar_height,
            )

            text message:
                xpos 190
                xsize 450
                yalign 0.5
                size 26
                color "#2d2432"
                text_align 0.5
    else:
        frame:
            background Solid("#f6eddc")
            xsize 760
            ysize 92
            xalign 0.5
            ypos 46

            text message:
                xalign 0.5
                yalign 0.5
                size 26
                color "#2d2432"
                text_align 0.5

    timer 2.8 action Hide("custom_notification")
