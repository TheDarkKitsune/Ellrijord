# Tsuki's Memory Challenge, adapted from the supplied Ren'Py 8 prototype.
# Live boards are save-local; only personal bests persist across playthroughs.

default ell_memory_game = None
default persistent.ell_memory_bests = {}

init -3 python:
    ELL_MEMORY_DIFFICULTIES = (
        ("easy", "Easy", 4, 3),
        ("normal", "Normal", 4, 4),
        ("hard", "Hard", 6, 4),
        ("expert", "Expert", 6, 6),
        ("tsuki", "Tsuki's Challenge", 8, 6),
    )
    # Temporary visual identities; only the cat has an established collectible
    # ID. These names do not define or unlock new story collectibles.
    ELL_MEMORY_TEMP_NAMES = ("Cat", "Fox", "Bunny", "Teddy", "Panda", "Red Panda", "Raccoon", "Penguin", "Owl", "Fawn", "Duck", "Shiba", "Dragon", "Lamb", "Koala")
    ELL_MEMORY_DECKS = {
        "tsuki_plushies": {
            "name": "Tsuki's 15 Plushies",
            "art_dir": "images/minigames/memory/tsuki_plushies",
            "cards": tuple({
                "id": "plush_{:02d}".format(i),
                "name": ELL_MEMORY_TEMP_NAMES[i - 1],
                "collectible_id": "cat_plush_1" if i == 1 else None,
            } for i in range(1, 16)),
        },
    }

    def ell_memory_difficulty(difficulty_id):
        return next((d for d in ELL_MEMORY_DIFFICULTIES if d[0] == difficulty_id), None)

    def ell_memory_can_play(difficulty_id, deck_id="tsuki_plushies", mode="classic"):
        difficulty = ell_memory_difficulty(difficulty_id)
        deck = ELL_MEMORY_DECKS.get(deck_id)
        return bool(mode == "classic" and difficulty and deck and
                    difficulty[2] * difficulty[3] // 2 <= len(set(c["id"] for c in deck["cards"])))

    def ell_memory_art(deck_id, layer, card_id=None):
        filename = "illustrations/{}.png".format(card_id) if layer == "illustration" else layer + ".png"
        path = ELL_MEMORY_DECKS[deck_id]["art_dir"] + "/" + filename
        return path if renpy.loadable(path) else None

    def ell_memory_card_name(deck_id, card_id):
        return next(c["name"] for c in ELL_MEMORY_DECKS[deck_id]["cards"] if c["id"] == card_id)

    def ell_memory_best(deck_id, difficulty_id, mode="classic"):
        return (persistent.ell_memory_bests or {}).get((deck_id, difficulty_id, mode))

    def ell_memory_record_result(result):
        if result["status"] != "completed":
            return
        key = (result["deck"], result["difficulty"], result["mode"])
        bests = dict(persistent.ell_memory_bests or {})
        old = bests.get(key)
        score = (result["moves"], result["elapsed_seconds"])
        if old is None or score < (old["moves"], old["elapsed_seconds"]):
            bests[key] = {"moves": score[0], "elapsed_seconds": score[1]}
            persistent.ell_memory_bests = bests
            renpy.save_persistent()

    class EllrijordMemory(renpy.python.RevertableObject):
        def __init__(self, difficulty_id, deck_id="tsuki_plushies", mode="classic"):
            if not ell_memory_can_play(difficulty_id, deck_id, mode):
                raise ValueError("Unsupported memory difficulty, deck or mode.")
            self.difficulty_id = difficulty_id
            self.deck_id = deck_id
            self.mode = mode
            difficulty = ell_memory_difficulty(difficulty_id)
            self.columns, self.rows = difficulty[2:]
            self.pairs = self.columns * self.rows // 2
            choices = list(dict.fromkeys(c["id"] for c in ELL_MEMORY_DECKS[deck_id]["cards"]))
            renpy.random.shuffle(choices)
            cards = choices[:self.pairs] * 2
            renpy.random.shuffle(cards)
            # Immutable tuples plus RevertableObject attribute assignments make
            # flips, matches and mismatch recovery safe for saves and rollback.
            self.cards = tuple(cards)
            self.opened = ()
            self.matched = ()
            self.moves = 0
            self.locked = False
            self.turning = ()
            self.started_runtime = renpy.get_game_runtime()
            self.finished_seconds = None
            self.reaction = "ready"

        @property
        def elapsed(self):
            finished = getattr(self, "finished_seconds", None)
            if finished is not None:
                return finished
            return max(0, int(renpy.get_game_runtime() - getattr(self, "started_runtime", renpy.get_game_runtime())))

        @property
        def complete(self):
            return len(self.matched) == len(self.cards)

        def prepare(self):
            # Existing prototype saves predate the stopwatch and visual fields.
            # Start their new clock when resumed without changing their board.
            if not hasattr(self, "started_runtime"):
                self.started_runtime = renpy.get_game_runtime()
            if not hasattr(self, "finished_seconds"):
                self.finished_seconds = 0 if self.complete else None
            if not hasattr(self, "turning"):
                self.turning = ()
            if not hasattr(self, "reaction"):
                self.reaction = "complete" if self.complete else "miss" if self.locked else "ready"

        def flip(self, index):
            self.prepare()
            if self.locked or index < 0 or index >= len(self.cards) or index in self.matched or index in self.opened:
                return
            self.opened += (index,)
            self.turning = (index,)
            self.reaction = "thinking"
            if len(self.opened) == 2:
                self.moves += 1
                a, b = self.opened
                if self.cards[a] == self.cards[b]:
                    self.matched += self.opened
                    self.opened = ()
                    self.reaction = "complete" if self.complete else "match"
                    if self.complete:
                        self.finished_seconds = self.elapsed
                else:
                    self.locked = True
                    self.reaction = "miss"

        def hide(self):
            self.prepare()
            self.turning = self.opened
            self.opened = ()
            self.locked = False

        def result(self):
            return ell_minigame_result(
                "tsuki_memory", "completed" if self.complete else "abandoned",
                difficulty=self.difficulty_id, deck=self.deck_id, mode=self.mode,
                moves=self.moves, pairs_found=len(self.matched) // 2,
                pairs_total=self.pairs,
                elapsed_seconds=self.elapsed,
            )



# Screens and visual assets live in ellrijord_memory_ui.rpy.

label ellrijord_memory(difficulty=None, deck_id="tsuki_plushies", mode="classic", _previous_quick_menu=None, _playing=True, _restart_runtime=0.0):
    if not ell_minigame_available("tsuki_memory") or deck_id not in ELL_MEMORY_DECKS or mode != "classic":
        return
    $ _previous_quick_menu = quick_menu
    $ quick_menu = False
    $ renpy.stop_skipping()
    if difficulty is None:
        call screen ell_memory_setup(deck_id)
        $ difficulty = _return
    if not ell_memory_can_play(difficulty, deck_id, mode):
        $ quick_menu = _previous_quick_menu
        return
    $ ell_memory_game = EllrijordMemory(difficulty, deck_id, mode)
    # Ren'Py saves at the beginning of an interactive statement. End the screen
    # for each action so the next interaction starts with the updated board.
    while _playing:
        $ ell_memory_game.prepare()
        call screen ellrijord_memory_screen(ell_memory_game)
        if _return[0] == "flip":
            $ ell_memory_game.flip(_return[1])
        elif _return[0] == "hide":
            $ ell_memory_game.hide()
        elif _return[0] == "tick":
            $ ell_memory_game.turning = ()
        elif _return[0] == "restart":
            $ _restart_runtime = renpy.get_game_runtime()
            call screen ell_memory_restart_confirm
            if _return:
                $ ell_memory_game = EllrijordMemory(difficulty, deck_id, mode)
            else:
                $ ell_memory_game.started_runtime = getattr(ell_memory_game, "started_runtime", _restart_runtime) + renpy.get_game_runtime() - _restart_runtime
        else:
            $ _playing = False
    $ ell_minigame_last_result = ell_memory_game.result()
    $ ell_memory_record_result(ell_minigame_last_result)
    $ ell_memory_game = None
    $ quick_menu = _previous_quick_menu
    return ell_minigame_last_result
