import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage
import joblib
import os

@st.cache_resource
def load_model_from_gcs(bucket_name, blob_name):
    try:
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
        model = joblib.load(temp_name)
            
        # Limpieza
        if os.path.exists(temp_name):
            os.remove(temp_name)
        
        return model

    except Exception as e:
        st.error(f"Error crítico conectando con GCS: {e}")
        return None