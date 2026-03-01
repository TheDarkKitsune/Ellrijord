# gameplay_images.rpy
# Gameplay gallery preview resolver.

init -2 python:
    def gallery_gameplay_images_preview(default_path):
        candidates = [
            "gui/extra/gameplay_images.png",
            "gui/extra/gameplay_images.jpg",
            "gui/extra/gameplay_images.webp",
        ]
        for p in candidates:
            if renpy.loadable(p):
                return p
        return default_path

