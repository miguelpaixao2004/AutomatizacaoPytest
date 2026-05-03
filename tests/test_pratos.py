from fastapi.testclient import TestClient
from main import app  # Garanta que o nome do seu arquivo principal é main.py

client = TestClient(app)

# 1. GET /pratos retorna status 200 e uma lista
def test_listar_pratos_retorna_status_200_e_lista():
    response = client.get("/pratos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# 2. GET /pratos?categoria=pizza retorna apenas pratos da categoria correta
def test_listar_pratos_por_categoria_pizza():
    response = client.get("/pratos?categoria=pizza")
    assert response.status_code == 200
    pratos = response.json()
    
    # Valida se a lista não veio vazia e se todos são da categoria certa
    assert len(pratos) > 0 
    for prato in pratos:
        assert prato["categoria"].lower() == "pizza"

# 3. GET /pratos/1 retorna um prato com os campos esperados
def test_obter_prato_por_id_valido():
    response = client.get("/pratos/1")
    assert response.status_code == 200
    prato = response.json()
    
    # Verifica se as chaves existem no dicionário retornado
    assert "id" in prato
    assert "nome" in prato
    assert "preco" in prato
    assert prato["id"] == 1

# 4. GET /pratos/9999 retorna status 404
def test_obter_prato_id_inexistente_retorna_404():
    response = client.get("/pratos/9999")
    assert response.status_code == 404

# --- NOVOS TESTES DE POST ---

def test_criar_prato_retorna_sucesso():
    novo_prato = {
        "nome": "Funghi Trifolati",
        "categoria": "massa",
        "preco": 54.0,
        "disponivel": True
    }
    response = client.post("/pratos", json=novo_prato)
    assert response.status_code in [200, 201]
    assert response.json()["nome"] == "Funghi Trifolati"

def test_criar_prato_com_preco_negativo_retorna_422():
    prato_invalido = {
        "nome": "Prato Inválido",
        "categoria": "pizza",
        "preco": -10.0
    }
    response = client.post("/pratos", json=prato_invalido)
    assert response.status_code == 422

def test_criar_prato_com_nome_muito_curto_retorna_422():
    prato_invalido = {
        "nome": "Pi", # Menos de 3 caracteres
        "categoria": "pizza",
        "preco": 40.0
    }
    response = client.post("/pratos", json=prato_invalido)
    assert response.status_code == 422

def test_criar_prato_com_categoria_invalida_retorna_422():
    prato_invalido = {
        "nome": "Prato Estranho",
        "categoria": "churrasco", # Categoria não permitida
        "preco": 40.0
    }
    response = client.post("/pratos", json=prato_invalido)
    assert response.status_code == 422

def test_prato_criado_aparece_no_get():
    prato_unico = {
        "nome": "Ravioli Especial de Teste",
        "categoria": "massa",
        "preco": 65.0
    }
    # 1. Cria o prato com POST
    client.post("/pratos", json=prato_unico)
    
    # 2. Faz o GET para ver se ele foi parar na lista
    response = client.get("/pratos")
    lista_pratos = response.json()
    
    # Pega apenas os nomes dos pratos na lista
    nomes_dos_pratos = [prato["nome"] for prato in lista_pratos]
    
    # Verifica se o nome único que criamos está na lista
    assert "Ravioli Especial de Teste" in nomes_dos_pratos