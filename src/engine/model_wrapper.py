import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from .engine_utils import schema_validation

class Model:
    def __init__(self, pipeline: Pipeline, label_encoder: LabelEncoder, metadata: dict):

        self.pipeline = pipeline
        self.label_encoder = label_encoder
        self.metadata = metadata

    @classmethod
    def from_dict(cls, model_dict: dict):
        """
        Método de fábrica para crear una instancia directamente desde un diccionario.
        """
        # Validamos que las claves existan para evitar errores crípticos
        required_keys = {'pipeline', 'label_encoder', 'metadata'}
        if not required_keys.issubset(model_dict.keys()):
            raise ValueError(f"El diccionario del modelo debe contener las claves: {required_keys}")
        
        return cls(
            pipeline=model_dict['pipeline'],
            label_encoder=model_dict['label_encoder'],
            metadata=model_dict['metadata']
        )

    def predict(self, data: pd.DataFrame):
        """Validates the data, makes predictions using the model, and returns the confidence."""

        validated_data = schema_validation(data, mode='predict') # creates column '__fecha__' for internal use

        # new variables for training the model
        validated_data['fecha_day'] = validated_data['__fecha__'].dt.day
        validated_data['fecha_month'] = validated_data['__fecha__'].dt.month
        validated_data['fecha_year'] = validated_data['__fecha__'].dt.year

        features = ['fecha_day', 'fecha_month','fecha_year','descripcion','importe','saldo']
        target = 'etiqueta'

        X = validated_data[features]
        Y_pred = self.pipeline.predict(X)
        Y_pred_proba = self.pipeline.predict_proba(X)
        confidence = np.max(Y_pred_proba, axis=1)

        Y_pred_labels = self.label_encoder.inverse_transform(Y_pred)
        data[target] = Y_pred_labels

        return data, confidence

    def __repr__(self):
        v = self.metadata.get('version', 'N/A')
        c = self.metadata.get('client', 'N/A')
        d = self.metadata.get('date', 'N/A')
        return f"<Model: client='{c}' version='{v}' date='{d}' type='XGBClassifier'>"