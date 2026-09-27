import os
import requests
import streamlit as st


# ============================================================
# GEOAPIFY API
# ============================================================

GEOCODING_URL = (
    "https://api.geoapify.com/v1/geocode/search"
)

PLACES_URL = (
    "https://api.geoapify.com/v2/places"
)


# ============================================================
# GET API KEY
# ============================================================

def get_geoapify_api_key():

    # --------------------------------------------------------
    # Streamlit secrets
    # --------------------------------------------------------

    try:

        key = st.secrets.get(
            "GEOAPIFY_API_KEY",
            ""
        )

        if key:

            return str(key).strip()

    except Exception:

        pass


    # --------------------------------------------------------
    # Environment variable fallback
    # --------------------------------------------------------

    key = os.getenv(
        "GEOAPIFY_API_KEY",
        ""
    )

    return str(key).strip()


# ============================================================
# CHECK API
# ============================================================

def geoapify_available():

    return bool(
        get_geoapify_api_key()
    )


# ============================================================
# GEOCODE LOCATION
# ============================================================

def geocode_location(
    state,
    city,
    area="All Areas"
):

    api_key = get_geoapify_api_key()


    if not api_key:

        return None


    # --------------------------------------------------------
    # Build search text
    # --------------------------------------------------------

    if area and area != "All Areas":

        search_text = (
            f"{area}, "
            f"{city}, "
            f"{state}, "
            f"India"
        )

    else:

        search_text = (
            f"{city}, "
            f"{state}, "
            f"India"
        )


    params = {

        "text":
            search_text,

        "apiKey":
            api_key,

        "limit":
            1
    }


    try:

        response = requests.get(
            GEOCODING_URL,
            params=params,
            timeout=15
        )


        response.raise_for_status()


        data = response.json()


    except (
        requests.RequestException,
        ValueError
    ):

        return None


    features = data.get(
        "features",
        []
    )


    if not features:

        return None


    feature = features[0]


    geometry = feature.get(
        "geometry",
        {}
    )


    coordinates = geometry.get(
        "coordinates",
        []
    )


    if len(coordinates) < 2:

        return None


    try:

        longitude = float(
            coordinates[0]
        )

        latitude = float(
            coordinates[1]
        )

    except (
        TypeError,
        ValueError
    ):

        return None


    if not (
        -90 <= latitude <= 90
        and
        -180 <= longitude <= 180
    ):

        return None


    return {
        "latitude":
            latitude,

        "longitude":
            longitude
    }


# ============================================================
# SEARCH HOSPITALS
# ============================================================

def search_nearby_hospitals(
    state,
    city,
    area="All Areas",
    radius=10000,
    limit=20
):

    api_key = get_geoapify_api_key()


    if not api_key:

        return []


    # ========================================================
    # FIRST GET LOCATION COORDINATES
    # ========================================================

    location = geocode_location(
        state,
        city,
        area
    )


    if not location:

        return []


    latitude = location["latitude"]

    longitude = location["longitude"]


    # ========================================================
    # GEOAPIFY PLACE SEARCH
    # ========================================================

    params = {

        "categories":
            "healthcare.hospital",

        "filter":
            (
                f"circle:"
                f"{longitude},"
                f"{latitude},"
                f"{radius}"
            ),

        "bias":
            (
                f"proximity:"
                f"{longitude},"
                f"{latitude}"
            ),

        "limit":
            limit,

        "apiKey":
            api_key
    }


    try:

        response = requests.get(
            PLACES_URL,
            params=params,
            timeout=15
        )


        response.raise_for_status()


        data = response.json()


    except (
        requests.RequestException,
        ValueError
    ):

        return []


    features = data.get(
        "features",
        []
    )


    hospitals = []


    # ========================================================
    # CONVERT RESULTS
    # ========================================================

    for feature in features:

        properties = feature.get(
            "properties",
            {}
        )


        geometry = feature.get(
            "geometry",
            {}
        )


        coordinates = geometry.get(
            "coordinates",
            []
        )


        if len(coordinates) < 2:

            continue


        try:

            hospital_longitude = float(
                coordinates[0]
            )

            hospital_latitude = float(
                coordinates[1]
            )

        except (
            TypeError,
            ValueError
        ):

            continue


        if not (
            -90 <= hospital_latitude <= 90
            and
            -180 <= hospital_longitude <= 180
        ):

            continue


        # ----------------------------------------------------
        # Name
        # ----------------------------------------------------

        name = (

            properties.get(
                "name"
            )

            or properties.get(
                "address_line1"
            )

            or "Hospital"
        )


        # ----------------------------------------------------
        # Address
        # ----------------------------------------------------

        address = (

            properties.get(
                "formatted"
            )

            or ""
        )


        # ----------------------------------------------------
        # Area
        # ----------------------------------------------------

        hospital_area = (

            properties.get(
                "suburb"
            )

            or properties.get(
                "district"
            )

            or properties.get(
                "quarter"
            )

            or area
        )


        if hospital_area == "All Areas":

            hospital_area = (
                properties.get(
                    "city_district"
                )
                or city
            )


        # ----------------------------------------------------
        # City
        # ----------------------------------------------------

        hospital_city = (

            properties.get(
                "city"
            )

            or properties.get(
                "municipality"
            )

            or properties.get(
                "town"
            )

            or city
        )


        # ----------------------------------------------------
        # State
        # ----------------------------------------------------

        hospital_state = (

            properties.get(
                "state"
            )

            or state
        )


        # ====================================================
        # STANDARD HOSPITAL FORMAT
        # ====================================================

        hospitals.append({

            "name":
                name,

            "state":
                hospital_state,

            "city":
                hospital_city,

            "area":
                hospital_area,

            "address":
                address,

            "latitude":
                hospital_latitude,

            "longitude":
                hospital_longitude,

            "type":
                "Hospital / Healthcare"
        })


    return hospitals