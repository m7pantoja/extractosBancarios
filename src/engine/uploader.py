from .engine_utils import schema_validation, generate_hash
from src.database.upload import upload_data_to_bigquery
from src.database.upload import upload_feedback_to_bigquery
import pandas as pd

def upload_review(df, mode):
    """
    Sube el DataFrame a BigQuery previamente procesado.
    
    Args:
        df: DataFrame original tras la edición por parte del empleado.
    """

    # FORMATEO DE LOS DATOS (ERRORES CONTROLADOS)

    data = df.copy()
    
    data_validated = schema_validation(data, 'train')
    data_validated['fecha'] = data_validated['fecha'].dt.date

    data_validated['id_hash'] = data_validated.apply(generate_hash, axis=1)
    data_validated['trained'] = False
    
    cols_ordered = ['fecha', 'descripcion', 'importe', 'saldo', 'etiqueta', 'trained', 'id_hash']
    
    data_upload = data_validated[cols_ordered]

    # SUBIDA A BIGQUERY (ERRORES CONTROLADOS)

    upload_data_to_bigquery(data_upload, mode)

def upload_feedback(comment: str):
    """
    Sube un comentario de feedback a la tabla 'feedback' en BigQuery.
    
    Args:
        comment: El texto del comentario.
    """

    df_feedback = pd.DataFrame([{
        'comentario': comment,
        'fecha': pd.Timestamp.now()
    }])

    upload_feedback_to_bigquery(df_feedback)