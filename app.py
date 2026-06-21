import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
from src import data_pipeline

kpis = data_pipeline()

st.set_page_config(layout='wide')
st.title('Sales Dashboard')
st.text('Welcome to the Sales Dashboard! Here we analyse the data from the Superstore dataset.')


nav=st.sidebar.title('Navigation')
st.subheader("KPI's")
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
st.subheader('Sales Performance')

source = kpis['Yearly Sales']['value']
# Selection that follows the mouse
nearest = alt.selection_point(
    nearest=True,
    on='pointerover',
    fields=['Order Year'],
    empty=False
)

# Base line
line = alt.Chart(source).mark_line().encode(
    x=alt.X('Order Year:O', title='Year'),
    y=alt.Y('Sales:Q', title='Sales')
)

# Highlighted point
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Vertical line following mouse
rules = alt.Chart(source).mark_rule(color='gray').encode(x='Order Year:O').transform_filter(nearest)

# Tooltip
tooltips = alt.Chart(source).mark_rule(opacity=0).encode(
    x='Order Year:O',
    tooltip=[
        alt.Tooltip('Order Year:O', title='Year'),
        alt.Tooltip('Sales:Q', title='Sales', format='$,.2f')
    ]
).add_params(nearest)

chart = alt.layer(
    line,
    points,
    rules,
    tooltips
)
st.altair_chart(chart)

st.divider()
st.subheader('Distribution of Category & Sub-Category')

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
st.subheader('Product Performance Analysis')

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
st.subheader('Customer Analysis')

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

    