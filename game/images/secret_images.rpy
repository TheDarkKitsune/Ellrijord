# secret_images.rpy
# Secret gallery preview resolver.

init -2 python:
    def gallery_secret_images_preview(default_path):
        candidates = [
            "gui/extra/secret_images.png",
            "gui/extra/secret_images.jpg",
            "gui/extra/secret_images.webp",
        ]
        for p in candidates:
            if renpy.loadable(p):
                return p
        return default_path

