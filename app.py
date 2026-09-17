import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Car Sale Analysis",
    layout="wide"
)

# App header
st.header('Car Sale Analysis')

# Reading data
car_data = pd.read_csv('vehicles_us.csv')


# Histogram checkbox
build_histogram = st.checkbox('Build Histogram')

if build_histogram:
    st.write('Creating a histogram of the odometer column')

    fig = px.histogram(
        car_data,
        x='odometer'
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
