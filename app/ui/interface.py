import logging

import gradio as gr

from app.config import settings
# from app.services.chat_service import get_chat_response, history_service

logger = logging.getLogger("app")


import logging
import gradio as gr
from app.config import settings

logger = logging.getLogger("app")


def blank_response(message, temperature, top_p, max_new_tokens, repetition_penalty):
    logger.info("Пользователь отправил сообщение в интерфейсе")
    return (
        f"Заглушка. Ответ не сгенерирован моделью.\n"
        f"message: {message}\n"
        f"temperature: {temperature}, top_p: {top_p}, max_new_tokens: {max_new_tokens}, repetition_penalty: {repetition_penalty}"
    )


def launch_ui(share: bool = False):
    logger.info("Запуск Gradio-интерфейса...")

    with gr.Blocks(title="Custom Chatbot") as demo:
        gr.Markdown(
            f"""
            ## Chatbot на базе {settings.MODEL_NAME}
            Введите сообщение и при необходимости настройте параметры генерации.
            """
        )

        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(label="Диалог")
                chat_state = gr.State([])

                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Введите сообщение и нажмите Enter или кнопку Отправить...",
                        show_label=False,
                        lines=2
                    )
                    send_btn = gr.Button("Отправить")

                clear_btn = gr.Button("Очистить чат")

            with gr.Column(scale=1):
                gr.Markdown("### Параметры генерации")
                temperature = gr.Slider(0.1, 1.5, value=0.7, step=0.1, label="Temperature")
                top_p = gr.Slider(0.1, 1.0, value=0.9, step=0.05, label="Top-p")
                max_tokens = gr.Slider(32, 1024, value=256, step=32, label="Max new tokens")
                repetition_penalty = gr.Slider(1.0, 2.0, value=1.1, step=0.1, label="Repetition penalty")

        def respond(message, chat_state, temperature, top_p, max_new_tokens, repetition_penalty):
            response = blank_response(message, temperature, top_p, max_new_tokens, repetition_penalty)
            chat_state = chat_state + [(message, response)]
            return "", chat_state, chat_state

        def clear_chat():
            logger.info("Чат очищен")
            # history_service.clear_history()
            return [], []

        # Привязка действий
        msg.submit(respond, inputs=[msg, chat_state, temperature, top_p, max_tokens, repetition_penalty], outputs=[msg, chatbot, chat_state])
        send_btn.click(respond, inputs=[msg, chat_state, temperature, top_p, max_tokens, repetition_penalty], outputs=[msg, chatbot, chat_state])
        clear_btn.click(fn=clear_chat, outputs=[chatbot, chat_state])

    demo.launch(share=share)