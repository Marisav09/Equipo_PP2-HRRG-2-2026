import fitz  # PyMuPDF
import argparse
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar variables de entorno desde .env

BASE_DIR = Path(__file__).parent.parent
RAW_DOCUMENTS_DIR = BASE_DIR / os.getenv("RAW_DOCUMENTS_DIR", "data/raw")
PROCESSED_DOCUMENTS_DIR = BASE_DIR / os.getenv("PROCESSED_DOCUMENTS_DIR", "data/processed")
SEMI_PROCESSED_DOCUMENTS_DIR = BASE_DIR / os.getenv("SEMI_PROCESSED_DOCUMENTS_DIR", "data/semi-processed")
IMGS_DIR = BASE_DIR / os.getenv("IMGS_DIR", "data/images")

try:
    import pymupdf.layout as layout
    layout.activate()
    print("pymupdf.layout activado para mejor análisis de diseño de página.")
except ImportError:
    print("pymupdf.layout no está instalado; usando extracción estándar de PyMuPDF.")

# 1. Configuración inicial
parser = argparse.ArgumentParser(description="Extrae texto e imágenes de un PDF a Markdown.")
parser.add_argument("--file", required=True, help="Archivo PDF de entrada")
parser.add_argument("--equipment", required=True, help="Nombre del equipo para el documento Markdown")
args = parser.parse_args()

pdf_path = SEMI_PROCESSED_DOCUMENTS_DIR / args.file
output_img_dir = IMGS_DIR / args.file.replace('.pdf', '')
output_text_dir = PROCESSED_DOCUMENTS_DIR
doc_metadata = {"equipo": args.equipment}

# Crear carpetas de salida si no existen
os.makedirs(output_img_dir, exist_ok=True)
os.makedirs(output_text_dir, exist_ok=True)


def normalize_text_for_md(raw_text):
    lines = [line.strip() for line in raw_text.splitlines()]
    paragraphs = []
    current = []
    for line in lines:
        if not line:
            if current:
                paragraphs.append(" ".join(current))
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append(" ".join(current))
    return "\n\n".join(paragraphs)

# Abrir documento
doc = fitz.open(pdf_path)
full_document_md = ""

# 2. Iterar por cada página
for page_num in range(len(doc)):
    page = doc[page_num]
    page_text = f"# Página {page_num + 1}\n\n"
    page_text += f"**Equipo:** {doc_metadata['equipo']}\n\n"

    # A. Extraer contenido en orden de bloques para insertar imágenes en su posición
    blocks = page.get_text("dict")["blocks"]
    img_index = 0
    for block in blocks:
        if block["type"] == 0:
            # Texto
            line_texts = []
            for line in block.get("lines", []):
                spans = [span.get("text", "") for span in line.get("spans", []) if span.get("text", "").strip()]
                if spans:
                    line_texts.append(" ".join(spans))
            if line_texts:
                page_text += normalize_text_for_md("\n".join(line_texts)) + "\n\n"
        elif block["type"] == 1:
            # Imagen en bloque
            img_bytes = block.get("image")
            img_path = os.path.join(f"data/images/{args.file.replace('.pdf', '')}", f"P{page_num + 1}_I{img_index}.png")
            if isinstance(img_bytes, (bytes, bytearray)):
                with open(img_path, "wb") as img_file:
                    img_file.write(img_bytes)
            else:
                # Fallback a get_images si el bloque no trae bytes claros
                imagenes = page.get_images()
                if img_index < len(imagenes):
                    xref = imagenes[img_index][0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n > 4:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    pix.save(img_path)
                    pix = None
            print(f"Guardando imagen: {img_path}")

            img_path_md = img_path.replace('\\', '/')
            page_text += "```metadata\n"
            page_text += f"pagina: {page_num + 1}\n"
            page_text += f"imagen: {img_path_md}\n"
            page_text += "contexto: \n"
            page_text += "```\n\n"
            page_text += f"![Imagen página {page_num + 1} - {img_index}]({img_path_md})\n\n"
            img_index += 1
    full_document_md += page_text + "\n\n"

# Guardar documento completo en un solo archivo Markdown
output_md_path = os.path.join(output_text_dir, f"{args.file.replace('.pdf', '')}.md")
with open(output_md_path, "w", encoding="utf-8") as f:
    f.write(full_document_md)
print(f"Guardado documento completo: {output_md_path}")

