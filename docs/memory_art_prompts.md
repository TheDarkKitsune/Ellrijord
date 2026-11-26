# Temporary memory-game artwork

Created for the temporary in-game skin using the built-in **imagegen** tool.
These are provisional designs; commissioned artwork can replace the files.
No CLI/API fallback was used.

## Saved assets and sources

- Source atlas: `tools/assets/memory/plush_atlas.png`.
- Runtime illustrations: `game/images/minigames/memory/tsuki_plushies/illustrations/plush_01.png` through `plush_15.png`.
- Card textures: `front.png`, `back.png`, `highlight.png`, `incorrect.png` alongside the illustrations folder.
- UI skin: `game/images/minigames/memory/ui/`.
- Authoring utility: `tools/build_memory_ui_assets.py`.

The atlas supplies fourteen temporary plush illustrations. The first runtime
card fits a copy of `game/secrets/plushies/kittycat_plush.png` to the same
400 × 560 transparent canvas. Original artwork is never overwritten.
The Tsuki panel references the existing
`game/gui/inventory_system/collectibles/tsuki_plushies.png` directly.

The authoring utility performs mechanical atlas extraction/canvas fitting and
draws the simple UI geometry. All runtime card layers, including highlights,
use 400 × 560 RGBA PNG canvases. The background, panel frames and buttons use
their own independent replaceable textures.

## Exact imagegen prompt

Use case: stylized-concept. Asset type: ONE production-ready game sprite atlas, a 4 by 4 grid of 16 distinct adorable stuffed-animal plush illustrations, each isolated on genuine transparent background. Square 2048 x 2048 canvas, exact equal 512 x 512 cells, NO visible grid or cell borders. Each animal centered within its cell with generous 65px clear transparent padding on all four sides; no illustration crosses its cell. Order left to right, top to bottom: orange fox, lavender bunny, honey teddy bear, black and white panda; russet red panda, grey raccoon, blue penguin, lavender owl; small fawn with antlers, yellow duck, cream shiba puppy, mint baby dragon; white lamb, grey koala, brown otter, golden hamster. All are sitting full-body plush toys with big embroidered eyes, small smiles, soft pink cheeks, tiny visible seams, round stuffed limbs, soft velvety watercolor texture, polished warm 2D storybook/anime game inventory illustration. Keep each silhouette and colour distinct at small card size. Consistent soft studio light, cream highlights, gentle dark-plum contours, pastel lavender accents #A58AC5, soft pink #E7A9BC, warm gold #E4C575. These are temporary cute collectible plush designs for a visual novel memory card game. No characters, no hands, no scenery, no text, no labels, no numbers, no cards, no frames, no watermark, no drop shadow connecting cells. Transparent alpha everywhere outside the individual plush toys.
