from fastapi import APIRouter, HTTPException
import json

# Импортируем наши модули
from app.data_models.pydantic_models import PredictionInput
from app.services.model import predict_toxicity
from app.services.cache import get_from_cache, set_to_cache, redis_client

# Создаем роутер
router = APIRouter()

@router.get("/health")
def health():
    try:
        redis_client.ping()
        return {"status": "OK", "redis_status": "OK"}
    except Exception:
        return {"status": "OK", "redis_status": "Error"}

@router.post("/predict_model")
def predict_model(input_data: PredictionInput):
    text_to_predict = input_data.text.strip()

    if not text_to_predict:
        raise HTTPException(status_code=422, detail="Text cannot be empty.")

    # 1. Проверяем кэш
    cached_result = get_from_cache(text_to_predict)
    if cached_result:
        print(f"Cache HIT for: '{text_to_predict}'")
        return json.loads(cached_result)

    # 2. Если в кэше нет, вызываем модель
    print(f"Cache MISS for: '{text_to_predict}'")
    result = predict_toxicity(text_to_predict)

    # 3. Сохраняем в кэш
    set_to_cache(text_to_predict, result)

    return result