import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="PocketSmart AI", page_icon="💰")

# Title
st.title("💰 PocketSmart AI")
st.subheader("Your Smart Budget & Recommendation Assistant")

# Sidebar - Budget Setup
st.sidebar.header("Budget Setup")
monthly_income = st.sidebar.number_input("Monthly Income (Rs)", value=20000)
food_budget = st.sidebar.number_input("Food Budget", value=5000)
travel_budget = st.sidebar.number_input("Travel Budget", value=3000)
shopping_budget = st.sidebar.number_input("Shopping Budget", value=4000)

# Initialize expenses
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Add Expense Form
st.header("➕ Add New Expense")
col1, col2, col3 = st.columns(3)
with col1:
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Others"])
with col2:
    amount = st.number_input("Amount Rs", min_value=1, value=100)
with col3:
    date = st.date_input("Date", datetime.now())

if st.button("Add Expense"):
    st.session_state.expenses.append({
        "Category": category,
        "Amount": amount,
        "Date": date
    })
    st.success(f"Added Rs.{amount} for {category}")

# Dashboard
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    st.header("📊 Your Spending Dashboard")
    
    total_spent = df['Amount'].sum()
    remaining = monthly_income - total_spent
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Spent", f"Rs.{total_spent}")
    c2.metric("Remaining", f"Rs.{remaining}")
    c3.metric("Income", f"Rs.{monthly_income}")

    # Pie Chart
    st.subheader("Category-wise Spending")
    fig, ax = plt.subplots()
    df.groupby('Category')['Amount'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    st.pyplot(fig)
    
    # Data Table
    st.dataframe(df)

    # --- PocketSmart AI RECOMMENDATION ENGINE ---
    st.header("🤖 PocketSmart AI Suggestions")
    
    food_spent = df[df['Category'] == 'Food']['Amount'].sum()
    if food_spent > food_budget:
        st.warning(f"⚠️ Food la budget cross pannitta! Neenga Rs.{food_spent - food_budget} adhigama selavu panitteenga. Adutha vaaram home food try pannunga.")
    elif food_spent > food_budget * 0.8:
        st.info("💡 Food budget 80% mudinjiduchu. Konjam control pannunga.")
    
    if total_spent > monthly_income * 0.9:
        st.error("🚨 Danger! Month mudiya munadiye 90% income kaliyaniduchu. Ippa irundhu saving mode on pannunga!")
    elif remaining < 2000:
        st.warning("Purse kaali aaga poguthu! Shopping-a konjam thallipodalam.")
    else:
        st.success("✅ Super! Neenga budget-a nalla manage panreenga. Ippadiye continue pannunga.")

    if remaining > 5000:
        st.success(f"🎉 Congratulations! Neenga indha maasam Rs.{remaining} save panna mudiyum. Adha SIP la invest pannalam.")

else:
    st.info("Innum expense add pannala. Mela add pannunga, AI suggestion varum.")