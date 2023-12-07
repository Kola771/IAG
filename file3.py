# -------------------------------------------------------------------------------- LIBRAIRIES
# import numpy as np
# import time 
import io
import os
import logging
import collections
# import tempfile
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders.word_document import Docx2txtLoader
from langchain.document_loaders import UnstructuredFileLoader, UnstructuredExcelLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# -------------------------------------------------------------------------------- MODELE
# Le model qu'on veut utiliser
MODEL = "sentence-transformers/msmarco-distilbert-cos-v5"
# Le nombre de tokens par chunk c-à-d le nombre de token par section de documents
CHUNK_SIZE = 1000
# Le nombre de tokens de recouvrement entre deux sections
CHUNK_OVERLAP = 200

# Le dossier contenant les documents
folder = "iag"

# Le dossier contenant la base de données des indexes
output_folder = "GEN_ALPHA_EMBEDDING"

# Le model qu'on utilise pour faire toutes les manipulations
embeddings = HuggingFaceEmbeddings(
    model_name=MODEL,
    # cache_folder=os.getenv("SENTENCE_TRANSFORMERS_HOME")
    cache_folder=None
)

# Tout ce qui a lien avec le contenu de chaque document
text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = CHUNK_SIZE,
    chunk_overlap  = CHUNK_OVERLAP,
    length_function = len,
)

# -------------------------------------------------------------------------------- FONCTIONS
# Pour chercher les fichiers contenus dans le répertoire 'folder'
def list_paths_in_partition(folder):
    paths = [folder + '\\' + f for f in os.listdir(folder)]
    stop = False
    while not stop :
        stop = True
        for path in paths :
            if os.path.isdir(path) : 
                paths.remove(path)
                paths += [path + "\\" + f for f in os.listdir(path)]
                stop = False
    return(paths)

# -------------------------------------------------------------------------------- CODE
# paths récupère tous les documents contenus dans le répertoire 'folder'
paths = list_paths_in_partition(folder) 
filenames = set([os.path.basename(f) for f in paths])

to_keep = set()

# Chargements des index des documents (s'ils ont déjà été construit)
#      ! A VOIR UNE FOIS UN PREMIER EMBEDDING REALISE !

index = None


docs = []

to_add = [f for f in paths if os.path.basename(f) not in to_keep]
for path in to_add:
    print(f"\nEmbedding du document : {path} -----------------------")
    # Sélectionnez le chargeur de documents approprié
    if path.endswith(".pdf"):
        loader = PyPDFLoader(path)
    elif path.endswith(".docx"):
        loader = Docx2txtLoader(path)
    elif path.endswith(".xlsx"):
        loader = UnstructuredExcelLoader(path, mode='elements')
    else:
        loader = UnstructuredFileLoader(path)

    # Chargez les documents et divisez-les en morceaux
    chunks = loader.load_and_split(text_splitter=text_splitter)
    counter, counter2 = collections.Counter(), collections.Counter()
    filename = os.path.basename(path)

    # Définir un identifiant unique pour chaque morceau
    if "page" in chunks[0].metadata:
        for chunk in chunks:
            counter[chunk.metadata['page']] += 1
        for i in range(len(chunks)):
            counter2[chunks[i].metadata['page']] += 1
            chunks[i].metadata['source'] = f"{filename}, page {chunks[i].metadata['page'] + 1}"
            if counter[chunks[i].metadata['page']] > 1:
                chunks[i].metadata['source'] += f" ({counter2[chunks[i].metadata['page']]}"
                chunks[i].metadata['source'] += f"/{counter[chunks[i].metadata['page']]})"
    else:
        if len(chunks) == 1:
            chunks[0].metadata['source'] = filename
        else:
            for i in range(len(chunks)):
                chunks[i].metadata['source'] = f"{filename} ({i+1}/{len(chunks)})"
        docs += chunks

# les messages dans la console
# logging.info(f"{len(docs)} vectors added")

if len(docs) > 0:
    if index is not None:
        # Calculez l'intégration de chaque morceau et indexez ces morceaux
        new_index = FAISS.from_documents(docs, embeddings)
        index.merge_from(new_index)
    else:
        index = FAISS.from_documents(docs, embeddings)

# logging.info(f"{len(index.docstore._dict)} vectors in the index")

index.save_local("./output/faiss_index")             