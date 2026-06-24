import pandas as pd

def get_kpis(df):
    # Calculate basic numeric KPIs
    total_sale = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_customers = df['Customer ID'].nunique()
    total_uni_orders = df["Order ID"].nunique()
    avg_order_val = total_sale / total_uni_orders
    profit_margin = (total_profit / total_sale) * 100

    # Sales by categories, sub-categories, regions, and states
    cat_sales = df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
    cat_sales['Profit_Margin'] = (cat_sales['Profit'] / cat_sales['Sales']) * 100

    sub_cat_sales = df.groupby(["Category", "Sub-Category"])[["Sales", "Profit"]].sum().reset_index()
    sub_cat_sales['Profit_Margin'] = (sub_cat_sales['Profit'] / sub_cat_sales['Sales']) * 100
    sub_cat_sales.sort_values(['Category', 'Profit_Margin'], ascending=[True, False], inplace=True)

    region_sales = df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()

    # State Sales for Choropleth Map mapping
    us_state_to_abbrev = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
        "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
        "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
        "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
        "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
        "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
        "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
    }
    state_sales = df.groupby("State")[["Sales", "Profit"]].sum().reset_index()
    state_sales["State_Code"] = state_sales["State"].map(us_state_to_abbrev)

    # Correlation Matrix & Scatter Data Calculations
    corr_cols = ["Sales", "Profit", "Discount", "Quantity", "Shipping Days"]
    correlation_matrix = df[corr_cols].corr()
    scatter_df = df[["Profit", "Discount", "Sales", "Category", "Sub-Category"]].copy()

    # Sales history
    yearly_sales = df.groupby('Order Year')[['Sales', 'Profit']].sum().reset_index()
    monthly_sales = df.resample('ME', on='Order Date')[['Sales']].sum().reset_index()

    # Customer Metrics and Segmentations
    customer_df = df.groupby('Customer Name').agg(
        Segment=('Segment', 'first'),
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index()

    q25 = customer_df['Profit'].quantile(0.25)
    q75 = customer_df['Profit'].quantile(0.75)

    def get_value_segment(profit):
        if profit >= q75:
            return 'High Value'
        elif profit >= q25:
            return 'Mid Value'
        else:
            return 'Low Value'

    customer_df['Value Segment'] = customer_df['Profit'].apply(get_value_segment)
    customer_df = customer_df.sort_values(by='Profit', ascending=False).reset_index(drop=True)
    
    top_10_customers = customer_df.head(10).copy()
    top_10_customers.insert(0, 'Rank', range(1, 11))

    # Product Performance
    top_products = df.groupby('Product Name')['Profit'].sum().nlargest(10)
    top_loss_products = df.groupby('Product Name')['Profit'].sum().nsmallest(10).rename({'Profit': 'Loss'})

    kpis = {
        "Total Sale": {
            "value": total_sale,
            "type": "Numeric"
        },
        "Total Profit": {
            "value": total_profit,
            "type": "Numeric"
        },
        "Total Customers": {
            "value": total_customers,
            "type": "Numeric"
        },
        "Total Unique Orders": {
            "value": total_uni_orders,
            "type": "Numeric"
        },
        "Average Order Value": {
            "value": avg_order_val,
            "type": "Numeric"
        },
        "Profit Margin": {
            "value": profit_margin,
            "type": "Numeric"
        },
        "Category Sales": {
            "value": cat_sales,
            "type": "DataFrame"
        },
        "Sub-Category Sales": {
            "value": sub_cat_sales,
            "type": "DataFrame"
        },
        "Region Sales": {
            "value": region_sales,
            "type": "DataFrame"
        },
        "Yearly Sales": {
            "value": yearly_sales,
            "type": "DataFrame"
        },
        "Monthly Sales": {
            "value": monthly_sales,
            "type": "DataFrame"
        },
        "Top Products": {
            "value": top_products,
            "type": "Series"
        },
        "Top Loss Products": {
            "value": top_loss_products,
            "type": "Series"
        },
        "Customer Data": {
            "value": customer_df,
            "type": "DataFrame"
        },
        "Top 10 Customers": {
            "value": top_10_customers,
            "type": "DataFrame"
        },
        "State Sales": {
            "value": state_sales,
            "type": "DataFrame"
        },
        "Correlation Matrix": {
            "value": correlation_matrix,
            "type": "DataFrame"
        },
        "Scatter Data": {
            "value": scatter_df,
            "type": "DataFrame"
        }
    }
    return kpis