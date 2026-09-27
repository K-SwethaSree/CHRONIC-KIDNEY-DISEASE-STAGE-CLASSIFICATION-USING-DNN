import streamlit as st
import pandas as pd
from urllib.parse import quote

from prediction import predict_ckd

from recommendation.risk_factors import (
    analyze_risk_factors
)

from recommendation.diet import (
    get_diet_recommendations
)

from recommendation.lifestyle import (
    get_lifestyle_recommendations
)

from language.translations import (
    get_translation,
    get_recommendation_translation
)

from location.hospital_data import (
    get_states,
    get_cities,
    get_areas,
    get_hospitals
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CKD Health Support System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# IMPORTANT: THIS MUST COME BEFORE t(), rec(), etc.
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "English"

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None


# ============================================================
# LIGHT PROFESSIONAL UI
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F8FAFC;
    }

    section[data-testid="stSidebar"] {
        background-color: #EEF6F7;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        color: #0F4C5C;
    }

    h2 {
        color: #155E75;
    }

    h3 {
        color: #164E63;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #D9E2EC;
        border-radius: 14px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    }

    div[data-testid="stMetricValue"] {
        color: #0F4C5C;
    }

    .footer {
        text-align: center;
        color: #64748B;
        font-size: 13px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LANGUAGES
# ============================================================

LANGUAGES = [
    "English",
    "Telugu",
    "Hindi"
]


# ============================================================
# TRANSLATION HELPERS
# ============================================================

def t(key):
    """
    Translate normal UI text using the currently selected language.
    """
    return get_translation(
        st.session_state.language,
        key
    )


def rec(text):
    """
    Translate recommendation text using the currently selected language.
    """
    return get_recommendation_translation(
        st.session_state.language,
        text
    )


def option_text(value):
    """
    Translate selectbox option text.
    """
    return get_translation(
        st.session_state.language,
        value
    )


def original_from_display(display_value, options):
    """
    Convert translated selectbox value back to original English value.
    """

    for option in options:

        if option_text(option) == display_value:
            return option

    return display_value


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🩺 " +
        get_translation(
            "English",
            "app_title"
        )
    )

    selected_language = st.selectbox(
        "🌐 Select Language",
        LANGUAGES,
        index=LANGUAGES.index(
            st.session_state.language
        ),
        key="language_selector"
    )

    # Synchronize selected language with session state
    st.session_state.language = selected_language

    st.divider()


# ============================================================
# HEADER
# ============================================================

st.title(
    "🩺 " +
    t("app_title")
)

st.subheader(
    t("subtitle")
)


# ============================================================
# MEDICAL DISCLAIMER
# ============================================================

st.info(
    "⚕️ " +
    t("Important medical disclaimer")
)


# ============================================================
# MEDICAL INFORMATION
# ============================================================

st.header(
    "🧪 " +
    t("Medical Information")
)


# ============================================================
# KIDNEY FUNCTION
# ============================================================

st.subheader(
    "🩺 " +
    t("Kidney Function Parameters")
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    gfr = st.number_input(
        t("GFR"),
        min_value=0.0,
        max_value=200.0,
        value=60.0,
        step=1.0
    )


with col2:

    serum_creatinine = st.number_input(
        t("Serum Creatinine"),
        min_value=0.0,
        max_value=20.0,
        value=1.0,
        step=0.1
    )


with col3:

    bun = st.number_input(
        t("BUN"),
        min_value=0.0,
        max_value=200.0,
        value=20.0,
        step=1.0
    )


with col4:

    serum_calcium = st.number_input(
        t("Serum Calcium"),
        min_value=0.0,
        max_value=20.0,
        value=9.0,
        step=0.1
    )


# ============================================================
# BLOOD / URINE
# ============================================================

st.subheader(
    "🧪 " +
    t("Blood & Urine Information")
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    ana = st.selectbox(
        t("ANA"),
        [0, 1]
    )


with col2:

    c3_c4 = st.selectbox(
        t("C3/C4"),
        [0, 1]
    )


with col3:

    hematuria = st.selectbox(
        t("Hematuria"),
        [0, 1]
    )


with col4:

    oxalate_levels = st.number_input(
        t("Oxalate Levels"),
        min_value=0.0,
        max_value=200.0,
        value=30.0,
        step=1.0
    )


col1, col2 = st.columns(2)


with col1:

    urine_ph = st.number_input(
        t("Urine pH"),
        min_value=0.0,
        max_value=14.0,
        value=6.0,
        step=0.1
    )


with col2:

    blood_pressure = st.number_input(
        t("Blood Pressure"),
        min_value=0.0,
        max_value=300.0,
        value=120.0,
        step=1.0
    )


# ============================================================
# LIFESTYLE
# ============================================================

st.header(
    "🏃 " +
    t("Lifestyle Information")
)


ACTIVITY_LEVELS = [
    "Low",
    "Moderate",
    "High"
]

PREFERRED_ACTIVITIES = [
    "Walking",
    "Yoga",
    "Exercise",
    "Cycling",
    "None"
]

YES_NO = [
    "Yes",
    "No"
]


col1, col2, col3, col4 = st.columns(4)


with col1:

    activity_display = st.selectbox(
        t("Activity Level"),
        [
            option_text(x)
            for x in ACTIVITY_LEVELS
        ],
        key="activity_level_selector"
    )

    activity_level = original_from_display(
        activity_display,
        ACTIVITY_LEVELS
    )


with col2:

    preferred_display = st.selectbox(
        t("Preferred Activity"),
        [
            option_text(x)
            for x in PREFERRED_ACTIVITIES
        ],
        key="preferred_activity_selector"
    )

    preferred_activity = original_from_display(
        preferred_display,
        PREFERRED_ACTIVITIES
    )


with col3:

    smoking_display = st.selectbox(
        t("Smoking"),
        [
            option_text(x)
            for x in YES_NO
        ],
        index=1,
        key="smoking_selector"
    )

    smoking = original_from_display(
        smoking_display,
        YES_NO
    )


with col4:

    alcohol_display = st.selectbox(
        t("Alcohol"),
        [
            option_text(x)
            for x in YES_NO
        ],
        index=1,
        key="alcohol_selector"
    )

    alcohol = original_from_display(
        alcohol_display,
        YES_NO
    )


# ============================================================
# FOOD
# ============================================================

st.header(
    "🥗 " +
    t("Food Preference")
)


FOOD_PREFERENCES = [
    "Vegetarian",
    "Non-Vegetarian",
    "Vegan"
]


REGIONS = [
    "South India",
    "North India",
    "East India",
    "West India",
    "Northeast India"
]


col1, col2, col3 = st.columns(3)


with col1:

    food_display = st.selectbox(
        t("Food Preference"),
        [
            option_text(x)
            for x in FOOD_PREFERENCES
        ],
        key="food_preference_selector"
    )

    food_preference = original_from_display(
        food_display,
        FOOD_PREFERENCES
    )


with col2:

    region_display = st.selectbox(
        t("Region"),
        [
            option_text(x)
            for x in REGIONS
        ],
        key="region_selector"
    )

    region = original_from_display(
        region_display,
        REGIONS
    )


with col3:

    allergies = st.text_input(
        t("Allergies"),
        placeholder=t(
            "Example: Milk, peanuts"
        )
    )


col1, col2 = st.columns(2)


with col1:

    water_intake = st.number_input(
        t("Daily Water Intake (Litres)"),
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.1
    )


with col2:

    salt_display = st.selectbox(
        t("High Salt Intake"),
        [
            option_text(x)
            for x in YES_NO
        ],
        index=1,
        key="salt_selector"
    )

    high_salt = original_from_display(
        salt_display,
        YES_NO
    )


# ============================================================
# PREDICT
# ============================================================

st.divider()

predict_button = st.button(
    "🔍 " +
    t("Predict CKD Stage"),
    type="primary",
    use_container_width=True,
    key="predict_button"
)


# ============================================================
# RUN PREDICTION
# ============================================================

if predict_button:

    patient = {

        "gfr": gfr,

        "serum_creatinine":
            serum_creatinine,

        "bun":
            bun,

        "serum_calcium":
            serum_calcium,

        "ana":
            ana,

        "c3_c4":
            c3_c4,

        "hematuria":
            hematuria,

        "oxalate_levels":
            oxalate_levels,

        "urine_ph":
            urine_ph,

        "blood_pressure":
            blood_pressure
    }


    try:

        result = predict_ckd(
            patient
        )

        st.session_state.prediction_result = result

    except Exception as e:

        st.error(
            t("Prediction could not be completed.")
        )

        st.exception(e)

        st.stop()


# ============================================================
# SHOW SAVED PREDICTION
# ============================================================

result = st.session_state.prediction_result


if result is not None:

    stage = result["stage"]

    confidence = result["confidence"]


    # ========================================================
    # RESULT
    # ========================================================

    st.header(
        "📊 " +
        t("Prediction Result")
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            t("Predicted Stage"),
            t(stage)
        )


    with col2:

        st.metric(
            t("Confidence"),
            f"{confidence:.2f}%"
        )


    # ========================================================
    # STAGE PROBABILITIES
    # ========================================================

    st.subheader(
        "📈 " +
        t("Stage Probabilities")
    )


    for stage_name, probability in result[
        "probabilities"
    ].items():

        st.write(
            f"**{t(stage_name)}: "
            f"{probability:.2f}%**"
        )

        st.progress(
            min(
                max(
                    float(probability) / 100,
                    0
                ),
                1
            )
        )


    # ========================================================
    # RISK FACTORS
    # ========================================================

    st.header(
        "⚠️ " +
        t("Risk Factors")
    )


    try:

        risk_results = analyze_risk_factors(
            gfr=gfr,
            serum_creatinine=serum_creatinine,
            bun=bun,
            blood_pressure=blood_pressure,
            hematuria=hematuria
        )


        if not risk_results:

            risk_results = [
                "No major risk factors were identified from the entered values."
            ]


        for risk in risk_results:

            st.write(
                "• " +
                rec(str(risk))
            )


    except Exception as e:

        st.error(
            "Risk analysis error: " +
            str(e)
        )


    # ========================================================
    # DIET RECOMMENDATIONS
    # ========================================================

    st.header(
        "🥗 " +
        t("Diet Recommendations")
    )


    try:

        diet_results = get_diet_recommendations(

            stage,

            food_preference,

            region,

            allergies,

            water_intake,

            high_salt
        )


        for recommendation in diet_results:

            st.write(
                "• " +
                rec(str(recommendation))
            )


        # ----------------------------------------------------
        # WATER GUIDANCE
        # ----------------------------------------------------

        if water_intake < 1.0:

            if st.session_state.language == "Telugu":

                st.write(
                    "• మీరు తీసుకుంటున్న నీటి పరిమాణం తక్కువగా "
                    "ఉండవచ్చు. మీ కిడ్నీ పరిస్థితిని బట్టి "
                    "సరైన ద్రవ పరిమాణం కోసం ఆరోగ్య నిపుణుడిని "
                    "సంప్రదించండి."
                )

            elif st.session_state.language == "Hindi":

                st.write(
                    "• आपका पानी का सेवन कम हो सकता है। "
                    "अपनी किडनी की स्थिति के अनुसार उचित "
                    "तरल मात्रा के लिए स्वास्थ्य विशेषज्ञ "
                    "से सलाह लें।"
                )

            else:

                st.write(
                    "• Your reported water intake is relatively "
                    "low. Discuss appropriate fluid intake with "
                    "a healthcare professional based on your "
                    "kidney condition."
                )


        elif water_intake > 5.0:

            if st.session_state.language == "Telugu":

                st.write(
                    "• మీరు నివేదించిన నీటి తీసుకునే పరిమాణం "
                    "చాలా ఎక్కువగా ఉండవచ్చు. మీ వ్యక్తిగత "
                    "కిడ్నీ పరిస్థితికి సరైన ద్రవ పరిమాణాన్ని "
                    "ఆరోగ్య నిపుణుడితో చర్చించండి."
                )

            elif st.session_state.language == "Hindi":

                st.write(
                    "• आपका बताया गया पानी का सेवन अधिक हो "
                    "सकता है। अपनी व्यक्तिगत किडनी स्थिति के "
                    "अनुसार उचित तरल मात्रा के बारे में "
                    "स्वास्थ्य विशेषज्ञ से चर्चा करें।"
                )

            else:

                st.write(
                    "• Your reported water intake is relatively "
                    "high. Discuss the appropriate fluid amount "
                    "for your individual kidney condition with "
                    "a healthcare professional."
                )


    except Exception as e:

        st.error(
            "Diet recommendation error: " +
            str(e)
        )


    # ========================================================
    # LIFESTYLE
    # ========================================================

    st.header(
        "🏃 " +
        t("Lifestyle Recommendations")
    )


    try:

        lifestyle_results = (
            get_lifestyle_recommendations(

                stage,

                activity_level,

                preferred_activity,

                smoking,

                alcohol
            )
        )


        for recommendation in lifestyle_results:

            st.write(
                "• " +
                rec(str(recommendation))
            )


        # ----------------------------------------------------
        # PERSONALIZED ACTIVITY GUIDANCE
        # ----------------------------------------------------

        if preferred_activity == "Yoga":

            if st.session_state.language == "Telugu":

                st.write(
                    "• మీకు యోగ ఇష్టమైతే, మీ శారీరక సామర్థ్యానికి "
                    "అనుగుణంగా తేలికపాటి యోగను పరిగణించండి."
                )

            elif st.session_state.language == "Hindi":

                st.write(
                    "• यदि आपको योग पसंद है, तो अपनी शारीरिक "
                    "क्षमता के अनुसार हल्के योग अभ्यास पर विचार करें।"
                )

            else:

                st.write(
                    "• Since you prefer yoga, consider gentle "
                    "yoga practices appropriate for your physical "
                    "ability."
                )


        elif preferred_activity == "Cycling":

            if st.session_state.language == "Telugu":

                st.write(
                    "• సైక్లింగ్ మీకు ఇష్టమైన కార్యకలాపమైతే, "
                    "మీ సామర్థ్యానికి అనుగుణంగా మితమైన సైక్లింగ్ "
                    "చేయడాన్ని పరిగణించండి."
                )

            elif st.session_state.language == "Hindi":

                st.write(
                    "• यदि आपको साइकिल चलाना पसंद है, तो अपनी "
                    "क्षमता के अनुसार मध्यम स्तर की साइकिलिंग पर विचार करें।"
                )

            else:

                st.write(
                    "• Since you prefer cycling, consider moderate "
                    "cycling according to your physical ability."
                )


        elif preferred_activity == "Walking":

            if st.session_state.language == "Telugu":

                st.write(
                    "• మీకు నడక ఇష్టమైతే, మీ ఆరోగ్య నిపుణుడి "
                    "సలహా ప్రకారం క్రమంగా నడకను కొనసాగించండి."
                )

            elif st.session_state.language == "Hindi":

                st.write(
                    "• यदि आपको पैदल चलना पसंद है, तो अपने "
                    "स्वास्थ्य विशेषज्ञ की सलाह के अनुसार नियमित "
                    "रूप से पैदल चलना जारी रखें."
                )

            else:

                st.write(
                    "• Since you prefer walking, continue regular "
                    "walking gradually according to your healthcare "
                    "professional's advice."
                )


    except Exception as e:

        st.error(
            "Lifestyle recommendation error: " +
            str(e)
        )


# ============================================================
# NEARBY KIDNEY CARE HOSPITALS
# ============================================================

st.divider()

st.header(
    "🏥 " +
    t("Nearby Kidney Care Hospitals")
)


if st.session_state.language == "Telugu":

    st.info(
        "మీ రాష్ట్రం, నగరం మరియు ప్రాంతాన్ని ఎంచుకుని "
        "కిడ్నీ / నెఫ్రాలజీ ఆసుపత్రులను చూడండి."
    )

elif st.session_state.language == "Hindi":

    st.info(
        "अपने राज्य, शहर और क्षेत्र का चयन करके "
        "किडनी / नेफ्रोलॉजी अस्पताल देखें."
    )

else:

    st.info(
        "Select your state, city and area to view "
        "available kidney/nephrology hospitals."
    )


# ============================================================
# LOCATION
# ============================================================

states = get_states()


if states:

    selected_state = st.selectbox(
        t("State"),
        states,
        key="hospital_state"
    )


    cities = get_cities(
        selected_state
    )


    if cities:

        selected_city = st.selectbox(
            t("City"),
            cities,
            key="hospital_city"
        )


        areas = get_areas(
            selected_state,
            selected_city
        )


        area_options = [
            "All Areas"
        ] + areas


        selected_area = st.selectbox(
            t("Area"),
            area_options,
            key="hospital_area"
        )


        # ====================================================
        # GET HOSPITALS
        # ====================================================

        hospitals = get_hospitals(
            selected_state,
            selected_city,
            selected_area
        )


        if hospitals:

            # =================================================
            # MAP
            # =================================================

            st.subheader(
                "📍 " +
                t("Hospital Locations")
            )


            map_data = pd.DataFrame(
                [
                    {
                        "latitude": hospital["latitude"],
                        "longitude": hospital["longitude"]
                    }

                    for hospital in hospitals

                    if hospital.get("latitude") is not None
                    and hospital.get("longitude") is not None
                ]
            )


            if not map_data.empty:

                st.map(
                    map_data,
                    use_container_width=True
                )


            # =================================================
            # HOSPITAL CARDS
            # =================================================

            st.subheader(
                "🏥 " +
                t("Available Kidney Care Hospitals")
            )


            for hospital in hospitals:

                with st.container(
                    border=True
                ):

                    st.subheader(
                        "🏥 " +
                        hospital["name"]
                    )


                    st.write(
                        f"**{t('Area')}:** "
                        f"{hospital['area']}"
                    )


                    st.write(
                        f"**{t('City')}:** "
                        f"{hospital['city']}"
                    )


                    st.write(
                        f"**{t('State')}:** "
                        f"{hospital['state']}"
                    )


                    st.write(
                        f"**{t('Service')}:** "
                        f"{hospital['type']}"
                    )


                    if hospital.get("address"):

                        st.write(
                            f"**{t('Address')}:** "
                            f"{hospital['address']}"
                        )


                    # -----------------------------------------
                    # GOOGLE MAPS LINK
                    # -----------------------------------------

                    search_text = (
                        f"{hospital['name']}, "
                        f"{hospital['area']}, "
                        f"{hospital['city']}, "
                        f"{hospital['state']}"
                    )


                    google_maps_url = (
                        "https://www.google.com/maps/search/"
                        "?api=1&query="
                        + quote(search_text)
                    )


                    st.link_button(
                        "📍 " +
                        t(
                            "Open Location in Google Maps"
                        ),
                        google_maps_url
                    )


        else:

            st.info(
                t(
                    "No hospitals found for the selected location."
                )
            )


    else:

        st.info(
            t(
                "No cities are available for this state."
            )
        )


else:

    st.info(
        t(
            "No hospital location data is currently available."
        )
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    f"""
    <div class="footer">

    <strong>
    🩺 {t("footer")}
    </strong>

    <br><br>

    {t("footer_note")}

    </div>
    """,
    unsafe_allow_html=True
)