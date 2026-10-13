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
def build(case):
    directory = ROOT / 'examples' / case
    data = json.loads((directory/'content.json').read_text(encoding='utf-8'))
    sections = []
    for i,p in enumerate(data['pages'],1):
        paras = ([p['lead']] if p.get('lead') else []) + p['paragraphs'] + ([p['closing']] if p.get('closing') else [])
        body = ''.join('<p>'+e(t)+'</p>' for t in paras)
        caption = '本页内容已在上方以可选择文字完整呈现。' + p['note']
        labels = p.get('scene_labels',p.get('labels',[]))
        if labels:
            body += '<p class="note">画面索引：'+e('；'.join(labels))+'。</p>'
        sections.append('<section aria-labelledby="page'+str(i)+'"><h2 id="page'+str(i)+'">'+e(p['title']).replace('\n','<br>')+'</h2>'+body+'<details><summary>查看第'+str(i)+'页图文成稿</summary><figure><img loading="lazy" src="output/page-'+str(i).zfill(2)+'.png" alt="'+e(p['title'].replace('\n',''))+'；'+e('；'.join(labels))+'"><figcaption>'+e(caption)+'</figcaption></figure></details></section>')
    document = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(data['title'])+'</title><style>'+STYLE+'</style><main><nav aria-label="文档导航"><a href="../../docs/getting-started.html">上手入口</a><a href="output/'+case+'.pdf">下载两页 PDF</a><a href="sources.md">完整来源</a></nav><h1>'+e(data['title'])+'</h1><p class="note">同一份两页案例的文字阅读版，适合手机与辅助阅读工具。插画细节可展开每页成稿查看。</p>'+''.join(sections)+'<footer><a href="process.md">制作过程</a> · <a href="../../THIRD_PARTY_NOTICES.md">素材许可</a></footer></main></html>'
    (directory/'read.html').write_text(document,encoding='utf-8')
if __name__=='__main__':
    for case in ['solar-system','cells']:build(case)
    print('Built two reading versions from content.json')
