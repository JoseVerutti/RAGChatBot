import os
from dotenv import load_dotenv
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext

load_dotenv()

def get_sharepoint_context_using_app():
    try:
        secret = os.getenv("SECRET_SHAREPOINT")
        app_id = os.getenv("APP_ID")
        sharepoint_url = 'https://ongecohabitats.sharepoint.com'

        if not secret or not app_id:
            raise ValueError("Las credenciales de SharePoint (SECRET_SHAREPOINT o APP_ID) no están configuradas en las variables de entorno.")

        client_credentials = ClientCredential(app_id, secret)

        ctx = ClientContext(sharepoint_url).with_credentials(client_credentials)

        return ctx

    except ValueError as ve:
        print(f"Error de configuración: {ve}")
        raise
    except ConnectionError as ce:
        print(f"Error de conexión: {ce}")
        raise
    except Exception as e:
        print(f"Error inesperado al obtener el contexto de SharePoint: {e}")
        raise