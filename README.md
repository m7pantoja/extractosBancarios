# 📊 Etiquetado Automático de Extractos Bancarios

Herramienta interactiva basada en Streamlit para el procesamiento, limpieza y etiquetado automático de extractos bancarios. Esta aplicación está diseñada para facilitar la categorización de movimientos financieros mediante reglas y modelos de Machine Learning, con integración directa a Google Cloud BigQuery.

## 🚀 Características Principales

- **Múltiples Modos de Etiquetado:**
  - **General:** Etiquetado basado en reglas generales predefinidas.
  - **Personalizado:** Permite subir un archivo histórico para entrenar un modelo específico y aplicarlo a nuevos datos.
  - **Ibecosol:** Flujo de trabajo específico para la entidad Ibecosol.
- **Interfaz Intuitiva:** Subida de archivos (CSV, Excel) y revisión interactiva de datos mediante tablas editables.
- **Feedback de Usuario:** Sistema integrado para enviar comentarios y sugerencias de mejora.
- **Integración Cloud:** Almacenamiento seguro de resultados y predicciones en Google BigQuery.
- **Validación de Datos:** Verificación automática de esquemas y formatos de archivo.

## 🛠️ Tecnologías

El proyecto utiliza un stack moderno de Python:

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Procesamiento de Datos:** Pandas, Pandera (validación), OpenPyXL/Xlrd (Excel)
- **Machine Learning:** Scikit-learn, XGBoost
- **Infraestructura Cloud:** Google Cloud BigQuery, Google Cloud Storage, Google OAuth2
- **Gestión de Dependencias:** `uv` (basado en `pyproject.toml`)

## 📂 Estructura del Proyecto

```

├── src/
│   ├── database/    # Lógica de conexión y carga a bases de datos (BigQuery)
│   ├── engine/      # Motores de procesamiento (tagger, uploader...)
│   ├── views/       # Vistas de la interfaz de usuario (home, etc.)
│   ├── main.py      # Punto de entrada de la aplicación
│   └── widgets.py   # Componentes reutilizables de UI
├── .streamlit/      # Configuración de Streamlit (carpeta oculta)
├── pyproject.toml   # Definición de dependencias del proyecto
├── uv.lock          # Archivo de bloqueo de versiones (uv)
└── README.md        # Documentación del proyecto
```

## ⚙️ Instalación y Configuración

### Prerrequisitos
- Python 3.12 o superior.
- [uv](https://github.com/astral-sh/uv) instalado (recomendado para gestión de dependencias).
- Credenciales de Google Cloud Service Account configuradas en `.streamlit/secrets.toml`.

### Pasos
1. **Clonar el repositorio** (si aplica) o navegar al directorio del proyecto.

2. **Instalar dependencias:**
   ```bash
   uv sync
   ```
   O usando pip estándar:
   ```bash
   pip install .
   ```

3. **Configurar Secretos:**
   Asegúrate de tener el archivo `.streamlit/secrets.toml` con la estructura adecuada para conectar con Google Cloud:
   ```toml
   [gcp_service_account]
   type = "service_account"
   project_id = "tu-project-id"
   private_key_id = "..."
   private_key = "..."
   client_email = "..."
   ...
   ```

## ▶️ Ejecución

Para iniciar la aplicación localmente:

```bash
uv run streamlit run src/main.py
```
*(O `streamlit run src/main.py` si tienes el entorno activado manualmente)*

## 📝 Uso

1. **Inicio:** Selecciona el modo de trabajo deseado (General, Personalizado o Ibecosol).
2. **Carga:** Sube tus archivos de extractos bancarios (y datos de entrenamiento si usas el modo personalizado).
3. **Etiquetado:** Pulsa "Etiquetar" para procesar los datos.
4. **Revisión:** Verifica las categorías asignadas, corrige si es necesario y observa el nivel de confianza.
5. **Guardado:** Confirma la grabación para subir los datos validados a BigQuery.
