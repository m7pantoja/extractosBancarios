import streamlit as st
from src import widgets

def show_page():
    widgets.home_button()
    st.header("Etiquetado Personalizado")

    # INSTRUCCIONES SOBRE EL FORMATO DE LOS ARCHIVOS
    st.markdown("### Instrucciones sobre el formato de los archivos:")
    st.markdown("""
    1. Los archivos deben estar en formato `.xlsx`, `.xls` o `.csv`.
    2. Los archivos deben tener **obligatoriamente** 4 columnas referentes a la `Fecha`, la `Descripción`, el `Importe` y el `Saldo` de la transacción.
    3. Los archivos de entrenamiento deben contener además una columna llamada `etiqueta` que indique la categoría a la que pertenece cada transacción.
    4. Para cada conjunto de archivos (etiquetados y no etiquetados) se debe tener la **misma estructura** entre sí, es decir, las mismas columnas.
    """)

    training_files = widgets.file_uploader("Arrastra los archivos de entrenamiento o haz clic para buscar")
    predict_files = widgets.file_uploader("Arrastra los archivos que quieres etiquetar o haz clic para buscar")
    uploaded_files = [training_files, predict_files]

    df_result, label_encoder = widgets.tag_button(uploaded_files, 'personalized')
    widgets.show_data(df_result, label_encoder)
