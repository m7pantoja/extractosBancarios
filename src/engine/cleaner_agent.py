from pydantic import BaseModel, Field
from typing import Optional
from google import genai
from google.genai import types
import streamlit as st
import logging
import custom_exceptions
import pandas as pd

class BankStatementSchema(BaseModel):
    header_row_index: int = Field(description="El índice de la fila (0-based) donde se encuentran los nombres de las columnas reales. Ignora títulos o metadatos superiores.")
    fecha_col_name: str = Field(description="El nombre exacto de la columna en el archivo original que actúa como FECHA.")
    desc_col_name: str = Field(description="El nombre exacto de la columna en el archivo original que actúa como DESCRIPCIÓN/CONCEPTO.")
    importe_col_name: str = Field(description="El nombre exacto de la columna en el archivo original que actúa como IMPORTE.")
    saldo_col_name: str = Field(description="El nombre exacto de la columna de SALDO, si existe.")
    date_format: str = Field(description="Formato de fecha Python detectado (ej: %d/%m/%Y).")
    decimal_separator: str = Field(description="Separador decimal detectado ('.' o ',').")
    thousand_separator: Optional[str] = Field(description="El separador de miles ('.', ',' o null).")
    currency_symbol: Optional[str] = Field(description="Símbolo de moneda o texto extra que acompaña al número (ej: '€', '$', 'EUR').")
    is_valid: bool = Field(description="True si parece un extracto bancario válido.")
    validation_reason: Optional[str] = Field(description="Si is_valid es False, explica brevemente por qué. Si es True, dejar vacío.")


def get_mapping_instructions(df_sample: pd.DataFrame) -> BankStatementSchema:
    try:
        client = genai.Client(api_key=st.secrets["google_ai"]["api_key"])
        csv_text = df_sample.to_csv(index=False)
        
        prompt = f"""
        Analiza este fragmento de archivo (CSV) que puede contener metadatos al principio.
        
        DATOS:
        ---
        {csv_text}
        ---
        
        1. Identifica header_row_index y los nombres originales de las columnas Fecha, Descripción, Importe y Saldo.
        2. Analiza las columnas numéricas (Importe/Saldo) minuciosamente para detectar el formato numérico:
           - ¿Qué caracter separa los decimales? (decimal_separator)
           - ¿Se usa algún caracter para separar los miles? (thousand_separator)
           - ¿Hay símbolos de moneda ($, €, £) o códigos (EUR, USD) dentro de la celda? (currency_symbol)
        3. Detecta el formato de fecha (date_format).
        4. Confirma si es un extracto bancario válido (is_valid). Si no es válido, explica brevemente por qué (validation_reason).

        IMPORTANTE: Los nombres de las columnas deben coincidir exactamente con los que aparecen en la fila identificada como header.
        """

        models_to_try = ["gemini-3-flash","gemini-2.5-flash", "gemini-2.5-flash-lite"]

        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name, 
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=BankStatementSchema,
                    ),
                )
                return response.parsed
            except Exception as e:
                error_msg = str(e).lower()
                if "429" in error_msg or "resource has been exhausted" in error_msg:
                    logging.warning(f"Límite excedido para el modelo {model_name}. Probando el siguiente...")
                    continue
                elif "503" in error_msg or "overloaded" in error_msg:
                    logging.warning(f"Modelo {model_name} sobrecargado (503). Probando el siguiente...")
                    continue
                elif "404" in error_msg or "not found" in error_msg:
                    logging.warning(f"Modelo {model_name} no encontrado. Probando el siguiente...")
                    continue
                else:
                    logging.error(f"Error usando el Agente de IA: {e}")
                    raise custom_exceptions.IAAgentError("¡Error usando el Agente de IA!")

        # Si el loop termina sin retornar, es que todos los modelos dieron error de cuota
        raise custom_exceptions.quotaExceededError("Se ha excedido el límite de uso en todos los modelos de IA disponibles. Por favor intentalo de nuevo más tarde.")

    except (custom_exceptions.quotaExceededError, custom_exceptions.IAAgentError):
        raise
    except Exception as e:
        logging.error(f"Error usando el Agente de IA: {e}")
        raise custom_exceptions.IAAgentError("¡Error usando el Agente de IA!")