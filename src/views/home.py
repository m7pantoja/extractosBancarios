import streamlit as st
from engine.uploader import upload_feedback
import time
from src import custom_exceptions

def show_page():
    st.title("Etiquetado de Extractos Bancarios")
    st.write("Selecciona el tipo de etiquetado que deseas realizar:")
    st.write("")
    
    col1, col2, col3 = st.columns([1, 6, 1]) # Columnas de margen para centrar visualmente
    with col2:
        if st.button("Etiquetado General", width='stretch'):
            st.session_state['current_view'] = 'general'
            st.rerun()
            
        st.write("")
        
        if st.button("Etiquetado Personalizado", width='stretch'):
            st.session_state['current_view'] = 'personalized'
            st.rerun()
            
        st.write("") 

        if st.button("Etiquetado Ibecosol", width='stretch'):
            st.session_state['current_view'] = 'ibecosol'
            st.rerun()

        st.write("")

        if st.button("Etiquetado Erretres", width='stretch'):
            st.session_state['current_view'] = 'erretres'
            st.rerun()

    st.text("\n")

    st.subheader("Comentarios y Sugerencias")
    
    with st.form("feedback_form", clear_on_submit=True):
        comment = st.text_area("Deja tu comentario para mejorar la herramienta:", height=100)
        submitted = st.form_submit_button("Enviar Comentario")
        
        if submitted:
            if comment.strip():
                with st.spinner("Enviando comentario..."):
                    try:
                        upload_feedback(comment)
                        st.success("¡Gracias por tu comentario!")
                        time.sleep(2)
                        st.rerun()
                    except custom_exceptions.DataUploadError:
                        st.error(f"¡Error al subir el comentario a la base de datos!")
            else:
                st.warning("Por favor, escribe un comentario antes de enviar.")
