import redis
import json
import os

# Подключаемся к Redis, используя переменные окружения для гибкости
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"), 
    port=6379, 
    db=0, 
    decode_responses=True
)

def get_from_cache(key: str):
    """
    Получает результат из кэша.
    """
    return redis_client.get(key)

def set_to_cache(key: str, value: dict):
    """
    Сохраняет результат в кэш с TTL на 24 часа.
    """
    # Превращаем словарь в JSON-строку
    value_json = json.dumps(value, ensure_ascii=False)
    redis_client.set(key, value_json, ex=86400)