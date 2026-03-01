# extra_images.rpy
# Extra gallery preview resolver.

init -2 python:
    def gallery_extra_images_preview(default_path):
        candidates = [
            "gui/extra/extra_images.png",
            "gui/extra/extra_images.jpg",
            "gui/extra/extra_images.webp",
        ]
        for p in candidates:
            if renpy.loadable(p):
                return p
        return default_path

