import joblib
import pandas as pd
import streamlit as st

from src.surge import compute_surge

MODEL_PATH = "models/pricing_model.pkl"
DATA_PATH = "data/processed_data.csv"
RAIN_MAP = {"Clear": "none", "Light rain": "light", "Heavy rain": "heavy"}

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_routes():
    df = pd.read_csv(DATA_PATH, usecols=["name", "source", "destination", "distance"])
    routes = df.groupby(["source", "destination"])["distance"].median().reset_index()
    products = sorted(df["name"].unique())
    return products, routes

st.title("Dynamic Pricing Engine")

model = load_model()
products, routes = load_routes()

product = st.selectbox("Product", products)
source = st.selectbox("From", sorted(routes["source"].unique()))
destinations = sorted(routes[routes["source"] == source]["destination"].unique())
destination = st.selectbox("To", destinations)

route_mask = (routes["source"] == source) & (routes["destination"] == destination)
distance = routes[route_mask]["distance"].iloc[0]

X = pd.DataFrame([{
    "name": product,
    "source": source,
    "destination": destination,
    "distance": distance,
}])
base_price = model.predict(X)[0]

st.write(f"Distance: {distance:.2f} mi")
st.subheader("Conditions")
hour = st.slider("Hour", 0, 23, 12)
weather = st.selectbox("Weather", list(RAIN_MAP.keys()))
event = st.checkbox("Event nearby")
weekend = st.checkbox("Weekend")

surge = compute_surge(
    product, hour, rain=RAIN_MAP[weather], event=event, weekend=weekend
)
final_price = base_price * surge

col1, col2, col3 = st.columns(3)
col1.metric("Base price", f"${base_price:.2f}")
col2.metric("Surge", f"x{surge:.2f}")
col3.metric("Final price", f"${final_price:.2f}")

