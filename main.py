# from dotenv import load_dotenv
import os
import openai

from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import AzureChatOpenAI
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings

import gradio as gr
import time 

from dotenv import load_dotenv

load_dotenv()

#load environment variables
# load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_DEPLOYMENT_ENDPOINT = os.getenv("OPENAI_API_BASE")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
OPENAI_DEPLOYMENT_VERSION = os.getenv("OPENAI_API_VERSION")

# Configuration de l'API OpenAI 
openai.api_type = "azure"
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_version = os.getenv('OPENAI_API_VERSION')

# Modèle de la complétion
llm = AzureChatOpenAI(
                      deployment_name=OPENAI_DEPLOYMENT_NAME,
                      model_name=OPENAI_MODEL_NAME,
                      openai_api_base=OPENAI_DEPLOYMENT_ENDPOINT,
                      openai_api_version=OPENAI_DEPLOYMENT_VERSION,
                      openai_api_key=OPENAI_API_KEY,
                      openai_api_type="azure")

# Modèle de l'embedding
MODEL = "sentence-transformers/msmarco-distilbert-cos-v5"
embeddings = HuggingFaceEmbeddings(
    model_name=MODEL,
    cache_folder=os.getenv("SENTENCE_TRANSFORMERS_HOME")
)


# Initialize gpt-35-turbo and our embedding model
# Chargement du vecteur FAISS chargé en mémoire 
vectorStore = FAISS.load_local("./output/faiss_index", embeddings)

# Utilisation du vecteur pour retrouver les bonnes informations localement 
retriever = vectorStore.as_retriever(search_type="similarity", search_kwargs={"k":2})


QUESTION_PROMPT = PromptTemplate.from_template("""Exprimes-toi dans un langue facile à comprendre et claire. Tu es Joe, un assistant intelligent qui ne peut que répondre aux questions liées à l'immobilier, l'energie et la fibre optique. Si la question ne concerne pas ni l'immobilier, ni la fibre optique, ni l'énergie, réponds par: Je ne sais pas !!!. Bases-toi sur les documentations qui te sont fournis.

    Chat History:
    {chat_history}
    Follow Up Input: {question}""")

qa = ConversationalRetrievalChain.from_llm(llm=llm,
                                            retriever=retriever,
                                            condense_question_prompt=QUESTION_PROMPT,
                                            return_source_documents=True,
                                            verbose=False)

def generate_response(message, history):
    print(f"\n\nMessage : {message}\n")

    # correction du format de l'historique (gradio : list[list] et qa : list[Tuple])
    # historique = []
    # for completion in history : 
    #     historique.append((completion[0], completion[1]))

    # print(f"Historique corrigé : {historique}\n")    

    # result = qa({"question": message, "chat_history": historique})
    result = qa({"question": message, "chat_history": []})

    message = result["answer"]
    source = result["source_documents"]
    print(f"Reponse : {message}\n")
    print(f"Source : {source}\n")

    # affichage en streaming
    for i in range(len(message)):
        time.sleep(0.01)
        yield message[: i+1]
    

iface = gr.ChatInterface(
                generate_response,
                textbox= gr.Textbox(placeholder="Posez des questions sur le document fourni", container=False, scale=7),
                title= "Chatbot Podcast",
                description="Démonstration chatbot langchain",
                theme="soft",
                retry_btn=None,
                undo_btn="Supprimer dernier message",
                clear_btn="Supprimer l'historique", 
                submit_btn="Envoyer"
)


if __name__ == "__main__":
    iface.queue().launch(auth = ('user','password'), auth_message = "Enter login and password:", share=True)
    