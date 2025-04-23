from typing import List


class HistoryService:
    def __init__(self):
        self.history: List[str] = []

    def add_user_message(self, message: str):
        self.history.append(f"User: {message}")

    def add_bot_message(self, message: str):
        self.history.append(f"System: {message}")

    def get_formatted_prompt(self) -> str:
        """Возвращает всю историю как строку — для подачи в модель."""
        return "\n".join(self.history) + "\nSystem:"

    def clear_history(self):
        self.history.clear()

    def get_raw_history(self) -> List[str]:
        """Если нужно для UI или анализа."""
        return self.history.copy()
