import pandas as pd
def preprocess_data(df):
    # Handle missing values
    df.fillna(method='ffill', inplace=True)

    needed_cols = {'Order ID', 'Customer ID', 'Order Date', 'Ship Date', 'Sales', 'Profit', 'Discount', 'Category', 'Sub-Category', 'Region', 'Segment', 'City', 'Product Name'}
    if not (needed_cols).issubset(df.columns):
        missing_cols = needed_cols - set(df.columns)
        print(f"Missing columns: {missing_cols}")
        return None
    
    # Correcting Date formats
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    return df
