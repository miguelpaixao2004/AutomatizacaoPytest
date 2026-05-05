from main import app  # Garanta que o nome do seu arquivo principal é main.py


# 1. GET /pratos retorna status 200 e uma lista
def test_listar_pratos_retorna_status_200_e_lista(client):
    response = client.get("/pratos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 2. GET /pratos?categoria=pizza retorna apenas pratos da categoria correta
def test_listar_pratos_por_categoria_pizza(client):
    response = client.get("/pratos?categoria=pizza")
    assert response.status_code == 200
    pratos = response.json()

    # Valida se a lista não veio vazia e se todos são da categoria certa
    assert len(pratos) > 0
    for prato in pratos:
        assert prato["categoria"].lower() == "pizza"


# 3. GET /pratos/1 retorna um prato com os campos esperados
def test_obter_prato_por_id_valido(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200
    prato = response.json()

    # Verifica se as chaves existem no dicionário retornado
    assert "id" in prato
    assert "nome" in prato
    assert "preco" in prato
    assert prato["id"] == 1


# 4. GET /pratos/9999 retorna status 404
def test_obter_prato_id_inexistente_retorna_404(client):
    response = client.get("/pratos/9999")
    assert response.status_code == 404


# --- NOVOS TESTES DE POST ---


def test_criar_prato_retorna_sucesso(client):
    novo_prato = {
        "nome": "Funghi Trifolati",
        "categoria": "massa",
        "preco": 54.0,
        "disponivel": True,
    }
    response = client.post("/pratos", json=novo_prato)
    assert response.status_code in [200, 201]
    assert response.json()["nome"] == "Funghi Trifolati"


def test_criar_prato_com_preco_negativo_retorna_422(client):
    prato_invalido = {"nome": "Prato Inválido", "categoria": "pizza", "preco": -10.0}
    response = client.post("/pratos", json=prato_invalido)
    assert response.status_code == 422


def test_criar_prato_com_nome_muito_curto_retorna_422(client):
    prato_invalido = {
        "nome": "Pi",  # Menos de 3 caracteres
        "categoria": "pizza",
        "preco": 40.0,
    }
    response = client.post("/pratos", json=prato_invalido)
    assert response.status_code == 422


def test_criar_prato_com_categoria_invalida_retorna_422(client):
    prato_invalido = {
        "nome": "Prato Estranho",
        "categoria": "churrasco",  # Categoria não permitida
        "preco": 40.0,
    }
    response = client.post("/pratos", json=prato_invalido)
    assert response.status_code == 422


def test_prato_criado_aparece_no_get(client):
    prato_unico = {
        "nome": "Ravioli Especial de Teste",
        "categoria": "massa",
        "preco": 65.0,
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


# Teste A: Contagem exata
def test_lista_pratos_nao_esta_vazia(client):
    response = client.get("/pratos")
    assert response.status_code == 200
    assert len(response.json()) > 0  # Robusto: funciona com 1 ou 100 pratos


# Teste B: Dependência de ordem
def test_margherita_está_presente_na_lista(client):
    response = client.get("/pratos")
    nomes = [prato["nome"] for prato in response.json()]
    assert "Pizza Margherita" in nomes  # Robusto: procura em qualquer posição


# Teste C: ID Previsóvel
def test_novo_prato_recebe_um_id_valido(client, prato_valido):
    response = client.post("/pratos", json=prato_valido)
    dados = response.json()
    assert "id" in dados  # Robusto: verifica se a chave existe
    assert isinstance(dados["id"], int)  # E se é um número inteiro


# Teste D: Volume de dados fixos
def test_filtro_pizza_retorna_apenas_pizzas(client):
    response = client.get("/pratos?categoria=pizza")
    pratos = response.json()
    for prato in pratos:
        assert (
            prato["categoria"].lower() == "pizza"
        )  # Robusto: valida a lógica do filtro


import pytest


# 1. Categorias inválidas retornam 422
@pytest.mark.parametrize(
    "categoria_ruim", ["japonesa", "churrasco", "esoterica", "fast-food"]
)
def test_categorias_invalidas_retornam_422(client, categoria_ruim):
    prato = {"nome": "Prato Teste", "categoria": categoria_ruim, "preco": 35.0}
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422


# 2. IDs inexistentes retornam 404
@pytest.mark.parametrize("id_inexistente", [9999, 8888, 123456, 7777])
def test_ids_inexistentes_retornam_404(client, id_inexistente):
    response = client.get(f"/pratos/{id_inexistente}")
    assert response.status_code == 404


# 3. Filtro de categoria funciona para cada categoria válida
@pytest.mark.parametrize("categoria_valida", ["pizza", "massa", "entrada", "sobremesa"])
def test_filtro_categoria_funciona_corretamente(client, categoria_valida):
    # Primeiro garantimos que existe ao menos um prato daquela categoria para o teste ser real
    prato_exemplo = {
        "nome": f"Exemplo {categoria_valida}",
        "categoria": categoria_valida,
        "preco": 20.0,
    }
    client.post("/pratos", json=prato_exemplo)

    # Agora testamos o filtro
    response = client.get(f"/pratos?categoria={categoria_valida}")
    assert response.status_code == 200

    pratos_filtrados = response.json()
    for prato in pratos_filtrados:
        assert prato["categoria"].lower() == categoria_valida.lower()


# 5. Categorias inválidas retornam 422
@pytest.mark.smoke
def test_categorias_invalidas_retornam_422(client, categoria_ruim):
    prato = {"nome": "Prato Teste", "categoria": categoria_ruim, "preco": 35.0}
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422


@pytest.mark.validacao  # <--- Marcador de grupo
@pytest.mark.parametrize(
    "categoria_ruim", ["japonesa", "churrasco", "esoterica", "fast-food"]
)  # <--- O fornecedor de dados
def test_categorias_invalidas_retornam_422(client, categoria_ruim):
    prato = {"nome": "Prato Teste", "categoria": categoria_ruim, "preco": 35.0}
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422


# 2. IDs inexistentes retornam 404
@pytest.mark.smoke
@pytest.mark.parametrize(
    "id_inexistente", [9999, 8888]
)  # O parametrize PRECISA estar aqui
def test_ids_inexistentes_retornam_404(client, id_inexistente):
    response = client.get(f"/pratos/{id_inexistente}")
    assert response.status_code == 404


# 3. Filtro de categoria funciona para cada categoria válida
@pytest.mark.smoke
@pytest.mark.parametrize("categoria_valida", ["pizza", "massa"])
def test_filtro_categoria_funciona_corretamente(client, categoria_valida):
    response = client.get(f"/pratos?categoria={categoria_valida}")
    assert response.status_code == 200


# 3. Filtro de categoria funciona para cada categoria válida
@pytest.mark.smoke
@pytest.mark.parametrize("categoria_valida", ["pizza", "massa", "entrada", "sobremesa"])
def test_filtro_categoria_funciona_corretamente(client, categoria_valida):
    # Primeiro garantimos que existe ao menos um prato daquela categoria para o teste ser real
    prato_exemplo = {
        "nome": f"Exemplo {categoria_valida}",
        "categoria": categoria_valida,
        "preco": 20.0,
    }
    client.post("/pratos", json=prato_exemplo)

    # Agora testamos o filtro
    response = client.get(f"/pratos?categoria={categoria_valida}")
    assert response.status_code == 200

    pratos_filtrados = response.json()
    for prato in pratos_filtrados:
        assert prato["categoria"].lower() == categoria_valida.lower()
