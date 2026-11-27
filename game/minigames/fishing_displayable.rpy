# Rendering and input adapter. The simulation lives in fishing_model.rpy.
init -1 python:
    import pygame as fishing_pygame

    ELL_FISHING_AUDIO = {
        "hook": "audio/fishing/hook.ogg", "catch": "audio/fishing/catch.ogg",
        "hurt": "audio/fishing/hurt.ogg", "rare": "audio/fishing/rare.ogg",
        "bait": "audio/fishing/bait.ogg", "omen": "audio/fishing/omen.ogg",
    }

    class EllFishingDisplayable(renpy.Displayable):
        def __init__(self, period="day", rod="wooden", **kwargs):
            super(EllFishingDisplayable, self).__init__(**kwargs)
            self.model = EllFishingModel(period, rod)
            self.last_st = None
            self.cache = {}
            self.text_cache = {}
            self.background = Transform("images/minigames/fishing/backgrounds/" + period + ".png", xysize=(1920, 1080))
            self.shade = Solid("#0d052a99", xysize=(1920, 778))

        def set_pause(self, value=True):
            self.model.paused = value
            self.last_st = None
            renpy.redraw(self, 0)

        def abandon(self):
            self.model.finish("abandoned")
            return self.model.result()

        def leave(self):
            renpy.end_interaction(self.abandon())

        def sprite(self, path, size, direction=1, phase=0, alpha=1.0):
            key = (path, size, direction, phase, alpha)
            if key not in self.cache:
                self.cache[key] = Transform(path, xysize=size, xzoom=direction,
                                             yzoom=(1.0, 0.97, 1.03)[phase], alpha=alpha)
            return self.cache[key]

        def draw(self, render, child, x, y, st):
            rendered = renpy.render(child, 1920, 1080, st, st)
            render.blit(rendered, (int(x), int(y)))

        def label(self, render, text, x, y, st, size=24, color="#fff1db"):
            key = (text, size, color)
            if key not in self.text_cache:
                if len(self.text_cache) > 160:
                    self.text_cache.clear()
                self.text_cache[key] = Text(text, font="DejaVuSans.ttf", size=size, color=color, substitute=False, outlines=[(1, "#111827aa", 0, 1)])
            self.draw(render, self.text_cache[key], x, y, st)

        def render(self, width, height, st, at):
            m = self.model
            # Only event() advances the model: prediction and render-to-file
            # cannot move a hook, collect a fish or grant rewards.
            render = renpy.Render(1920, 1080)
            t = m.elapsed
            self.draw(render, self.background, 0, 0, t)
            if m.encounter:
                self.draw(render, self.shade, 0, 302, t)
                if m.encounter == "omen":
                    silhouette = self.sprite("images/minigames/fishing/silhouettes/void_leviathan.png", (700, 330), alpha=0.55)
                    self.draw(render, silhouette, 1100 - m.encounter_time * 100, 570, t)
            # Deterministic atmosphere follows simulation time, including pause.
            for i in range(16):
                bx = (i * 139 + fishing_math.sin(t * 0.4 + i) * 16) % 1880 + 20
                by = 1040 - ((t * (24 + i % 5 * 6) + i * 61) % 715)
                size = 9 + i % 4 * 3
                self.draw(render, self.sprite("images/minigames/fishing/effects/bubble.png", (size, size)), bx, by, t)
            canvas = render.canvas()
            for i in range(7):
                sx = i * 340 - 150 + int(fishing_math.sin(t * 0.25 + i) * 25)
                canvas.polygon("#caeff509", [(sx, 309), (sx + 35, 309), (sx + 280, 1010), (sx + 110, 1010)])
            for e in m.entities:
                path = ELL_FISHING_SPECIES[e["id"]]["art"] if e["kind"] == "fish" else "images/minigames/fishing/hazards/" + e["id"] + ".png" if e["kind"] == "hazard" else "images/minigames/fishing/gear/bait.png"
                phase = int(t * 5 + e["phase"]) % 3
                self.draw(render, self.sprite(path, (e["width"], e["height"]), e["direction"], phase), e["x"] - e["width"] / 2, e["y"] - e["height"] / 2, t)
                if e["kind"] == "fish" and ELL_FISHING_SPECIES[e["id"]]["rarity"] in ("Rare", "Epic", "Legendary"):
                    self.draw(render, self.sprite("images/minigames/fishing/effects/spark.png", (24, 24)), e["x"] - 30, e["y"] - e["height"] / 2 - 10, t)
            x = int(m.config["hook_x"])
            # Draw the line as its own layer so GL texture caching cannot hide
            # canvas edits made after another child has already been rendered.
            self.draw(render, self.sprite("images/minigames/fishing/gear/rod.png", (300, 150)), x - 292, 111, t)
            self.draw(render, Solid("#26364f99", xysize=(4, max(1, int(m.hook_y - 131)))), x + 1, 131, t)
            self.draw(render, Solid("#e6f3e5dd", xysize=(2, max(1, int(m.hook_y - 131)))), x, 131, t)
            if not m.invulnerable or int(t * 10) % 2:
                self.draw(render, self.sprite("images/minigames/fishing/gear/hook.png", (34, 48)), x - 27, m.hook_y - 8, t)
                if m.hooked:
                    spec = ELL_FISHING_SPECIES[m.hooked]
                    sw, sh = spec["size"]
                    self.draw(render, self.sprite(spec["art"], (sw, sh), -1, int(t * 7) % 3), x - sw * 0.55, m.hook_y - sh * 0.35, t)
                else:
                    self.draw(render, self.sprite("images/minigames/fishing/gear/bait.png", (28, 30)), x - 8, m.hook_y + 17, t)
            for effect in m.effects:
                age = effect["age"]
                self.draw(render, self.sprite("images/minigames/fishing/effects/catch.png", (110, 80), alpha=round(max(0.0, 1 - age / 1.2), 1)), x - 55, effect["y"] - age * 70, t)
                self.label(render, "+{}".format(effect["points"]), x + 45, effect["y"] - age * 100, t, 30, "#ffe49b")
            for i in range(5):
                sy = 302 + int(fishing_math.sin(t * 1.3 + i) * 2)
                canvas.line("#cbfff650", (i * 410 + 10, sy), (i * 410 + 240, sy), width=2)
            self.draw(render, self.sprite("images/minigames/fishing/ui/hud.png", (1872, 112)), 24, 18, t)
            self.label(render, "FOREST LAKE", 54, 36, t, 31, "#e4c575")
            self.label(render, "{}  |  {}".format(m.period.title(), ELL_FISHING_RODS[m.rod_id]["name"]), 54, 80, t, 20)
            stats = [("CATCH", "{} / {}".format(m.caught, m.config["target"])), ("BAIT", "{} / {}".format(m.bait, m.config["max_bait"])), ("SCORE", "{:,}".format(m.score)), ("STREAK", "{}  /  x{}".format(m.streak, m.multiplier))]
            for i, (caption, value) in enumerate(stats):
                sx = 490 + i * 212
                self.label(render, caption, sx, 35, t, 15, "#bfaed1")
                self.label(render, value, sx, 66, t, 29)
            self.draw(render, self.sprite("images/minigames/fishing/ui/notice.png", (1300, 65)), 310, 991, t)
            message = m.notice if m.notice_time else "Lower the hook to meet a fish. Raise it above the glowing waterline to land it."
            self.label(render, message, 340, 1010, t, 21)
            if m.encounter:
                self.label(render, "THE DEEP IS LISTENING  |  {}s".format(max(0, int(m.config["legendary_duration"] - m.encounter_time))), 1240, 930, t, 20, "#dbc5ff")
            if m.reverse or m.slow or m.snare:
                status = "REVERSED" if m.reverse else "SNAGGED" if m.snare else "SLOWED"
                self.label(render, status, x + 50, m.hook_y - 65, t, 20, "#ffc79d")
            renpy.redraw(self, 1.0 / 60.0)
            renpy.timeout(1.0 / 120.0)
            return render

        def event(self, ev, x, y, st):
            m = self.model
            if ev.type == fishing_pygame.MOUSEMOTION:
                # Ren'Py supplies these in virtual displayable coordinates.
                m.mouse_y = float(y)
            if ev.type == fishing_pygame.ACTIVEEVENT and not ev.gain:
                self.set_pause(True)
                renpy.run(SetScreenVariable("overlay", "pause"))
            if self.last_st is not None:
                m.update(st - self.last_st)
            self.last_st = st
            while m.events:
                path = ELL_FISHING_AUDIO.get(m.events.pop(0))
                if path and renpy.loadable(path):
                    renpy.sound.play(path)
            if m.finished:
                return m.result()
            renpy.timeout(1.0 / 120.0)

        def visit(self):
            return [self.background, self.shade] + list(self.cache.values()) + list(self.text_cache.values())
