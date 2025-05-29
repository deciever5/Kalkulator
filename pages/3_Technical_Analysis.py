import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.translations import init_language, t, translate_options, render_language_selector

# Page configuration
st.set_page_config(
    page_title="Technical Analysis - KAN-BUD",
    page_icon="🔬",
    layout="wide"
)

# Initialize translation system
init_language()

# Add language selector in sidebar
with st.sidebar:
    render_language_selector()

# Page header
st.title(t('technical_analysis'))
st.markdown(f"### {t('configuration_summary')}")

# Configuration form
with st.form("technical_config"):
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

        climate_zone = st.selectbox(
            t('climate_zone'),
            options=['Central European', 'Scandinavian', 'Mediterranean', 'Atlantic Maritime', 'Continental', 'Alpine', 'Baltic', 'Temperate Oceanic'],
            format_func=lambda x: t(x)
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
    st.success(t('estimate_ready'))

    st.subheader(t('configuration_summary'))

    config_data = {
        t('container_type'): t(container_type),
        t('main_purpose'): t(main_purpose),
        t('environment'): t(environment),
        t('climate_zone'): t(climate_zone),
        t('finish_level'): t(finish_level),
        t('flooring'): t(flooring),
        t('electrical_system'): t('yes') if electrical_system else t('no'),
        t('plumbing_system'): t('yes') if plumbing_system else t('no'),
        t('hvac_system'): t('yes') if hvac_system else t('no'),
        t('insulation_package'): t('yes') if insulation_package else t('no'),
        t('structural_reinforcement'): t('yes') if structural_reinforcement else t('no')
    }

    for key, value in config_data.items():
        st.write(f"**{key}:** {value}")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button(t('back_to_home'), key="home_nav", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button(t('go_to_configurator'), key="config_nav", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")