# =====================================================
# Day By Day - Scooby's Tracker
# =====================================================
import streamlit as st
import pandas as pd
from datetime import date
import json
from pathlib import Path

st.set_page_config(page_title="Day By Day", layout="wide")
st.title("🚗 Day By Day")
st.markdown("**Your daily tracker • Built for real life**")

DATA_DIR = Path("dash_data")
DATA_DIR.mkdir(exist_ok=True)
CURRENT_FILE = DATA_DIR / "current_session.json"
BACKUP_DIR = DATA_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

def load_data():
    if CURRENT_FILE.exists():
        try:
            with open(CURRENT_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"daily_logs": {}, "goals": [], "last_iteration": 0}

def save_data(data):
    with open(CURRENT_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()

# ====================== ADD DASH ======================
def add_dash(income: float, spending: float, minutes: int, miles: float, dash_count: int = 1):
    global data
    today_str = str(date.today())
   
    if today_str not in data["daily_logs"]:
        data["daily_logs"][today_str] = {
            "income": 0.0, "spending": 0.0, "dashes": 0,
            "miles": 0.0, "active_minutes": 0, "iteration": 0
        }
   
    day = data["daily_logs"][today_str]
    day["income"] += income
    day["spending"] += spending
    day["dashes"] += dash_count
    day["miles"] += miles
    day["active_minutes"] += minutes
    day["iteration"] += 1
   
    save_data(data)
    return day["iteration"]

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("Quick Add Dash")
    
    # Clean text inputs instead of number inputs
    income_str = st.text_input("Income ($)", value="0.00", key="income")
    spending_str = st.text_input("Spending ($)", value="0.00", key="spending")
    minutes = st.number_input("Active Minutes", value=0, step=1)
    miles = st.number_input("Miles Driven", value=0.0, step=0.1)
    dashes = st.number_input("Dash Count", value=1, step=1)
   
    if st.button("✅ Add to Log", type="primary"):
        try:
            income = float(income_str) if income_str else 0.0
            spending = float(spending_str) if spending_str else 0.0
            iter_num = add_dash(income, spending, minutes, miles, dashes)
            st.success(f"Added! Iteration {iter_num}")
        except:
            st.error("Please enter valid numbers")

    st.divider()
    if st.button("🗑️ Reset All Data", type="secondary"):
        if st.checkbox("Are you sure? This cannot be undone"):
            CURRENT_FILE.unlink(missing_ok=True)
            st.success("All data cleared! Refresh the page.")
            st.rerun()

# ====================== MAIN TABS ======================
tab1, tab2, tab3 = st.tabs(["📊 Today", "📅 History", "📈 Stats"])

with tab1:
    today_str = str(date.today())
    today = data["daily_logs"].get(today_str, {"income":0,"spending":0,"dashes":0,"miles":0,"active_minutes":0})
   
    net = today["income"] - today["spending"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Net Today", f"${net:.2f}")
    col2.metric("Income", f"${today['income']:.2f}")
    col3.metric("Spending", f"${today['spending']:.2f}")
    col4.metric("Dashes", today["dashes"])

with tab2:
    st.subheader("Daily History")
    if data["daily_logs"]:
        df = pd.DataFrame.from_dict(data["daily_logs"], orient="index")
        st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("Lifetime Stats")
    total_income = sum(d.get("income",0) for d in data["daily_logs"].values())
    total_spending = sum(d.get("spending",0) for d in data["daily_logs"].values())
    st.metric("Total Earned", f"${total_income:.2f}")
    st.metric("Total Spent", f"${total_spending:.2f}")

st.caption("Auto-saves • Day By Day")
