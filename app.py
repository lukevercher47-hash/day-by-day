# =====================================================
# Day By Day - Clean Input + Reliable Add
# =====================================================
import streamlit as st
from datetime import date

st.set_page_config(page_title="Day By Day", layout="wide")
st.title("🚗 Day By Day")
st.markdown("**Your daily tracker • Built for real life**")

# Simple persistent storage
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

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("Quick Add Dash")
    
    income_str = st.text_input("Income ($)", value="", placeholder="0.00", key="inc")
    spending_str = st.text_input("Spending ($)", value="", placeholder="0.00", key="spend")
    minutes_str = st.text_input("Active Minutes", value="", placeholder="0", key="min")
    miles_str = st.text_input("Miles Driven", value="", placeholder="0.0", key="mil")
    count = st.number_input("Dash Count", value=1, step=1)
    
    if st.button("✅ Add to Log", type="primary"):
        try:
            income = float(income_str) if income_str.strip() else 0.0
            spending = float(spending_str) if spending_str.strip() else 0.0
            minutes = int(minutes_str) if minutes_str.strip() else 0
            miles = float(miles_str) if miles_str.strip() else 0.0
            
            add_dash(income, spending, minutes, miles, count)
            st.success("✅ Added successfully!")
            st.rerun()
        except:
            st.error("Please enter valid numbers only")

# ====================== TODAY ======================
today = str(date.today())
dashes = st.session_state.daily_logs.get(today, [])
total_income = sum(d["income"] for d in dashes)
total_spending = sum(d["spending"] for d in dashes)

st.metric("Net Today", f"${total_income - total_spending:.2f}")
st.metric("Income", f"${total_income:.2f}")
st.metric("Spending", f"${total_spending:.2f}")
st.metric("Dashes Today", len(dashes))

st.caption("Day By Day • Clean Input Version")