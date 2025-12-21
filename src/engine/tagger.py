from .engine_utils import files_to_dataframe
from . import model_wrapper
from .trainer import train_model
from src.database.download import download_model_from_gcs
from typing import Literal

def tag_files(uploaded_files: list, mode: Literal['general', 'ibecosol','erretres','personalized']):

        if mode == 'personalized':
            unified_train = files_to_dataframe(uploaded_files[0])
            unified_predict = files_to_dataframe(uploaded_files[1])

            model = train_model(unified_train, {'client': 'personalized'}) # posibles errores no controlados
            le = model.label_encoder
            df_result, _ = model.predict(unified_predict) # posibles errores no controlados. 

            return df_result, le
        else:           
            unified_df = files_to_dataframe(uploaded_files)

            model_dict = download_model_from_gcs(mode)
            model = model_wrapper.Model.from_dict(model_dict) # posibles errores no controlados
            le = model.label_encoder

            df_result, confidence = model.predict(unified_df) # posibles errores no controlados.
            df_result['confidence'] = confidence

            return df_result, le
