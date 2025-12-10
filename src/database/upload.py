from google.oauth2 import service_account
from google.cloud import bigquery
import streamlit as st
import logging
import custom_exceptions
from typing import Literal

table_ids = {'general':'cloud-lf.extractosBancarios.general_tagged',
             'ibecosol':'cloud-lf.extractosBancarios.ibecosol_tagged'}

def upload_data_to_bigquery(df, mode: Literal['general', 'ibecosol']):
    """
    Sube un DataFrame a BigQuery.
    
    Args:
        df: DataFrame a subir.
        mode: Modo de la aplicación ('general' o 'ibecosol') para determinar la tabla destino.
    """
    try:

        # Autenticación
        info = st.secrets["gcp_service_account"]
        credentials = service_account.Credentials.from_service_account_info(info)
        
        # Conexión
        client = bigquery.Client(credentials=credentials, project=info["project_id"])
        table_id = table_ids[mode]

        # Configuración del trabajo de carga
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        
        job.result() 
        
        logging.info(f"Cargadas {job.output_rows} filas en {table_id}.")

    except Exception as e:
        logging.error(f"Error al subir datos a BigQuery: {e}")
        raise custom_exceptions.DataUploadError(f"Error al subir datos a BigQuery: {str(e)}")
