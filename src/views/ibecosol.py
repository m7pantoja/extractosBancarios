import streamlit as st
import home
import src_utils

def show_page():
    st.button("⬅️ Volver al Inicio", on_click=home.show_page())
    st.header("Etiquetado Ibecosol")

    # INSTRUCCIONES SOBRE EL FORMATO DE LOS ARCHIVOS
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

    # FILE UPLOADER
    uploaded_files = src_utils.file_uploader()

    # TAG BUTTON
    df_result = src_utils.tag_button(uploaded_files, 'ibecosol')