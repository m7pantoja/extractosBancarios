import pandas as pd
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils.class_weight import compute_sample_weight
from . import model_wrapper
from .engine_utils import schema_validation

# FUNCIÓN PRINCIPAL ------------------------------------------------

def train_model(df: pd.DataFrame, metadata: dict) -> model_wrapper.Model:
    '''
    Validates data, engineers date features, 
    and trains a class-weighted XGBoost pipeline with TF-IDF text processing,
    returning an object of the class Model with the provided metadata.
    '''

    validated_df = schema_validation(df, mode='train')

    # new variables for training the model
    validated_df['fecha_day'] = validated_df['fecha'].dt.day
    validated_df['fecha_month'] = validated_df['fecha'].dt.month
    validated_df['fecha_year'] = validated_df['fecha'].dt.year

    # ENCODING

    features = ['fecha_day','fecha_month','fecha_year','descripcion','importe']
    target = 'etiqueta'

    X = validated_df[features]
    Y = validated_df[target]

    le = LabelEncoder()
    Y_encoded = le.fit_transform(Y)

    sample_weights = compute_sample_weight(class_weight='balanced',y=Y_encoded)

    # PREPROCESSOR DEFINITION

    numeric_transformer = 'passthrough'
    text_transformer = TfidfVectorizer(
            ngram_range=(1, 2), 
            max_features=1500
        )

    numeric_features = ['fecha_day','fecha_month','fecha_year','importe']

    preprocessor = ColumnTransformer(
            transformers=[
                ('text_trans', text_transformer, 'descripcion'),
                ('num_trans', numeric_transformer, numeric_features)
            ])

    # PIPELINE

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', XGBClassifier(  
            eval_metric='mlogloss',    
            n_estimators=100,          
            random_state=42,           
            n_jobs=-1                  
        ))
    ])

    # MODEL TRAINING AND PREDICTION

    pipeline.fit(X, Y_encoded, classifier__sample_weight=sample_weights)

    deployed_model = model_wrapper.Model(pipeline, le, metadata)

    return deployed_model