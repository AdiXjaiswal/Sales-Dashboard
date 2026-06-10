import pandas as pd
def get_kpis(df):
    # Calculate KPIs
    overall_month_sales=pd.DataFrame(columns=["Month", "Number of sales", "Total sales", "Total profit"])
    overall_month_sales= df.groupby("Order Month", sort=True).agg(
        Number_of_sales=("Sales","count"), Total_sales=("Sales","sum"),
        Total_profit=("Profit","sum")).reset_index()
    overall_month_sales.rename(columns={"Order Month": "Month"}, inplace=True)
    overall_month_sales["Month"]=pd.to_datetime(overall_month_sales["Month"],format="%m").dt.month_name()

    total_sale=overall_month_sales["Total_sales"].sum()
    total_profit=overall_month_sales["Total_profit"].sum()
    total_uni_orders=df["Order ID"].nunique()
    avg_order_val=total_sale/total_uni_orders
    profit_margin=(total_profit/total_sale)*100

    cat_sales=df.groupby("Category")[["Sales","Profit"]].sum().reset_index()
    sub_cat_sales=df.groupby(["Category", "Sub-Category"])[["Sales","Profit"]].sum().reset_index()
    region_sales=df.groupby("Region")[["Sales","Profit"]].sum().reset_index()
    seg_sales=df.groupby("Segment")[["Sales","Profit"]].sum().reset_index()

    city_sales = df.groupby('City')[['Sales', 'Profit']].sum().sort_values(by='Profit', ascending=False)
    cat_sales['Profit_Margin']=(cat_sales['Profit'] / cat_sales['Sales']) * 100
    sub_cat_sales['Profit_Margin']=(sub_cat_sales['Profit'] / sub_cat_sales['Sales']) * 100
    sub_cat_sales.sort_values(['Category','Profit_Margin'], ascending=[True,False], inplace=True)

    seasonality = df.groupby('Order Month')['Sales'].mean()
    loss_products = df[df['Profit'] < 0].sort_values('Profit')
    loss_by_subcat = loss_products.groupby('Sub-Category')['Profit'].sum().sort_values()

    max_cat_sales=cat_sales.max()
    max_sub_sales=sub_cat_sales.max()
    max_reg_sales=region_sales.max()
    max_seg_sales=seg_sales.max()
    best_sales={
        "Best category": [max_cat_sales["Category"], max_cat_sales["Sales"], max_cat_sales["Profit"]],
        "Best Sub category": [max_sub_sales["Sub-Category"], max_sub_sales["Sales"], max_sub_sales["Profit"]],
        "Best Region": [max_reg_sales["Region"], max_reg_sales["Sales"], max_reg_sales["Profit"]],
        "Best Segment": [max_seg_sales["Segment"],max_seg_sales["Sales"], max_seg_sales["Profit"]]
    }
    best_sales=pd.DataFrame(best_sales)
    best_sales.index=["Name","Sales","Profit"]

    yearly_sales=df.groupby('Order Year')[['Sales', 'Profit']].sum().reset_index()
    yearly_sales.set_index('Order Year', inplace=True)

    monthly_sales=df.resample('ME', on='Order Date').apply(
    lambda x:pd.Series({
        'Sales': x['Sales'].sum(),
        'Profit': x['Profit'].sum(),
        'Weighted_discount': (x['Sales']*x['Discount']).sum()/x['Sales'].sum()
        })
    )
    monthly_sales['Sales_MA_3'] = monthly_sales['Sales'].rolling(window=3).mean()
    monthly_sales['Sales_MA_6'] = monthly_sales['Sales'].rolling(window=6).mean()

    repeat_cust= df['Customer ID'].value_counts()
    repeat_cust=repeat_cust[repeat_cust>1].count()

    top_customers = df.groupby('Customer ID')['Sales'].sum().sort_values(ascending=False).head(10)
    top_products = df.groupby('Product Name')['Sales'].sum().nlargest(10)

    # Revenue per order (can be removed if not needed)
    orders = df.groupby('Order ID')[['Sales','Profit']].sum()

    kpis={
        "Overall Month Sales":{
            "value": overall_month_sales,
            "type": "DataFrame"
        },
        "Total Sale":{
            "value": total_sale,
            "type": "Numeric"
        },
        "Total Profit":{
            "value": total_profit,
            "type": "Numeric"
        },
        "Total Unique Orders":{
            "value": total_uni_orders,
            "type": "Numeric"
        },
        "Average Order Value":{
            "value": avg_order_val,
            "type": "Numeric"
        },
        "Profit Margin (%)":{
            "value": profit_margin,
            "type": "Numeric"
        },
        "Category Sales":{
            "value": cat_sales,
            "type": "DataFrame"
        },
        "Sub-Category Sales":{
            "value": sub_cat_sales,
            "type": "DataFrame"
        },
        "Region Sales":{
            "value": region_sales,
            "type": "DataFrame"
        },
        "Segment Sales":{
            "value": seg_sales,
            "type": "DataFrame"
        },
        "City Sales":{
            "value": city_sales,
            "type": "DataFrame"
        },
        "Best Sales":{
            "value": best_sales,
            "type": "DataFrame"
        },
        "Yearly Sales":{
            "value": yearly_sales,
            "type": "DataFrame"
        },
        "Monthly Sales":{
            "value": monthly_sales,
            "type": "DataFrame"
        },
        "Repeat Customers":{
            "value": repeat_cust,
            "type": "Numeric"
        },
        "Top Customers":{
            "value": top_customers,
            "type": "Series"
        },
        "Top Products":{
            "value": top_products,
            "type": "Series"
        },
        "Loss Products":{
            "value": loss_products,
            "type": "DataFrame"
        },
        "Loss by Sub-Category":{
            "value": loss_by_subcat,
            "type": "Series"
        },
        "Seasonality":{
            "value": seasonality,
            "type": "Series"
        }
    }
    rtet