import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage
import joblib
import os
import engine.model as model

@st.cache_resource
def load_model_from_gcs(bucket_name, blob_name) -> model.Model:
    try:
        deployed_model = None
        
        # Autenticación
        info = st.secrets["gcp_service_account"]
        credentials = service_account.Credentials.from_service_account_info(info)
        
        # Conexión
        client = storage.Client(credentials=credentials, project=info["project_id"])
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        # Descarga
        temp_name = "temp_model.joblib"
        blob.download_to_filename(temp_name)
        
        # Carga
        model_dict = joblib.load(temp_name)
            
        # Limpieza
        if os.path.exists(temp_name):
            os.remove(temp_name)
        
        # Instanciación
        deployed_model = model.Model.from_dict(model_dict)
        
        return deployed_model

    except Exception as e:
        st.error(f"Error crítico conectando con GCS: {e}")
        return None