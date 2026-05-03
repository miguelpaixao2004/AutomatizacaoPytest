from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_criar_pedido_com_prato_existente_disponivel():
    # O Prato 1 (Pizza Margherita) custa 45.0 e está disponível
    pedido = {"prato_id": 1, "quantidade": 2}
    response = client.post("/pedidos", json=pedido)
    
    assert response.status_code == 201
    dados = response.json()
    assert dados["prato_id"] == 1
    assert dados["quantidade"] == 2
    assert dados["valor_total"] == 90.0 # 45.0 * 2

def test_criar_pedido_com_prato_inexistente():
    pedido = {"prato_id": 9999, "quantidade": 1}
    response = client.post("/pedidos", json=pedido)
    assert response.status_code == 404

def test_criar_pedido_com_prato_indisponivel():
    # O Prato 3 (Tiramisu Esgotado) tem disponivel=False no nosso banco de dados mock
    pedido = {"prato_id": 3, "quantidade": 1}
    response = client.post("/pedidos", json=pedido)
    assert response.status_code == 400