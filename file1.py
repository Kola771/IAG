# https://www.gradio.app/guides/quickstart
# pip install gradio
 
import gradio as gr

def response(message, history):
    return "Bonjour " + message + " !"

demo = gr.ChatInterface(response)

demo.launch()