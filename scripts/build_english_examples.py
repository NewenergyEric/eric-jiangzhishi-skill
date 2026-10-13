"""Typeset complete English editions using the original, text-free illustrations."""
from pathlib import Path
import hashlib
import json
import re
from build_example import prepare_fonts, ROOT, W, H, PAPER, INK
from fontTools.ttLib import TTFont as FontFile
from fontTools.varLib.instancer import instantiateVariableFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from PIL import Image
from pypdf import PdfReader
import pypdfium2 as pdfium


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(case):
    base=ROOT/'examples'/case
    out=base/'output'
    data=json.loads((base/'content.en.json').read_text(encoding='utf-8'))
    fonts=prepare_fonts()
    hand=ROOT/'.build/fonts/Caveat-700.ttf'
    source=FontFile(ROOT/'vendor/fonts/Caveat.ttf',recalcTimestamp=False)
    instantiateVariableFont(source,{'wght':700},inplace=True).save(hand)
    pdfmetrics.registerFont(TTFont('Hand',str(hand)))
    fonts['Hand']=FontFile(hand)
    target=out/f'{case}.en.pdf'
    c=canvas.Canvas(str(target),pagesize=(W,H),pageCompression=1,invariant=1)
    c.setTitle(data['title']+' | Making Sense Together')
    c.setAuthor('eric-jiangzhishi-skill contributors')
    c.setCreator('build_english_examples.py')
    c.setSubject('Complete English illustrated edition')
    records=[]
    sources=['scripts/build_english_examples.py','scripts/build_example.py',f'examples/{case}/content.en.json','vendor/fonts/Caveat.ttf','vendor/fonts/NotoSansSC.ttf']

    def text(page,key,value,x,y,w,size=15.5,leading=23,font='Body',limit=None,center=False):
        lines=[]
        for para in value.split('\n'):
            current=''
            for word in para.split():
                candidate=(current+' '+word).strip()
                if pdfmetrics.stringWidth(candidate,font,size)>w and current:
                    lines.append(current);current=word
                else:current=candidate
            if current:lines.append(current)
        if limit is not None and len(lines)*leading>limit:
            raise ValueError(f'{case} {key} needs {len(lines)*leading}, available {limit}')
        c.setFont(font,size);c.setFillColor(HexColor(INK))
        cmap=fonts[font].getBestCmap();units=fonts[font]['head'].unitsPerEm
        for n,line in enumerate(lines):
            width=pdfmetrics.stringWidth(line,font,size)
            if width>w:raise ValueError('Unbreakable word: '+key)
            left=x+(w-width)/2 if center else x
            baseline=y+size+n*leading
            c.drawString(left,H-baseline,line)
            glyph_boxes=[];cursor=left
            for ch in line:
                if ord(ch) not in cmap:raise ValueError('Missing glyph: '+ch)
                glyph=fonts[font]['glyf'][cmap[ord(ch)]]
                if hasattr(glyph,'xMin'):
                    glyph_boxes.append([cursor+glyph.xMin/units*size,baseline-glyph.yMax/units*size,cursor+glyph.xMax/units*size,baseline-glyph.yMin/units*size])
                cursor+=pdfmetrics.stringWidth(ch,font,size)
            if glyph_boxes:
                bounds=[min(b[0] for b in glyph_boxes),min(b[1] for b in glyph_boxes),max(b[2] for b in glyph_boxes),max(b[3] for b in glyph_boxes)]
                if bounds[0]<0 or bounds[1]<0 or bounds[2]>W or bounds[3]>H:raise ValueError('Text out of page: '+key)
                records.append({'page':page,'id':key,'text':line,'font':font,'size':size,'bounds':bounds})
        return y+len(lines)*leading

    def art(name,x,y,w,h,clip=None):
        rel=f'examples/{case}/art/{name}'
        if rel not in sources:sources.append(rel)
        c.saveState()
        if clip:
            cx,cy,cw,ch=clip;p=c.beginPath();p.rect(cx,H-cy-ch,cw,ch);c.clipPath(p,stroke=0,fill=0)
        c.drawImage(ImageReader(str(ROOT/rel)),x,H-y-h,width=w,height=h,mask='auto')
        c.restoreState()

    def leader(points):
        c.setStrokeColor(HexColor('#668274'));c.setLineWidth(.8)
        p=c.beginPath();p.moveTo(points[0][0],H-points[0][1])
        for x,y in points[1:]:p.lineTo(x,H-y)
        c.drawPath(p);c.setFillColor(HexColor('#668274'))
        c.circle(points[-1][0],H-points[-1][1],2,fill=1,stroke=0)

    def base(page):
        c.setFillColor(HexColor(PAPER));c.rect(0,0,W,H,stroke=0,fill=1)
        icon='icon-telescope.png' if case=='solar-system' else 'icon-microscope.png'
        art(icon,43,19,34,40)
        p=data['pages'][page-1]
        text(page,'eyebrow',p['eyebrow'],89,34,575,12,18)
        text(page,'title',p['title'],46,83,633,44,45,'Hand',limit=100)
        c.setStrokeColor(HexColor('#D9BE64'));c.setLineWidth(2)
        line=c.beginPath();line.moveTo(48,H-183);line.curveTo(102,H-178,166,H-186,228,H-180);c.drawPath(line)

    def footer(page):
        p=data['pages'][page-1]
        c.setStrokeColor(HexColor('#A3B0A0'));c.setLineWidth(.6);c.line(48,57,672,57)
        text(page,'note',p['note'],48,911,587,9.5,13,limit=26)
        text(page,'number',f'{page:02d}',647,911,25,11,16,center=True)
        value='Sources: NASA; IAU. Full references online.' if case=='solar-system' else 'Sources: NHGRI; OpenStax Biology 2e, Chapter 4. Full references online.'
        text(page,'sources',value,48,941,624,9.5,13)
        c.linkURL(f'https://github.com/NewenergyEric/eric-jiangzhishi-skill/blob/main/examples/{case}/sources.md',(48,2,650,20),relative=0,thickness=0)

    p=data['pages'][0];base(1)
    text(1,'lead',p['lead'],48,207,624,16,23,limit=92)
    if case=='solar-system':
        art('inner-planets.png',0,263,720,480,clip=(0,326,720,285))
        for label,center in zip(p['labels'],[140,294,471,639]):text(1,'label.'+label,label,center-67,602,134,14,20,'Heading',center=True)
        text(1,'sun','Sun (a star)',48,343,120,11,16)
        text(1,'order','Moving outward from the Sun',48,640,350,11,16)
        y=673
    else:
        art('animal-cell.png',100,324,520,520*2/3)
        labels=[
            ('Cell membrane',552,328,130,[(579,352),(574,394),(550,424)]),
            ('Cytoplasm',575,596,105,[(592,591),(565,586),(522,557)]),
            ('Nucleus',48,408,94,[(128,431),(196,431),(283,484)]),
            ('Ribosomes',48,608,100,[(141,618),(182,592),(205,555)]),
            ('Mitochondria',600,430,108,[(595,447),(548,447),(469,411)])]
        for label,x,y,w,points in labels:
            leader(points);text(1,'label.'+label,label,x,y,w,13,19,'Heading')
        y=695
    for i,value in enumerate(p['paragraphs']):y=text(1,f'paragraph.{i}',value,48,y,624,15,22)+12
    if y>900:raise ValueError(f'{case} page 1 footer collision: {y}')
    footer(1);c.showPage()

    p=data['pages'][1];base(2)
    if case=='solar-system':
        art('outer-planets.png',351,216,354,531)
        y=218
        for i,value in enumerate(p['paragraphs']):y=text(2,f'paragraph.{i}',value,48,y,290,14.5,21)+14
        if y>759:raise ValueError(f'{case} page 2 body collision: {y}')
        for label,x,y,w in [(p['labels'][0],370,292,118),(p['labels'][1],579,462,116),(p['labels'][2],347,568,130),(p['labels'][3],526,718,140)]:text(2,'label.'+label,label,x,y,w,13,19,'Heading',center=True)
        text(2,'closing',p['closing'],48,778,624,15,22,limit=110)
    else:
        art('plant-and-bacterium.png',365,255,318,477)
        y=224
        for i,value in enumerate(p['paragraphs']):y=text(2,f'paragraph.{i}',value,48,y,295,15,22)+16
        if y>765:raise ValueError(f'{case} page 2 body collision: {y}')
        labels=[
            ('Leaf cell',385,221,140,[]),
            ('Cell wall',587,241,94,[(611,263),(628,290)]),
            ('Chloroplast',570,594,112,[(605,594),(590,564),(570,524)]),
            ('Central vacuole',426,393,154,[]),
            ('Bacterium',381,736,120,[]),
            ('Nucleoid (DNA)',525,737,162,[(575,734),(566,716),(503,658)])]
        for label,x,y,w,points in labels:
            if points:leader(points)
            text(2,'label.'+label,label,x,y,w,13,19,'Heading')
        text(2,'closing',p['closing'],48,789,624,15.5,23,limit=110)
    footer(2);c.showPage();c.save()
    overlaps=[]
    for i,a in enumerate(records):
        for b in records[i+1:]:
            if a['page']!=b['page']:continue
            x,y,r,t=a['bounds'];X,Y,R,T=b['bounds']
            if min(r,R)-max(x,X)>1 and min(t,T)-max(y,Y)>1:overlaps.append([a['page'],a['id'],b['id']])
    if overlaps:raise ValueError('Text overlap: '+str(overlaps))
    pdf=PdfReader(target)
    for page,expected in zip(pdf.pages,data['pages']):
        actual=''.join(page.extract_text().split())
        if re.search(r'[\u3400-\u9fff]',actual):raise ValueError('Chinese text in English PDF')
        for value in [expected['title'],expected['eyebrow'],expected.get('lead',''),*expected['paragraphs'],expected.get('closing',''),*expected['labels'],expected['note']]:
            if ''.join(value.split()) not in actual:raise ValueError('Missing English copy: '+value)
    outputs=[target]
    doc=pdfium.PdfDocument(str(target))
    for i in range(2):
        image=out/f'page-{i+1:02d}.en.png';doc[i].render(scale=2).to_pil().convert('RGB').save(image,optimize=True);outputs.append(image)
    doc.close()
    audit={'language':'en','pages':2,'pageSize':[W,H],'text':records,'textOverlaps':overlaps,'completeCopyVerified':True,'chineseTextFound':False,'sourceHashes':{name:digest(ROOT/name) for name in sources},'outputHashes':{p.name:digest(p) for p in outputs}}
    (out/'layout.en.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'case':case,'englishPages':2,'copyVerified':True,'textOverlaps':len(overlaps),'outputs':[p.name for p in outputs]}))


if __name__=='__main__':
    for case in ['solar-system','cells']:build(case)
