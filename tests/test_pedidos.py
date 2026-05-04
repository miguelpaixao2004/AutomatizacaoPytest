from fastapi.testclient import TestClient
from main import app

# tests/test_pedidos.py

def test_criar_pedido_com_prato_existente_disponivel(client):
    pedido = {"prato_id": 1, "quantidade": 2}
    response = client.post("/pedidos", json=pedido)
    assert response.status_code == 201
    assert response.json()["valor_total"] == 90.0 # 45.0 * 2

def test_criar_pedido_com_prato_inexistente(client):
    pedido = {"prato_id": 9999, "quantidade": 1}
    response = client.post("/pedidos", json=pedido)
    assert response.status_code == 404

def test_criar_pedido_com_prato_indisponivel(client):
    # O Prato 3 é o Tiramisu que marcamos como disponível=False no main.py
    pedido = {"prato_id": 3, "quantidade": 1}
    response = client.post("/pedidos", json=pedido)
    assert response.status_code == 400