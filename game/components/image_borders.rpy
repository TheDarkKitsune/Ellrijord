# Adjacent image.png.meta files supply automatic nine-slice borders.
# Install before game styles, image declarations, and controller icon setup.
init -999 python in ell_image_borders:
    import json
    import unicodedata
    from collections.abc import Mapping

    _original_image = renpy.store.Image
    _original_frame = renpy.store.Frame
    _sides = ("left", "top", "right", "bottom")
    _extensions = (".png", ".jpg", ".jpeg", ".webp", ".avif", ".svg", ".bmp", ".gif", ".tga")

    def _key(filename):
        return unicodedata.normalize("NFC", filename.replace("\\", "/").lstrip("/").lower())

    def parse_metadata(data, filename):
        """Return (left, top, right, bottom), or None for an empty sidecar."""
        def invalid(message):
            raise ValueError("{}: {}".format(filename, message))

        if not isinstance(data, Mapping):
            invalid("expected a JSON object")
        if "border" not in data:
            return None

        border = data["border"]
        if isinstance(border, Mapping):
            unknown = set(border) - set(_sides)
            if unknown:
                invalid("unknown border side(s): {}".format(", ".join(sorted(unknown))))
            values = tuple(border.get(side, 0) for side in _sides)
        else:
            values = (border,) * 4

        for side, value in zip(_sides, values):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                invalid("border {} must be a non-negative integer".format(side))
        return values

    # Read once during init, never from render/prediction. Ren'Py's loader also
    # supports packaged RPA files, Android assets, and Shift+R reloads.
    _metadata = {}
    _files = {_key(name) for name in renpy.list_files()}
    for _filename in sorted(renpy.list_files()):
        if not _filename.lower().endswith(".meta"):
            continue
        _image_filename = _filename[:-5]
        if not _image_filename.lower().endswith(_extensions):
            continue
        try:
            # Use the exact listed path: translated metadata must not replace
            # the base asset's metadata while we are building this index.
            with renpy.loader.load(_filename, tl=False) as _stream:
                _data = json.loads(_stream.read().decode("utf-8-sig"))
            _metadata[_key(_image_filename)] = parse_metadata(_data, _filename)
        except (ValueError, UnicodeError) as _error:
            raise ValueError("Invalid image metadata {}: {}".format(_filename, _error)) from _error

    def get_borders(filename):
        # Match the engine's image search order, including translated assets
        # and the implicit images/ fallback. An image without a sidecar wins
        # over later files that happen to share its name.
        for prefix in renpy.loader.get_prefixes(directory="images"):
            candidate = _key(prefix + filename)
            if candidate in _files:
                return _metadata.get(candidate)
        return None

    class MetadataImage(renpy.display.im.Image):
        """Remain an Image for image_size, prediction, and bitmap operations."""
        def __init__(self, filename, borders, **properties):
            super(MetadataImage, self).__init__(filename, **properties)
            self.borders = borders
            self.identity += (borders,)
            self.const_size = False
            self.raw_image = _original_image(filename, **properties)
            self.border_frame = _original_frame(self.raw_image, *borders)
            self.border_frame.style = self.style

        def render(self, width, height, st, at):
            return renpy.render(self.border_frame, width, height, st, at)

        def visit(self):
            return [self.border_frame]

        def predict_one(self):
            # The visited frame predicts its unmodified source image.
            pass

    def image(arg, loose=False, **properties):
        if isinstance(arg, str):
            borders = get_borders(arg)
            if borders is not None:
                return MetadataImage(arg, borders, **properties)
        return _original_image(arg, loose=loose, **properties)

    class MetadataFrame(_original_frame):
        # Existing Frame(...) calls must not nine-slice a MetadataImage twice.
        # Resolve at render time so [prefix_] hover/selected images work too.
        def render(self, width, height, st, at):
            child = self.style.child or self.image
            if isinstance(child, renpy.display.image.DynamicImage):
                if child.target is None:
                    child.find_target()
            target = child._target()
            if not isinstance(target, MetadataImage):
                return super(MetadataFrame, self).render(width, height, st, at)

            signature = (target, self.style.xminimum, self.style.yminimum)
            if getattr(self, "_metadata_signature", None) != signature:
                self._metadata_signature = signature
                self._metadata_frame = _original_frame(
                    target.raw_image, *target.borders,
                    tile=self.tile, tile_ratio=self.tile_ratio,
                    xminimum=self.style.xminimum, yminimum=self.style.yminimum)
            return renpy.render(self._metadata_frame, width, height, st, at)

    # Filename displayables (including dynamic images) use store.Image.
    # Keep the engine's bitmap loader itself intact for low-level operations.
    renpy.store.Image = image
    renpy.store.Frame = MetadataFrame
