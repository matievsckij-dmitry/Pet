from detoxify import Detoxify

print("Загрузка модели Detoxify...")
model = Detoxify('multilingual')
print("Модель загружена.")

def predict_toxicity(text: str) -> dict:
    """
    Делает предсказание и возвращает словарь с меткой и вероятностью.
    """
    predictions = model.predict(text)
    toxicity_score = float(predictions['toxicity'])
    
    if toxicity_score > 0.5:
        label = 'Токсичный'
    else:
        label = 'Не токсичный'
        
    return {"label": label, "score": toxicity_score}