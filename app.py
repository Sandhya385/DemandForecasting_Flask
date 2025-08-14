from flask import Flask,request,jsonify,render_template
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import base64
from datetime import timedelta,datetime
from xgboost import XGBRegressor

app=Flask(__name__)

def load_data():
    dates=pd.date_range(start="2023-01-01",end=datetime.today(),freq='D')
    n=len(dates)
    price=np.round(np.random.normal(loc=10,scale=2,size=n),2)
    promotion=np.random.binomial(1,0.2,size=n)
    holiday=np.random.binomial(1,0.1,size=n)
    temperature=20+10*np.sin(2*np.pi*dates.dayofyear/365) + np.random.normal(0,2,n)
    temperature=np.round(temperature,2)

    #Seasonality based base model
    day_of_year=dates.dayofyear.values
    base_demand=100+20*np.sin(2*np.pi*day_of_year/365)

    #Demand formula with noise
    demand=np.round(
        base_demand
        -2*price
        +15*promotion
        -10*holiday
        +0.5*temperature
        +np.random.normal(0,5,n)).astype(int)

    #Create a DataFrame
    df=pd.DataFrame({
        "date": dates,
        "demand": demand,
        "price": price,
        "promotion": promotion,
        "holiday": holiday,
        "temperature": temperature
    })
    
    df['day_of_week']=df['date'].dt.dayofweek   #Monday=0,sunday=6
    df['weekend']=df['day_of_week'].isin([5,6]).astype(int)  #1 if saturday or sunday
    df['month']=df['date'].dt.month
    df['quarter']=df['date'].dt.quarter
    df['is_month_start']=df['date'].dt.is_month_start.astype(int)
    df['is_month_end']=df['date'].dt.is_month_end.astype(int)

    #sort by date to ensure the order
    df=df.sort_values("date").reset_index(drop=True)

    #lag features
    df['lag_1']=df['demand'].shift(1)
    df['lag_7']=df['demand'].shift(7)

    #Rolling mean features
    df['rolling_mean_3']=df['demand'].shift(1).rolling(window=3).mean()
    df['rolling_mean_7']=df['demand'].shift(1).rolling(window=7).mean()
    df=df.dropna().reset_index(drop=True)
    return df

#train model once
df=load_data()
features= ['price', 'promotion', 'holiday', 'temperature',
            'day_of_week', 'weekend', 'month', 'quarter',
            'is_month_start', 'is_month_end', 'lag_1', 'lag_7',
            'rolling_mean_3', 'rolling_mean_7']
X=df[features]
y=df['demand']
#model=XGBRegressor(objective="reg:squarederror", random_state=42)
model=joblib.load("xgb_model.pkl")
model.fit(X,y)
joblib.dump(model,"model.pkl")


def generate_forecast_plot():
    model = joblib.load("xgb_model.pkl")
    hist_df = df.copy()

    future_dates = [hist_df['date'].max() + timedelta(days=i) for i in range(1, 8)]
    future_df = pd.DataFrame({'date': future_dates})

    # Fill synthetic future features
    future_df['price'] = np.round(np.random.normal(loc=10, scale=2, size=7), 2)
    future_df['promotion'] = np.random.binomial(1, 0.2, size=7)
    future_df['holiday'] = np.random.binomial(1, 0.1, size=7)
    future_df['temperature'] = 20 + 10 * np.sin(2 * np.pi * pd.Series(future_dates).dt.dayofyear / 365) + np.random.normal(0, 2, 7)
    future_df['temperature'] = np.round(future_df['temperature'], 2)

    full_df = pd.concat([hist_df, future_df], ignore_index=True)

    full_df['day_of_week'] = full_df['date'].dt.dayofweek
    full_df['weekend'] = full_df['day_of_week'].isin([5, 6]).astype(int)
    full_df['month'] = full_df['date'].dt.month
    full_df['quarter'] = full_df['date'].dt.quarter
    full_df['is_month_start'] = full_df['date'].dt.is_month_start.astype(int)
    full_df['is_month_end'] = full_df['date'].dt.is_month_end.astype(int)

    full_df['lag_1'] = full_df['demand'].shift(1)
    full_df['lag_7'] = full_df['demand'].shift(7)
    full_df['rolling_mean_3'] = full_df['demand'].shift(1).rolling(window=3).mean()
    full_df['rolling_mean_7'] = full_df['demand'].shift(1).rolling(window=7).mean()

    for i in range(len(hist_df), len(full_df)):
        X_future = full_df.loc[i, features].values.reshape(1, -1)
        full_df.loc[i, 'demand'] = model.predict(X_future)[0]

        # Update lag/rolling for next step
        if i < len(full_df) - 1:
            for col, shift_val in [('lag_1', 1), ('lag_7', 7)]:
                full_df.loc[i+1, col] = full_df.loc[i+1-shift_val, 'demand']
            full_df.loc[i+1, 'rolling_mean_3'] = full_df['demand'].iloc[i-2:i+1].mean()
            full_df.loc[i+1, 'rolling_mean_7'] = full_df['demand'].iloc[i-6:i+1].mean()

    forecast_data=pd.DataFrame({
        'Date': future_dates,
        'Forecast_Demand': full_df.loc[len(hist_df):, 'demand'].values
    })

    

    plt.figure(figsize=(10,5))
    plt.plot(hist_df['date'][-60:], hist_df['demand'][-60:], label="Historical Demand",marker='o')
    # Extend forecast so it connects to the last historical point
    forecast_dates_extended = [hist_df['date'].iloc[-1]] + list(future_dates)
    forecast_values_extended = [hist_df['demand'].iloc[-1]] + list(full_df.loc[len(hist_df):, 'demand'])

    # Plot forecast
    plt.plot(forecast_dates_extended, forecast_values_extended, label="Forecast", marker='x', linestyle='--')
    
    plt.xlabel("Date")
    plt.ylabel("Demand")
    plt.title("Historical and Forecasted Demand")
    plt.legend()
    os.makedirs("static", exist_ok=True)
    plt.savefig("static/forecast_plot.png")
    plt.close()

    return hist_df,forecast_data
    

##Routes
@app.route('/')
def index():
    return render_template('index.html')  #form for what-if simulation

@app.route('/forecast')
def forecast():
    hist_df,forecast_data=generate_forecast_plot()
    #Convert records so Jinga can loop over them
    forecast_records=forecast_data.to_dict(orient='records')
    return render_template('forecast.html',plot_url='/static/forecast_plot.png',forecast_records=forecast_records)

@app.route('/simulate',methods=['POST'])
def simulate():
    #Extract feature values from form
    model = joblib.load("model.pkl")
    input_data = pd.DataFrame([{
        'price': float(request.form['price']),
        'promotion': int(request.form['promotion']),
        'holiday': int(request.form['holiday']),
        'temperature': float(request.form['temperature']),
        'day_of_week': int(request.form['day_of_week']),
        'weekend': int(request.form['weekend']),
        'month': int(request.form['month']),
        'quarter': int(request.form['quarter']),
        'is_month_start': int(request.form['is_month_start']),
        'is_month_end': int(request.form['is_month_end']),
        'lag_1': float(request.form['lag_1']),
        'lag_7': float(request.form['lag_7']),
        'rolling_mean_3': float(request.form['rolling_mean_3']),
        'rolling_mean_7': float(request.form['rolling_mean_7'])
    }])

    prediction = model.predict(input_data)[0]
    return render_template('simulate.html', prediction=round(prediction, 2))

def get_combined_data():
    hist_df,forecast_data=generate_forecast_plot()
    hist_df_copy=hist_df.copy()
    hist_df_copy['type']='historical' 

    forecast_df_copy=forecast_data.copy()  
    forecast_df_copy['type']='forecast'

    #rename forecast column to match demand
    forecast_df_copy.rename(columns={'Date':'date','Forecast_Demand':'demand'},inplace=True)
    hist_df_copy.rename(columns={'date':'date','demand':'demand'},inplace=True)

    #combine both
    combined_df=pd.concat([hist_df_copy[['date','demand','type']],forecast_df_copy[['date','demand','type']]])
    combined_df.sort_values(by='date',inplace=True)
    return combined_df

#@app.route('/combined_data')
#def combined_data():
    #df=get_combined_data()
    #return df.to_csv(index=False)

@app.route('/combined_data_json')
def combined_data_json():
    df=get_combined_data()
    return jsonify(df.to_dict(orient='records'))
 
if __name__== "__main__":
    app.run(debug=True)






