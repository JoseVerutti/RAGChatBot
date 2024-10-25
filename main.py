import json
from config.chatgpt import getChatGPTEmbeddings, client
from config.pinecone import conectPineconeIndex

from services.chunks import getChunks, getChunksSingleFile
from services.pinecone import searchDB, updateDB, getAllDocuments, searchDBFilter
from services.chatgpt import get_answer



embeddings = getChatGPTEmbeddings()

db = conectPineconeIndex(embeddings, "rag-liz-texts")

def actualizarDB(filename):

    chunks = getChunks(filename)

    response = updateDB(db,chunks)

    return response


import os
import shutil
from datetime import datetime

def uploadDocDB(file):
    # Definir la carpeta de destino
    carpeta_destino = "pdfs"

    # Asegurarnos de que la carpeta existe, si no la creamos
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # Obtener el nombre del archivo y el path
    nombre_archivo = os.path.basename(file)  # Solo el nombre del archivo sin el path
    archivo_destino = os.path.join(carpeta_destino, nombre_archivo)

    # Verificar si ya existe un archivo con el mismo nombre y renombrarlo si es necesario
    if os.path.exists(archivo_destino):
        # Si el archivo ya existe, agregar un sufijo para evitar sobrescribirlo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo, ext = os.path.splitext(nombre_archivo)
        archivo_destino = os.path.join(carpeta_destino, f"{nombre_archivo}_{timestamp}{ext}")

    # Copiar el archivo a la carpeta destino
    shutil.copy(file, archivo_destino)

    # Ahora, procesamos el archivo como se hacía originalmente
    chunks = getChunksSingleFile(archivo_destino)

    # Supongo que updateDB es una función que actualiza la base de datos con los "chunks" del archivo
    response = updateDB(db, chunks)

    return response


def respuestaCompleta(userPrompt , context):

    answer = get_answer(userPrompt, context, client)

    return answer

def getContext(input, k ):

    response = searchDB(db, input, k = k)

    formatted_documents = []

    for doc in response:

        formatted_doc = {
                            'metadata': {
                                'nombre_archivo': doc.metadata['Nombre del archivo'],
                                'pagina': doc.metadata['Pagina']
                            },
                            'content': doc.page_content
                        }
        formatted_documents.append(formatted_doc)

    return formatted_documents

def getContextFilter(lstDocs, input, k ):

    response = searchDBFilter(lstDocs,db, input, k = k)

    formatted_documents = []

    for doc in response:

        formatted_doc = {
                            'metadata': {
                                'nombre_archivo': doc.metadata['Nombre del archivo'],
                                'pagina': doc.metadata['Pagina']
                            },
                            'content': doc.page_content
                        }
        formatted_documents.append(formatted_doc)

    return formatted_documents

def getAllDB():

    response = getAllDocuments(db)

    formatted_documents = []

    for doc in response:

        formatted_doc = {
                            'metadata': {
                                'nombre_archivo': doc['Nombre del archivo'],
                                'pagina': doc['Pagina']
                            },
                            'content': doc['text']
                        }
        formatted_documents.append(formatted_doc)

    return formatted_documents

def añadirHist(user, sistem):
    archivo_historial = 'historial_chat.json'
    try:
        with open(archivo_historial, 'r') as file:
            historial = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        historial = []

    historial.append({'User': user, 'Sistem': sistem})

    with open(archivo_historial, 'w') as file:
        json.dump(historial, file, indent=4)

    return 'Entrada añadida al historial.'


def obtenerHist():
    archivo_historial = 'historial_chat.json'
    try:
        with open(archivo_historial, 'r') as file:
            historial = json.load(file)
            return historial
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []