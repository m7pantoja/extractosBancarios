from .engine_utils import schema_validation, generate_hash
from database.upload import upload_data_to_bigquery

def upload_review(df, mode):
    """
    Sube el DataFrame a BigQuery previamente procesado.
    
    Args:
        df: DataFrame original tras la edición por parte del empleado.
    """

    # FORMATEO DE LOS DATOS (ERRORES CONTROLADOS)

    data = df.copy()
    
    data_validated = schema_validation(data, 'train')
    data_validated['fecha'] = data_validated['__fecha__'].dt.date

    data_validated['id_hash'] = data_validated.apply(generate_hash, axis=1)
    data_validated['trained'] = False
    
    cols_ordered = ['fecha', 'descripcion', 'importe', 'saldo', 'etiqueta', 'trained', 'id_hash']
    
    data_upload = data_validated[cols_ordered]

    # SUBIDA A BIGQUERY (ERRORES CONTROLADOS)

    upload_data_to_bigquery(data_upload, mode)

