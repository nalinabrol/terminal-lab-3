#!/usr/bin/env python3
"""Read-only formative feedback, not proof of independent work or understanding."""
import os
from pathlib import Path
import re
import subprocess
import sys
from setup import originals, valid_id

ENV = dict(os.environ, LC_ALL='C')
GUIDED = ['practice/notices', 'practice/posters', 'practice/recordings']
CHALLENGE = ['challenge/design', 'challenge/notes', 'challenge/interviews']

def run(root, *args):
    return subprocess.check_output(args, cwd=root, env=ENV, text=True).strip()

def human(value):
    m = re.fullmatch(r'(\d+(?:\.\d+)?)([KMGTPEZY]?)', value)
    if not m:
        raise ValueError('Not a human-readable storage value')
    return float(m[1]) * 1024 ** ('KMGTPEZY'.index(m[2]) + 1 if m[2] else 0)

def du_rows(text):
    result = {}
    for line in text.splitlines():
        size, path = line.split()
        if path in result:
            raise ValueError('Duplicate folder')
        human(size)
        result[path] = size
    return result

def df_row(text):
    lines = text.splitlines()
    if len(lines) != 2 or lines[0].split() != ['Filesystem','Size','Used','Avail','Use%','Mounted','on']:
        raise ValueError('Keep the df -h . header and data row')
    row = lines[1].split()
    if len(row) != 6:
        raise ValueError('Expected one filesystem row')
    total, used, available = map(human, row[1:4])
    if total <= 0 or used > total * 1.11 or available > total * 1.11:
        raise ValueError('Implausible capacity fields')
    if not re.fullmatch(r'\d+%', row[4]) or not 0 <= int(row[4][:-1]) <= 100:
        raise ValueError('Expected a percentage from 0% to 100%')
    return row

def evaluate(root):
    root = Path(root).resolve()
    results = []
    def check(label, predicate, hint):
        try:
            ok = bool(predicate())
        except (OSError, ValueError, KeyError, IndexError, subprocess.SubprocessError):
            ok = False
        results.append((ok, label, hint))
    def read(name):
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ValueError('Expected a regular result file')
        return path.read_text()
    try:
        ident = dict(line.split('=',1) for line in read('identity.txt').splitlines())
        lab_id = ident['LAB_ID']
        if not valid_id(lab_id):
            raise ValueError('Invalid lab ID')
        expected = originals(lab_id)
    except (OSError, ValueError, KeyError):
        return [(False, 'Lab identity', 'Run from your lab root; ask for help if identity.txt changed.')]
    def preserved():
        actual = {str(p.relative_to(root)) for d in ['practice','challenge'] for p in (root/d).rglob('*') if p.is_file() or p.is_symlink()}
        names = set(expected) - {'identity.txt'}
        return actual == names and all(not (root/n).is_symlink() and (root/n).read_bytes() == b for n,b in expected.items())
    def obs():
        lines = read('work/observations.txt').splitlines()
        pairs = [line.split('=',1) for line in lines if line.strip()]
        result = dict(pairs)
        if len(pairs) != len(result):
            raise ValueError('Duplicate observation key')
        return result
    def measured(file, paths):
        return du_rows(read(file)) == du_rows(run(root,'du','-sh',*paths))
    def df_valid():
        saved = df_row(read('work/filesystem.txt'))
        live = df_row(run(root,'df','-h','.'))
        # Capacity usage changes with time. Only identity/mount must still agree.
        return saved[0] == live[0] and saved[5] == live[5]
    def mapped():
        row = df_row(read('work/filesystem.txt'))
        keys = ['filesystem_size','filesystem_used','filesystem_available','filesystem_use_percent','filesystem_mounted_on']
        return all(obs()[key] == val for key,val in zip(keys,row[1:]))
    def copy_growth():
        before = du_rows(read('work/copy-before.txt'))
        after = du_rows(read('work/copy-after.txt'))
        path = 'work/copy-target'
        return set(before) == {path} and set(after) == {path} and human(before[path]) < human(after[path]) and after == du_rows(run(root,'du','-sh',path))
    check('Original evidence preserved',preserved,'Keep identity.txt, practice/ and challenge/ unchanged; ask for help restoring originals.')
    check('Three guided folder measurements',lambda: measured('work/guided-usage.txt',GUIDED),'Save all three du -sh output lines with sizes, units and paths.')
    check('Largest guided folder',lambda: obs()['guided_largest'] == 'recordings','Compare units as well as numbers; enter only the folder name.')
    check('Filesystem snapshot',df_valid,'Save df -h . from the lab root, including its header; do not invent fixed values.')
    check('Filesystem columns interpreted',mapped,'Copy Size, Used, Avail, Use% and Mounted on from your saved snapshot to the matching keys.')
    check('Working copy preserved',lambda: not (root/'work/copy-target/recording.bin').is_symlink() and (root/'work/copy-target/recording.bin').read_bytes() == expected['practice/recordings/recording.bin'],'Copy the named recording into work/copy-target; leave the original intact.')
    check('Copy before and after evidence',copy_growth,'Measure the empty target before copying and again afterwards; do not replace the before snapshot on a rerun.')
    check('Three independent folder measurements',lambda: measured('work/challenge-usage.txt',CHALLENGE),'Measure each challenge folder and save the three output lines.')
    check('Largest independent folder',lambda: obs()['challenge_largest'] == 'interviews','Use your challenge report to select a folder; enter only its name.')
    return results

def main():
    results = evaluate(Path.cwd())
    for ok,label,hint in results:
        print(('PASS  ' if ok else 'CHECK ') + label)
        if not ok:
            print('      ' + hint)
    passed = sum(ok for ok,_,_ in results)
    print(f'\n{passed}/{len(results)} file checks passed.')
    print('Read-only feedback: nothing repaired, uploaded or submitted.')
    print('Your predictions, explanations and command choices need instructor review.')
    return 0 if passed == len(results) else 1

if __name__ == '__main__':
    sys.exit(main())
