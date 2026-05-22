import streamlit as st
from datetime import date

st.set_page_config(page_title="Day By Day", layout="wide")
st.title("🚗 Day By Day")
st.markdown("**Your daily tracker • Built for real life**")

# Simple data storage
if 'daily_logs' not in st.session_state:
    st.session_state.daily_logs = {}

def add_dash(income=0.0, spending=0.0, minutes=0, miles=0.0, count=1):
    today = str(date.today())
    if today not in st.session_state.daily_logs:
        st.session_state.daily_logs[today] = []
    
    st.session_state.daily_logs[today].append({
        "income": round(float(income), 2),
        "spending": round(float(spending), 2),
        "minutes": int(minutes),
        "miles": round(float(miles), 1),
        "count": int(count),
        "time": date.today().strftime("%H:%M")
    })

# Sidebar Input
with st.sidebar:
    st.header("Quick Add Dash")
    
    income = st.number_input("Income ($)", value=0.0, step=0.01)
    spending = st.number_input("Spending ($)", value=0.0, step=0.01)
    minutes = st.number_input("Active Minutes", value=0, step=1)
    miles = st.number_input("Miles Driven", value=0.0, step=0.1)
    count = st.number_input("Dash Count", value=1, step=1)
    
    if st.button("✅ Add to Log", type="primary"):
        add_dash(income, spending, minutes, miles, count)
        st.success("✅ Added successfully!")
        st.rerun()

# Main Display
today = str(date.today())
dashes = st.session_state.daily_logs.get(today, [])

total_income = sum(d["income"] for d in dashes)
total_spending = sum(d["spending"] for d in dashes)

st.metric("Net Today", f"${total_income - total_spending:.2f}")
st.metric("Income Today", f"${total_income:.2f}")
st.metric("Spending Today", f"${total_spending:.2f}")
st.metric("Dashes Today", len(dashes))

st.caption("Day By Day - Clean Foundation")