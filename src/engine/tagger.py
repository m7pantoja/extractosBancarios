from .engine_utils import files_to_dataframe, schema_validation
from . import model_wrapper
from .trainer import train_model
from database.download_models import download_model_from_gcs
from typing import Literal
import pandas as pd

def tag_files(uploaded_files: list, mode: Literal['general', 'ibecosol','personalized']) -> pd.DataFrame:

        if mode == 'personalized':
            unified_train = files_to_dataframe(uploaded_files[0])
            unified_predict = files_to_dataframe(uploaded_files[1])

            validated_train = schema_validation(unified_train, mode='train')
            validated_predict = schema_validation(unified_predict, mode='predict')

            model = train_model(validated_train, {'client': 'personalized'}) # posibles errores no controlados
            df_result = model.predict(validated_predict) # posibles errores no controlados

            return df_result
        else:           
            unified_df = files_to_dataframe(uploaded_files)
            validated_df = schema_validation(unified_df, mode='predict')

            model_dict = download_model_from_gcs(mode)
            model = model_wrapper.Model.from_dict(model_dict) # posibles errores no controlados

            df_result = model.predict(validated_df) # posibles errores no controlados

            return df_result
    
