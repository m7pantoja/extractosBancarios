from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st
import joblib
import os
import logging
from typing import Literal
import custom_exceptions

bucket_name = 'extractosbancarios-cloud-lf'
blob_names = {'general':'models/general/general_v1.joblib',
              'ibecosol':'models/ibecosol/ibecosol_v1.joblib',
              'erretres':'models/erretres/erretres_v1.joblib'}

@st.cache_resource
def download_model_from_gcs(model_name: Literal['general', 'ibecosol','erretres']) -> dict:
    try:

        # Autenticación
        info = st.secrets["gcp_service_account"]
        credentials = service_account.Credentials.from_service_account_info(info)
        
        # Conexión
        client = storage.Client(credentials=credentials, project=info["project_id"])
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_names[model_name])
        
        # Descarga
        temp_name = "temp_model.joblib"
        blob.download_to_filename(temp_name)
        
        # Carga
        model_dict = joblib.load(temp_name)
            
        # Limpieza
        if os.path.exists(temp_name):
            os.remove(temp_name)
        
        return model_dict  

    except Exception as e:
        logging.error(f"Error al descargar el modelo de GCS: {e}")
        raise custom_exceptions.ModelDownloadError(f"Error al descargar el modelo.")
        return None