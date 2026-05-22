# =====================================================
# Day By Day - Clean Foundation v1
# =====================================================
import streamlit as st
from datetime import date
import json
from pathlib import Path

st.set_page_config(page_title="Day By Day", layout="wide")
st.title("🚗 Day By Day")
st.markdown("**Your daily tracker • Built for real life**")

# Data storage setup
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

# Add a new dash
def add_dash(income=0.0, spending=0.0, minutes=0, miles=0.0, count=1):
    global data
    today = str(date.today())
    if today not in data["daily_logs"]:
        data["daily_logs"][today] = []
    
    data["daily_logs"][today].append({
        "income": round(float(income), 2),
        "spending": round(float(spending), 2),
        "minutes": int(minutes),
        "miles": round(float(miles), 1),
        "count": int(count),
        "time": date.today().strftime("%H:%M")
    })
    save_data(data)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("Quick Add Dash")
    
    income = st.number_input("Income ($)", value=0.0, step=0.01, format="%.
