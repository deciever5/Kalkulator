import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.translations import init_language, t, translate_options, render_language_selector
from utils.calculations import calculate_container_cost

# Page configuration
st.set_page_config(
    page_title="Container Configurator - KAN-BUD",
    page_icon="🔧",
    layout="wide"
)

# Initialize translation system
init_language()

# Add language selector in sidebar
with st.sidebar:
    render_language_selector()

# Page header
st.title(t('container_configurator'))
st.markdown(f"### {t('configure_container')}")

# Configuration form
with st.form("container_config"):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(t('base_container_spec'))

        container_type = st.selectbox(
            t('container_type'),
            options=['20ft Standard', '40ft Standard', '40ft High Cube', '20ft Refrigerated'],
            format_func=lambda x: t(x)
        )

        main_purpose = st.selectbox(
            t('main_purpose'),
            options=['Office Space', 'Residential', 'Storage', 'Workshop', 'Retail', 'Restaurant', 'Medical', 'Laboratory'],
            format_func=lambda x: t(x)
        )

        environment = st.selectbox(
            t('environment'),
            options=['Indoor', 'Outdoor', 'Marine', 'Industrial'],
            format_func=lambda x: t(x)
        )

        climate_zone = st.selectbox(
            t('climate_zone'),
            options=['Central European', 'Scandinavian', 'Mediterranean', 'Atlantic Maritime', 'Continental', 'Alpine', 'Baltic', 'Temperate Oceanic'],
            format_func=lambda x: t(x)
        )

    with col2:
        st.subheader(t('modification_requirements'))

        finish_level = st.selectbox(
            t('finish_level'),
            options=['Basic', 'Standard', 'Premium', 'Luxury'],
            format_func=lambda x: t(x)
        )

        flooring = st.selectbox(
            t('flooring'),
            options=['Plywood', 'Vinyl', 'Carpet', 'Hardwood', 'Polished Concrete'],
            format_func=lambda x: t(x)
        )

        number_of_windows = st.number_input(
            t('number_of_windows'),
            min_value=0,
            max_value=20,
            value=2
        )

        additional_doors = st.number_input(
            t('additional_doors'),
            min_value=0,
            max_value=10,
            value=1
        )

    # Systems section
    st.subheader(t('systems_installations'))

    col3, col4 = st.columns(2)

    with col3:
        electrical_system = st.checkbox(t('electrical_system'), value=True)
        plumbing_system = st.checkbox(t('plumbing_system'), value=False)
        hvac_system = st.checkbox(t('hvac_system'), value=True)

    with col4:
        insulation_package = st.checkbox(t('insulation_package'), value=True)
        structural_reinforcement = st.checkbox(t('structural_reinforcement'), value=False)

    # Submit button
    submitted = st.form_submit_button(t('calculate'), use_container_width=True)

# Results section
if submitted:
    with st.container():
        st.success(t('estimate_ready'))

        # Calculate costs
        config = {
            'container_type': container_type,
            'main_purpose': main_purpose,
            'environment': environment,
            'climate_zone': climate_zone,
            'finish_level': finish_level,
            'flooring': flooring,
            'number_of_windows': number_of_windows,
            'additional_doors': additional_doors,
            'electrical_system': electrical_system,
            'plumbing_system': plumbing_system,
            'hvac_system': hvac_system,
            'insulation_package': insulation_package,
            'structural_reinforcement': structural_reinforcement
        }

        cost_data = calculate_container_cost(config)

        # Display cost breakdown
        st.subheader(t('cost_breakdown'))

        col5, col6 = st.columns(2)

        with col5:
            st.metric(t('basic_cost'), f"€{cost_data['basic_cost']:,.2f}")
            st.metric(t('modifications_cost'), f"€{cost_data['modifications_cost']:,.2f}")

        with col6:
            st.metric(t('total_cost'), f"€{cost_data['total_cost']:,.2f}", delta=f"€{cost_data['modifications_cost']:,.2f}")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button(t('back_to_home'), key="home_nav", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button(t('go_to_ai_estimate'), key="ai_nav", use_container_width=True):
        st.switch_page("pages/2_AI_Cost_Estimator.py")