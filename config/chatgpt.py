import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

def getChatGPTEmbeddings(GPTmodel="text-embedding-3-large"):
    try:
        
        if not api_key:
            raise ValueError("La API key de OpenAI no está configurada en las variables de entorno.")
        
        embeddings = OpenAIEmbeddings(model=GPTmodel, openai_api_key=api_key)
        return embeddings
    
    except ValueError as ve:
        print(f"Error de configuración: {ve}")
        raise
    except Exception as e:
        print(f"Error inesperado al obtener embeddings: {e}")
        raise





