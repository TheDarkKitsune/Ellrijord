# Minigames

From Day 2, finish or skip Mini Tsuki's exploration tutorial, then open the
bedroom PC and choose **Minigames → Tsuki's Memory Challenge**. The menu also
allows replay. Leaving a board returns to the minigame menu; Back restores the
PC and its previous tab. Shutting down the PC returns to the same room.
Playing currently consumes no world time.

## Implemented scope

Classic matching with a polished temporary 15-card plushie deck:

| Difficulty | Board | Pairs | Availability |
| --- | --- | --- | --- |
| Easy | 4 × 3 | 6 | Playable |
| Normal | 4 × 4 | 8 | Playable |
| Hard | 6 × 4 | 12 | Playable |
| Expert | 6 × 6 | 18 | Disabled until the deck has enough unique cards |
| Tsuki's Challenge | 8 × 6 | 24 | Disabled until the deck has enough unique cards |

One move means turning over two cards. Mismatches remain visible for 0.85 seconds
and block further flips until hidden. Matched cards remain face up. Time Attack,
Limited Moves, Against Tsuki and Chaos Mode are not implemented or selectable.
The larger board dimensions are configured; they still need artwork and playtesting.

## Code and integration

- `game/minigames/minigame_core.rpy`: activity registry, Day 2 availability,
  replay menu and result format.
- `game/minigames/minigame_ui.rpy`: shared rounded panels, textured buttons,
  icons, fonts and skin paths, independent of memory-game rules.
- `game/minigames/ellrijord_memory.rpy`: deck/difficulty metadata, board state,
  save-safe stopwatch, personal bests and the callable game label.
- `game/minigames/ellrijord_memory_ui.rpy`: split board/companion layout, card
  animations, reactions, instructions and restart confirmation.
- `game/components/exploration.rpy` and `game/scripts/day2_intro.rpy`: PC entry
  and normal-context calls. Day 1 is unchanged by this integration.

Other story locations or future interfaces should call a label in the normal
game context, then resume their own interface after it returns:

```renpy
call ell_minigames
# Or call the game directly, optionally choosing a difficulty:
call ellrijord_memory
call ellrijord_memory("normal")
```

Both entry points refuse access before Day 2. Do not launch gameplay using
`CallInNewContext` or from a `ShowMenu` context: saves need the normal story
context. A calling screen should return a command to its owning label, which
then calls the game, as the PC does. The wrappers preserve `quick_menu`; they do
not change the room, clock, background scene, inventory or collectibles.

`EllrijordMemory` uses a rollback-aware object with immutable card/index tuples,
`renpy.random` and a store `default` for the active board. Each flip and mismatch
timeout returns a command to a Ren'Py script loop. This gives Ren'Py a statement
boundary with the updated state before the next interaction. Keeping all flips
inside a single screen statement would cause mid-game saves to restore stale
state. Loading a visible mismatch restarts its short reveal timer safely.

The game label returns a save-local dictionary, also stored in
`ell_minigame_last_result`:

```python
{
    "minigame_id": "tsuki_memory",
    "status": "completed",  # or "abandoned"
    "difficulty": "normal",
    "deck": "tsuki_plushies",
    "mode": "classic",
    "moves": 11,
    "pairs_found": 8,
    "pairs_total": 8,
    "elapsed_seconds": 45,
}
```

Cancelling difficulty selection returns `None` and leaves the previous result
alone. Finishing or abandoning clears the active board. Completed rounds
record a personal best in `persistent.ell_memory_bests`, separately for each
deck/difficulty/mode. Fewest moves wins; elapsed seconds breaks a tie. Records
are committed when Finish is pressed, so unfinished/restarted rounds do not
count. Repeating Finish after loading is harmless. Rewards, achievements and
collection unlocks remain future work. Future handlers can consume the returned
result after the call; rendering/prediction must never award anything.

The Classic stopwatch uses Ren'Py's saved game runtime, not the operating-system
clock ([Ren'Py runtime documentation](https://www.renpy.org/doc/html/other.html#renpy.get_game_runtime)).
It survives save/load, freezes on completion, and excludes time in the
instructions, save and pause menus. Restart asks for confirmation; cancelling
preserves the board and excludes confirmation time. Restarting shuffles a fresh
board and resets its counters. The timer is informational, not a Time Attack mode.
Older prototype boards without timer/animation fields are upgraded without
reshuffling; their new stopwatch starts from zero when play resumes.

Tsuki has short, deterministic UI reactions for thinking, matches, mismatches
and completion. These do not call story labels or alter relationships. The
existing `gui/inventory_system/collectibles/tsuki_plushies.png` is referenced
directly in her companion panel; the original file is unchanged.

Add Cooking with Hana or Classroom Quizzes as separate scripts and register
their own callable labels in `ELL_MINIGAMES`. They can reuse the shell,
controls, availability check and result helper without depending on memory
game rules. Future deck unlock checks and score/reward handlers belong at the
availability/label/result boundaries, not inside card rendering.

## Replacing temporary artwork

Use aligned **400 × 560 RGBA PNG canvases** for every layer. Keep transparent
padding on each layer so they line up. No final art is generated or required.
The following paths are relative to `game/`:

```text
images/minigames/memory/tsuki_plushies/
    front.png
    back.png
    highlight.png
    incorrect.png
    illustrations/
        plush_01.png
        plush_02.png
        ...
        plush_15.png
```

Revealed cards compose `front.png`, then the card's illustration. `back.png`
covers hidden cards. `highlight.png` provides a subtle pulsing golden matched
outline; `incorrect.png` briefly highlights mismatches in red. Hover gently lifts
cards and buttons. A two-part horizontal flip switches faces at its narrowest
point. Replacing any PNG retains these behaviors. Missing card layers fall back
independently so an incomplete replacement cannot crash the board. Cards keep
the portrait aspect ratio and align all layers to the same canvas.

`images/minigames/memory/ui/` contains the plum/lavender background, rounded
gold-bordered panel/button textures, button states, portrait mask and icons.
Panels/buttons are nine-slice frames; keep their 36px corners when replacing
them, or update the shared UI helper. The companion portrait can be replaced by
changing `ELL_MEMORY_TSUKI_ART`; its crop/mask is defined alongside the layout.

Update names and optional `collectible_id` links in `ELL_MEMORY_DECKS` when
the plushie designs are supplied. `plush_01` maps to the existing
`cat_plush_1`; slots 02–15 have temporary animal names and no invented
collectible IDs. They are visual stand-ins, not additions to character canon.
Playing cards does not mark those collectibles as found. Existing collectible
UI advertises 15 plushies while the older quest target is 25; that unrelated
discrepancy is preserved for a later content decision.

Additional decks need a unique registry key, art directory and unique stable
card IDs. Expert and Tsuki's Challenge require at least 18 and 24 distinct
identities, respectively; duplicating the same card more than twice does not
provide a valid larger deck. Keep existing label, class and card IDs stable
once saves have been released.

`tools/assets/memory/plush_atlas.png` is the source illustration sheet generated
with the built-in imagegen tool. `tools/build_memory_ui_assets.py` extracts its
sprites, fits a copy of the existing cat plush to a card canvas, and draws the
temporary UI geometry. It never writes the original character or collectible
images. This is an optional authoring tool, not a runtime step; do not rerun it
over commissioned replacements. See `docs/memory_art_prompts.md` for provenance
and the exact illustration prompt.

## Verification

```powershell
python -B tools/test_memory_minigame.py --sdk ../renpy-8.5.1-sdk --output "$env:TEMP/ell-memory-tests"
python -B tools/test_day2_exploration.py --sdk ../renpy-8.5.1-sdk --output "$env:TEMP/ell-day2-tests"
```

The memory runner reuses the existing Day 2 test snapshot/process helpers. It
copies scripts and links read-only assets into temporary projects with isolated
saves, runs compile/lint, and exercises actual screen actions and save/load.
It checks all three playable difficulties, blocked larger boards, Day 1 guards,
cancellation/completion, pause/save menus, return navigation, inventory and
collectible preservation, rollback, restart/cancellation, instructions, menu
clock pausing, completion clock freezing and personal-best ordering. The three
isolated runs cover the installed skin, temporary 400 × 560 layer fixtures and
missing-card fallback. Fixtures break their hard links before being written,
so tests cannot overwrite shipped artwork. Reports and full-size screen renders
are copied to the output folder. No test hooks enter the working game.

For a baseline lint comparison, pass `--baseline /path/to/pre-change/project`.
The comparison ignores shifted source line numbers. Existing lint warnings
(including optional art, dynamically created characters, duplicate thumbnail
settings and the missing `ui_test_demo` label) are outside this integration.

The temporary visual skin passed compile/lint on Ren'Py 8.5.3 with no added
lint findings. Its installed-art, fixture-art and missing-card-art runs each
passed 93 distinct assertions. The existing Day 2 regression passed 38 checks
for each protagonist. Day 1 and the original Tsuki/cat artwork were compared
with the pre-change snapshot and remained identical. An actual engine render
is saved at `docs/previews/tsuki-memory-classic.png`.
