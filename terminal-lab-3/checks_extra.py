"""Checks saved evidence without extracting archives or executing their contents."""
import json
import re
import tarfile
import zipfile
from lab_process import live


def extend(root, check, read, expected):
    def values(name):
        pairs=[line.split('=',1) for line in read(name).splitlines() if line.strip()]
        out=dict(pairs)
        if len(out)!=len(pairs): raise ValueError('Duplicate key')
        return out
    def memory():
        rows=read('work/memory.txt').splitlines()
        header=rows[0].split()
        row=next(x.split()[1:] for x in rows if x.startswith('Mem:'))
        swap=next(x.split()[1:] for x in rows if x.startswith('Swap:'))
        return dict(zip(header,row)),swap
    def memory_ok():
        m,sw=memory()
        return set(m)=={'total','used','free','shared','buff/cache','available'} and len(sw)==3 and all(re.fullmatch(r'\d+(?:\.\d+)?(?:[KMGTPE]i|B)?',v) for v in [*m.values(),*sw])
    def memory_map():
        m,sw=memory();v=values('work/system.txt')
        return v['memory_total']==m['total'] and v['memory_available']==m['available'] and v['swap_total']==sw[0]
    def uptime():
        match=re.search(r' up (.+?),\s*\d+ users?,\s*load average[s]?:\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)',read('work/uptime.txt'))
        if not match: raise ValueError('Keep full uptime output')
        return match.groups()
    def uptime_map():
        return all(values('work/system.txt')[k]==v for k,v in zip(['uptime_elapsed','load_1','load_5','load_15'],uptime()))
    def record(): return json.loads(read('work/process.json'))
    def ps_row(name):
        rows=read(name).strip().splitlines()
        if len(rows)!=2 or rows[0].split()!=['PID','STAT','COMMAND']: raise ValueError('ps header/row')
        return rows[1].split(None,2)
    def process_ok(name):
        r=record();p=ps_row(name)
        return p[0]==str(r['pid']) and 'lab_process.py worker '+r['token'] in p[2] and p[1][0] in 'RSDIT'
    def process_map():
        p=ps_row('work/process-before.txt');v=values('work/process-notes.txt')
        return v['pid']==p[0] and v['state']==p[1] and v['command']==p[2]
    def top_ok():
        text=read('work/top.txt');r=record()
        return 'top -' in text and '%CPU' in text and '%MEM' in text and re.search(r'^\s*'+str(r['pid'])+r'\s',text,re.M) is not None
    def top_notes():
        v=values('work/process-notes.txt')
        return all(re.fullmatch(r'\d+(?:\.\d+)?',v[k]) for k in ['top_cpu_first','top_cpu_later','top_mem_percent']) and re.fullmatch(r'\d+(?:\.\d+)?[kKmMgGtT]?',v['top_res'])
    def stopped():
        r=record();e=json.loads(read('work/process-exit.json'))
        return not live(r) and e=={'token':r['token'],'pid':r['pid'],'reason':'SIGTERM'}
    def after(): return read('work/process-after.txt').split()==['PID','STAT','COMMAND']
    def members(prefix): return {n:b for n,b in expected.items() if n.startswith(prefix+'/')}
    def zip_ok(file,prefix):
        p=root/file
        if p.is_symlink(): return False
        try:
            with zipfile.ZipFile(p) as z:
                entries=[i for i in z.infolist() if not i.is_dir()]
                return len(entries)==len(members(prefix)) and {i.filename:z.read(i) for i in entries}==members(prefix)
        except (zipfile.BadZipFile,RuntimeError): return False
    def extracted(folder,prefix):
        base=root/folder
        paths=list(base.rglob('*'))
        return not base.is_symlink() and not any(p.is_symlink() for p in paths) and {str(p.relative_to(base)):p.read_bytes() for p in paths if p.is_file()}==members(prefix)
    def listing(file,prefix):
        text=read(file)
        return all(name in text for name in members(prefix))
    def tar_ok(file,prefix,mode):
        p=root/file
        if p.is_symlink(): return False
        try:
            with tarfile.open(p,mode) as t:
                entries=[i for i in t if not i.isdir()]
                return all(i.isfile() for i in entries) and len(entries)==len(members(prefix)) and {i.name:t.extractfile(i).read() for i in entries}==members(prefix)
        except tarfile.TarError:return False
    def compression_sizes():
        rows=read('work/archive-sizes.txt').splitlines()
        from check import du_rows, run
        return du_rows('\n'.join(rows))==du_rows(run(root,'du','-h','work/bundle.tar','work/bundle.tar.gz')) and (root/'work/bundle.tar.gz').stat().st_size < (root/'work/bundle.tar').stat().st_size
    check('E2 memory snapshot',memory_ok,'Save the whole free -h output to work/memory.txt.')
    check('E2 memory columns',memory_map,'Use Mem total/available and Swap total from your saved snapshot.')
    check('E2 uptime snapshot',lambda: bool(uptime()),'Save the complete uptime line to work/uptime.txt.')
    check('E2 uptime and load interpretation',uptime_map,'Copy elapsed uptime and the 1, 5 and 15 minute loads into system.txt.')
    check('E3 designated process snapshot',lambda:process_ok('work/process-before.txt'),'Use ps -p with the current helper PID and -o pid,stat,args.')
    check('E3 PID, state and command',process_map,'Copy all three fields from process-before.txt to process-notes.txt.')
    check('E4 top snapshot',top_ok,'Save top -b -n 1 -p PID to work/top.txt while the worker is running.')
    check('E4 written readings present',top_notes,'Record two CPU readings, RES and %MEM. Your instructor checks them against your live observation.')
    check('E5 identity rechecked',lambda:process_ok('work/process-confirm.txt'),'Save a fresh ps row just before kill, matching the helper token.')
    check('E5 designated worker terminated',stopped,'Use ordinary kill only on the confirmed live worker. Timeout is not a completed stop.')
    check('E5 no remaining process row',after,'After stopping, save the same ps selection to work/process-after.txt; only the header should remain.')
    for kind,prefix,archive,dest,lst,diff in [
        ('guided','practice/dispatch','work/dispatch.zip','work/unzipped','work/zip-list.txt','work/zip-diff.txt'),
        ('independent','challenge/dispatch','work/magazine.zip','work/magazine-out','work/magazine-list.txt','work/magazine-diff.txt')]:
        check('E6 '+kind+' ZIP contents',lambda a=archive,p=prefix:zip_ok(a,p),'Include the entire named folder with zip -r, including nested files.')
        check('E6 '+kind+' ZIP listing',lambda l=lst,p=prefix:listing(l,p),'Save unzip -l output; inspect every expected path.')
        check('E6 '+kind+' extracted files',lambda d=dest,p=prefix:extracted(d,p),'Extract into the named separate work/ folder; compare with the originals.')
        check('E6 '+kind+' comparison report',lambda d=diff:read(d)=='','Save diff -r output after extraction. No output means no differences found.')
    check('E7 uncompressed tar contents',lambda:tar_ok('work/bundle.tar','practice/compress','r:'),'Create tar -cf with both compression samples.')
    check('E7 compressed tar contents',lambda:tar_ok('work/bundle.tar.gz','practice/compress','r:gz'),'Create tar -czf; renaming a .tar file does not compress it.')
    check('E7 archive listings',lambda:listing('work/tar-list.txt','practice/compress') and listing('work/targz-list.txt','practice/compress'),'Save tar -tf and tar -tzf listings.')
    check('E7 extracted files',lambda:extracted('work/tar-out','practice/compress'),'Extract bundle.tar.gz with -xzf into work/tar-out.')
    check('E7 comparison report',lambda:read('work/tar-diff.txt')=='','Save diff -r after extraction; verify the output is empty.')
    check('E7 measured archive sizes',compression_sizes,'Save du -h for both complete archive paths; compare with units.')
    check('E7 independent archive',lambda:tar_ok('work/magazine.tar.gz','challenge/dispatch','r:gz'),'Package the challenge dispatch folder as a compressed tar archive.')
