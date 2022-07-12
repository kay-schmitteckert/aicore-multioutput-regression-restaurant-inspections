"""Model serving example"""

from os.path import exists
from typing import Dict
import joblib
import pandas as pd
from flask import Flask, request
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import OrdinalEncoder
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

sentence_transformer: SentenceTransformer = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
regr_model: MultiOutputRegressor
ordinal_encoder: OrdinalEncoder

@app.before_first_request
def init():
    """
    Load the model if it is available locally
    """
    global regr_model
    global ordinal_encoder
    MODEL_OUTPUT_PATH = "/mnt/models"
    MODEL_NAME = "inspection-mo-regression-model.pickle"
    ENCODER_NAME = "ord-enc.pickle"
    MODEL_PATH = f"{MODEL_OUTPUT_PATH}/{MODEL_NAME}"
    ENCODER_PATH = f"{MODEL_OUTPUT_PATH}/{ENCODER_NAME}"

    if exists(MODEL_PATH):
        print(f"Loading regression model from {MODEL_PATH}")
        regr_model = joblib.load(MODEL_PATH)
    else:
        raise FileNotFoundError(MODEL_PATH)

    if exists(ENCODER_PATH):
        print(f"Loading encoder model from {ENCODER_PATH}")
        regr_model = joblib.load(ENCODER_PATH)
    else:
        raise FileNotFoundError(ENCODER_PATH)

    return None

def prepare_input_data(input_data: Dict) -> pd.DataFrame:
    FEATURES_CATEGORICAL = ["business_name", "business_postal_code"]
    FEATURES_EMBEDDINGS = ["violation_description"]

    inspections = pd.DataFrame.from_records(input_data)
    inspections = inspections[["business_name", "business_postal_code", "violation_description"]]

    inspections_processed = pd.DataFrame()

    """
    ENCODE CATEGORICAL FEATURES
    """
    print("ENCODE CATEGORICAL FEATURES")
    inspections_processed[FEATURES_CATEGORICAL] = ordinal_encoder.transform(inspections[FEATURES_CATEGORICAL].values)
    inspections_processed[FEATURES_CATEGORICAL] = inspections_processed[FEATURES_CATEGORICAL].astype('category')

    """
    CALCULATE EMBEDDINGS
    """
    print("CALCULATE EMBEDDINGS")
    for feature in FEATURES_EMBEDDINGS:
        feature_values = list(inspections[feature].values)
        embeddings = sentence_transformer.encode(feature_values)
        embedding_columns = [feature + f"_{str(i)}" for i in range(embeddings[0].shape[0])]
        inspections_processed = pd.concat([inspections_processed, pd.DataFrame(list(embeddings), columns=embedding_columns)], axis=1)
    
    return inspections_processed

@app.route("/v1/models/{}:predict".format("regrmodel"), methods=["POST"])
def predict():
    "Make the model available for inference requests."
    input_data: pd.DataFrame = prepare_input_data(dict(request.json))
    prediction = regr_model.predict([input_data["text"]])
    output = {"predictions": prediction}

    return output


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0", debug=True, port=9001)

# curl --location --request POST 'http://localhost:9001/v1/models/regrmodel:predict' --header 'Content-Type: application/json' --data-raw '{"text": "A restaurant with great ambiance"}'