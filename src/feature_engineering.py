import pandas as pd
def feature_engineering(df):
    # Create new features
    df["Order Month"]=df["Order Date"].dt.month
    df["Ship Month"]=df["Ship Date"].dt.month
    df["Order Year"]=df["Order Date"].dt.year
    df["Ship Year"]=df["Ship Date"].dt.year

    drop_cols=['Row ID','Order ID','Order Date', 'Ship Date','Customer ID', 'Customer Name', 'Country', 'Postal Code', 'Product ID', 'Product Name',]

    one_encoded_cols=['Ship Mode', 'Segment', 'State', 'Region', 'Category', 'Sub-Category']

    #dropping columns
    df=df.drop(columns=drop_cols+['Sales','Profit'])

    #Frequency encoding
    city_fq=df['City'].value_counts()
    df['City']=df['City'].map(city_fq)

    # One-Hot encoding
    df=pd.get_dummies(df, columns=one_encoded_cols, drop_first=True)