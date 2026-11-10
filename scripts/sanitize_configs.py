"""Clean exported Cisco configs for GitHub.

Usage:  python sanitize_configs.py <input_dir> <output_dir>

For every .txt file in input_dir this script:
  1. keeps only the last 'show running-config' output (drops boot messages, logs, login prompts)
  2. replaces passwords, secrets and keys with <lab-secret>
  3. replaces the licence serial number with <serial>
and writes the result to output_dir. Open the results and check them before you commit.
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
    (r'^(\s*license udi pid \S+ sn )\S+', r'\1<serial>'),
]
COMPILED = [(re.compile(p, re.M), r) for p, r in RULES]


def extract_config(text):
    text = text.replace('\r', '')
    start = text.rfind('Building configuration')
    if start != -1:
        text = text[start:]
    end = re.search(r'^end\s*$', text, re.M)
    if end:
        text = text[:end.end()] + '\n'
    return text


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
        text = clean(extract_config(f.read_text(errors='ignore')))
        (dst / f.name).write_text(text)
        warn = '' if re.search(r'^hostname ', text, re.M) else '  [WARN] no hostname line: export looks incomplete, export it again'
        print(f'[OK] {f.name}{warn}')


if __name__ == '__main__':
    main()
