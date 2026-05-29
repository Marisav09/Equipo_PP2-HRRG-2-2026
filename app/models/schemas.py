from __future__ import annotations

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
        )


@dataclass(frozen=True)
class SourceCitation:
    # Fuente interna del RAG. Puede ser Markdown procesado.
    source_file: str

    # Página visible principal. Para el usuario debe corresponder al PDF original.
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

    # Trazabilidad interna al Markdown procesado.
    markdown_page: int | str | None = None

    def visible_source(self) -> str:
        return self.display_source or self.original_pdf or self.source_file

    def visible_page(self) -> int | str:
        return self.pdf_page if self.pdf_page not in (None, "") else self.page

    def label(self) -> str:
        visual_note = " | contiene imagenes" if self.has_images else ""
        return f"{self.visible_source()}, pagina {self.visible_page()}, chunk {self.chunk_id}{visual_note}"

    def document_url(self) -> str:
        if self.url:
            return self.url

        source_for_link = self.original_pdf or self.display_source or self.source_file
        encoded_name = quote(str(source_for_link))
        page = self.visible_page()
        page_fragment = f"#page={page}" if str(page).isdigit() else ""
        return f"/manuals/{encoded_name}{page_fragment}"

    def to_dict(self) -> dict[str, Any]:
        images = list(self.images)

        source_for_preview = self.original_pdf or self.display_source or self.source_file
        page = self.visible_page()

        if self.has_images and not images and str(source_for_preview).lower().endswith(".pdf"):
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
            "page": page,
            "chunk_id": self.chunk_id,
            "equipment_name": self.equipment_name,
            "has_images": self.has_images,
            "image_count": self.image_count,
            "label": self.label(),
            "url": self.document_url(),
            "images": images,

            # Campos nuevos para interfaz/fuentes visibles.
            "display_source": self.visible_source(),
            "original_pdf": self.original_pdf or "",
            "pdf_page": page,
            "markdown_page": self.markdown_page if self.markdown_page is not None else "",
        }


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