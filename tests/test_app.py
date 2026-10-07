from app import app


class DummyConnection:
    def close(self):
        pass


class DummyRedis:
    def __init__(self, *args, **kwargs):
        pass

    def ping(self):
        return True


def test_home_page(monkeypatch):
    monkeypatch.setattr("app.get_notes", lambda: ["test note"])
    monkeypatch.setattr("app.redis.Redis", DummyRedis)

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"RabTech Task 03 - Docker Demo" in response.data
    assert b"test note" in response.data


def test_health_when_dependencies_are_available(monkeypatch):
    monkeypatch.setattr("app.get_db_connection", lambda: DummyConnection())
    monkeypatch.setattr("app.redis.Redis", DummyRedis)

    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"
