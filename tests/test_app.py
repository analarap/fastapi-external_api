import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_get_success(mocker):
    """Mock para GET bem-sucedido"""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"userId": 1, "id": 1, "title": "Post 1", "body": "Conteúdo"}
    ]
    mocker.patch("app.main.requests.get", return_value=mock_response)
    return mock_response


@pytest.fixture
def mock_get_fail(mocker):
    """Mock para GET com falha"""
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch("app.main.requests.get", return_value=mock_response)
    return mock_response


@pytest.fixture
def mock_post_success(mocker):
    """Mock para POST bem-sucedido"""
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 101,
        "title": "Novo Post",
        "body": "Texto de teste",
        "userId": 1,
    }
    mocker.patch("app.main.requests.post", return_value=mock_response)
    return mock_response


@pytest.fixture
def mock_post_fail(mocker):
    """Mock para POST com falha"""
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mocker.patch("app.main.requests.post", return_value=mock_response)
    return mock_response


def test_listar_dados_sucesso(mock_get_success):
    response = client.get("/data")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["title"] == "Post 1"


def test_buscar_dado_sucesso(mock_get_success):
    mock_get_success.json.return_value = {
        "userId": 1,
        "id": 1,
        "title": "Post 1",
        "body": "Conteúdo",
    }
    response = client.get("/data/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_criar_dado_sucesso(mock_post_success):
    novo_post = {"title": "Novo Post", "body": "Texto de teste", "userId": 1}
    response = client.post("/data", json=novo_post)
    assert response.status_code == 201 or response.status_code == 200
    assert response.json()["title"] == "Novo Post"


def test_listar_dados_falha(mock_get_fail):
    response = client.get("/data")
    assert response.status_code == 500


def test_buscar_dado_falha(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch("app.main.requests.get", return_value=mock_response)
    response = client.get("/data/9999")
    assert response.status_code == 404


def test_criar_dado_falha():
    response = client.post("/data", json={"title": "Sem campos obrigatórios"})
    assert response.status_code == 400
