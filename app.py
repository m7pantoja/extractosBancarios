import streamlit as st
import app_utils
import engine.engine_utils as engine_utils
import gcs_utils
from engine.trainer import train_model

#  Constantes
bucket_name = 'extractosbancarios-cloud-lf'
blob_name_general = 'models/general/general_v1.joblib'
blob_name_ibecosol = 'models/ibecosol/ibecosol_v1.joblib'

# Configuración de la página
st.set_page_config(
    page_title="Etiquetado de Extractos Bancarios",
    page_icon="🏦",
    layout="wide"
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

    st.markdown("### Instrucciones sobre el formato de los archivos:")
    st.markdown("""
    1. Los archivos deben estar en formato `.xlsx`, `.xls` o `.csv`.
    2. Los archivos deben contener en la **primera fila** los nombres de las variables o columnas.
    3. Los archivos deben tener **obligatoriamente** las siguientes 4 columnas, en cualquier orden, pero con estos nombres:

        - **fecha**. La fecha (y opcionalmente la hora) en la que se registró la transacción. Debe de usarse un formato válido y preferiblemente único en todo el conjunto de datos.

        Ejemplo: `2025-03-12 00:00:00`

        - **descripcion**. El texto o concepto del movimiento bancario.

        Ejemplo: `PRIMA SEG. AUTONOMO, 094089860700300`

        - **importe**. El monto de la transacción. Los gastos/salidas deben ser números negativos y los ingresos/entradas números positivos. No se deben incluir carácteres especiales de monedas como `€` o `$` y el separador decimal debe ser el punto `.`.

        Ejemplo: `-4395.75` o `224.89`

        - **saldo**. El saldo de la cuenta después de que la transacción se haya efectuado. Se aplican las mismas restricciones que a la columna `importe`.

        Ejemplo: `5025.14`
    4. Los archivos deben tener la **misma estructura** entre sí, es decir, las mismas columnas.
    """)

    # Files uploader
    uploaded_files = st.file_uploader(
        "Arrastra los archivos que quieres etiquetar o haz clic para buscar", 
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Soporta archivos Excel y CSV"
    )

    if st.button("Etiquetar", type="primary"):
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
                            st.error("No se pudo cargar el modelo desde GCS.")
                else:
                    st.error("No se pudieron leer datos de los archivos subidos.")


def show_personalized():
    st.button("⬅️ Volver al Inicio", on_click=go2homepage)
    st.header("Etiquetado Personalizado")

    st.markdown("### Instrucciones sobre el formato de los archivos:")
    st.markdown("""
    1. Los archivos deben estar en formato `.xlsx`, `.xls` o `.csv`.
    2. Los archivos deben contener en la **primera fila** los nombres de las variables o columnas.
    3. Los archivos deben tener **obligatoriamente** las siguientes 4 columnas, en cualquier orden, pero con estos nombres:

        - **fecha**. La fecha (y opcionalmente la hora) en la que se registró la transacción. Debe de usarse un formato válido y preferiblemente único en todo el conjunto de datos.

        Ejemplo: `2025-03-12 00:00:00`

        - **descripcion**. El texto o concepto del movimiento bancario.

        Ejemplo: `PRIMA SEG. AUTONOMO, 094089860700300`

        - **importe**. El monto de la transacción. Los gastos/salidas deben ser números negativos y los ingresos/entradas números positivos. No se deben incluir carácteres especiales de monedas como `€` o `$` y el separador decimal debe ser el punto `.`.

        Ejemplo: `-4395.75` o `224.89`

        - **saldo**. El saldo de la cuenta después de que la transacción se haya efectuado. Se aplican las mismas restricciones que a la columna `importe`.

        Ejemplo: `5025.14`
    4. Los archivos de entrenamiento deben contener además una columna llamada **etiqueta** que indique la categoría a la que pertenece cada transacción.
    5. Para cada conjunto de archivos (etiquetados y no etiquetados) se debe tener la **misma estructura** entre sí, es decir, las mismas columnas.
    """)

    # Training files uploader
    training_files = st.file_uploader(
        "Arrastra los archivos de entrenamiento o haz clic para buscar", 
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Soporta archivos Excel y CSV"
    )

    # Predict files uploader
    predict_files = st.file_uploader(
        "Arrastra los archivos que quieres etiquetar o haz clic para buscar", 
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Soporta archivos Excel y CSV"
    )

    if st.button("Etiquetar", type="primary"):
        if not predict_files or not training_files:
            st.warning("⚠️ Por favor, sube al menos un archivo de cada tipo para continuar.")
        else:
            with st.spinner("Procesando archivos..."):

                # 1. Unificar archivos
                df_train = app_utils.files_to_dataframe(training_files)
                df_predict = app_utils.files_to_dataframe(predict_files)

                if df_train is not None and not df_train.empty:
                    # 2. Validar esquema
                    df_train_validado = engine_utils.schema_validation(df_train, mode='train')

                if df_predict is not None and not df_predict.empty:
                    # 2. Validar esquema
                    df_predict_validado = engine_utils.schema_validation(df_predict, mode='predict')
                    
                    if df_predict_validado is not None:
                        # 3. Entrenar modelo
                        loaded_model = train_model(df_train_validado, {'client': 'personalized'})
                        
                        if loaded_model:
                            # 4. Predicción
                            try:
                                df_result = loaded_model.predict(df_predict_validado)
                                st.success("✅ ¡Etiquetado completado con éxito!")
                                st.dataframe(df_result, use_container_width=True)
                            except Exception as e:
                                st.error(f"Error durante la predicción: {e}")
                        else:
                            st.error("No se pudo cargar el modelo desde GCS.")
                else:
                    st.error("No se pudieron leer datos de los archivos subidos.")


def show_ibecosol():
    st.button("⬅️ Volver al Inicio", on_click=go2homepage)
    st.header("Etiquetado Ibecosol")
    
    st.markdown("### Instrucciones sobre el formato de los archivos:")
    st.markdown("""
    1. Los archivos deben estar en formato `.xlsx`, `.xls` o `.csv`.
    2. Los archivos deben contener en la **primera fila** los nombres de las variables o columnas.
    3. Los archivos deben tener **obligatoriamente** las siguientes 4 columnas, en cualquier orden, pero con estos nombres:

        - **fecha**. La fecha (y opcionalmente la hora) en la que se registró la transacción. Debe de usarse un formato válido y preferiblemente único en todo el conjunto de datos.

        Ejemplo: `2025-03-12 00:00:00`

        - **descripcion**. El texto o concepto del movimiento bancario.

        Ejemplo: `PRIMA SEG. AUTONOMO, 094089860700300`

        - **importe**. El monto de la transacción. Los gastos/salidas deben ser números negativos y los ingresos/entradas números positivos. No se deben incluir carácteres especiales de monedas como `€` o `$` y el separador decimal debe ser el punto `.`.

        Ejemplo: `-4395.75` o `224.89`

        - **saldo**. El saldo de la cuenta después de que la transacción se haya efectuado. Se aplican las mismas restricciones que a la columna `importe`.

        Ejemplo: `5025.14`
    4. Los archivos deben tener la **misma estructura** entre sí, es decir, las mismas columnas.
    """)

    # Files uploader
    uploaded_files = st.file_uploader(
        "Arrastra los archivos que quieres etiquetar o haz clic para buscar", 
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Soporta archivos Excel y CSV"
    )

    if st.button("Etiquetar", type="primary"):
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
                        loaded_model = gcs_utils.load_model_from_gcs(
                            bucket_name, 
                            blob_name_ibecosol
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
                            st.error("No se pudo cargar el modelo desde GCS.")
                else:
                    st.error("No se pudieron leer datos de los archivos subidos.")

# --- CONTROLADOR PRINCIPAL ---
    
if st.session_state['current_view'] == 'homepage':
    show_homepage()
elif st.session_state['current_view'] == 'general':
    show_general()
elif st.session_state['current_view'] == 'personalized':
    show_personalized()
elif st.session_state['current_view'] == 'ibecosol':
    show_ibecosol()