#!/usr/bin/env python3
"""Small deterministic synthetic exports. Never overwrite an existing attempt."""
import hashlib
import re
import shlex
import sys
from pathlib import Path

DATA_VERSION = 'book3-v2'
LEGACY_VERSION = 'book3-stage1-v1'
PAYLOADS = {
    'practice/notices/notices.bin': 64 * 1024,
    'practice/posters/posters.bin': 768 * 1024,
    'practice/recordings/recording.bin': 4 * 1024 * 1024,
    'challenge/design/design.bin': 2 * 1024 * 1024,
    'challenge/notes/notes.bin': 256 * 1024,
    'challenge/interviews/interviews.bin': 6 * 1024 * 1024,
}
TEMPLATE = '''guided_largest=
filesystem_size=
filesystem_used=
filesystem_available=
filesystem_use_percent=
filesystem_mounted_on=
challenge_largest=
'''

def valid_id(value):
    return re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,23}', value) is not None

def originals(lab_id, version=DATA_VERSION):
    if not valid_id(lab_id):
        raise ValueError('Use 1-24 letters/digits, hyphens or underscores; begin with a letter/digit.')
    files = {'identity.txt': f'LAB_ID={lab_id}\nDATA_VERSION={version}\n'.encode()}
    files['practice/README.txt'] = b'''Campus event storage audit: notices, posters and recordings.
The .bin files are synthetic stand-ins for stored exports, not playable media.
Use du to measure their folders. Do not display binary files with cat or nano.
Keep practice/ and challenge/ unchanged. Save results and copies in work/.
'''
    files['challenge/brief.txt'] = b'''The student magazine team has design, notes and interviews folders.
Measure each folder and identify the largest storage user.
Save a three-line du -sh report as work/challenge-usage.txt.
Record the largest folder name in work/observations.txt.
Explain which command would check available space before another export.
Keep all original evidence unchanged. No files need to be removed.
'''
    for name, size in PAYLOADS.items():
        # Write every byte; SHAKE output is reproducible and hard to compress.
        files[name] = hashlib.shake_256((LEGACY_VERSION + '/' + name).encode()).digest(size)
    if version == DATA_VERSION:
        files.update({
            'practice/dispatch/notice.txt': b'Campus showcase\nDoors open at 10:00.\n',
            'practice/dispatch/lists/rooms.csv': b'activity,room\nRobotics,Lab-2\nDesign,Hall-1\n',
            'practice/dispatch/notes.txt': b'Keep the room list with this notice.\n',
            'challenge/dispatch/brief.txt': b'Magazine handover: send both the brief and the nested credits file.\n',
            'challenge/dispatch/team/credits.txt': b'Editor: Ada\nDesign: Lin\n',
            'practice/compress/repeated.txt': (b'Keep a verified copy of the campus event records.\n' * 2048),
            'practice/compress/noise.bin': hashlib.shake_256(b'book3-compression').digest(98304),
        })
    elif version != LEGACY_VERSION:
        raise ValueError('Unknown data version')
    return files

def create(lab_id, destination):
    files = originals(lab_id)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    for name, data in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (destination / 'work/copy-target').mkdir(parents=True)
    (destination / 'work/observations.txt').write_text(TEMPLATE)
    (destination / 'work/system.txt').write_text('memory_total=\nmemory_available=\nswap_total=\nuptime_elapsed=\nload_1=\nload_5=\nload_15=\n')
    (destination / 'work/process-notes.txt').write_text('pid=\ncommand=\nstate=\ntop_cpu_first=\ntop_cpu_later=\ntop_res=\ntop_mem_percent=\n')
    return destination

def main():
    lab_id = input('Enter your instructor-assigned lab ID (not your email): ').strip()
    if not valid_id(lab_id):
        sys.exit('Invalid ID. Use 1-24 letters/digits, hyphens or underscores; begin with a letter/digit.')
    base = Path(__file__).resolve().parent.parent / 'lab-work'
    if base.is_symlink():
        sys.exit('lab-work is a symbolic link. Ask your instructor for help.')
    destination = base / ('lab3-' + lab_id)
    if destination.is_symlink():
        sys.exit('This attempt is a symbolic link. Ask your instructor for a new ID.')
    try:
        create(lab_id, destination)
        print('Created your seven-experiment workspace.')
    except FileExistsError:
        if not destination.is_dir():
            sys.exit('The attempt path is not a folder. Ask your instructor for help.')
        print('This attempt already exists. All files have been preserved; nothing was reset.')
    print('\nEnter your lab folder with this exact command:')
    print('cd ' + shlex.quote(str(destination)))
    print('Then run: pwd')
    print('Then run: cat identity.txt')
    print('Follow Experiment Book 3. Older stage-1 attempts stay unchanged; use a new ID for the full book.')

if __name__ == '__main__':
    main()
