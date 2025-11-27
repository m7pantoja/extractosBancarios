import streamlit as st

def show_page():
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
