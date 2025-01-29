from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class DeepSeekModel:
    def __init__(self, model_name="deepseek-ai/deepseek-vl2-small ", device=None):
        """
        Инициализация модели DeepSeek-V3
        :param model_name: Имя модели на Hugging Face
        :param device: Устройство для работы с моделью ("cuda" / "cpu")
        """
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        # Загрузка модели и токенизатора
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
        
        # Перемещение модели на нужное устройство
        self.model.to(self.device)
        self.model.eval()  # Переключение в режим инференса

    def generate_response(self, prompt: str, context: list = None, max_length: int = 512, temperature: float = 0.7, top_p: float = 0.9):
        """
        Генерация ответа модели на основе входного промпта и контекста
        :param prompt: Входное сообщение пользователя
        :param context: История диалога (список строк)
        :param max_length: Максимальная длина ответа
        :param temperature: Параметр случайности вывода
        :param top_p: Параметр nucleus-sampling (отбор вероятностных токенов)
        :return: Сгенерированный ответ модели
        """
        if context:
            full_prompt = "\n".join(context) + "\n" + prompt
        else:
            full_prompt = prompt

        # Токенизация входного текста
        inputs = self.tokenizer(full_prompt, return_tensors="pt", truncation=True, max_length=1024)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Генерация ответа модели
        with torch.no_grad():
            output_tokens = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True
            )

        # Декодирование ответа
        response = self.tokenizer.decode(output_tokens[0], skip_special_tokens=True)
        
        # Удаление оригинального промпта из вывода (если модель его повторяет)
        response = response.replace(full_prompt, "").strip()
        
        return response

# Создаем экземпляр модели при старте сервера
# deepseek_model = DeepSeekModel()
