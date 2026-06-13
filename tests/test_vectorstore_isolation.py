from __future__ import annotations

from types import SimpleNamespace

import pytest
from langchain_core.documents import Document

from app.core.exceptions import EquipmentScopeError
import app.services.vectorstore_service as vectorstore_module
from app.services.vectorstore_service import VectorstoreService


class FakeCollection:
    def count(self) -> int:
        return 2

    def get(self, where, include, limit=None):
        return {
            "documents": [
                "Procedimiento documentado para la alarma de puerta.",
                "Descripcion general sin coincidencia.",
            ],
            "metadatas": [
                {
                    "equipment_name": "Esterilizadora Sterrad 100",
                    "source_file": "manual.md",
                    "markdown_page": 12,
                    "chunk_id": "a",
                },
                {
                    "equipment_name": "Esterilizadora Sterrad 100",
                    "source_file": "manual.md",
                    "markdown_page": 13,
                    "chunk_id": "b",
                },
            ],
        }


class FakeStore:
    def __init__(self) -> None:
        self._collection = FakeCollection()
        self.last_filter = None

    def similarity_search_with_score(self, question, k, filter):
        self.last_filter = filter
        return [
            (
                Document(
                    page_content="Procedimiento documentado para la alarma de puerta.",
                    metadata={
                        "equipment_name": "Esterilizadora Sterrad 100",
                        "source_file": "manual.md",
                        "markdown_page": 12,
                        "chunk_id": "a",
                    },
                ),
                0.12,
            )
        ]


class FakeReranker:
    def predict(self, pairs, batch_size, show_progress_bar):
        return [1.0 if "alarma de puerta" in text else 0.0 for _question, text in pairs]


class FakeVectorstoreService(VectorstoreService):
    def __init__(self, store: FakeStore) -> None:
        self.store = store
        self._lexical_cache = {}

    def get_store(self):
        return self.store

    def get_page_store(self):
        return self.store

    @property
    def reranker(self):
        return FakeReranker()


def test_retrieve_applies_exact_equipment_filter_and_hybrid_ranking():
    store = FakeStore()
    service = FakeVectorstoreService(store)

    chunks = service.retrieve("alarma de puerta", "Esterilizadora Sterrad 100", role="operador")

    assert store.last_filter == {"equipment_name": "Esterilizadora Sterrad 100"}
    assert chunks
    assert "alarma de puerta" in chunks[0].text
    assert chunks[0].score is not None


def test_lexical_similarity_adds_weight_to_candidate():
    service = FakeVectorstoreService(FakeStore())

    chunks = service._lexical_candidates("alarma de puerta", "Esterilizadora Sterrad 100")

    assert chunks[0].citation.chunk_id == "a"
    assert float(chunks[0].score or 0.0) > 0


def test_retrieve_rejects_unscoped_search():
    service = FakeVectorstoreService(FakeStore())

    with pytest.raises(EquipmentScopeError):
        service.retrieve("alarma puerta", None)


def test_reranker_device_auto_uses_cuda_when_available(monkeypatch):
    service = FakeVectorstoreService(FakeStore())
    monkeypatch.setattr(vectorstore_module, "settings", SimpleNamespace(reranker_device="auto"))

    import torch

    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)

    assert service._resolve_reranker_device() == "cuda"


def test_reranker_device_auto_falls_back_to_cpu(monkeypatch):
    service = FakeVectorstoreService(FakeStore())
    monkeypatch.setattr(vectorstore_module, "settings", SimpleNamespace(reranker_device="auto"))

    import torch

    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)

    assert service._resolve_reranker_device() == "cpu"


def test_reranker_device_can_be_forced(monkeypatch):
    service = FakeVectorstoreService(FakeStore())
    monkeypatch.setattr(vectorstore_module, "settings", SimpleNamespace(reranker_device="cpu"))

    assert service._resolve_reranker_device() == "cpu"
