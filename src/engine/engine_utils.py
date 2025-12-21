import pandera.pandas as pa
from pandera import Column, DataFrameSchema
import pandas as pd
import numpy as np
import hashlib
from typing import Literal
import custom_exceptions
import logging
from .cleaner_agent import get_mapping_instructions, BankStatementSchema

def schema_validation(df: pd.DataFrame, mode: Literal['train','predict']) -> pd.DataFrame:
    '''
    Validates the DataFrame against the required structure and data types.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to validate.
    mode (Literal['train','predict']): The mode of validation.

    With mode='train', the 'etiqueta' column is expected. With mode='predict', it is not.
    
    Returns:
    pd.DataFrame
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
        return df_validado
    except pa.errors.SchemaError as e:
        logging.error(f"Error al validar esquema: {e}")
        raise custom_exceptions.SchemaValidationError(f"Error al validar esquema.")
        return None


def clean_file(file, file_type: Literal['excel','csv'], schema: BankStatementSchema) -> pd.DataFrame:
    
    if not schema.is_valid:
        reason = schema.validation_reason if schema.validation_reason else "El formato del archivo no es válido para el modelo predictor."
        raise custom_exceptions.InvalidFileError(f"Archivo inválido: {reason}")
    
    try:
        file.seek(0) # Reiniciar puntero del archivo por si fue leído anteriormente
        
        header_row_index = schema.header_row_index

        if file_type == 'excel':
            df = pd.read_excel(file, header=header_row_index)
        if file_type == 'csv':
            df = pd.read_csv(file, header=header_row_index)
            
        # Mapeo de columnas
        cols_map = {
            schema.fecha_col_name: 'fecha',
            schema.desc_col_name: 'descripcion',
            schema.importe_col_name: 'importe',
            schema.saldo_col_name: 'saldo'
        }

        # Renombrar
        df_renamed = df.rename(columns=cols_map)
        
        # --- Limpieza de Tipos ---
        
        # 1. Fecha
        df_renamed['fecha'] = pd.to_datetime(df_renamed['fecha'], format=schema.date_format)
        
        # 2. Importe y Saldo
        def clean_decimal(val):

            if pd.isna(val) or val == '':
                return np.nan

            s = str(val).strip()

            if not s: 
                return np.nan
                
            # Si el separador decimal es coma
            if schema.decimal_separator == ',':
                # Eliminar puntos de miles, cambiar coma decimal por punto
                s = s.replace('.', '').replace(',', '.')
            else:
                # Si es punto, solo eliminamos comas de miles
                s = s.replace(',', '')
                
            try:
                return float(s)
            except ValueError:
                return np.nan

        df_renamed['importe'] = df_renamed['importe'].apply(clean_decimal)
        df_renamed['saldo'] = df_renamed['saldo'].apply(clean_decimal)


        df_clean = df_renamed.dropna(subset=['fecha','descripcion','importe','saldo'])
        
        return df_clean

    except Exception as e:
        logging.error(f"Error limpiando archivo: {e}")
        raise custom_exceptions.CleaningFileError("Error limpiando archivo")


def files_to_dataframe(uploaded_files: list) -> pd.DataFrame: 
    """
    Transforma los archivos de una lista de UploadedFile en un único DataFrame, limpiando los datos
    con el Agente de IA.

    Args:
        uploaded_files: La lista de archivos de tipo UploadedFile.
    Returns:
        Un DataFrame de pandas con los datos de los archivos.
    """

    dfs = list()
    NSamples = 20

    for file in uploaded_files:

        # 1. XLSX y XLSs
        if file.name.endswith('.xlsx') or file.name.endswith('.xls'):

            try:
                sample_data = pd.read_excel(file,nrows=NSamples)
            except Exception as e:
                logging.error(f"Error al leer el archivo {file.name}: {e}")
                raise custom_exceptions.FileProcessingError(f"Error al procesar el archivo {file.name}")

            mapping_instructions = get_mapping_instructions(sample_data)
            clean_data = clean_file(file,'excel',mapping_instructions)
            dfs.append(clean_data)

        # 2. CSV
        elif file.name.endswith('.csv'):

            try:
                sample_data = pd.read_csv(file,nrows=NSamples)
            except Exception as e:
                logging.error(f"Error al leer el archivo {file.name}: {e}")
                raise custom_exceptions.FileProcessingError(f"Error al procesar el archivo {file.name}")

            mapping_instructions = get_mapping_instructions(sample_data)
            clean_data = clean_file(file,'csv',mapping_instructions)
            dfs.append(clean_data)
    try:     
        data = pd.concat(dfs)
    except Exception as e:
        logging.error(f"Error al concatenar los archivos: {e}")
        raise custom_exceptions.FileStructureError("Los archivos no tienen la misma estructura")

    return data

def generate_hash(row):
    try:
        
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

    except Exception as e:
        logging.error(f"Error al generar hash: {e}")
        raise custom_exceptions.HashGenerationError(f"Error al generar hash.")
