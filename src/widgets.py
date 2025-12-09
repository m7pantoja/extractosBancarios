import streamlit as st
from engine.tagger import tag_files
import custom_exceptions
from typing import Literal
import pandas as pd
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import logging

def file_uploader(msg: str) -> list:

    uploaded_files = st.file_uploader(
        msg, 
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Soporta archivos Excel y CSV"
    )

    return uploaded_files

def show_data(result, mode: Literal['general','ibecosol','personalized']):

    cmap = cm.get_cmap('RdYlGn') # Selección del mapa de calor

    def color_row(row):
        val = row['confidence']
        rgba = cmap(val) # Obtenemos el color RGBA para este valor exacto (0.0 a 1.0)
        
        soft_color = mcolors.to_rgba(rgba, alpha=0.3)
        css_color = mcolors.to_hex(soft_color, keep_alpha=True)
        
        return [f'background-color: {css_color}'] * len(row) # Devolvemos el string CSS para pintar TODA la fila

    if mode == 'personalized':
        st.dataframe(result[0], use_container_width=True)
    else:
        df = result[0]
        df['confidence'] = result[1]

        styler = df.style.apply(color_row, axis=1)
        st.dataframe(styler, use_container_width=True,column_config={'confidence': None})


def tag_button(uploaded_files, mode: Literal['general','ibecosol','personalized']):

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
                    result = tag_files(uploaded_files, mode)
                    
                    st.success("✅ ¡Etiquetado completado con éxito!")
                    show_data(result,mode)

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

    
