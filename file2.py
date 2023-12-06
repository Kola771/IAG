# https://www.gradio.app/guides/quickstart
# pip install gradio
 
import openai
import gradio as gr

openai.api_type = "azure"
openai.api_base = "https://interstisopenaiformation.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = '6ea9703016b54b9686e3a744defdd5c3'


message_init_system = [{"role":"system","content":"Tu sais comment gérer ton argent, ton capital jusqu'au point de le fructifier."},{"role":"user","content":"bonsoir"},{"role":"assistant","content":"Bonsoir! Comment puis-je vous aider ce soir?"},{"role":"user","content":"aide-moi à me développer financièrement"},{"role":"assistant","content":"Bien sûr, je serais ravi de vous aider à vous développer financièrement. Voici quelques étapes que vous pouvez suivre pour y parvenir :\n\n1. Établissez un budget : Il est important de savoir combien vous gagnez et combien vous dépensez chaque mois. Établissez un budget pour vous aider à suivre vos dépenses et à économiser de l'argent.\n\n2. Économisez de l'argent : Trouvez des moyens d'économiser de l'argent chaque mois, que ce soit en réduisant vos dépenses ou en augmentant vos revenus.\n\n3. Investissez dans votre éducation financière : Apprenez à gérer votre argent en lisant des livres, en suivant des cours en ligne ou en travaillant avec un conseiller financier.\n\n4. Investissez votre argent : Investissez votre argent dans des actions, des obligations ou des fonds indiciels pour augmenter votre richesse à long terme.\n\n5. Planifiez votre retraite : Commencez à planifier votre retraite dès maintenant en investissant dans un compte de retraite individuel (IRA) ou un plan 401(k) offert par votre employeur.\n\n6. Établissez des objectifs financiers : Établissez des objectifs financiers à court et à long terme pour vous aider à rester motivé et à atteindre vos objectifs.\n\nJ'espère que ces conseils vous aideront à vous développer financièrement. N'hésitez pas à me poser des questions si vous en avez besoin."},{"role":"user","content":"merci"},{"role":"assistant","content":"De rien, n'hésitez pas à me contacter si vous avez besoin d'autres conseils ou d'aide pour votre développement financier. Bonne chance!"},{"role":"user","content":"donne-moi autres conseils"},{"role":"assistant","content":"Bien sûr, voici quelques autres conseils pour vous aider à vous développer financièrement :\n\n1. Évitez les dettes à taux d'intérêt élevé : Évitez les dettes à taux d'intérêt élevé, comme les cartes de crédit, car elles peuvent vous coûter cher à long terme.\n\n2. Économisez pour les urgences : Économisez de l'argent pour les urgences afin de pouvoir faire face à des dépenses imprévues, comme des réparations de voiture ou des frais médicaux.\n\n3. Évitez les dépenses inutiles : Évitez les dépenses inutiles, comme les achats impulsifs, les abonnements que vous n'utilisez pas et les repas à emporter coûteux.\n\n4. Négociez vos factures : Négociez vos factures, comme votre facture de câble ou de téléphone, pour obtenir un meilleur tarif.\n\n5. Établissez un plan de remboursement de dettes : Si vous avez des dettes, établissez un plan de remboursement pour vous aider à rembourser vos dettes plus rapidement.\n\n6. Augmentez vos revenus : Trouvez des moyens d'augmenter vos revenus, comme en travaillant des heures supplémentaires, en lançant une entreprise parallèle ou en vendant des articles que vous n'utilisez plus.\n\n7. Établissez des objectifs d'épargne : Établissez des objectifs d'épargne pour vous aider à atteindre vos objectifs financiers à long terme, comme l'achat d'une maison ou la retraite.\n\nJ'espère que ces conseils vous aideront à vous"}]

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
    textbox=gr.Textbox(placeholder="Posez votre question : ", container=False, scale=7),
    title="Test Chat Open AI",
    description="Bonjour, à votre service !",
    theme="soft",
    retry_btn=None,
    undo_btn=None,
    clear_btn=None
).queue()

demo.launch()