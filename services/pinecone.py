from uuid import uuid4
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def updateDB(db, chunks):
    try:
        if not db:
            raise ValueError("La base de datos no está inicializada o conectada.")

        if not chunks or not isinstance(chunks, list):
            raise ValueError("Se requiere una lista de 'chunks' no vacía.")

        uuids = [str(uuid4()) for _ in range(len(chunks))]
        response = db.add_documents(documents=chunks, ids=uuids)

        logging.info(f"Se agregaron {len(chunks)} documentos a la base de datos.")
        return response

    except ValueError as ve:
        logging.error(f"Error de validación en updateDB: {ve}")
        raise
    except Exception as e:
        logging.error(f"Error inesperado al actualizar la base de datos: {e}")
        raise

def searchDB(db, prompt: str, k=2):
    try:
        if not db:
            raise ValueError("La base de datos no está inicializada o conectada.")

        if not prompt:
            raise ValueError("El 'prompt' no puede estar vacío.")

        results = db.similarity_search(prompt, k=k)

        if not results:
            logging.warning(f"No se encontraron resultados para el prompt: {prompt}")
        else:
            logging.info(f"Se encontraron {len(results)} resultados para el prompt.")

        return results

    except ValueError as ve:
        logging.error(f"Error de validación en searchDB: {ve}")
        raise
    except Exception as e:
        logging.error(f"Error inesperado al buscar en la base de datos: {e}")
        raise


def getAllDocuments(db):
    try:
        if not db:
            raise ValueError("La base de datos no está inicializada o conectada.")

        # Obtener la dimensión del índice
        index_stats = db._index.describe_index_stats()
        index_dimension = index_stats['dimension']
        vector_count = index_stats['total_vector_count']

        # Crear un vector de consulta con la dimensión correcta
        query_vector = [0] * index_dimension

        results = db._index.query(
            vector=query_vector,
            top_k=vector_count,
            include_metadata=True
        )

        # Extraer los documentos de los resultados
        documents = [match['metadata'] for match in results['matches']]

        logging.info(f"Se recuperaron {len(documents)} documentos de la base de datos.")
        return documents

    except ValueError as ve:
        logging.error(f"Error de validación al obtener documentos: {ve}")
        raise
    except Exception as e:
        logging.error(f"Error inesperado al obtener documentos: {e}")
        raise