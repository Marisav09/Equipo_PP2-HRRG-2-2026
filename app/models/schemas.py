from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from urllib.parse import quote


@dataclass(frozen=True)
class SourceCitation:
    source_file: str
    page: int | str
    chunk_id: str
    has_images: bool = False
    image_count: int = 0

    def label(self) -> str:
        image_note = " | contiene imagenes" if self.has_images else ""
        return f"{self.source_file}, pagina {self.page}, chunk {self.chunk_id}{image_note}"

    def pdf_url(self) -> str:
        encoded_name = quote(self.source_file)
        page_fragment = f"#page={self.page}" if str(self.page).isdigit() else ""
        return f"/manuals/{encoded_name}{page_fragment}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_file": self.source_file,
            "page": self.page,
            "chunk_id": self.chunk_id,
            "has_images": self.has_images,
            "image_count": self.image_count,
            "label": self.label(),
            "url": self.pdf_url(),
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
    ticket_id: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "answer": self.answer,
            "sources": [source.to_dict() for source in self.sources],
            "mode": self.mode,
            "ticket_id": self.ticket_id,
        }


@dataclass(frozen=True)
class TicketRecord:
    question: str
    reason: str
    equipment: str | None = None
    status: str = "abierto"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
