from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path
from typing import Any

import fitz
from PIL import Image


BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR = BASE_DIR / "data" / "raw"
SEMI_PROCESSED_DIR = BASE_DIR / "data" / "semi-processed"
INVENTORY_DIR = BASE_DIR / "data" / "inventory"

CURATION_CSV = INVENTORY_DIR / "curaduria_activa.csv"
OVERRIDES_CSV = INVENTORY_DIR / "pdf_source_overrides.csv"
OUTPUT_CSV = INVENTORY_DIR / "page_mapping_markdown_to_official.csv"

HASH_SIZE = 32
VISUAL_RENDER_DPI = 50

TEXT_MIN_NORMALIZED_CHARS = 80

TEXT_VERIFIED_SCORE = 0.70
TEXT_VERIFIED_COVERAGE = 0.60
TEXT_VERIFIED_MARGIN = 0.03
TEXT_STRONG_SCORE = 0.92
TEXT_STRONG_COVERAGE = 0.85

TEXT_APPROX_SCORE = 0.45
TEXT_APPROX_COVERAGE = 0.35

VISUAL_VERIFIED_SCORE = 0.97
VISUAL_VERIFIED_MARGIN = 0.03
VISUAL_APPROX_SCORE = 0.90
VISUAL_APPROX_MARGIN = 0.01

SEQUENCE_EVIDENCE_VERIFIED = 0.95
SEQUENCE_EVIDENCE_APPROXIMATE = 0.90


@dataclass
class MarkdownPage:
    source_file: str
    markdown_page: int
    text: str


@dataclass
class PdfTextPage:
    official_pdf: str
    official_pdf_page: int
    text: str


@dataclass
class MappingCandidate:
    official_pdf_page: int | str
    page_confidence: str
    score: float
    status: str
    mapping_method: str

    text_score: float = 0.0
    text_coverage: float = 0.0
    text_jaccard: float = 0.0
    text_sequence: float = 0.0
    text_margin: float = 0.0

    visual_score: float = 0.0
    visual_margin: float = 0.0
    visual_second_page: int | str = ""


def normalize_text(value: str) -> str:
    if not value:
        return ""

    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def useful_terms(value: str) -> set[str]:
    normalized = normalize_text(value)
    stopwords = {
        "para",
        "como",
        "este",
        "esta",
        "estos",
        "estas",
        "manual",
        "pagina",
        "paginas",
        "equipo",
        "sistema",
        "usuario",
        "servicio",
        "tecnico",
        "tecnica",
        "informacion",
        "documento",
        "fuente",
        "figura",
        "tabla",
        "advertencia",
        "precaucion",
    }

    return {
        token
        for token in normalized.split()
        if len(token) >= 5 and token not in stopwords
    }


def strip_markdown_noise(text: str) -> str:
    text = re.sub(r"```metadata.*?```", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"(?m)^#{1,6}\s+", "", text)
    return text.strip()


def split_markdown_pages(source_file: str, markdown_text: str) -> list[MarkdownPage]:
    pattern = r"(?im)^#{1,6}\s*P(?:a|ÃƒÂ¡|Ã¡|á)gina\s+(\d+)\s*$"
    matches = list(re.finditer(pattern, markdown_text))

    if not matches:
        return [
            MarkdownPage(
                source_file=source_file,
                markdown_page=1,
                text=strip_markdown_noise(markdown_text),
            )
        ]

    pages: list[MarkdownPage] = []
    for index, match in enumerate(matches):
        page_number = int(match.group(1))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown_text)
        page_text = strip_markdown_noise(markdown_text[start:end])
        pages.append(
            MarkdownPage(
                source_file=source_file,
                markdown_page=page_number,
                text=page_text,
            )
        )

    return pages


@lru_cache(maxsize=128)
def load_pdf_text_pages(official_pdf: str) -> tuple[PdfTextPage, ...]:
    pdf_path = RAW_DIR / official_pdf
    pages: list[PdfTextPage] = []

    with fitz.open(pdf_path) as pdf:
        for index, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()
            pages.append(
                PdfTextPage(
                    official_pdf=official_pdf,
                    official_pdf_page=index,
                    text=text,
                )
            )

    return tuple(pages)


def score_text_match(markdown_text: str, pdf_text: str) -> tuple[float, float, float, float]:
    md_norm = normalize_text(markdown_text)
    pdf_norm = normalize_text(pdf_text)

    if not md_norm or not pdf_norm:
        return 0.0, 0.0, 0.0, 0.0

    md_terms = useful_terms(markdown_text)
    pdf_terms = useful_terms(pdf_text)

    if not md_terms or not pdf_terms:
        return 0.0, 0.0, 0.0, 0.0

    overlap = len(md_terms & pdf_terms)
    coverage = overlap / max(len(md_terms), 1)
    jaccard = overlap / max(len(md_terms | pdf_terms), 1)

    md_sample = md_norm[:2500]
    pdf_sample = pdf_norm[:2500]
    sequence = SequenceMatcher(None, md_sample, pdf_sample).ratio()

    score = (coverage * 0.70) + (jaccard * 0.20) + (sequence * 0.10)
    return score, coverage, jaccard, sequence


def text_confidence_label(score: float, coverage: float, margin: float) -> str:
    strong_match = score >= TEXT_STRONG_SCORE and coverage >= TEXT_STRONG_COVERAGE
    clear_match = (
        score >= TEXT_VERIFIED_SCORE
        and coverage >= TEXT_VERIFIED_COVERAGE
        and margin >= TEXT_VERIFIED_MARGIN
    )

    if strong_match or clear_match:
        return "verified"

    if score >= TEXT_APPROX_SCORE and coverage >= TEXT_APPROX_COVERAGE:
        return "approximate"

    return "unresolved"


def best_text_page_for(markdown_page: MarkdownPage, pdf_pages: tuple[PdfTextPage, ...]) -> MappingCandidate:
    normalized_markdown = normalize_text(markdown_page.text)

    if len(normalized_markdown) < TEXT_MIN_NORMALIZED_CHARS:
        return MappingCandidate(
            official_pdf_page="",
            page_confidence="unresolved",
            score=0.0,
            status="markdown_page_without_enough_text",
            mapping_method="text_similarity",
        )

    candidates: list[dict[str, Any]] = []

    for pdf_page in pdf_pages:
        score, coverage, jaccard, sequence = score_text_match(markdown_page.text, pdf_page.text)
        candidates.append(
            {
                "official_pdf_page": pdf_page.official_pdf_page,
                "score": score,
                "coverage": coverage,
                "jaccard": jaccard,
                "sequence": sequence,
            }
        )

    if not candidates:
        return MappingCandidate(
            official_pdf_page="",
            page_confidence="unresolved",
            score=0.0,
            status="no_pdf_pages",
            mapping_method="text_similarity",
        )

    candidates.sort(key=lambda item: item["score"], reverse=True)
    best = candidates[0]
    second = candidates[1] if len(candidates) > 1 else None
    second_score = float(second["score"]) if second else 0.0
    margin = float(best["score"]) - second_score

    confidence = text_confidence_label(
        score=float(best["score"]),
        coverage=float(best["coverage"]),
        margin=margin,
    )

    status = "text_matched" if confidence != "unresolved" else "low_text_similarity"

    return MappingCandidate(
        official_pdf_page=int(best["official_pdf_page"]) if confidence != "unresolved" else "",
        page_confidence=confidence,
        score=round(float(best["score"]), 4),
        status=status,
        mapping_method="text_similarity",
        text_score=round(float(best["score"]), 4),
        text_coverage=round(float(best["coverage"]), 4),
        text_jaccard=round(float(best["jaccard"]), 4),
        text_sequence=round(float(best["sequence"]), 4),
        text_margin=round(margin, 4),
    )


def page_fingerprint(page: fitz.Page) -> tuple[int, ...]:
    pixmap = page.get_pixmap(dpi=VISUAL_RENDER_DPI, alpha=False)
    image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    image = image.convert("L")

    image.thumbnail((HASH_SIZE, HASH_SIZE))
    canvas = Image.new("L", (HASH_SIZE, HASH_SIZE), 255)

    x = (HASH_SIZE - image.width) // 2
    y = (HASH_SIZE - image.height) // 2
    canvas.paste(image, (x, y))

    pixels = list(canvas.tobytes())
    average = sum(pixels) / len(pixels)

    return tuple(1 if pixel >= average else 0 for pixel in pixels)


def hamming_similarity(left: tuple[int, ...], right: tuple[int, ...]) -> float:
    if len(left) != len(right):
        return 0.0

    distance = sum(1 for a, b in zip(left, right) if a != b)
    return 1.0 - (distance / len(left))


@lru_cache(maxsize=128)
def load_pdf_fingerprints(pdf_path_text: str) -> tuple[tuple[int, tuple[int, ...]], ...]:
    pdf_path = Path(pdf_path_text)
    fingerprints: list[tuple[int, tuple[int, ...]]] = []

    with fitz.open(pdf_path) as pdf:
        for index, page in enumerate(pdf, start=1):
            fingerprints.append((index, page_fingerprint(page)))

    return tuple(fingerprints)


def visual_confidence_label(score: float, margin: float) -> str:
    if score >= VISUAL_VERIFIED_SCORE and margin >= VISUAL_VERIFIED_MARGIN:
        return "verified"

    if score >= VISUAL_APPROX_SCORE and margin >= VISUAL_APPROX_MARGIN:
        return "approximate"

    return "unresolved"


def best_visual_page_for(
    markdown_page: MarkdownPage,
    semi_pdf: str,
    official_pdf: str,
) -> MappingCandidate:
    if not semi_pdf:
        return MappingCandidate(
            official_pdf_page="",
            page_confidence="unresolved",
            score=0.0,
            status="missing_semi_pdf_for_visual_mapping",
            mapping_method="visual_similarity",
        )

    semi_path = SEMI_PROCESSED_DIR / semi_pdf
    official_path = RAW_DIR / official_pdf

    if not semi_path.exists():
        return MappingCandidate(
            official_pdf_page="",
            page_confidence="unresolved",
            score=0.0,
            status="semi_pdf_not_found_for_visual_mapping",
            mapping_method="visual_similarity",
        )

    if not official_path.exists():
        return MappingCandidate(
            official_pdf_page="",
            page_confidence="unresolved",
            score=0.0,
            status="official_pdf_not_found_for_visual_mapping",
            mapping_method="visual_similarity",
        )

    try:
        with fitz.open(semi_path) as semi_document:
            if markdown_page.markdown_page < 1 or markdown_page.markdown_page > semi_document.page_count:
                return MappingCandidate(
                    official_pdf_page="",
                    page_confidence="unresolved",
                    score=0.0,
                    status="markdown_page_outside_semi_pdf_range",
                    mapping_method="visual_similarity",
                )

            semi_hash = page_fingerprint(semi_document[markdown_page.markdown_page - 1])
    except Exception as exc:
        return MappingCandidate(
            official_pdf_page="",
            page_confidence="unresolved",
            score=0.0,
            status=f"semi_pdf_visual_error:{exc}",
            mapping_method="visual_similarity",
        )

    try:
        official_fingerprints = load_pdf_fingerprints(str(official_path))
    except Exception as exc:
        return MappingCandidate(
            official_pdf_page="",
            page_confidence="unresolved",
            score=0.0,
            status=f"official_pdf_visual_error:{exc}",
            mapping_method="visual_similarity",
        )

    candidates = [
        (official_page, hamming_similarity(semi_hash, official_hash))
        for official_page, official_hash in official_fingerprints
    ]

    if not candidates:
        return MappingCandidate(
            official_pdf_page="",
            page_confidence="unresolved",
            score=0.0,
            status="no_official_visual_pages",
            mapping_method="visual_similarity",
        )

    candidates.sort(key=lambda item: item[1], reverse=True)

    best_page, best_score = candidates[0]
    second_page, second_score = candidates[1] if len(candidates) > 1 else ("", 0.0)
    margin = best_score - float(second_score)

    confidence = visual_confidence_label(best_score, margin)
    status = "visual_matched" if confidence != "unresolved" else "low_visual_similarity"

    return MappingCandidate(
        official_pdf_page=int(best_page) if confidence != "unresolved" else "",
        page_confidence=confidence,
        score=round(float(best_score), 4),
        status=status,
        mapping_method="visual_similarity",
        visual_score=round(float(best_score), 4),
        visual_margin=round(float(margin), 4),
        visual_second_page=second_page,
    )


def confidence_rank(confidence: str) -> int:
    return {
        "unresolved": 0,
        "approximate": 1,
        "verified": 2,
    }.get(confidence, 0)


def merge_candidates(text_candidate: MappingCandidate, visual_candidate: MappingCandidate) -> MappingCandidate:
    if confidence_rank(visual_candidate.page_confidence) > confidence_rank(text_candidate.page_confidence):
        chosen = visual_candidate
    elif confidence_rank(text_candidate.page_confidence) > confidence_rank(visual_candidate.page_confidence):
        chosen = text_candidate
    else:
        chosen = text_candidate if text_candidate.score >= visual_candidate.score else visual_candidate

    return MappingCandidate(
        official_pdf_page=chosen.official_pdf_page,
        page_confidence=chosen.page_confidence,
        score=chosen.score,
        status=chosen.status,
        mapping_method=chosen.mapping_method,
        text_score=text_candidate.text_score,
        text_coverage=text_candidate.text_coverage,
        text_jaccard=text_candidate.text_jaccard,
        text_sequence=text_candidate.text_sequence,
        text_margin=text_candidate.text_margin,
        visual_score=visual_candidate.visual_score,
        visual_margin=visual_candidate.visual_margin,
        visual_second_page=visual_candidate.visual_second_page,
    )


def best_page_for(
    markdown_page: MarkdownPage,
    pdf_pages: tuple[PdfTextPage, ...],
    semi_pdf: str,
    official_pdf: str,
    enable_visual: bool,
) -> MappingCandidate:
    text_candidate = best_text_page_for(markdown_page, pdf_pages)

    if text_candidate.page_confidence == "verified":
        return text_candidate

    if not enable_visual:
        return text_candidate

    visual_candidate = best_visual_page_for(
        markdown_page=markdown_page,
        semi_pdf=semi_pdf,
        official_pdf=official_pdf,
    )

    return merge_candidates(text_candidate, visual_candidate)


def as_int(value: object) -> int | None:
    try:
        if value in (None, ""):
            return None
        return int(str(value))
    except (TypeError, ValueError):
        return None


def as_float(value: object) -> float:
    try:
        if value in (None, ""):
            return 0.0
        return float(str(value))
    except (TypeError, ValueError):
        return 0.0


def is_anchor_row(row: dict[str, object]) -> bool:
    page = as_int(row.get("official_pdf_page"))
    confidence = str(row.get("page_confidence") or "")
    return page is not None and confidence in {"verified", "approximate"}


def evidence_score(row: dict[str, object]) -> float:
    return max(
        as_float(row.get("score")),
        as_float(row.get("text_score")),
        as_float(row.get("visual_score")),
    )


def apply_sequence_refinement(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """
    Tercera capa de trazabilidad.

    Solo resuelve paginas no resueltas cuando:
    - la pagina Markdown anterior inmediata esta mapeada;
    - la pagina Markdown posterior inmediata esta mapeada;
    - ambas obligan al mismo numero de pagina PDF oficial;
    - existe evidencia visual/textual alta en la fila ambigua.

    No baja umbrales globales ni fuerza paginas cuando la continuidad no cierra.
    """
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("source_file") or ""), []).append(row)

    refined_rows: list[dict[str, object]] = []

    for source_file, source_rows in grouped.items():
        sorted_rows = sorted(source_rows, key=lambda item: as_int(item.get("markdown_page")) or 0)
        by_markdown_page = {
            as_int(row.get("markdown_page")): row
            for row in sorted_rows
            if as_int(row.get("markdown_page")) is not None
        }

        for row in sorted_rows:
            confidence = str(row.get("page_confidence") or "")
            markdown_page = as_int(row.get("markdown_page"))

            if confidence != "unresolved" or markdown_page is None:
                refined_rows.append(row)
                continue

            previous_row = by_markdown_page.get(markdown_page - 1)
            next_row = by_markdown_page.get(markdown_page + 1)

            if not previous_row or not next_row:
                refined_rows.append(row)
                continue

            if not is_anchor_row(previous_row) or not is_anchor_row(next_row):
                refined_rows.append(row)
                continue

            previous_pdf_page = as_int(previous_row.get("official_pdf_page"))
            next_pdf_page = as_int(next_row.get("official_pdf_page"))

            if previous_pdf_page is None or next_pdf_page is None:
                refined_rows.append(row)
                continue

            expected_from_previous = previous_pdf_page + 1
            expected_from_next = next_pdf_page - 1

            if expected_from_previous != expected_from_next:
                refined_rows.append(row)
                continue

            evidence = evidence_score(row)

            if evidence >= SEQUENCE_EVIDENCE_VERIFIED:
                refined = dict(row)
                refined["official_pdf_page"] = expected_from_previous
                refined["page_confidence"] = "verified"
                refined["score"] = round(evidence, 4)
                refined["status"] = "sequence_resolved_between_adjacent_pages"
                refined["mapping_method"] = "sequence_continuity"
                refined_rows.append(refined)
                continue

            if evidence >= SEQUENCE_EVIDENCE_APPROXIMATE:
                refined = dict(row)
                refined["official_pdf_page"] = expected_from_previous
                refined["page_confidence"] = "approximate"
                refined["score"] = round(evidence, 4)
                refined["status"] = "sequence_approximate_between_adjacent_pages"
                refined["mapping_method"] = "sequence_continuity"
                refined_rows.append(refined)
                continue

            refined_rows.append(row)

    return refined_rows


def load_pdf_overrides() -> dict[str, str]:
    if not OVERRIDES_CSV.exists():
        return {}

    overrides: dict[str, str] = {}

    with OVERRIDES_CSV.open("r", encoding="utf-8-sig", errors="replace", newline="") as file:
        for row in csv.DictReader(file):
            source_file = (row.get("source_file") or "").strip()
            original_pdf = (row.get("original_pdf") or "").strip()

            if source_file and original_pdf:
                overrides[source_file] = original_pdf.replace("\\", "/")

    return overrides


def active_curation_rows() -> list[dict[str, str]]:
    if not CURATION_CSV.exists():
        return []

    rows: list[dict[str, str]] = []

    with CURATION_CSV.open("r", encoding="utf-8-sig", errors="replace", newline="") as file:
        for row in csv.DictReader(file):
            source_file = (row.get("source_file") or "").strip()
            decision = (row.get("decision_curaduria") or "").strip().lower()
            status = (row.get("estado_producto") or "").strip().lower()

            if not source_file:
                continue

            if decision == "incluir" and status in {"activo", "validado", "aprobado"}:
                rows.append(row)

    return rows


def fallback_processed_markdowns() -> list[dict[str, str]]:
    return [
        {"source_file": path.name}
        for path in sorted(PROCESSED_DIR.glob("*.md"))
        if path.is_file()
    ]


def pdf_exists(root: Path, relative_pdf: str) -> bool:
    if not relative_pdf:
        return False

    return (root / relative_pdf).exists()


def find_pdf_by_name(root: Path, pdf_name: str) -> str:
    if not root.exists() or not pdf_name:
        return ""

    direct = root / pdf_name
    if direct.exists():
        return pdf_name

    for pdf_path in root.rglob("*.pdf"):
        if pdf_path.name == pdf_name:
            return pdf_path.relative_to(root).as_posix()

    return ""


def expected_pdf_name_for_markdown(source_file: str) -> str:
    return f"{Path(source_file).stem}.pdf"


def build_document_pairs_from_sources() -> list[dict[str, str]]:
    """
    Construye los pares Markdown -> PDF oficial sin depender de
    document_source_pairs.csv.

    Fuente principal:
    - data/inventory/curaduria_activa.csv, solo documentos incluidos/activos.

    Apoyos:
    - data/inventory/pdf_source_overrides.csv para casos donde el nombre del
      Markdown no coincide con el PDF oficial.
    - data/raw para localizar el PDF oficial.
    - data/semi-processed para habilitar fallback visual cuando exista el PDF
      semiprocesado equivalente.

    Si no existe curaduria_activa.csv, usa todos los Markdown de data/processed
    como fallback operativo.
    """
    overrides = load_pdf_overrides()
    curation_rows = active_curation_rows()
    source_rows = curation_rows if curation_rows else fallback_processed_markdowns()

    pairs: list[dict[str, str]] = []

    for row in source_rows:
        source_file = (row.get("source_file") or "").strip()
        if not source_file:
            continue

        direct_pdf = expected_pdf_name_for_markdown(source_file)
        override_pdf = (overrides.get(source_file) or "").strip()
        official_candidate = override_pdf or direct_pdf

        official_pdf = ""
        if pdf_exists(RAW_DIR, official_candidate):
            official_pdf = official_candidate
        else:
            official_pdf = find_pdf_by_name(RAW_DIR, official_candidate)

        if not official_pdf and override_pdf:
            official_pdf = find_pdf_by_name(RAW_DIR, direct_pdf)

        if not official_pdf:
            official_pdf = official_candidate

        semi_pdf = ""
        if pdf_exists(SEMI_PROCESSED_DIR, direct_pdf):
            semi_pdf = direct_pdf
        elif find_pdf_by_name(SEMI_PROCESSED_DIR, direct_pdf):
            semi_pdf = find_pdf_by_name(SEMI_PROCESSED_DIR, direct_pdf)
        elif pdf_exists(SEMI_PROCESSED_DIR, official_pdf):
            semi_pdf = official_pdf
        elif find_pdf_by_name(SEMI_PROCESSED_DIR, official_pdf):
            semi_pdf = find_pdf_by_name(SEMI_PROCESSED_DIR, official_pdf)

        pairs.append(
            {
                "source_file": source_file,
                "equipo": (row.get("equipo") or "").strip(),
                "tipo_documento": (row.get("tipo_documento") or "").strip(),
                "official_pdf": official_pdf,
                "official_pdf_found": str(pdf_exists(RAW_DIR, official_pdf)),
                "semi_pdf": semi_pdf,
                "semi_pdf_found": str(pdf_exists(SEMI_PROCESSED_DIR, semi_pdf)) if semi_pdf else "False",
                "mapping_strategy": "auto_from_curation_and_overrides",
            }
        )

    return pairs


def load_document_pairs() -> list[dict[str, str]]:
    pairs = build_document_pairs_from_sources()

    if not pairs:
        raise FileNotFoundError(
            "No se pudieron construir pares Markdown -> PDF oficial. "
            "Verificar data/inventory/curaduria_activa.csv o archivos .md en data/processed."
        )

    return pairs


def build_page_mapping(
    limit: int | None = None,
    source_file_filter: str | None = None,
    enable_visual: bool = True,
    enable_sequence: bool = True,
) -> list[dict[str, object]]:
    pairs = load_document_pairs()

    if source_file_filter:
        pairs = [row for row in pairs if row.get("source_file") == source_file_filter]

    if limit is not None:
        pairs = pairs[:limit]

    output_rows: list[dict[str, object]] = []

    for doc_index, pair in enumerate(pairs, start=1):
        source_file = str(pair.get("source_file") or "").strip()
        official_pdf = str(pair.get("official_pdf") or "").strip()
        semi_pdf = str(pair.get("semi_pdf") or "").strip()

        print(f"[{doc_index}/{len(pairs)}] {source_file}")

        markdown_path = PROCESSED_DIR / source_file
        official_pdf_path = RAW_DIR / official_pdf

        if not markdown_path.exists():
            output_rows.append(
                unresolved_row(
                    source_file=source_file,
                    official_pdf=official_pdf,
                    semi_pdf=semi_pdf,
                    status="missing_markdown",
                )
            )
            continue

        if not official_pdf_path.exists():
            output_rows.append(
                unresolved_row(
                    source_file=source_file,
                    official_pdf=official_pdf,
                    semi_pdf=semi_pdf,
                    status="missing_official_pdf",
                )
            )
            continue

        markdown_text = markdown_path.read_text(encoding="utf-8", errors="replace")
        markdown_pages = split_markdown_pages(source_file, markdown_text)
        pdf_pages = load_pdf_text_pages(official_pdf)

        for markdown_page in markdown_pages:
            best = best_page_for(
                markdown_page=markdown_page,
                pdf_pages=pdf_pages,
                semi_pdf=semi_pdf,
                official_pdf=official_pdf,
                enable_visual=enable_visual,
            )

            output_rows.append(
                {
                    "source_file": source_file,
                    "semi_pdf": semi_pdf,
                    "official_pdf": official_pdf,
                    "markdown_page": markdown_page.markdown_page,
                    "official_pdf_page": best.official_pdf_page,
                    "page_confidence": best.page_confidence,
                    "score": best.score,
                    "text_score": best.text_score,
                    "text_coverage": best.text_coverage,
                    "text_jaccard": best.text_jaccard,
                    "text_sequence": best.text_sequence,
                    "text_margin": best.text_margin,
                    "visual_score": best.visual_score,
                    "visual_margin": best.visual_margin,
                    "visual_second_page": best.visual_second_page,
                    "status": best.status,
                    "mapping_method": best.mapping_method,
                    "markdown_preview": normalize_text(markdown_page.text)[:180],
                }
            )

    if enable_sequence:
        output_rows = apply_sequence_refinement(output_rows)

    return output_rows


def unresolved_row(
    source_file: str,
    official_pdf: str,
    semi_pdf: str,
    status: str,
) -> dict[str, object]:
    return {
        "source_file": source_file,
        "semi_pdf": semi_pdf,
        "official_pdf": official_pdf,
        "markdown_page": "",
        "official_pdf_page": "",
        "page_confidence": "unresolved",
        "score": 0.0,
        "text_score": 0.0,
        "text_coverage": 0.0,
        "text_jaccard": 0.0,
        "text_sequence": 0.0,
        "text_margin": 0.0,
        "visual_score": 0.0,
        "visual_margin": 0.0,
        "visual_second_page": "",
        "status": status,
        "mapping_method": "unresolved",
        "markdown_preview": "",
    }


def write_mapping(rows: list[dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "source_file",
        "semi_pdf",
        "official_pdf",
        "markdown_page",
        "official_pdf_page",
        "page_confidence",
        "score",
        "text_score",
        "text_coverage",
        "text_jaccard",
        "text_sequence",
        "text_margin",
        "visual_score",
        "visual_margin",
        "visual_second_page",
        "status",
        "mapping_method",
        "markdown_preview",
    ]

    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows: list[dict[str, object]]) -> None:
    total = len(rows)
    verified = sum(1 for row in rows if row["page_confidence"] == "verified")
    approximate = sum(1 for row in rows if row["page_confidence"] == "approximate")
    unresolved = sum(1 for row in rows if row["page_confidence"] == "unresolved")

    text_rows = sum(1 for row in rows if row["mapping_method"] == "text_similarity")
    visual_rows = sum(1 for row in rows if row["mapping_method"] == "visual_similarity")
    sequence_rows = sum(1 for row in rows if row["mapping_method"] == "sequence_continuity")

    print()
    print("Resumen de mapeo")
    print("-----------------")
    print(f"filas: {total}")
    print(f"verified: {verified}")
    print(f"approximate: {approximate}")
    print(f"unresolved: {unresolved}")
    print(f"text_similarity: {text_rows}")
    print(f"visual_similarity: {visual_rows}")
    print(f"sequence_continuity: {sequence_rows}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Mapea paginas Markdown activas contra paginas reales del PDF oficial. "
            "Los pares Markdown/PDF se construyen automaticamente desde curaduria_activa.csv, "
            "pdf_source_overrides.csv, data/raw y data/semi-processed."
        )
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--source-file", type=str, default=None)
    parser.add_argument("--output", type=Path, default=OUTPUT_CSV)
    parser.add_argument(
        "--no-visual",
        action="store_true",
        help="Desactiva el fallback visual y usa solo similitud textual.",
    )
    parser.add_argument(
        "--no-sequence",
        action="store_true",
        help="Desactiva el refinamiento por continuidad secuencial.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = build_page_mapping(
        limit=args.limit,
        source_file_filter=args.source_file,
        enable_visual=not args.no_visual,
        enable_sequence=not args.no_sequence,
    )
    write_mapping(rows, args.output)
    print_summary(rows)
    print(f"CSV generado: {args.output}")


if __name__ == "__main__":
    main()