import json
from dotenv import load_dotenv
from langchain_core.documents import Document

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
