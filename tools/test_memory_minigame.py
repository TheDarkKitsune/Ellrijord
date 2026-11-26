"""Run the memory game in isolated copies using the real Ren'Py engine.

python tools/test_memory_minigame.py --sdk ../renpy-8.5.1-sdk --output /path/to/results
Optional --baseline compares lint with a pre-change project snapshot.
"""

import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import sys
import tempfile
import zlib

sys.dont_write_bytecode = True
from test_day2_exploration import snapshot, run_hidden


HARNESS = r'''
define config.default_fullscreen = False
define config.sound = False
define config.autosave_on_choice = False
define config.autosave_on_quit = False
define config.physical_width = 1280
define config.physical_height = 720
define config.image_cache_size_mb = 64
default memory_test_stage = 0
default memory_test_round = 0
default memory_test_pause_seen = False
default memory_test_ui_save_seen = False
default memory_test_extra = 0
default memory_test_menu_ticks = 0
default memory_test_complete_ticks = 0
default memory_test_clock = 0
default memory_test_board = None

init 999 python:
    config.default_fullscreen = False
    import json as mt_json
    import os as mt_os
    from collections import Counter as mt_counter
    memory_test_checks = []
    memory_test_captures = set()
    config.overlay_screens.append('_memory_test_driver')

    def mt_ensure_driver():
        if not renpy.get_screen('_memory_test_driver'):
            renpy.show_screen('_memory_test_driver')
    config.interact_callbacks.append(mt_ensure_driver)

    def mt_check(name, condition):
        if not condition:
            raise AssertionError(name)
        memory_test_checks.append(name)

    def mt_capture(name):
        if name not in memory_test_captures:
            screen = next(renpy.get_screen(n) for n in ('save', 'showmenu', 'ell_memory_instructions', 'ell_memory_restart_confirm', 'ellrijord_memory_screen', 'ell_memory_setup', 'ell_minigames_menu', 'ell_world_pc') if renpy.get_screen(n))
            renpy.render_to_file(screen, name + '.png', width=1920, height=1080, resize=True)
            memory_test_captures.add(name)

    def mt_click(screen, widget_id):
        widget = renpy.get_widget(screen, widget_id)
        if widget is None or not widget.is_sensitive():
            raise AssertionError('Missing or disabled {} on {}'.format(widget_id, screen))
        renpy.display.screen.push_current_screen(renpy.get_screen(screen))
        try:
            result = renpy.run(widget.clicked)
        finally:
            renpy.display.screen.pop_current_screen()
        if result is not None:
            renpy.end_interaction(result)

    def mt_state():
        g = ell_memory_game
        return (g.cards, g.opened, g.matched, g.moves, g.locked, getattr(g, 'turning', ()), g.started_runtime, g.finished_seconds)

    def mt_model():
        for difficulty_id, caption, columns, rows in ELL_MEMORY_DIFFICULTIES:
            enabled = columns * rows // 2 <= 15
            mt_check(difficulty_id + ' deck capacity', ell_memory_can_play(difficulty_id) == enabled)
            if enabled:
                g = EllrijordMemory(difficulty_id)
                mt_check(difficulty_id + ' dimensions and pairs', (g.columns, g.rows) == (columns, rows) and len(g.cards) == columns * rows and all(n == 2 for n in mt_counter(g.cards).values()))
                mt_check(difficulty_id + ' rollback-safe immutable fields', isinstance(g.cards, tuple) and isinstance(g.opened, tuple) and isinstance(g.matched, tuple))
                a = 0
                b = next(i for i in range(1, len(g.cards)) if g.cards[i] != g.cards[a])
                g.flip(-1)
                g.flip(len(g.cards))
                mt_check(difficulty_id + ' invalid indices ignored', not g.opened and g.moves == 0)
                g.flip(a)
                g.flip(a)
                mt_check(difficulty_id + ' duplicate flip ignored', g.opened == (a,) and g.moves == 0)
                g.flip(b)
                before = (g.opened, g.moves)
                g.flip(next(i for i in range(len(g.cards)) if i not in (a, b)))
                mt_check(difficulty_id + ' mismatch locks input', g.locked and (g.opened, g.moves) == before)
                g.hide()
                for card in set(g.cards):
                    indices = [i for i, value in enumerate(g.cards) if value == card]
                    g.flip(indices[0])
                    g.flip(indices[1])
                mt_check(difficulty_id + ' completion and result', g.complete and g.result()['status'] == 'completed' and g.moves == g.pairs + 1)
                before = g.moves
                g.flip(0)
                mt_check(difficulty_id + ' matched flip ignored', g.moves == before)
            else:
                try:
                    EllrijordMemory(difficulty_id)
                except ValueError:
                    mt_check(difficulty_id + ' construction refused', True)
                else:
                    raise AssertionError('Undersized deck accepted')
        mt_check('unknown configurations rejected', not ell_memory_can_play('bad') and not ell_memory_can_play('easy', 'bad') and not ell_memory_can_play('easy', mode='time_attack'))
        artwork = mt_os.environ['ELL_MEMORY_ART'] == '1'
        mt_check('artwork or placeholder path', bool(ell_memory_art('tsuki_plushies', 'front')) == artwork and bool(ell_memory_art('tsuki_plushies', 'illustration', 'plush_01')) == artwork)
        old_bests = persistent.ell_memory_bests
        try:
            persistent.ell_memory_bests = {}
            sample = dict(minigame_id='tsuki_memory', status='abandoned', deck='tsuki_plushies', difficulty='easy', mode='classic', moves=6, elapsed_seconds=20)
            ell_memory_record_result(sample)
            mt_check('abandon never records a personal best', not persistent.ell_memory_bests)
            sample['status'] = 'completed'
            ell_memory_record_result(sample)
            sample['elapsed_seconds'] = 25
            ell_memory_record_result(sample)
            mt_check('slower tie preserves personal best', ell_memory_best('tsuki_plushies', 'easy')['elapsed_seconds'] == 20)
            sample['elapsed_seconds'] = 15
            ell_memory_record_result(sample)
            mt_check('faster tie improves personal best', ell_memory_best('tsuki_plushies', 'easy')['elapsed_seconds'] == 15)
            sample['difficulty'] = 'normal'
            ell_memory_record_result(sample)
            mt_check('personal bests separated by difficulty', len(persistent.ell_memory_bests) == 2)
        finally:
            persistent.ell_memory_bests = old_bests
        mt_check('clock formatting', ell_memory_time(125) == '02:05')
        old_game = EllrijordMemory('easy')
        old_cards = old_game.cards
        for attribute in ('started_runtime', 'finished_seconds', 'turning', 'reaction'):
            delattr(old_game, attribute)
        old_game.prepare()
        mt_check('prototype save fields migrate without reshuffling', old_game.cards == old_cards and old_game.elapsed == 0 and not old_game.turning and old_game.reaction == 'ready')

    def mt_roundtrip(name):
        marker = mt_os.path.join(config.basedir, name + '-loaded')
        if not mt_os.path.exists(marker):
            expected = mt_state()
            renpy.save('memory-' + name)
            with open(marker, 'w') as stream:
                mt_json.dump(expected, stream)
            ell_memory_game.hide()
            ell_memory_game.moves = 999
            renpy.store.ell_world_location = 'park'
            renpy.store.ell_world_minutes = 999
            renpy.load('memory-' + name)
            return False
        with open(marker) as stream:
            expected = mt_json.load(stream)
        mt_check(name + ' real save/load restores exact board and counters', mt_json.loads(mt_json.dumps(mt_state())) == expected)
        mt_check(name + ' save/load preserves world', ell_world_location == 'bedroom' and ell_world_minutes == 615)
        return True

    def mt_drive():
        s = renpy.store
        try:
            if renpy.get_screen('ell_memory_instructions'):
                mt_capture('instructions')
                s.memory_test_menu_ticks += 1
                if memory_test_menu_ticks < 12:
                    return
                mt_check('instructions pause game timer', ell_memory_game.elapsed == memory_test_clock)
                mt_click('ell_memory_instructions', 'memory_instructions_back')
                return
            if renpy.get_screen('ell_memory_restart_confirm'):
                mt_capture('restart-confirmation')
                mt_click('ell_memory_restart_confirm', 'memory_restart_no' if memory_test_extra == 3 else 'memory_restart_yes')
                return
            if renpy.get_screen('save'):
                mt_capture('save-menu')
                s.memory_test_ui_save_seen = True
                renpy.end_interaction(renpy.run(Return()))
                return
            if renpy.get_screen('showmenu'):
                mt_capture('pause-menu')
                s.memory_test_pause_seen = True
                renpy.end_interaction(renpy.run(Return()))
                return
            if renpy.get_screen('ell_world_pc'):
                if memory_test_stage == 0:
                    mt_check('PC entry unavailable during tutorial', not renpy.get_widget('ell_world_pc', 'world_pc_minigames').is_sensitive())
                    # A save made inside the old PC label has no new parameter.
                    del s._pc_tab
                    s.ell_world_bulletin_read = True
                    s.ell_world_tutorial_active = False
                    s.memory_test_stage = 1
                    renpy.end_interaction('bulletin')
                elif memory_test_stage == 1:
                    mt_check('old PC label state tolerates missing tab local', renpy.get_screen('ell_world_pc').scope['pc_tab'] == 'bulletin')
                    s.memory_test_stage = 11
                    mt_click('ell_world_pc', 'world_pc_tab_journal')
                elif memory_test_stage == 11:
                    s.memory_test_stage = 2
                    mt_capture('pc-entry')
                    mt_click('ell_world_pc', 'world_pc_minigames')
                else:
                    mt_check('PC restored after hub exit', memory_test_stage == 20 and ell_world_location == 'bedroom' and ell_world_minutes == 615)
                    mt_check('previous PC tab restored', renpy.get_screen('ell_world_pc').scope['pc_tab'] == 'journal')
                    mt_click('ell_world_pc', 'world_pc_close')
                return
            if renpy.get_screen('ell_minigames_menu'):
                mt_capture('minigame-menu')
                if memory_test_round in (2, 3, 4):
                    expected = {2: ('easy', 6), 3: ('normal', 8), 4: ('hard', 12)}[memory_test_round]
                    mt_check(expected[0] + ' completed result returned through hub', ell_minigame_last_result['status'] == 'completed' and ell_minigame_last_result['difficulty'] == expected[0] and ell_minigame_last_result['pairs_found'] == expected[1] and ell_minigame_last_result['moves'] == expected[1] + 1)
                    mt_check(expected[0] + ' actual completed game records best', ell_memory_best('tsuki_plushies', expected[0])['moves'] == expected[1] + 1)
                if memory_test_round == 5:
                    s.memory_test_stage = 20
                    mt_click('ell_minigames_menu', 'minigame_back')
                else:
                    mt_click('ell_minigames_menu', 'minigame_tsuki_memory')
                return
            if renpy.get_screen('ell_memory_setup'):
                mt_capture('difficulty-menu')
                mt_check('larger difficulty buttons disabled', not renpy.get_widget('ell_memory_setup', 'memory_difficulty_expert').is_sensitive() and not renpy.get_widget('ell_memory_setup', 'memory_difficulty_tsuki').is_sensitive())
                if memory_test_round == 0:
                    mt_check('setup cancellation has no result', ell_minigame_last_result is None)
                    s.memory_test_round = 1
                    mt_click('ell_memory_setup', 'minigame_back')
                else:
                    difficulty = {1: 'easy', 2: 'normal', 3: 'hard', 4: 'easy'}[memory_test_round]
                    s.memory_test_stage = 3
                    mt_click('ell_memory_setup', 'memory_difficulty_' + difficulty)
                return
            if not renpy.get_screen('ellrijord_memory_screen'):
                return
            g = ell_memory_game
            mt_check('quick menu hidden in board', not quick_menu)
            if memory_test_round == 7:
                if memory_test_extra == 0:
                    s.memory_test_extra = 1
                    s.memory_test_clock = g.elapsed
                    mt_click('ellrijord_memory_screen', 'memory_instructions')
                elif memory_test_extra == 1:
                    mt_check('instructions restore board and clock', not g.opened and g.moves == 0 and g.elapsed == memory_test_clock)
                    s.memory_test_extra = 2
                    mt_click('ellrijord_memory_screen', 'memory_card_0')
                elif memory_test_extra == 2:
                    s.memory_test_board = mt_state()
                    s.memory_test_extra = 3
                    mt_click('ellrijord_memory_screen', 'memory_restart')
                elif memory_test_extra == 3:
                    mt_check('restart cancellation preserves card state', mt_state()[:5] == memory_test_board[:5])
                    s.memory_test_extra = 4
                    mt_click('ellrijord_memory_screen', 'memory_restart')
                elif memory_test_extra == 4:
                    mt_check('restart resets board and timer', not g.opened and not g.matched and not g.locked and g.moves == 0 and g.elapsed == 0)
                    s.memory_test_extra = 5
                elif memory_test_extra == 5:
                    if g.elapsed < 1:
                        return
                    mt_check('Classic timer advances while playing', g.elapsed >= 1)
                    mt_capture('restarted-board')
                    mt_click('ellrijord_memory_screen', 'minigame_back')
                return
            if memory_test_round == 6:
                marker = mt_os.path.join(config.basedir, 'rollback-phase')
                phase = open(marker).read() if mt_os.path.exists(marker) else 'initial'
                if phase == 'initial':
                    with open(marker, 'w') as stream:
                        stream.write('flipped')
                    mt_click('ellrijord_memory_screen', 'memory_card_0')
                elif phase == 'flipped':
                    with open(marker, 'w') as stream:
                        stream.write('rolled-back')
                    mt_check('real rollback is available after flip', renpy.can_rollback())
                    renpy.rollback(force=True, checkpoints=1, greedy=False)
                else:
                    mt_check('real rollback restores pre-flip board', not g.opened and not g.matched and g.moves == 0)
                    mt_click('ellrijord_memory_screen', 'minigame_back')
                return
            if memory_test_round == 5:
                mt_click('ellrijord_memory_screen', 'minigame_back')
                return
            if memory_test_round == 4:
                if not g.opened:
                    mt_click('ellrijord_memory_screen', 'memory_card_0')
                    return
                s.memory_test_round = 5
                mt_click('ellrijord_memory_screen', 'minigame_back')
                return
            if memory_test_stage == 3:
                mt_capture('board-' + g.difficulty_id)
                s.memory_test_stage = 4
                mt_click('ellrijord_memory_screen', 'memory_card_0')
                return
            if memory_test_stage == 4:
                if not mt_roundtrip('one-card-' + g.difficulty_id):
                    return
                s.memory_test_stage = 5
                mt_click('ellrijord_memory_screen', 'memory_card_' + str(next(i for i in range(1, len(g.cards)) if g.cards[i] != g.cards[0])))
                return
            if memory_test_stage == 5:
                if not mt_roundtrip('mismatch-' + g.difficulty_id):
                    return
                mt_check('loaded mismatch still locked', g.locked and len(g.opened) == 2)
                mt_capture('mismatch-' + g.difficulty_id)
                s.memory_test_stage = 6
                return
            if memory_test_stage == 6:
                if g.locked:
                    return
                mt_check('mismatch timer recovers after load', not g.opened)
                s.memory_test_stage = 7
                mt_click('ellrijord_memory_screen', 'minigame_pause')
                return
            if memory_test_stage == 7:
                mt_check('pause menu returned to board', memory_test_pause_seen)
                s.memory_test_stage = 8
                mt_click('ellrijord_memory_screen', 'minigame_save')
                return
            if memory_test_stage == 8:
                mt_check('save menu returned to board', memory_test_ui_save_seen)
                s.memory_test_stage = 9
            if g.complete:
                s.memory_test_complete_ticks += 1
                if memory_test_complete_ticks < 3:
                    return
                mt_check('completed clock is frozen', g.elapsed == g.finished_seconds)
                mt_capture('completed-' + g.difficulty_id)
                if not mt_roundtrip('complete-' + g.difficulty_id):
                    return
                mt_check('complete board stable after load', g.complete)
                s.memory_test_round += 1
                s.memory_test_complete_ticks = 0
                mt_click('ellrijord_memory_screen', 'minigame_back')
                return
            # Match one pair through the actual card actions, then round-trip it.
            if g.matched and memory_test_stage == 9:
                if not mt_roundtrip('matched-' + g.difficulty_id):
                    return
                s.memory_test_stage = 10
            if g.opened:
                index = next(i for i, card in enumerate(g.cards) if card == g.cards[g.opened[0]] and i not in g.opened and i not in g.matched)
            else:
                index = next(i for i in range(len(g.cards)) if i not in g.matched)
            mt_click('ellrijord_memory_screen', 'memory_card_' + str(index))
        except (renpy.display.core.EndInteraction, renpy.game.JumpException, renpy.game.FullRestartException):
            raise
        except Exception:
            import traceback
            with open(mt_os.path.join(config.basedir, 'test-error.txt'), 'w') as stream:
                traceback.print_exc(file=stream)
            renpy.quit(status=1, save=False)

screen _memory_test_driver():
    zorder 1000
    timer 0.12 repeat True action Function(mt_drive)

label _memory_test_start:
    $ _preferences.fullscreen = False
    $ renpy.set_physical_size((1280, 720))
    $ mt_model()
    $ ell_day = 1
    call ellrijord_memory
    $ mt_check('direct entry blocked on Day 1', _return is None and ell_memory_game is None)
    call ell_minigames
    $ mt_check('hub entry blocked on Day 1', _return is None)
    $ ell_day = 2
    $ ell_world_location = 'bedroom'
    $ ell_world_minutes = 615
    $ ell_world_sync_time()
    $ ell_world_tutorial_active = True
    $ persistent.plushies_found = {'existing-plush'}
    $ persistent.picture_frames_found = {'existing-frame'}
    $ inventory.add_item('uniform_top', notify=False)
    $ memory_test_quick_menu = quick_menu
    call ell_world_use_pc
    $ mt_check('quick menu restored after nested calls', quick_menu == memory_test_quick_menu)
    $ mt_check('abandon result distinguished from win', ell_minigame_last_result['status'] == 'abandoned' and ell_minigame_last_result['moves'] == 0)
    $ mt_check('active board cleaned up', ell_memory_game is None)
    $ mt_check('collectibles and inventory preserved', persistent.plushies_found == {'existing-plush'} and persistent.picture_frames_found == {'existing-frame'} and inventory.has_item('uniform_top'))
    # Also test direct calls from a location outside the PC/hub.
    $ ell_world_location = 'courtyard'
    $ quick_menu = False
    call ellrijord_memory('normal')
    $ mt_check('direct call restores location and disabled quick menu', ell_world_location == 'courtyard' and not quick_menu)
    $ memory_test_round = 6
    call ellrijord_memory('easy')
    $ memory_test_round = 7
    call ellrijord_memory('easy')
    python:
        with open(mt_os.path.join(config.basedir, 'results.json'), 'w') as stream:
            mt_json.dump({'checks': memory_test_checks, 'screenshots': sorted(memory_test_captures)}, stream, indent=2)
    $ renpy.quit(status=0, save=False)
'''


def fixture_png(path, color):
    """Solid RGBA fixtures exercise compositing at the designer's source size."""
    path.parent.mkdir(parents=True, exist_ok=True)

    def chunk(kind, data):
        return struct.pack('!I', len(data)) + kind + data + struct.pack('!I', zlib.crc32(kind + data))

    pixels = (b'\0' + bytes(color) * 400) * 560
    # The snapshot hard-links runtime art. Break that link before writing a
    # fixture so testing can never overwrite the working game's PNGs.
    if path.exists():
        path.unlink()
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!2I5B', 400, 560, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(pixels)) + chunk(b'IEND', b''))


def lint(command, project, env):
    compiled = run_hidden(command + [str(project), '--savedir', str(project / 'isolated-saves'), 'compile'], env)
    (project / 'compile.txt').write_text(compiled.stdout + compiled.stderr, encoding='utf-8')
    if compiled.returncode:
        raise RuntimeError('RenPy compile failed:\n' + compiled.stdout[-6000:] + compiled.stderr[-2000:])
    result = run_hidden(command + [str(project), '--savedir', str(project / 'isolated-saves'), 'lint'], env)
    output = result.stdout + result.stderr
    (project / 'lint.txt').write_text(output, encoding='utf-8')
    if result.returncode:
        raise RuntimeError('RenPy lint failed:\n' + output[-6000:])
    # Strip the version/date banner and final statistics before comparison.
    warnings = re.split(r'\nStatistics:', result.stdout)[0]
    warnings = re.sub(r'^.*(?:Ren.Py|lint report).*\n', '', warnings, flags=re.MULTILINE)
    warnings = re.sub(r'(\.rpy):\d+', r'\1:<line>', warnings)
    return collections.Counter(block.strip() for block in warnings.split('\n\n') if block.strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sdk', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--baseline', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[1]
    day1_hash = hashlib.sha256((root / 'game/scripts/day1_intro.rpy').read_bytes()).hexdigest()
    command = [str(args.sdk.resolve() / 'lib/py3-windows-x86_64/python.exe'), str(args.sdk.resolve() / 'renpy.py')]
    env = dict(os.environ, PYTHONFAULTHANDLER='1', SDL_VIDEODRIVER='windows', SDL_AUDIODRIVER='dummy', RENPY_RENDERER='gl2', RENPY_DISABLE_SOUND='1', RENPY_SKIP_SPLASHSCREEN='1', RENPY_SKIP_MAIN_MENU='1')
    baseline_warnings = lint(command, args.baseline, env) if args.baseline else None
    for artwork in ('installed-art', 'art-fixtures', 'missing-card-art'):
        name = artwork
        with tempfile.TemporaryDirectory(prefix='ell-memory-' + name + '-') as temp:
            project = Path(temp)
            snapshot(root / 'game', project / 'game')
            destination = args.output / name
            destination.mkdir(parents=True, exist_ok=True)
            try:
                if artwork == 'installed-art':
                    warnings = lint(command, project, env)
                    if baseline_warnings is not None:
                        added = list((warnings - baseline_warnings).elements())
                        removed = list((baseline_warnings - warnings).elements())
                        comparison = {'added': added, 'removed': removed}
                        (project / 'lint-comparison.json').write_text(json.dumps(comparison, indent=2), encoding='utf-8')
                        if added:
                            raise AssertionError('New lint warnings:\n' + '\n\n'.join(added))
                    print('RenPy lint completed' + ('; no new warnings' if baseline_warnings is not None else ''), flush=True)
                if artwork == 'missing-card-art':
                    art = project / 'game/images/minigames/memory/tsuki_plushies'
                    for path in art.rglob('*.png'):
                        if not path.resolve().is_relative_to(project.resolve()):
                            raise AssertionError('Test asset escaped its isolated project')
                        path.unlink()
                if artwork == 'art-fixtures':
                    art = project / 'game/images/minigames/memory/tsuki_plushies'
                    for layer, color in [('front', (50, 45, 85, 230)), ('back', (95, 55, 115, 230)), ('highlight', (255, 220, 100, 50))]:
                        fixture_png(art / (layer + '.png'), color)
                    for index in range(1, 16):
                        fixture_png(art / 'illustrations' / ('plush_{:02d}.png'.format(index)), (index * 14, 130, 180, 200))
                start = project / 'game/scripts/script.rpy'
                source = start.read_text(encoding='utf-8-sig')
                start.write_text(source.replace('label start:\n', 'label start:\n    jump _memory_test_start\n', 1), encoding='utf-8')
                (project / 'game/zz_memory_test.rpy').write_text(HARNESS, encoding='utf-8')
                result = run_hidden(command + [str(project), '--savedir', str(project / 'isolated-saves'), 'run'], dict(env, ELL_MEMORY_ART='0' if artwork == 'missing-card-art' else '1'))
                (project / 'test-process.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
                if result.returncode or not (project / 'results.json').exists():
                    for filename in ('test-error.txt', 'errors.txt', 'traceback.txt', 'test-process.txt'):
                        path = project / filename
                        if path.exists():
                            print(path.read_text(encoding='utf-8-sig')[-7000:])
                    raise RuntimeError('RenPy memory checks failed: ' + name)
                report = json.loads((project / 'results.json').read_text())
                print('{}: passed {} assertions ({} distinct); captured {} screens'.format(name, len(report['checks']), len(set(report['checks'])), len(report['screenshots'])), flush=True)
            finally:
                for path in project.iterdir():
                    if path.is_file() and path.suffix in {'.png', '.json', '.txt'}:
                        shutil.copy2(path, destination / path.name)
    if hashlib.sha256((root / 'game/scripts/day1_intro.rpy').read_bytes()).hexdigest() != day1_hash:
        raise AssertionError('Day 1 changed while tests ran')


if __name__ == '__main__':
    main()
