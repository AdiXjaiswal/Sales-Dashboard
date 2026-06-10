import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
from sklearn.multioutput import MultiOutputRegressor  # type: ignore[import]  # because I want to predict multiple targets: Sales, Profit
from xgboost import XGBRegressor

def forecast_sales_profit(df):

    drop_cols=['Row ID','Order ID','Order Date', 'Ship Date','Customer ID', 'Customer Name',
              'Country', 'Postal Code', 'Product ID', 'Product Name',]
    x=df.drop(columns=drop_cols+['Sales','Profit'])
    y=df[['Sales','Profit']]

    x_train, x_test, y_train, y_test=train_test_split(
        x,y, test_size=0.2, random_state=42
    )

    model = MultiOutputRegressor(
    XGBRegressor(
            n_estimators=500, learning_rate=0.05, max_depth=4, random_state=42, min_child_weight=5,
            subsample=0.8, colsample_bytree=0.8, gamma=0.1, reg_alpha=0.1, reg_lambda=1,
        )
    )
    model.fit(x_train, y_train)

    y_pred=model.predict(x_test)
    y_pred=pd.DataFrame(y_pred, columns=['Sales','Profit'])

    xg_rmse_sales=root_mean_squared_error(y_test['Sales'], y_pred['Sales'])
    xg_rmse_profit=root_mean_squared_error(y_test['Profit'], y_pred['Profit'])