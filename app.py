# =====================================================
# Scooby's DoorDash Tracker - Improved Version
# Fixed: success messages, zero persistence, cleaner state
# =====================================================

import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
from pathlib import Path

st.set_page_config(page_title="Scooby Dash Tracker", layout="wide")
st.title("🚗 Scooby's DoorDash Tracker")
st.markdown("**Day By Day Mode**")

DATA_DIR = Path("dash_data")
DATA_DIR.mkdir(exist_ok=True)
CURRENT_FILE = DATA_DIR / "current_session.json"

def load_data():
    if CURRENT_FILE.exists():
        try:
            with open(CURRENT_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "current_date": str(date.today()),
        "income": 0.0,
        "spent": 0.0,
        "dashes": 0,
        "miles": 0.0,
        "active_minutes": 0,
        "dash_log": []
    }

def save_data(data):
    with open(CURRENT_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("Add New Dash")
    income = st.number_input("Income ($)", value=0.0, step=0.01, key="inc")
    minutes = st.number_input("Active Minutes", value=0, step=1, key="min")
    miles = st.number_input("Miles", value=0.0, step=0.1, key="mil")
    dash_count = st.number_input("Dash Count", value=1, step=1, key="cnt")
    
    if st.button("✅ Add Dash", type="primary"):
        data["income"] += income
        data["spent"] = data.get("spent", 0.0)
        data["dashes"] += dash_count
        data["miles"] += miles
        data["active_minutes"] += minutes
        
        data["dash_log"].append({
            "time": datetime.now().strftime("%I:%M %p"),
            "income": round(income, 2),
            "minutes": minutes,
            "miles": round(miles, 1),
            "count": dash_count
        })
        
        save_data(data)
        st.success(f"✅ Added ${income:.2f} | {dash_count} dash(es)")

    if st.button("Clear All Data"):
        if st.checkbox("Confirm clear all?"):
            data = load_data()  # reset
            save_data(data)
            st.success("All data cleared")

# ====================== MAIN DASHBOARD ======================
st.subheader("Today's Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Net", f"${data['income'] - data.get('spent',0):.2f}")
col2.metric("Income", f"${data['income']:.2f}")
col3.metric("Spent", f"${data.get('spent',0):.2f}")
col4.metric("Dashes", data["dashes"])

st.metric("Active Time", f"{data['active_minutes']//60}h {data['active_minutes']%60}m")
st.metric("Miles", f"{data['miles']:.1f}")

progress = min(data['income'] / 110, 1.0)
st.progress(progress, text=f"Progress to $110 — {progress*100:.1f}%")

# Dash Log
if data["dash_log"]:
    st.subheader("Dash Log")
    log_df = pd.DataFrame(data["dash_log"])
    st.dataframe(log_df, use_container_width=True)

st.caption("Auto-saved • Data in dash_data/ folder")