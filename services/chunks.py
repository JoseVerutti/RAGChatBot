import json
import PyPDF2
from dotenv import load_dotenv
from langchain_core.documents import Document
import os

def getChunks(filename: str):
    load_dotenv()

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    chunks = [  #Evaluar sets y tiempo de ejecución
        Document(
            page_content=item["Texto de la pagina"],
            metadata={
                "Indice": item["Indice"],
                "Nombre del archivo": item["Nombre del archivo"],
                "Pagina" : item["Pagina"]
            }
        ) for item in data
    ]
    return chunks

def getChunksSingleFile(archivo):

    lista_json = []

    if archivo.endswith(".pdf"):

        with open(archivo, 'rb') as f:

            lector_pdf = PyPDF2.PdfReader(f)
            for num_pagina, pagina in enumerate(lector_pdf.pages, start=1):
                texto_pagina = pagina.extract_text().strip()
                if texto_pagina:
                    lista_json.append({
                        "Nombre del archivo": os.path.basename(archivo),
                        "Pagina": num_pagina,
                        "Texto de la pagina": texto_pagina
                    })

    chunks = [  #Evaluar sets y tiempo de ejecución
        Document(
            page_content=item["Texto de la pagina"],
            metadata={
                "Nombre del archivo": item["Nombre del archivo"],
                "Pagina" : item["Pagina"]
            }
        ) for item in lista_json ]
    
    return chunks
