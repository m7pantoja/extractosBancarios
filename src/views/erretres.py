import streamlit as st
import widgets

def show_page():
    widgets.home_button()
    st.header("Etiquetado Erretres")

    # INSTRUCCIONES SOBRE EL FORMATO DE LOS ARCHIVOS
    st.markdown("### Instrucciones sobre el formato de los archivos:")
    st.markdown("""
    1. Los archivos deben estar en formato `.xlsx`, `.xls` o `.csv`.
    2. Los archivos deben tener **obligatoriamente** 4 columnas referentes a la `Fecha`, la `Descripción`, el `Importe` y el `Saldo` de la transacción.
    3. Si se sube más de un archivo, deben tener la **misma estructura** entre sí, es decir, las mismas columnas.
    """)
    
    # FILE UPLOADER
    uploaded_files = widgets.file_uploader("Arrastra los archivos que quieres etiquetar o haz clic para buscar")

    # TAG BUTTON
    df_result, label_encoder = widgets.tag_button(uploaded_files, 'erretres')
    df_edited = widgets.show_data(df_result, label_encoder)
    widgets.save_review(df_edited, 'erretres')