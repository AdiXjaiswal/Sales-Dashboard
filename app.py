import streamlit as st
import pandas as pd
from src import data_pipeline

kpis = data_pipeline()

st.title('Sales Dashboard')
st.text('Welcome to the Sales Dashboard! Here we analyse the data from the Superstore dataset to gain insights into sales performance, customer behavior, and product trends. Use the sidebar to navigate through different sections of the dashboard and explore the data visualizations and key metrics.')


nav=st.sidebar.title('Navigation')
st.subheader("KPI's")
con1=st.container(width=1200, height=110)

c1, c2, c3, c4 = con1.columns(4)
c1=c1.metric(label='Avg Order Value', value=kpis['Average Order Value']['value'].round(2))
c2=c2.metric(label='Total Sales', value=kpis['Total Sale']['value'].round(1))
c3=c3.metric(label='Total Profit', value=kpis['Total Profit']['value'].round(2))
c4=c4.metric(label='Overall Profit Margin', value=kpis['Profit Margin']['value'].round(2).astype(str)+'%')

st.divider()
st.subheader('Sales Performance')
