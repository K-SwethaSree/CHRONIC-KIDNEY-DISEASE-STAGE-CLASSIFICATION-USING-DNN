# Chronic Kidney Disease Stage Classification Using DNN

### An AI-Assisted Kidney Health Support System

A web-based application that uses a Deep Neural Network (DNN) model to classify Chronic Kidney Disease (CKD) stages from selected medical and lifestyle inputs. Along with prediction, the system provides risk-factor analysis, personalized diet and lifestyle recommendations, multilingual support, and nearby kidney-care hospital information.

## 📌 Project Overview

Chronic Kidney Disease requires monitoring of different health parameters and lifestyle factors. This project provides a simple web interface where users can enter relevant medical, blood, urine, lifestyle, food, and hydration information and receive a CKD stage prediction.

The system is designed not only to provide a prediction, but also to give supporting information based on the entered values. It includes risk-factor analysis, personalized recommendations, multilingual support, and a hospital section for finding nearby kidney-care facilities.

## 🎯 Objectives

* Classify CKD stages using a DNN-based model
* Accept relevant medical and lifestyle information from the user
* Display the predicted CKD stage and stage probabilities
* Analyze selected risk factors from the entered information
* Provide personalized diet recommendations
* Provide lifestyle recommendations based on user preferences
* Support multiple languages
* Help users find nearby kidney-care hospitals
* Display hospital locations on a map

## 🔄 System Workflow

```text
User Medical & Lifestyle Inputs
              ↓
       Data Preprocessing
              ↓
        DNN Prediction Model
              ↓
       CKD Stage Prediction
              ↓
     ┌────────┼──────────┐
     ↓        ↓          ↓
Risk Factor  Diet      Lifestyle
  Analysis  Recommendations
              ↓
     Nearby Kidney Hospitals
              ↓
       Map & Hospital Details
```

## 🧠 CKD Stage Classification

The application collects the required input values and passes the processed information to the trained DNN model.

The prediction section displays:

* Predicted CKD stage
* Prediction confidence
* Stage-wise probability values

This allows the user to see both the predicted stage and how the model's probabilities are distributed across the different stages.

## 🩺 Medical and Lifestyle Inputs

The application accepts information from different categories.

### Kidney Function Parameters

* GFR
* Serum Creatinine
* BUN
* Calcium
* Other kidney-related parameters

### Blood and Urine Information

* ANA
* C3/C4
* Hematuria
* Oxalate
* Urine pH
* Blood pressure

### Lifestyle Information

* Physical activity level
* Preferred activity
* Smoking
* Alcohol consumption

### Food and Hydration

* Food preference
* Water intake
* Salt intake
* Food allergies

The entered information is used for CKD prediction and for generating relevant recommendations.

## 📊 Risk Factor Analysis

After the prediction, the application analyzes selected input values and identifies possible risk factors.

This section helps the user understand which of the entered health or lifestyle parameters may require attention.

## 🥗 Personalized Recommendations

The system provides recommendations based on the user's entered information rather than displaying exactly the same recommendations for every user.

### Diet Recommendations

The diet section considers factors such as:

* Food preference
* Water intake
* Salt intake
* Food allergies
* CKD stage

The recommendations are adjusted according to the available user information.

### Lifestyle Recommendations

Lifestyle recommendations are also based on the user's selected activity preference.

The application supports activities such as:

* Walking
* Yoga
* Exercise
* Cycling

## 🌐 Multilingual Support

The application provides a multilingual interface so that users can interact with the system in different supported languages.

The translated interface includes application text and recommendation-related content.

## 🏥 Nearby Kidney-Care Hospitals

The application includes a hospital-support section for finding kidney-care hospitals.

Users can select:

```text
State
  ↓
City
  ↓
Area
```

Based on the selected location, available hospital information is displayed.

The hospital section provides details such as:

* Hospital name
* Area
* City
* State
* Hospital type
* Address

Hospital locations are also displayed on a map, and users can open the selected location through Google Maps.

## 🗺️ Hospital Location Flow

```text
Select State
     ↓
Select City
     ↓
Select Area
     ↓
Display Hospitals
     ↓
View Hospital on Map
     ↓
Open Location in Google Maps
```

The hospital information is maintained using project data rather than requiring a location API key.

## 🖥️ Application Features

The current application includes:

* CKD stage prediction
* Prediction confidence
* Stage probability visualization
* Risk-factor analysis
* Personalized diet recommendations
* Personalized lifestyle recommendations
* Food and hydration-based guidance
* Activity-based recommendations
* Multilingual support
* State, city and area based hospital selection
* Hospital information display
* Hospital map visualization
* Google Maps navigation

## 🎥 Project Demo

[▶️ Watch the CKD Project Demo] (https://drive.google.com/file/d/1oWLtebL9GH9N_6vS6sEa38YORPVGCb3o/view?usp=sharing)

## 🛠️ Technologies Used

### Programming Language

* Python

### Machine Learning

* TensorFlow / Keras
* NumPy
* Pandas
* Scikit-learn

### Web Application

* Streamlit

### Development Tools

* Jupyter Notebook
* Visual Studio Code
* Git
* GitHub

## 📂 Project Structure

```text
CKD/
│
├── app.py
├── prediction.py
├── train_model.py
├── test_prediction.py
├── chronic_Disease.ipynb
├── requirements.txt
│
├── data/
│
├── models/
│
├── language/
│
├── location/
│
├── recommendation/
│
├── demo/
│   └── CKD_Project_Demo.mp4
│
├── .streamlit/
│
├── .gitignore
└── README.md
```

## 📈 Project Output

The application produces a CKD stage prediction based on the entered values and displays the corresponding stage probabilities.

In addition to the prediction, the application provides:

* Risk-factor information
* Diet recommendations
* Lifestyle recommendations
* Multilingual content
* Nearby hospital information
* Hospital map visualization

## 🚀 Future Scope

The project can be further improved by:

* Training with larger and more diverse datasets
* Improving model performance through further experimentation
* Adding more regional languages
* Expanding personalized recommendation logic
* Adding more healthcare facilities and location information
* Adding model explainability features
* Improving the visualization of prediction results
* Integrating additional healthcare resources
