from fastapi.testclient import TestClient
from app.main import app # Импортируем наш FastAPI-объект 'app'

# Создаем специальный тестовый клиент, который будет "общаться" с нашим API
# Это происходит в памяти, без реального запуска веб-сервера.
client = TestClient(app)

def test_read_main_root():
    """
    Тестирует корневой эндпоинт GЕТ /
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Добро пожаловать в классификатор токсичности на API"}

def test_predict_non_toxic():
    """
    Тестирует предсказание для нетоксичного текста.
    """
    response = client.post(
        "/predict_model",
        json={"text": "я очень люблю пиццу и хорошую погоду"}
    )
    # Проверяем, что запрос прошел успешно
    assert response.status_code == 200
    
    data = response.json()
    
    # Проверяем структуру ответа
    assert "label" in data
    assert "score" in data
    
    # Проверяем логику ответа
    assert data["label"] == "Не токсичный"
    assert isinstance(data["score"], float)

def test_predict_toxic():
    """
    Тестирует предсказание для токсичного текста.
    """
    response = client.post(
        "/predict_model",
        json={"text": "ты глупый идиот, я тебя ненавижу"}
    )
    assert response.status_code == 200
    
    data = response.json()
    
    assert "label" in data
    assert "score" in data
    
    assert data["label"] == "Токсичный"
    assert isinstance(data["score"], float)
    assert data["score"] > 0.5 # Ожидаем высокую вероятность токсичности

def test_predict_empty_text():
    """
    Тестирует, как API реагирует на пустой текст.
    """
    # FastAPI/Pydantic по умолчанию не пропустит такой запрос
    # и вернет ошибку 422 Unprocessable Entity
    response = client.post("/predict_model", json={"text": "   "})
    assert response.status_code == 422
