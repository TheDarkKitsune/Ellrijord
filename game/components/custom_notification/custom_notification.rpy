init python:
    def pm_notify(message, sound_type="default"):
        sound_map = {
            "default": "components/custom_notification/notification.mp3",
            "error": "components/custom_notification/error.mp3",
            "success": "components/custom_notification/success.mp3",
            "remove": "components/custom_notification/remove.mp3",
        }

        sound_path = sound_map.get(sound_type, sound_map["default"])
        if renpy.loadable(sound_path):
            renpy.sound.play(sound_path)

        renpy.hide_screen("custom_notification")
        renpy.show_screen("custom_notification", message=message, sound_type=sound_type)


screen custom_notification(message, sound_type="default"):
    zorder 250
    $ notification_bg = ("components/custom_notification/images/gui/notification.png" if renpy.loadable("components/custom_notification/images/gui/notification.png") else Solid("#081220ee"))

    frame:
        background notification_bg
        xsize 920
        ysize 92
        xalign 0.5
        ypos 46

        text message:
            xalign 0.5
            yalign 0.5
            size 26
            color "#0b1020"
            text_align 0.5

    timer 2.8 action Hide("custom_notification")
