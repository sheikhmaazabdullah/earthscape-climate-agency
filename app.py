"""EarthScape Climate Agency - Streamlit Dashboard.
Accounts are configured via environment variables (see README - Authentication). Run: streamlit run app.py"""
import streamlit as st, pandas as pd, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent/"src"))
from ml_models import detect_anomalies, forecast_trend, correlations
from alerts import check as check_alerts, THRESHOLDS
import os
def _load_users():
    # Accounts are configured through environment variables - no credentials live in this code.
    # Set one or more of: EARTHSCAPE_ADMIN_PASSWORD, EARTHSCAPE_ANALYST_PASSWORD, EARTHSCAPE_VIEWER_PASSWORD
    # The username is the role name (admin / analyst / viewer).
    users={}
    for role in ("admin","analyst","viewer"):
        pw=os.environ.get(f"EARTHSCAPE_{role.upper()}_PASSWORD")
        if pw: users[role]=(pw,role)
    return users
USERS=_load_users()
st.set_page_config(page_title="EarthScape Climate Agency", layout="wide")
if "user" not in st.session_state:
    st.title("EarthScape Climate Agency - Login")
    if not USERS: st.warning("No accounts configured. Set EARTHSCAPE_ADMIN_PASSWORD (and optionally EARTHSCAPE_ANALYST_PASSWORD / EARTHSCAPE_VIEWER_PASSWORD) in your environment, then restart. See README - Authentication.")
    u=st.text_input("Username"); p=st.text_input("Password", type="password")
    if st.button("Login"):
        if u in USERS and USERS[u][0]==p: st.session_state.user=(u,USERS[u][1]); st.rerun()
        else: st.error("Invalid credentials.")
    st.stop()
user, role = st.session_state.user
st.sidebar.write(f"Logged in: **{user}** ({role})")
if st.sidebar.button("Logout"): del st.session_state.user; st.rerun()
@st.cache_data
def load():
    df=pd.read_csv(pathlib.Path(__file__).parent/"data"/"raw"/"climate_records.csv", parse_dates=["date"])
    return detect_anomalies(df)
df=load()
page=st.sidebar.radio("Page", ["Dashboard","Monthly Analysis (MapReduce)","ML Insights","Alerts","Support"] +
                      (["Admin - Support Tickets"] if role=="admin" else []))
station=st.sidebar.selectbox("Station", sorted(df.station.unique())); d=df[df.station==station]
if page=="Dashboard":
    st.title("EarthScape Climate Agency - Climate Intelligence Dashboard")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Avg Temp", f"{d.temperature_c.mean():.1f} C"); c2.metric("Total Rainfall", f"{d.rainfall_mm.sum():,.0f} mm")
    c3.metric("Anomalies", int(d.is_anomaly.sum())); c4.metric("Alerts", len(check_alerts(d)))
    st.subheader(f"Temperature - {station}"); st.line_chart(d.set_index("date")["temperature_c"])
    st.subheader("Rainfall"); st.bar_chart(d.set_index("date")["rainfall_mm"])
    st.subheader("Station comparison - average temperature")
    st.bar_chart(df.groupby("station")["temperature_c"].mean())
elif page=="Monthly Analysis (MapReduce)":
    st.title("Monthly Aggregates - Hadoop MapReduce Output")
    m=pd.read_csv(pathlib.Path(__file__).parent/"data"/"processed"/"monthly_summary.csv")
    st.dataframe(m[m.station==station]); st.line_chart(m[m.station==station].set_index("year_month")["avg_temp_c"])
    st.caption("Produced by mapreduce/mapper.py + reducer.py (Hadoop Streaming) - 300 rows = 5 stations x 60 months.")
elif page=="ML Insights":
    st.title("Machine Learning Insights")
    st.subheader("Anomalies detected (per station-month z-score > 3)")
    st.dataframe(d[d.is_anomaly][["date","temperature_c","rainfall_mm","temp_z"]])
    st.subheader("Correlation analysis"); st.dataframe(correlations(df).round(2))
    fut, per_year = forecast_trend(df, station)
    st.subheader(f"Trend forecast - {station}: {per_year:+.3f} C/year"); st.line_chart(fut.set_index("date")["predicted_temp_c"])
elif page=="Alerts":
    st.title("Notifications & Alerts"); st.write("Thresholds:", THRESHOLDS)
    a=check_alerts(d); st.write(f"{len(a)} alerts for {station}"); st.write(a[:50] or "No alerts.")
elif page=="Support":
    st.title("Feedback & Support")
    with st.form("support"):
        msg=st.text_area("Describe your issue / feedback")
        if st.form_submit_button("Submit") and msg:
            with open(pathlib.Path(__file__).parent/"data"/"support_tickets.txt","a") as fh: fh.write(f"{user}: {msg}\n")
            st.success("Ticket saved.")
else:
    st.title("Admin - Support Tickets")
    f=pathlib.Path(__file__).parent/"data"/"support_tickets.txt"
    st.write(f.read_text() if f.exists() else "No tickets yet.")
