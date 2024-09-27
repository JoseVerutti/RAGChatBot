import requests
import os
import pandas as pd

# Asegúrate de que esta ruta sea correcta
archivo_excel = "Doi.xlsx"

# Verifica si el archivo existe
if not os.path.exists(archivo_excel):
    print(f"El archivo {archivo_excel} no se encuentra en la ubicación actual.")
    print(f"Directorio actual: {os.getcwd()}")
    exit()

df = pd.read_excel(archivo_excel)
dois = df.iloc[:, 0].tolist()

carpeta_destino = "pdfs"

if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

api_key = "1018610e50e34eff05c27ec8b65a65df"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "X-ELS-APIKey": api_key,
    "Accept": "application/pdf"
}

for doi_url in dois:
    doi = doi_url.split('/')[-2] + '/' + doi_url.split('/')[-1]
    
    url = f"https://api.elsevier.com/content/article/doi/{doi}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        nombre_archivo = f"{doi.replace('/', '_')}.pdf"
        ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)
        
        with open(ruta_archivo, "wb") as file:
            file.write(response.content)
        
        print(f"PDF descargado: {nombre_archivo}")
    else:
        print(f"Error al descargar el PDF para el DOI: {doi}")
        print(f"Código de estado: {response.status_code}")
        print(f"Mensaje de error: {response.text}") 