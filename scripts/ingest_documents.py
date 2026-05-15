from pathlib import Path
import json
import fitz  # PyMuPDF


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def extract_pages_from_pdf(pdf_path):
    """
    Extrae el texto de un PDF página por página usando PyMuPDF.
    Devuelve una lista de diccionarios, donde cada elemento contiene
    el número de página y el texto correspondiente.
    """
    document = fitz.open(pdf_path)
    pages = []

    for page_number, page in enumerate(document, start=1):
        page_text = page.get_text().strip()

        if page_text:
            pages.append({
                "page": page_number,
                "text": page_text
            })

    document.close()
    return pages


def save_full_text(pages, pdf_path):
    """
    Guarda el texto completo extraído del PDF, manteniendo marcas visibles
    de número de página para revisión humana.
    """
    full_text = ""

    for page in pages:
        full_text += f"\n\n--- Página {page['page']} ---\n\n"
        full_text += page["text"]

    txt_output_file = PROCESSED_DIR / f"{pdf_path.stem}.txt"

    with open(txt_output_file, "w", encoding="utf-8") as file:
        file.write(full_text)

    return txt_output_file


def split_text_into_chunks(text, chunk_size=800, overlap=150):
    """
    Divide un texto en fragmentos con solapamiento.
    El overlap permite conservar contexto entre fragmentos consecutivos.
    """
    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks_from_pages(pages, pdf_path):
    """
    Genera chunks a partir del texto de cada página.
    Cada chunk hereda directamente el número de página desde el origen.
    """
    chunk_records = []
    chunk_id = 1

    for page in pages:
        page_number = page["page"]
        page_text = page["text"]

        page_chunks = split_text_into_chunks(page_text)

        for chunk in page_chunks:
            chunk_records.append({
                "chunk_id": chunk_id,
                "source_file": pdf_path.name,
                "page": page_number,
                "document_type": "documento_de_prueba",
                "text": chunk
            })

            chunk_id += 1

    return chunk_records


def save_chunks_as_json(chunk_records, pdf_path):
    """
    Guarda los chunks en un archivo JSON con metadatos ampliados.
    """
    output_file = PROCESSED_DIR / f"chunks_{pdf_path.stem}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(chunk_records, file, ensure_ascii=False, indent=4)

    return output_file


def process_pdfs():
    """
    Busca archivos PDF en data/raw, extrae el texto por página,
    guarda el texto completo y genera chunks con metadatos claros.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No se encontraron archivos PDF en data/raw.")
        return

    for pdf_path in pdf_files:
        print(f"Procesando: {pdf_path.name}")

        pages = extract_pages_from_pdf(pdf_path)

        txt_output_file = save_full_text(pages, pdf_path)
        print(f"Texto extraído guardado en: {txt_output_file}")

        chunk_records = create_chunks_from_pages(pages, pdf_path)

        json_output_file = save_chunks_as_json(chunk_records, pdf_path)

        print(f"Chunks generados: {len(chunk_records)}")
        print(f"Chunks guardados en: {json_output_file}")


if __name__ == "__main__":
    process_pdfs()