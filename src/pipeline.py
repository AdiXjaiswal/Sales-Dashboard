import pandas as pd
from .data_loader import load_data
from . import feature_engineering as fe
from .kpi import get_kpis
from .model_forecast import forecast_future_sales

def data_pipeline():
    df=load_data('J:/Sales-Dashboard/data/raw_superstore_data.csv')
    fe.date_time_features(df)
    kpis=get_kpis(df)
    return kpis

def model_pipeline(future_period=3):
    print('\n----- Model Pipeline -----\n')
    df=load_data('J:/Sales-Dashboard/data/raw_superstore_data.csv')
    fe.date_time_features(df)
    monthly_sales=fe.monthly_df(df)
    model_path='J:/Sales-Dashboard/outputs/models/xgb_model3.json'

    future_sales=forecast_future_sales(model_path, monthly_sales, future_period=future_period)
    # print(future_sales)
    return future_sales