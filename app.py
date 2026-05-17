# =====================================================
# Day By Day - Safe Version (Step 11)
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

def load_data():
    if CURRENT_FILE.exists():
        try:
            with open(CURRENT_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"daily_logs": {}}

def save_data(data):
    with open(CURRENT_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()

def add_dash(income: float, spending: float, minutes: int, miles: float, dash_count: int = 1):
    global data
    today_str = str(date.today())
    
    if today_str not in data["daily_logs"]:
        data["daily_logs"][today_str] = []
    
    new_dash = {
        "income": round(income, 2),
        "spending": round(spending, 2),
        "minutes": minutes,
        "miles": round(miles, 1),
        "count": dash_count,
        "time": date.today().strftime("%H:%M")
    }
    
    data["daily_logs"][today_str].append(new_dash)
    save_data(data)
    return len(data["daily_logs"][today_str])

# Sidebar
with st.sidebar:
    st.header("Quick Add Dash")
    
    income_str = st.text_input("Income ($)", value="", placeholder="0.00")
    spending_str = st.text_input("Spending ($)", value="", placeholder="0.00")
    minutes_str = st.text_input("Active Minutes", value="", placeholder="0")
    miles_str = st.text_input("Miles Driven", value="", placeholder="0.0")
    dashes = st.number_input("Dash Count", value=1, step=1)
   
    if st.button("✅ Add to Log", type="primary"):
        try:
            income = float(income_str) if income_str.strip() else 0.0
            spending = float(spending_str) if spending_str.strip() else 0.0
            minutes = int(minutes_str) if minutes_str.strip() else 0
            miles = float(miles_str) if miles_str.strip() else 0.0
            
            iter
