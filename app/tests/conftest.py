import pytest

from app.models.deepseek_model import DeepSeekModel

@pytest.fixture(scope="module")
def model():
    return DeepSeekModel()
