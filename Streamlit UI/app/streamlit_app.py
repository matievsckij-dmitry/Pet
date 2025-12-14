import streamlit as st
import requests
import os
from requests.exceptions import ConnectionError, RequestException

# --- Конфигурация API ---
# Читаем хост и порт API из переменных окружения.
# Если они не заданы, используем значения по умолчанию для локального запуска.
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))

# Собираем полный URL для эндпоинта
API_URL = f"http://{API_HOST}:{API_PORT}/predict_model"

# --- Функция для вызова API ---
def get_prediction(text: str):
    """Отправляет текст в API и возвращает результат или ошибку."""
    payload = {"text": text}
    try:
        # Устанавливаем таймаут, чтобы не ждать вечно
        resp = requests.post(API_URL, json=payload, timeout=20)
        # Проверяем, не вернул ли сервер ошибку (код 4xx или 5xx)
        resp.raise_for_status()
        return resp.json(), None  # Возвращаем данные и отсутствие ошибки
    except ConnectionError:
        error_message = f"Не удалось подключиться к API по адресу: {API_URL}. Убедитесь, что FastAPI-сервер запущен."
        return None, error_message
    except RequestException as e:
        # Другие ошибки, связанные с запросом (например, таймаут)
        error_message = f"Ошибка запроса к API: {e}"
        return None, error_message
    except ValueError: # Может возникнуть, если resp.json() не сможет распарсить ответ
        error_message = "Не удалось прочитать ответ от API. Ответ не является корректным JSON."
        return None, error_message


# --- Интерфейс приложения ---
st.title("Классификатор токсичности текста")
st.write("Введите текст для анализа:")

text = st.text_area("Текст", value="Пример текста для проверки", height=150, key="text_input")

if st.button("Анализировать"):
    if not text.strip():
        st.error("Введите, пожалуйста, непустой текст.")
    else:
        with st.spinner('Анализирую...'):
            data, error = get_prediction(text)

        if error:
            st.error(error)
        elif data:
            if "label" in data and "score" in data:
                label, score = data["label"], data["score"]
                
                st.success(f"Классификация: {label}")
                st.write(f"Вероятность токсичности: {score:.3f} ({score*100:.1f}%)")
                st.progress(score)
            else:
                st.error("API вернул ответ в неожиданном формате.")
                st.json(data)

st.info(f"Приложение подключено к API по адресу: {API_URL}")