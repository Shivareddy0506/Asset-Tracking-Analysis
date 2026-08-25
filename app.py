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
    alert_df = fetch_alerts_data()
except Exception as e:
    st.error(f"Failed to connect to database: {e}")
    st.stop()

col_header, col_refresh = st.columns([4, 1])
with col_header:
    st.caption(f"Last database sync: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
with col_refresh:
    if st.button("🔄 Sync Live Data"):  # Fixed: Added missing colon
        st.rerun()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Peak Asset Activity Tracking")
    heatmap_data = alert_df.groupby(["day", "hour"])["device_id"].nunique().reset_index()
    heatmap_data.columns = ["day", "hour", "unique_devices"]
    
    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x="hour",
        y="day",
        z="unique_devices",
        title="Active Hours Heatmap Matrix",
        labels={'hour': 'Hour of Day (24h)', 'day': 'Day of Week', 'unique_devices': 'Active Assets'}, # Fixed label mapping
        color_continuous_scale='RdYlGn_r',
        category_orders={'day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']} # Fixed category key
    )
    fig_heatmap.update_layout(xaxis_nticks=24, template='plotly_dark')
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown('--------------')
