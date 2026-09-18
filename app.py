import pandas as pd
import plotly.express as px
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Vehicle Market Analysis",
    page_icon="🚗",
    layout="wide"
)

# Loading the dataset
car_data = pd.read_csv("vehicles_us.csv")

# App header
st.title("🚗 Vehicle Market Analysis")

st.write(
    "Explore used vehicle listings, pricing patterns, mileage, "
    "vehicle characteristics, and listing activity."
)

# Sidebar filter
st.sidebar.header("Filters")

# Vehicle type filter
vehicle_types = sorted(
    car_data["type"].dropna().unique()
)

selected_types = st.sidebar.multiselect(
    "Vehicle Type",
    options=vehicle_types,
    default=vehicle_types
)


# Condition filter
conditions = sorted(
    car_data["condition"].dropna().unique()
)

selected_conditions = st.sidebar.multiselect(
    "Condition",
    options=conditions,
    default=conditions
)


# Transmission filter
transmissions = sorted(
    car_data["transmission"].dropna().unique()
)

selected_transmissions = st.sidebar.multiselect(
    "Transmission",
    options=transmissions,
    default=transmissions
)


# Model year filter
min_year = int(car_data["model_year"].min())
max_year = int(car_data["model_year"].max())

selected_years = st.sidebar.slider(
    "Model Year",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)


# Price filter
min_price = int(car_data["price"].min())
max_price = int(car_data["price"].max())

selected_price = st.sidebar.slider(
    "Price Range ($)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# Filter data
filtered_data = car_data[
    (car_data["type"].isin(selected_types))
    & (car_data["condition"].isin(selected_conditions))
    & (car_data["transmission"].isin(selected_transmissions))
    & (
        car_data["model_year"].between(
            selected_years[0],
            selected_years[1]
        )
    )
    & (
        car_data["price"].between(
            selected_price[0],
            selected_price[1]
        )
    )
]

# Handle empty filtered data

if filtered_data.empty:
    st.warning(
        "No vehicle listings match the selected filters. "
        "Please adjust the filters in the sidebar."
    )
    st.stop()

# Key metrics
total_listings = filtered_data.shape[0]
median_price = filtered_data["price"].median()
median_mileage = filtered_data["odometer"].median()
median_year = filtered_data["model_year"].median()
median_days = filtered_data["days_listed"].median()


st.subheader("Market Snapshot")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Listings",
    f"{total_listings:,}"
)

col2.metric(
    "Median Price",
    f"${median_price:,.0f}"
)

col3.metric(
    "Median Mileage",
    f"{median_mileage:,.0f} mi"
)

col4.metric(
    "Median Model Year",
    f"{median_year:.0f}"
)

col5.metric(
    "Median Days Listed",
    f"{median_days:.0f} days"
)


st.divider()

# Market overview
st.header("Market Overview")

# Vehicle type distribution
type_counts = (
    filtered_data["type"]
    .value_counts()
    .reset_index()
)

type_counts.columns = [
    "type",
    "count"
]


fig_type = px.bar(
    type_counts,
    x="type",
    y="count",
    title="Vehicle Listings by Type",
    labels={
        "type": "Vehicle Type",
        "count": "Number of Listings"
    }
)

fig_type.update_layout(
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig_type,
    use_container_width=True
)


# ------------------------------------------------------
# VEHICLE DISTRIBUTIONS
# ------------------------------------------------------

st.subheader("Vehicle Distributions")

col1, col2 = st.columns(2)


# Price distribution
with col1:

    price_limit = filtered_data["price"].quantile(0.95)

    fig_price = px.histogram(
        filtered_data,
        x="price",
        nbins=50,
        title="Price Distribution",
        labels={
            "price": "Price ($)"
        }
    )

    fig_price.update_xaxes(
        range=[0, price_limit]
    )

    st.plotly_chart(
        fig_price,
        use_container_width=True
    )

    st.caption(
        "The x-axis focuses on the lower 95% of listing prices "
        "to prevent extreme values from compressing the distribution."
    )


# Mileage distribution
with col2:

    mileage_limit = (
        filtered_data["odometer"]
        .dropna()
        .quantile(0.95)
    )

    fig_mileage = px.histogram(
        filtered_data,
        x="odometer",
        nbins=40,
        title="Mileage Distribution",
        labels={
            "odometer": "Mileage (miles)"
        }
    )

    fig_mileage.update_xaxes(
        range=[0, mileage_limit]
    )

    st.plotly_chart(
        fig_mileage,
        use_container_width=True
    )

    st.caption(
        "The x-axis focuses on the lower 95% of mileage values "
        "so the main distribution remains readable."
    )


st.divider()

# Price analysis
st.header("Price Analysis")

st.write(
    "Explore how vehicle price relates to mileage, "
    "model year, condition, and vehicle type."
)


# Price vs mileage
fig_scatter = px.scatter(
    filtered_data,
    x="odometer",
    y="price",
    title="Price vs. Mileage",
    labels={
        "odometer": "Mileage (miles)",
        "price": "Price ($)"
    },
    opacity=0.4,
    hover_data=[
        "model",
        "model_year",
        "condition",
        "type"
    ]
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# Price vs model year

fig_year = px.scatter(
    filtered_data,
    x="model_year",
    y="price",
    title="Price vs. Model Year",
    labels={
        "model_year": "Model Year",
        "price": "Price ($)"
    },
    opacity=0.4,
    hover_data=[
        "model",
        "odometer",
        "condition",
        "type"
    ]
)

st.plotly_chart(
    fig_year,
    use_container_width=True
)

# Price by vehicle characteristics
st.subheader("Price by Vehicle Characteristics")

col1, col2 = st.columns(2)


# Price by condition
with col1:

    fig_condition = px.box(
        filtered_data,
        x="condition",
        y="price",
        title="Price by Vehicle Condition",
        labels={
            "condition": "Condition",
            "price": "Price ($)"
        }
    )

    st.plotly_chart(
        fig_condition,
        use_container_width=True
    )


# Price by vehicle type
with col2:

    fig_vehicle_type = px.box(
        filtered_data,
        x="type",
        y="price",
        title="Price by Vehicle Type",
        labels={
            "type": "Vehicle Type",
            "price": "Price ($)"
        }
    )

    fig_vehicle_type.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_vehicle_type,
        use_container_width=True
    )


st.divider()

# Listing activity
st.header("Listing Activity")

st.write(
    "Explore how long vehicle advertisements remain listed."
)


fig_days = px.histogram(
    filtered_data,
    x="days_listed",
    nbins=40,
    title="Days Listed Distribution",
    labels={
        "days_listed": "Days Listed"
    }
)

st.plotly_chart(
    fig_days,
    use_container_width=True
)


st.divider()