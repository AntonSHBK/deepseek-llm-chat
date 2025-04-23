import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

from app.config import settings

logger = logging.getLogger("model")


class DeepSeekModel:
    def __init__(self):
        logger.info("Загрузка токенизатора и модели DeepSeek...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            settings.MODEL_NAME,
            cache_dir=settings.CACHE_DIR
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            settings.MODEL_NAME,
            cache_dir=settings.CACHE_DIR
        )
        self.model.eval()
        logger.info(f"Модель загружена на устройство: {settings.DEVICE}")

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 512,
        do_sample: bool = True,
        temperature: float = 0.7,
        top_k: int = 50,
        top_p: float = 0.95,
        repetition_penalty: float = 1.0,
        num_beams: int = 1,
        no_repeat_ngram_size: int = 0,
        early_stopping: bool = False,
    ) -> str:
        logger.debug(f"Генерация ответа для: {prompt}")

        inputs = self.tokenizer(prompt, return_tensors="pt").to(settings.DEVICE)

        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                repetition_penalty=repetition_penalty,
                num_beams=num_beams,
                no_repeat_ngram_size=no_repeat_ngram_size,
                early_stopping=early_stopping,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)
        logger.debug(f"Результат генерации: {decoded}")
        return decoded

    def generate_response(self, prompt: str) -> str:
        """Обёртка для простого использования с параметрами по умолчанию."""
        return self.generate(prompt=prompt)
