from engine import files_to_dataframe, schema_validation, model.Model
from database import download_model_from_gcs
from typing import Literal

def tag_files(uploaded_files: list, model_name: Literal['general', 'ibecosol']) -> pd.DataFrame:

        unified_df = files_to_dataframe(uploaded_files)
        validated_df = schema_validation(unified_df, mode='predict')

        model_dict = download_model_from_gcs(model_name)
        model = model.Model.from_dict(model_dict) # posibles errores no controlados

        df_result = model.predict(validated_df) # posibles errores no controlados

        return df_result
    
    