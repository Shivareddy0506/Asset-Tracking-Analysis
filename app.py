import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from urllib import parse

#page
st.set_page_config(page_title="Indoor Navigation Analytics",
                   page_icon="🔎",
                   layout= "wide"
                   )
st.title("🛰️ Indoor Navigation And Asset Tracking")
st.markdown("------------------")

DB_USER = st.secrets[DB_USER]
DB_PASS = urllib.parse.quote_plus(st.secrets[DB_PASS])
DB_HOST = st.secrets[DB_HOST]
DB_PORT = st.secrets[DB_PORT]
DB_NAME = st.secrets[DB_NAME]

@st.cache_resource
def get_engine():
    connection_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_url)

@st.cache_data(ttl=0)
def fetch_alerts_data():
    engine = get_engine
    query = "SELECT * FROM alerts"
    query1 = "SELECT * FROM devices"
    query2 = "SELECT * FROM zones"
    query3 = "SELECT * FROM floors"
    alert_df = pd.read_sql(query,engine)
    device_df = pd.read_sql(query1,engine)
    zones_df = pd.read_sql(query2,engine)
    floor_df = pd.read_sql(query3,engine)

    alert_df["created_at"] = pd.to_datetime(alert_df["created_at"])
    alert_df["hour"] = alert_df["created_at"].dt.hour
    alert_df["day"] = alert_df["created_at"].dt.day_name()
    return alert_df

try:
    