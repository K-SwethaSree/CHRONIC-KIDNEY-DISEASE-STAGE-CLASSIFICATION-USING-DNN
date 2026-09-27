from prediction import predict_ckd


patient = {

    "gfr": 45,

    "serum_creatinine": 2.0,

    "bun": 35,

    "serum_calcium": 9.0,

    "ana": 1,

    "c3_c4": 1,

    "hematuria": 1,

    "oxalate_levels": 30,

    "urine_ph": 6.0,

    "blood_pressure": 140
}


result = predict_ckd(patient)


print("\n==============================")
print("CKD PREDICTION")
print("==============================")

print(
    "Predicted Stage:",
    result["stage"]
)

print(
    "Confidence:",
    result["confidence"],
    "%"
)

print("\nStage Probabilities:")

for stage, probability in result["probabilities"].items():

    print(
        f"{stage}: {probability}%"
    )