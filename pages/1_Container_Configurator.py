
import streamlit as st
import pandas as pd
from utils.container_database import ContainerDatabase
from utils.calculations import calculate_container_cost
from utils.translations import t, get_current_language

# Page configuration
st.set_page_config(
    page_title="Container Configurator - KAN-BUD",
    page_icon="📦",
    layout="wide"
)

# Initialize database
if 'container_db' not in st.session_state:
    st.session_state.container_db = ContainerDatabase()

st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
.header-title {
    color: white;
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}
.header-subtitle {
    color: #e8f4f8;
    font-size: 1.2rem;
    text-align: center;
}
.config-section {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid #e8f4f8;
    margin-bottom: 2rem;
}
.section-title {
    color: #2E86AB;
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e8f4f8;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="main-header">
    <div class="header-title">📦 {t('nav.container_configurator')}</div>
    <div class="header-subtitle">Professional container modification configurator</div>
</div>
""", unsafe_allow_html=True)

# Navigation
col1, col2 = st.columns(2)
with col1:
    current_language = get_current_language()
    home_text = t('ui.back_to_home')
    if st.button(home_text, key="home_nav", use_container_width=True):
        st.switch_page("app.py")

with col2:
    ai_text = t('ui.go_to_ai_estimate')
    if st.button(ai_text, key="ai_nav", use_container_width=True):
        st.switch_page("pages/2_AI_Cost_Estimator.py")

# Configuration form
st.markdown(f'<div class="config-section"><div class="section-title">🏗️ {t("container.types.20ft_standard").split()[0]} Configuration</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Container type
    container_type = st.selectbox(
        t('form.labels.container_type'),
        ["20ft Standard", "40ft Standard", "40ft High Cube", "20ft Refrigerated"],
        key="container_type"
    )
    
    # Main purpose
    main_purpose = st.selectbox(
        t('form.labels.main_purpose'),
        ["Office Space", "Residential", "Storage", "Workshop", "Retail", "Restaurant", "Medical", "Laboratory"],
        key="main_purpose"
    )
    
    # Environment
    environment = st.selectbox(
        t('form.labels.environment'),
        ["Indoor", "Outdoor", "Marine", "Industrial"],
        key="environment"
    )

with col2:
    # Finish level
    finish_level = st.selectbox(
        t('form.labels.finish_level'),
        ["Basic", "Standard", "Premium", "Luxury"],
        key="finish_level"
    )
    
    # Flooring
    flooring = st.selectbox(
        t('form.labels.flooring'),
        ["Plywood", "Vinyl", "Carpet", "Hardwood", "Polished Concrete"],
        key="flooring"
    )
    
    # Climate zone
    climate_zone = st.selectbox(
        t('form.labels.climate_zone'),
        ["Central European", "Scandinavian", "Mediterranean", "Atlantic Maritime", "Continental", "Alpine", "Baltic", "Temperate Oceanic"],
        key="climate_zone"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Systems and installations
st.markdown(f'<div class="config-section"><div class="section-title">⚙️ Systems & Installations</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Windows and doors
    number_of_windows = st.number_input(
        t('form.labels.number_of_windows'),
        min_value=0,
        max_value=20,
        value=2,
        key="number_of_windows"
    )
    
    additional_doors = st.checkbox(
        t('form.labels.additional_doors'),
        key="additional_doors"
    )

with col2:
    # Systems
    electrical_system = st.checkbox(
        t('form.labels.electrical_system'),
        value=True,
        key="electrical_system"
    )
    
    plumbing_system = st.checkbox(
        t('form.labels.plumbing_system'),
        key="plumbing_system"
    )
    
    hvac_system = st.checkbox(
        t('form.labels.hvac_system'),
        key="hvac_system"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Configuration summary and cost calculation
config = {
    'container_type': container_type,
    'main_purpose': main_purpose,
    'environment': environment,
    'finish_level': finish_level,
    'flooring': flooring,
    'climate_zone': climate_zone,
    'number_of_windows': number_of_windows,
    'additional_doors': additional_doors,
    'electrical_system': electrical_system,
    'plumbing_system': plumbing_system,
    'hvac_system': hvac_system
}

# Calculate cost
cost_breakdown = calculate_container_cost(config)

# Summary
st.markdown(f'<div class="config-section"><div class="section-title">📊 Configuration Summary</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Base Container:**")
    st.write(f"• Type: {container_type}")
    st.write(f"• Use Case: {main_purpose}")
    st.write(f"• Environment: {environment}")
    
    st.markdown("**Key Modifications:**")
    st.write(f"• Finish Level: {finish_level}")
    st.write(f"• Flooring: {flooring}")
    st.write(f"• Windows: {number_of_windows}")
    if additional_doors:
        st.write("• Additional doors included")

with col2:
    st.markdown("**Cost Breakdown:**")
    st.write(f"• Base Cost: €{cost_breakdown['base_cost']:,.2f}")
    st.write(f"• Modifications: €{cost_breakdown['modifications_cost']:,.2f}")
    st.write(f"• Multiplier: {cost_breakdown['multiplier']:.1f}x")
    st.markdown(f"**Total Cost: €{cost_breakdown['total_cost']:,.2f}**")

st.markdown('</div>', unsafe_allow_html=True)

# Save configuration
if st.button("💾 Save Configuration", use_container_width=True, type="primary"):
    st.session_state.container_config = config
    st.session_state.cost_breakdown = cost_breakdown
    st.success("Configuration saved successfully!")
    st.balloons()
