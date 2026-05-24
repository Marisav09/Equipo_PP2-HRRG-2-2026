from __future__ import annotations

import pytest
from langchain_core.documents import Document

from app.core.exceptions import EquipmentScopeError
from app.services.vectorstore_service import VectorstoreService


class FakeCollection:
    def count(self) -> int:
        return 2


class FakeStore:
    def __init__(self) -> None:
        self._collection = FakeCollection()
        self.last_filter = None

    def similarity_search_with_score(self, question, k, filter):
        self.last_filter = filter
        return [
            (
                Document(
                    page_content="Procedimiento correcto para Sterrad 100.",
                    metadata={
                        "equipment_name": "Esterilizadora Sterrad 100",
                        "source_file": "manual_sterrad.pdf",
                        "page": 12,
                        "chunk_id": "a",
                    },
                ),
                0.12,
            ),
            (
                Document(
                    page_content="Este fragmento pertenece a otro equipo y debe descartarse.",
                    metadata={
                        "equipment_name": "Rodantes MAC GMM",
                        "source_file": "manual_mac.pdf",
                        "page": 3,
                        "chunk_id": "b",
                    },
                ),
                0.20,
            ),
        ]


class FakeVectorstoreService(VectorstoreService):
    def __init__(self, store: FakeStore) -> None:
        self.store = store

    def get_store(self):
        return self.store


def test_retrieve_applies_exact_equipment_filter():
    store = FakeStore()
    service = FakeVectorstoreService(store)

    chunks = service.retrieve("alarma puerta", "Esterilizadora Sterrad 100")

    assert store.last_filter == {"equipment_name": "Esterilizadora Sterrad 100"}
    assert len(chunks) == 1
    assert chunks[0].citation.equipment_name == "Esterilizadora Sterrad 100"
    assert "Sterrad" in chunks[0].text


def test_retrieve_rejects_unscoped_search():
    service = FakeVectorstoreService(FakeStore())

    with pytest.raises(EquipmentScopeError):
        service.retrieve("alarma puerta", None)
