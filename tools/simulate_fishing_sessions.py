"""Run reproducible standard sessions with a simple mouse-targeting angler."""
import json
from pathlib import Path
from test_fishing_model import Model


def play(period, seed):
    game=Model(period,seed=seed,config={"legendary_chance":0})
    for _ in range(60*300):
        if game.finished:
            break
        target=248 if game.hooked else 430
        if not game.hooked:
            candidates=[]
            for e in game.entities:
                if e["kind"]!="fish":
                    continue
                arrival=(760-e["x"])/(e["direction"]*e["speed"])
                if 0 <= arrival < 3:
                    candidates.append((arrival,e))
            if candidates:
                arrival,e=min(candidates,key=lambda pair:pair[0])
                target=e["y"]
        if game.reverse:
            target=game.config["min_y"]+game.config["max_y"]-target
        game.mouse_y=target
        game.update(1/60)
    return dict(seed=seed,bait=game.bait,finished=game.finished,**game.result())


if __name__=="__main__":
    results=[play(period,seed) for period in ("day","twilight","night") for seed in (11,42,93)]
    destination=Path(__file__).resolve().parents[1]/"output/fishing-tests/simulated-sessions.json"
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(results,indent=2),encoding="utf-8")
    for result in results:
        print("{} seed {}: {} fish, {} bait, {}s, {}".format(result["period"],result["seed"],result["caught"],result["bait"],result["elapsed_seconds"],result["reason"]))
    if any(not r["finished"] or r["reason"]!="target" for r in results):
        raise SystemExit("Some anglers did not complete the target; inspect results.")
