from __future__ import annotations

from app.services.system_health_service import SystemHealthService


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self):
        return self.payload


class FakeCollection:
    def __init__(self, count: int) -> None:
        self._count = count

    def count(self) -> int:
        return self._count


class FakeStore:
    def __init__(self, count: int) -> None:
        self._collection = FakeCollection(count)


class FakeVectorstore:
    def __init__(self, count: int = 3) -> None:
        self.count = count

    def get_store(self):
        return FakeStore(self.count)


class FakeAudit:
    def __init__(self, documents):
        self.documents = documents

    def list_latest(self):
        return self.documents


def test_system_health_ok_when_dependencies_are_ready():
    def http_get(url, timeout):
        return FakeResponse(
            {
                "models": [
                    {"name": "llama3.2:3b"},
                    {"name": "nomic-embed-text:latest"},
                ]
            }
        )

    service = SystemHealthService(
        vectorstore=FakeVectorstore(count=10),
        audit_service=FakeAudit([{"status": "indexed"}]),
        http_get=http_get,
    )

    result = service.check()

    assert result["ok"] is True
    assert result["status"] == "ok"


def test_system_health_degraded_when_models_are_missing():
    def http_get(url, timeout):
        return FakeResponse({"models": [{"name": "llama3.2:3b"}]})

    service = SystemHealthService(
        vectorstore=FakeVectorstore(count=0),
        audit_service=FakeAudit([]),
        http_get=http_get,
    )

    result = service.check()

    assert result["ok"] is False
    assert result["status"] == "degraded"
    assert "nomic-embed-text" in result["components"]["ollama"]["missing_models"][0]
