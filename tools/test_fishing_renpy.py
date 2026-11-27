"""Exercise fishing screens, input, progression and save/load in real Ren'Py.

Copies scripts into an isolated project and hard-links read-only artwork.
Usage: python tools/test_fishing_renpy.py --sdk ../renpy-8.5.1-sdk --output output/fishing-tests
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
from test_day2_exploration import snapshot, run_hidden

HARNESS = r'''
define config.default_fullscreen = False
define config.sound = False
define config.autosave_on_choice = False
define config.autosave_on_quit = False
define config.physical_width = 1280
define config.physical_height = 720
default ft_stage = 0
default ft_ticks = 0
default ft_before = None
default ft_first_result = None
default persistent.ft_loaded = False

init 999 python:
    import json as ft_json
    import os as ft_os
    import types as ft_types
    ft_checks = []
    ft_captures = set()
    config.overlay_screens.append('_fishing_test_driver')

    def ft_check(name, condition):
        if not condition:
            raise AssertionError(name)
        ft_checks.append(name)

    def ft_capture(name, screen):
        if name not in ft_captures:
            renpy.render_to_file(renpy.get_screen(screen), name + '.png', width=1920, height=1080, resize=True)
            ft_captures.add(name)

    def ft_click(screen, widget_id):
        widget = renpy.get_widget(screen, widget_id)
        ft_check('button available: '+widget_id, widget is not None and widget.is_sensitive())
        renpy.display.screen.push_current_screen(renpy.get_screen(screen))
        try:
            result = renpy.run(widget.clicked)
        finally:
            renpy.display.screen.pop_current_screen()
        if result is not None:
            renpy.end_interaction(result)

    def ft_lake():
        return renpy.get_widget('ell_fishing_play','fishing_lake')

    def ft_drive():
        s = renpy.store
        try:
            s.ft_ticks += 1
            if ft_ticks > 500:
                raise AssertionError('driver stalled at stage '+str(ft_stage))
            if ft_stage == 0 and renpy.get_screen('ell_fishing_setup'):
                ft_check('time follows existing world clock',ell_fishing_period()=='night')
                ft_check('unowned rods locked',not renpy.get_widget('ell_fishing_setup','fishing_rod_moonlight').is_sensitive())
                ft_capture('setup-night','ell_fishing_setup')
                s.ft_stage = 1
                ft_click('ell_fishing_setup','fishing_journal')
            elif ft_stage == 1 and renpy.get_screen('ell_fishing_journal_screen'):
                ft_check('journal starts undiscovered',not ell_fishing_journal)
                ft_capture('journal-undiscovered','ell_fishing_journal_screen')
                ft_click('ell_fishing_journal_screen','fishing_entry_void_leviathan')
                ft_click('ell_fishing_journal_screen','fishing_journal_close')
                s.ft_stage=2
                ft_click('ell_fishing_setup','fishing_play')
            elif ft_stage==2 and renpy.get_screen('ell_fishing_tutorial'):
                ft_capture('tutorial','ell_fishing_tutorial')
                s.ft_stage=3
                ft_click('ell_fishing_tutorial','fishing_tutorial_start')
            elif ft_stage==3 and renpy.get_screen('ell_fishing_play'):
                lake=ft_lake();m=lake.model
                if m.elapsed < .4:
                    return
                lake.event(ft_types.SimpleNamespace(type=fishing_pygame.MOUSEMOTION),760,700,lake.last_st)
                ft_check('CDD receives virtual mouse coordinates',m.mouse_y==700)
                for i,fish_id in enumerate(('goldenfin','mossback_carp','moonfin','foxfire_koi','crystal_perch')):
                    e=m.spawn('fish',fish_id)
                    e.update(x=300+i*310,base_y=480+i*76,y=480+i*76)
                before=(m.elapsed,m.caught,m.score)
                ft_capture('gameplay-night','ell_fishing_play')
                ft_check('render capture has no gameplay side effects',before==(m.elapsed,m.caught,m.score))
                s.ft_stage=4
                ft_click('ell_fishing_play','fishing_pause')
                s.ft_before=(m.elapsed,m.hook_y,m.fish_clock,m.reverse,[(e['x'],e['y']) for e in m.entities])
                s.ft_ticks=0
            elif ft_stage==4:
                m=ft_lake().model
                if ft_ticks < 4:
                    return
                now=(m.elapsed,m.hook_y,m.fish_clock,m.reverse,[(e['x'],e['y']) for e in m.entities])
                ft_check('pause freezes every entity and timer',now==ft_before)
                ft_capture('pause','ell_fishing_play')
                ft_click('ell_fishing_play','fishing_pause_help')
                s.ft_stage=5
            elif ft_stage==5:
                ft_capture('instructions','ell_fishing_play')
                ft_click('ell_fishing_play','fishing_resume')
                s.ft_stage=6
            elif ft_stage==6:
                ft_check('resume unpauses model',not ft_lake().model.paused)
                ft_click('ell_fishing_play','fishing_pause')
                s.ft_stage=60
            elif ft_stage==60:
                ft_click('ell_fishing_play','fishing_restart')
                s.ft_stage=7
            elif ft_stage==7:
                ft_capture('restart-confirm','ell_fishing_play')
                s.ft_stage=8
                ft_click('ell_fishing_play','fishing_restart_confirm')
            elif ft_stage==8:
                lake=ft_lake();m=lake.model
                ft_check('restart resets bait score and catches',(m.bait,m.score,m.caught)==(3,0,0))
                # A real event-driven collision, followed by raising the hook.
                m.entities=[]
                m.hook_y=m.mouse_y=600
                e=m.spawn('fish','goldenfin');e.update(x=760,y=600,base_y=600,speed=0)
                s.ft_stage=9
            elif ft_stage==9:
                m=ft_lake().model
                ft_check('live event loop hooks a colliding fish',m.hooked=='goldenfin')
                m.mouse_y=248
                s.ft_stage=10
            elif ft_stage==10:
                m=ft_lake().model
                if not m.caught:
                    return
                ft_check('live reel lands fish without bait loss',m.catches=={'goldenfin':1} and m.bait==3)
                m.hooked='moonfin';m.collect()
                ft_click('ell_fishing_play','fishing_exit')
                s.ft_stage=11
            elif ft_stage==11:
                ft_check('opening exit does not end the session',not ft_lake().model.finished)
                ft_capture('exit-confirm','ell_fishing_play')
                s.ft_stage=12
                ft_click('ell_fishing_play','fishing_exit_confirm')
            elif ft_stage==12 and renpy.get_screen('ell_fishing_results'):
                result=ell_minigame_last_result
                ft_check('completed results register species',set(ell_fishing_journal)=={'goldenfin','moonfin'})
                ft_check('existing inventory receives catches',inventory.has_item('goldenfin',1) and inventory.has_item('moonfin',1))
                ft_check('result has rare count and rewards',result['rare_caught']==1 and result['rewards']['inventory']==2)
                ft_check('reapplying result cannot duplicate rewards',not ell_fishing_commit(result))
                ft_capture('results','ell_fishing_results')
                ft_click('ell_fishing_results','fishing_results_journal')
                s.ft_stage=13
            elif ft_stage==13:
                ft_click('ell_fishing_journal_screen','fishing_entry_moonfin')
                s.ft_stage=14
            elif ft_stage==14:
                ft_capture('journal-discovered','ell_fishing_journal_screen')
                ft_click('ell_fishing_journal_screen','fishing_journal_close')
                s.ft_stage=150
                ft_click('ell_fishing_results','fishing_again')
            elif ft_stage==150 and renpy.get_screen('ell_fishing_setup'):
                ft_check('play again returns to setup without duplicate rewards',ell_fishing_journal['moonfin']['count']==1)
                s.ft_stage=15
                ft_click('ell_fishing_setup','fishing_return')
            elif ft_stage==16 and renpy.get_screen('ell_fishing_setup'):
                s.ft_stage=17
                ft_click('ell_fishing_setup','fishing_play')
            elif ft_stage==17 and renpy.get_screen('ell_fishing_play'):
                m=ft_lake().model
                m.config.update(target=1,legendary_after=1,legendary_min_score=0,legendary_chance=1)
                m.hooked='goldenfin';m.collect()
                m.hook_y=m.mouse_y=700
                s.ft_stage=18
            elif ft_stage==18:
                m=ft_lake().model
                if m.encounter_time<1:
                    return
                ft_check('legendary encounter darkens lake',m.encounter=='omen')
                ft_capture('legendary-silhouette','ell_fishing_play')
                s.ft_stage=19
            elif ft_stage==19:
                m=ft_lake().model
                if m.encounter!='visible':
                    return
                ft_capture('legendary-visible','ell_fishing_play')
                m.hooked='moonfin'
                m.hook_y=m.mouse_y=700
                e=next(e for e in m.entities if e['id']=='void_leviathan')
                e.update(x=760,y=700,base_y=700,speed=0)
                s.ft_stage=20
            elif ft_stage==20:
                m=ft_lake().model
                ft_check('live legendary collision uses Moonfin lure (hook={}, paused={}, y={}, elapsed={})'.format(m.hooked,m.paused,m.hook_y,m.elapsed),m.hooked=='void_leviathan')
                m.mouse_y=248
                s.ft_stage=21
            elif ft_stage==21 and renpy.get_screen('ell_fishing_results'):
                ft_check('legendary results register guardian',ell_minigame_last_result['legendary'] and 'void_leviathan' in ell_fishing_journal)
                ft_capture('legendary-results','ell_fishing_results')
                s.ft_stage=22
                ft_click('ell_fishing_results','fishing_results_return')
            elif ft_stage==23 and renpy.get_screen('ell_world_map'):
                ft_capture('exploration-map','ell_world_map')
                ft_check('night lake accessible on map',renpy.get_widget('ell_world_map','world_destination_forest_lake').is_sensitive())
                s.ft_stage=24
                renpy.end_interaction('forest_lake')
        except renpy.display.core.EndInteraction:
            raise
        except Exception:
            import traceback
            with open(ft_os.path.join(config.basedir,'test-error.txt'),'w') as f:
                f.write(traceback.format_exc())
            renpy.quit(status=1,save=False)

screen _fishing_test_driver():
    zorder 999
    timer .15 repeat True action Function(ft_drive)

label _fishing_test_start:
    $ ell_day=1
    $ ft_check('Day 1 fishing unavailable',not ell_minigame_available('forest_fishing'))
    $ ell_day=2
    $ ell_world_location='forest_lake'
    $ ell_world_minutes=1290
    $ ell_world_sync_time()
    $ ell_world_tutorial_active=False
    $ ft_check('Day 2 fishing available',ell_minigame_available('forest_fishing'))
    $ ft_check('night travel allowed',not ell_world_travel_reason('forest_lake'))
    call ellrijord_fishing
    $ ft_check('return preserves location and clock',ell_world_location=='forest_lake' and ell_world_minutes==1290)
    $ ft_check('live screen disposed',renpy.get_screen('ell_fishing_play') is None)
    $ ft_first_result=ell_minigame_last_result
    $ renpy.save('fishing-checkpoint')
    if not persistent.ft_loaded:
        $ persistent.ft_loaded=True
        $ ell_fishing_journal={}
        $ inventory=Inventory()
        $ renpy.load('fishing-checkpoint')
    $ ft_check('save/load restores journal',ell_fishing_journal['moonfin']['count']==1)
    $ ft_check('save/load restores inventory',inventory.has_item('moonfin',1))
    $ ft_check('loaded results still cannot duplicate',not ell_fishing_commit(ft_first_result))
    $ ft_stage=16
    call ellrijord_fishing
    $ ft_check('second return preserves location',ell_world_location=='forest_lake')
    $ ft_stage=23
    call screen ell_world_map
    # Overflow uses the real inventory slot limits and never discards rewards.
    $ inventory=Inventory(unlocked_slots=0)
    $ ell_fishing_pending={'goldenfin':4}
    $ ft_check('overflow retained',ell_fishing_deliver()==0 and ell_fishing_pending=={'goldenfin':4})
    $ inventory.unlocked_slots=7
    $ ft_check('overflow collected exactly once',ell_fishing_deliver()==4 and ell_fishing_deliver()==0 and inventory.has_item('goldenfin',4))
    # Verify all three installed paintings render using the same composition.
    python:
        for period in ('day','twilight'):
            lake=EllFishingDisplayable(period)
            lake.model.spawn('fish','goldenfin').update(x=900,y=600,base_y=600)
            renpy.render_to_file(lake,'gameplay-'+period+'.png',width=1920,height=1080,resize=True)
            ft_captures.add('gameplay-'+period)
        with open(ft_os.path.join(config.basedir,'results.json'),'w') as f:
            ft_json.dump({'checks':ft_checks,'screenshots':sorted(ft_captures)},f,indent=2)
    $ renpy.quit(status=0,save=False)
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    root=Path(__file__).resolve().parents[1]
    command=[str(args.sdk.resolve()/"lib/py3-windows-x86_64/python.exe"),str(args.sdk.resolve()/"renpy.py")]
    env=dict(os.environ,PYTHONFAULTHANDLER="1",SDL_VIDEODRIVER="windows",SDL_AUDIODRIVER="dummy",RENPY_RENDERER="gl2",RENPY_DISABLE_SOUND="1",RENPY_SKIP_SPLASHSCREEN="1",RENPY_SKIP_MAIN_MENU="1")
    with tempfile.TemporaryDirectory(prefix="ell-fishing-") as temp:
        project=Path(temp)
        snapshot(root/"game",project/"game")
        start=project/"game/scripts/script.rpy"
        start.write_text(start.read_text(encoding="utf-8-sig").replace("label start:\n","label start:\n    jump _fishing_test_start\n",1),encoding="utf-8")
        (project/"game/zz_fishing_test.rpy").write_text(HARNESS,encoding="utf-8")
        try:
            completed=run_hidden(command+[str(project),"--savedir",str(project/"isolated-saves"),"run"],env)
            (project/"test-process.txt").write_text(completed.stdout+completed.stderr,encoding="utf-8")
            if completed.returncode or not (project/"results.json").exists():
                for name in ("test-error.txt","errors.txt","traceback.txt","test-process.txt"):
                    p=project/name
                    if p.exists(): print(p.read_text(encoding="utf-8-sig")[-6500:])
                raise RuntimeError("Ren'Py fishing harness failed")
            report=json.loads((project/"results.json").read_text())
            for name in ("test-error.txt", "errors.txt", "traceback.txt"):
                stale=args.output/name
                if stale.exists():
                    stale.unlink()
            print("Passed {} assertions; captured {} screens.".format(len(report["checks"]),len(report["screenshots"])))
        finally:
            for path in project.iterdir():
                if path.is_file() and path.suffix in {".png",".json",".txt"}:
                    shutil.copy2(path,args.output/path.name)


if __name__=="__main__": main()
