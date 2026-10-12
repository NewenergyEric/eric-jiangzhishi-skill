"""Check an exported layout manifest. Does not replace visual proofing.

Manifest keys: issues, minimum_sizes, blocks, text. Blocks include page, role,
x/y/w/h (actual), allocated_h, size; text lines include page, x/y/w/h, role.
Use the page's own coordinate unit consistently, usually PDF points.
"""
from pathlib import Path
import argparse,json,sys

def check(data,width=600,height=800):
    issues=list(data.get('issues',[]))
    for b in data.get('blocks',[]):
        minimum=data.get('minimum_sizes',{}).get(b['role'],0)
        if b['size']<minimum:
            issues.append(dict(type='below_type_floor',page=b['page'],role=b['role'],size=b['size'],minimum=minimum))
        if b['h']>b.get('allocated_h',b['h'])+.1:
            issues.append(dict(type='box_overflow',page=b['page'],role=b['role']))
    lines=data.get('text',[])
    for i,a in enumerate(lines):
        floor=data.get('minimum_sizes',{}).get(a.get('role'),0)
        if a['size']<floor:
            issues.append(dict(type='below_type_floor',page=a['page'],role=a['role'],size=a['size'],minimum=floor))
        if a['x']<0 or a['y']<0 or a['x']+a['w']>width or a['y']+a['h']>height:
            issues.append(dict(type='page_overflow',page=a['page'],text=a['text']))
        for b in lines[i+1:]:
            if a['page']!=b['page']:continue
            if a.get('block') is not None and a.get('block')==b.get('block'):continue
            dx=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])
            dy=min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])
            if dx>1 and dy>1:
                issues.append(dict(type='text_overlap',page=a['page'],text_a=a['text'],text_b=b['text'],intersection=[round(dx,2),round(dy,2)]))
    return issues

def main():
    p=argparse.ArgumentParser();p.add_argument('manifest',type=Path);p.add_argument('--report',type=Path)
    p.add_argument('--width',type=float,default=600);p.add_argument('--height',type=float,default=800)
    args=p.parse_args();data=json.loads(args.manifest.read_text(encoding='utf-8'))
    issues=check(data,args.width,args.height)
    report=dict(passed=not issues,issues=issues,
                limitation='Checks recorded text geometry and size floors. Inspect actual glyphs, sign interiors, contrast, artwork and reading flow separately.')
    serialized=json.dumps(report,ensure_ascii=False,indent=2)
    if args.report:args.report.write_text(serialized,encoding='utf-8')
    print(serialized);return int(bool(issues))
if __name__=='__main__':sys.exit(main())
