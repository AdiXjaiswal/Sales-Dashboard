import pandas as pd
import numpy as np

def date_time_features(df):
    df["Order Date"]=pd.to_datetime(df["Order Date"])
    df["Ship Date"]=pd.to_datetime(df["Ship Date"])
    
    df["Order Month"]=df["Order Date"].dt.month
    df["Ship Month"]=df["Ship Date"].dt.month
    df["Order Year"]=df["Order Date"].dt.year
    df["Ship Year"]=df["Ship Date"].dt.year
    df["Shipping Days"]=(df["Ship Date"]-df["Order Date"]).dt.days
    df["Quarter"]=df["Order Date"].dt.quarter

    df.sort_values(by=['Order Date'], inplace=True)
    df.reset_index(drop=True, inplace=True)

def encoding(df):
    drop_cols=['Row ID','Order ID','Order Date', 'Ship Date','Customer ID', 'Customer Name', 'Country', 'Postal Code', 'Product ID', 'Product Name',]

    one_encoded_cols=['Ship Mode', 'Segment', 'State', 'Region', 'Category', 'Sub-Category']
    
    # Cyclic encoding of Order Month
    df["month_sin"] = np.sin(2 * np.pi * df["Order Month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["Order Month"] / 12)

    #dropping columns
    df=df.drop(columns=drop_cols)

    #Frequency encoding
    city_fq=df['City'].value_counts()
    df['City']=df['City'].map(city_fq)

    # One-Hot encoding
    df=pd.get_dummies(df, columns=one_encoded_cols)
    return df

def monthly_df(df):
    monthly_sales=df.resample('ME', on='Order Date').agg(
        Sales=('Sales', 'sum')
    )
    monthly_sales.reset_index(inplace=True)

    monthly_sales['Month_sin']=np.sin(2*np.pi*(monthly_sales['Order Date'].dt.month)/12)
    monthly_sales['Month_cos']=np.cos(2*np.pi*(monthly_sales['Order Date'].dt.month)/12)
    monthly_sales['Month_Quarter']=monthly_sales['Order Date'].dt.quarter

    monthly_sales['Sales_MA_3'] = monthly_sales['Sales'].rolling(window=3).mean() #.fillna(0)
    monthly_sales['Sales_MA_6'] = monthly_sales['Sales'].rolling(window=6).mean() #.fillna(0)
    monthly_sales['Sales_MA_12']= monthly_sales['Sales'].rolling(window=12).mean()

    monthly_sales['Lag_3']=monthly_sales['Sales'].shift(3)
    monthly_sales['Lag_6']=monthly_sales['Sales'].shift(6)
    monthly_sales['Lag_12']=monthly_sales['Sales'].shift(12)

    monthly_sales["Rolling_Std_3"] = (monthly_sales["Sales"].shift(1).rolling(window=3).std())
    monthly_sales["Rolling_Std_6"] = (monthly_sales["Sales"].shift(1).rolling(window=6).std())
    monthly_sales["Rolling_Std_12"] = (monthly_sales["Sales"].shift(1).rolling(window=12).std())
    print('monthly_sales created')
    return monthly_sales