# gui_animations.rpy
# Safe ATL transforms used by the custom main menu.

init -2:

    # Falling petal animation.
    # Works in a 1920x1080 logical screen.
    transform petal_fall(xstart=0.5, t=12.0, s=0.08, r=360, drift=0.10, delay=0.0):
        xpos int(1920 * xstart)
        ypos -200
        zoom s
        rotate 0
        alpha 0.9

        pause delay

        parallel:
            linear t ypos 1200

        parallel:
            linear t xpos int(1920 * (xstart + drift))

        parallel:
            linear t rotate r

        repeat
