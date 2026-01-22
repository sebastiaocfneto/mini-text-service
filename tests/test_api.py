from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_info():
    r = client.get("/info")
    assert r.status_code == 200
    data = r.json()
    assert data["service"] == "mini-text-service"
    assert "/classify" in data["endpoints"]


def test_classify_pergunta():
    r = client.post("/classify", json={"text": "Como faço para isso?"})
    assert r.status_code == 200
    data = r.json()
    assert data["category"] == "pergunta"
    assert 0.0 <= data["confidence"] <= 1.0
    assert data["strategy"] == "rules"
    assert isinstance(data["elapsed_ms"], int)


def test_classify_reclamacao():
    r = client.post("/classify", json={"text": "Não funciona, deu erro aqui."})
    assert r.status_code == 200
    assert r.json()["category"] == "reclamacao"


def test_classify_relato_default():
    r = client.post("/classify", json={"text": "Hoje testei o sistema e registrei um caso."})
    assert r.status_code == 200
    assert r.json()["category"] == "relato"


def test_invalid_strategy():
    r = client.post("/classify", json={"text": "Oi", "strategy": "model"})
    assert r.status_code == 400
    assert r.json()["detail"] == "unsupported strategy"
