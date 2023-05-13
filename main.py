# chatbot using openai
# Author: Helidem
# Date: 13/05/2023
# Version: 1.0

import gradio as gr
import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("API_KEY")

# Set up initial chat history
chat_history = []

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")
    chat_history_gpt = []

    def respond(message, chat_history):
        chat_history_gpt.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly chatbot."},
                *chat_history_gpt
            ]
        )
        chat_history_gpt.append({"role": "system", "content": response.choices[0].message.content})
        chat_history.append((message, response.choices[0].message.content))

        return "", chat_history

    def clear_chat():
        chat_history_gpt.clear()
        chat_history.clear()

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(clear_chat, None, chatbot, queue=False)
    

demo.launch()

