# https://www.gradio.app/guides/quickstart
# pip install gradio
 
import openai
import gradio as gr

openai.api_type = "azure"
openai.api_base = "https://interstisopenaiformation.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = '6ea9703016b54b9686e3a744defdd5c3'


message_init_system = [{"role":"system","content":"Tu es un coach de gym."},{"role":"user","content":"bonjour"},{"role":"assistant","content":"Bonjour! Comment puis-je vous aider aujourd'hui?"},{"role":"user","content":"j'aimerais avoir quelques conseils pour prendre du poids"},{"role":"assistant","content":"Bien sûr, voici quelques conseils pour prendre du poids de manière saine:\n\n1. Augmentez votre apport calorique: Pour prendre du poids, vous devez consommer plus de calories que vous n'en brûlez. Essayez d'ajouter 500 calories à votre apport quotidien pour commencer.\n\n2. Choisissez des aliments riches en nutriments: Manger des aliments riches en nutriments tels que des fruits, des légumes, des noix, des graines, des viandes maigres, des poissons gras, des céréales complètes et des produits laitiers entiers vous aidera à prendre du poids tout en améliorant votre santé globale.\n\n3. Mangez plus souvent: Essayez de manger plus souvent tout au long de la journée, au lieu de trois gros repas. Cela peut aider à augmenter votre apport calorique.\n\n4. Ajoutez des collations riches en calories: Ajoutez des collations riches en calories à votre alimentation, comme des noix, du beurre de cacahuète, des fruits secs, des barres protéinées, etc.\n\n5. Faites de l'exercice: L'exercice peut vous aider à prendre du poids en développant votre masse musculaire. Essayez de faire de l'exercice de résistance, comme la musculation, pour développer votre masse musculaire.\n\n6. Soyez patient: Prendre du poids de manière saine peut prendre du temps. Soyez patient et persévérant dans vos efforts.\n\nJ'espère que ces conseils vous aideront à prendre du poids de manière saine!"},{"role":"user","content":"merci"},{"role":"assistant","content":"De rien, n'hésitez pas à me contacter si vous avez d'autres questions!"},{"role":"user","content":"donne-moi autres conseils"},{"role":"assistant","content":"Bien sûr, voici quelques autres conseils pour prendre du poids de manière saine:\n\n1. Évitez les aliments transformés: Les aliments transformés sont souvent riches en calories, mais pauvres en nutriments. Essayez de manger des aliments entiers et frais autant que possible.\n\n2. Buvez des shakes protéinés: Les shakes protéinés peuvent être un moyen facile et pratique d'augmenter votre apport en calories et en protéines. Essayez de faire un shake avec du lait entier, des fruits, du beurre de cacahuète et de la poudre de protéines.\n\n3. Dormez suffisamment: Le sommeil est important pour la croissance et la récupération musculaire. Essayez de dormir au moins 7 à 8 heures par nuit.\n\n4. Évitez les boissons gazeuses et les jus sucrés: Les boissons gazeuses et les jus sucrés sont riches en calories vides et peuvent contribuer à la prise de poids non désirée. Buvez plutôt de l'eau, du lait entier ou des jus de fruits frais.\n\n5. Consultez un professionnel de la santé: Si vous avez des problèmes de santé ou si vous avez du mal à prendre du poids, consultez un professionnel de la santé pour obtenir des conseils personnalisés.\n\nJ'espère que ces conseils vous aideront à atteindre vos objectifs de prise de poids de manière saine!"}]

message_init_user_1 = {
    "role": "assistant",
    "content": "Hello! It's nice to meet you. Is there anything I can help you with today ?"
    }
# fonction pour envoyer les messages
def response(message, history):
    # return "Bonjour " + message + " !"
    messages_history = []
    # messages_history.append(message_init_system)
    # messages_history = message_init_system + [{"role": "user", "content": message}]
    messages_history = message_init_system + [{"role": "user", "content": message}]


    for human, assistant in history:
        messages_history.append({"role": "user", "content": human})
        messages_history.append({"role": "assistant", "content": assistant})

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
    textbox=gr.Textbox(placeholder="Votre question : ", container=False, scale=7),
    title="VIPP Chat Open AI",
    description="Bonjour, à votre service !",
    theme="soft",
    examples=["qui est Christophe Colomb ?", " exemple 2"],
    cache_examples=True,
    retry_btn=None,
    undo_btn=None,
    clear_btn=None
).queue()

demo.launch()