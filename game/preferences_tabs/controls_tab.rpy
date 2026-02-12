# preferences_tabs/controls_tab.rpy

screen preferences_tab_controls(pref_remapper, pref_yadj):
    vbox:
        spacing 14

        hbox:
            spacing 18
            use pref_small_button("pref_button_calibrate_gamepad", GamepadCalibrate(), tooltip_key="pref_tip_calibrate_gamepad")
            use pref_small_button("pref_button_change_icon_set", CycleControllerLayout(), tooltip_key="pref_tip_change_icon_set")

        side "c r":
            controller_viewport:
                xysize (1440, 520)
                mousewheel True
                draggable True
                shortcuts True
                id "pref_controls_viewport"
                yadjustment pref_yadj
                has vbox
                spacing 26

                fixed:
                    xsize 1360
                    ysize 70
                    text "HOLD TO SKIP" style "pref_label":
                        xpos 0
                        ypos 8
                    fixed:
                        xpos 560
                        ypos 0
                        use pref_tiny_button("ON", SetField(persistent, "hold_to_skip", True), selected=persistent.hold_to_skip, tooltip="Hold button to keep skipping")
                    fixed:
                        xpos 770
                        ypos 0
                        use pref_tiny_button("OFF", SetField(persistent, "hold_to_skip", False), selected=not persistent.hold_to_skip, tooltip="Tap to toggle skipping")

                fixed:
                    xsize 1360
                    ysize 70
                    text "LEFT STICK X-AXIS" style "pref_label":
                        xpos 0
                        ypos 8
                    fixed:
                        xpos 560
                        ypos 0
                        use pref_tiny_button("NORMAL", SetStickInversion("left", "x", False), selected=not persistent.left_stick_invert_x, tooltip="Normal left stick x-axis")
                    fixed:
                        xpos 770
                        ypos 0
                        use pref_tiny_button("INVERTED", SetStickInversion("left", "x", True), selected=persistent.left_stick_invert_x, tooltip="Invert left stick x-axis")

                fixed:
                    xsize 1360
                    ysize 70
                    text "LEFT STICK Y-AXIS" style "pref_label":
                        xpos 0
                        ypos 8
                    fixed:
                        xpos 560
                        ypos 0
                        use pref_tiny_button("NORMAL", SetStickInversion("left", "y", False), selected=not persistent.left_stick_invert_y, tooltip="Normal left stick y-axis")
                    fixed:
                        xpos 770
                        ypos 0
                        use pref_tiny_button("INVERTED", SetStickInversion("left", "y", True), selected=persistent.left_stick_invert_y, tooltip="Invert left stick y-axis")

                fixed:
                    xsize 1360
                    ysize 82
                    text "LEFT STICK DEAD ZONE" style "pref_label":
                        xpos 0
                        ypos 12
                    text "MIN" style "pref_label":
                        xpos 560
                        ypos 12
                    bar value StickDeadzoneAdjustment("left") style "pref_bar":
                        xpos 640
                        ypos 0
                    text "MAX" style "pref_label":
                        xpos 1210
                        ypos 12

                fixed:
                    xsize 1360
                    ysize 82
                    text "LEFT STICK SENSITIVITY" style "pref_label":
                        xpos 0
                        ypos 12
                    text "LOW" style "pref_label":
                        xpos 560
                        ypos 12
                    bar value StickSensitivityAdjustment("left") style "pref_bar":
                        xpos 640
                        ypos 0
                    text "HIGH" style "pref_label":
                        xpos 1210
                        ypos 12

                fixed:
                    xsize 1360
                    ysize 70
                    text "RIGHT STICK X-AXIS" style "pref_label":
                        xpos 0
                        ypos 8
                    fixed:
                        xpos 560
                        ypos 0
                        use pref_tiny_button("NORMAL", SetStickInversion("right", "x", False), selected=not persistent.right_stick_invert_x, tooltip="Normal right stick x-axis")
                    fixed:
                        xpos 770
                        ypos 0
                        use pref_tiny_button("INVERTED", SetStickInversion("right", "x", True), selected=persistent.right_stick_invert_x, tooltip="Invert right stick x-axis")

                fixed:
                    xsize 1360
                    ysize 70
                    text "RIGHT STICK Y-AXIS" style "pref_label":
                        xpos 0
                        ypos 8
                    fixed:
                        xpos 560
                        ypos 0
                        use pref_tiny_button("NORMAL", SetStickInversion("right", "y", False), selected=not persistent.right_stick_invert_y, tooltip="Normal right stick y-axis")
                    fixed:
                        xpos 770
                        ypos 0
                        use pref_tiny_button("INVERTED", SetStickInversion("right", "y", True), selected=persistent.right_stick_invert_y, tooltip="Invert right stick y-axis")

                fixed:
                    xsize 1360
                    ysize 82
                    text "RIGHT STICK DEAD ZONE" style "pref_label":
                        xpos 0
                        ypos 12
                    text "MIN" style "pref_label":
                        xpos 560
                        ypos 12
                    bar value StickDeadzoneAdjustment("right") style "pref_bar":
                        xpos 640
                        ypos 0
                    text "MAX" style "pref_label":
                        xpos 1210
                        ypos 12

                fixed:
                    xsize 1360
                    ysize 82
                    text "RIGHT STICK SENSITIVITY" style "pref_label":
                        xpos 0
                        ypos 12
                    text "LOW" style "pref_label":
                        xpos 560
                        ypos 12
                    bar value StickSensitivityAdjustment("right") style "pref_bar":
                        xpos 640
                        ypos 0
                    text "HIGH" style "pref_label":
                        xpos 1210
                        ypos 12

                null height 12

                for title, act, p in pad_remap.REMAPPABLE_EVENTS:
                    hbox:
                        spacing 16
                        fixed:
                            xsize 230
                            ysize 68
                            text title style "pref_label" xalign 0.0 yalign 0.5
                        $ pad_images = pad_remap.get_images(act, pref_remapper.get_current_bindings())
                        grid 3 1:
                            spacing 12
                            for i, img in enumerate(pad_images):
                                use pref_icon_button(
                                    img[0],
                                    [Function(pref_remapper.remove_button, img[1], act),
                                        If((act not in pad_remap.REQUIRED_EVENTS
                                                or len(pad_images) > 1), None,
                                            Function(renpy.call_in_new_context,
                                                "listen_for_remap", title, act, pref_yadj,
                                                pref_remapper))],
                                    tooltip_key="pref_tip_remove_binding"
                                )
                            for i in range(3 - len(pad_images)):
                                use pref_add_binding_button(
                                    Function(renpy.call_in_new_context,
                                        "listen_for_remap", title, act, pref_yadj,
                                        pref_remapper),
                                    tooltip_key="pref_tip_add_binding"
                                )
            vbar value YScrollValue("pref_controls_viewport") keyboard_focus False
