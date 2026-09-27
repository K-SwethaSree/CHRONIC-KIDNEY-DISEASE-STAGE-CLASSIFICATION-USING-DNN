

def analyze_risk_factors(
    gfr,
    serum_creatinine,
    bun,
    blood_pressure,
    hematuria
):

    risks = []

    # GFR
    if gfr < 15:
        risks.append(
            "Very low GFR detected. Medical evaluation is important."
        )

    elif gfr < 30:
        risks.append(
            "Low GFR detected. Kidney function should be monitored by a healthcare professional."
        )

    elif gfr < 60:
        risks.append(
            "Reduced GFR detected. Discuss kidney health with a healthcare professional."
        )

    # Serum Creatinine
    if serum_creatinine > 1.5:
        risks.append(
            "Elevated serum creatinine may indicate reduced kidney function."
        )

    # BUN
    if bun > 40:
        risks.append(
            "Elevated BUN detected. Discuss the result with a healthcare professional."
        )

    # Blood Pressure
    if blood_pressure >= 140:
        risks.append(
            "High blood pressure detected. Blood pressure management is important for kidney health."
        )

    elif blood_pressure >= 130:
        risks.append(
            "Blood pressure is above the preferred range. Regular monitoring is recommended."
        )

    # Hematuria
    if hematuria == 1:
        risks.append(
            "Blood detected in urine. Discuss this finding with a healthcare professional."
        )

    # No major risk found
    if not risks:
        risks.append(
            "No major risk factors were identified from the entered values."
        )

    return risks