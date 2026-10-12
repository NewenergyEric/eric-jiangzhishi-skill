"""Compare immutable source files or semantic JSON snapshots using stdlib only."""
from pathlib import Path
import argparse,hashlib,json,sys

def compare(a,b,path='$'):
    if type(a)!=type(b):return [path+': type changed']
    if isinstance(a,dict):
        out=[]
        for key in sorted(a.keys()|b.keys()):
            if key not in a or key not in b:out.append(path+'.'+key+': key changed')
            else:out.extend(compare(a[key],b[key],path+'.'+key))
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [path+': length changed']
        return [err for i,(x,y) in enumerate(zip(a,b)) for err in compare(x,y,f'{path}[{i}]')]
    return [] if a==b else [path+': value changed']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('baseline',type=Path);ap.add_argument('candidate',type=Path);ap.add_argument('--report',type=Path);args=ap.parse_args()
    a=args.baseline.read_bytes();b=args.candidate.read_bytes()
    if args.baseline.suffix==args.candidate.suffix=='.json':
        differences=compare(json.loads(a.decode('utf-8-sig')),json.loads(b.decode('utf-8-sig')))
    else:differences=[] if a==b else ['$: file bytes changed']
    report={'unchanged':not differences,'baseline_sha256':hashlib.sha256(a).hexdigest(),'candidate_sha256':hashlib.sha256(b).hexdigest(),'differences':differences}
    data=json.dumps(report,ensure_ascii=False,indent=2)
    if args.report:args.report.write_text(data,encoding='utf-8')
    print(data);return 0 if not differences else 1

if __name__=='__main__':sys.exit(main())
