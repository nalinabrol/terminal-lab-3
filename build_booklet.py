from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'Experiment_Book_3_Review_Draft.pdf'
TEXT = ROOT/'Experiment_Book_3_Review_Draft.md'
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

page('LAB 3 / REVIEW DRAFT / STAGE 1', 'Experiment Book 3')
para('Inspect storage, manage processes, and package files')
para('<b>This draft contains setup and Experiment 1 only.</b> Begin with folder usage and available filesystem space. Stop at the review checkpoint at the end of this draft.')
lines('Name: __________________________  Lab ID: ______________  Section: __________', 0)
h('Get ready')
para('Sign in with your own GitHub account. Open the Lab 3 link below and create a Codespace on <b>main</b>. Later, resume that same Codespace to continue. Books 1 and 2 use different repositories.')
para('<link href="https://codespaces.new/nalinabrol/terminal-lab-3?quickstart=1" color="#0E6A50"><u>https://codespaces.new/nalinabrol/terminal-lab-3?quickstart=1</u></link>', 'small')
para('Wait for setup to finish. Choose <b>Trust Folder &amp; Continue</b> if asked. A Bash terminal opens. If needed, use the Command Palette command <b>Lab 3: Focus Bash Terminal</b>. At the repository root, run:')
code('bash terminal-lab-3/start.sh')
para('Enter your instructor-assigned lab ID, not your email. Run the exact <b>cd</b> command printed by setup. Then run these commands one at a time:')
code('pwd\ncat identity.txt\nls')
lines('My lab root (the complete path printed by pwd):', 1)
table([['Folder', 'Purpose'], ['practice/', 'Original event exports. Keep these files unchanged.'], ['challenge/', 'Original evidence for a short independent application.'], ['work/', 'Your saved measurements, observations and working copies.']], [95,W-95])
para('<b>How to work:</b> predict, run, inspect, explain. Start each section at your lab root. Use familiar terminal commands and nano; no solution scripts are needed. Save only inside work/.', 'small')
para('Reusing an ID preserves every existing file; it does not reset an attempt. Save in nano with Ctrl+O, Enter, then exit with Ctrl+X. Use Control on a Mac too. Keep this Codespace for review; ignored lab-work/ is not a GitHub backup.', 'small')

page('EXPERIMENT 1 / A', 'Which folder uses the most?')
start()
para('The campus event team has notices, posters and recordings. Before making another copy, inspect the space these folders already use. A folder name alone does not tell you its size.')
code('cat practice/README.txt\nls practice\nls practice/recordings')
para('The .bin files are simulated stored exports, not playable media. Measure their folders; do not open these binary files in cat or nano.', 'small')
h('1A | Predict, then measure')
lines('I predict the largest folder is __________________ because:', 1)
code('du -sh practice/notices practice/posters practice/recordings')
para('<b>du</b> estimates the storage used by the files and folders you name. <b>-s</b> gives one summary per named path, including its contents. <b>-h</b> displays readable units. You can combine them as <b>-sh</b>. This command measures; it does not change the folders.')
table([['Folder', 'My displayed size, including its unit'], ['notices', ''], ['posters', ''], ['recordings', '']], [170,W-170])
h('1B | Read the units before comparing')
para('For these GNU commands, <b>K</b> means units of 1,024 bytes, <b>M</b> means 1,024 K, and <b>G</b> means 1,024 M. Displays are rounded. Compare the units as well as the numbers: a value in M may exceed a larger-looking number in K.')
lines('Which is larger: 900K or 2.0M? Explain:', 1)
h('1C | Save evidence')
code('du -sh practice/notices practice/posters practice/recordings > work/guided-usage.txt\ncat work/guided-usage.txt\nnano work/observations.txt')
para('Fill <b>guided_largest=</b> with only the largest folder name, after the equals sign. Leave the other lines for later. Save and exit. The report retains all three sizes and paths; your answer identifies the largest folder.', 'small')
para('The &gt; symbol replaces its destination file. It must point to work/, never to an original evidence file. Exact totals can include folder overhead; your classmate may see slightly different values.', 'small')

page('EXPERIMENT 1 / B', 'How much space is available?')
start()
para('A <b>filesystem</b> is the storage area in which files and folders are organised. Your lab folder occupies only part of one filesystem. Available space belongs to that filesystem, not to a folder with its own separate allowance.')
h('1D | Inspect the filesystem containing this folder')
code('df -h .')
para('<b>df</b> reports filesystem capacity and space usage. <b>-h</b> uses readable units. The dot <b>.</b> means your current folder; here it selects the filesystem containing your lab root. It does not ask df to add up the files in that folder.')
table([['Column', 'What to read'], ['Filesystem', 'The filesystem/device label. Its name can vary.'], ['Size', 'Total capacity reported for this filesystem.'], ['Used', 'Space already used across the filesystem.'], ['Avail', 'Space reported as available for use.'], ['Use%', 'The reported percentage used, not the percentage free.'], ['Mounted on', 'Where this filesystem is attached to the directory tree.']], [100,W-100])
para('These values describe storage inside your remote Linux Codespace, not the free space on your own laptop. In Codespaces, the mount can be /workspaces or another path. Read what your output actually says.', 'small')
h('1E | Save one snapshot and interpret it')
code('df -h . > work/filesystem.txt\ncat work/filesystem.txt\nnano work/observations.txt')
para('Fill <b>filesystem_size</b>, <b>filesystem_used</b>, <b>filesystem_available</b>, <b>filesystem_use_percent</b> and <b>filesystem_mounted_on</b> from your <b>saved</b> output. Keep the units, percent sign and full mount path. Save and exit.')
lines('Which column would you inspect before saving another large export?', 1)
para('Capacity, usage and available space can differ across students and change during the session. Do not copy someone else\'s numbers. Rounded values and filesystem accounting mean Used + Avail need not exactly equal Size. No exact free-space value is required.', 'small')

page('EXPERIMENT 1 / C', 'Two commands, two questions')
start()
h('1F | Compare the same dot')
code('du -sh .\ndf -h .')
lines('du -sh . displays this size for my lab folder: __________________', 0)
lines('df -h . displays this filesystem Size: ________ and Avail: ________', 0)
lines('Both commands use . . Why do they answer different questions?', 2)
h('1G | Predict a small, controlled change')
para('The folder <b>work/copy-target/</b> starts empty. You will copy one supplied recording into it, keeping the original. Predict which folder measurement will increase. Will a rounded df display necessarily change?')
lines('My prediction and reason:', 1)
code('ls work/copy-target\ndu -sh work/copy-target > work/copy-before.txt\ncp practice/recordings/recording.bin work/copy-target/\ndu -sh work/copy-target > work/copy-after.txt\ncat work/copy-before.txt work/copy-after.txt\ndu -sh practice/recordings\ndu -sh .\ndf -h .')
para('Run the copy sequence once. If resuming after the copy, inspect your saved before/after reports instead of overwriting the before report. If the target already contains a file on your first attempt, ask your instructor for help.', 'small')
lines('What grew? What evidence shows that the original still exists?', 1)
para('A small copy can increase folder usage while rounded df values look unchanged. Other Codespace activity can also change filesystem usage. An unchanged Avail display does not prove that the copy used no storage. An empty directory may itself occupy a little space.', 'small')

page('EXPERIMENT 1 / INDEPENDENT APPLICATION', 'Inspect a new set of exports')
start()
para('The student magazine team needs the same kind of storage audit. Use fresh evidence in challenge/. Choose the commands yourself, drawing on the guided work.')
code('cat challenge/brief.txt\nls challenge')
h('Your task')
step('1. Predict.', 'Write down which of <b>design</b>, <b>notes</b> or <b>interviews</b> you expect to occupy the most storage.')
lines('My prediction and reason:', 1)
step('2. Measure.', 'Use du to get one readable summary for each of the three folders. Save the three output lines as <b>work/challenge-usage.txt</b>. Do not measure only the combined challenge folder.')
lines('My command:', 1)
step('3. Inspect.', 'Read your saved report. Compare the values with their units, then fill <b>challenge_largest=</b> in <b>work/observations.txt</b> with only the largest folder name.')
lines('The largest folder and the displayed size supporting my answer:', 1)
step('4. Apply.', 'The team now asks whether this filesystem has space for another export. Run the appropriate command from your lab root. Write the command and the column you inspected.')
lines('Command and column:', 1)
lines('My available-space reading, with its unit:', 1)
lines('Why would measuring only the largest folder fail to answer that question?', 2)
para('Keep all originals in challenge/ unchanged. You do not need to copy or remove any challenge data. A folder can be the largest in this small dataset while using only a small fraction of filesystem capacity.', 'small')

page('EXPERIMENT 1 / CHECK AND EXPLAIN', 'Make your evidence reviewable')
start()
h('Check saved work')
code('cat work/observations.txt\npython3 ../../terminal-lab-3/check.py')
para('The checker reports <b>9 file checks</b>. PASS means a saved result meets that check. CHECK names something to inspect and gives a hint. It never repairs, uploads or submits your files. Correct the named result, save it, and run the checker again.')
table([['Evidence in work/', 'What it records'], ['guided-usage.txt / challenge-usage.txt', 'Three folder summaries in each report.'], ['filesystem.txt', 'The saved df header and filesystem row.'], ['observations.txt', 'Your two folder choices and five filesystem fields.'], ['copy-before.txt / copy-after.txt', 'The target folder measurement before/after the copy.'], ['copy-target/recording.bin', 'The working copy; the original remains in practice/.']], [250,W-250])
h('Understanding check - explain in your own words')
lines('1. A friend says "du -sh . tells me how much more I can save here." Correct the claim and give the command they need.', 2)
lines('2. Does Used in df describe just your lab folder? Explain.', 2)
lines('3. After your copy, Avail looks unchanged. What evidence shows the copy happened, and why might Avail look the same?', 2)
lines('4. What do -s and -h each contribute to du -sh?', 2)
para('<b>Review checkpoint:</b> show your instructor the saved reports and your explanations. File checks do not prove understanding or independent work. This review draft ends with Experiment 1; there is no next experiment to complete yet.', 'small')

page('EXPERIMENT 1 / HINTS AND REFERENCE', 'Keep beside your terminal')
para('Try a task before reading its hint. Examples below support Experiment 1 only.')
table([['Command', 'Question it answers'], ['du -sh FOLDER', 'How much storage does this folder and its contents use?'], ['du -sh FOLDER_A FOLDER_B', 'How much storage does each named folder use?'], ['du -sh .', 'How much storage does my current folder and its contents use?'], ['df -h .', 'What capacity, usage and availability does the filesystem containing my current folder report?']], [220,W-220])
h('Familiar tools you will reuse')
table([['Command / keys', 'Reminder'], ['pwd / ls / cd PATH', 'Show your location / list names / change folder.'], ['cat work/report.txt', 'Read a saved text report.'], ['COMMAND > work/report.txt', 'Save command output; replace that destination file.'], ['cp SOURCE DESTINATION', 'Copy to the named destination; can overwrite a file.'], ['nano work/observations.txt', 'Edit the observation lines. Keep their key names.'], ['Ctrl+O, Enter / Ctrl+X', 'In nano: save and confirm filename / exit.']], [240,W-240])
h('Hints without the answers')
para('<b>Choosing the largest:</b> compare units first. Do not sort the displayed size as ordinary text and assume that gives the storage order.')
para('<b>Reading df:</b> follow each column heading vertically. Use the saved snapshot for the five observation fields, even if a fresh run has changed.')
para('<b>Independent report:</b> use the three named challenge folders as separate du arguments. Save the report in work/ and inspect it with cat.')
para('<b>Unexpected CHECK:</b> confirm your location with pwd. Check spelling, units and destination paths. A rerun of setup preserves mistakes too. Ask for help if originals or before-copy evidence were changed.')
para('<b>Preserve progress:</b> save editor changes and resume this same Codespace. Download work/ for a separate copy if your instructor requests it. Deleting a Codespace can lose its unbacked-up work.', 'small')
para('Command behaviour reference: <link href="https://www.gnu.org/software/coreutils/manual/html_node/File-space-usage.html" color="#0E6A50"><u>GNU Coreutils - File space usage</u></link>. Linux outputs may vary; record observations from your own Codespace.', 'small')

# Two passes obtain a true page count; explicit page breaks preserve teaching order.
from reportlab.pdfgen import canvas
class NumberedCanvas(canvas.Canvas):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs); self.states=[]
    def showPage(self):
        self.states.append(dict(self.__dict__)); self._startPage()
    def save(self):
        total=len(self.states)
        if total != 7:
            raise RuntimeError(f'Booklet overflow: expected 7 pages, got {total}.')
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
    c.drawString(42,28,'TENSOR SCHOOL | EXPERIMENT BOOK 3 | REVIEW DRAFT THROUGH EXPERIMENT 1')

SimpleDocTemplate(str(OUT),pagesize=(595.27,841.89),rightMargin=42,leftMargin=42,
    topMargin=48,bottomMargin=55,title='Experiment Book 3 - Review Draft through Experiment 1',
    author='Tensor School',subject='Folder storage usage and filesystem space: du and df').build(
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
