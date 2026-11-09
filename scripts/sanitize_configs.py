"""Replace secrets in exported running-configs with <lab-secret>.

Usage:  python sanitize_configs.py <input_dir> <output_dir>
Reads every .txt file in input_dir and writes a cleaned copy to output_dir.
Always open the output and check it before you commit.
"""
import re
import sys
from pathlib import Path

RULES = [
    (r'^(\s*enable (?:secret|password) )(?:\d+ )?\S+', r'\1<lab-secret>'),
    (r'^(\s*username \S+ (?:privilege \d+ )?(?:secret|password) )(?:\d+ )?\S+', r'\1<lab-secret>'),
    (r'^(\s*crypto isakmp key )(?:\d+ )?\S+', r'\1<lab-secret>'),
    (r'(message-digest-key \d+ md5 )(?:\d+ )?\S+', r'\1<lab-secret>'),
    (r'^(\s*password )(?:\d+ )?\S+', r'\1<lab-secret>'),
]
COMPILED = [(re.compile(p, re.M), r) for p, r in RULES]


def clean(text):
    for pattern, repl in COMPILED:
        text = pattern.sub(repl, text)
    return text


def main():
    if len(sys.argv) != 3:
        sys.exit('usage: python sanitize_configs.py <input_dir> <output_dir>')
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.glob('*.txt')):
        (dst / f.name).write_text(clean(f.read_text()))
        print(f'[OK] {f.name}')


if __name__ == '__main__':
    main()
