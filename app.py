# ===============================
# STREAMLIT UI FOR SAVINGS PREDICTION (ENHANCED)
# ===============================

import streamlit as st

# 🚨 MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Personal Savings Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np
import joblib
from pathlib import Path

# ===============================
# STYLING
# ===============================
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .css-1d391kg {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        font-weight: 700;
    }
    h2, h3 {
        color: #34495e;
    }
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ===============================
# PATHS
# ===============================
MODEL_VERSION = "v1"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / f"random_forest_{MODEL_VERSION}.joblib"
FEATURES_PATH = PROJECT_ROOT / "models" / f"random_forest_features_{MODEL_VERSION}.pkl"
APP_DIR = Path(__file__).parent

# ===============================
# LOAD MODEL & FEATURES
# ===============================
#@st.cache_resource

def load_model_and_features():
    model = joblib.load(APP_DIR / f"random_forest_{MODEL_VERSION}.joblib")
    feature_names = joblib.load(APP_DIR / f"random_forest_features_{MODEL_VERSION}.pkl")
    return model, feature_names

model, FEATURE_NAMES = load_model_and_features()


# ===============================
# UI HEADER
# ===============================
st.title("💰 Personal Savings Prediction System")

st.markdown(
    """
    <div style='text-align: center; padding: 20px; background: white; border-radius: 10px; margin-bottom: 20px;'>
    <h3 style='color: #667eea;'>AI-Powered Financial Insights</h3>
    <p>This application predicts <b>Desired Savings</b> based on income and spending behavior 
    using a <b>Random Forest Machine Learning model</b>.</p>
    <p style='color: #7f8c8d;'>It demonstrates <b>training–serving consistency</b>, a key MLOps principle.</p>
    </div>
    """, unsafe_allow_html=True
)

# ===============================
# SIDEBAR INPUTS WITH SLIDERS
# ===============================
st.sidebar.header("📥 Enter Financial Details")

st.sidebar.markdown("### 💼 Personal Information")
Income = st.sidebar.slider("Income (₹)", min_value=10000, max_value=500000, value=50000, step=5000, 
                           help="Your monthly income")
Age = st.sidebar.slider("Age", min_value=18, max_value=80, value=30, step=1,
                        help="Your current age")
Dependents = st.sidebar.slider("Dependents", min_value=0, max_value=10, value=1, step=1,
                               help="Number of dependents")

st.sidebar.markdown("### 🏠 Housing & Utilities")
Rent = st.sidebar.slider("Rent (₹)", min_value=0, max_value=100000, value=12000, step=1000,
                         help="Monthly rent")
Utilities = st.sidebar.slider("Utilities (₹)", min_value=0, max_value=10000, value=2500, step=500,
                              help="Electricity, water, internet, etc.")

st.sidebar.markdown("### 🛒 Daily Expenses")
Groceries = st.sidebar.slider("Groceries (₹)", min_value=0, max_value=30000, value=6000, step=500,
                              help="Monthly grocery expenses")
Transport = st.sidebar.slider("Transport (₹)", min_value=0, max_value=20000, value=3000, step=500,
                              help="Fuel, public transport, etc.")

st.sidebar.markdown("### 🎓 Health & Education")
Healthcare = st.sidebar.slider("Healthcare (₹)", min_value=0, max_value=20000, value=2000, step=500,
                               help="Medical expenses")
Education = st.sidebar.slider("Education (₹)", min_value=0, max_value=50000, value=3000, step=1000,
                              help="Tuition, courses, books, etc.")

st.sidebar.markdown("### 🎮 Lifestyle")
Entertainment = st.sidebar.slider("Entertainment (₹)", min_value=0, max_value=20000, value=2500, step=500,
                                  help="Movies, dining, hobbies, etc.")
Miscellaneous = st.sidebar.slider("Miscellaneous (₹)", min_value=0, max_value=20000, value=2000, step=500,
                                  help="Other expenses")

# ===============================
# RAW USER INPUT (PARTIAL FEATURES)
# ===============================
user_input = {
    "Income": Income,
    "Age": Age,
    "Dependents": Dependents,
    "Rent": Rent,
    "Groceries": Groceries,
    "Transport": Transport,
    "Utilities": Utilities,
    "Healthcare": Healthcare,
    "Education": Education,
    "Entertainment": Entertainment,
    "Miscellaneous": Miscellaneous
}

# ===============================
# ALIGN INPUT WITH TRAINING FEATURES
# ===============================
model_input = pd.DataFrame(columns=FEATURE_NAMES)
model_input.loc[0] = 0.0

for feature, value in user_input.items():
    if feature in model_input.columns:
        model_input.at[0, feature] = value

# ===============================
# PREDICTION
# ===============================
prediction = model.predict(model_input)[0]

# ===============================
# CALCULATIONS
# ===============================
expenses = {
    "Rent": Rent,
    "Groceries": Groceries,
    "Transport": Transport,
    "Utilities": Utilities,
    "Healthcare": Healthcare,
    "Education": Education,
    "Entertainment": Entertainment,
    "Miscellaneous": Miscellaneous
}

total_expenses = sum(expenses.values())
actual_savings = Income - total_expenses
savings_rate = (actual_savings / Income * 100) if Income > 0 else 0
predicted_savings_rate = (prediction / Income * 100) if Income > 0 else 0

# ===============================
# KPI METRICS
# ===============================
st.markdown("## 📊 Financial Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💵 Monthly Income",
        value=f"₹ {Income:,.0f}",
        delta=None
    )

with col2:
    st.metric(
        label="💸 Total Expenses",
        value=f"₹ {total_expenses:,.0f}",
        delta=f"{(total_expenses/Income*100):.1f}% of income",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="💰 Predicted Savings",
        value=f"₹ {prediction:,.0f}",
        delta=f"{predicted_savings_rate:.1f}% savings rate"
    )

with col4:
    st.metric(
        label="📈 Actual Savings",
        value=f"₹ {actual_savings:,.0f}",
        delta=f"₹ {prediction - actual_savings:,.0f} difference",
        delta_color="off" if abs(prediction - actual_savings) < 1000 else "normal"
    )

# ===============================
# MAIN VISUALIZATIONS
# ===============================
st.markdown("---")
st.markdown("## 📈 Interactive Visualizations")

# Create tabs for different visualizations
tab1, tab2, tab3, tab4 = st.tabs(["💸 Expense Analysis", "📊 Financial Comparison", "🎯 Savings Goals", "🔍 Model Insights"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Interactive Pie Chart using Plotly
        st.markdown("### 🥧 Expense Distribution")
        fig_pie = px.pie(
            values=list(expenses.values()),
            names=list(expenses.keys()),
            title="Monthly Expense Breakdown",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            showlegend=True,
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Horizontal Bar Chart
        st.markdown("### 📊 Category-wise Spending")
        expense_df = pd.DataFrame(list(expenses.items()), columns=['Category', 'Amount'])
        expense_df = expense_df.sort_values('Amount', ascending=True)
        
        fig_bar = px.bar(
            expense_df,
            x='Amount',
            y='Category',
            orientation='h',
            title="Spending by Category",
            color='Amount',
            color_continuous_scale='Viridis',
            text='Amount'
        )
        fig_bar.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        fig_bar.update_layout(
            showlegend=False,
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Income vs Expenses vs Savings
        st.markdown("### 💵 Financial Comparison")
        comparison_data = {
            'Category': ['Income', 'Expenses', 'Actual Savings', 'Predicted Savings'],
            'Amount': [Income, total_expenses, actual_savings, prediction]
        }
        fig_comparison = go.Figure(data=[
            go.Bar(
                x=comparison_data['Category'],
                y=comparison_data['Amount'],
                text=comparison_data['Amount'],
                texttemplate='₹%{text:,.0f}',
                textposition='outside',
                marker=dict(
                    color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'],
                    line=dict(color='rgb(8,48,107)', width=1.5)
                )
            )
        ])
        fig_comparison.update_layout(
            title="Income, Expenses & Savings Overview",
            yaxis_title="Amount (₹)",
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    with col2:
        # Waterfall Chart
        st.markdown("### 🌊 Cash Flow Waterfall")
        fig_waterfall = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "relative", 
                     "relative", "relative", "relative", "total"],
            x=["Income"] + list(expenses.keys()) + ["Net Savings"],
            textposition="outside",
            text=[f"₹{Income:,.0f}"] + [f"-₹{v:,.0f}" for v in expenses.values()] + [f"₹{actual_savings:,.0f}"],
            y=[Income] + [-v for v in expenses.values()] + [actual_savings],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#e74c3c"}},
            increasing={"marker": {"color": "#2ecc71"}},
            totals={"marker": {"color": "#3498db"}}
        ))
        fig_waterfall.update_layout(
            title="Monthly Cash Flow",
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Gauge Chart for Savings Rate
        st.markdown("### 🎯 Savings Rate Gauge")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=predicted_savings_rate,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Predicted Savings Rate (%)", 'font': {'size': 24}},
            delta={'reference': 20, 'suffix': '%'},
            gauge={
                'axis': {'range': [None, 50], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 10], 'color': '#e74c3c'},
                    {'range': [10, 20], 'color': '#f39c12'},
                    {'range': [20, 50], 'color': '#2ecc71'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 20
                }
            }
        ))
        fig_gauge.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "darkblue", 'family': "Arial"}
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.info("💡 **Tip**: A savings rate of 20% or higher is considered healthy!")
    
    with col2:
        # Savings Projection
        st.markdown("### 📅 1-Year Savings Projection")
        months = list(range(1, 13))
        projected_savings = [prediction * i for i in months]
        
        fig_projection = px.area(
            x=months,
            y=projected_savings,
            labels={'x': 'Month', 'y': 'Cumulative Savings (₹)'},
            title="Projected Annual Savings Growth"
        )
        fig_projection.update_traces(
            line_color='#3498db',
            fillcolor='rgba(52, 152, 219, 0.3)'
        )
        fig_projection.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_projection, use_container_width=True)
        
        st.success(f"💰 **12-Month Target**: ₹ {prediction * 12:,.0f}")

with tab4:
    st.markdown("### 🔍 Feature Importance Analysis")
    
    importances = model.feature_importances_
    importance_df = pd.DataFrame({
        "Feature": FEATURE_NAMES,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False).head(15)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Interactive Feature Importance Chart
        fig_importance = px.bar(
            importance_df,
            x='Importance',
            y='Feature',
            orientation='h',
            title="Top 15 Most Important Features",
            color='Importance',
            color_continuous_scale='RdYlGn',
            text='Importance'
        )
        fig_importance.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig_importance.update_layout(
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_importance, use_container_width=True)
    
    with col2:
        st.markdown("#### 📝 Interpretation")
        st.markdown("""
        **Feature Importance** shows how much each factor influences the savings prediction.
        
        - **Higher values** = stronger influence
        - **Income** typically has the highest impact
        - **Expense categories** show spending patterns
        
        The model considers all these factors to make accurate predictions.
        """)
        
        # Top 3 features
        st.markdown("#### 🏆 Top 3 Features")
        for idx, row in importance_df.head(3).iterrows():
            st.markdown(f"**{row['Feature']}**: {row['Importance']:.4f}")

# ===============================
# INSIGHTS & RECOMMENDATIONS
# ===============================
st.markdown("---")
st.markdown("## 💡 Personalized Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🎯 Savings Status")
    if actual_savings < 0:
        st.error("⚠️ You're spending more than you earn!")
        st.markdown("Consider reducing expenses or increasing income.")
    elif savings_rate < 10:
        st.warning("⚡ Your savings rate is low (< 10%)")
        st.markdown("Try to save at least 20% of your income.")
    elif savings_rate < 20:
        st.info("👍 You're saving, but there's room for improvement")
        st.markdown("Aim for a 20-30% savings rate.")
    else:
        st.success("🌟 Excellent savings rate!")
        st.markdown("You're on track for financial security.")

with col2:
    st.markdown("### 📉 Biggest Expenses")
    top_3_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)[:3]
    for i, (category, amount) in enumerate(top_3_expenses, 1):
        pct = (amount / total_expenses * 100) if total_expenses > 0 else 0
        st.markdown(f"{i}. **{category}**: ₹{amount:,.0f} ({pct:.1f}%)")

with col3:
    st.markdown("### 🚀 Quick Tips")
    st.markdown("""
    - 🏠 Housing should be < 30% of income
    - 🍕 Food should be < 15% of income
    - 💰 Save at least 20% of income
    - 📊 Review expenses monthly
    - 🎯 Set specific savings goals
    """)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 20px; background: white; border-radius: 10px;'>
    <p>📌 <i>This application demonstrates deployment-safe inference using a trained ML model 
    with strict feature schema alignment (MLOps best practice).</i></p>
    <p style='color: #7f8c8d; margin-top: 10px;'>Built with ❤️ using Streamlit, Plotly & Scikit-learn</p>
    </div>
    """,
    unsafe_allow_html=True
)

