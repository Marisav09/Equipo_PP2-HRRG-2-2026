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
    source_file: str
    page: int | str
    chunk_id: str
    equipment_name: str
    has_images: bool = False
    image_count: int = 0
    url: str | None = None
    images: tuple[dict[str, Any], ...] = ()

    def label(self) -> str:
        visual_note = " | contiene imagenes" if self.has_images else ""
        return f"{self.source_file}, pagina {self.page}, chunk {self.chunk_id}{visual_note}"

    def document_url(self) -> str:
        if self.url:
            return self.url
        encoded_name = quote(self.source_file)
        page_fragment = f"#page={self.page}" if str(self.page).isdigit() else ""
        return f"/manuals/{encoded_name}{page_fragment}"

    def to_dict(self) -> dict[str, Any]:
        images = list(self.images)
        if self.has_images and not images and str(self.source_file).lower().endswith(".pdf"):
            encoded_name = quote(self.source_file)
            images.append(
                {
                    "url": f"/manual-thumbnails/{encoded_name}/page/{self.page}.png",
                    "page": self.page,
                    "label": f"Vista previa pagina {self.page}",
                }
            )
        return {
            "source_file": self.source_file,
            "page": self.page,
            "chunk_id": self.chunk_id,
            "equipment_name": self.equipment_name,
            "has_images": self.has_images,
            "image_count": self.image_count,
            "label": self.label(),
            "url": self.document_url(),
            "images": images,
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
