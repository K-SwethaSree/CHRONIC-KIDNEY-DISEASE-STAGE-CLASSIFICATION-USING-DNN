import os
import pickle

import numpy as np
import pandas as pd

from tensorflow.keras.models import load_model


# ============================================================
# PATHS
# ============================================================

BASE_DIR = r"C:\CKD"

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "ckd_model.keras"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "scaler.pkl"
)

FEATURE_PATH = os.path.join(
    BASE_DIR,
    "models",
    "feature_names.pkl"
)

STAGE_PATH = os.path.join(
    BASE_DIR,
    "models",
    "stage_names.pkl"
)


# ============================================================
# LOAD MODEL
# ============================================================

model = load_model(MODEL_PATH)


# ============================================================
# LOAD SCALER
# ============================================================

with open(SCALER_PATH, "rb") as file:
    scaler = pickle.load(file)


# ============================================================
# LOAD FEATURE NAMES
# ============================================================

with open(FEATURE_PATH, "rb") as file:
    feature_names = pickle.load(file)


# ============================================================
# LOAD STAGE NAMES
# ============================================================

with open(STAGE_PATH, "rb") as file:
    stage_names = pickle.load(file)


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_ckd(patient_data):

    """
    Predict CKD stage from patient clinical values.

    Required patient_data keys:

    gfr
    serum_creatinine
    bun
    serum_calcium
    ana
    c3_c4
    hematuria
    oxalate_levels
    urine_ph
    blood_pressure
    """

    # Create DataFrame
    patient_df = pd.DataFrame(
        [patient_data],
        columns=feature_names
    )

    # Convert values to numeric
    patient_df = patient_df.astype(float)

    # Apply the SAME scaler used during training
    patient_scaled = scaler.transform(
        patient_df
    )

    # Get prediction probabilities
    probabilities = model.predict(
        patient_scaled,
        verbose=0
    )[0]

    # Get predicted class number
    predicted_stage_number = int(
        np.argmax(probabilities)
    )

    # Get stage name
    predicted_stage = stage_names[
        predicted_stage_number
    ]

    # Calculate confidence
    confidence = float(
        np.max(probabilities) * 100
    )

    # Create probability dictionary
    stage_probabilities = {}

    for i, stage in enumerate(stage_names):

        stage_probabilities[stage] = round(
            float(probabilities[i] * 100),
            2
        )

    # Return results
    return {
        "stage_number": predicted_stage_number,
        "stage": predicted_stage,
        "confidence": round(
            confidence,
            2
        ),
        "probabilities": stage_probabilities
    }