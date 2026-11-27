# Forest Lake Fishing

## Launch and controls

From Day 2 free exploration, open **Map → Forest Lake → Cast a line**.
The forest path also links to the lake. Alternatively, use the bedroom PC's
**Minigames → Forest Lake Fishing**, alongside Tsuki's Memory Challenge.
Fishing returns to the location from which it was opened. Day 1 is unchanged.
Existing saves also gain access to the lake from Day 2 without a new playthrough.

Move the mouse down to lower the hook and up to raise it. Horizontal mouse
position does not move the line. Touch a fish with the bait, then raise it above
the waterline to land it. Catching and landing do not consume bait. Only one fish
can be carried at once. Esc, Space or Pause freezes the game; Help and exit
confirmation also pause it. Losing window focus pauses automatically.

A session starts with three bait lives and ends at 30 landed fish, after any
bonus encounter, or when bait runs out. Spare bait can restore lives up to five.
Every fifth consecutive catch increases the score multiplier, up to x5. A stolen
or lost fish resets the streak. Early Return keeps landed catches; Restart
discards the current session after confirmation.

The world's activity clock stays still during fishing, like the existing memory
game. It chooses the lighting and available species when a session starts:
day before 18:00, twilight 18:00–21:00, night from 21:00. The forest and lake are
accessible until the existing 23:00 day boundary. Travel still uses the existing
15-minute cost between areas.

## Mechanics and progression

- All eight requested species and all seven hazards are implemented.
- Hazards unlock after 4/6/8/10/14/18/20 catches. They enter from the edges,
  with at least three seconds' approach time to the hook at current speeds.
- Boot and pike steal the attached fish; branches briefly snag the line;
  weeds slow it; crab and eel remove a bait life; night wisps reverse controls.
- Bait damage grants 2.5 seconds of protection. The reinforced and later rods
  can resist hazards. Six rods are configured; only Wooden Rod starts unlocked.
- The journal records save-local discoveries, counts, first discovery date and
  game day, availability and locations. Undiscovered information stays hidden.
- Personal best score persists across playthroughs, like the memory game's bests.
- Existing achievements award the first catch, a 30-fish session and the guardian.

At night, after 26 catches and 2,500 points, the guardian has a 50% chance to
appear. Normal fish and hazards stop spawning; the lake darkens and a large
silhouette precedes the encounter. Moonfin continue to appear as possible lures.
Keep a Moonfin hooked, lower it to meet the Leviathan, then bring the Leviathan
above the surface. Ordinary bait and other fish cannot catch it. The Moonfin used
as a lure is consumed, without counting as a landed Moonfin. The encounter has a
65-second window; missing it resumes normal fishing. A landed Leviathan awards
6,000 base points and a journal entry. These conditions are configurable.

Catches use the existing `Inventory.add_item` API and ordinary species item IDs,
so future Cooking with Hana can consume them through the existing inventory.
Full stacks or slots send overflow to `ell_fishing_pending`, displayed at the
lake setup screen. **Collect stored fish** retries delivery without losing or
duplicating fish. No currency or separate shop was added. Sell values and rod
ownership are ready for later integration with the project's future shops.

Completed results are plain dictionaries. Live screens run in a disposable
Ren'Py context; swimming entities and timers are not included in completed saves.
Save after returning to exploration. Each session has a unique ID and a
save-local claimed ledger. Reapplying a result cannot deliver rewards twice;
rollback is blocked across session and reward boundaries. Loading an earlier
save restores that save's inventory and journal. Restarting has no reward commit.

## Files

Created:

- `game/minigames/fishing_model.rpy`: data, tuning, simulation and swept collisions.
- `game/minigames/fishing_displayable.rpy`: rendering, virtual mouse input, audio.
- `game/minigames/fishing_ui.rpy`: setup, tutorial, play, pause, results and journal.
- `game/minigames/fishing.rpy`: entry labels, rewards, inventory and achievements.
- `game/images/minigames/fishing/`: 3 paintings, 8 fish, 8 silhouettes,
  7 hazards, 3 gear sprites, 3 effects and 3 interface/journal assets.
- `game/gui/inventory_system/icons/{species_id}.png`: 8 inventory icons.
- `tools/build_fishing_assets.py`: repeatable original procedural artwork builder.
- `tools/assets/fishing_background_prompts.json`: exact built-in imagegen prompts.
- `tools/test_fishing_model.py`, `tools/test_fishing_renpy.py`,
  `tools/simulate_fishing_sessions.py`: mechanical, engine and session checks.
- This guide and test evidence under `output/fishing-tests/`.

Modified:

- `game/scripts/exploration.rpy`: lake location, forest link, night access and actions.
- `game/scripts/day2_intro.rpy`: dispatch lake actions from the exploration loop.
- `game/components/exploration.rpy`: lake map button and availability text.
- `tools/test_day2_exploration.py`: expect the newly opened forest and lake routes.
- `docs/minigames.md`: link the fishing guide from the existing minigame documentation.

The pre-existing `game/gui/menu/logo.png` edit was left alone.

## Replace artwork and tune content

Replace files under `game/images/minigames/fishing/`, keeping their names, or
change the corresponding data paths. All gameplay objects have transparency;
backgrounds contain environment only. Fish face **right** in their source art;
the renderer flips them when travelling left. Use the same visual centre for
fish and silhouettes. `size` controls display size; `bounds` controls the
collision ellipse independently of transparent padding.

Backgrounds share a 16:9 composition and are fitted to the 1920×1080 game canvas.
Keep the waterline around y=302 and the dock tip around x=760. If your replacement
composition moves those, update `surface`, `collect_y`, `hook_x`, hook limits and
the gear anchors in the displayable together. Native painting dimensions are
1672×941; keeping 1920×1080 or any matching wide ratio also works.

Each fish entry supports ID, name, art, silhouette, rarity, weight, speed range,
depth range, display size, collision bounds, score, sell value, time availability,
description, behaviour and location IDs. Add a species entry, sprite, silhouette
and inventory icon; the journal and results iterate the registry automatically.
New location names belong in `ELL_FISHING_LOCATIONS`, with their IDs in species
`locations`. Additional playable locations would also need their own launch and
background selection, while reusing the model and journal.

`ELL_FISHING_CONFIG` controls target, bait, movement, spawn intervals, protection
and guardian conditions. `ELL_FISHING_HAZARDS` controls unlock counts, sizes,
speeds and effects. `ELL_FISHING_RODS` defines equipment bonuses. Future shops can
add a rod ID to `ell_fishing_rods`; the setup screen then allows equipping it.
These are prepared extension points, not currently implemented purchases.

The three environment paintings were created with the built-in imagegen tool.
Sprites and decorative interface artwork use deterministic antialiased
procedural drawing; the rest of the UI reuses the existing minigame skin and
Tsuki portrait. Run `python tools/build_fishing_assets.py` only before replacing
the temporary sprites: it rebuilds those assets. It leaves lake paintings alone
and creates inventory icons only when they are missing. Pillow is a build-time
dependency already used by the project's other artwork builder; gameplay has no
new external dependency.

Optional sound paths are listed in `ELL_FISHING_AUDIO` in the displayable.
Add `hook.ogg`, `catch.ogg`, `hurt.ogg`, `rare.ogg`, `bait.ogg` or `omen.ogg` under
`game/audio/fishing/`, or point the mapping to suitable existing files. Missing
audio is checked before playback and is silent. Existing audio was not modified.

## Validation

Run from the project root with the existing Ren'Py 8.5.1 SDK:

```powershell
python tools/test_fishing_model.py
python tools/simulate_fishing_sessions.py
python tools/test_fishing_renpy.py --sdk ../renpy-8.5.1-sdk --output output/fishing-tests
python tools/test_day2_exploration.py --sdk ../renpy-8.5.1-sdk --output output/fishing-tests/exploration-regression
python tools/test_memory_minigame.py --sdk ../renpy-8.5.1-sdk --output output/fishing-tests/memory-regression
```

Recorded checks:

- 14 deterministic mechanical tests: swept hit/miss, hook/land, bait, all hazard
  effects and immunity, streak/target, pause, rates at 30/60/144 fps, species times,
  rods, spawn fairness, guardian lure/landing/timeout and required assets.
- Nine full simulated 30-fish sessions: three seeds at each time of day, completed
  in 56–66 simulated seconds with 1–4 bait remaining. This uses an automated angler,
  not a measurement of human difficulty.
- Real-engine fishing harness: 53 assertions and 16 captures, including actual
  event-driven catches, restart, exit, pause, journal, save/load, reward idempotency,
  overflow, night map access and the guardian. Runs at 1280×720 physical resolution
  against the game's 1920×1080 virtual coordinates.
- Existing Day 2 exploration: 39 checks for each protagonist and 22 captures each.
- Existing Memory Challenge: 242 assertions per artwork mode; all three modes pass.
- Ren'Py compile succeeds. Lint has no additional warnings compared with the
  pre-change report. Existing missing story images, `ui_test_demo` and a controller
  escape-sequence warning remain outside this change.

Screenshots, lint reports and JSON results are in `output/fishing-tests/`.
Automated input and rendering were tested; manual mouse feel, audible sound
effects and controller/touch-specific fishing controls have not been playtested.
The requested mouse controls are implemented. Optional fishing audio files are
not supplied. Shops, selling, cooking recipes and unlocking later rods remain
future integrations as requested.
