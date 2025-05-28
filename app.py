import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.container_database import ContainerDatabase
from utils.calculations import StructuralCalculations

# Page configuration
st.set_page_config(
    page_title="Steel Container Sales Calculator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'container_db' not in st.session_state:
    st.session_state.container_db = ContainerDatabase()

if 'calculations' not in st.session_state:
    st.session_state.calculations = StructuralCalculations()

# Main dashboard
st.title("🏗️ Steel Container Sales Calculator")
st.markdown("*AI-Powered Cost Estimation for Container Modifications*")

# Sidebar navigation info
with st.sidebar:
    st.header("Navigation")
    st.markdown("""
    **Pages Available:**
    1. 📦 Container Configurator
    2. 🤖 AI Cost Estimator  
    3. 🔧 Technical Analysis
    4. 📋 Quote Generator
    5. ⚖️ Comparison Tool
    """)
    
    st.divider()
    st.subheader("Quick Stats")
    
    # Display some quick statistics
    container_types = st.session_state.container_db.get_container_types()
    st.metric("Available Container Types", len(container_types))
    st.metric("Standard Sizes", "6 (20ft, 40ft, 45ft, 48ft, 53ft, Custom)")
    st.metric("Modification Categories", "8")

# Main dashboard content
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Quick Overview")
    st.markdown("""
    **Container Modification Services:**
    - Structural reinforcements
    - Custom openings & windows
    - Insulation & HVAC systems
    - Electrical installations
    - Plumbing & utilities
    - Interior fit-outs
    """)

with col2:
    st.subheader("🎯 Key Features")
    st.markdown("""
    **AI-Powered Analysis:**
    - Intelligent cost estimation
    - Technical feasibility check
    - Material optimization
    - Compliance verification
    - Risk assessment
    - Timeline prediction
    """)

with col3:
    st.subheader("💼 Sales Tools")
    st.markdown("""
    **Professional Outputs:**
    - Detailed quotes
    - Technical specifications
    - 3D visualizations
    - Cost comparisons
    - Project timelines
    - Compliance reports
    """)

st.divider()

# Recent activity and quick actions
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Market Insights")
    
    # Sample market data visualization
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    steel_prices = [2800, 2850, 2920, 3100, 3050, 2980, 3150, 3200, 3180, 3250, 3300, 3280]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, 
        y=steel_prices,
        mode='lines+markers',
        name='Steel Price ($/ton)',
        line=dict(color='#1f77b4', width=3)
    ))
    
    fig.update_layout(
        title="Steel Price Trends 2024",
        xaxis_title="Month",
        yaxis_title="Price (USD/ton)",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🚀 Quick Actions")
    
    if st.button("🆕 New Container Project", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")
    
    if st.button("💰 Get AI Cost Estimate", use_container_width=True):
        st.switch_page("pages/2_AI_Cost_Estimator.py")
    
    if st.button("🔍 Technical Analysis", use_container_width=True):
        st.switch_page("pages/3_Technical_Analysis.py")
    
    if st.button("📄 Generate Quote", use_container_width=True):
        st.switch_page("pages/4_Quote_Generator.py")
    
    st.divider()
    
    st.subheader("💡 Tips")
    st.info("""
    **Best Practices:**
    - Start with Container Configurator
    - Use AI Cost Estimator for accuracy
    - Run Technical Analysis for compliance
    - Generate professional quotes
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
<p>Steel Container Sales Calculator v1.0 | Built with Streamlit & AI</p>
<p>For technical support, contact your system administrator</p>
</div>
""", unsafe_allow_html=True)
