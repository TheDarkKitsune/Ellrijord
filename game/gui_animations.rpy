# gui_animations.rpy
# Falling petals/leaves + optional gentle drift.
# Put your petal image at: gui/petal.png

init -2:

    # Reusable transform for a single falling petal.
    # xstart: 0.0 to 1.0 (screen fraction)
    # t: fall duration (seconds)
    # s: zoom (size)
    # r: rotation amount (degrees)
    # drift: how far to drift sideways during the fall (screen fraction)
    # delay: start delay (seconds)
    transform petal_fall(xstart=0.5, t=12.0, s=0.06, r=220, drift=0.06, delay=0.0):

        # Start above screen.
        xalign xstart
        yalign -0.15
        zoom s
        rotate 0

        # Optional stagger.
        pause delay

        parallel:
            # Fall top -> bottom.
            linear t yalign 1.15

        parallel:
            # Side drift.
            linear t xalign (xstart + drift)

        parallel:
            # Slow rotation while falling.
            linear t rotate r

        repeat
