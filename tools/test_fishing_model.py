"""Deterministic mechanical tests of the exact simulation shipped in the RPY."""
from pathlib import Path
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
namespace = {}
source = (ROOT / "game/minigames/fishing_model.rpy").read_text(encoding="utf-8")
exec(compile(textwrap.dedent(source.split("init -3 python:\n", 1)[1]), "fishing_model.rpy", "exec"), namespace)
Model = namespace["EllFishingModel"]
SPECIES = namespace["ELL_FISHING_SPECIES"]
HAZARDS = namespace["ELL_FISHING_HAZARDS"]


def advance(game, seconds, fps=60):
    for _ in range(round(seconds * fps)):
        game.update(1.0 / fps)


def collision(game, fish_id="goldenfin", kind="fish"):
    entity = game.spawn(kind, fish_id)
    entity.update(x=game.config["hook_x"], y=game.hook_y, base_y=game.hook_y,
                  speed=0, phase=-game.elapsed*1.8)
    game.update(1 / 60)
    return entity


class FishingTests(unittest.TestCase):
    def test_hook_and_land_without_bait_cost(self):
        game = Model(seed=1)
        collision(game)
        self.assertEqual(game.hooked, "goldenfin")
        self.assertEqual(game.caught, 0)
        game.mouse_y = 248
        advance(game, .5)
        self.assertEqual((game.caught, game.bait, game.score), (1, 3, 100))
        self.assertIsNone(game.hooked)

    def test_one_fish_only(self):
        game = Model(seed=2)
        collision(game)
        collision(game, "mossback_carp")
        self.assertEqual(game.hooked, "goldenfin")
        self.assertEqual(len(game.entities), 1)

    def test_swept_collision_and_miss(self):
        hit = namespace["ell_fishing_swept_hit"]
        self.assertTrue(hit(-1000, 0, 1000, 0, 40, 30))
        self.assertFalse(hit(-1000, 100, 1000, 100, 40, 30))
        game = Model(seed=1)
        entity = game.spawn("fish", "goldenfin")
        entity.update(x=game.config["hook_x"]-100, base_y=game.hook_y, speed=30000, direction=1)
        game.update(1/120)
        self.assertEqual(game.hooked, "goldenfin")

    def test_hazards_and_invulnerability(self):
        game = Model(seed=2)
        game.hooked = "goldenfin"
        game.streak = 6
        game.hazard_hit({"id": "boot"})
        self.assertIsNone(game.hooked)
        self.assertEqual((game.streak, game.bait), (0, 3))
        game.invulnerable = 0
        game.hazard_hit({"id": "crab"})
        game.hazard_hit({"id": "eel"})
        self.assertEqual(game.bait, 2)
        advance(game, 2.6)
        game.hazard_hit({"id": "eel"})
        self.assertEqual(game.bait, 1)
        game.invulnerable = 0
        game.hazard_hit({"id": "crab"})
        self.assertTrue(game.finished)
        self.assertEqual(game.reason, "no_bait")

    def test_slow_snare_reverse_and_expiry(self):
        game = Model(seed=2)
        game.mouse_y = 900
        game.hazard_hit({"id": "branch"})
        advance(game, .5)
        self.assertEqual(game.hook_y, 390)
        advance(game, .5)
        self.assertTrue(390 < game.hook_y < 500)
        game.hazard_hit({"id": "weeds"})
        self.assertGreater(game.slow, 0)
        game.hazard_hit({"id": "wisp"})
        game.hook_y = 600
        game.mouse_y = 900
        advance(game, .5)
        self.assertLess(game.hook_y, 600)
        advance(game, 4)
        self.assertEqual(game.reverse, 0)

    def test_bait_pickup_capped(self):
        game = Model(seed=1)
        game.bait = 4
        collision(game, "bait", "bait")
        self.assertEqual(game.bait, 5)
        collision(game, "bait", "bait")
        self.assertEqual(game.bait, 5)

    def test_streak_score_and_target(self):
        game = Model(seed=1)
        for _ in range(30):
            game.hooked = "goldenfin"
            game.collect()
        self.assertEqual(game.longest_streak, 30)
        self.assertEqual(game.multiplier, 5)
        self.assertEqual(game.score, 10400)
        self.assertTrue(game.finished)
        self.assertEqual(game.reason, "target")

    def test_pause_all_state_and_timers(self):
        game = Model("night",seed=19)
        advance(game, 12)
        game.hazard_hit({"id":"wisp"})
        game.paused = True
        import pickle
        before = pickle.dumps(vars(game))
        advance(game, 20)
        self.assertEqual(before, pickle.dumps(vars(game)))

    def test_frame_rate_independent(self):
        games = [Model(seed=71) for _ in range(3)]
        for game, fps in zip(games, (30, 60, 144)):
            game.mouse_y = 780
            advance(game, 10, fps)
        for game in games[1:]:
            self.assertAlmostEqual(game.elapsed, games[0].elapsed, places=7)
            self.assertAlmostEqual(game.hook_y, games[0].hook_y, places=7)
            self.assertEqual(len(game.entities), len(games[0].entities))
            for a,b in zip(game.entities,games[0].entities):
                self.assertAlmostEqual(a["x"],b["x"],places=7)

    def test_time_availability_and_rods(self):
        self.assertNotIn("moonfin",Model("day").eligible())
        self.assertNotIn("sunset_koi",Model("night").eligible())
        self.assertNotIn("silverstream_trout",Model("night").eligible())
        self.assertIn("sunset_koi",Model("twilight").eligible())
        self.assertNotIn("void_leviathan",Model("night").eligible())
        def count(rod, species):
            game=Model("night",rod,seed=17)
            return sum(game.choose_fish()==species for _ in range(10000))
        self.assertGreater(count("moonlight","moonfin"),count("wooden","moonfin"))
        self.assertGreater(count("foxfire","foxfire_koi"),count("wooden","foxfire_koi"))
        normal,fast=Model(),Model(rod="silverstream")
        normal.mouse_y=fast.mouse_y=900
        advance(normal,.2);advance(fast,.2)
        self.assertGreater(fast.hook_y,normal.hook_y)
        game=Model(rod="reinforced",seed=1)
        game.hazard_hit({"id":"crab"})
        self.assertEqual(game.bait,3)

    def test_spawn_fairness_and_progression(self):
        game=Model("day",seed=11)
        self.assertIsNone(game.spawn("hazard"))
        game.catches={"goldenfin":30}
        self.assertEqual(game.difficulty,1)
        for _ in range(100):
            e=game.spawn("hazard")
            self.assertNotEqual(e["id"],"wisp")
            self.assertTrue(e["x"]<0 or e["x"]>1920)
            reaction=abs(e["x"]-game.config["hook_x"])/e["speed"]
            self.assertGreater(reaction,3)
        game=Model("night",seed=11)
        game.catches={"goldenfin":30}
        self.assertIn("wisp",{game.spawn("hazard")["id"] for _ in range(100)})

    def test_legend_requires_moonfin_and_landing(self):
        game=Model("night",seed=9,config={"legendary_chance":1,"legendary_min_score":0,"legendary_after":1})
        game.hooked="goldenfin";game.collect()
        self.assertEqual(game.encounter,"omen")
        game.hook_y=game.mouse_y=720
        advance(game,4.1)
        self.assertEqual(game.encounter,"visible")
        self.assertTrue(all(e["id"] in ("moonfin","void_leviathan") for e in game.entities))
        collision(game,"void_leviathan")
        self.assertIsNone(game.hooked)
        game.hooked="goldenfin"
        collision(game,"void_leviathan")
        self.assertEqual(game.hooked,"goldenfin")
        game.hooked="moonfin"
        collision(game,"void_leviathan")
        self.assertEqual(game.hooked,"void_leviathan")
        self.assertFalse(game.legend_caught)
        game.mouse_y=248
        advance(game,1)
        self.assertTrue(game.legend_caught)
        self.assertEqual(game.catches["void_leviathan"],1)
        self.assertNotIn("moonfin",game.catches)
        self.assertGreaterEqual(game.score,6000)

    def test_bonus_timeout_finishes_completed_target(self):
        game=Model("night",seed=1,config={"target":1,"legendary_after":1,"legendary_min_score":0,"legendary_chance":1,"legendary_duration":5})
        game.hooked="goldenfin";game.collect()
        self.assertFalse(game.finished)
        advance(game,5.1)
        self.assertTrue(game.finished)
        self.assertEqual(game.reason,"target")

    def test_result_and_assets(self):
        game=Model("night",seed=1)
        game.hooked="moonfin";game.collect();game.finish("abandoned")
        result=game.result()
        self.assertEqual(result["rare_caught"],1)
        self.assertEqual(result["status"],"abandoned")
        self.assertNotIn("entities",result)
        for fish_id,spec in SPECIES.items():
            self.assertTrue((ROOT/"game"/spec["art"]).is_file(),fish_id)
            self.assertTrue((ROOT/"game"/spec["silhouette"]).is_file(),fish_id)
            self.assertTrue((ROOT/"game/gui/inventory_system/icons"/(fish_id+".png")).is_file())
        for hazard_id in HAZARDS:
            self.assertTrue((ROOT/"game/images/minigames/fishing/hazards"/(hazard_id+".png")).is_file())


if __name__ == "__main__": unittest.main(verbosity=2)
