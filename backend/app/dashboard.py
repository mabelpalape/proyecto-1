import streamlit as st
import pandas as pd
import plotly.express as px
from sqlmodel import Session, select
import sys
import os

# Add backend to path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.core.db import engine, create_db_and_tables
from app.models.analysis import Recommendation, RFMProfile
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order # Fixes relationship resolution

st.set_page_config(page_title="E-commerce Predictive Analytics", layout="wide")

# Ensure tables exist (crucial for Streamlit Cloud where DB is ephemeral)
create_db_and_tables()

st.title("📊 Predictive Analytics & Recommendations")

def load_data():
    """Load recommendations from database, returns empty DataFrame if no data or error."""
    try:
        with Session(engine) as session:
            # Load Recommendations
            recs_query = select(Recommendation, Customer, Product).join(Customer).join(Product)
            recs = session.exec(recs_query).all()
            
            rec_data = []
            for r, c, p in recs:
                rec_data.append({
                    "Customer ID": c.customer_id,
                    "Customer Email": c.email,
                    "Product": p.product_name,
                    "Window": r.recommended_contact_window,
                    "Confidence": r.confidence_level,
                    "Reasoning": r.reasoning,
                    "Date": r.generated_date
                })
                
            if not rec_data:
                return pd.DataFrame(columns=[
                    "Customer ID", "Customer Email", "Product", 
                    "Window", "Confidence", "Reasoning", "Date"
                ])
                
            return pd.DataFrame(rec_data)
    except Exception as e:
        # If there's any error (table doesn't exist, config issue, etc), return empty DataFrame
        # This allows the app to load so user can click "Generate Mock Data"
        return pd.DataFrame(columns=[
            "Customer ID", "Customer Email", "Product", 
            "Window", "Confidence", "Reasoning", "Date"
        ])

df_recs = load_data()

# --- Metrics Section ---
col1, col2, col3 = st.columns(3)
if not df_recs.empty:
    col1.metric("Total Recommendations", len(df_recs))
    col2.metric("High Confidence", len(df_recs[df_recs['Confidence'] == 'high']))
    col3.metric("Urgent (Early/On-time)", len(df_recs[df_recs['Window'].isin(['Early Reminder', 'On-time'])]))

st.divider()

# --- Main View ---

# Filters
st.sidebar.header("Filters")
selected_window = st.sidebar.multiselect(
    "Contact Window", 
    options=df_recs['Window'].unique(),
    default=df_recs['Window'].unique()
)

if not df_recs.empty:
    filtered_df = df_recs[df_recs['Window'].isin(selected_window)]

    st.subheader("Actionable Recommendations")
    st.dataframe(
        filtered_df[['Customer ID', 'Customer Email', 'Product', 'Window', 'Confidence', 'Date']],
        use_container_width=True,
        selection_mode="single-row",
        on_select="rerun",
        key="rec_table"
    )

    # --- Detail View (Sidebar or Below) ---
    if len(st.session_state.rec_table.selection.rows) > 0:
        row_idx = st.session_state.rec_table.selection.rows[0]
        selected_row = filtered_df.iloc[row_idx]
        
        with st.sidebar:
            st.divider()
            st.subheader("Customer Insight")
            st.info(f"**Customer:** {selected_row['Customer Email']}")
            st.write(f"**Target Product:** {selected_row['Product']}")
            
            confidence_color = "green" if selected_row['Confidence'] == "high" else "orange"
            st.markdown(f"**Confidence:** :{confidence_color}[{selected_row['Confidence'].upper()}]")
            
            st.markdown("### 🧠 AI Reasoning")
            st.write(selected_row['Reasoning'])
            
            st.button("Mark as Contacted", key="contact_btn")

else:
    st.info("No recommendations found. Run the analytics pipeline first.")

st.sidebar.divider()
if st.sidebar.button("⚡ Generate Mock Data (Reset DB)"):
    try:
        with st.spinner("Generating 4 years of history..."):
            # Import here to avoid circulars or early exec issues if needed
            from app.core.db import create_db_and_tables
            from app.services.mock_data import create_mock_data
            from app.services.rfm import run_rfm_analysis
            from app.services.recommendation import run_recommendation_engine
            
            create_db_and_tables()
            create_mock_data()
            run_rfm_analysis()
            run_recommendation_engine()
        st.success("Data generated! Refreshing...")
        st.rerun()
    except Exception as e:
        st.error(f"Error generating data: {str(e)}")
        st.error("Please check the logs for details or try again.")

# --- Analytics / RFM Charts ---
st.divider()
st.subheader("Analytics Overview")

if not df_recs.empty:
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.write("**Recommendations by Window**")
        fig_window = px.pie(df_recs, names='Window', hole=0.4)
        st.plotly_chart(fig_window, use_container_width=True)
        
    with chart_col2:
        st.write("**Confidence Distribution**")
        fig_conf = px.bar(df_recs, x='Confidence', color='Confidence')
        st.plotly_chart(fig_conf, use_container_width=True)
