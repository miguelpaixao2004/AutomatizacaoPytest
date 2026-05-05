from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_listar_bebidas_geral():
    response = client.get("/bebidas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_listar_bebidas_com_filtro_tipo_e_alcoolica():
    response = client.get("/bebidas?tipo=cerveja&alcoolica=true")
    assert response.status_code == 200
    bebidas = response.json()
    assert len(bebidas) > 0
    for b in bebidas:
        assert b["tipo"] == "cerveja"
        assert b["alcoolica"] is True


def test_obter_bebida_existente():
    response = client.get("/bebidas/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_obter_bebida_inexistente():
    response = client.get("/bebidas/9999")
    assert response.status_code == 404


def test_criar_bebida_dados_validos():
    nova_bebida = {
        "nome": "Vinho Tinto",
        "tipo": "vinho",
        "alcoolica": True,
        "preco": 80.0,
    }
    response = client.post("/bebidas", json=nova_bebida)
    assert response.status_code == 201
    assert response.json()["nome"] == "Vinho Tinto"


def test_criar_bebida_dados_invalidos():
    bebida_invalida = {
        "nome": "Água",
        "tipo": "agua",
        "alcoolica": False,
        "preco": -5.0,
    }  # Preço negativo
    response = client.post("/bebidas", json=bebida_invalida)
    assert response.status_code == 422
