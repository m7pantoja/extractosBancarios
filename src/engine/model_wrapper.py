import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

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

    def predict(self, validated_data: pd.DataFrame):
        "Make predictions using the model. The dataframe must have been validated."

        data = validated_data.copy()
        # new variables for training the model
        data['fecha_day'] = data['fecha'].dt.day
        data['fecha_month'] = data['fecha'].dt.month
        data['fecha_year'] = data['fecha'].dt.year

        features = ['fecha_day', 'fecha_month','fecha_year','descripcion','importe','saldo']
        target = 'etiqueta'

        X = data[features]
        Y_pred = self.pipeline.predict(X)

        Y_pred_labels = self.label_encoder.inverse_transform(Y_pred)
        validated_data[target] = Y_pred_labels

        return validated_data

    def __repr__(self):
        v = self.metadata.get('version', 'N/A')
        c = self.metadata.get('client', 'N/A')
        d = self.metadata.get('date', 'N/A')
        return f"<Model: client='{c}' version='{v}' date='{d}' type='XGBClassifier'>"