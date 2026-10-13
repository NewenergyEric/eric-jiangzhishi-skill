"""Small, local README labels in the guide's paper and ink palette."""
from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parents[1]
BADGES=[
    ('license',142,'License','MIT','#C5D6B8','M8 5h8v14H8z M10 9h4 M10 12h4 M10 15h3'),
    ('skills',168,'Skills','2 independent','#E4C36D','M4 6q5-2 8 0q3-2 8 0v13q-5-2-8 0q-3-2-8 0z M12 6v13'),
    ('languages',159,'Read','EN + 中文','#C9BADA','M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18 M3 12h18 M12 3q-7 9 0 18q7-9 0-18'),
    ('formats',168,'Make','PDF · MP4 · GIF','#A9C8CE','M4 5h16v12H4z M10 8l5 3-5 3z M8 21h8 M12 17v4'),
]

def build():
    folder=ROOT/'media/badges';folder.mkdir(parents=True,exist_ok=True)
    for name,width,label,value,color,icon in BADGES:
        split=78
        svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="30" viewBox="0 0 {width} 30" role="img" aria-label="{escape(label+' '+value)}">
<title>{escape(label+' '+value)}</title>
<rect width="{width}" height="30" rx="5" fill="{color}"/>
<path d="M5 0H{split}V30H5a5 5 0 0 1-5-5V5a5 5 0 0 1 5-5" fill="#29483F"/>
<path d="{icon}" transform="translate(5 3)" fill="none" stroke="#FCF8EE" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
<g font-family="Arial,Microsoft YaHei,sans-serif" font-size="11" font-weight="600" text-anchor="middle">
<text x="52" y="19" fill="#FCF8EE">{escape(label)}</text><text x="{(split+width)/2}" y="19" fill="#192F2A">{escape(value)}</text>
</g></svg>
'''
        (folder/(name+'.svg')).write_text(svg,encoding='utf-8',newline='\n')

if __name__=='__main__':build()
