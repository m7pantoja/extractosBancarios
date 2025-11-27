import streamlit as st
from engine import tag_files
import custom_exceptions
from typing import Literal
import pandas as pd

def file_uploader() -> list:

    uploaded_files = st.file_uploader(
        "Arrastra los archivos que quieres etiquetar o haz clic para buscar", 
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Soporta archivos Excel y CSV"
    )

    return uploaded_files

def tag_button(uploaded_files, model_name: Literal['general', 'ibecosol']) -> pd.DataFrame:
    if st.button("Etiquetar", type="primary"):
        if not uploaded_files:
            st.warning("⚠️ Por favor, sube al menos un archivo para continuar.")
        else:
            with st.spinner("Procesando archivos..."):
                try: 
                    df_result = tag_files(uploaded_files, model_name)
                    
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
                    st.error(f"¡Error no identificado!")


