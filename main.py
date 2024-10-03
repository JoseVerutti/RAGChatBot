import json
from config.chatgpt import getChatGPTEmbeddings, client
from config.pinecone import conectPineconeIndex
from config.sharepoint import get_sharepoint_context_using_app

from services.chunks import getChunks, getChunksSingleFile
from services.pinecone import searchDB, updateDB, getAllDocuments, searchDBFilter
from services.sharepoint import get_files, post_files
from services.chatgpt import get_answer



embeddings = getChatGPTEmbeddings()

db = conectPineconeIndex(embeddings, "rag-gianpi-texts")

ctx = get_sharepoint_context_using_app()

url = "sites/Python_SOS_Doctorado/Documentos%20compartidos"

def actualizarDB(filename):

    chunks = getChunks(filename)

    response = updateDB(db,chunks)

    return response

def uploadDocDB(file):

    chunks = getChunksSingleFile(file)

    response = updateDB(db,chunks)

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