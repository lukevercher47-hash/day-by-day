# =====================================================
# Day By Day - Stable & Forgiving Version
# =====================================================
import streamlit as st
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

def add_dash(income=0.0, spending=0.0, minutes=0, miles=0.0, count=1):
    global data
    today = str(date.today())
    if today not in data["daily_logs"]:
        data["daily_logs"][today] = []
    
    data["daily_logs"][today].append({
        "income": round(income, 2),
        "spending": round(spending, 2),
        "minutes": minutes,
        "miles": round(miles, 1),
        "count": count,
        "time": date.today().strftime("%H:%M")
    })
    save_data(data)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("Quick Add Dash")
    income = st.number_input("Income ($)", value=0.0, step=0.01)
    spending = st.number_input("Spending ($)", value=0.0, step=0.01)
    minutes = st.number_input("Active Minutes", value=0, step=1)
    miles = st.number_input("Miles Driven", value=0.0, step=0.1)
    count = st.number_input("Dash Count", value=1, step=1)
    
    if st.button("✅ Add to Log"):
        add_dash(income, spending, minutes, miles, count)
        st.success("✅ Added!")
        st.rerun()

# ====================== TABS ======================
tab1, tab2, tab3 = st.tabs(["📊 Today", "📅 History", "📈 Stats"])

with tab1:
    today = str(date.today())
    dashes = data["daily_logs"].get(today, [])
    total_income = sum(d.get("income", 0) for d in dashes)
    total_spending = sum(d.get("spending", 0) for d in dashes)
    
    st.metric("Net Today", f"${total_income - total_spending:.2f}")
    st.metric("Income", f"${total_income:.2f}")
    st.metric("Spending", f"${total_spending:.2f}")
    st.metric("Dashes Today", len(dashes))

with tab2:
    st.subheader("Daily History")
    for day in sorted(data["daily_logs"].keys(), reverse=True):
        dashes = data["daily_logs"][day]
        total = sum(d.get("income", 0) for d in dashes)
        with st.expander(f"{day} — ${total:.2f}"):
            for i, d in enumerate(dashes, 1):
                st.write(f"Dash {i} @ {d.get('time','')} | +${d.get('income',0):.2f} | -${d.get('spending',0):.2f}")

with tab3:
    st.subheader("Lifetime Stats")
    all_dashes = [d for day_dashes in data["daily_logs"].values() for d in day_dashes]
    total_income = sum(d.get("income", 0) for d in all_dashes)
    total_spending = sum(d.get("spending", 0) for d in all_dashes)
    st.metric("Total Earned", f"${total_income:.2f}")
    st.metric("Total Spent", f"${total_spending:.2f}")

st.caption("Day By Day - Stable Version")