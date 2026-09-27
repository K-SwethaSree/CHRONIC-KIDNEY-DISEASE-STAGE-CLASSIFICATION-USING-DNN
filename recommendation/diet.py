def get_diet_recommendations(
    stage,
    food_preference,
    region,
    allergies,
    water_intake,
    high_salt
):

    recommendations = []


    # ========================================================
    # GENERAL
    # ========================================================

    recommendations.append(
        "Prefer balanced meals and limit highly processed foods."
    )


    # ========================================================
    # SALT
    # ========================================================

    if high_salt == "Yes":

        recommendations.append(
            "Consider reducing added salt and high-sodium processed foods."
        )


    # ========================================================
    # WATER
    # ========================================================

    # water_intake is a numeric value from Streamlit.
    # We consider less than 1 litre as low for this prototype.

    if water_intake < 1.0:

        recommendations.append(
            "Review your fluid intake with a healthcare professional, "
            "because appropriate fluid intake can vary between people "
            "with kidney disease."
        )


    # ========================================================
    # VEGETARIAN
    # ========================================================

    if food_preference == "Vegetarian":

        recommendations.append(
            "Choose a varied vegetarian diet with appropriate portions "
            "of grains, vegetables and other foods based on individual "
            "kidney health requirements."
        )


    # ========================================================
    # VEGAN
    # ========================================================

    elif food_preference == "Vegan":

        recommendations.append(
            "Maintain a varied plant-based diet while discussing "
            "protein, potassium and phosphorus requirements with "
            "a healthcare professional."
        )


    # ========================================================
    # NON-VEGETARIAN
    # ========================================================

    elif food_preference == "Non-Vegetarian":

        recommendations.append(
            "Choose balanced portions of protein foods and discuss "
            "the appropriate protein amount with a healthcare professional."
        )


    # ========================================================
    # REGION
    # ========================================================

    if region == "South India":

        recommendations.append(
            "For South Indian meals, consider balanced portions of "
            "rice or other grains, vegetables and suitable protein "
            "sources while controlling added salt."
        )

    elif region == "North India":

        recommendations.append(
            "For North Indian meals, consider balanced portions of "
            "roti or rice, vegetables and suitable protein sources "
            "while controlling added salt."
        )

    elif region == "East India":

        recommendations.append(
            "For East Indian meals, consider balanced portions of "
            "rice, vegetables and suitable protein sources while "
            "controlling added salt."
        )

    elif region == "West India":

        recommendations.append(
            "For West Indian meals, consider balanced portions of "
            "grains, vegetables and suitable protein sources while "
            "controlling added salt."
        )

    elif region == "Northeast India":

        recommendations.append(
            "For Northeast Indian meals, choose balanced portions "
            "of grains, vegetables and suitable protein sources "
            "while controlling added salt."
        )


    # ========================================================
    # ALLERGIES
    # ========================================================

    if allergies.strip():

        recommendations.append(
            f"Avoid foods that contain your reported allergens: "
            f"{allergies}."
        )


    # ========================================================
    # CKD STAGE
    # ========================================================

    if stage in [
        "Stage 3",
        "Stage 4",
        "Stage 5"
    ]:

        recommendations.append(
            "For advanced CKD, dietary requirements can depend on "
            "laboratory results and treatment. Consult a qualified "
            "renal dietitian or healthcare professional for an "
            "individualized plan."
        )


    # ========================================================
    # RETURN
    # ========================================================

    return recommendations