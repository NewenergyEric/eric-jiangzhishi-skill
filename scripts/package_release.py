"""Create reproducible ZIPs from the reviewed public allowlist only."""
from pathlib import Path
import hashlib
import json
import zipfile
from verify_project import audit, manifest
ROOT=Path(__file__).resolve().parents[1]

def package():
    result=audit()
    if not result['passed']:raise ValueError('Public audit failed')
    version=(ROOT/'VERSION').read_text().strip()
    output=ROOT/'dist';output.mkdir(exist_ok=True)
    files=manifest()
    groups={
        f'eric-jiangzhishi-skill-{version}.zip':files,
        f'eric-jiangzhishi-skills-{version}.zip':[p for p in files if p.startswith('skills/')]+['LICENSE','VERSION','docs/skills-package.md','docs/skills-package.en.md'],
    }
    products=[]
    for name,members in groups.items():
        path=output/name
        with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for member in sorted(members):
                info=zipfile.ZipInfo(member,date_time=(2026,10,12,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o644<<16
                archive.writestr(info,(ROOT/member).read_bytes())
        with zipfile.ZipFile(path) as archive:
            if archive.namelist()!=sorted(members):raise ValueError('ZIP membership mismatch')
            for member in members:
                if archive.read(member)!=(ROOT/member).read_bytes():raise ValueError('ZIP bytes mismatch')
        products.append(path)
    for case in ['solar-system','cells']:
        for locale in ['', '.en']:
            path=output/f'{case}{locale}.pdf';path.write_bytes((ROOT/'examples'/case/'output'/f'{case}{locale}.pdf').read_bytes());products.append(path)
    for ratio in ['wide','square','vertical']:
        directory=ROOT/'media/intro'/(ratio if ratio!='wide' else '')
        for locale in ['', '.en']:
            for ext in ['mp4','gif']:
                name='intro'+('' if ratio=='wide' else '-'+ratio)+locale+'.'+ext
                path=output/name
                path.write_bytes((directory/('intro'+locale+'.'+ext)).read_bytes())
                products.append(path)
    sums=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in products)
    (output/'SHA256SUMS.txt').write_text(sums,encoding='utf-8')
    print(json.dumps({'version':version,'assets':[p.name for p in products]+['SHA256SUMS.txt'],'zip_members_verified':True}))
if __name__=='__main__':package()
