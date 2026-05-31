from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import quote


@dataclass(frozen=True)
class ChatRequest:
    query: str
    equipment_id: str | None
    equipment_name: str | None
    role: str
    force_fallback: bool
    request_id: str
    chat_id: str = ""

    @classmethod
    def from_payload(cls, payload: dict) -> "ChatRequest":
        raw_role = str(payload.get("role", "tecnico")).strip().lower()
        role = "operador" if raw_role == "operador" else "tecnico"
        return cls(
            query=str(payload.get("query", "")).strip(),
            equipment_id=str(payload.get("equipment_id", "")).strip() or None,
            equipment_name=str(payload.get("equipment_name", "")).strip() or None,
            role=role,
            force_fallback=bool(payload.get("force_fallback", False)),
            request_id=str(payload.get("request_id", "")).strip(),
            chat_id=str(payload.get("chat_id", "")).strip(),
        )


@dataclass(frozen=True)
class SourceCitation:
    # Fuente interna del RAG. Puede ser Markdown procesado.
    source_file: str

    # Campo legado. No debe usarse como pagina visible si no hay pdf_page verificada.
    page: int | str

    chunk_id: str
    equipment_name: str
    has_images: bool = False
    image_count: int = 0
    url: str | None = None
    images: tuple[dict[str, Any], ...] = ()

    # Fuente visible para usuario final.
    display_source: str | None = None
    original_pdf: str | None = None
    pdf_page: int | str | None = None

    # Confianza y metodo del mapeo de pagina.
    pdf_page_confidence: str | None = None
    page_mapping_method: str | None = None
    page_mapping_status: str | None = None

    # Trazabilidad interna al Markdown procesado.
    markdown_page: int | str | None = None

    def visible_source(self) -> str:
        return self.display_source or self.original_pdf or self.source_file

    def reliable_pdf_page(self) -> int | None:
        confidence = str(self.pdf_page_confidence or "").strip().lower()
        if confidence != "verified":
            return None

        try:
            if self.pdf_page in (None, ""):
                return None
            page = int(str(self.pdf_page))
        except (TypeError, ValueError):
            return None

        return page if page > 0 else None

    def has_reliable_pdf_page(self) -> bool:
        return self.reliable_pdf_page() is not None

    def visible_page(self) -> int | str:
        page = self.reliable_pdf_page()
        return page if page is not None else ""

    def label(self) -> str:
        visual_note = " | contiene imagenes" if self.has_images else ""
        page = self.reliable_pdf_page()

        if page is not None:
            return f"{self.visible_source()}, pagina {page}, chunk {self.chunk_id}{visual_note}"

        return f"{self.visible_source()}, pagina no verificada, chunk {self.chunk_id}{visual_note}"

    def document_url(self) -> str:
        page = self.reliable_pdf_page()

        if self.url:
            if page is not None:
                return self.url
            return self._remove_page_anchor(self.url)

        source_for_link = self.original_pdf or self.display_source or self.source_file
        encoded_name = quote(str(source_for_link))

        if page is not None:
            return f"/manuals/{encoded_name}#page={page}"

        return f"/manuals/{encoded_name}"

    def to_dict(self) -> dict[str, Any]:
        images = list(self.images)

        source_for_preview = self.original_pdf or self.display_source or self.source_file
        page = self.reliable_pdf_page()

        if (
            self.has_images
            and not images
            and page is not None
            and str(source_for_preview).lower().endswith(".pdf")
        ):
            encoded_name = quote(str(source_for_preview))
            images.append(
                {
                    "url": f"/manual-thumbnails/{encoded_name}/page/{page}.png",
                    "page": page,
                    "label": f"Vista previa pagina {page}",
                }
            )

        return {
            # Compatibilidad: source_file sigue disponible para trazabilidad interna.
            "source_file": self.source_file,
            "page": page if page is not None else "",
            "chunk_id": self.chunk_id,
            "equipment_name": self.equipment_name,
            "has_images": self.has_images,
            "image_count": self.image_count,
            "label": self.label(),
            "url": self.document_url(),
            "images": images,

            # Campos para interfaz/fuentes visibles.
            "display_source": self.visible_source(),
            "original_pdf": self.original_pdf or "",
            "pdf_page": page if page is not None else "",
            "has_reliable_pdf_page": page is not None,
            "pdf_page_confidence": self.pdf_page_confidence or "",
            "page_mapping_method": self.page_mapping_method or "",
            "page_mapping_status": self.page_mapping_status or "",

            # Trazabilidad interna, no debe usarse como pagina visible del PDF.
            "markdown_page": self.markdown_page if self.markdown_page is not None else "",
        }

    def _remove_page_anchor(self, url: str) -> str:
        cleaned = re.sub(r"#page=\d+", "", url)
        cleaned = re.sub(r"([?&])page=\d+(&?)", r"\1", cleaned)
        return cleaned.rstrip("?&")


@dataclass(frozen=True)
class RetrievedChunk:
    text: str
    citation: SourceCitation
    score: float | None = None


@dataclass(frozen=True)
class AssistantResponse:
    answer: str
    sources: list[SourceCitation] = field(default_factory=list)
    mode: str = "llm"

    def to_dict(self) -> dict[str, Any]:
        return {
            "answer": self.answer,
            "sources": [source.to_dict() for source in self.sources],
            "mode": self.mode,
        }
