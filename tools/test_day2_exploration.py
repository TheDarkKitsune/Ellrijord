"""Exercise Day 2 with the real Ren'Py engine in isolated projects.

python tools/test_day2_exploration.py --sdk ../renpy-8.5.1-sdk --output /path/to/results
Assets are read through temporary hard links; scripts, saves and caches are isolated.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading


HARNESS = r'''
define config.default_fullscreen = False
define config.sound = False
define config.autosave_on_choice = False
define config.autosave_on_quit = False
define config.physical_width = 1280
define config.physical_height = 720
define config.image_cache_size_mb = 64
default world_test_stage = 0
default world_test_target = None
default world_test_replayed = False
default world_test_loaded = False
default world_test_wait_lunch = False
default world_test_pc_view = 0
default world_test_pause_ticks = 0
default world_test_wait_cancel = False
default world_test_help_cancel = False
default world_test_unchanged_clock = -1
default world_test_unchanged_location = ""
default world_test_unchanged_name = ""
default world_test_map_locks_checked = False

init 999 python:
    import json as test_json
    import os as test_os
    import copy as test_copy
    test_checks = []
    test_captures = set()
    test_say_original = renpy.exports.say
    config.overlay_screens.append('_world_test_driver')
    def test_ensure_driver():
        if not renpy.get_screen('_world_test_driver'):
            renpy.show_screen('_world_test_driver')
    config.interact_callbacks.append(test_ensure_driver)
    def test_check(name, condition):
        if not condition:
            raise AssertionError(name)
        test_checks.append(name)

    def test_capture(name):
        if name not in test_captures:
            renpy.screenshot(test_os.path.join(config.basedir, name + '.png'))
            test_captures.add(name)

    def test_click(screen, widget_id):
        widget = renpy.get_widget(screen, widget_id)
        if widget is None:
            raise AssertionError('Missing {} on {}; ids: {}'.format(widget_id, screen, list(renpy.get_screen(screen).widgets)))
        if not widget.is_sensitive():
            raise AssertionError('Disabled action: ' + widget_id)
        renpy.display.screen.push_current_screen(renpy.get_screen(screen))
        try:
            result = renpy.run(widget.clicked)
        finally:
            renpy.display.screen.pop_current_screen()
        if result is not None:
            renpy.end_interaction(result)

    def test_say(who, what, *args, **kwargs):
        kwargs['interact'] = False
        return test_say_original(who, what, *args, **kwargs)

    def test_menu(items):
        # The only menu added by this feature is the bed's rest/sleep choice.
        label, value = next((label, value) for label, value in items if label == 'Sleep until morning.')
        return value() if callable(value) else value

    def test_model():
        s = renpy.store
        names = ['ell_day', 'ell_time_of_day'] + [name for name in vars(s) if name.startswith('ell_world_') and not callable(getattr(s, name))]
        names += ['ell_active_quests', 'ell_completed_quests', 'ell_quest_progress']
        backup = {name: test_copy.deepcopy(getattr(s, name)) for name in names}
        try:
            s.ell_day = 2
            s.ell_world_minutes = 420
            s.ell_world_location = 'bedroom'
            s.ell_world_unlocked = set(ELL_WORLD_STARTING_LOCATIONS)
            test_check('park initially locked', bool(ell_world_travel_reason('park')))
            test_check('locked trip rejected', not ell_world_travel('park') and ell_world_minutes == 420)
            s.ell_world_notice = ''
            test_check('bulletin unlocks once', ell_world_read_bulletin() and ell_world_minutes == 425)
            test_check('routes unlocked', {'park', 'library'} <= ell_world_unlocked)
            test_check('rereading consumes no time', not ell_world_read_bulletin() and ell_world_minutes == 425)
            test_check('same-area movement free', ell_world_travel('kitchen') and ell_world_minutes == 425)
            s.ell_world_minutes = 450
            test_check('cross-area movement 15 minutes', ell_world_travel('school_gate') and ell_world_minutes == 465)
            test_check('Tsuki before school', ell_world_npc_location('tsuki', 479) == 'kitchen')
            test_check('Tsuki arrives at school', ell_world_npc_location('tsuki', 480) == 'school_corridor')
            test_check('students unavailable in lessons', all(ell_world_npc_location(npc, 510) is None for npc in ELL_WORLD_NPCS if npc != 'hana'))
            test_check('lunch schedule boundary', len([npc for npc in ELL_WORLD_NPCS if ell_world_npc_location(npc, 720) == 'courtyard']) == 7)
            test_check('afternoon schedule boundary', ell_world_npc_location('mimi', 900) == 'library' and ell_world_npc_location('kuroe', 900) == 'park')
            s.ell_world_location = 'classroom'
            s.ell_world_classes = set()
            test_check('morning lesson advances to lunch', ell_world_attend_class() and ell_world_minutes == 720)
            test_check('no duplicate morning credit', not ell_world_attend_class())
            s.ell_world_minutes = 780
            test_check('afternoon lesson advances to 15:00', ell_world_attend_class() and ell_world_minutes == 900)
            test_check('school quest completes', 'day2_school_day' in ell_completed_quests)
            s.ell_world_location = 'hallway'
            s.ell_world_minutes = 1070
            test_check('opening hours checked at arrival', not ell_world_travel('school_gate') and ell_world_minutes == 1070)
            s.ell_world_location = 'school_corridor'
            ell_world_advance(20)
            test_check('closing school exits into town', ell_world_location == 'town_centre' and bool(ell_world_notice))
            s.ell_world_minutes = 1255
            ell_world_advance(10)
            test_check('closing town returns home', ell_world_location == 'hallway' and ell_time_of_day == 'night')
            ell_world_advance(999)
            test_check('clock caps at 23:00', ell_world_minutes == 1380)
            s.ell_world_tutorial_complete = True
            ell_world_new_day()
            test_check('sleep rolls over day and clock', ell_day == 3 and ell_world_minutes == 420 and ell_time_of_day == 'morning')
            test_check('sleep preserves unlocks/tutorial', {'library', 'park'} <= ell_world_unlocked and ell_world_tutorial_complete)
            s.ell_completed_quests = set(ell_completed_quests) - {'day2_school_day'}
            s.ell_active_quests = set(ell_active_quests) | {'day2_school_day'}
            s.ell_quest_progress = dict(ell_quest_progress, day2_school_day=1)
            ell_world_new_day()
            test_check('unfinished school day resets partial progress', ell_quest_progress['day2_school_day'] == 0)
            s.ell_world_location = 'classroom'
            s.ell_world_minutes = 480
            ell_world_attend_class()
            s.ell_world_minutes = 780
            ell_world_attend_class()
            test_check('missed school quest can finish on a later day', 'day2_school_day' in ell_completed_quests)
            ell_world_new_day()
            s.ell_world_location = 'classroom'
            s.ell_world_minutes = 480
            ell_world_attend_class()
            test_check('later classes do not reopen a completed quest', 'day2_school_day' in ell_completed_quests and 'day2_school_day' not in ell_active_quests)
        finally:
            for name, value in backup.items():
                setattr(s, name, value)

    def test_drive():
        s = renpy.store
        try:
            if renpy.get_screen('showmenu'):
                s.world_test_pause_ticks += 1
                if world_test_pause_ticks < 3:
                    return
                test_capture('pause-menu')
                renpy.end_interaction(renpy.run(Return()))
                return
            if renpy.get_screen('day1_game_ui_popup') or renpy.get_screen('day1_secret_discovered_popup'):
                renpy.end_interaction(renpy.run(Return()))
                return
            if renpy.get_screen('ell_world_pc'):
                test_capture('pc')
                if not ell_world_bulletin_read:
                    test_click('ell_world_pc', 'world_pc_read')
                elif world_test_pc_view == 0:
                    s.world_test_pc_view = 1
                    test_click('ell_world_pc', 'world_pc_tab_routine')
                elif world_test_pc_view == 1:
                    test_capture('pc-routines')
                    s.world_test_pc_view = 2
                    test_click('ell_world_pc', 'world_pc_tab_journal')
                else:
                    test_capture('pc-journal')
                    test_click('ell_world_pc', 'world_pc_close')
                return
            if renpy.get_screen('inventory_menu'):
                test_capture('inventory')
                renpy.end_interaction(renpy.run(Return()))
                return
            if renpy.get_screen('ell_world_map'):
                test_capture('map')
                if not ell_world_tutorial_active and not world_test_map_locks_checked:
                    test_check('locked forest button disabled', not renpy.get_widget('ell_world_map', 'world_destination_forest').is_sensitive())
                    test_check('closed school button disabled', not renpy.get_widget('ell_world_map', 'world_destination_school_gate').is_sensitive())
                    s.world_test_map_locks_checked = True
                target = world_test_target
                s.world_test_target = None
                test_click('ell_world_map', 'world_destination_' + target if target else 'world_map_back')
                return
            if renpy.get_screen('ell_world_wait'):
                wait_id = 'world_wait_back' if world_test_wait_cancel else 'world_wait_next' if world_test_wait_lunch else 'world_wait_60'
                s.world_test_wait_cancel = False
                s.world_test_wait_lunch = False
                test_click('ell_world_wait', wait_id)
                return
            if renpy.get_screen('ell_world_help'):
                if world_test_help_cancel:
                    s.world_test_help_cancel = False
                    test_click('ell_world_help', 'world_help_back')
                    return
                s.world_test_replayed = True
                test_click('ell_world_help', 'world_replay')
                return
            if not renpy.get_screen('ell_world_room'):
                return
            if ell_world_tutorial_active:
                key = ELL_WORLD_TUTORIAL[ell_world_tutorial_step][0]
                test_capture('tutorial-' + key)
                if world_test_replayed:
                    test_click('ell_world_room', 'world_tutorial_skip')
                elif key == 'time':
                    marker = test_os.path.join(config.basedir, 'save-marker')
                    if not test_os.path.exists(marker):
                        renpy.save('day2-roundtrip')
                        with open(marker, 'w') as stream:
                            stream.write('saved')
                        s.ell_world_minutes = 999
                        s.ell_world_location = 'park'
                        renpy.load('day2-roundtrip')
                        return
                    if not world_test_loaded:
                        test_check('real save/load restores tutorial, place and clock', ell_world_minutes == 425 and ell_world_location == 'bedroom' and ell_world_tutorial_step == 4)
                        s.world_test_loaded = True
                    test_click('ell_world_room', 'world_tutorial_next')
                else:
                    action = {'welcome': 'world_tutorial_next', 'map': 'world_map', 'inventory': 'world_inventory', 'pc': 'world_hotspot_pc', 'door': 'world_hotspot_travel', 'finish': 'world_tutorial_next'}[key]
                    test_click('ell_world_room', action)
                return
            test_capture('room-' + ell_world_location)
            if world_test_unchanged_clock >= 0:
                test_check(world_test_unchanged_name + ' preserves clock and location', ell_world_minutes == world_test_unchanged_clock and ell_world_location == world_test_unchanged_location)
                s.world_test_unchanged_clock = -1
            if ell_day == 3:
                test_check('actual tutorial completed', ell_world_tutorial_complete)
                test_check('actual classes completed', 'day2_school_day' in ell_completed_quests)
                test_check('actual NPC conversations occurred', world_test_stage >= 18)
                test_check('new day preserves items', inventory.has_item('uniform_top') and inventory.has_item('uniform_skirt') and inventory.has_item('uniform_shoes'))
                test_check('new day preserves collectibles', {'existing_plush', 'cat_plush_1'} <= persistent.plushies_found and {'existing_frame', 'picture1'} <= persistent.picture_frames_found)
                test_check('Akari dream follow-up restricted to female route', day2_hana_dream_discussed == (mc_gender == 'female'))
                renpy.run(Jump('_world_test_complete'))
                return
            plan = (
                ('pause', None),
                ('map_cancel', None), ('wait_cancel', None), ('help_cancel', None),
                ('travel', 'kitchen'), ('talk', 'hana'), ('talk_repeat', 'hana'), ('breakfast', None),
                ('map', 'school_gate'), ('travel', 'school_corridor'), ('talk', 'rika'),
                ('travel', 'classroom'), ('class', None), ('travel', 'school_corridor'),
                ('travel', 'courtyard'), ('talk', 'aria'), ('wait_lunch', None),
                ('travel', 'school_corridor'), ('travel', 'classroom'), ('class', None),
                ('travel', 'school_corridor'), ('travel', 'library'), ('talk', 'mimi'),
                ('map', 'park'), ('talk', 'kuroe'), ('map', 'hallway'),
                ('travel', 'bedroom'), ('cat', None), ('frame', None), ('help', None),
            )
            if world_test_stage < len(plan):
                action, target = plan[world_test_stage]
                s.world_test_stage += 1
                if action in ('map_cancel', 'wait_cancel', 'help_cancel', 'talk_repeat'):
                    s.world_test_unchanged_clock = ell_world_minutes
                    s.world_test_unchanged_location = ell_world_location
                    s.world_test_unchanged_name = action
                if action in ('map', 'map_cancel'):
                    s.world_test_target = target
                    widget = 'world_map'
                elif action in ('travel', 'breakfast', 'class'):
                    widget = 'world_action_{}_{}'.format(action, target)
                elif action in ('talk', 'talk_repeat'):
                    widget = 'world_npc_' + target
                elif action == 'cat':
                    widget = 'world_collect_cat'
                elif action == 'frame':
                    widget = 'world_collect_picture1'
                elif action in ('help', 'help_cancel'):
                    s.world_test_help_cancel = (action == 'help_cancel')
                    widget = 'world_help'
                elif action == 'pause':
                    widget = 'world_pause'
                else:
                    s.world_test_wait_cancel = (action == 'wait_cancel')
                    widget = 'world_wait'
                # Wait to 13:00 after lunch; future waits advance by one hour.
                if action == 'wait_lunch':
                    s.world_test_wait_lunch = True
                test_click('ell_world_room', widget)
            elif ell_world_minutes < 1260:
                test_click('ell_world_room', 'world_wait')
            else:
                test_click('ell_world_room', 'world_action_rest_None')
        except (renpy.display.core.EndInteraction, renpy.game.JumpException, renpy.game.FullRestartException):
            raise
        except Exception:
            import traceback
            with open(test_os.path.join(config.basedir, 'test-error.txt'), 'w') as stream:
                traceback.print_exc(file=stream)
            renpy.quit(status=1, save=False)

screen _world_test_driver():
    zorder 1000
    timer 0.15 repeat True action Function(test_drive)

label _world_test_start:
    $ test_model()
    $ set_mc_gender(test_os.environ['ELL_TEST_GENDER'])
    $ day1_ensure_characters()
    $ inventory.add_item('uniform_top', notify=False)
    $ inventory.add_item('uniform_skirt', notify=False)
    $ inventory.add_item('uniform_shoes', notify=False)
    $ persistent.plushies_found = {'existing_plush'}
    $ persistent.picture_frames_found = {'existing_frame'}
    $ day1_akari_dream_seen = (mc_gender == 'female')
    $ renpy.exports.say = test_say
    $ store.menu = test_menu
    jump day1_end_of_intro

label _world_test_complete:
    python:
        with open(test_os.path.join(config.basedir, 'results.json'), 'w') as stream:
            test_json.dump({'checks': test_checks, 'screenshots': sorted(test_captures)}, stream, indent=2)
    $ renpy.quit(status=0, save=False)
'''


def snapshot(source, target):
    for path in source.rglob('*'):
        relative = path.relative_to(source)
        if any(p in {'cache', 'saves', '__pycache__'} for p in relative.parts):
            continue
        if path.suffix in {'.rpyc', '.rpymc', '.bak', '.old', '.new', '.pyc', '.pyo'}:
            continue
        dest = target / relative
        if path.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix in {'.rpy', '.rpym', '.py'}:
                shutil.copy2(path, dest)
            else:
                try:
                    os.link(path, dest)
                except OSError:
                    shutil.copy2(path, dest)


def run_hidden(command, env):
    """Keep the native renderer's test window hidden on Windows."""
    kwargs = {}
    if os.name == 'nt':
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = 0
        kwargs.update(startupinfo=info, creationflags=subprocess.CREATE_NO_WINDOW)
    process = subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, **kwargs)
    if os.name == 'nt':
        def hide_windows():
            import ctypes
            from ctypes import wintypes
            user32 = ctypes.windll.user32
            callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
            def visit(window, unused):
                owner = wintypes.DWORD()
                user32.GetWindowThreadProcessId(window, ctypes.byref(owner))
                if owner.value == process.pid:
                    user32.ShowWindow(window, 0)
                return True
            callback = callback_type(visit)
            while process.poll() is None:
                user32.EnumWindows(callback, 0)
                threading.Event().wait(0.1)
        threading.Thread(target=hide_windows, daemon=True).start()
    try:
        stdout, stderr = process.communicate(timeout=55)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        raise RuntimeError('RenPy test timed out.\n' + stdout[-2000:] + stderr[-2000:])
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sdk', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    sdk = args.sdk.resolve()
    root = Path(__file__).resolve().parents[1]
    for gender in ('female', 'male'):
        with tempfile.TemporaryDirectory(prefix='ell-day2-' + gender + '-') as temp:
            project = Path(temp)
            snapshot(root / 'game', project / 'game')
            start = project / 'game/scripts/script.rpy'
            text = start.read_text(encoding='utf-8-sig')
            start.write_text(text.replace('label start:\n', 'label start:\n    jump _world_test_start\n', 1), encoding='utf-8')
            (project / 'game/zz_world_test.rpy').write_text(HARNESS, encoding='utf-8')
            env = dict(os.environ, PYTHONFAULTHANDLER='1', ELL_TEST_GENDER=gender, SDL_VIDEODRIVER='windows', SDL_AUDIODRIVER='dummy', RENPY_RENDERER='gl2', RENPY_DISABLE_SOUND='1', RENPY_SKIP_SPLASHSCREEN='1', RENPY_SKIP_MAIN_MENU='1')
            try:
                completed = run_hidden([str(sdk / 'lib/py3-windows-x86_64/python.exe'), str(sdk / 'renpy.py'), str(project), '--savedir', str(project / 'isolated-saves'), 'run'], env)
                (project / 'test-process.txt').write_text(completed.stdout + '\n' + completed.stderr, encoding='utf-8')
                result = project / 'results.json'
                if completed.returncode or not result.exists():
                    print('RenPy process exit:', completed.returncode)
                    print(completed.stdout[-3000:])
                    print(completed.stderr[-2000:])
                    for name in ('test-error.txt', 'errors.txt', 'traceback.txt'):
                        path = project / name
                        if path.exists():
                            print(path.read_text(encoding='utf-8-sig')[-8000:])
                    raise SystemExit('Day 2 checks failed for ' + gender)
                report = json.loads(result.read_text())
                print('{}: passed {} checks; captured {} screens'.format(gender, len(report['checks']), len(report['screenshots'])))
            finally:
                if args.output:
                    destination = args.output / gender
                    destination.mkdir(parents=True, exist_ok=True)
                    # Retain reports and screenshots, without copying a gigabyte
                    # of the game's audio, movies and other linked test assets.
                    for artifact in project.iterdir():
                        if artifact.is_file() and artifact.suffix in {'.png', '.json', '.txt'}:
                            shutil.copy2(artifact, destination / artifact.name)


if __name__ == '__main__':
    main()
