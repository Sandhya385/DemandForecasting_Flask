# 📈 Demand Forecasting with Flask API & Power BI

## 🔹 Project Overview
This project predicts **future demand** for a single product using **3.5 years of historical sales data**.
The forecasting is performed using **SARIMAX** (statistical approach) and **XGBoost**(machine learning approach).

The project includes:
-A **Flask API** deployed on Render for real-time forecasting
-An **interactive Power BI dashboard** for visualization and insights
-Simulation capabilities to test hypothetical demand scenarios

---

## 🔹 Features
- ⏳ **Time Series Forecasting** using SARIMAX & XGBoost
- 🌐 **Flask API Deployment** (hosted on Render)
- 📊 **Interactive Power BI Dashboard**
- ✅ **Model Evaluation** with RMSE & MAE
- 🎯 **7-Day Rolling Forecast** 
- 🧪 **Simulation Mode** for “what-if” scenarios
- 📂 **Daily Forecast Updates** possible via API

---

## 🔹 Dataset
- **Source**: Synthetic dataset generated for demo purposes
- **Duration**: 3.5 years of daily sales
 
---

## 🔹 Project Workflow
1. **Data Preprocessing** – Cleaning, formatting dates, handling missing values.
2. **Feature Engineering** – Adding time-based features, lags, and rolling means
3. **Model Training** – SARIMAX for trend/seasonality & XGBoost for patterns in features
4. **Model Evaluation** – RMSE and MAE calculated for both models
5. **Forecasting** – Generating 7-day forecast results
6. **API Development** – Building /forecast endpoint in Flask
7. **Deployment** – Hosting Flask API on Render
8. **Visualization** – Connecting API results to Power BI dashboard

---

## 🔹 Flask API 
**Live API URL**
🔗 https://demandforecasting-flask-1.onrender.com/

---
## 🔹 Screenshots

| Feature                       | Screenshot |
|--------------------------------|------------|
| **Power BI Dashboard**         | ![Power BI Dashboard](screenshots/powerbi_dashboard.PNG) |
| **Flask API UI**                | ![Flask API UI](screenshots/flask_API_UI.PNG) |
| **7-Day Forecast**              | ![7-Day Forecast](screenshots/forecast.PNG) |
| **Single Record Simulation**    | ![Single Record Simulation](screenshots/Simulation_Singlerecord.PNG) |

---

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

## 🔹 DemandForecasting_Flask

│── app.py                  # Flask API script
│── requirements.txt        # Python dependencies
│── predictions.ipynb       # Historical dataset
│── runtime.txt             # Python version
│── xgb_model.pkl           # Trained XGBoost model
|── DemandForecasting.pbix  # PowerBI
│── templates/
│    └── index.html         # API UI template
     └── forecast.html      # 7 days forecast
     └── simulate.html      # Predicted value for single entry
      
│── screenshots/
│    ├── powerbi_dashboard.PNG
│    ├── flask_API_UI.PNG
│    ├── forecast.PNG
│    └── Simulation_Singlerecord.PNG
│── README.md



### 🔹How to Run Locally
# 1. Clone repo
git clone https://github.com/username/demand_forecasting.git
cd demand_forecasting

# 2. Install dependencies
pip install -r requirements.txt

# 3. Flask API
python app.py

# 4. Access API
http://127.0.0.1:5000/forecast





