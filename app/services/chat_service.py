import logging

from app.models.deepseek_model import DeepSeekModel
from app.services.history_service import HistoryService


logger = logging.getLogger("app")

# Инициализируем один раз
model = DeepSeekModel()
history_service = HistoryService()


def get_chat_response(user_input: str) -> str:
    logger.info("Получено сообщение от пользователя")

    # Обновляем историю
    history_service.add_user_message(user_input)
    prompt = history_service.get_formatted_prompt()

    logger.debug(f"Промпт для модели:\n{prompt}")

    # Генерация ответа
    raw_response = model.generate(prompt=prompt)
    response = clean_response(raw_response)

    # Обновляем историю
    history_service.add_bot_message(response)
    logger.info("Ответ сгенерирован и добавлен в историю")

    return response


def clean_response(raw_text: str) -> str:
    """
    Извлекаем ответ из общего текста, отсекая prompt и лишнее.
    """
    if "Bot:" in raw_text:
        parts = raw_text.split("Bot:")
        return parts[-1].strip()
    return raw_text.strip()
