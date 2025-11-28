import streamlit as st
from engine.tagger import tag_files
import custom_exceptions
from typing import Literal
import pandas as pd
import logging

def file_uploader(msg: str) -> list:

    uploaded_files = st.file_uploader(
        msg, 
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Soporta archivos Excel y CSV"
    )

    return uploaded_files

def tag_button(uploaded_files, mode: Literal['general','ibecosol','personalized']) -> pd.DataFrame:

    if st.button("Etiquetar", type="primary"):

        if not uploaded_files:
            st.warning("⚠️ Por favor, sube al menos un archivo para continuar.")
            return
        if mode == 'personalized' and (not uploaded_files[0] or not uploaded_files[1]):
            st.warning("⚠️ Por favor, sube al menos un archivo de entrenamiento y otro de predicción para continuar.")
            return

        else:
            with st.spinner("Procesando archivos..."):
                try: 
                    df_result = tag_files(uploaded_files, mode)
                    
                    st.success("✅ ¡Etiquetado completado con éxito!")
                    st.dataframe(df_result, use_container_width=True)
                    
                    return df_result
                
                except custom_exceptions.FileProcessingError:
                    st.error(f"¡Error al procesar los archivos!")

                except custom_exceptions.SchemaValidationError:
                    st.error(f"¡Error al validar el esquema!")
                
                except custom_exceptions.DateConversionError:
                    st.error(f"¡Error al convertir la fecha. Formato no válido!")

                except custom_exceptions.ModelDownloadError:
                    st.error(f"¡Error al descargar el modelo!")

                except Exception as e:
                    logging.error(f"Error no identificado: {e}")
                    st.error(f"¡Error no identificado!")

def home_button():
    if st.button("⬅️ Volver al Inicio"):
        st.session_state['current_view'] = 'home'
        st.rerun()

    
