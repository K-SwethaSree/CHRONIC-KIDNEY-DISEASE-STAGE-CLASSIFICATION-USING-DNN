import os
import random
import pickle

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau


# ============================================================
# 1. SETTINGS
# ============================================================

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
keras.utils.set_random_seed(SEED)

DATA_PATH = r"C:\CKD\data\CKD_Dataset.csv"
MODEL_DIR = r"C:\CKD\models"


# ============================================================
# 2. CREATE MODEL FOLDER
# ============================================================

os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================================
# 3. LOAD DATASET
# ============================================================

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ============================================================
# 4. FEATURES
# ============================================================

FEATURES = [
    "gfr",
    "serum_creatinine",
    "bun",
    "serum_calcium",
    "ana",
    "c3_c4",
    "hematuria",
    "oxalate_levels",
    "urine_ph",
    "blood_pressure"
]

TARGET = "ckd_stage"

STAGE_NAMES = [
    "No CKD",
    "Stage 1",
    "Stage 2",
    "Stage 3",
    "Stage 4",
    "Stage 5"
]


# ============================================================
# 5. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = FEATURES + [TARGET]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns in dataset: {missing_columns}"
    )


# ============================================================
# 6. SELECT FEATURES AND TARGET
# ============================================================

X = df[FEATURES].copy()
y = df[TARGET].astype(int)


# ============================================================
# 7. HANDLE MISSING VALUES
# ============================================================

X = X.fillna(X.median())


# ============================================================
# 8. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=SEED,
    stratify=y
)


# ============================================================
# 9. FEATURE SCALING
# ============================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ============================================================
# 10. BUILD DNN MODEL
# ============================================================

n_features = X_train_scaled.shape[1]

model = Sequential([
    Input(shape=(n_features,)),

    Dense(128, activation="relu"),
    Dropout(0.1),

    Dense(64, activation="relu"),
    Dropout(0.1),

    Dense(32, activation="relu"),

    Dense(6, activation="softmax")
])


# ============================================================
# 11. COMPILE MODEL
# ============================================================

model.compile(
    optimizer=keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# ============================================================
# 12. CALLBACKS
# ============================================================

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=25,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=6,
    min_lr=1e-5
)


# ============================================================
# 13. TRAIN MODEL
# ============================================================

print("\nTraining model...")

history = model.fit(
    X_train_scaled,
    y_train,
    validation_split=0.20,
    epochs=300,
    batch_size=32,
    callbacks=[
        early_stopping,
        reduce_lr
    ],
    verbose=1
)


# ============================================================
# 14. EVALUATE MODEL
# ============================================================

test_probabilities = model.predict(
    X_test_scaled,
    verbose=0
)

test_predictions = np.argmax(
    test_probabilities,
    axis=1
)

accuracy = accuracy_score(
    y_test,
    test_predictions
)

print("\n================================")
print("MODEL PERFORMANCE")
print("================================")

print("Test Accuracy:", round(accuracy, 4))

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        test_predictions,
        labels=list(range(6)),
        target_names=STAGE_NAMES,
        zero_division=0
    )
)


# ============================================================
# 15. SAVE MODEL
# ============================================================

model_path = os.path.join(
    MODEL_DIR,
    "ckd_model.keras"
)

model.save(model_path)


# ============================================================
# 16. SAVE SCALER
# ============================================================

scaler_path = os.path.join(
    MODEL_DIR,
    "scaler.pkl"
)

with open(scaler_path, "wb") as file:
    pickle.dump(scaler, file)


# ============================================================
# 17. SAVE FEATURE NAMES
# ============================================================

feature_path = os.path.join(
    MODEL_DIR,
    "feature_names.pkl"
)

with open(feature_path, "wb") as file:
    pickle.dump(FEATURES, file)


# ============================================================
# 18. SAVE STAGE NAMES
# ============================================================

stage_path = os.path.join(
    MODEL_DIR,
    "stage_names.pkl"
)

with open(stage_path, "wb") as file:
    pickle.dump(STAGE_NAMES, file)


# ============================================================
# 19. FINISHED
# ============================================================

print("\n================================")
print("MODEL SAVING COMPLETED")
print("================================")

print("Model:", model_path)
print("Scaler:", scaler_path)
print("Features:", feature_path)
print("Stages:", stage_path)