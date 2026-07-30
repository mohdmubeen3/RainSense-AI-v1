<div align="center">

# 🌧️ RainSense AI v1

### Intelligent Rainfall Prediction using Machine Learning & Live Weather Data

A Flask-powered Machine Learning web application that predicts the probability of rainfall using **real-time weather observations** retrieved from the **Open-Meteo API** and a trained **Random Forest Classifier**.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikitlearn)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?logo=numpy)
![Open-Meteo](https://img.shields.io/badge/Open--Meteo-Weather%20API-2E86DE)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

# 📖 Project Overview

RainSense AI v1 is an end-to-end Machine Learning web application that predicts the likelihood of rainfall using live weather observations.

The application allows users to enter any city name. It automatically retrieves the city's geographical coordinates, downloads recent weather observations from the Open-Meteo API, preprocesses the data, performs feature engineering, and generates a rainfall prediction using a trained Random Forest machine learning model.

Unlike static ML demonstrations that rely on manually entered datasets, RainSense AI combines **Machine Learning**, **API Integration**, **Data Preprocessing**, and **Flask Web Development** into a single interactive application.

The project was developed to demonstrate how a trained machine learning model can be integrated into a production-style web application capable of making predictions from live weather data.

---

# ✨ Key Features

- 🌍 Predict rainfall for any supported city worldwide
- 🌦️ Live weather data using the Open-Meteo API
- 🤖 Random Forest Machine Learning model
- 📊 Displays Rain and No-Rain probabilities
- ⚡ Automatic preprocessing and feature engineering
- 🎨 Responsive Glassmorphism user interface
- 📱 Mobile-friendly design
- 🚫 Graceful handling of invalid city names
- 🔄 Real-time prediction workflow
- 🧩 Modular Flask application structure

---

# 🎯 Problem Statement

Weather conditions change continuously, making rainfall prediction an important challenge for agriculture, transportation, outdoor planning, and disaster preparedness.

Traditional machine learning projects often demonstrate predictions using static CSV datasets. RainSense AI extends this idea by integrating live weather observations with a trained machine learning model, allowing users to generate predictions dynamically through a web interface.
---

# 📸 Application Preview

## 🏠 Home Page

The user enters a city name to retrieve live weather observations and generate a rainfall prediction.

---

## 🌧️ Prediction Result

After processing the weather observations, the application displays:

- Current Weather Information
- Rainfall Prediction
- Rain Probability
- No-Rain Probability
- 
---

# 🏗️ System Architecture

```
                     User
                       │
                       ▼
              Enter City Name
                       │
                       ▼
          Flask Web Application
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
Open-Meteo Geocoding API     Weather Archive API
        │                             │
        └──────────────┬──────────────┘
                       ▼
            Weather Data Retrieved
                       │
                       ▼
              Data Preprocessing
                       │
                       ▼
            Feature Engineering
                       │
                       ▼
      Random Forest Machine Learning Model
                       │
                       ▼
            Prediction & Probabilities
                       │
                       ▼
           Results Displayed to User
```

---

# ⚙️ Application Workflow

The application follows the workflow below:

### Step 1 – City Input

The user enters the name of a city.

↓

### Step 2 – Geocoding

The Open-Meteo Geocoding API converts the city name into geographical coordinates (latitude and longitude).

↓

### Step 3 – Weather Retrieval

Historical weather observations are retrieved automatically using the Open-Meteo Archive API.

↓

### Step 4 – Data Preprocessing

The raw API response is transformed into a structured dataset suitable for machine learning.

↓

### Step 5 – Feature Engineering

Relevant weather features are extracted and engineered before being passed to the prediction model.

↓

### Step 6 – Machine Learning Prediction

The trained Random Forest classifier predicts whether rainfall is likely.

↓

### Step 7 – Result Visualization

The prediction, confidence scores, and weather observations are displayed in a responsive web interface.

---

# 🧠 Machine Learning Pipeline

The prediction pipeline consists of the following stages:

```
Raw Weather Data
        │
        ▼
Data Cleaning
        │
        ▼
Feature Extraction
        │
        ▼
Feature Engineering
        │
        ▼
Feature Alignment
        │
        ▼
Random Forest Classifier
        │
        ▼
Rain / No Rain Prediction
        │
        ▼
Probability Estimation
```

The trained model predicts:

- 🌧️ Rain Tomorrow
- ☀️ No Rain Tomorrow

along with the probability of each outcome.

---

# 📂 Project Structure

```
RainSense-AI-v1
│
├── app.py                     # Flask application
├── prediction.py              # Model loading & prediction
├── requirement.txt            # Project dependencies
├── README.md
│
├── model/
│   ├── rainsense_rf_model.pkl
│   └── feature_columns.pkl
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   └── index.html
│
├── utils/
│   └── preprocessing.py
│
└── assets/
    ├── homepage.png
    └── prediction.png
```

---

# 🔍 Weather Parameters Used

The model utilizes weather-related observations including:

- 🌡 Temperature
- 💧 Relative Humidity
- 🌬 Wind Speed
- 🌧 Rainfall
- ☀ Sunshine Duration
- 🌫 Atmospheric Pressure
- ☁ Cloud Cover
- 🧭 Wind Direction
- 🌪 Wind Gust
- 🌦 Weather Code

These observations are processed into engineered features before being passed to the machine learning model for prediction.
