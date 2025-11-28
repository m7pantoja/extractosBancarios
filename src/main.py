import streamlit as st
import views

# CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Etiquetado de Extractos Bancarios",
    page_icon="🏦",
    layout="wide"
)

# Inicializar el estado de la navegación si no existe
if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'home'

# --- CONTROLADOR PRINCIPAL ---

if st.session_state['current_view'] == 'home':
    views.home.show_page()
elif st.session_state['current_view'] == 'general':
    views.general.show_page()
elif st.session_state['current_view'] == 'personalized':
    views.personalized.show_page()
elif st.session_state['current_view'] == 'ibecosol':
    views.ibecosol.show_page()