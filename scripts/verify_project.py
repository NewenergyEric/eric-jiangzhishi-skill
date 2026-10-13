"""Audit only the exact public allowlist, local links, media and staged bytes."""
from pathlib import Path
import argparse
import hashlib
import html
import importlib.util
import json
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit
from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
TEXT = {'.md','.txt','.json','.yaml','.py','.html','.mjs'}
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
    skill_entries = sorted(name for name in files if re.fullmatch(r'skills/[^/]+/SKILL\.md',name))
    if skill_entries != ['skills/knowledge-card-art-direction/SKILL.md','skills/knowledge-to-friendly-product/SKILL.md']:
        errors.append({'rule':'two_independent_skills'})
    for case in ('solar-system','cells'):
        base=root/'examples'/case
        content=json.loads((base/'content.json').read_text(encoding='utf-8'))
        english=json.loads((base/'content.en.json').read_text(encoding='utf-8'))
        if english['translationOf']['sha256'] != hashlib.sha256((base/'content.json').read_bytes()).hexdigest():
            errors.append({'rule':'translation_source_changed','file':case})
        if len(content['pages']) != len(english['pages']) or len(english['pages']) != 2:
            errors.append({'rule':'translation_page_count','file':case})
        for language, data in [('zh',content),('en',english)]:
            reading=html.unescape(re.sub(r'<[^>]+>',' ',(base/('read.en.html' if language=='en' else 'read.html')).read_text(encoding='utf-8')))
            reading=''.join(reading.split())
            for page in data['pages']:
                for item in [page['title'],page.get('lead',''),*page['paragraphs'],page.get('closing',''),*page.get('labels',[])]:
                    if ''.join(item.split()) not in reading:errors.append({'rule':'reading_text_mismatch','file':case,'language':language})
        for original,translated in zip(content['pages'],english['pages']):
            if original['id']!=translated['id'] or len(original['paragraphs'])!=len(translated['paragraphs']) or len(original['labels'])!=len(translated['labels']):
                errors.append({'rule':'translation_structure_mismatch','file':case})
        pdf=PdfReader(base/'output'/f'{case}.pdf')
        for i,page in enumerate(pdf.pages):
            actual=''.join(page.extract_text().split())
            data=content['pages'][i]
            for item in [data['title'],data.get('lead',''),*data['paragraphs'],data.get('closing',''),*data.get('labels',[]),*data.get('scene_labels',[])]:
                if ''.join(item.split()) not in actual:errors.append({'rule':'pdf_content_mismatch','file':case,'page':i+1})
            with Image.open(base/'output'/f'page-{i+1:02d}.png') as im:
                if im.size!=(1440,1920):errors.append({'rule':'preview_size','file':case})
    media=root/'media/intro'
    profiles=json.loads((media/'formats.json').read_text(encoding='utf-8'))['formats']
    for locale in ['', '.en']:
        story_path=media/f'story{locale}.json'
        story=json.loads(story_path.read_text(encoding='utf-8'))
        shared_source=None
        shared_copy=None
        for profile in profiles:
            directory=media/(profile['id'] if profile['id']!='wide' else '')
            label=profile['id']+'/'+(locale or 'zh')
            report=json.loads((directory/f'report{locale}.json').read_text(encoding='utf-8'))
            if hashlib.sha256(story_path.read_bytes()).hexdigest()!=report['storySha256']:
                errors.append({'rule':'video_story_changed_without_rebuild','variant':label})
            if report['version']!=(root/'VERSION').read_text().strip() or report['language']!=story['language'] or report['format']!=profile:
                errors.append({'rule':'video_version_language_or_format','variant':label})
            for name,expected in report['sourceHashes'].items():
                if name not in allowed or hashlib.sha256((root/name).read_bytes()).hexdigest()!=expected:
                    errors.append({'rule':'video_source_changed_without_rebuild','file':name})
            for suffix in ['mp4','gif']:
                payload=(directory/f'intro{locale}.{suffix}').read_bytes();record=report['outputs'][suffix]
                if hashlib.sha256(payload).hexdigest()!=record['sha256'] or len(payload)!=record['bytes']:
                    errors.append({'rule':'video_output_mismatch','variant':label,'format':suffix})
                if len(payload)>profile['budgets'][suffix+'Bytes']:
                    errors.append({'rule':'video_size_budget','variant':label,'format':suffix})
            movie_record=report['outputs']['mp4']
            if (movie_record['width'],movie_record['height'],movie_record['frames'],movie_record['seconds'])!=(profile['width'],profile['height'],round(story['duration']*story['fps']),story['duration']):
                errors.append({'rule':'mp4_geometry_frames_or_duration','variant':label})
            with Image.open(directory/f'intro{locale}.gif') as gif:
                duration=0
                for frame in range(gif.n_frames):
                    gif.seek(frame);duration+=gif.info.get('duration',0)
                expected_size=(profile['gifWidth'],round(profile['height']*profile['gifWidth']/profile['width']))
                if gif.size!=expected_size or gif.n_frames!=round(story['duration']*profile['gifFps']) or duration!=story['duration']*1000:
                    errors.append({'rule':'gif_geometry_or_duration','variant':label})
            poster=directory/f'poster{locale}.png'
            if hashlib.sha256(poster.read_bytes()).hexdigest()!=report['posterSha256']:
                errors.append({'rule':'video_poster_mismatch','variant':label})
            with Image.open(poster) as im:
                if im.size!=(profile['width'],profile['height']):errors.append({'rule':'video_poster_geometry','variant':label})
            cover=directory/f'cover{locale}.png'
            if hashlib.sha256(cover.read_bytes()).hexdigest()!=report['cover']['sha256'] or cover.stat().st_size!=report['cover']['bytes'] or cover.stat().st_size>profile['budgets']['coverBytes']:
                errors.append({'rule':'video_cover_mismatch_or_budget','variant':label})
            with Image.open(cover) as im:
                if im.width!=profile['coverWidth']:errors.append({'rule':'video_cover_geometry','variant':label})
            audit_file=directory/f'audit{locale}.json'
            layout=json.loads(audit_file.read_text(encoding='utf-8'))
            if hashlib.sha256(audit_file.read_bytes()).hexdigest()!=report['auditSha256']:
                errors.append({'rule':'layout_audit_hash','variant':label})
            if layout['mode']!='native' or layout['embeddedMasterVideo'] is not False or layout['errors'] or layout.get('allFramesChecked')!=round(story['duration']*story['fps']) or any(sample['overlaps'] for sample in layout['samples']):
                errors.append({'rule':'native_layout_audit','variant':label})
            copy={sample['frame']:{row['id']:''.join(row['text'].split()) for row in sample['rows'] if row['kind']=='text'} for sample in layout['samples']}
            if shared_source is None:
                shared_source=layout['sourceHash'];shared_copy=copy
            elif layout['sourceHash']!=shared_source or copy!=shared_copy:
                errors.append({'rule':'ratio_source_or_copy_mismatch','variant':label})
            if layout['sourceHash']!=report['sourceHash'] or not report['fullDecodeVerified']:
                errors.append({'rule':'media_verification_record','variant':label})
        readme=(root/('README.en.md' if locale else 'README.md')).read_text(encoding='utf-8')
        if f'](media/intro/cover{locale}.png)' not in readme or re.search(r'!\[[^\]]*\]\([^)]*\.gif\)',readme):
            errors.append({'rule':'readme_small_cover','language':locale or 'zh'})
    if staged:
        indexed=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode('utf-8').split('\0')
        if set(filter(None,indexed))!=allowed:errors.append({'rule':'git_allowlist_mismatch'})
        for name in files:
            content=subprocess.check_output(['git','show',':'+name],cwd=root)
            if content!=(root/name).read_bytes():errors.append({'rule':'staged_bytes_differ','file':name})
    return {'passed':not errors,'files':len(files),'checks':['exact_allowlist','local_links','privacy_patterns','media_metadata','two_independent_skills','pdf_text','two_pages_per_case','bilingual_reading_text','translation_source_and_structure','preview_dimensions','six_video_source_and_output_hashes','media_size_budgets','gif_frames_and_duration','native_ratio_copy_parity','small_readme_covers']+(['staged_bytes'] if staged else []),'errors':errors,'limits':'Patterns and geometry do not replace human privacy review, visual proofing or host loading tests.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--staged',action='store_true')
    args=parser.parse_args()
    result=audit(staged=args.staged)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(0 if result['passed'] else 1)
