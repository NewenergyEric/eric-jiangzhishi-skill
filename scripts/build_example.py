"""Build the two-page example from local, editable sources. No network calls."""
from pathlib import Path
import argparse
import hashlib
import html
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
# Optional project-local dependencies; normal installations use requirements.txt.
if (ROOT / '.build/deps').is_dir():
    sys.path.insert(0, str(ROOT / '.build/deps'))
from fontTools.ttLib import TTFont as FontFile
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader
import pypdfium2 as pdfium

EXAMPLE = ROOT / 'examples/solar-system'
W, H = 720, 960
PAPER, INK = '#FCF8EE', '#192F2A'
CLOSE = set('，。！？；：、）】》」』”’')
OPEN = set('（【《「『“‘')
KEEP = ['水星','金星','地球','火星','木星','土星','天王星','海王星','太阳系','银河系','主小行星带','类地行星','温室效应','气态巨行星','冰巨行星','矮行星','细胞膜','细胞质','细胞核','核糖体','线粒体','细胞壁','叶绿体','大液泡','拟核']


def prepare_fonts():
    folder = ROOT / '.build/fonts'
    folder.mkdir(parents=True, exist_ok=True)
    source = ROOT / 'vendor/fonts/NotoSansSC.ttf'
    result = {}
    for weight, name in [(400, 'Body'), (700, 'Heading')]:
        target = folder / f'NotoSansSC-{weight}-stable.ttf'
        if not target.exists():
            font = FontFile(source, recalcTimestamp=False)
            instantiateVariableFont(font, {'wght': weight}, inplace=True).save(target)
        pdfmetrics.registerFont(TTFont(name, str(target)))
        result[name] = FontFile(target)
    return result


def wrap(text, font, size, width):
    lines = []
    for paragraph in text.split('\n'):
        remaining = paragraph
        while remaining:
            count = 1
            while count <= len(remaining) and pdfmetrics.stringWidth(remaining[:count], font, size) <= width:
                count += 1
            count -= 1
            if count < 1:
                raise ValueError('Text box narrower than one glyph')
            if count < len(remaining) and remaining[count] in CLOSE:
                count -= 1
            if remaining[count-1] in OPEN:
                count -= 1
            for term in KEEP:
                start = remaining.find(term)
                if 0 < start < count < start+len(term):
                    count = start
            # Keep short Latin words and numerals together.
            if count < len(remaining) and remaining[count-1].isascii() and remaining[count].isascii() and remaining[count-1].isalnum() and remaining[count].isalnum():
                split = count
                while split > 0 and remaining[split-1].isascii() and remaining[split-1].isalnum():
                    split -= 1
                if split:
                    count = split
            lines.append(remaining[:count])
            remaining = remaining[count:]
    return lines


def build(output, case='solar-system'):
    example = ROOT / 'examples' / case
    output.mkdir(parents=True, exist_ok=True)
    data = json.loads((example / 'content.json').read_text(encoding='utf-8'))
    fonts = prepare_fonts()
    manifest = {'page_size':[W,H], 'minimum_sizes':{'body':17,'lead':18,'label':15,'caption':13,'note':10.5,'title':36,'eyebrow':12}, 'blocks':[], 'text':[], 'issues':[]}
    rendered = {}
    target = output / f'{case}.pdf'
    c = canvas.Canvas(str(target), pagesize=(W,H), pageCompression=1, invariant=1)
    c.setTitle(data['title']+' | 把知识讲给人听')
    c.setAuthor('eric-jiangzhishi-skill contributors')
    c.setSubject('Two-page illustrated guide with primary sources and original AI-generated artwork')
    c.setCreator('eric-jiangzhishi-skill build_example.py')

    def text_block(page, key, text, x, top, width, size=18, leading=28, role='body', font='Body', max_height=None, centered=False):
        lines = wrap(text, font, size, width)
        allocated = max_height if max_height is not None else len(lines)*leading+size
        if len(lines)*leading > allocated:
            raise ValueError(f'{key}: text needs {len(lines)*leading} pt, allocated {allocated}')
        c.setFillColor(HexColor(INK))
        c.setFont(font,size)
        glyphs = fonts[font]['glyf']
        cmap = fonts[font].getBestCmap()
        units = fonts[font]['head'].unitsPerEm
        for row, line in enumerate(lines):
            baseline = top + size + row*leading
            actual_x = x + (width-pdfmetrics.stringWidth(line,font,size))/2 if centered else x
            cursor = actual_x
            bounds = []
            for character in line:
                glyph_name = cmap.get(ord(character))
                if glyph_name is None:
                    raise ValueError(f'Missing glyph in {key}: U+{ord(character):04X}')
                glyph = glyphs[glyph_name]
                if hasattr(glyph,'xMin'):
                    bounds.append((cursor+glyph.xMin/units*size, baseline-glyph.yMax/units*size, cursor+glyph.xMax/units*size, baseline-glyph.yMin/units*size))
                cursor += pdfmetrics.stringWidth(character,font,size)
            c.drawString(actual_x,H-baseline,line)
            if bounds:
                xmin,ymin,xmax,ymax = min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds)
                manifest['text'].append({'page':page,'block':key,'role':role,'size':size,'text':line,'x':round(xmin,3),'y':round(ymin,3),'w':round(xmax-xmin,3),'h':round(ymax-ymin,3)})
        manifest['blocks'].append({'page':page,'block':key,'role':role,'size':size,'x':x,'y':top,'w':width,'h':len(lines)*leading,'allocated_h':allocated})
        rendered[key] = '\n'.join(lines)
        return top+len(lines)*leading

    def art(filename,x,top,width,height,clip=None):
        c.saveState()
        if clip:
            cx,cy,cw,ch = clip
            path=c.beginPath()
            path.rect(cx,H-cy-ch,cw,ch)
            c.clipPath(path,stroke=0,fill=0)
        c.drawImage(ImageReader(str(example/'art'/filename)),x,H-top-height,width=width,height=height)
        c.restoreState()

    def title(page):
        # Generated lettering is an image asset, not an installable font.
        # Preserve searchable wording in a hidden text layer and accessible HTML.
        wording=data['pages'][page-1]['title']
        t=c.beginText(48,H-90); t.setFont('Heading',38); t.setTextRenderMode(3)
        for line in wording.split('\n'):
            t.textLine(line)
        t.setTextRenderMode(0)
        c.drawText(t)
        im=Image.open(example/'art'/f'title-{page:02d}.png').convert('RGBA')
        im=im.crop(im.getchannel('A').getbbox())
        scale=min(530/im.width,123/im.height)
        c.drawImage(ImageReader(im),48,H-73-im.height*scale,width=im.width*scale,height=im.height*scale,mask='auto')
        manifest.setdefault('lettering',[]).append({'page':page,'x':48,'y':73,'w':im.width*scale,'h':im.height*scale,'semantic_text':wording,'verified_by':'visual proof; separate from type geometry'})
        rendered[f'p{page}.title']=wording

    def base(page):
        c.setFillColor(HexColor(PAPER)); c.rect(0,0,W,H,fill=1,stroke=0)
        filename='icon-telescope.png' if case=='solar-system' else 'icon-microscope.png'
        im=Image.open(example/'art'/filename).convert('RGBA')
        im=im.crop(im.getchannel('A').getbbox())
        scale=min(30/im.width,30/im.height)
        c.drawImage(ImageReader(im),48+(30-im.width*scale)/2,H-25-im.height*scale,width=im.width*scale,height=im.height*scale,mask='auto')
        text_block(page,f'p{page}.eyebrow',data['pages'][page-1]['eyebrow'],88,33,550,12,18,'eyebrow')

    def footer(page):
        p = data['pages'][page-1]
        c.setStrokeColor(HexColor('#A3B0A0'));c.setLineWidth(.55);c.line(48,55,672,55)
        text_block(page,f'p{page}.note',p['note'],48,914,595,10.5,16,'note')
        text_block(page,f'p{page}.number',f'{page:02d}',647,914,25,11,16,'note',centered=True)
        source_line='资料：NASA 行星事实页；IAU 行星分类决议。完整出处 ↗' if case=='solar-system' else '资料：NHGRI 术语表；OpenStax Biology 2e，第 4 章。完整出处 ↗'
        text_block(page,f'p{page}.sources',source_line,48,937,624,10.5,16,'note')
        c.linkURL(f'https://github.com/NewenergyEric/eric-jiangzhishi-skill/blob/main/examples/{case}/sources.md',(48,4,633,48),relative=0,thickness=0)

    if case=='solar-system':
        p = data['pages'][0]
        base(1); title(1)
        text_block(1,'p1.lead',p['lead'],48,218,624,18,29,'lead',max_height=116)
        art('inner-planets.png',0,279,720,480,clip=(0,330,720,285))
        for label, center in zip(p['labels'],[142,294,471,641]):
            text_block(1,'p1.label.'+label,label,center-54,610,108,16,22,'label','Heading',centered=True)
        text_block(1,'p1.sun','太阳（恒星）',48,346,110,11,16,'note')
        text_block(1,'p1.order','从太阳向外 →',48,640,160,11,16,'note')
        y=672
        for i,paragraph in enumerate(p['paragraphs']):
            y=text_block(1,f'p1.paragraph.{i}',paragraph,48,y,624,18,28,'body',max_height=130)+13
        if y > 899: raise ValueError(f'Page 1 narrative overlaps footer: {y}')
        footer(1); c.showPage()

        p=data['pages'][1]
        base(2); title(2)
        art('outer-planets.png',348,214,358,537)
        y=224
        for i,paragraph in enumerate(p['paragraphs']):
            y=text_block(2,f'p2.paragraph.{i}',paragraph,48,y,295,17,26,'body',max_height=235)+18
        if y>766: raise ValueError(f'Page 2 narrative too tall: {y}')
        for label,x,top,width in [(p['labels'][0],365,293,100),(p['labels'][1],599,464,105),(p['labels'][2],350,572,128),(p['labels'][3],523,719,135)]:
            text_block(2,'p2.label.'+label,label,x,top,width,15,22,'label','Heading',centered=True)
        text_block(2,'p2.closing',p['closing'],48,787,624,18,28,'body',max_height=115)
        footer(2); c.showPage()
    else:
        def leader(points):
            c.saveState()
            c.setStrokeColor(HexColor('#668274'));c.setLineWidth(.8)
            path=c.beginPath();path.moveTo(points[0][0],H-points[0][1])
            for x,y in points[1:]:path.lineTo(x,H-y)
            c.drawPath(path)
            c.setFillColor(HexColor('#668274'))
            c.circle(points[-1][0],H-points[-1][1],2,fill=1,stroke=0)
            c.restoreState()
        p=data['pages'][0]
        base(1); title(1)
        text_block(1,'p1.lead',p['lead'],48,216,624,18,27,'lead',max_height=105)
        art('animal-cell.png',100,324,520,520*2/3)
        specs=[
            ('细胞膜',555,335,105,[(579,360),(574,394),(550,424)]),
            ('细胞质',595,589,77,[(592,605),(565,586),(522,557)]),
            ('细胞核',48,407,94,[(128,431),(196,431),(283,484)]),
            ('核糖体',48,608,94,[(130,618),(182,592),(205,555)]),
            ('线粒体',605,436,67,[(600,454),(548,454),(469,411)])
        ]
        for label,x,top,width,points in specs:
            leader(points)
            text_block(1,'p1.label.'+label,label,x,top,width,15,22,'label','Heading')
        y=695
        for i,paragraph in enumerate(p['paragraphs']):
            y=text_block(1,f'p1.paragraph.{i}',paragraph,48,y,624,18,27,'body',max_height=135)+12
        if y>900: raise ValueError(f'Cells page 1 too tall: {y}')
        footer(1);c.showPage()
        p=data['pages'][1]
        base(2);title(2)
        art('plant-and-bacterium.png',365,255,318,477)
        y=230
        for i,paragraph in enumerate(p['paragraphs']):
            y=text_block(2,f'p2.paragraph.{i}',paragraph,48,y,295,17,26,'body',max_height=205)+18
        if y>770: raise ValueError(f'Cells page 2 too tall: {y}')
        specs=[
            ('叶片细胞',385,220,140,[]),
            ('细胞壁',576,240,100,[(611,263),(628,290)]),
            ('叶绿体',570,594,100,[(605,594),(590,564),(570,524)]),
            ('大液泡',433,393,105,[]),
            ('细菌',391,737,75,[]),
            ('拟核（DNA）',528,737,144,[(575,737),(566,716),(503,658)])
        ]
        for label,x,top,width,points in specs:
            if points:leader(points)
            text_block(2,'p2.label.'+label,label,x,top,width,15,22,'label','Heading')
        text_block(2,'p2.closing',p['closing'],48,782,624,18,28,'body',max_height=115)
        footer(2);c.showPage()
    c.save()

    reader=PdfReader(target)
    if len(reader.pages)!=2:
        raise ValueError('Expected exactly two pages')
    for i,page in enumerate(reader.pages):
        actual=''.join(page.extract_text().split())
        expected=data['pages'][i]
        for value in [expected['title'],*expected['paragraphs'],*expected['labels'],expected.get('lead',''),expected.get('closing','')]:
            if ''.join(value.split()) not in actual:
                raise ValueError(f'PDF text differs on page {i+1}')

    document=pdfium.PdfDocument(str(target))
    for i in range(2):
        bitmap=document[i].render(scale=2)
        bitmap.to_pil().convert('RGB').save(output/f'page-{i+1:02d}.png',optimize=True)
    document.close()
    (ROOT/f'.build/layout-{case}.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/f'.build/rendered-text-{case}.json').write_text(json.dumps(rendered,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'case':case,'pages':2,'pdf_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'png_size':[1440,1920],'body_size_pt':[18,17],'paragraph_bottoms_checked':True}))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['solar-system','cells'],default='solar-system');ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    build(args.output or ROOT/'examples'/args.case/'output',args.case)
