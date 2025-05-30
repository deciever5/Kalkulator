import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.calculations import StructuralCalculations
from utils.translations import t, render_language_selector, get_current_language, render_language_selector
from utils.components import render_back_to_home
from utils.shared_header import render_shared_header

# Page configuration - MUST BE FIRST
st.set_page_config(
    page_title="Technical Analysis - KAN-BUD",
    page_icon="🔧",
    layout="wide"
)

from utils.translations import t, init_language
from utils.shared_header import render_shared_header

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Render consistent header with language selector at top
render_shared_header(show_login=True, current_page="Technical_Analysis")

st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="main-header">
    <div class="header-title">🔧 {t('nav.technical_analysis')}</div>
    <div class="header-subtitle">Structural and engineering analysis</div>
</div>
""", unsafe_allow_html=True)

# Navigation
col1, col2 = st.columns(2)
with col1:
    if st.button(t('ui.back_to_home'), key="home_nav", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button(t('ui.go_to_configurator'), key="config_nav", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")

# Initialize calculations
if 'calculations' not in st.session_state:
    st.session_state.calculations = StructuralCalculations()

calc = st.session_state.calculations

# Check if configuration exists
if 'container_config' not in st.session_state:
    st.warning("No container configuration found. Please configure your container first.")
    if st.button("🔧 Go to Configurator", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")
else:
    config = st.session_state.container_config

    st.markdown("### Container Specifications:")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Container Type", config['container_type'])
        st.metric("Purpose", config['main_purpose'])

    with col2:
        st.metric("Environment", config['environment'])
        st.metric("Finish Level", config['finish_level'])

    with col3:
        st.metric("Windows", config['number_of_windows'])
        st.metric("Climate Zone", config['climate_zone'])

    st.markdown("---")

    # Technical calculations
    st.markdown("### 🔬 Technical Analysis:")

    # Calculate structural requirements
    structural_reqs = calc.calculate_structural_requirements(config)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Structural Requirements:")
        for req, value in structural_reqs.items():
            if isinstance(value, (int, float)):
                st.write(f"• {req.replace('_', ' ').title()}: {value}")
            else:
                st.write(f"• {req.replace('_', ' ').title()}: {value}")

    with col2:
        st.markdown("#### Load Analysis:")
        loads = calc.calculate_loads(config)
        for load_type, value in loads.items():
            st.write(f"• {load_type.replace('_', ' ').title()}: {value}")

    # Climate considerations
    st.markdown("### 🌡️ Climate Considerations:")
    climate_data = calc.get_climate_requirements(config['climate_zone'])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Min Temperature", f"{climate_data['min_temp']}°C")
        st.metric("Max Temperature", f"{climate_data['max_temp']}°C")

    with col2:
        st.metric("Wind Load", f"{climate_data['wind_load']} kN/m²")
        st.metric("Snow Load", f"{climate_data['snow_load']} kN/m²")

    with col3:
        st.metric("Humidity Range", f"{climate_data['humidity']}%")
        st.metric("Insulation R-Value", f"R-{climate_data['insulation_r']}")

    # Material specifications
    st.markdown("### 🏗️ Material Specifications:")
    materials = calc.get_material_specs(config)

    df_materials = pd.DataFrame(materials)
    st.dataframe(df_materials, use_container_width=True)

    # Visualization
    st.markdown("### 📊 Analysis Visualization:")

    # Create load distribution chart
    load_data = list(loads.values())
    load_labels = [label.replace('_', ' ').title() for label in loads.keys()]

    fig = px.bar(
        x=load_labels,
        y=load_data,
        title="Load Distribution Analysis",
        labels={'x': 'Load Type', 'y': 'Load (kN)'}
    )
    st.plotly_chart(fig, use_container_width=True)

    # Generate technical report
    if st.button("📋 Generate Technical Report", use_container_width=True, type="primary"):
        st.success("Technical report generated!")

        report = f"""
        ## Technical Analysis Report

        **Container:** {config['container_type']}
        **Purpose:** {config['main_purpose']}
        **Environment:** {config['environment']}

        ### Structural Requirements:
        {chr(10).join([f"• {k.replace('_', ' ').title()}: {v}" for k, v in structural_reqs.items()])}

        ### Load Analysis:
        {chr(10).join([f"• {k.replace('_', ' ').title()}: {v}" for k, v in loads.items()])}

        ### Climate Considerations:
        • Temperature Range: {climate_data['min_temp']}°C to {climate_data['max_temp']}°C
        • Wind Load: {climate_data['wind_load']} kN/m²
        • Snow Load: {climate_data['snow_load']} kN/m²
        • Required Insulation: R-{climate_data['insulation_r']}
        """

        st.markdown(report)
        st.session_state.technical_report = report

# Render shared header without login button
render_shared_header(show_login=False)

# Language selector already rendered at the top

# Back to home button at the bottom
st.markdown("---")
render_back_to_home()