from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'Experiment_Book_3.pdf'
TEXT = ROOT/'Experiment_Book_3.md'
FONT = Path('/System/Library/Fonts/Supplemental')
font_files=[('Body','Arial.ttf'),('Bold','Arial Bold.ttf'),('Italic','Arial Italic.ttf'),('Mono','Courier New.ttf')]
if not (FONT/'Arial.ttf').exists():
    FONT=Path('/usr/share/fonts/truetype/dejavu')
    font_files=[('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Italic','DejaVuSans-Oblique.ttf'),('Mono','DejaVuSansMono.ttf')]
for name,file in font_files:
    pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
GREEN_DARK=colors.HexColor('#0E6A50'); MINT=colors.HexColor('#18CB96'); INK=colors.HexColor('#373643'); GRAY=colors.HexColor('#55526A'); PALE=colors.HexColor('#EAFAF4'); LINE=colors.HexColor('#B7D9CC')
styles={
 'body': ParagraphStyle('body',fontName='Body',fontSize=10.3,leading=14.1,textColor=INK,spaceAfter=6),
 'small': ParagraphStyle('small',fontName='Body',fontSize=9.1,leading=12.2,textColor=GRAY,spaceAfter=5),
 'h': ParagraphStyle('h',fontName='Bold',fontSize=12,leading=15,textColor=GREEN_DARK,spaceBefore=12,spaceAfter=6),
 'title': ParagraphStyle('title',fontName='Bold',fontSize=23,leading=27,textColor=GREEN_DARK,spaceAfter=9),
 'kicker': ParagraphStyle('kicker',fontName='Bold',fontSize=9,leading=12,textColor=GREEN_DARK,spaceAfter=8),
 'code': ParagraphStyle('code',fontName='Mono',fontSize=9.1,leading=12.3,textColor=INK,spaceAfter=0),
 'table': ParagraphStyle('table',fontName='Body',fontSize=9,leading=11.9,textColor=INK),
}
W=511.27
story=[]; md=[]
class Lines(Flowable):
 def __init__(self,n=1): Flowable.__init__(self); self.width=W;self.height=n*20;self.n=n
 def draw(self):
  self.canv.setStrokeColor(LINE);self.canv.setLineWidth(.5)
  self.canv.setDash(2, 3)
  for i in range(self.n):self.canv.line(12,self.height-16-i*20,W-12,self.height-16-i*20)
  self.canv.setDash()

def para(s,kind='body'):
 story.append(Paragraph(s,styles[kind]));md.append(('# ' if kind == 'title' else '## ' if kind == 'h' else '') + s.replace('<b>','**').replace('</b>','**').replace('<br/>','\n'))
def h(s):para(s,'h')
def code(s):
 p=Paragraph(escape(s).replace(' ','&#160;').replace('\n','<br/>'),styles['code'])
 box=Table([[p]],colWidths=[W]);box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.4,LINE),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
 story.extend([box,Spacer(1,7)]);md.append('```bash\n'+s+'\n```')
def lines(label,n=1):
 para(label,'small')
 if n:
  story.append(Lines(n));md.append('_' * 65 + '\n')
 story.append(Spacer(1,10 if n == 0 else 3))
def table(rows,widths,compact=False):
 cells=[[Paragraph(escape(c).replace('\n','<br/>'),styles['table']) for c in row] for row in rows]
 t=Table(cells,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),PALE),('LINEBELOW',(0,0),(-1,0),.6,LINE),('LINEBELOW',(0,1),(-1,-1),.3,LINE),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),3 if compact else 6),('BOTTOMPADDING',(0,0),(-1,-1),3 if compact else 6)]));story.extend([t,Spacer(1,7)]);md.append('\n'.join([' | '.join(rows[0]), ' | '.join(['---']*len(rows[0]))] + [' | '.join(row) for row in rows[1:]]))
def page(kicker,title):
 if story:story.append(PageBreak());md.append('\n---\n')
 para(kicker,'kicker');para(title,'title')
def step(label,text):para('<b>'+label+'</b> '+text)
def start():para('<b>Start:</b> your lab root - the absolute path you wrote on page 1. Begin each experiment here unless instructed otherwise.','small')

page('LAB 3 / TERMINAL TOOLS', 'Experiment Book 3')
para('Storage, memory, processes and archives | Bash in GitHub Codespaces')
lines('Name: __________________________  Lab ID: ______________  Section: __________',0)
para('Prepare a campus event handover. Measure storage, inspect a running program, stop a designated lab process, and package files so another person can recover them.')
h('Get ready')
para('Sign in with your own GitHub account. Open this link and create a Codespace on <b>main</b>. Later, resume the same Codespace to keep working.')
para('<link href="https://codespaces.new/nalinabrol/terminal-lab-3?quickstart=1" color="#0E6A50"><u>https://codespaces.new/nalinabrol/terminal-lab-3?quickstart=1</u></link>','small')
para('Wait for setup. Choose <b>Trust Folder &amp; Continue</b> if asked. A Bash terminal opens. If needed, use <b>Lab 3: Focus Bash Terminal</b> in the Command Palette. At the repository root, run:')
code('bash terminal-lab-3/start.sh')
para('Enter your assigned lab ID, not your email. Run the exact <b>cd</b> command printed by setup. Then run:')
code('pwd\ncat identity.txt\nls')
lines('My lab root (the complete path from pwd):',1)
table([['Location','Purpose'],['practice/ and challenge/','Original evidence. Keep it unchanged.'],['work/','Your reports, notes, copies and archives.']], [165,W-165])
para('<b>Start every experiment at your lab root.</b> Type commands one at a time. Predict, run, inspect and explain. Write in this book or a separate notes file. Hints are on page 14; the command reference is on page 15.')
para('Setup preserves an existing attempt, including mistakes. Use a new ID for a fresh attempt. Old stage-1 attempts remain unchanged. In nano, save with <b>Ctrl+O, Enter</b>; exit with <b>Ctrl+X</b> or <b>F2</b> if the browser intercepts Ctrl+X. Use Control on a Mac too.','small')
para('Save changes before leaving. Files in lab-work/ are ignored by Git, not backed up to GitHub. Resume this Codespace; download your work when a separate copy is needed.','small')

page('EXPERIMENT 1 / A', 'Folder usage and free space')
para('The event team has notices, posters and recordings. Predict which folder uses the most storage, then measure it. The .bin files are synthetic exports, not playable media; do not open them in cat or nano.')
lines('My prediction and reason:',1)
code('du -sh practice/notices practice/posters practice/recordings\ndu -sh practice/notices practice/posters practice/recordings > work/guided-usage.txt')
para('<b>du</b> estimates allocated storage used by the named files and folders. <b>-s</b> gives one summary per path, including its contents; <b>-h</b> uses readable units. Here K, M and G increase in steps of 1,024. Compare units as well as numbers.')
lines('notices: __________  posters: __________  recordings: __________',0)
lines('Which is larger, 900K or 2.0M? Why?',1)
h('Read the containing filesystem')
code('df -h . > work/filesystem.txt\ncat work/filesystem.txt')
para('<b>df</b> reports filesystem space. The dot selects the filesystem containing your current folder; it does not add up just that folder. These readings describe the remote Linux environment, not your laptop.')
table([['Column','Meaning'],['Size / Used','Total filesystem capacity / space already used.'],['Avail / Use%','Available space / percentage used, not free.'],['Mounted on','Where the filesystem is attached to the directory tree.']], [130,W-130],True)
code('nano work/observations.txt')
para('Fill <b>guided_largest</b> with the folder name. Fill the five <b>filesystem_</b> fields from your saved df row, keeping units, the percent sign and full mount path. Leave challenge_largest for the next page.','small')
lines('Why does df Used include more than this lab folder?',1)

page('EXPERIMENT 1 / B', 'Make a copy and compare')
para('Predict what will change after copying one recording. The target starts empty. Run this sequence once; when resuming, read the saved reports instead of replacing the before measurement.')
lines('My prediction for du and df:',1)
code('ls work/copy-target\ndu -sh work/copy-target > work/copy-before.txt\ncp practice/recordings/recording.bin work/copy-target/\ndu -sh work/copy-target > work/copy-after.txt\ncat work/copy-before.txt work/copy-after.txt\ndu -sh practice/recordings\ndu -sh .\ndf -h .')
lines('Before: __________  After: __________  Evidence the original remains:',1)
para('An empty directory may occupy storage. A small copy can increase du while rounded df values look unchanged. Other activity can also change filesystem usage; Used + Avail need not exactly equal Size.')
h('Apply it independently')
para('Measure <b>challenge/design</b>, <b>challenge/notes</b> and <b>challenge/interviews</b> separately. Save their three du summaries as <b>work/challenge-usage.txt</b>. Fill <b>challenge_largest</b> in observations.txt with the largest folder name.')
lines('My command and largest folder, with its displayed size:',2)
para('The magazine team asks how much more it can save. Run the appropriate command, then record the column and its value.')
lines('Command: ____________________ Column and value: ____________________',0)
lines('A friend says "du -sh . tells me how much more I can save." Correct the claim.',2)

page('EXPERIMENT 2 / A', 'RAM is not disk space')
para('Disk storage holds saved files. RAM holds code and data used by running programs. Closing a program can release RAM without deleting its saved files. An archive needs disk space; opening it may also require memory.')
h('Read a memory snapshot')
code('free -h > work/memory.txt\ncat work/memory.txt\ndf -h .')
para('<b>free</b> reports memory; <b>-h</b> adds readable units such as Mi and Gi. Read the <b>Mem:</b> row for RAM and the <b>Swap:</b> row for swap. Swap is storage used to support memory management; it is not extra physical RAM.')
table([['Memory column','What it tells you'],['total','Usable RAM reported by the environment.'],['used / free','Memory in use / memory currently unused.'],['buff/cache','Memory used for buffers and caches; some can be reclaimed.'],['available','An estimate of memory available for new applications without swapping.']], [110,W-110])
para('A small free value alone does not prove a memory shortage: useful cached data occupies RAM too. Look at available. Swap total may be zero in this environment.')
code('nano work/system.txt')
para('Fill <b>memory_total</b> and <b>memory_available</b> from Mem, and <b>swap_total</b> from Swap in your saved snapshot. Keep each displayed unit. Leave the remaining fields for the next page.')
lines('My Mem total: __________  available: __________  Swap total: __________',0)
lines('Why can available be larger than free?',2)
para('Container readings can reflect the host kernel view and may differ from the Codespace resource limit. Do not treat free or top as a statement of your account quota. No fixed reading is expected.','small')

page('EXPERIMENT 2 / B', 'Uptime and load averages')
code('uptime > work/uptime.txt\ncat work/uptime.txt')
para('<b>uptime</b> shows the current time, elapsed system uptime, logged-in user count and three load averages. The averages cover the last <b>1, 5 and 15 minutes</b>, in that order. System uptime is not the time spent on this exercise.')
para('Load averages reflect runnable work and work in uninterruptible waits, often I/O. They are not CPU percentages. A value needs context, including the number of CPUs and the kind of waiting; it is not a pass/fail score for your Codespace.')
h('Interpret your snapshot')
code('nano work/system.txt')
para('Fill <b>uptime_elapsed</b> with the text after "up" and before the user count; omit the separating comma. Copy the three decimal values to <b>load_1</b>, <b>load_5</b> and <b>load_15</b>. Use your saved output even if a new run differs.')
lines('Elapsed uptime: _________________________________________________',0)
lines('1 minute: __________  5 minutes: __________  15 minutes: __________',0)
lines('Which average reflects the shortest interval? What might a higher 1-minute value than 15-minute value suggest?',2)
h('Apply it independently')
para('For each request, choose a command, run it and record one relevant reading. Explain your choice; the two readings describe different resources.')
table([['Request','Command and reading'],['Can I store another large video file?',''],['How much RAM may be available to another application?','']], [265,W-265])
lines('Why would a large df Avail value fail to answer the RAM question?',2)
lines('Is a load average of 2.00 the same as 2% CPU usage? Explain.',1)

page('EXPERIMENT 3', 'Programs, processes and PIDs')
para('A <b>program</b> is stored instructions. A <b>process</b> is a running instance. Linux assigns each process a numeric <b>PID</b>. The same program can have several processes with different PIDs.')
code('ps\npython3 ../../terminal-lab-3/lab_process.py start')
para('<b>ps</b> takes a process snapshot; plain ps normally selects processes of your user on this terminal. The supplied helper starts one designated worker for this attempt. It mostly waits, holds about 8 MiB of data and expires after one hour. Leave it running until Experiment 5.')
lines('Helper PID: ______________  LAB3 token: ___________________________',0)
para('In every command below, replace <b>PID</b> with the positive number printed by your helper. Do not type the word PID or use a classmate\'s number.')
code('ps -p PID -o pid,stat,args\nps -p PID -o pid,stat,args > work/process-before.txt\nnano work/process-notes.txt')
para('<b>-p</b> selects a PID; <b>-o</b> chooses columns. STAT is the state: S means sleeping/waiting, R means running or ready; extra letters add detail. COMMAND shows the program and its arguments. Fill <b>pid</b>, <b>state</b> and <b>command</b> from the saved row; keep the complete command text.')
lines('What in COMMAND identifies this as your designated lab worker?',1)
h('Apply it independently')
code('ps -e -o pid,comm')
para('<b>-e</b> selects all visible processes; comm is the short command name. Find a program name with more than one PID if one is present. Observe only; do not stop it.')
lines('Program and PIDs (or "none in this snapshot"):',1)
lines('Why is the program name alone insufficient to identify one process?',1)
para('Rerunning the helper while its worker is live reuses it. Once stopped or expired, preserve this attempt and use a new lab ID for another process exercise.','small')

page('EXPERIMENT 4', 'Watch CPU and memory with top')
para('<b>top</b> refreshes its display as processes run. The summary describes the system; each process row describes one process. Unlike a saved ps snapshot, the live screen changes.')
code('top')
para('Watch two refreshes. Press <b>Shift+P</b> to sort by CPU, then <b>Shift+M</b> to sort by memory. Identify the PID and COMMAND of a visible row. Press <b>q</b> to return to Bash. These keys act inside top.')
lines('A row I observed (PID and COMMAND):',1)
code('python3 ../../terminal-lab-3/lab_process.py status\ntop -p PID')
para('Replace PID with your worker\'s current number. Watch at least two refreshes. The worker should usually be idle; 0.0 CPU or rounded 0.0 memory is a valid observation.')
table([['Field','Meaning'],['%CPU','CPU usage over the sampling interval; not a load average.'],['RES','Resident memory held in physical RAM; read displayed units.'],['%MEM','Resident memory as a share of reported physical memory.'],['VIRT','Virtual address space; not the amount of physical RAM used.']], [100,W-100],True)
para('Record two %CPU readings, RES and %MEM in the spaces below. Press q, then enter them in <b>work/process-notes.txt</b> as <b>top_cpu_first</b>, <b>top_cpu_later</b>, <b>top_res</b> and <b>top_mem_percent</b>. Use numeric CPU/%MEM values without a percent sign.')
lines('CPU first: ______ later: ______  RES: ______ (unit: _____)  %MEM: ______',0)
code('top -b -n 1 -p PID > work/top.txt')
para('<b>-b</b> produces text output; <b>-n 1</b> limits it to one snapshot. Keep the interactive observations too: a batch report cannot show that you used the live controls.','small')
lines('Apply: choose top or ps to watch a changing process list. Why?',1)
lines('Does a sleeping process with 0.0 CPU use no memory? Explain.',1)

page('EXPERIMENT 5', 'Stop only the lab worker')
para('<b>kill</b> sends a signal to a process. With no option it requests termination using SIGTERM, giving the program a chance to clean up. It does not delete the program file. For this exercise, stop only the worker created for your attempt.')
h('Confirm the identity immediately before stopping')
code('python3 ../../terminal-lab-3/lab_process.py status\nps -p PID -o pid,stat,args > work/process-confirm.txt\ncat work/process-confirm.txt')
para('Continue only if the helper says <b>RUNNING</b> and the ps row contains <b>lab_process.py worker</b> and your exact <b>LAB3 token</b> from page 6. Replace PID with that same current number. If anything differs, stop and ask for help. Never guess a PID, use 0 or a negative number, or signal another visible process.')
lines('Confirmed PID: __________  Matching token: _______________________',0)
code('kill PID\nps -p PID -o pid,stat,args > work/process-after.txt\ncat work/process-after.txt\npython3 ../../terminal-lab-3/lab_process.py status')
para('Expect the ps header with no data row and helper status <b>STOPPED</b>. When ps finds no matching process it can return a nonzero exit status; the header is still useful evidence. If a row briefly remains, wait a moment and repeat only the ps check. Do not send more signals blindly.')
lines('What evidence shows that the designated worker stopped?',1)
h('Apply it independently')
para('Inspect the recorded PID again with ps. Explain why you must not send kill again just because you remember that number: Linux can later reuse a PID for another process.')
lines('My command and explanation:',2)
lines('Why does an empty terminal response from kill alone not prove completion?',1)
para('Do not use kill -9, broad name-based stopping or top\'s kill action. If the worker expired before this step, preserve this attempt and use a new ID to repeat Experiments 3-5.','small')

page('EXPERIMENT 6 / A', 'Package files with zip')
para('An <b>archive</b> stores several files and their paths in one file. A ZIP archive can also compress file data. Packaging is useful only if the expected files can be listed, recovered and compared with the originals.')
code('ls practice/dispatch\nls practice/dispatch/lists\ncat practice/dispatch/notice.txt')
lines('Predict: will archiving remove the originals?',1)
code('zip -r work/dispatch.zip practice/dispatch\nunzip -l work/dispatch.zip > work/zip-list.txt\ncat work/zip-list.txt')
para('<b>zip -r</b> includes the folder recursively, including nested files. The archive name comes before the source folder. <b>unzip -l</b> lists contents without extracting. Paths are relative to the folder where you ran zip.')
lines('Which listed path proves that the nested room list is included?',1)
h('Extract into a separate folder')
code('unzip work/dispatch.zip -d work/unzipped\ndiff -r practice/dispatch work/unzipped/practice/dispatch > work/zip-diff.txt\ncat work/zip-diff.txt')
para('<b>-d</b> selects the extraction destination; unzip creates it if needed. <b>diff -r</b> compares corresponding files through the directory trees. An empty comparison report means no differences were found. Inspect any printed difference before continuing.')
lines('My extraction path and comparison result:',1)
lines('Why is seeing an archive filename in ls insufficient verification?',1)
para('Create each named archive once. zip updates an existing archive and can retain old entries. Re-extraction may ask about overwriting; do not approve blindly. Recovery guidance is on page 14.','small')

page('EXPERIMENT 6 / B', 'Send a magazine handover')
para('The magazine team has a new handover in <b>challenge/dispatch/</b>. Complete this without copying the guided command block unchanged. Keep the nested team folder and both text files.')
code('cat challenge/dispatch/brief.txt\nls challenge/dispatch\nls challenge/dispatch/team')
h('Build, inspect and recover')
step('1.', 'Create <b>work/magazine.zip</b> from the complete challenge/dispatch folder.')
lines('My packaging command:',1)
step('2.', 'Save its listing as <b>work/magazine-list.txt</b>. Inspect the paths before extracting.')
lines('My listing command and the nested path I checked:',2)
step('3.', 'Extract into <b>work/magazine-out/</b>. Work out where the original folder path will appear inside this destination.')
lines('My extraction command:',1)
step('4.', 'Compare the recovered dispatch folder with challenge/dispatch. Save the recursive diff output as <b>work/magazine-diff.txt</b>.')
lines('My comparison command and result:',2)
h('Understanding check')
lines('A ZIP lists brief.txt but no team/credits.txt. What likely went wrong, and how would you check before sending it?',2)
lines('Does a successful extraction prove that the source and recovered files match? Why?',1)

page('EXPERIMENT 7 / A', 'Archiving versus compression')
para('<b>tar</b> collects files and paths into an archive. Plain tar does not compress their data. Adding gzip compression can reduce the archive size; how much depends on the data. Changing a filename extension does not change its contents.')
para('The supplied <b>practice/compress/</b> folder has repeated text and deterministic binary noise of similar size. Predict which would compress more. Do not display noise.bin as text.')
lines('My prediction and reason:',1)
code('ls -l practice/compress\ntar -cf work/bundle.tar practice/compress\ntar -tf work/bundle.tar > work/tar-list.txt\ncat work/tar-list.txt')
para('<b>-c</b> creates; <b>-t</b> lists; <b>-f</b> takes the archive filename immediately after the options. The source folder follows. A directory is included recursively.')
code('tar -czf work/bundle.tar.gz practice/compress\ntar -tzf work/bundle.tar.gz > work/targz-list.txt\ncat work/targz-list.txt\ndu -h work/bundle.tar work/bundle.tar.gz > work/archive-sizes.txt\ncat work/archive-sizes.txt')
para('<b>-z</b> adds gzip compression. Both listings should describe the same source files. du measures allocated disk usage; <b>ls -l</b> shows logical file bytes. Tiny archives may occupy equal disk blocks even if byte sizes differ.')
lines('tar size: __________  tar.gz size: __________  Compare with units:',1)
lines('If both contain the same files, why can their sizes differ?',1)
para('A combined archive cannot show which individual sample compressed best. On the next page, measure each sample separately to test your prediction.','small')

page('EXPERIMENT 7 / B', 'Recover and test your prediction')
code('mkdir -p work/tar-out\ntar -xzf work/bundle.tar.gz -C work/tar-out\ndiff -r practice/compress work/tar-out/practice/compress > work/tar-diff.txt\ncat work/tar-diff.txt')
para('<b>-x</b> extracts; <b>-C</b> chooses an existing destination folder. mkdir -p creates it if missing. Extract these supplied archives only into work/, then compare the recovered files with the originals.')
lines('My comparison result and what it means:',1)
h('Test the two samples separately')
code('tar -czf work/text.tar.gz practice/compress/repeated.txt\ntar -czf work/noise.tar.gz practice/compress/noise.bin\nls -l practice/compress/repeated.txt practice/compress/noise.bin\nls -l work/text.tar.gz work/noise.tar.gz')
lines('Text bytes before/after: __________ / __________',0)
lines('Noise bytes before/after: __________ / __________',0)
lines('Did the result support your prediction? Explain any archive overhead.',1)
h('Apply it independently')
para('Create <b>work/magazine.tar.gz</b> from <b>challenge/dispatch</b>. List it to confirm that both files, including the nested credits file, are included.')
lines('My create and list commands:',2)
lines('A friend renames bundle.tar to bundle.tar.gz. Has compression occurred? How would you distinguish a name from an operation?',1)
para('An archive does not replace the originals or guarantee a backup. Keep a separately stored, verified copy when you need recovery beyond this Codespace.','small')

page('CHECK AND EXPLAIN', 'Review your evidence')
code('python3 ../../terminal-lab-3/check.py')
para('Run the checker from your lab root at any point. <b>PASS</b> means a saved result meets that check. <b>CHECK</b> names something to inspect. Future experiments remain unfinished until you do them. The full book has <b>35 checks</b>; the checker never repairs, uploads or submits work.')
table([['Experiment','Evidence in work/'],['1','usage reports, filesystem.txt, observations.txt, before/after copy and recording copy'],['2','memory.txt, uptime.txt, system.txt'],['3-5','process-before/confirm/after.txt, process-notes.txt, top.txt and helper records'],['6','both ZIPs, listings, recovered folders and diff reports'],['7','tar and tar.gz files, listings, recovered folder, diff and size reports']], [85,W-85])
para('File checks cannot grade explanation quality or prove that you used interactive tools independently. Show your instructor your live top controls and discuss the choices below.')
lines('1. Which commands answer "largest folder", "available storage" and "available RAM"? Why are these different questions?',2)
lines('2. What would you verify before stopping a process, even if you wrote its PID down earlier?',2)
lines('3. What evidence would you provide with an archive to show that its nested files can be recovered correctly?',2)
lines('4. Does a larger load average necessarily mean a higher CPU percentage? Explain what else you need to know.',2)
para('Save notes and editor buffers. Keep this Codespace for review. Your instructor may ask you to download work/ separately; the checker is feedback, not a submission system.','small')

page('SHARED HINTS', 'When a result surprises you')
h('Check location and saved evidence')
para('Use <b>pwd</b> before relative paths. Return to the lab root recorded on page 1. Read the saved report with cat; do not fill observation fields from a newer snapshot. The <b>&gt;</b> symbol replaces its destination, so point it only at the intended work/ file.')
h('Storage and memory')
para('Compare units before numbers. du summarizes named folders; df describes their containing filesystem. In free, find the Mem row and available column. In uptime, the final three values are ordered from shortest to longest interval. Readings may change without an action from you.')
h('Processes')
para('Use the helper\'s actual PID wherever the book says PID. Match the complete LAB3 token in the ps command line. An S state or 0.0 CPU can be normal. top may show a short program name; the ps arguments are the stronger identity check. Press q to leave top before entering shell commands.')
para('If the helper says STOPPED before Experiment 5, do not reuse that PID. It may have expired after an hour or the Codespace may have stopped. Preserve your files and use a new lab ID for a fresh process attempt. The helper will not silently replace a stopped worker.')
h('Archives')
para('An archive stores paths relative to where you created it. Listing first tells you which path to expect after extraction. ZIP uses <b>-d</b> for the destination; tar uses <b>-C</b> and needs that folder to exist. Check the archive name after -f carefully.')
para('If you must redo a ZIP, first move the old archive and extraction folder to unused backup names inside work/ using familiar mv. Then recreate and extract into the now-unused names from the book. Do not update a suspect archive repeatedly or overwrite originals. Ask for help if unsure.')
h('Read checker feedback')
para('Fix the named result, save, and run the checker again. A missing report differs from an incorrect explanation. If original files or before-copy evidence changed, preserve the attempt and ask for a new ID. Setup reruns do not reset or repair anything.')
h('Use the manual when needed')
para('Use <b>man COMMAND</b> for the Linux command installed here; q exits the manual. Read options in context before trying them. The lab requires only the commands shown in this book.')

page('COMMAND REFERENCE', 'Ten new commands')
table([['Command / example','Purpose'],['du -sh FOLDER','One readable allocated-storage summary.'],['df -h .','Capacity and space of the containing filesystem.'],['free -h','Readable RAM and swap snapshot.'],['uptime','Elapsed uptime; 1, 5 and 15 minute load averages.'],['ps -p PID -o pid,stat,args','Snapshot of one PID, its state and command line.'],['top / top -p PID','Live process display / one selected PID.'],['kill PID','Request termination of the confirmed lab worker.'],['zip -r work/name.zip FOLDER','Package a folder and its nested contents.'],['unzip -l work/name.zip','List a ZIP archive.'],['unzip work/name.zip -d work/out','Extract ZIP into the named destination.'],['tar -cf work/name.tar FOLDER','Create an uncompressed tar archive.'],['tar -czf work/name.tar.gz FOLDER','Create a gzip-compressed tar archive.'],['tar -tf work/name.tar','List tar contents; use -tzf for gzip.'],['tar -xzf work/name.tar.gz -C work/out','Extract gzip tar into an existing folder.']], [275,W-275],True)
h('Familiar tools and keys')
para('<b>pwd / cd / ls</b>: location, navigation, listing. <b>cat</b>: read text. <b>cp / mv</b>: copy or move a named file. <b>mkdir -p</b>: create a destination folder. <b>diff -r A B</b>: compare folder trees. <b>COMMAND &gt; work/file</b>: save output, replacing that file. <b>nano</b>: edit notes.')
para('<b>nano:</b> Ctrl+O, Enter saves; Ctrl+X or F2 exits. <b>top:</b> Shift+P sorts CPU, Shift+M sorts memory, q exits. <b>top -b -n 1 -p PID</b> saves a single batch snapshot when redirected.','small')
para('References: <link href="https://www.gnu.org/software/coreutils/manual/html_node/File-space-usage.html" color="#0E6A50"><u>GNU file space usage</u></link>; <link href="https://man7.org/linux/man-pages/man1/free.1.html" color="#0E6A50"><u>free</u></link>, <link href="https://man7.org/linux/man-pages/man1/uptime.1.html" color="#0E6A50"><u>uptime</u></link>, <link href="https://man7.org/linux/man-pages/man1/ps.1.html" color="#0E6A50"><u>ps</u></link>, <link href="https://man7.org/linux/man-pages/man1/top.1.html" color="#0E6A50"><u>top</u></link>; installed <b>man zip</b>, <b>man unzip</b>, <b>man tar</b> and Bash <b>help kill</b>.','small')

# Two passes obtain a true page count; explicit page breaks preserve teaching order.
from reportlab.pdfgen import canvas
class NumberedCanvas(canvas.Canvas):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs); self.states=[]
    def showPage(self):
        self.states.append(dict(self.__dict__)); self._startPage()
    def save(self):
        total=len(self.states)
        if total != 15:
            raise RuntimeError(f'Booklet overflow: expected 15 pages, got {total}.')
        for state in self.states:
            self.__dict__.update(state)
            self.setFont('Body',8);self.setFillColor(GRAY)
            self.drawRightString(553.27,28,f'{self._pageNumber} / {total}')
            super().showPage()
        super().save()
def decorate(c,doc):
    width,height=doc.pagesize
    c.setStrokeColor(MINT);c.setLineWidth(3);c.line(42,height-30,width-42,height-30)
    c.setStrokeColor(LINE);c.setLineWidth(.5);c.line(42,42,width-42,42)
    c.setFont('Body',7.5);c.setFillColor(GRAY)
    c.drawString(42,28,'TENSOR SCHOOL | EXPERIMENT BOOK 3')

SimpleDocTemplate(str(OUT),pagesize=(595.27,841.89),rightMargin=42,leftMargin=42,
    topMargin=48,bottomMargin=55,title='Experiment Book 3',
    author='Tensor School',subject='Storage, memory, processes and archives').build(
    story,onFirstPage=decorate,onLaterPages=decorate,canvasmaker=NumberedCanvas)
import re
from html import unescape
clean=[]
for block in md:
    if block.startswith('```'):
        clean.append(block)
    else:
        block=re.sub(r'<link href="([^"]+)"[^>]*>(.*?)</link>',r'[\2](\1)',block)
        clean.append(unescape(re.sub(r'</?(?:u|b|i|br|font)\b[^>]*>','',block)))
TEXT.write_text('\n'.join(line.rstrip() for line in '\n\n'.join(clean).splitlines())+'\n',encoding='utf-8')
print(OUT)
