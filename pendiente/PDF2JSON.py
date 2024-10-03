import json
import os
import PyPDF2

def leer_archivos_pdf(carpeta):
    lista_json = []
    indice_global = 1
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".pdf"):
            ruta_completa = os.path.join(carpeta, archivo)
            with open(ruta_completa, 'rb') as f:
                lector_pdf = PyPDF2.PdfReader(f)
                for num_pagina, pagina in enumerate(lector_pdf.pages, start=1):
                    texto_pagina = pagina.extract_text().strip()
                    if texto_pagina:
                        lista_json.append({
                            "Nombre del archivo": archivo,
                            "Pagina": num_pagina,
                            "Texto de la pagina": texto_pagina
                        })
                        indice_global += 1
    return lista_json

def guardar_json(lista_json, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(lista_json, archivo, ensure_ascii=False, indent=2)

# Ejemplo de uso
carpeta_archivos = "pdfs"
archivo_salida = "salida.json"

lista_json = leer_archivos_pdf(carpeta_archivos)
guardar_json(lista_json, archivo_salida)