# 1. Schema de resposta de GET /pratos/{id}
def test_contrato_get_prato_id(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200
    dados = response.json()

    campos_obrigatorios = {"id", "nome", "categoria", "preco", "disponivel"}
    assert campos_obrigatorios.issubset(
        dados.keys()
    ), "Campos obrigatórios ausentes no GET"

    assert isinstance(dados["id"], int)
    assert isinstance(dados["nome"], str)
    assert isinstance(
        dados["preco"], (float, int)
    )  # Aceita ambos para evitar erro com números inteiros
    assert isinstance(dados["disponivel"], bool)


# 2. Schema de resposta de POST /pratos
def test_contrato_post_prato(client):
    novo_prato = {
        "nome": "Risotto de Alho Poró",
        "categoria": "massa",
        "preco": 48.90,
        "disponivel": True,
    }
    response = client.post("/pratos", json=novo_prato)
    assert response.status_code == 201
    dados = response.json()

    # O POST deve retornar o prato criado com o novo ID
    assert "id" in dados
    assert dados["nome"] == "Risotto de Alho Poró"
    assert isinstance(dados["id"], int)


# 3. Schema de resposta de erro 404
def test_contrato_erro_404(client):
    response = client.get("/pratos/999999")
    assert response.status_code == 404
    dados = response.json()

    # O FastAPI por padrão usa a chave "detail"
    assert "detail" in dados
    assert isinstance(dados["detail"], str)
    assert len(dados["detail"]) > 0


# 4. Schema de resposta de erro 422 (Validação Pydantic)
def test_contrato_erro_422(client):
    # Enviando nome muito curto para forçar o 422
    prato_invalido = {"nome": "Ab", "categoria": "pizza", "preco": 10.0}
    response = client.post("/pratos", json=prato_invalido)

    assert response.status_code == 422
    dados = response.json()

    # Valida o formato padrão do FastAPI/Pydantic
    assert "detail" in dados
    assert isinstance(dados["detail"], list)

    for erro in dados["detail"]:
        assert "loc" in erro
        assert "msg" in erro
        assert isinstance(erro["loc"], list)
        assert isinstance(erro["msg"], str)
