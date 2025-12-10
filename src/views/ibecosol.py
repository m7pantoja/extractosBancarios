import streamlit as st
import widgets

def show_page():
    widgets.home_button()
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
    uploaded_files = widgets.file_uploader("Arrastra los archivos que quieres etiquetar o haz clic para buscar")

    # TAG BUTTON
    df_result, label_encoder = widgets.tag_button(uploaded_files, 'ibecosol')
    df_edited = widgets.show_data(df_result, label_encoder)
    widgets.save_review(df_edited, 'ibecosol')