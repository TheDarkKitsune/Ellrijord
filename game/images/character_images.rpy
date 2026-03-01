# character_images.rpy
# Character gallery preview resolver.

init -2 python:
    def gallery_character_images_preview(default_path):
        candidates = [
            "gui/extra/character_images.png",
            "gui/extra/character_images.jpg",
            "gui/extra/character_images.webp",
        ]
        for p in candidates:
            if renpy.loadable(p):
                return p
        return default_path

