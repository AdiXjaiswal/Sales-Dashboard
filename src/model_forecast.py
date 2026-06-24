import pandas as pd
import numpy as np
from xgboost import XGBRegressor
# import sklearn
# from pandas.tseries.offsets import MonthEnd

def forecast_future_sales(model_path, monthly_sales, future_period=3):
    model=XGBRegressor()
    model.load_model(model_path)
    print("XGBoost model imported")
    
    future_preds=[]
    temp_df=monthly_sales.copy() # monthly_sales is sorted by the order date (ASC)
    # temp_df.drop(columns=['Profit', 'Weighted_discount'], inplace=True)
    temp_df.set_index('Order Date', inplace=True)
    
    features=['Month_sin', 'Month_cos', 'Month_Quarter', 'Sales_MA_3', 'Sales_MA_6', 'Sales_MA_12', 'Lag_3', 'Lag_6', 'Lag_12', 'Rolling_Std_3', 'Rolling_Std_6', 'Rolling_Std_12']
    for i in range(future_period):
        # next month date
        next_date=(temp_df.index[-1].replace(day=1) + pd.DateOffset(months=1)) + pd.offsets.MonthEnd(0)
        #new row
        new_row=pd.DataFrame(index=[next_date])
        month=next_date.month
        #cyclic month
        new_row['Month_sin']=np.sin(2*np.pi*month/12)
        new_row['Month_cos']=np.cos(2*np.pi*month/12)
        #quarter
        new_row['Month_Quarter']=((month-1)//3)+1 # or new_row.index.max().quarter
        # Moving averages
        new_row['Sales_MA_3'] = temp_df['Sales'].tail(3).mean()
        new_row['Sales_MA_6'] = temp_df['Sales'].tail(6).mean()
        new_row['Sales_MA_12'] = temp_df['Sales'].tail(12).mean()
        # Lag features
        new_row['Lag_3'] = temp_df['Sales'].iloc[-3]
        new_row['Lag_6'] = temp_df['Sales'].iloc[-6]
        new_row['Lag_12'] = temp_df['Sales'].iloc[-12]
        # Rolling std
        new_row['Rolling_Std_3'] = temp_df['Sales'].tail(3).std()
        new_row['Rolling_Std_6'] = temp_df['Sales'].tail(6).std()
        new_row['Rolling_Std_12'] = temp_df['Sales'].tail(12).std()
        # Predict
        X_future = new_row[features]
        pred = model.predict(X_future)[0] #it returns numpy array so for int I use: [0]
        # Store prediction
        new_row['Sales'] = pred
    
        future_preds.append(
            {'Date': next_date, 'Forecast_Sales': pred}
        )
    
        # Append prediction for recursive forecasting
        temp_df = pd.concat([temp_df, new_row])

    return pd.DataFrame(future_preds)

# ---------TESTING---------------
# def main():
#     from data_loader import load_data
#     from feature_engineering import date_time_features, monthly_df
    
#     model='J:/Sales-Dashboard/outputs/models/xgb_model3.json'
#     df=load_data('J:/Sales-Dashboard/data/raw_superstore_data.csv')
#     date_time_features(df)
#     monthly_sales=monthly_df(df)
    
#     future_sales=forecast_future_sales(model, monthly_sales, future_period=3)
#     print(future_sales)

# if __name__=='__main__':
#     main()