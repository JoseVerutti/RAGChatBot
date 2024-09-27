import os
import time
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

def conectPineconeIndex(embeddings, index_name: str, cloud: str = "aws", region: str = "us-east-1", metric: str = "cosine"):
    try:
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("La API key de Pinecone no está configurada en las variables de entorno.")

        pc = Pinecone(api_key=api_key)

        try:
            existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
        except Exception as e:
            raise ConnectionError(f"No se pudo obtener la lista de índices: {str(e)}")

        if index_name not in existing_indexes:
            try:
                pc.create_index(
                    name=index_name,
                    dimension=3072,
                    metric=metric,
                    spec=ServerlessSpec(cloud=cloud, region=region),
                )
                while not pc.describe_index(index_name).status["ready"]:
                    print("Esperando que el índice esté listo...")
                    time.sleep(1)
            except Exception as e:
                raise RuntimeError(f"Error al crear el índice: {str(e)}")
        else:
            print(f"El índice {index_name} ya existe")

        try:
            index = pc.Index(index_name)
        except Exception as e:
            raise ConnectionError(f"No se pudo conectar al índice: {str(e)}")

        try:
            vector_store = PineconeVectorStore(index=index, embedding=embeddings)
        except Exception as e:
            raise RuntimeError(f"Error al crear PineconeVectorStore: {str(e)}")

        return vector_store

    except ValueError as ve:
        print(f"Error de configuración: {ve}")
        raise
    except ConnectionError as ce:
        print(f"Error de conexión: {ce}")
        raise
    except RuntimeError as re:
        print(f"Error de ejecución: {re}")
        raise
    except Exception as e:
        print(f"Error inesperado: {e}")
        raise