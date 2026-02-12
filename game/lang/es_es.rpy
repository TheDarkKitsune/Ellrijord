# lang/es_es.rpy
# Spanish (ES) UI strings.

init -1 python:
    register_ui_lang("es_es", {
        "lang_name": "Español (ES)",

        # Tabs.
        "pref_tab_display": "PANTALLA",
        "pref_tab_audio": "AUDIO",
        "pref_tab_controls": "CONTROLES",
        "pref_tab_access": "ACCESO",
        "pref_tip_tab_display": "Modo de pantalla, reglas de salto y ajustes de velocidad.",
        "pref_tip_tab_audio": "Silenciar y ajustar niveles de audio.",
        "pref_tip_tab_controls": "Calibración del mando y asignación de botones.",
        "pref_tip_tab_access": "Configuración de salto y transiciones.",

        # Audio.
        "pref_label_mute_all": "SILENCIAR TODO",
        "pref_button_muted": "SILENCIADO",
        "pref_button_not_muted": "NO SILENCIADO",
        "pref_tip_muted": "Silenciar música, efectos y voz.",
        "pref_tip_not_muted": "Activar todos los canales de audio.",
        "pref_label_music_volume": "VOLUMEN MÚSICA",
        "pref_label_sfx_volume": "VOLUMEN SFX",
        "pref_label_voice_volume": "VOLUMEN VOZ",
        "pref_tip_music_volume": "Ajusta el volumen de la música.",
        "pref_tip_sfx_volume": "Ajusta el volumen de los efectos de sonido.",
        "pref_tip_voice_volume": "Ajusta el volumen de la voz.",

        # Display.
        "pref_label_display": "PANTALLA",
        "pref_button_window": "VENTANA",
        "pref_button_fullscreen": "PANTALLA COMPLETA",
        "pref_tip_window": "Ejecutar en modo ventana.",
        "pref_tip_fullscreen": "Usar pantalla completa.",
        "pref_label_skip_unseen": "SALTAR TEXTO NO VISTO",
        "pref_tip_skip_unseen_on": "Permite saltar texto no leído.",
        "pref_tip_skip_unseen_off": "Solo saltar texto ya visto.",
        "pref_label_skip_after_choices": "SALTAR TRAS ELECCIONES",
        "pref_tip_skip_after_choices_on": "Seguir saltando tras elecciones.",
        "pref_tip_skip_after_choices_off": "Detener el salto en elecciones.",
        "pref_label_text_speed": "VELOCIDAD DE TEXTO",
        "pref_label_min": "MÍN",
        "pref_label_max": "MÁX",
        "pref_label_auto_forward": "RETARDO DE AUTOAVANCE",
        "pref_tip_text_speed": "Cambia la velocidad de aparición del texto.",
        "pref_tip_auto_forward": "Cambia el retardo de autoavance.",

        # Access.
        "pref_label_skip_mode": "MODO SALTO",
        "pref_label_seen": "VISTO",
        "pref_label_all": "TODO",
        "pref_label_skip_transitions": "SALTAR TRANSICIONES",
        "pref_tip_transitions_on": "Saltar transiciones de pantalla.",
        "pref_tip_transitions_off": "Reproducir transiciones de pantalla.",
        "pref_tip_font_size": "Escala el tamaño del texto del menú y diálogo.",
        "pref_tip_line_spacing": "Ajusta el espacio entre líneas de texto.",
        "pref_tip_self_voicing_volume": "Reduce el volumen del juego al usar autovoz.",

        # Controls.
        "pref_button_calibrate_gamepad": "CALIBRAR BOTONES DEL MANDO",
        "pref_tip_calibrate_gamepad": "Iniciar la calibración del mando.",
        "pref_button_change_icon_set": "CAMBIAR ICONOS",
        "pref_tip_change_icon_set": "Cambiar el diseño de los iconos del mando.",
        "pref_button_add_binding": "+",
        "pref_tip_add_binding": "Añadir una nueva asignación.",
        "pref_tip_remove_binding": "Eliminar esta asignación.",

        # Footer.
        "pref_button_main_menu": "MENÚ PRINCIPAL",
        "pref_tip_main_menu": "Volver al menú principal.",
        "pref_button_back": "VOLVER",
        "pref_tip_back": "Volver a la pantalla anterior.",
        "pref_button_default": "PREDETERMINADO",
        "pref_tip_default": "Restablecer ajustes.",

        # Shared toggles.
        "pref_button_on": "ACTIVADO",
        "pref_button_off": "DESACTIVADO",
        "pref_tip_generic_on": "Habilitar esta opción.",
        "pref_tip_generic_off": "Deshabilitar esta opción.",
    })
