

def get_lifestyle_recommendations(
    stage,
    activity_level,
    preferred_activity,
    smoking,
    alcohol
):

    recommendations = []

    # ========================================================
    # ACTIVITY
    # ========================================================

    if activity_level == "Low":

        recommendations.append(
            "Try to include suitable physical activity gradually, according to your healthcare professional's advice."
        )

    elif activity_level == "Moderate":

        recommendations.append(
            "Continue regular physical activity at a comfortable level."
        )

    elif activity_level == "High":

        recommendations.append(
            "Maintain physical activity at a level appropriate for your health condition."
        )


    # ========================================================
    # PREFERRED ACTIVITY
    # ========================================================

    if preferred_activity == "Walking":

        recommendations.append(
            "Walking can be a convenient form of regular physical activity."
        )

    elif preferred_activity == "Yoga":

        recommendations.append(
            "Gentle yoga or stretching may be considered if appropriate for your health condition."
        )

    elif preferred_activity == "Exercise":

        recommendations.append(
            "Choose exercises that are appropriate for your current health condition."
        )

    elif preferred_activity == "Cycling":

        recommendations.append(
            "Cycling may be considered as a physical activity if it is comfortable and medically appropriate."
        )

    elif preferred_activity == "None":

        recommendations.append(
            "Discuss suitable physical activity options with a healthcare professional."
        )


    # ========================================================
    # SMOKING
    # ========================================================

    if smoking == "Yes":

        recommendations.append(
            "Consider stopping smoking because smoking can negatively affect overall and cardiovascular health."
        )

    else:

        recommendations.append(
            "Continue avoiding tobacco and smoking."
        )


    # ========================================================
    # ALCOHOL
    # ========================================================

    if alcohol == "Yes":

        recommendations.append(
            "Discuss alcohol use with your healthcare professional, especially if you have kidney disease or take medicines."
        )

    else:

        recommendations.append(
            "Continue avoiding or limiting alcohol according to your healthcare professional's advice."
        )


    # ========================================================
    # STAGE-SPECIFIC MESSAGE
    # ========================================================

    if stage == "No CKD":

        recommendations.append(
            "Continue healthy lifestyle habits and regular health monitoring."
        )

    elif stage == "Stage 1":

        recommendations.append(
            "Continue healthy lifestyle habits and follow recommended kidney health monitoring."
        )

    elif stage == "Stage 2":

        recommendations.append(
            "Maintain healthy lifestyle habits and follow regular kidney health monitoring."
        )

    elif stage == "Stage 3":

        recommendations.append(
            "Regular medical follow-up and individualized lifestyle guidance are important."
        )

    elif stage == "Stage 4":

        recommendations.append(
            "Regular specialist follow-up and individualized lifestyle guidance are important."
        )

    elif stage == "Stage 5":

        recommendations.append(
            "Specialist kidney care and an individualized treatment plan are important."
        )


    return recommendations