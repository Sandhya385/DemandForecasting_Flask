# 📈 Demand Forecasting with Flask API & Power BI

## 🔹 Project Overview
This project predicts **future demand** for a single product based on **3.5 years of historical sales data**.  
The forecasting is performed using **SARIMAX** and **XGBoost**, deployed via a **Flask API** on Render,  
and visualized with an **interactive Power BI dashboard**.

The goal is to provide accurate short-term demand forecasts for decision-making in supply chain and inventory management.

---

## 🔹 Features
- ⏳ **Time Series Forecasting** using SARIMAX & XGBoost
- 🌐 **Flask API Deployment** (hosted on Render)
- 📊 **Interactive Power BI Dashboard**
- ✅ **Model Evaluation** with RMSE & MAE
- 📂 **Simulation Mode** for hypothetical scenarios

---

## 🔹 Dataset
- **Source**: Synthetic dataset generated for demo purposes
- **Duration**: 3.5 years of daily sales
 
---

## 🔹 Project Workflow
1. **Data Preprocessing** – Clean and prepare the dataset.
2. **Model Training** – Train SARIMAX and XGBoost models.
3. **Forecasting** – Predict demand for the next 7 days.
4. **Deployment** – Deploy the Flask API on Render.
5. **Visualization** – Build Power BI dashboard for results.

---

## 🔹 Flask API
The API is hosted at:  
**https://demandforecasting-flask-1.onrender.com/**

---
## 🔹 Screenshots ##
-Power BI Dashboard (screenshots/powerbi_dashboard.PNG)
-Flask API UI (screenshots/flask_API_UI.PNG)
-7day forecast (screenshots/forecast.PNG)
-Single record simulation (screenshots/Simulation_Singlerecord.PNG)

### 🔹Forecast Accuracy -
- **SARIMAX**: RMSE = 20.09, MAE = 17.22 
- **XGBoost**: RMSE = 7.78, MAE = 6.1

---
  
### 🔹API Endpoint
`/forecast`

---

**Example Local URL:**  
'http://127.0.0.1:5000/forecast'

## 🔹 Technologies Used

-Python (Pandas, NumPy, Scikit-learn, Statsmodels, XGBoost)
-Flask (for API deployment)
-Power BI (for visualization)
-Render (for hosting)
-Matplotlib / Seaborn (for plots)



