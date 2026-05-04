import pytest
import numpy as np

# Ajuste REPO_ID para o seu usuário e nome do modelo no Hugging Face
REPO_ID = "miguelpaixao2004/mlops-bella-tavola-v1" 

# ==========================================
# EXERCÍCIO 5.2: TESTANDO O MODELO PURO
# ==========================================

@pytest.fixture(scope="module")
def modelo():
    """
    Mock do modelo para isolar os testes do pipeline de CI/CD.
    Garante que a estrutura da API funciona independentemente do Hugging Face.
    """
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np
    
    # Features: [valor_pedido, hora_pedido, num_itens, historico_cancelamentos, distancia_entrega]
    X_dummy = np.array([[120.0, 20, 3.0, 0, 2.5], [50.0, 12, 1.0, 1, 1.0]])
    y_dummy = np.array([1, 0])
    
    clf = RandomForestClassifier(n_estimators=10, random_state=42)
    clf.fit(X_dummy, y_dummy)
    return clf

@pytest.fixture
def amostra_valida():
    # Array simulando: [valor_pedido, hora_pedido, num_itens, historico_cancelamentos, distancia_entrega]
    return np.array([[120.0, 20, 3.0, 0, 2.5]]) 

@pytest.mark.integracao
def test_modelo_carregado_nao_e_none(modelo):
    assert modelo is not None

@pytest.mark.integracao
def test_modelo_tem_metodo_predict(modelo):
    assert hasattr(modelo, "predict")

@pytest.mark.integracao
def test_modelo_tem_metodo_predict_proba(modelo):
    assert hasattr(modelo, "predict_proba")

@pytest.mark.integracao
def test_predict_retorna_array_com_formato_correto(modelo, amostra_valida):
    resultado = modelo.predict(amostra_valida)
    assert resultado.shape == (1,)
    assert resultado[0] in [0, 1]

@pytest.mark.integracao
def test_predict_proba_retorna_probabilidades_validas(modelo, amostra_valida):
    probas = modelo.predict_proba(amostra_valida)
    assert probas.shape == (1, 2)
    assert abs(probas[0].sum() - 1.0) < 1e-6
    assert all(0 <= p <= 1 for p in probas[0])

# ==========================================
# EXERCÍCIO 5.3: TESTANDO O ENDPOINT DA API
# ==========================================

PAYLOAD_VALIDO = {
    "valor_pedido": 120.0,
    "hora_pedido": 20,
    "num_itens": 3,
    "historico_cancelamentos": 0,
    "distancia_entrega": 2.5
}

@pytest.mark.integracao
def test_predict_retorna_200(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert response.status_code == 200

@pytest.mark.integracao
def test_predict_retorna_campos_esperados(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    dados = response.json()
    assert "prediction" in dados
    assert "probability" in dados
    assert "label" in dados

@pytest.mark.integracao
def test_predict_prediction_e_binario(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert response.json()["prediction"] in [0, 1]

@pytest.mark.integracao
def test_predict_sem_campo_obrigatorio_retorna_422(client):
    payload_incompleto = {"valor_pedido": 120.0}
    response = client.post("/ml/predict", json=payload_incompleto)
    assert response.status_code == 422

@pytest.mark.integracao
@pytest.mark.parametrize("campo,valor_invalido", [
    ("hora_pedido", 25),       # hora fora de 0-23
    ("hora_pedido", -1),       # hora negativa
    ("num_itens", 0),          # quantidade inválida
    ("valor_pedido", -50.0),   # valor negativo
])
def test_predict_campo_invalido_retorna_422(client, campo, valor_invalido):
    payload = {**PAYLOAD_VALIDO, campo: valor_invalido}
    response = client.post("/ml/predict", json=payload)
    assert response.status_code == 422