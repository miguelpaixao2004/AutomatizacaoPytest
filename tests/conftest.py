import pytest
from fastapi.testclient import TestClient
from main import app   # ajuste se necessário

client = TestClient(app)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def prato_valido():
    """Payload de prato válido reutilizável nos testes."""
    return {
        "nome": "Prato de Teste",
        "categoria": "massa",
        "preco": 40.0,
        "disponivel": True
    }