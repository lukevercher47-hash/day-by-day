# =====================================================
# Day By Day - Stable & Simple Version
# =====================================================
import streamlit as st
from datetime import date

st.set_page_config(page_title="Day By Day", layout="wide")
st.title("🚗 Day By Day")
st.markdown("**Your daily tracker • Built for real life**")

# Simple persistent storage using session state (stable on cloud)
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
    
    income = st.number_input("Income ($)", value=0.0, step=0.01)
    spending = st.number_input("Spending ($)", value=0.0, step=0.01)
    minutes = st.number_input("Active Minutes", value=0, step=1)
    miles = st.number_input("Miles Driven", value=0.0, step=0.1)
    count = st.number_input("Dash Count", value=1, step=1)
    
    if st.button("✅ Add to Log", type="primary"):
        add_dash(income, spending, minutes, miles, count)
        st.success("✅ Added successfully!")
        st.rerun()

# ====================== TABS ======================
tab1, tab2, tab3 = st.tabs(["📊 Today", "📅 History", "📈 Stats"])

with tab1:
    today = str(date.today())
    dashes = st.session_state.daily_logs.get(today, [])
    
    total_income = sum(d["income"] for d in dashes)
    total_spending = sum(d["spending"] for d in dashes)
    net = total_income - total_spending
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Net Today", f"${net:.2f}")
    col2.metric("Income", f"${total_income:.2f}")
    col3.metric("Spending", f"${total_spending:.2f}")
    col4.metric("Dashes", len(dashes))

with tab2:
    st.subheader("Daily History")
    for day in sorted(st.session_state.daily_logs.keys(), reverse=True):
        dashes = st.session_state.daily_logs[day]
        total = sum(d["income"] for d in dashes)
        with st.expander(f"{day} — Net ${total - sum(d['spending'] for d in dashes):.2f}"):
            for i, d in enumerate(dashes, 1):
                st.write(f"Dash {i} @ {d['time']} | +${d['income']:.2f} | -${d['spending']:.2f} | {d['minutes']}min | {d['miles']}mi")

with tab3:
    st.subheader("Lifetime Stats")
    all_dashes = [d for day_dashes in st.session_state.daily_logs.values() for d in day_dashes]
    total_income = sum(d["income"] for d in all_dashes)
    total_spending = sum(d["spending"] for d in all_dashes)
    st.metric("Total Earned", f"${total_income:.2f}")
    st.metric("Total Spent", f"${total_spending:.2f}")

st.caption("Day By Day • Stable Version")
