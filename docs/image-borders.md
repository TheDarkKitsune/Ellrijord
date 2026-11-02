# Image borders

Put a JSON sidecar beside an image, keeping its complete filename:

```text
game/gui/panel.png
game/gui/panel.png.meta
```

Use the same border thickness on every side:

```json
{"border": 5}
```

Or specify individual sides. Missing sides are zero:

```json
{
  "border": {
    "left": 5,
    "right": 5,
    "top": 8,
    "bottom": 8
  }
}
```

`{}` (or no sidecar) keeps normal image behavior. `{"border": {}}` and
`{"border": 0}` stretch the entire image with no protected edges. Values must
be non-negative whole numbers; keys require quotes, as in standard JSON.
Invalid metadata stops startup with the filename and a useful error.
Other top-level keys are reserved for future metadata and are ignored.

Borders describe nine-slice regions **inside the existing artwork**, in Ren'Py
logical pixels. They do not draw an outline or add padding. Corners retain
their size, edges stretch along one axis, and the centre stretches along both.
Ren'Py proportionally clamps borders when the source or destination is too
small. Oversampled images use their logical size for border values.

Continue using normal filenames:

```renpy
frame:
    background "gui/panel.png"
    xysize (600, 240)

add "gui/panel.png" xysize (600, 240)

image example_panel = "gui/panel.png"
```

This also works with `Image(...)`, `Transform(..., xsize=..., ysize=...)`,
imagebuttons, interpolated filenames, and automatically registered images.
Images with metadata behave like a `Frame`: they fill the space offered by
their container, so give standalone images a size when needed.
`zoom` scales the finished displayable, including its borders.

For existing `Frame("gui/panel.png", ...)` calls, metadata takes precedence
over the borders in code and prevents double slicing. Existing tiling settings
are retained. Files without a `border` entry keep the explicit Frame behavior.
Low-level bitmap manipulators (`im.*`) operate on the original pixels; apply
metadata to the final image filename you display instead.

Metadata is read once at startup or Shift+R reload, using Ren'Py's asset loader.
Sidecars can be packaged alongside images in RPA archives and Android assets.
Translated assets use their own adjacent metadata; a translated image without
a sidecar renders normally. Commit the `.meta` files along with their images.

Implementation: `game/components/image_borders.rpy` (Ren'Py 8.5.3).

Run the isolated engine checks from the project root:

```powershell
python tools/test_image_borders.py --sdk ../renpy-8.5.3-sdk
```

The checks render generated fixtures and compare pixels, including archived
images and sidecars. They also render the actual settings border at three panel
sizes to check visibility and consistent corner proportions. No project artwork
or saves are changed. To exercise the transparency mask on the GPU, add
`--renderer gl2` (opens a temporary test window).
Ren'Py's [Frame documentation](https://www.renpy.org/doc/html/displayables.html#Frame)
describes the underlying nine-slice behavior.
