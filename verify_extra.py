"""Instructor-only automation of the later experiments and adversarial feedback."""
import json
from pathlib import Path
import re
import subprocess
import sys
import time


def solve(root, command, capture):
    from verify_lab import ROOT
    helper=str(ROOT/'terminal-lab-3/lab_process.py')
    mem=capture(root,'work/memory.txt','free','-h')
    rows=mem.splitlines();m=dict(zip(rows[0].split(),rows[1].split()[1:]));sw=rows[2].split()[1:]
    up=capture(root,'work/uptime.txt','uptime')
    fields=re.search(r' up (.+?),\s*\d+ users?,\s*load average[s]?:\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)',up).groups()
    values={'memory_total':m['total'],'memory_available':m['available'],'swap_total':sw[0]}
    values.update(zip(['uptime_elapsed','load_1','load_5','load_15'],fields))
    (root/'work/system.txt').write_text(''.join(f'{k}={v}\n' for k,v in values.items()))
    command(root,sys.executable,helper,'start')
    rec=json.loads((root/'work/process.json').read_text());pid=str(rec['pid'])
    command(root,sys.executable,helper,'start')
    assert json.loads((root/'work/process.json').read_text())==rec,'Duplicate worker on rerun'
    ps=capture(root,'work/process-before.txt','ps','-p',pid,'-o','pid,stat,args')
    fields=ps.splitlines()[1].split(None,2)
    top=capture(root,'work/top.txt','top','-b','-n','1','-p',pid)
    top_row=next(l.split() for l in top.splitlines() if l.split() and l.split()[0]==pid)
    values=dict(zip(['pid','state','command'],fields))
    values.update(top_cpu_first=top_row[8],top_cpu_later=top_row[8],top_res=top_row[5],top_mem_percent=top_row[9])
    (root/'work/process-notes.txt').write_text(''.join(f'{k}={v}\n' for k,v in values.items()))
    capture(root,'work/process-confirm.txt','ps','-p',pid,'-o','pid,stat,args')
    subprocess.run(['kill',pid],check=True)
    for _ in range(30):
        result=subprocess.run(['ps','-p',pid,'-o','pid,stat,args'],text=True,capture_output=True)
        if len(result.stdout.strip().splitlines())==1:break
        time.sleep(.1)
    (root/'work/process-after.txt').write_text(result.stdout)
    command(root,sys.executable,helper,'status')
    command(root,sys.executable,helper,'start')
    assert json.loads((root/'work/process.json').read_text())==rec,'Stopped worker replaced'
    for prefix,archive,dest,lst,diff in [
        ('practice/dispatch','work/dispatch.zip','work/unzipped','work/zip-list.txt','work/zip-diff.txt'),
        ('challenge/dispatch','work/magazine.zip','work/magazine-out','work/magazine-list.txt','work/magazine-diff.txt')]:
        command(root,'zip','-r',archive,prefix)
        capture(root,lst,'unzip','-l',archive)
        command(root,'unzip',archive,'-d',dest)
        capture(root,diff,'diff','-r',prefix,dest+'/'+prefix)
    command(root,'tar','-cf','work/bundle.tar','practice/compress')
    capture(root,'work/tar-list.txt','tar','-tf','work/bundle.tar')
    command(root,'tar','-czf','work/bundle.tar.gz','practice/compress')
    capture(root,'work/targz-list.txt','tar','-tzf','work/bundle.tar.gz')
    capture(root,'work/archive-sizes.txt','du','-h','work/bundle.tar','work/bundle.tar.gz')
    (root/'work/tar-out').mkdir()
    command(root,'tar','-xzf','work/bundle.tar.gz','-C','work/tar-out')
    capture(root,'work/tar-diff.txt','diff','-r','practice/compress','work/tar-out/practice/compress')
    command(root,'tar','-czf','work/text.tar.gz','practice/compress/repeated.txt')
    command(root,'tar','-czf','work/noise.tar.gz','practice/compress/noise.bin')
    assert (root/'work/text.tar.gz').stat().st_size < (root/'work/noise.tar.gz').stat().st_size
    command(root,'tar','-czf','work/magazine.tar.gz','challenge/dispatch')
    command(root,'tar','-tzf','work/magazine.tar.gz')


def wrong_cases(root, evaluate):
    paths=[
        (9,'memory.txt'),(10,'system.txt'),(11,'uptime.txt'),(12,'system.txt'),
        (13,'process-before.txt'),(14,'process-notes.txt'),(15,'top.txt'),(16,'process-notes.txt'),
        (17,'process-confirm.txt'),(18,'process-exit.json'),(19,'process-after.txt'),
        (20,'dispatch.zip'),(21,'zip-list.txt'),(22,'unzipped/practice/dispatch/notice.txt'),(23,'zip-diff.txt'),
        (24,'magazine.zip'),(25,'magazine-list.txt'),(26,'magazine-out/challenge/dispatch/brief.txt'),(27,'magazine-diff.txt'),
        (28,'bundle.tar'),(29,'bundle.tar.gz'),(30,'tar-list.txt'),(31,'tar-out/practice/compress/repeated.txt'),
        (32,'tar-diff.txt'),(33,'archive-sizes.txt'),(34,'magazine.tar.gz')]
    for index,name in paths:
        p=root/'work'/name;good=p.read_bytes();p.write_bytes(b'wrong\n')
        try: assert not evaluate(root)[index][0],(index,name)
        finally:p.write_bytes(good)
    # Correct archive type matters, not extension. Reject valid ZIP with missing nested file.
    import zipfile
    p=root/'work/dispatch.zip';good=p.read_bytes()
    with zipfile.ZipFile(p,'w') as z:z.writestr('practice/dispatch/notice.txt',(root/'practice/dispatch/notice.txt').read_bytes())
    assert not evaluate(root)[20][0]
    p.write_bytes(good)
    p=root/'work/bundle.tar.gz';good=p.read_bytes();p.write_bytes((root/'work/bundle.tar').read_bytes())
    assert not evaluate(root)[29][0]
    p.write_bytes(good)
    # Valid record structure but timeout is not evidence of SIGTERM.
    p=root/'work/process-exit.json';good=p.read_bytes();r=json.loads(good);r['reason']='timeout';p.write_text(json.dumps(r))
    assert not evaluate(root)[18][0]
    p.write_bytes(good)
