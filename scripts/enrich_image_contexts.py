from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Completa campos contexto: vacios en bloques ```metadata``` de un Markdown "
            "usando un modelo vision local de Ollama."
        )
    )
    parser.add_argument(
        "markdown",
        type=Path,
        help="Archivo Markdown a enriquecer, por ejemplo data/processed/manual.md.",
    )
    parser.add_argument(
        "--vision-model",
        default="moondream:latest",
        help="Modelo vision de Ollama para leer imagenes. Ej: moondream:latest o llama3.2-vision:latest.",
    )
    parser.add_argument(
        "--text-model",
        default="llama3.2:3b",
        help="Modelo de texto de Ollama para normalizar la descripcion al espanol tecnico.",
    )
    parser.add_argument(
        "--ollama-url",
        default="http://127.0.0.1:11434",
        help="URL base de Ollama.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Cantidad maxima de bloques a procesar en esta corrida.",
    )
    parser.add_argument(
        "--include-filled",
        action="store_true",
        help="Tambien reemplaza contextos ya completados. Por defecto solo completa vacios o SIN_CONTEXTO_UTIL.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra lo que haria sin escribir el Markdown.",
    )
    parser.add_argument(
        "--no-text-normalizer",
        action="store_true",
        help="Guarda directamente la respuesta del modelo vision, sin pasarla por el modelo de texto.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=260,
        help="Timeout por llamada a Ollama, en segundos.",
    )
    parser.add_argument(
        "--keep-alive",
        default="0s",
        help="keep_alive para Ollama. 0s libera memoria tras cada llamada; util en maquinas chicas.",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        default=30,
        help="Cantidad maxima de palabras sugerida para el contexto final.",
    )
    return parser.parse_args()


def ollama_generate(
    *,
    ollama_url: str,
    model: str,
    prompt: str,
    image_path: Path | None = None,
    timeout: int,
    keep_alive: str,
    num_predict: int = 120,
) -> str:
    payload: dict[str, object] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": keep_alive,
        "options": {
            "temperature": 0,
            "num_predict": num_predict,
        },
    }
    if image_path:
        payload["images"] = [base64.b64encode(image_path.read_bytes()).decode("ascii")]

    request = urllib.request.Request(
        f"{ollama_url.rstrip('/')}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
            return str(data.get("response") or "").strip()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama HTTP {exc.code}: {body}") from exc


def clean_nearby_text(value: str, max_chars: int = 900) -> str:
    value = re.sub(r"```metadata.*?```", " ", value, flags=re.DOTALL | re.IGNORECASE)
    value = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value[:max_chars]


def page_context(full_text: str, position: int) -> str:
    page_headers = list(re.finditer(r"(?im)^#\s*P.*?gina\s+\d+\s*$", full_text))
    start = 0
    end = len(full_text)
    for index, match in enumerate(page_headers):
        if match.start() <= position:
            start = match.start()
            end = page_headers[index + 1].start() if index + 1 < len(page_headers) else len(full_text)
        else:
            break
    return clean_nearby_text(full_text[start:end])


def resolve_image_path(raw_path: str, markdown_path: Path) -> Path:
    candidate = Path(raw_path.replace("\\", "/"))
    if candidate.is_absolute():
        return candidate

    root_candidate = ROOT_DIR / candidate
    if root_candidate.exists():
        return root_candidate

    markdown_candidate = markdown_path.parent / candidate
    if markdown_candidate.exists():
        return markdown_candidate

    return root_candidate


def sanitize_context(value: str) -> str:
    value = re.sub(
        r"(?i)^\s*(contexto|frase|respuesta|descripcion|description)\s*:\s*",
        "",
        value.strip(),
    )
    value = re.sub(r"(?i)^\s*(la imagen muestra|esta imagen muestra)\s+", "", value)
    value = value.strip(" \"'`")
    value = re.sub(r"\s+", " ", value).strip()
    if not value or len(value) < 12:
        return "SIN_CONTEXTO_UTIL"
    if value.endswith("."):
        value = value[:-1].strip()
    return value[:260]


def fallback_from_text(args: argparse.Namespace, nearby: str) -> str:
    if not nearby:
        return "SIN_CONTEXTO_UTIL"

    prompt = f"""Genera UNA frase breve en espanol para describir una imagen tecnica asociada a este fragmento de manual.
Debe comenzar con "Imagen asociada a" y usar solo el tema del texto cercano.
Maximo {args.max_words} palabras. No inventes procedimientos ni componentes.

Texto cercano:
{nearby[:700]}

Frase:"""
    response = ollama_generate(
        ollama_url=args.ollama_url,
        model=args.text_model,
        prompt=prompt,
        timeout=args.timeout,
        keep_alive=args.keep_alive,
        num_predict=90,
    )
    return sanitize_context(response)


def normalize_to_spanish(args: argparse.Namespace, vision_text: str, nearby: str) -> str:
    if args.no_text_normalizer:
        return sanitize_context(vision_text)

    if not vision_text.strip():
        return fallback_from_text(args, nearby)

    prompt = f"""Converti esta descripcion visual a UNA frase tecnica en espanol neutro para metadata de busqueda documental.
Maximo {args.max_words} palabras.
No agregues procedimientos ni datos que no esten presentes.
Sin prefacios, sin comillas.
Si la descripcion visual es incoherente o no aporta informacion, usa el texto cercano y comienza con "Imagen asociada a".

Descripcion visual:
{vision_text}

Texto cercano del manual:
{nearby[:700]}

Frase:"""
    response = ollama_generate(
        ollama_url=args.ollama_url,
        model=args.text_model,
        prompt=prompt,
        timeout=args.timeout,
        keep_alive=args.keep_alive,
        num_predict=100,
    )
    context = sanitize_context(response)
    return fallback_from_text(args, nearby) if context == "SIN_CONTEXTO_UTIL" else context


def should_process(current_context: str, include_filled: bool) -> bool:
    if include_filled:
        return True
    return not current_context.strip() or current_context.strip() == "SIN_CONTEXTO_UTIL"


def enrich_markdown(args: argparse.Namespace) -> int:
    markdown_path = args.markdown
    if not markdown_path.is_absolute():
        markdown_path = ROOT_DIR / markdown_path
    markdown_path = markdown_path.resolve()

    if not markdown_path.exists():
        raise FileNotFoundError(f"No existe el Markdown: {markdown_path}")

    text = markdown_path.read_text(encoding="utf-8", errors="replace")
    metadata_pattern = re.compile(r"```metadata\s*(?P<body>.*?)```", flags=re.DOTALL | re.IGNORECASE)
    replacements: list[tuple[int, int, str]] = []
    processed = 0

    for match in metadata_pattern.finditer(text):
        if args.limit is not None and processed >= args.limit:
            break

        body = match.group("body")
        image_match = re.search(r"(?im)^\s*imagen\s*:\s*(?P<path>\S+)\s*$", body)
        context_match = re.search(r"(?im)^\s*contexto\s*:\s*(?P<value>.*)$", body)
        if not image_match or not context_match:
            continue

        current_context = context_match.group("value").strip()
        if not should_process(current_context, args.include_filled):
            continue

        raw_image_path = image_match.group("path")
        image_path = resolve_image_path(raw_image_path, markdown_path)
        nearby = page_context(text, match.start())

        if not image_path.exists():
            context = fallback_from_text(args, nearby)
        else:
            prompt = f"""Describe this image from a technical manual in one concise sentence.
Describe only visible content useful for document retrieval.
Do not infer procedures.
Nearby manual text:
{nearby[:500]}"""
            try:
                vision_text = ollama_generate(
                    ollama_url=args.ollama_url,
                    model=args.vision_model,
                    prompt=prompt,
                    image_path=image_path,
                    timeout=args.timeout,
                    keep_alive=args.keep_alive,
                    num_predict=120,
                )
                context = normalize_to_spanish(args, vision_text, nearby)
            except Exception as exc:
                print(f"WARN {raw_image_path}: {exc}")
                context = fallback_from_text(args, nearby)

        new_body = re.sub(
            r"(?im)^\s*contexto\s*:.*$",
            f"contexto: {context}",
            body,
            count=1,
        )
        replacements.append((match.start("body"), match.end("body"), new_body))
        processed += 1
        print(f"{processed}: {raw_image_path} -> {context}")

    if replacements and not args.dry_run:
        new_text = text
        for start, end, new_body in reversed(replacements):
            new_text = new_text[:start] + new_body + new_text[end:]
        markdown_path.write_text(new_text, encoding="utf-8")

    print(f"processed={processed}")
    print(f"dry_run={args.dry_run}")
    return processed


def main() -> int:
    args = parse_args()
    try:
        enrich_markdown(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
