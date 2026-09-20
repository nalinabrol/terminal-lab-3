#!/usr/bin/env python3
"""Launch one bounded lab worker per attempt. No signal is sent by this helper."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import uuid


def live(record):
    try:
        p = Path('/proc') / str(record['pid'])
        fields = (p/'stat').read_text().rsplit(')',1)[1].split()
        args = (p/'cmdline').read_bytes().split(b'\0')
        return fields[0] != 'Z' and fields[19] == record['start_ticks'] and record['token'].encode() in args
    except (OSError, KeyError, IndexError):
        return False


def main():
    root=Path.cwd()
    if len(sys.argv)>1 and sys.argv[1]=='worker':
        token=sys.argv[2]
        marker=root/'work/process-exit.json'
        def finish(reason):
            marker.write_text(json.dumps({'token':token,'pid':os.getpid(),'reason':reason})+'\n')
            sys.exit(0)
        signal.signal(signal.SIGTERM,lambda *_:finish('SIGTERM'))
        payload=bytearray(8*1024*1024)
        deadline=time.monotonic()+3600
        while time.monotonic()<deadline:
            payload[0]=(payload[0]+1)%256
            time.sleep(.2)
        finish('timeout')
    if not (root/'identity.txt').is_file() or not (root/'work').is_dir():
        sys.exit('Run this helper from your lab root.')
    record_path=root/'work/process.json'
    action=sys.argv[1] if len(sys.argv)>1 else 'status'
    if action not in ('start','status'):
        sys.exit('Use start or status.')
    if record_path.exists():
        record=json.loads(record_path.read_text())
        if live(record):
            print(f"RUNNING: designated LAB3 worker PID {record['pid']} token {record['token']}")
            return
        print('STOPPED: the recorded worker is no longer running. Do not reuse its PID.')
        print('Keep this evidence. For another process attempt, use a new lab ID.')
        return
    if action=='status':
        sys.exit('No worker yet. Run the helper with start.')
    token='LAB3-'+uuid.uuid4().hex[:12]
    child=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'worker',token],cwd=root,
        stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
    ticks=(Path('/proc')/str(child.pid)/'stat').read_text().rsplit(')',1)[1].split()[19]
    record={'pid':child.pid,'token':token,'start_ticks':ticks}
    record_path.write_text(json.dumps(record)+'\n')
    # Allow signal handler installation before returning to the student.
    time.sleep(.15)
    print(f"RUNNING: designated LAB3 worker PID {child.pid} token {token}")
    print('Uses about 8 MiB of data, mostly waits, and expires after one hour.')
    print('Inspect with ps; only this exact current worker may be stopped in Experiment 5.')

if __name__=='__main__':
    main()
