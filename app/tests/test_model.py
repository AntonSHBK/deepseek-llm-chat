def test_model_loads(model):
    """Проверка, что модель и токенизатор загружаются"""
    assert model.tokenizer is not None
    assert model.model is not None

def test_basic_generation(model):
    """Базовая генерация ответа"""
    prompt = "User: Привет! Что ты умеешь?\nBot:"
    response = model.generate(prompt, max_new_tokens=64)
    
    assert isinstance(response, str)
    assert len(response.strip()) > 0
    assert "User:" not in response
    assert "System:" in response or len(response) > 10

