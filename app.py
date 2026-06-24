import streamlit as st
import pandas as pd
import plotly.express as px
from src import data_pipeline, model_pipeline

st.set_page_config(layout='wide')
st.title('Sales Dashboard')

@st.cache_data
def cached_data_pipeline():
    return data_pipeline()

@st.cache_data
def cached_model_pipeline(future_period):
    return model_pipeline(future_period)

kpis = cached_data_pipeline()

st.text('Welcome to the Sales Dashboard! Here we analyse the data from the Superstore dataset.')

st.markdown("""
<style>
section[data-testid="stSidebar"] a {
    color: black !important;
    # font-weight: 700 !important;
    # font-size: 18px !important;
    text-decoration: none !important;
}

section[data-testid="stSidebar"] a:hover {
    color: #3b82f6 !important;
    text-decoration: none !important;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title('Navigation')
st.sidebar.markdown("""
- [KPIs Overview](#kpis-overview)
- [Sales Performance](#sales-performance)
- [Category & Sub-Category](#category-distribution)
- [Product Performance](#product-performance)
- [Customer Analysis](#customer-analysis)
- [Regional & State Analysis](#regional-analysis)
- [Feature Analysis](#feature-analysis)
- [Sales Forecasting](#sales-forecasting)
""")

st.subheader("KPI's", anchor="kpis-overview")
con1=st.container(width=1200, height=220, vertical_alignment="center")

c1, c2, c3, c4 = con1.columns(4, vertical_alignment="center")
c1=c1.metric(label='Avg Order Value', value=kpis['Average Order Value']['value'].round(2))
c2=c2.metric(label='Total Sales', value=kpis['Total Sale']['value'].round(2))
c3=c3.metric(label='Total Profit', value=kpis['Total Profit']['value'].round(2))
c4=c4.metric(label='Overall Profit Margin', value=kpis['Profit Margin']['value'].round(2).astype(str)+'%')

c5, c6, c7, c8 = con1.columns(4, vertical_alignment="center")
c5=c5.metric(label='# of Customers', value=kpis['Total Customers']['value'])
c6=c6.metric(label='# of categories', value=kpis['Category Sales']['value'].shape[0])
c7=c7.metric(label='# of Sub-Categories', value=kpis['Sub-Category Sales']['value'].shape[0])
c8=c8.metric(label='# of Orders', value=kpis['Total Unique Orders']['value'])

st.divider()
st.subheader('Sales Performance', anchor="sales-performance")

source = kpis['Yearly Sales']['value']

col_perf1, col_perf2 = st.columns(2)

with col_perf1:
    st.write("#### Yearly Sales Growth")
    latest_sales = source.loc[source['Order Year'] == 2017, 'Sales'].values[0]
    prev_sales = source.loc[source['Order Year'] == 2016, 'Sales'].values[0]
    sales_growth = ((latest_sales - prev_sales) / prev_sales) * 100
    st.metric(
        label="Sales (2017)", 
        value=f"${latest_sales:,.2f}", 
        delta=f"{sales_growth:+.2f}% YoY Growth"
    )
    
    fig_sales = px.line(
        source,
        x='Order Year',
        y='Sales',
        markers=True,
        color_discrete_sequence=['#3b82f6'] # Premium Royal Blue
    )
    fig_sales.update_layout(
        xaxis_title="Year",
        yaxis_title="Total Sales ($)",
        xaxis=dict(type='category'),
        margin=dict(t=20, l=10, r=10, b=10),
        font=dict(family="Outfit, Inter, sans-serif", size=12),
        height=350,
        hovermode="x unified"
    )
    fig_sales.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate="<b>Year: %{x}</b><br>Sales: %{y:$,.2f}<extra></extra>"
    )
    st.plotly_chart(fig_sales, width="stretch")

with col_perf2:
    st.write("#### Yearly Profit Growth")
    latest_profit = source.loc[source['Order Year'] == 2017, 'Profit'].values[0]
    prev_profit = source.loc[source['Order Year'] == 2016, 'Profit'].values[0]
    profit_growth = ((latest_profit - prev_profit) / prev_profit) * 100
    st.metric(
        label="Profit (2017)", 
        value=f"${latest_profit:,.2f}", 
        delta=f"{profit_growth:+.2f}% YoY Growth"
    )
    
    fig_profit = px.line(
        source,
        x='Order Year',
        y='Profit',
        markers=True,
        color_discrete_sequence=['#10b981'] # Premium Emerald Green
    )
    fig_profit.update_layout(
        xaxis_title="Year",
        yaxis_title="Total Profit ($)",
        xaxis=dict(type='category'),
        margin=dict(t=20, l=10, r=10, b=10),
        font=dict(family="Outfit, Inter, sans-serif", size=12),
        height=350,
        hovermode="x unified"
    )
    fig_profit.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate="<b>Year: %{x}</b><br>Profit: %{y:$,.2f}<extra></extra>"
    )
    st.plotly_chart(fig_profit, width="stretch")

st.divider()
st.subheader('Distribution of Category & Sub-Category', anchor="category-distribution")

# Interactivity control: allow user to select coloring metric
color_option = st.selectbox(
    "Color Treemap By:",
    options=["Category", "Sales","Profit", "Profit Margin"],
    index=0,
    help="Choose the metric to color-code the Treemap rectangles."
)

sub_cat_df = kpis['Sub-Category Sales']['value']
sub_cat_df['Profit_abs'] = sub_cat_df['Profit'].abs()

# Define styling configurations based on user selection
# Note: 'values' is always set to 'Sales' because treemap rectangle sizes must be positive,
# whereas Profit and Profit Margin can be negative, which would crash Plotly JS.
if color_option == "Category":
    fig = px.treemap(
        sub_cat_df,
        path=['Category', 'Sub-Category'],
        values='Sales',
        color='Category',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hover_data={'Sales': ':$,.2f', 'Profit': ':$,.2f', 'Profit_Margin': ':.2f%'}
    )
elif color_option == "Sales":
    fig = px.treemap(
        sub_cat_df,
        path=['Category', 'Sub-Category'],
        values='Sales',
        color='Sales',
        color_continuous_scale='Blues',
        hover_data={'Sales': ':$,.2f', 'Profit': ':$,.2f', 'Profit_Margin': ':.2f%'}
    )
elif color_option == "Profit":
    fig = px.treemap(
        sub_cat_df,
        path=['Category', 'Sub-Category'],
        values='Profit_abs',
        color='Profit',
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=0,
        hover_data={'Sales': ':$,.2f', 'Profit': ':$,.2f', 'Profit_Margin': ':.2f%'}
    )
    fig.update_traces(
        texttemplate="%{label}<br>%{customdata[1]:$,.2f}"  # customdata[1] = Profit
    )
else: # Profit Margin
    fig = px.treemap(
        sub_cat_df,
        path=['Category', 'Sub-Category'],
        values='Sales',
        color='Profit_Margin',
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=0,
        hover_data={'Sales': ':$,.2f', 'Profit': ':$,.2f', 'Profit_Margin': ':.2f%'}
    )

# Premium UI styling tweaks for the Treemap
fig.update_layout(
    margin=dict(t=30, l=10, r=10, b=10),
    font=dict(family="Outfit, Inter, sans-serif", size=14),
    height=600
)
fig.update_traces(
    textinfo="label+value",
)

st.plotly_chart(fig, width="stretch")

st.divider()
st.subheader('Product Performance Analysis', anchor="product-performance")

col1, col2 = st.columns(2)

with col1:
    st.write("#### Top 10 Profit-Making Products")
    top_products_series = kpis['Top Products']['value']
    top_products_df = top_products_series.reset_index()
    top_products_df.columns = ['Product Name', 'Profit']
    
    # Truncate product names for clean visual presentation
    top_products_df['Display Name'] = top_products_df['Product Name'].apply(
        lambda x: x[:35] + '...' if len(x) > 35 else x
    )
    
    fig_top = px.bar(
        top_products_df,
        x='Profit',
        y='Display Name',
        orientation='h',
        color_discrete_sequence=['#10b981'],  # Premium Emerald Green
        hover_data={'Product Name': False, 'Profit': ':$,.2f', 'Display Name': False}
    )
    
    fig_top.update_layout(
        xaxis_title="Total Profit ($)",
        yaxis_title=None,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(t=10, l=10, r=10, b=10),
        font=dict(family="Outfit, Inter, sans-serif", size=12),
        height=400,
        hovermode="y unified"
    )
    # fig_top.update_traces(
    #     marker=dict(pattern_fillmode="overlay")
    # )
    st.plotly_chart(fig_top, width="stretch")

with col2:
    st.write("#### Top 10 Loss-Making Products")
    top_loss_series = kpis['Top Loss Products']['value']
    top_loss_df = top_loss_series.reset_index()
    top_loss_df.columns = ['Product Name', 'Profit']
    
    # Use absolute loss for bar display, while preserving negative profit for tooltips
    top_loss_df['Loss'] = top_loss_df['Profit'].abs()
    top_loss_df['Display Name'] = top_loss_df['Product Name'].apply(
        lambda x: x[:35] + '...' if len(x) > 35 else x
    )
    
    fig_loss = px.bar(
        top_loss_df,
        x='Loss',
        y='Display Name',
        orientation='h',
        color_discrete_sequence=['#ef4444'],  # Premium Red
        hover_data={'Product Name': False, 'Loss': ':$,.2f', 'Display Name': False}
    )
    
    fig_loss.update_layout(
        xaxis_title="Total Loss ($)",
        yaxis_title=None,
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(t=10, l=10, r=10, b=10),
        font=dict(family="Outfit, Inter, sans-serif", size=12),
        height=400,
        hovermode="y unified"
    )
    st.plotly_chart(fig_loss, width="stretch")

st.divider()
st.subheader('Customer Analysis', anchor="customer-analysis")

col_cust1, col_cust2 = st.columns(2)

with col_cust1:
    st.write("#### Top 10 Customers by Profit")
    top_10_cust = kpis['Top 10 Customers']['value']
    st.dataframe(
        top_10_cust,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", format="%d"),
            "Customer Name": st.column_config.TextColumn("Customer Name"),
            "Segment": st.column_config.TextColumn("Segment"),
            "Sales": st.column_config.NumberColumn("Total Sales", format="$%,.2f"),
            "Profit": st.column_config.NumberColumn("Total Profit", format="$%,.2f"),
            "Orders": st.column_config.NumberColumn("Orders Count", format="%d")
        },
        hide_index=True,
        width="stretch"
    )

with col_cust2:
    st.write("#### Customer Segmentation by Value")
    
    value_segment_option = st.selectbox(
        "Select Customer Value Segment:",
        options=["High Value", "Mid Value", "Low Value"],
        index=0,
        help="Filter customers by their sales value segments (determined by quantiles)."
    )
    
    customer_data = kpis['Customer Data']['value']
    filtered_cust = customer_data[customer_data['Value Segment'] == value_segment_option].copy()
    filtered_cust.insert(0, 'Rank', range(1, len(filtered_cust) + 1))
    
    st.dataframe(
        filtered_cust,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", format="%d"),
            "Customer Name": st.column_config.TextColumn("Customer Name"),
            "Segment": st.column_config.TextColumn("Segment"),
            "Sales": st.column_config.NumberColumn("Total Sales", format="$%,.2f"),
            "Profit": st.column_config.NumberColumn("Total Profit", format="$%,.2f"),
            "Orders": st.column_config.NumberColumn("Orders Count", format="%d"),
            "Value Segment": None
        },
        hide_index=True,
        width="stretch",
        height=300
    )

st.divider()
st.subheader('Regional & State Analysis', anchor="regional-analysis")

col_reg1, col_reg2 = st.columns(2)

with col_reg1:
    st.write("#### Sales & Profit by Region")
    region_sales_df = kpis['Region Sales']['value'].copy()
    region_melted = region_sales_df.melt(
        id_vars='Region', 
        value_vars=['Sales', 'Profit'], 
        var_name='Metric', 
        value_name='Amount'
    )
    
    fig_region = px.bar(
        region_melted,
        x='Region',
        y='Amount',
        color='Metric',
        barmode='stack',
        category_orders={
            'Metric': ['Profit', 'Sales']  # Bottom -> Top
        },
        color_discrete_map={
            'Sales': '#3b82f6',   # Premium Royal Blue
            'Profit': '#10b981'   # Premium Emerald Green
        },
        hover_data={'Region': True, 'Metric': True, 'Amount': ':$,.2f'}
    )
    
    fig_region.update_layout(
        xaxis_title="Region",
        yaxis_title="Amount ($)",
        margin=dict(t=20, l=10, r=10, b=10),
        font=dict(family="Outfit, Inter, sans-serif", size=12),
        height=400
    )
    st.plotly_chart(fig_region, width="stretch")

with col_reg2:
    st.write("#### Sales Map by US State")
    state_sales_df = kpis['State Sales']['value'].copy()
    
    fig_map = px.choropleth(
        state_sales_df,
        locations='State_Code',
        locationmode="USA-states",
        color='Sales',
        scope="usa",
        color_continuous_scale="Oranges",#Peach
        hover_data={'State': True, 'Sales': ':$,.2f', 'Profit': ':$,.2f', 'State_Code': False}
    )
    
    fig_map.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        font=dict(family="Outfit, Inter, sans-serif", size=12),
        height=400,
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            lakecolor='rgba(0,0,0,0)'
        )
    )
    st.plotly_chart(fig_map, width="stretch")

st.divider()
st.subheader('Feature Analysis', anchor="feature-analysis")

col_corr1, col_corr2 = st.columns(2)

with col_corr1:
    st.write("#### Correlation Matrix")
    corr_df = kpis['Correlation Matrix']['value']
    
    fig_corr = px.imshow(
        corr_df,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        color_continuous_midpoint=0,
        aspect="auto",
        labels=dict(color="Correlation")
    )
    
    fig_corr.update_layout(
        margin=dict(t=20, l=10, r=10, b=10),
        font=dict(family="Outfit, Inter, sans-serif", size=12),
        height=400
    )
    st.plotly_chart(fig_corr, width="stretch")

with col_corr2:
    st.write("#### Relationship between Profit & Discount")
    scatter_df = kpis['Scatter Data']['value']
    
    fig_scatter = px.scatter(
        scatter_df,
        x='Discount',
        y='Profit',
        color='Category',
        size='Sales',
        hover_data={'Category': True, 'Sub-Category': True, 'Discount': ':.0%', 'Profit': ':$,.2f', 'Sales': ':$,.2f'},
        color_discrete_sequence=px.colors.qualitative.Pastel,
        opacity=0.9
    )
    
    fig_scatter.update_layout(
        xaxis=dict(tickformat=".0%"),
        xaxis_title="Discount",
        yaxis_title="Profit ($)",
        margin=dict(t=20, l=10, r=10, b=10),
        font=dict(family="Outfit, Inter, sans-serif", size=12),
        height=400
    )
    st.plotly_chart(fig_scatter, width="stretch")

st.divider()
st.subheader('Sales Forecasting', anchor="sales-forecasting")
st.write("Predict future sales using our trained XGBoost recursive forecasting model.")

# Sidebar or inline slider for forecast period
forecast_period = st.slider(
    "Select Forecast Period (Months):",
    min_value=3,
    max_value=24,
    value=12,
    step=1,
    help="Select the number of future months to forecast sales for."
)

with st.spinner("Generating future sales forecast..."):
    future_sales = cached_model_pipeline(future_period=forecast_period)

# Access historical monthly sales from loaded KPIs
historical_sales = kpis['Monthly Sales']['value'].copy()

# Prepare dataframes for line chart
df_hist = historical_sales[['Order Date', 'Sales']].rename(columns={'Order Date': 'Date'})
df_hist['Date'] = pd.to_datetime(df_hist['Date'])
df_hist['Type'] = 'Historical'

df_fore = future_sales.rename(columns={'Forecast_Sales': 'Sales'})
df_fore['Date'] = pd.to_datetime(df_fore['Date'])
df_fore['Type'] = 'Forecast'

# Connect the lines smoothly by duplicating the last historical point into the forecast line
last_hist_point = df_hist.tail(1).copy()
last_hist_point['Type'] = 'Forecast'

combined_df = pd.concat([df_hist, last_hist_point, df_fore], ignore_index=True)
combined_df.sort_values(by='Date', inplace=True)

# Build a premium Plotly line chart
fig_forecast = px.line(
    combined_df,
    x='Date',
    y='Sales',
    color='Type',
    color_discrete_map={
        'Historical': '#3b82f6',  # Royal Blue
        'Forecast': '#ef4444'     # Premium Red
    },
    labels={'Sales': 'Sales ($)', 'Date': 'Date', 'Type': 'Data Type'}
)

fig_forecast.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Sales ($)",
    margin=dict(t=20, l=10, r=10, b=10),
    font=dict(family="Outfit, Inter, sans-serif", size=12),
    height=450,
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

fig_forecast.update_traces(
    line=dict(width=3),
    hovertemplate="<b>%{y:$,.2f}</b><extra></extra>"
)

# Display metrics
col_f1, col_f2, col_f3 = st.columns(3)
col_f1.metric(
    label="Total Forecasted Sales", 
    value=f"${future_sales['Forecast_Sales'].sum():,.2f}"
)
col_f2.metric(
    label="Average Monthly Forecasted Sales", 
    value=f"${future_sales['Forecast_Sales'].mean():,.2f}"
)
peak_row = future_sales.loc[future_sales['Forecast_Sales'].idxmax()]
col_f3.metric(
    label="Peak Forecasted Month", 
    value=peak_row['Date'].strftime('%b %Y'),
    delta=f"${peak_row['Forecast_Sales']:,.2f}"
)

# Render the plot
st.plotly_chart(fig_forecast,width='stretch')


