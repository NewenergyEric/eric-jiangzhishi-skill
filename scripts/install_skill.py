"""Copy one complete Skill to a user-selected directory; never overwrite."""
from pathlib import Path
import argparse
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('knowledge-to-friendly-product', 'knowledge-card-art-direction')

def install(name, destination):
    source = ROOT / 'skills' / name
    target = destination.expanduser().resolve() / name
    if not (source / 'SKILL.md').is_file():
        raise ValueError('Incomplete source Skill')
    if target.exists():
        raise FileExistsError('Target already exists; choose another destination')
    if source == target or source in target.parents:
        raise ValueError('Destination cannot be inside the source Skill')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    return target

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name', choices=NAMES)
    parser.add_argument('--dest', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = install(args.name, args.dest)
    except (ValueError, FileExistsError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    print('Copied complete Skill:', result)
    print('Host auto-discovery is a separate check.')
