from fastapi import FastAPI
from app.router.router import router as api_router

# Создаем экземпляр приложения
app = FastAPI(title="Toxicity Classifier API")

# Подключаем наш роутер
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в классификатор токсичности на API"}