import streamlit as st
import app_utils
import engine.engine_utils as engine_utils
import gcs_utils
import engine.model as model

#  Constantes
bucket_name = 'extractosbancarios-cloud-lf'
blob_name_general = 'models/general/general_v1.joblib'

# Configuración de la página
st.set_page_config(
    page_title="Etiquetado de Extractos Bancarios",
    page_icon="🏦",
    layout="centered" 
)

# Inicializar el estado de la navegación si no existe
if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'homepage'

# Función para volver al homepage
def go2homepage():
    st.session_state['current_view'] = 'homepage'

# --- DEFINICIÓN DE LAS VISTAS ---

def show_homepage():
    st.title("Etiquetado de Extractos Bancarios")
    st.write("Selecciona el tipo de etiquetado que deseas realizar:")
    st.write("")
    
    col1, col2, col3 = st.columns([1, 6, 1]) # Columnas de margen para centrar visualmente
    with col2:
        if st.button("Etiquetado General", width='stretch'):
            st.session_state['current_view'] = 'general'
            st.rerun()
            
        st.write("") # Pequeño espacio vertical
        
        if st.button("Etiquetado Personalizado", width='stretch'):
            st.session_state['current_view'] = 'personalized'
            st.rerun()
            
        st.write("") 

        if st.button("Etiquetado Ibecosol", width='stretch'):
            st.session_state['current_view'] = 'ibecosol'
            st.rerun()

def show_general():
    st.button("⬅️ Volver al Inicio", on_click=go2homepage)
    st.header("Etiquetado General")

    # Files uploader
    uploaded_files = st.file_uploader(
        "Arrastra tus archivos aquí o haz clic para buscar", 
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Soporta archivos Excel y CSV"
    )

    if st.button("🚀 Etiquetar", type="primary"):
        if not uploaded_files:
            st.warning("⚠️ Por favor, sube al menos un archivo para continuar.")
        else:
            with st.spinner("Procesando archivos..."):

                # 1. Unificar archivos
                df = app_utils.files_to_dataframe(uploaded_files)

                if df is not None and not df.empty:
                    # 2. Validar esquema
                    df_validado = engine_utils.schema_validation(df, mode='predict')
                    
                    if df_validado is not None:
                        # 3. Cargar modelo
                        st.info("Cargando modelo desde GCS...")
                        loaded_model = gcs_utils.load_model_from_gcs(
                            bucket_name, 
                            blob_name_general
                        )
                        
                        if loaded_model:
                            # 4. Predicción
                            try:
                                df_result = loaded_model.predict(df_validado)
                                st.success("✅ ¡Etiquetado completado con éxito!")
                                st.dataframe(df_result, use_container_width=True)
                            except Exception as e:
                                st.error(f"Error durante la predicción: {e}")
                        else:
                            st.error("No se pudo cargar el modelo.")
                else:
                    st.error("No se pudieron leer datos de los archivos subidos.")


def show_personalized():
    st.button("⬅️ Volver al Inicio", on_click=go2homepage)
    st.header("Etiquetado Personalizado")
    st.warning("Módulo de reglas personalizadas en construcción.")

def show_ibecosol():
    st.button("⬅️ Volver al Inicio", on_click=go2homepage)
    st.header("Etiquetado Ibecosol")
    
    # Files uploader
    uploaded_files = st.file_uploader(
        "Arrastra los archivos que quieres etiqueta o haz clic para buscar", 
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Soporta archivos Excel y CSV"
    )

# --- CONTROLADOR PRINCIPAL ---
    
if st.session_state['current_view'] == 'homepage':
    show_homepage()
elif st.session_state['current_view'] == 'general':
    show_general()
elif st.session_state['current_view'] == 'personalized':
    show_personalized()
elif st.session_state['current_view'] == 'ibecosol':
    show_ibecosol()