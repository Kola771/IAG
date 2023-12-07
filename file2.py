# https://www.gradio.app/guides/quickstart
# pip install gradio
 
import openai
import gradio as gr

openai.api_type = "azure"
openai.api_base = "https://interstisopenaiformation.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = '6ea9703016b54b9686e3a744defdd5c3'


message_init_system = {"role":"system","content":"Tu sais comment gérer ton argent, ton capital jusqu'au point de le fructifier."}

message_init_user_1 = {
    "role": "assistant",
    "content": "En quoi puis-je t'aider ?"
    }

# fonction pour envoyer les messages
def response(message, history):
    # return "Bonjour " + message + " !"
    messages_history = []
    messages_history.append(message_init_system)
    messages_history.append(message_init_user_1)
    # messages_history = message_init_system + [{"role": "user", "content": message}]


    for human, assistant in history:
        messages_history.append({"role": "user", "content": human})
        messages_history.append({"role": "assistant", "content": assistant})
        messages_history.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        engine = "gpt35",
        messages = messages_history,
        temperature = 0.8,
        max_tokens = 500,
        top_p = 0.95,
        frequency_penalty = 0,
        presence_penalty = 0,
        stop = None
    )

    return response.choices[0].message["content"]


# demo = gr.ChatInterface(response)

demo = gr.ChatInterface(
    fn= response,
    chatbot=gr.Chatbot(),
    textbox=gr.Textbox(placeholder="Posez votre question : ", container=False, scale=7),
    title="Test Chat Open AI",
    description="Bonjour, à votre service !",
    theme="soft",
    retry_btn=None,
    undo_btn=None,
    clear_btn=None
).queue()

demo.launch()