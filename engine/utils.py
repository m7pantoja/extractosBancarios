import pandera as pa
from pandera import Column, DataFrameSchema
import pandas as pd
import hashlib
from typing import Literal

def schema_validation(df: pd.DataFrame, mode: Literal['train','predict']) -> pd.DataFrame:
    '''
    Validates the DataFrame against the required structure and data types.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to validate.
    mode (Literal['train','predict']): The mode of validation.

    With mode='train', the 'etiqueta' column is expected. With mode='predict', it is not.
    
    Returns:
    pd.DataFrame: The validated DataFrame.
    '''

    columns = {
        "fecha": Column(pa.DateTime), 
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
        print(f"Error: {e}")

    return df_validado

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

