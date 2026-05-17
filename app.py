import streamlit as st
from datetime import date

st.set_page_config(page_title="Day By Day", layout="wide")
st.title("🚗 Day By Day")
st.markdown("**Your daily tracker • Built for real life**")

if 'data' not in st.session_state:
    st.session_state.data = {"daily_logs": {}}

data = st.session_state.data

def add_dash(income, spending, minutes, miles, count=1):
    today = str(date.today())
    if today not in data["daily_logs"]:
        data["daily_logs"][today] = []
    
    data["daily_logs"][today].append({
        "income": income,
        "spending": spending,
        "minutes": minutes,
        "miles": miles,
        "count": count,
        "time": date.today().strftime("%H:%M")
    })

# Sidebar
with st.sidebar:
    st.header("Quick Add Dash")
    income = st.number_input("Income ($)", value=0.0, step=0.01)
    spending = st.number_input("Spending ($)", value=0.0, step=0.01)
    minutes = st.number_input("Active Minutes", value=0, step=1)
    miles = st.number_input("Miles Driven", value=0.0, step=0.1)
    count = st.number_input("Dash Count", value=1, step=1)
    
    if st.button("✅ Add to Log"):
        add_dash(income, spending, minutes, miles, count)
        st.success("Added successfully!")
        st.rerun()

# Today
today = str(date.today())
dashes = data["daily_logs"].get(today, [])
total_income = sum(d["income"] for d in dashes)
total_spending = sum(d["spending"] for d in dashes)

st.metric("Net Today", f"${total_income - total_spending:.2f}")
st.metric("Income", f"${total_income:.2f}")
st.metric("Spending", f"${total_spending:.2f}")
st.metric("Dashes Today", len(dashes))

st.caption("Day By Day - Minimal Stable Version")
