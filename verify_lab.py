#!/usr/bin/env python3
"""Instructor validation in temporary attempts only; no student work is changed."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zlib

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'terminal-lab-3'))
import setup
import check

ENV = dict(os.environ, LC_ALL='C')

def command(root, *args):
    return subprocess.check_output(args, cwd=root, env=ENV, text=True)

def capture(root, file, *args):
    out = command(root, *args)
    (root / file).write_text(out)
    return out

def snapshot(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}

def solve(root):
    command(root,'pwd')
    command(root,'cat','identity.txt')
    command(root,'ls')
    command(root,'cat','practice/README.txt')
    command(root,'ls','practice')
    command(root,'ls','practice/recordings')
    capture(root,'work/guided-usage.txt','du','-sh',*check.GUIDED)
    command(root,'cat','work/guided-usage.txt')
    command(root,'df','-h','.')
    fs=capture(root,'work/filesystem.txt','df','-h','.')
    command(root,'cat','work/filesystem.txt')
    command(root,'du','-sh','.')
    command(root,'df','-h','.')
    command(root,'ls','work/copy-target')
    capture(root,'work/copy-before.txt','du','-sh','work/copy-target')
    subprocess.run(['cp','practice/recordings/recording.bin','work/copy-target/'],cwd=root,check=True)
    capture(root,'work/copy-after.txt','du','-sh','work/copy-target')
    command(root,'cat','work/copy-before.txt','work/copy-after.txt')
    command(root,'du','-sh','practice/recordings')
    command(root,'du','-sh','.')
    command(root,'df','-h','.')
    command(root,'cat','challenge/brief.txt')
    command(root,'ls','challenge')
    capture(root,'work/challenge-usage.txt','du','-sh',*check.CHALLENGE)
    command(root,'df','-h','.')
    row=check.df_row(fs)
    keys=['filesystem_size','filesystem_used','filesystem_available','filesystem_use_percent','filesystem_mounted_on']
    lines=['guided_largest=recordings']+[f'{k}={v}' for k,v in zip(keys,row[1:])]+['challenge_largest=interviews']
    (root/'work/observations.txt').write_text('\n'.join(lines)+'\n')
    command(root,'cat','work/observations.txt')

def main():
    if sys.platform != 'linux':
        sys.exit('Run validation in Linux (Codespace or CI): GNU df header/layout is required.')
    for lab_id in ['A017','B104','C233','student-42']:
        with tempfile.TemporaryDirectory(prefix='book3-verify-') as d:
            root=setup.create(lab_id,Path(d)/('lab3-'+lab_id))
            initial=check.evaluate(root)
            assert len(initial)==9 and sum(ok for ok,_,_ in initial)==1, initial
            for relative in setup.PAYLOADS:
                p=root/relative
                assert p.stat().st_blocks*512 >= p.stat().st_size, 'Sparse payload'
                assert len(zlib.compress(p.read_bytes())) > p.stat().st_size*.99, 'Compressible payload'
            solve(root)
            results=check.evaluate(root)
            assert len(results)==9 and all(ok for ok,_,_ in results), results
            before=snapshot(root)
            subprocess.run([sys.executable,str(ROOT/'terminal-lab-3/check.py')],cwd=root,check=True,stdout=subprocess.DEVNULL)
            assert snapshot(root)==before, 'Checker changed files'
            # Each feedback item is independently falsifiable.
            cases=[
                ('practice/notices/notices.bin',b'changed',0),
                ('work/guided-usage.txt',b'1K\tpractice/notices\n',1),
                ('work/observations.txt',(root/'work/observations.txt').read_bytes().replace(b'guided_largest=recordings',b'guided_largest=posters'),2),
                ('work/filesystem.txt',b'wrong header\n',3),
                ('work/observations.txt',(root/'work/observations.txt').read_bytes().replace(b'filesystem_available=',b'filesystem_available=wrong'),4),
                ('work/copy-target/recording.bin',b'incomplete',5),
                ('work/copy-before.txt',(root/'work/copy-after.txt').read_bytes(),6),
                ('work/challenge-usage.txt',b'1K\tchallenge/design\n',7),
                ('work/observations.txt',(root/'work/observations.txt').read_bytes().replace(b'challenge_largest=interviews',b'challenge_largest=notes'),8),
            ]
            for name,bad,index in cases:
                p=root/name; good=p.read_bytes();p.write_bytes(bad)
                assert not check.evaluate(root)[index][0], (name,index)
                p.write_bytes(good)
            p=root/'work/guided-usage.txt';good=p.read_bytes();p.unlink()
            assert not check.evaluate(root)[1][0], 'Missing report accepted'
            p.write_bytes(good)
            p=root/'practice/extra.txt';p.write_text('extra')
            assert not check.evaluate(root)[0][0], 'Added original accepted'
            p.unlink()
            p=root/'work/copy-target/recording.bin';good=p.read_bytes();p.unlink()
            p.symlink_to(root/'practice/recordings/recording.bin')
            # A symbolic link is not a student copy.
            assert not check.evaluate(root)[5][0], 'Symbolic link accepted as copy'
            p.unlink();p.write_bytes(good)
            try:
                setup.create(lab_id,root)
            except FileExistsError:
                pass
            else:
                raise AssertionError('Existing attempt overwritten')
            assert snapshot(root)==before, 'Repeat setup changed an attempt'
            assert all(ok for ok,_,_ in check.evaluate(root))
            print(f'PASS {lab_id}: 9/9, nine targeted failures, missing/extra/link cases, read-only check, rerun preservation, payload allocation/compression')
    for value in ['', '../escape','/tmp/escape','a b','-bad','a'*25]:
        assert not setup.valid_id(value), value
    print('PASS invalid IDs rejected; all stage-1 runtime checks passed.')

if __name__=='__main__':
    main()
