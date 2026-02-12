# preferences_tabs/controls_tab.rpy

screen preferences_tab_controls(pref_remapper, pref_yadj):
    default pref_controls_misc_yadj = ui.adjustment()

    hbox:
        spacing 25

        fixed:
            xsize 520
            ysize 600

            text "REMAPS" style "pref_setting_label":
                xpos 0
                ypos 0

            side "c r":
                xpos 0
                ypos 50
                controller_viewport:
                    xysize (520, 600)
                    mousewheel True
                    draggable True
                    shortcuts True
                    id "pref_controls_viewport"
                    yadjustment pref_yadj
                    has vbox
                    spacing 26

                    hbox:
                        spacing 18
                        use pref_small_button("pref_button_calibrate_gamepad", GamepadCalibrate(), tooltip_key="pref_tip_calibrate_gamepad")
                        use pref_small_button("pref_button_change_icon_set", CycleControllerLayout(), tooltip_key="pref_tip_change_icon_set")

                    for title, act, p in pad_remap.REMAPPABLE_EVENTS:
                        hbox:
                            spacing 16
                            fixed:
                                xsize 230
                                ysize 68
                                text title style "pref_setting_label" xalign 0.0 yalign 0.5
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

        fixed:
            xsize 925
            ysize 580

            text "CONTROLLER" style "pref_setting_label":
                xpos 0
                ypos 0

            side "c r":
                xpos 0
                ypos 50
                viewport:
                    id "pref_controls_misc_viewport"
                    xysize (925, 580)
                    mousewheel True
                    draggable True
                    yadjustment pref_controls_misc_yadj
                    has vbox
                    spacing 14

                    $ ctrl_left_w = 330
                    $ ctrl_right_w = 460
                    $ ctrl_row_h = 72
                    $ ctrl_slider_row_h = 88
                    $ ctrl_slider_block_w = 420

                    hbox:
                        spacing 10
                        fixed:
                            xsize ctrl_left_w
                            ysize ctrl_row_h
                            text "HOLD TO SKIP" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize ctrl_right_w
                            ysize ctrl_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                use pref_tiny_button("ON", SetField(persistent, "hold_to_skip", True), selected=persistent.hold_to_skip, tooltip="Hold button to keep skipping")
                                use pref_tiny_button("OFF", SetField(persistent, "hold_to_skip", False), selected=not persistent.hold_to_skip, tooltip="Tap to toggle skipping")

                    hbox:
                        spacing 10
                        fixed:
                            xsize ctrl_left_w
                            ysize ctrl_row_h
                            text "LEFT STICK X-AXIS" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize ctrl_right_w
                            ysize ctrl_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                use pref_tiny_button("NORMAL", SetStickInversion("left", "x", False), selected=not persistent.left_stick_invert_x, tooltip="Normal left stick x-axis")
                                use pref_tiny_button("INVERTED", SetStickInversion("left", "x", True), selected=persistent.left_stick_invert_x, tooltip="Invert left stick x-axis")

                    hbox:
                        spacing 10
                        fixed:
                            xsize ctrl_left_w
                            ysize ctrl_row_h
                            text "LEFT STICK Y-AXIS" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize ctrl_right_w
                            ysize ctrl_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                use pref_tiny_button("NORMAL", SetStickInversion("left", "y", False), selected=not persistent.left_stick_invert_y, tooltip="Normal left stick y-axis")
                                use pref_tiny_button("INVERTED", SetStickInversion("left", "y", True), selected=persistent.left_stick_invert_y, tooltip="Invert left stick y-axis")

                    hbox:
                        spacing 10
                        fixed:
                            xsize ctrl_left_w
                            ysize ctrl_slider_row_h
                            text "LEFT STICK DEAD ZONE" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize ctrl_right_w
                            ysize ctrl_slider_row_h
                            hbox:
                                xpos (ctrl_right_w - ctrl_slider_block_w)
                                spacing 8
                                fixed:
                                    xsize 54
                                    ysize ctrl_slider_row_h
                                    text "MIN" style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 300
                                    ysize ctrl_slider_row_h
                                    use ui_slider(StickDeadzoneAdjustment("left"), style_name="pref_bar", xsize=300, ysize=82, tooltip="Adjust the left stick dead zone.")
                                fixed:
                                    xsize 50
                                    ysize ctrl_slider_row_h
                                    text "MAX" style "pref_setting_label" xalign 1.0 yalign 0.5

                    hbox:
                        spacing 10
                        fixed:
                            xsize ctrl_left_w
                            ysize ctrl_slider_row_h
                            text "LEFT STICK SENSITIVITY" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize ctrl_right_w
                            ysize ctrl_slider_row_h
                            hbox:
                                xpos (ctrl_right_w - ctrl_slider_block_w)
                                spacing 8
                                fixed:
                                    xsize 54
                                    ysize ctrl_slider_row_h
                                    text "LOW" style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 300
                                    ysize ctrl_slider_row_h
                                    use ui_slider(StickSensitivityAdjustment("left"), style_name="pref_bar", xsize=300, ysize=82, tooltip="Adjust the left stick sensitivity.")
                                fixed:
                                    xsize 50
                                    ysize ctrl_slider_row_h
                                    text "HIGH" style "pref_setting_label" xalign 1.0 yalign 0.5

                    hbox:
                        spacing 10
                        fixed:
                            xsize ctrl_left_w
                            ysize ctrl_row_h
                            text "RIGHT STICK X-AXIS" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize ctrl_right_w
                            ysize ctrl_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                use pref_tiny_button("NORMAL", SetStickInversion("right", "x", False), selected=not persistent.right_stick_invert_x, tooltip="Normal right stick x-axis")
                                use pref_tiny_button("INVERTED", SetStickInversion("right", "x", True), selected=persistent.right_stick_invert_x, tooltip="Invert right stick x-axis")

                    hbox:
                        spacing 10
                        fixed:
                            xsize ctrl_left_w
                            ysize ctrl_row_h
                            text "RIGHT STICK Y-AXIS" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize ctrl_right_w
                            ysize ctrl_row_h
                            hbox:
                                xalign 1.0
                                spacing 8
                                use pref_tiny_button("NORMAL", SetStickInversion("right", "y", False), selected=not persistent.right_stick_invert_y, tooltip="Normal right stick y-axis")
                                use pref_tiny_button("INVERTED", SetStickInversion("right", "y", True), selected=persistent.right_stick_invert_y, tooltip="Invert right stick y-axis")

                    hbox:
                        spacing 10
                        fixed:
                            xsize ctrl_left_w
                            ysize ctrl_slider_row_h
                            text "RIGHT STICK DEAD ZONE" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize ctrl_right_w
                            ysize ctrl_slider_row_h
                            hbox:
                                xpos (ctrl_right_w - ctrl_slider_block_w)
                                spacing 8
                                fixed:
                                    xsize 54
                                    ysize ctrl_slider_row_h
                                    text "MIN" style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 300
                                    ysize ctrl_slider_row_h
                                    use ui_slider(StickDeadzoneAdjustment("right"), style_name="pref_bar", xsize=300, ysize=82, tooltip="Adjust the right stick dead zone.")
                                fixed:
                                    xsize 50
                                    ysize ctrl_slider_row_h
                                    text "MAX" style "pref_setting_label" xalign 1.0 yalign 0.5

                    hbox:
                        spacing 10
                        fixed:
                            xsize ctrl_left_w
                            ysize ctrl_slider_row_h
                            text "RIGHT STICK SENSITIVITY" style "pref_setting_label" yalign 0.5
                        fixed:
                            xsize ctrl_right_w
                            ysize ctrl_slider_row_h
                            hbox:
                                xpos (ctrl_right_w - ctrl_slider_block_w)
                                spacing 8
                                fixed:
                                    xsize 54
                                    ysize ctrl_slider_row_h
                                    text "LOW" style "pref_setting_label" xalign 1.0 yalign 0.5
                                fixed:
                                    xsize 300
                                    ysize ctrl_slider_row_h
                                    use ui_slider(StickSensitivityAdjustment("right"), style_name="pref_bar", xsize=300, ysize=82, tooltip="Adjust the right stick sensitivity.")
                                fixed:
                                    xsize 50
                                    ysize ctrl_slider_row_h
                                    text "HIGH" style "pref_setting_label" xalign 1.0 yalign 0.5

                vbar value YScrollValue("pref_controls_misc_viewport") keyboard_focus False
