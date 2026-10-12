"""Audit only the exact public allowlist, local links, media and staged bytes."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
TEXT = {'.md','.txt','.json','.yaml','.py','.html'}
PRIVATE = [
    ('private_path', re.compile(r'(?i)(?:\b[a-z]:[\\/]|/(?:Users|home)/[a-z0-9_])')),
    ('access_token', re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{25,})')),
    ('private_key', re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),
    ('thread_identifier', re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b',re.I)),
    ('contact_email', re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')),
]

def manifest(root=ROOT):
    files=json.loads((root/'publish-files.json').read_text(encoding='utf-8'))['files']
    if files!=sorted(set(files)):raise ValueError('Allowlist must be sorted and unique')
    for name in files:
        p=Path(name)
        if p.is_absolute() or '..' in p.parts or name.startswith(('.git/','.build/','dist/')):raise ValueError('Unsafe allowlist member')
        if not (root/p).is_file():raise ValueError('Missing allowlist file: '+name)
    return files

def audit(root=ROOT, staged=False):
    files=manifest(root); allowed=set(files); errors=[]
    def scan(name, value):
        # OFL attribution is intentionally retained as third-party license text.
        for rule,pattern in PRIVATE:
            if name=='vendor/fonts/OFL.txt' and rule=='contact_email':continue
            for match in pattern.finditer(value):
                line=value[:match.start()].count('\n')+1
                errors.append({'rule':rule,'file':name,'line':line})
    for name in files:
        p=root/name
        if p.suffix in TEXT or p.name in {'LICENSE','VERSION','.gitignore','.gitattributes'}:
            content=p.read_text(encoding='utf-8-sig');scan(name,content)
            refs=[]
            if p.suffix=='.md':
                refs+=re.findall(r'!?\[[^\]\n]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)',content)
            if p.suffix=='.html':
                refs+=re.findall(r'(?:href|src)="([^"]+)"',content)
            if p.suffix=='.json':json.loads(content)
            for ref in refs:
                if urlsplit(ref).scheme or ref.startswith(('#','//')):continue
                target=(p.parent/unquote(ref.split('#')[0].split('?')[0])).resolve()
                try:relative=target.relative_to(root.resolve()).as_posix()
                except ValueError:relative=''
                if relative not in allowed:errors.append({'rule':'missing_local_reference','file':name,'target':ref})
        elif p.suffix=='.png':
            with Image.open(p) as im:
                im.verify()
            with Image.open(p) as im:
                if im.info:errors.append({'rule':'unexpected_png_metadata','file':name,'keys':sorted(im.info)})
        elif p.suffix=='.pdf':
            doc=PdfReader(p)
            if len(doc.pages)!=2:errors.append({'rule':'pdf_page_count','file':name})
            scan(name,json.dumps(dict(doc.metadata or {}),ensure_ascii=False))
            for page in doc.pages:scan(name,page.extract_text())
    for case in ('solar-system','warcraft'):
        base=root/'examples'/case
        content=json.loads((base/'content.json').read_text(encoding='utf-8'))
        pdf=PdfReader(base/'output'/f'{case}.pdf')
        for i,page in enumerate(pdf.pages):
            actual=''.join(page.extract_text().split())
            data=content['pages'][i]
            for item in [data['title'],data.get('lead',''),*data['paragraphs'],data.get('closing',''),*data.get('labels',[]),*data.get('scene_labels',[])]:
                if ''.join(item.split()) not in actual:errors.append({'rule':'pdf_content_mismatch','file':case,'page':i+1})
            with Image.open(base/'output'/f'page-{i+1:02d}.png') as im:
                if im.size!=(1440,1920):errors.append({'rule':'preview_size','file':case})
    if staged:
        indexed=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode('utf-8').split('\0')
        if set(filter(None,indexed))!=allowed:errors.append({'rule':'git_allowlist_mismatch'})
        for name in files:
            content=subprocess.check_output(['git','show',':'+name],cwd=root)
            if content!=(root/name).read_bytes():errors.append({'rule':'staged_bytes_differ','file':name})
    return {'passed':not errors,'files':len(files),'checks':['exact_allowlist','local_links','privacy_patterns','media_metadata','pdf_text','two_pages_per_case','preview_dimensions']+(['staged_bytes'] if staged else []),'errors':errors,'limits':'Patterns and geometry do not replace human privacy review, visual proofing or host loading tests.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--staged',action='store_true')
    args=parser.parse_args()
    result=audit(staged=args.staged)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(0 if result['passed'] else 1)
