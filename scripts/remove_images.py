#!/usr/bin/env python3
"""
Script to select images from data/images/<document>, delete them, and remove
references and metadata entries from data/processed/<document>.md.

Usage:
  python remove_images.py --input-dir documento
  python remove_images.py --input-dir documento --dry-run
  python remove_images.py --input-dir documento --select 1,3-5 --yes
"""
import argparse
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
IMGS_DIR = BASE_DIR / os.getenv("IMGS_DIR", "data/images")
PROCESSED_DOCUMENTS_DIR = BASE_DIR / os.getenv("PROCESSED_DOCUMENTS_DIR", "data/processed")

IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp', '.tif', '.tiff'}
IMAGE_INDEX_RE = re.compile(r'P(\d+)_I(\d+)', flags=re.IGNORECASE)


def resolve_path(path):
    path = Path(path)
    if path.is_absolute():
        return path
    return BASE_DIR / path


def workspace_rel(path):
    path = Path(path).resolve()
    try:
        return path.relative_to(BASE_DIR.resolve()).as_posix()
    except ValueError:
        return path.name


def normalize_ref(value):
    return value.strip().replace('\\', '/')


def list_images(img_dir):
    files = [f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))]
    images = [f for f in files if os.path.splitext(f)[1].lower() in IMAGE_EXTS]
    images.sort(key=image_sort_key)
    return images


def image_sort_key(name):
    match = IMAGE_INDEX_RE.search(name)
    if match:
        page_num = int(match.group(1))
        image_num = int(match.group(2))
        return (page_num, image_num, name.lower())
    return (float('inf'), float('inf'), name.lower())


def print_images(images):
    for i, name in enumerate(images, start=1):
        size = os.path.getsize(os.path.join(args.img_dir, name))
        print(f"{i:3}: {name} ({size/1024:.1f} KB)")


def parse_selection(sel, max_index):
    sel = sel.replace(' ', '')
    chosen = set()
    for part in sel.split(','):
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            a = int(a); b = int(b)
            for v in range(a, b+1):
                if 1 <= v <= max_index:
                    chosen.add(v-1)
        else:
            v = int(part)
            if 1 <= v <= max_index:
                chosen.add(v-1)
    return sorted(chosen)


def make_backup(md_path):
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    backup = md_path + f'.bak.{ts}'
    shutil.copy2(md_path, backup)
    return backup


def clean_markdown(md_path, removed_paths, dry_run=False):
    removed_refs = {workspace_rel(path) for path in removed_paths}
    removed_names = {os.path.basename(path) for path in removed_paths}

    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    original = text
    total_removed = 0

    def is_removed_ref(value):
        value = normalize_ref(value)
        return value in removed_refs or os.path.basename(value) in removed_names

    # First: safely remove whole ```metadata``` blocks only when their 'imagen:' line
    # matches one of the selected image paths.
    def remove_metadata_blocks(text):
        lines = text.splitlines(keepends=True)
        out_lines = []
        i = 0
        removed_blocks = 0
        while i < len(lines):
            if lines[i].strip().lower().startswith('```metadata'):
                start = i
                i += 1
                found_image = False
                # scan until closing ``` or end
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    m = re.match(r'^\s*imagen\s*:\s*(.*)$', lines[i], flags=re.IGNORECASE)
                    if m:
                        found_image = is_removed_ref(m.group(1))
                    i += 1
                # include the closing ``` if present
                if i < len(lines) and lines[i].strip().startswith('```'):
                    end = i
                else:
                    end = i - 1
                i += 1
                if found_image:
                    removed_blocks += 1
                    # skip entire block
                    continue
                else:
                    # keep the block
                    out_lines.extend(lines[start:end+1])
            else:
                out_lines.append(lines[i])
                i += 1
        return ''.join(out_lines), removed_blocks

    text, md_removed = remove_metadata_blocks(text)
    total_removed += md_removed

    # Next: remove explicit image references (inline markdown, html <img>, and reference defs)
    for ref in sorted(removed_refs | removed_names, key=len, reverse=True):
        ref_esc = re.escape(ref)
        # Only remove inline images or links that contain the exact path or filename.
        patterns = [
            rf'!\[[^\]]*\]\([^\)]*{ref_esc}[^\)]*\)',
            rf'\[[^\]]*\]\([^\)]*{ref_esc}[^\)]*\)',
            rf'^\s*\[[^\]]+\]:\s*\S*{ref_esc}\S*\s*$',
            rf'<img[^>]*src=["\"][^"\']*{ref_esc}[^"\']*["\"][^>]*>',
        ]
        for pat in patterns:
            new_text, n = re.subn(pat, '', text, flags=re.IGNORECASE | re.MULTILINE)
            if n:
                total_removed += n
                text = new_text

    # Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    if dry_run:
        # Count occurrences of filenames in original for reporting
        removed_count = 0
        for ref in removed_refs:
            removed_count += len(re.findall(re.escape(ref), original.replace('\\', '/'), flags=re.IGNORECASE))
        return {'changed': original != text, 'matches': removed_count}

    if original != text:
        backup = make_backup(md_path)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return {'changed': True, 'backup': backup, 'removed_items': total_removed}
    else:
        return {'changed': False}


def confirm(prompt):
    resp = input(prompt + ' [y/N]: ').strip().lower()
    return resp in ('y', 'yes')


def remove_files(img_dir, names, dry_run=False):
    removed = []
    errors = []
    for name in names:
        path = os.path.join(img_dir, name)
        if dry_run:
            print(f'[dry-run] would remove {path}')
            removed.append(path)
            continue
        try:
            os.remove(path)
            removed.append(path)
        except Exception as e:
            errors.append((name, str(e)))
    return removed, errors


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Remove images and clean markdown references')
    p.add_argument('--input-dir', help='Document/image folder name under data/images and data/processed')
    p.add_argument('--img-dir', help='Images directory')
    p.add_argument('--md', help='Markdown file to clean')
    p.add_argument('--dry-run', action='store_true', help='Show what would be removed without changing files')
    p.add_argument('--select', help='Non-interactive selection string, e.g. "1,3-5"')
    p.add_argument('--yes', action='store_true', help='Skip confirmation prompts')
    args = p.parse_args()

    if args.input_dir:
        doc_name = Path(args.input_dir).stem
        img_dir = resolve_path(args.img_dir) if args.img_dir else IMGS_DIR / doc_name
        md_path = resolve_path(args.md) if args.md else PROCESSED_DOCUMENTS_DIR / f'{doc_name}.md'
    else:
        img_dir = resolve_path(args.img_dir) if args.img_dir else IMGS_DIR
        md_path = resolve_path(args.md) if args.md else PROCESSED_DOCUMENTS_DIR / 'documento_completo.md'

    args.img_dir = str(img_dir)
    args.md = str(md_path)

    if not os.path.isdir(args.img_dir):
        print('Images directory not found:', args.img_dir)
        sys.exit(1)
    if not os.path.isfile(args.md):
        print('Markdown file not found:', args.md)
        sys.exit(1)

    images = list_images(args.img_dir)
    if not images:
        print('No images found in', args.img_dir)
        sys.exit(0)

    print('Found images:')
    for i, name in enumerate(images, start=1):
        size = os.path.getsize(os.path.join(args.img_dir, name))
        print(f"{i:3}: {name} ({size/1024:.1f} KB)")

    if args.select:
        try:
            indices = parse_selection(args.select, len(images))
        except Exception as e:
            print('Invalid --select value:', e)
            sys.exit(1)
    else:
        sel = input('\nEscriba números separados por comas o rangos (ej. 1,3-5): ').strip()
        if not sel:
            print('No selection, exiting.')
            sys.exit(0)
        try:
            indices = parse_selection(sel, len(images))
        except Exception as e:
            print('Selección inválida:', e)
            sys.exit(1)

    chosen = [images[i] for i in indices]
    if not chosen:
        print('No valid images selected, exiting.')
        sys.exit(0)
    chosen_paths = [os.path.join(args.img_dir, name) for name in chosen]

    print('\nSelected images:')
    for name in chosen:
        print('-', name)

    if not args.yes:
        if not confirm('Confirmar borrado de los archivos listados y limpieza del markdown?'):
            print('Aborted by user.')
            sys.exit(0)

    # Dry-run behavior
    if args.dry_run:
        print('\n-- Dry run: scanning markdown for references --')
        report = clean_markdown(args.md, chosen_paths, dry_run=True)
        print('Matches found (approx):', report.get('matches', 0))
        print('\nDry-run complete. No files were deleted.')
        sys.exit(0)

    removed, errors = remove_files(args.img_dir, chosen, dry_run=False)
    print('\nRemoved files:')
    for r in removed:
        print('-', os.path.basename(r))
    if errors:
        print('\nErrors:')
        for name, err in errors:
            print(f'- {name}: {err}')

    print('\nCleaning markdown file:', args.md)
    result = clean_markdown(args.md, removed, dry_run=False)
    if result.get('changed'):
        print('Markdown updated. Backup created at', result.get('backup'))
        print('Total removed occurrences (approx):', result.get('removed_items'))
    else:
        print('No references found in markdown.')

    print('\nDone.')
