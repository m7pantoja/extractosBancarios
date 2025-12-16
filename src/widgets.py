import streamlit as st
from engine.tagger import tag_files
from engine.uploader import upload_review
import custom_exceptions
from typing import Literal
import pandas as pd
import logging
import time

# FUNCIONES AUXILIARES ----------

def clean_memory():
    st.session_state.pop("editor_memory", None)
    st.session_state.pop("data_memory", None)
    st.session_state.pop("classes_memory", None)

# WIDGETS -----------------------

def file_uploader(msg: str) -> list:

    uploaded_files = st.file_uploader(
        msg, 
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Soporta archivos Excel y CSV"
    )

    return uploaded_files

def show_data(df, label_encoder):

    DATA_KEY = "data_memory"
    CLASSES_KEY = "classes_memory"
    EDITOR_KEY = "editor_memory"

    if (df is None) and (DATA_KEY not in st.session_state):
        return
    
    if df is not None:
        st.session_state[DATA_KEY] = df.copy()

    if label_encoder is not None:
        st.session_state[CLASSES_KEY] = list(label_encoder.classes_)
    
    df_edited = st.data_editor(st.session_state[DATA_KEY],
                key=EDITOR_KEY,
                use_container_width=True,
                column_config={"confidence": st.column_config.ProgressColumn("Nivel de Confianza",
                                                                            format="%.2f",
                                                                            min_value=0,
                                                                            max_value=1),
                               "etiqueta": st.column_config.SelectboxColumn("Etiqueta",
                                                                            options=st.session_state[CLASSES_KEY],
                                                                            required=True),
                               "fecha": st.column_config.DateColumn("Fecha"),
                               "descripcion": st.column_config.TextColumn("Descripción"),
                               "importe": st.column_config.NumberColumn("Importe"),
                               "saldo": st.column_config.NumberColumn("Saldo")})

    return df_edited

def tag_button(uploaded_files, mode: Literal['general','ibecosol','personalized']):

    if st.button("Etiquetar", type="primary",on_click=clean_memory):

        if not uploaded_files:
            st.warning("⚠️ Por favor, sube al menos un archivo para continuar.")
            return None, None
        if mode == 'personalized' and (not uploaded_files[0] or not uploaded_files[1]):
            st.warning("⚠️ Por favor, sube al menos un archivo de entrenamiento y otro de predicción para continuar.")
            return None, None

        else:
            with st.spinner("Procesando archivos..."):
                try: 
                    df_result, label_encoder = tag_files(uploaded_files, mode)
                    st.success("✅ ¡Etiquetado completado con éxito!")
                    
                    return df_result, label_encoder

                except custom_exceptions.FileProcessingError:
                    st.error(f"¡Error al procesar los archivos!")

                except custom_exceptions.SchemaValidationError:
                    st.error(f"¡Error al validar el esquema!")
                
                except custom_exceptions.DateConversionError:
                    st.error(f"¡Error al convertir la fecha. Formato no válido!")

                except custom_exceptions.ModelDownloadError:
                    st.error(f"¡Error al descargar el modelo!")

                except custom_exceptions.FileStructureError:
                    st.error(f"¡Los archivos no tienen la misma estructura!")

                except custom_exceptions.InvalidFileError as e:
                    st.error(f"¡El archivo no es válido! {e}")

                except custom_exceptions.CleaningFileError:
                    st.error(f"¡Error limpiando archivo!")
                
                except custom_exceptions.IAAgentError:
                    st.error(f"¡Error usando el Agente de IA!")

                except Exception as e:
                    logging.error(f"Error no identificado: {e}")
                    st.error(f"¡Error no identificado!")

    return None, None

def home_button():
    if st.button("⬅️ Volver al Inicio", on_click=clean_memory):
        st.session_state['current_view'] = 'home'
        st.rerun()


@st.dialog("Confirmar Grabación")
def confirm_save_dialog(df, mode):
    st.write("¿Has revisado las etiquetas de las predicciones y estás seguro de que quieres grabar la revisión?")
    st.write("Los extractos que has revisado serán mandados directamente a la base de datos y se usarán para entrenar al modelo predictor.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Sí, estoy seguro", type="primary"):
            with st.spinner("Guardando revisión en la base de datos..."):
                try:
                    upload_review(df, mode)
                    
                    
                    st.success("✅ ¡Revisión guardada correctamente!")
                    time.sleep(2)
                    st.rerun()
                    
                except custom_exceptions.SchemaValidationError:
                    st.error(f"¡Error al validar el esquema!")
                
                except custom_exceptions.DateConversionError:
                    st.error(f"¡Error al convertir la fecha. Formato no válido!")
                
                except custom_exceptions.HashGenerationError:
                    st.error(f"¡Error al generar el hash de los extractos!")
                
                except custom_exceptions.DataUploadError:
                    st.error(f"¡Error al subir datos a BigQuery!")
                
                except Exception as e:
                    logging.error(f"Error no identificado: {e}")
                    st.error(f"¡Error no identificado!")

    with col2:
        if st.button("No, cancelar"):
            st.rerun()

def save_review(df_edited: pd.DataFrame, mode: Literal['general','ibecosol','personalized']):
    """
    Muestra el botón de guardar revisión y gestiona el flujo de confirmación.
    """
    if df_edited is not None and not df_edited.empty:
        st.caption("Una vez hayas revisado las etiquetas, guarda los cambios para mejorar el modelo.")
        if st.button("Grabar Revisión", type="primary"):
             confirm_save_dialog(df_edited, mode)

    
