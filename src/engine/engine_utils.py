import pandera.pandas as pa
from pandera import Column, DataFrameSchema
import pandas as pd
import hashlib
from typing import Literal
import custom_exceptions
import logging

def schema_validation(df: pd.DataFrame, mode: Literal['train','predict']) -> pd.DataFrame:
    '''
    Validates the DataFrame against the required structure and data types.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to validate.
    mode (Literal['train','predict']): The mode of validation.

    With mode='train', the 'etiqueta' column is expected. With mode='predict', it is not.
    
    Returns:
    pd.DataFrame: The validated DataFrame with additional column '__fecha__' for internal use.
    '''

    columns = {
        "fecha": Column(pa.String), 
        "descripcion": Column(pa.String),
        "importe": Column(pa.Float),
        "saldo": Column(pa.Float)
    }

    if mode == 'train':
        columns['etiqueta'] = Column(pa.Category, coerce=True)

    schema = DataFrameSchema(columns)

    try:
        df_validado = schema.validate(df)
    except pa.errors.SchemaError as e:
        logging.error(f"Error al validar esquema: {e}")
        raise custom_exceptions.SchemaValidationError(f"Error al validar esquema.")
        return None

    try:
        df_validado['__fecha__'] = pd.to_datetime(df_validado['fecha'], format='mixed')
        return df_validado
    except ValueError as e:
        logging.error(f"Error al convertir la fecha: {e}")
        raise custom_exceptions.DateConversionError(f"Error al convertir la fecha.")
        return None

def files_to_dataframe(uploaded_files: list) -> pd.DataFrame: 
    """
    Transforma los archivos de una lista de UploadedFile en un único DataFrame.

    Args:
        uploaded_files: La lista de archivos de tipo UploadedFile.
    Returns:
        Un DataFrame de pandas con los datos de los archivos.
    """

    dfs = list()
    try:
        for file in uploaded_files:

            # 1. XLSX y XLS
            if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                dfs.append(pd.read_excel(file))

            # 2. CSV
            elif file.name.endswith('.csv'):
                dfs.append(pd.read_csv(file))
            
        data = pd.concat(dfs)
    except Exception as e:
        logging.error(f"Error al procesar archivos: {e}")
        raise custom_exceptions.FileProcessingError(f"Error al procesar archivos.")

    return data

def generate_hash(row):
    # ESTANDARIZACIÓN
    # Formateamos floats a 2 decimales fijos y fechas a string ISO
    fecha_str = row['fecha'].strftime('%Y-%m-%d')
    desc_str = str(row['descripcion']).strip() # Quitamos espacios extra
    importe_str = "{:.2f}".format(row['importe']) 
    saldo_str = "{:.2f}".format(row['saldo'])
    
    # CONCATENACIÓN
    # Usamos '|' para evitar mezclas accidentales de columnas
    raw_string = f"{fecha_str}|{desc_str}|{importe_str}|{saldo_str}"
    
    # HASHING (SHA256)
    return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()

