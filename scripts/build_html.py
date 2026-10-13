"""Build accessible reading versions from the same content JSON."""
from pathlib import Path
import html
import json
ROOT = Path(__file__).resolve().parents[1]
def e(text):
    return html.escape(text)
STYLE = """
:root{color-scheme:light;--ink:#192f2a;--paper:#fcf8ee}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:system-ui,"Microsoft YaHei",sans-serif;line-height:1.85}
main{max-width:820px;margin:auto;padding:40px 24px 64px}a{color:#265f52;text-underline-offset:4px}
nav{font-size:15px;display:flex;gap:20px;flex-wrap:wrap}h1{font-size:clamp(28px,5vw,42px);line-height:1.35;margin:48px 0 16px}
h2{font-size:clamp(25px,4vw,34px);line-height:1.45;margin-top:56px}p{font-size:19px}figure{margin:26px 0}
img{display:block;width:100%;height:auto;border-radius:4px}figcaption,.note{font-size:14px;color:#4b5f53}section+section{border-top:1px solid #c8d0bf;margin-top:48px}
footer{border-top:1px solid #c8d0bf;margin-top:48px;padding-top:20px}summary{cursor:pointer}a:focus-visible,summary:focus-visible{outline:3px solid #587a68;outline-offset:5px}
@media(max-width:480px){main{padding:24px 20px 48px}p{font-size:18px}h1{margin-top:32px}}
"""
def build(case, language='zh'):
    directory = ROOT / 'examples' / case
    english = language == 'en'
    suffix = '.en' if english else ''
    data = json.loads((directory/('content'+suffix+'.json')).read_text(encoding='utf-8'))
    sections = []
    for i,p in enumerate(data['pages'],1):
        paras = ([p['lead']] if p.get('lead') else []) + p['paragraphs'] + ([p['closing']] if p.get('closing') else [])
        body = ''.join('<p>'+e(t)+'</p>' for t in paras)
        caption = ('Original Chinese artwork; the complete English text is above. ' if english else '本页内容已在上方以可选择文字完整呈现。') + p['note']
        labels = p.get('scene_labels',p.get('labels',[]))
        if labels:
            body += '<p class="note">'+('In the illustration: ' if english else '画面索引：')+e(('; ' if english else '；').join(labels))+('.' if english else '。')+'</p>'
        summary = 'View original Chinese page '+str(i) if english else '查看第'+str(i)+'页图文成稿'
        sections.append('<section aria-labelledby="page'+str(i)+'"><h2 id="page'+str(i)+'">'+e(p['title']).replace('\n','<br>')+'</h2>'+body+'<details><summary>'+summary+'</summary><figure><img loading="lazy" src="output/page-'+str(i).zfill(2)+'.png" alt="'+e(p['title'].replace('\n',' '))+'; '+e('; '.join(labels))+'"><figcaption>'+e(caption)+'</figcaption></figure></details></section>')
    nav = [('Get started' if english else '上手入口','../../docs/getting-started'+suffix+'.html'),('Original Chinese PDF' if english else '下载两页 PDF','output/'+case+'.pdf'),('Sources (Chinese notes)' if english else '完整来源','sources.md'),('中文' if english else 'English','read.html' if english else 'read.en.html')]
    note = 'The complete English text of the two-page guide, for phones and assistive reading tools. Expand each section to see the original Chinese illustrated page.' if english else '同一份两页案例的文字阅读版，适合手机与辅助阅读工具。插画细节可展开每页成稿查看。'
    document = '<!doctype html><html lang="'+('en' if english else 'zh-CN')+'"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(data['title'])+' · '+('Making Sense Together' if english else '一起读懂')+'</title><style>'+STYLE+'</style><main><nav aria-label="'+('Document navigation' if english else '文档导航')+'">'+''.join('<a href="'+url+'">'+label+'</a>' for label,url in nav)+'</nav><h1>'+e(data['title'])+'</h1><p class="note">'+note+'</p>'+''.join(sections)+'<footer><a href="process.md">'+('Production notes (Chinese)' if english else '制作过程')+'</a> · <a href="../../THIRD_PARTY_NOTICES'+suffix+'.md">'+('Licenses' if english else '素材许可')+'</a></footer></main></html>\n'
    (directory/('read'+suffix+'.html')).write_text(document,encoding='utf-8')
if __name__=='__main__':
    for case in ['solar-system','cells']:
        for language in ['zh','en']:build(case,language)
    print('Built four reading pages from the Chinese and English content files')
