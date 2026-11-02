"""Exercise image metadata in a temporary project using the real Ren'Py engine.

Run: python tools/test_image_borders.py --sdk ../renpy-8.5.3-sdk
No assets, saves, or generated scripts are written into the game project.
"""

import argparse
import json
import os
from pathlib import Path
import pickle
import shutil
import struct
import subprocess
import tempfile
import zlib


def png_bytes():
    # A 12px square with distinct 2px corners/edges and a grey centre.
    colors = (
        ((255, 0, 0), (255, 0, 255), (0, 255, 0)),
        ((255, 128, 0), (128, 128, 128), (0, 255, 255)),
        ((0, 0, 255), (128, 0, 255), (255, 255, 0)),
    )
    pixels = bytearray()
    for y in range(12):
        pixels.append(0)
        for x in range(12):
            pixels.extend(colors[0 if y < 2 else 2 if y >= 10 else 1]
                                [0 if x < 2 else 2 if x >= 10 else 1])

    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data)))

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 12, 12, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(pixels)) + chunk(b"IEND", b""))


def write_archive(path, files):
    """Minimal RPA-3 fixture using the SDK archiver's index format."""
    key = 0x42424242
    index = {}
    with path.open("wb") as stream:
        stream.write(b"RPA-3.0 XXXXXXXXXXXXXXXX XXXXXXXX\n")
        for filename, contents in files.items():
            offset = stream.tell()
            stream.write(contents)
            index[filename] = [(offset ^ key, len(contents) ^ key, b"")]
        index_offset = stream.tell()
        stream.write(zlib.compress(pickle.dumps(index, protocol=2)))
        stream.seek(0)
        stream.write(b"RPA-3.0 %016x %08x\n" % (index_offset, key))


HARNESS = r'''
define config.screen_width = 320
define config.screen_height = 240
define config.save_directory = None
define config.sound = False
define config.developer = True
define config.window = "hide"

default border_test_variant = "uniform"
image declared_border = "gui/uniform.png"

screen border_test_screen():
    frame:
        xysize (60, 36)
        padding (0, 0)
        background "gui/uniform.png"
    add "gui/uniform.png" xpos 70 xysize (60, 36)
    imagebutton:
        xpos 140
        xysize (60, 36)
        auto "gui/%s.png"
        action NullAction()

init python:
    def run_border_tests():
        import json
        import pickle
        import os
        import pygame_sdl2 as pygame
        from store import ell_image_borders as borders

        passed = []

        def check(name, condition):
            if not condition:
                raise AssertionError(name)
            passed.append(name)

        def surface(d, width=60, height=36):
            # SWDraw.screenshot returns the window, ignoring its render arg.
            # Read the actual offscreen Render texture for pixel assertions.
            if renpy.display.draw.info["renderer"] == "sw":
                return renpy.render(d, width, height, 0, 0).render_to_texture(True)
            return renpy.render_to_surface(d, width=width, height=height, resize=True)

        def same_pixels(a, b):
            return a.get_size() == b.get_size() and all(
                a.get_at((x, y)) == b.get_at((x, y))
                for y in range(a.get_height()) for x in range(a.get_width()))

        def compare(name, displayable, values=(2, 2, 2, 2), width=60, height=36):
            actual = surface(displayable, width, height)
            expected = surface(borders._original_frame(borders._original_image("gui/uniform.png"), *values), width, height)
            check(name, same_pixels(actual, expected))
            return actual

        check("uniform metadata", borders.get_borders("gui/uniform.png") == (2, 2, 2, 2))
        check("partial sides default to zero", borders.get_borders("gui/partial.png") == (2, 0, 3, 0))
        check("asymmetric metadata", borders.get_borders("gui/asymmetric.png") == (2, 1, 3, 4))
        check("empty object is unchanged", not isinstance(Image("gui/empty.png"), borders.MetadataImage))
        check("absent sidecar is unchanged", not isinstance(Image("gui/plain.png"), borders.MetadataImage))
        check("zero is an active frame", isinstance(Image("gui/zero.png"), borders.MetadataImage))
        check("images directory fallback", borders.get_borders("fallback.png") == (2, 2, 2, 2))
        check("first image without metadata wins", borders.get_borders("plain.png") is None)
        check("case insensitive paths", borders.get_borders("GUI/UNIFORM.PNG") == (2, 2, 2, 2))
        check("archived metadata is indexed", borders.get_borders("gui/archived.png") == (2, 2, 2, 2))
        check("image_size stays compatible", renpy.image_size("gui/uniform.png") == (12, 12))
        check("Image idempotence", Image(Image("gui/uniform.png")).borders == (2, 2, 2, 2))

        invalid = [[], {"border": -1}, {"border": True}, {"border": 1.5},
                   {"border": "5"}, {"border": None}, {"border": {"left": -1}},
                   {"border": {"left": False}}, {"border": {"lef": 2}}]
        for index, data in enumerate(invalid):
            try:
                borders.parse_metadata(data, "bad.png.meta")
            except ValueError as error:
                check("invalid metadata {} identifies filename".format(index), "bad.png.meta" in str(error))
            else:
                raise AssertionError("Accepted invalid metadata: {!r}".format(data))

        actual = compare("filename automatically slices", renpy.displayable("gui/uniform.png"))
        pygame.image.save(actual, os.path.join(config.basedir, "border-render.png"))
        check("protected corner and stretched regions", all(
            abs(channel - expected) <= 2
            for point, color in (((1, 1), (255, 0, 0)), ((6, 0), (255, 0, 255)), ((6, 6), (128, 128, 128)))
            for channel, expected in zip(tuple(actual.get_at(point))[:3], color)))
        compare("partial border renders", Image("gui/partial.png"), (2, 0, 3, 0))
        compare("asymmetric border renders", Image("gui/asymmetric.png"), (2, 1, 3, 4))
        compare("zero border stretches", Image("gui/zero.png"), (0, 0, 0, 0))
        compare("Transform xysize preserves borders", Transform("gui/uniform.png", xsize=60, ysize=36))
        compare("explicit Frame uses metadata once", Frame("gui/uniform.png", 5, 5))
        compare("explicit Image inside Frame", Frame(Image("gui/uniform.png"), 5, 5))
        compare("explicit Frame without metadata unchanged", Frame("gui/plain.png", 1, 1), (1, 1, 1, 1))
        compare("empty sidecar preserves explicit Frame", Frame("gui/empty.png", 1, 1), (1, 1, 1, 1))
        compare("declared image", renpy.displayable("declared_border"))
        compare("automatically registered image", renpy.displayable("fallback"))
        compare("archived image and metadata render", Image("gui/archived.png"))
        compare("archived automatically registered image", renpy.displayable("archived_auto"))
        compare("dynamic filename", renpy.displayable("gui/[border_test_variant].png"))
        compare("dynamic filename inside Frame", Frame("gui/[border_test_variant].png", 5, 5))
        prefix_frame = Frame("gui/[prefix_]panel.png", 5, 5)
        prefix_frame.set_style_prefix("hover_", True)
        compare("hover prefix inside Frame", prefix_frame, (2, 1, 3, 4))
        compare("tiny destination clamps borders", Image("gui/uniform.png"), width=3, height=3)
        compare("pickled image", pickle.loads(pickle.dumps(Image("gui/uniform.png"))))
        compare("pickled frame", pickle.loads(pickle.dumps(Frame("gui/uniform.png", 5, 5))))
        tiled = surface(Frame("gui/uniform.png", 5, 5, tile=True))
        expected_tiled = surface(borders._original_frame(borders._original_image("gui/uniform.png"), 2, 2, tile=True))
        check("Frame tile option preserved", same_pixels(tiled, expected_tiled))

        previous_language = renpy.game.preferences.language
        renpy.game.preferences.language = "test"
        check("translated metadata", borders.get_borders("gui/uniform.png") == (1, 1, 1, 1))
        check("translated image without sidecar", borders.get_borders("gui/plain.png") is None)
        renpy.game.preferences.language = previous_language

        previous_load = renpy.loader.load
        def reject_load(*args, **kwargs):
            raise AssertionError("Unexpected filesystem access after init")
        try:
            renpy.loader.load = reject_load
            for unused in range(20):
                Image("gui/uniform.png")
                Image("gui/plain.png")
            check("no metadata IO after init", True)
        finally:
            renpy.loader.load = previous_load

        # Exercise the actual settings helper, assets, mask, and sidecar. A
        # synthetic Frame alone does not catch fractional-position regressions.
        settings_renders = []
        for width, height in ((694, 190), (734, 258), (280, 760)):
            panel = Fixed(pref_border_frame(width, height), xsize=width, ysize=height, clipping=True)
            rendered = surface(panel, width, height)
            pygame.image.save(rendered, os.path.join(config.basedir, "settings-border-{}x{}.png".format(width, height)))
            check("settings border size {}x{}".format(width, height), rendered.get_size() == (width, height))
            for name, start_x, start_y in (("top left", 0, 0), ("top right", width - 36, 0),
                                          ("bottom left", 0, height - 36), ("bottom right", width - 36, height - 36)):
                visible = 0
                for y in range(start_y, start_y + 36):
                    for x in range(start_x, start_x + 36):
                        red, green, blue, alpha = rendered.get_at((x, y))
                        if alpha > 20 and red > 60 and green > 30:
                            visible += 1
                check("settings {} corner visible {}x{}".format(name, width, height), visible > 15)
            settings_renders.append(rendered)
        reference = settings_renders[0]
        for index, rendered in enumerate(settings_renders[1:], 1):
            check("settings corner proportions remain fixed {}".format(index), all(
                abs(a - b) <= 2
                for y in range(24) for x in range(24)
                for a, b in zip(reference.get_at((x, y)), rendered.get_at((x, y)))))

        pygame.image.save(actual, os.path.join(config.basedir, "border-render.png"))
        with open(os.path.join(config.basedir, "results.json"), "w") as stream:
            json.dump({"passed": passed}, stream)

label start:
    show screen border_test_screen
    $ renpy.pause(0.05)
    python:
        try:
            run_border_tests()
        except Exception:
            import traceback
            traceback.print_exc()
            renpy.quit(status=1, save=False)
    $ renpy.quit(status=0, save=False)
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="Keep test project and render for inspection")
    parser.add_argument("--renderer", choices=("sw", "gl2"), default="sw",
                        help="Use gl2 to verify masking and output on the real GPU")
    args = parser.parse_args()
    sdk = args.sdk.resolve()
    python = sdk / "lib" / "py3-windows-x86_64" / "python.exe"
    if not python.exists():
        parser.error("SDK's bundled Windows Python was not found")

    with tempfile.TemporaryDirectory(prefix="ell-image-borders-") as temp:
        project = Path(temp)
        game = project / "game"
        game.mkdir()
        root = Path(__file__).resolve().parents[1]
        shutil.copy2(root / "game/components/image_borders.rpy", game)
        preferences = (root / "game/custom_menus/custom_preferences.rpy").read_text(encoding="utf-8")
        helper_start = preferences.index("    def pref_border_frame(")
        helper_end = preferences.index("\n    def ", helper_start + 1)
        settings_helper = "\ninit python:\n    _pref_border_frame_cache = {}\n" + preferences[helper_start:helper_end]
        (game / "script.rpy").write_text(HARNESS + settings_helper, encoding="utf-8")
        fixtures = {
            "gui/uniform.png": {"border": 2},
            "gui/partial.png": {"border": {"left": 2, "right": 3}},
            "gui/asymmetric.png": {"border": {"left": 2, "top": 1, "right": 3, "bottom": 4}},
            "gui/empty.png": {}, "gui/plain.png": None,
            "gui/zero.png": {"border": 0},
            "images/fallback.png": {"border": 2},
            "images/plain.png": {"border": 2}, "plain.png": None,
            "gui/idle_panel.png": {"border": 2},
            "gui/hover_panel.png": {"border": {"left": 2, "top": 1, "right": 3, "bottom": 4}},
            "gui/idle.png": {"border": 2}, "gui/hover.png": {"border": 2},
            "tl/test/gui/uniform.png": {"border": 1}, "tl/test/gui/plain.png": None,
        }
        for filename, metadata in fixtures.items():
            image = game / filename
            image.parent.mkdir(parents=True, exist_ok=True)
            image.write_bytes(png_bytes())
            if metadata is not None:
                image.with_suffix(image.suffix + ".meta").write_text(json.dumps(metadata), encoding="utf-8")

        for filename in ("border.png", "border_mask.png", "border.png.meta"):
            shutil.copy2(root / "game/gui" / filename, game / "gui" / filename)

        write_archive(game / "border-fixtures.rpa", {
            "gui/archived.png": png_bytes(),
            "gui/archived.png.meta": b'{"border": 2}',
            "images/archived_auto.png": png_bytes(),
            "images/archived_auto.png.meta": b'{"border": 2}',
        })

        env = dict(os.environ, SDL_VIDEODRIVER="dummy" if args.renderer == "sw" else "windows",
                   SDL_AUDIODRIVER="dummy", RENPY_RENDERER=args.renderer, RENPY_DISABLE_SOUND="1")
        try:
            completed = subprocess.run([str(python), str(sdk / "renpy.py"), str(project), "run"],
                                       env=env, capture_output=True, text=True, timeout=45)
            results = project / "results.json"
            if completed.returncode or not results.exists():
                print(completed.stdout)
                print(completed.stderr)
                for name in ("errors.txt", "traceback.txt", "log.txt"):
                    if (project / name).exists():
                        print((project / name).read_text(encoding="utf-8-sig"))
                raise SystemExit("Ren'Py border integration tests failed")
            checks = json.loads(results.read_text())["passed"]
            print("Passed {} real-engine checks".format(len(checks)))
            for check in checks:
                print("  " + check)
        finally:
            if args.output:
                shutil.copytree(project, args.output, dirs_exist_ok=True)


if __name__ == "__main__":
    main()
