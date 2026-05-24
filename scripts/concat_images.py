"""Concatena imágenes de una carpeta en una sola imagen.

Uso:
    python concat_images.py --page 10
    python concat_images.py --input-dir static/img --pattern "Engstrom_P10_I*.png" --direction horizontal --output out.png

Dependencias:
    pip install pillow
"""

import os
import re
import glob
import math
import argparse
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image

load_dotenv()  # Cargar variables de entorno desde .env

BASE_DIR = Path(__file__).parent.parent
IMGS_DIR = BASE_DIR / os.getenv("IMGS_DIR", "data/images")
PROCESSED_DOCUMENTS_DIR = BASE_DIR / os.getenv("PROCESSED_DOCUMENTS_DIR", "data/processed")

IDX_RE = re.compile(r"I(\d+)")


def find_and_sort_images(input_dir, pattern):
    paths = glob.glob(os.path.join(input_dir, pattern))
    # extraer índice si existe y ordenar
    def idx_key(p):
        m = IDX_RE.search(os.path.basename(p))
        if m:
            return int(m.group(1))
        return os.path.basename(p)
    paths.sort(key=idx_key)
    return paths


def parse_selection(sel, max_index):
    sel = (sel or '').replace(' ', '')
    if not sel:
        return list(range(max_index))
    chosen = set()
    for part in sel.split(','):
        if not part:
            continue
        if '-' in part:
            try:
                a, b = part.split('-', 1)
                a = int(a); b = int(b)
            except ValueError:
                continue
            for v in range(a, b+1):
                if 1 <= v <= max_index:
                    chosen.add(v-1)
        else:
            try:
                v = int(part)
            except ValueError:
                continue
            if 1 <= v <= max_index:
                chosen.add(v-1)
    return sorted(chosen)


def concat_horizontal(images):
    widths = [im.width for im in images]
    heights = [im.height for im in images]
    total_w = sum(widths)
    max_h = max(heights) if heights else 0

    out = Image.new("RGB", (total_w, max_h), (255, 255, 255))
    x = 0
    for im in images:
        out.paste(im, (x, 0))
        x += im.width
    return out


def concat_vertical(images):
    widths = [im.width for im in images]
    heights = [im.height for im in images]
    max_w = max(widths) if widths else 0
    total_h = sum(heights)

    out = Image.new("RGB", (max_w, total_h), (255, 255, 255))
    y = 0
    for im in images:
        out.paste(im, (0, y))
        y += im.height
    return out


def concat_grid(images, cols=None):
    n = len(images)
    if n == 0:
        return None
    if cols is None or cols <= 0:
        cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    # compute row widths and heights
    row_widths = []
    row_heights = []
    grid = []
    it = iter(images)
    for r in range(rows):
        row = []
        w = 0
        h = 0
        for c in range(cols):
            try:
                im = next(it)
            except StopIteration:
                break
            row.append(im)
            w += im.width
            h = max(h, im.height)
        grid.append(row)
        row_widths.append(w)
        row_heights.append(h)

    total_w = max(row_widths) if row_widths else 0
    total_h = sum(row_heights) if row_heights else 0
    out = Image.new("RGB", (total_w, total_h), (255, 255, 255))

    y = 0
    for r, row in enumerate(grid):
        x = 0
        for im in row:
            out.paste(im, (x, y))
            x += im.width
        y += row_heights[r]
    return out


def load_images(paths):
    images = []
    for p in paths:
        try:
            with Image.open(p) as im:
                images.append(im.convert("RGB"))
        except Exception as e:
            print(f"No se pudo abrir {p}: {e}")
    return images


def delete_input_images(paths, output_path):
    output_path = os.path.abspath(output_path)
    for p in paths:
        p_abs = os.path.abspath(p)
        if p_abs == output_path:
            continue
        try:
            os.remove(p_abs)
            print(f"Eliminado: {p_abs}")
        except Exception as e:
            print(f"No se pudo eliminar {p_abs}: {e}")


def update_document_references(doc_path, image_paths, output_path):
    if not image_paths:
        return

    doc_path = os.path.abspath(doc_path)
    output_path = os.path.abspath(output_path)
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(doc_path), "..", ".."))
    def workspace_rel(path):
        path = os.path.abspath(path)
        try:
            return os.path.relpath(path, start=workspace_root).replace('\\', '/')
        except ValueError:
            return os.path.basename(path).replace('\\', '/')

    output_rel = workspace_rel(output_path)

    target_names = [os.path.basename(p) for p in image_paths]
    print(f"Actualizando referencias en {doc_path} para imágenes: {', '.join(target_names)} -> {output_rel}")
    target_rel_paths = [workspace_rel(p) for p in image_paths]
    first_rel_path = target_rel_paths[0]

    with open(doc_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    keep_first_block = None
    delete_ranges = []
    i = 0
    while i < len(lines):
        if lines[i].strip() != "```metadata":
            i += 1
            continue
        block_start = i
        i += 1
        imagen_line = None
        while i < len(lines) and lines[i].strip() != "```":
            if lines[i].strip().startswith("imagen:"):
                imagen_line = lines[i].split("imagen:", 1)[1].strip().replace('\\', '/')
            i += 1
        if i >= len(lines):
            break
        block_end = i
        i += 1
        next_nonblank = i
        while next_nonblank < len(lines) and lines[next_nonblank].strip() == "":
            next_nonblank += 1
        markdown_line_index = None
        if next_nonblank < len(lines) and next_nonblank > 0:
            if imagen_line and imagen_line in lines[next_nonblank]:
                markdown_line_index = next_nonblank
        if imagen_line not in target_rel_paths:
            continue
        if imagen_line == first_rel_path and keep_first_block is None:
            keep_first_block = (block_start, block_end, markdown_line_index)
            continue
        end_idx = markdown_line_index if markdown_line_index is not None else block_end
        delete_ranges.append((block_start, end_idx))
        i = end_idx + 1

    if keep_first_block is None:
        print(f"Advertencia: no se encontró la referencia del primer archivo {first_rel_path} en {doc_path}")
    else:
        block_start, block_end, markdown_idx = keep_first_block
        if output_rel != first_rel_path:
            for idx in range(block_start, block_end + 1):
                if lines[idx].strip().startswith("imagen:"):
                    lines[idx] = re.sub(r'^(imagen:\s*).*$', r"\1" + output_rel, lines[idx])
                    break
            if markdown_idx is not None:
                lines[markdown_idx] = re.sub(r'\(.*\)', f'({output_rel})', lines[markdown_idx])

    if not delete_ranges:
        with open(doc_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return

    new_lines = []
    skip_idx = 0
    sorted_ranges = sorted(delete_ranges)
    for start, end in sorted_ranges:
        if skip_idx < start:
            new_lines.extend(lines[skip_idx:start])
        skip_idx = end + 1
    if skip_idx < len(lines):
        new_lines.extend(lines[skip_idx:])

    cleaned_lines = []
    blank = False
    for line in new_lines:
        if line.strip() == "":
            if blank:
                continue
            blank = True
            cleaned_lines.append(line)
        else:
            blank = False
            cleaned_lines.append(line)

    with open(doc_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)


def main():
    parser = argparse.ArgumentParser(description="Concatena imágenes en una sola imagen")
    parser.add_argument("--input-dir", required=True, help="Carpeta con imágenes")
    parser.add_argument("--page", type=int, help="Número de página para filtrar por nombre P{page}_I*.png")
    parser.add_argument("--pattern", help="Patrón glob (si se especifica, ignora --page)")
    parser.add_argument("--direction", choices=["grid", "horizontal", "vertical"], default="vertical")
    parser.add_argument("--cols", type=int, default=0, help="Número de columnas para grid (0 auto)")
    parser.add_argument("--reverse", action="store_true", help="Invertir el orden de las imágenes antes de concatenar (útil para vertical)")
    parser.add_argument("--output", help="Archivo de salida (si no, se genera automáticamente)")
    parser.add_argument("--select", help='Selección no interactiva de imágenes, ej. "1,3-5"')
    args = parser.parse_args()

    input_dir = IMGS_DIR / args.input_dir

    # Determine which image files to consider. If user provided a pattern or a single page, use that.
    # Otherwise ask interactively for page numbers to limit the search to those pages.
    if args.pattern:
        paths = find_and_sort_images(input_dir, args.pattern)
    elif args.page is not None:
        paths = find_and_sort_images(input_dir, f"P{args.page}_I*.png")
    else:
        # Interactive prompt for pages (e.g. '1,3-5') or ENTER for all
        pages_input = input('Indique las páginas que contienen las imágenes (ej. 1,3-5), ENTER para todas: ').strip()
        if pages_input:
            page_indices = parse_selection(pages_input, 10000)  # large upper bound; we'll use numbers directly
            # page_indices contains zero-based indices; convert to page numbers
            page_nums = [i+1 for i in page_indices]
            paths = []
            for pnum in page_nums:
                paths.extend(find_and_sort_images(input_dir, f"P{pnum}_I*.png"))
        else:
            paths = find_and_sort_images(input_dir, "*.png")
    if not paths:
        search_pattern = args.pattern or (f"P{args.page}_I*.png" if args.page is not None else "*.png")
        print(f"No se encontraron imágenes en {input_dir} con patrón {search_pattern}")
        return

    # List found images and allow the user to select a subset by ranges
    print(f"Encontradas {len(paths)} imágenes.")
    for i, p in enumerate(paths, start=1):
        try:
            size_kb = os.path.getsize(p) / 1024
        except Exception:
            size_kb = 0
        print(f"{i:3}: {os.path.basename(p)} ({size_kb:.1f} KB)")

    # Determine selection (interactive or via --select)
    if args.select:
        indices = parse_selection(args.select, len(paths))
    else:
        sel = input('\nEscriba números separados por comas o rangos (ej. 1,3-5), ENTER para todas: ').strip()
        indices = parse_selection(sel, len(paths))

    if not indices:
        print('No hay imágenes seleccionadas, saliendo.')
        return

    # Filter paths to the selected ones preserving order
    paths = [paths[i] for i in indices]
    print(f"Seleccionadas {len(paths)} imágenes para concatenar. Preparando montaje...")
    images = load_images(paths)
    if args.reverse:
        images.reverse()
    if not images:
        print("Ninguna imagen válida para procesar.")
        return

    if not args.output:
        first_image_name = os.path.basename(paths[0])
        args.output = os.path.join(input_dir, first_image_name)

    if args.direction == "horizontal":
        out = concat_horizontal(images)
    elif args.direction == "vertical":
        out = concat_vertical(images)
    else:
        out = concat_grid(images, cols=(args.cols if args.cols>0 else None))

    if out is None:
        print("No se generó la imagen de salida.")
        return

    out.save(args.output)
    print(f"Guardado: {args.output}")

    update_document_references(PROCESSED_DOCUMENTS_DIR / f"{args.input_dir}.md", paths, args.output)
    delete_input_images(paths, args.output)


if __name__ == "__main__":
    main()
