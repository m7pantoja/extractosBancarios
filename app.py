import streamlit as st

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
    st.info("Aquí irán las herramientas para la clasificación general de extractos.")

def show_personalized():
    st.button("⬅️ Volver al Inicio", on_click=go2homepage)
    st.header("Etiquetado Personalizado")
    st.warning("Módulo de reglas personalizadas en construcción.")

def show_ibecosol():
    st.button("⬅️ Volver al Inicio", on_click=go2homepage)
    st.header("Etiquetado Ibecosol")
    st.success("Módulo específico para Ibecosol listo para configurar.")

# --- CONTROLADOR PRINCIPAL ---
    
if st.session_state['current_view'] == 'homepage':
    show_homepage()
elif st.session_state['current_view'] == 'general':
    show_general()
elif st.session_state['current_view'] == 'personalized':
    show_personalized()
elif st.session_state['current_view'] == 'ibecosol':
    show_ibecosol()