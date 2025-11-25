from streamlit import UploadedFile
import pandas as pd

def files_to_dataframe(uploaded_files: list[UploadedFile]) -> pd.DataFrame: 
    """
    Transforma los archivos de una lista de UploadedFile en un único DataFrame.

    Args:
        uploaded_files: La lista de archivos de tipo UploadedFile.
    Returns:
        Un DataFrame de pandas con los datos de los archivos.
    """

    dfs = list()

    for file in uploaded_files:

        # 1. XLSX y XLS
        if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
            try:
                dfs.append(pd.read_excel(file))
            except Exception as e:
                print(f'Error al cargar .xlsx: {e}')

        # 2. CSV
        elif file.name.endswith('.csv'):
            try:
                dfs.append(pd.read_csv(file))
            except Exception as e:
                print(f'Error al cargar .csv: {e}')

        # 3. FORMATO DESCONOCIDO 
        else:
            print(f"Error: Formato de archivo no reconocido o enlace no compatible: {file.name}")
            print("La función solo acepta archivos CSV, XLS y XLSX.")
        
    data = pd.concat(dfs)

    return data