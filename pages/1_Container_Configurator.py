# Page configuration - MUST BE FIRST
import streamlit as st
st.set_page_config(
    page_title="Container Configurator - KAN-BUD",
    page_icon="📦",
    layout="wide"
)

import pandas as pd
from utils.container_database import ContainerDatabase
from utils.calculations import calculate_container_cost
from utils.translations import t, init_language, get_current_language, set_language
from utils.shared_header import render_shared_header

init_language()

# Initialize session state for login
if 'employee_logged_in' not in st.session_state:
    st.session_state.employee_logged_in = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# Load animations
from utils.animations import add_hover_animations, show_loading_animation, create_animated_counter
add_hover_animations()

# Render shared header without login button
render_shared_header(show_login=False, current_page="Container_Configurator")

# Initialize database
if 'container_db' not in st.session_state:
    st.session_state.container_db = ContainerDatabase()

st.markdown("""
<style>
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

# Navigation
col1, col2 = st.columns(2)
with col1:
    home_text = t('ui.back_to_home')
    if st.button(home_text, key="home_nav", use_container_width=True):
        st.switch_page("app.py")

with col2:
    ai_text = t('ui.go_to_ai_estimate')
    if st.button(ai_text, key="ai_nav", use_container_width=True):
        st.switch_page("pages/2_AI_Cost_Estimator.py")

# Configuration form
st.markdown(f'<div class="config-section"><div class="section-title">🏗️ {t("configure_container")}</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Container type
    container_types = {
        t('container.types.20ft_standard'): "20ft Standard",
        t('container.types.40ft_standard'): "40ft Standard", 
        t('container.types.40ft_high_cube'): "40ft High Cube",
        t('container.types.20ft_refrigerated'): "20ft Refrigerated",
        t('container.types.20ft_double_door'): "20ft Double Door",
        t('container.types.40ft_double_door'): "40ft Double Door",
        t('container.types.40ft_hc_double_door'): "40ft HC Double Door",
        t('container.types.custom_size'): "Custom Size"
    }
    container_type_display = st.selectbox(
        t('form.labels.container_type'),
        list(container_types.keys()),
        key="container_type_display"
    )
    container_type = container_types[container_type_display]

    # Main purpose
    main_purposes = {
        t('container.use_cases.office_space'): "Office Space",
        t('container.use_cases.residential'): "Residential",
        t('container.use_cases.storage'): "Storage",
        t('container.use_cases.workshop'): "Workshop",
        t('container.use_cases.retail'): "Retail",
        t('container.use_cases.restaurant'): "Restaurant",
        t('container.use_cases.medical'): "Medical",
        t('container.use_cases.laboratory'): "Laboratory"
    }
    main_purpose_display = st.selectbox(
        t('form.labels.main_purpose'),
        list(main_purposes.keys()),
        key="main_purpose_display"
    )
    main_purpose = main_purposes[main_purpose_display]

    # Environment
    environments = {
        t('container.environment.indoor'): "Indoor",
        t('container.environment.outdoor'): "Outdoor",
        t('container.environment.marine'): "Marine",
        t('container.environment.industrial'): "Industrial"
    }
    environment_display = st.selectbox(
        t('form.labels.environment'),
        list(environments.keys()),
        key="environment_display"
    )
    environment = environments[environment_display]

with col2:
    # Finish level
    finish_levels = {
        t('container.finish_levels.basic'): "Basic",
        t('container.finish_levels.standard'): "Standard",
        t('container.finish_levels.premium'): "Premium",
        t('container.finish_levels.luxury'): "Luxury"
    }
    finish_level_display = st.selectbox(
        t('form.labels.finish_level'),
        list(finish_levels.keys()),
        key="finish_level_display"
    )
    finish_level = finish_levels[finish_level_display]

    # Flooring
    floorings = {
        t('container.flooring.plywood'): "Plywood",
        t('container.flooring.vinyl'): "Vinyl",
        t('container.flooring.carpet'): "Carpet",
        t('container.flooring.hardwood'): "Hardwood",
        t('container.flooring.polished_concrete'): "Polished Concrete"
    }
    flooring_display = st.selectbox(
        t('form.labels.flooring'),
        list(floorings.keys()),
        key="flooring_display"
    )
    flooring = floorings[flooring_display]

    # Climate zone
    climate_zones = {
        t('container.climate_zones.central_european'): "Central European",
        t('container.climate_zones.scandinavian'): "Scandinavian",
        t('container.climate_zones.mediterranean'): "Mediterranean",
        t('container.climate_zones.atlantic_maritime'): "Atlantic Maritime",
        t('container.climate_zones.continental'): "Continental",
        t('container.climate_zones.alpine'): "Alpine",
        t('container.climate_zones.baltic'): "Baltic",
        t('container.climate_zones.temperate_oceanic'): "Temperate Oceanic"
    }
    climate_zone_display = st.selectbox(
        t('form.labels.climate_zone'),
        list(climate_zones.keys()),
        key="climate_zone_display"
    )
    climate_zone = climate_zones[climate_zone_display]

st.markdown('</div>', unsafe_allow_html=True)

# Systems and installations
st.markdown(f'<div class="config-section"><div class="section-title">⚙️ {t("systems_installations")}</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Windows and doors
    number_of_windows = st.number_input(
        t('form.labels.number_of_windows'),
        min_value=0,
        max_value=20,
        value=2,
        key="number_of_windows",
        help=t('help.windows')
    )

    additional_doors = st.checkbox(
        t('form.labels.additional_doors'),
        key="additional_doors",
        help=t('help.additional_doors')
    )
    
    # Air intakes and ventilation
    air_intakes = st.selectbox(
        t('air_intakes_label'),
        [t('air_intakes.none'), t('air_intakes.standard'), t('air_intakes.industrial'), t('air_intakes.marine_grade')],
        key="air_intakes",
        help=t('help.air_intakes')
    )
    
    # Roof modifications
    roof_modifications = st.selectbox(
        t('roof_modifications_label'),
        [t('roof_modifications.none'), t('roof_modifications.skylight'), t('roof_modifications.roof_hatch'), t('roof_modifications.solar_ready')],
        key="roof_modifications",
        help=t('help.roof_modifications')
    )

with col2:
    # Systems
    electrical_system = st.selectbox(
        t('electrical_system'),
        [t('electrical.basic'), t('electrical.standard'), t('electrical.industrial'), t('electrical.smart_system')],
        index=1,
        key="electrical_system",
        help=t('help.electrical_system')
    )

    plumbing_system = st.selectbox(
        t('plumbing_system'),
        [t('plumbing.none'), t('plumbing.basic'), t('plumbing.full'), t('plumbing.commercial')],
        key="plumbing_system",
        help=t('help.plumbing_system')
    )

    hvac_system = st.selectbox(
        t('hvac_system'),
        [t('hvac.none'), t('hvac.basic'), t('hvac.split_system'), t('hvac.central'), t('hvac.heat_pump')],
        key="hvac_system",
        help=t('help.hvac_system')
    )

# Advanced modifications section
st.markdown(f'<div class="config-section"><div class="section-title">🔧 {t("advanced_modifications")}</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    # Security features
    security_features = st.selectbox(
        t('security_features'),
        [t('security.basic'), t('security.standard'), t('security.advanced'), t('security.high_security')],
        key="security_features",
        help=t('help.security_features')
    )
    
    # Exterior cladding
    exterior_cladding = st.selectbox(
        t('exterior_cladding'),
        [t('cladding.none'), t('cladding.metal'), t('cladding.composite'), t('cladding.wood'), t('cladding.brick_veneer')],
        key="exterior_cladding",
        help=t('help.exterior_cladding')
    )

with col2:
    # Additional openings
    additional_openings = st.selectbox(
        t('additional_openings'),
        [t('openings.none'), t('openings.service_hatch'), t('openings.loading_door'), t('openings.emergency_exit')],
        key="additional_openings",
        help=t('help.additional_openings')
    )
    
    # Fire safety systems
    fire_safety = st.selectbox(
        t('fire_safety_label'),
        [t('fire_safety.basic'), t('fire_safety.smoke_detection'), t('fire_safety.sprinkler'), t('fire_safety.full_system')],
        key="fire_safety",
        help=t('help.fire_safety')
    )

with col3:
    # Accessibility features
    accessibility = st.selectbox(
        t('accessibility_features'),
        [t('accessibility.standard'), t('accessibility.ramp'), t('accessibility.full_ada'), t('accessibility.disabled_friendly')],
        key="accessibility",
        help=t('help.accessibility')
    )
    
    # Custom paint finish
    paint_finish = st.selectbox(
        t('paint_finish'),
        [t('paint.standard'), t('paint.premium'), t('paint.anti_corrosion'), t('paint.marine_grade')],
        key="paint_finish",
        help=t('help.paint_finish')
    )

st.markdown('</div>', unsafe_allow_html=True)

# Delivery and logistics
st.markdown(f'<div class="config-section"><div class="section-title">🚛 {t("delivery_logistics")}</div>', unsafe_allow_html=True)

delivery_zones = {
    t('delivery.zones.local'): "Local",
    t('delivery.zones.poland'): "Poland", 
    t('delivery.zones.central_europe'): "Central_Europe",
    t('delivery.zones.western_europe'): "Western_Europe",
    t('delivery.zones.northern_europe'): "Northern_Europe",
    t('delivery.zones.southern_europe'): "Southern_Europe",
    t('delivery.zones.eastern_europe'): "Eastern_Europe",
    t('delivery.zones.uk_ireland'): "UK_Ireland",
    t('delivery.zones.international'): "International"
}

delivery_zone_display = st.selectbox(
    t('form.labels.delivery_zone'),
    list(delivery_zones.keys()),
    key="delivery_zone_display"
)
delivery_zone = delivery_zones[delivery_zone_display]

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
    'hvac_system': hvac_system,
    'air_intakes': air_intakes,
    'roof_modifications': roof_modifications,
    'security_features': security_features,
    'exterior_cladding': exterior_cladding,
    'additional_openings': additional_openings,
    'fire_safety': fire_safety,
    'accessibility': accessibility,
    'paint_finish': paint_finish,
    'delivery_zone': delivery_zone
}

# Calculate cost
cost_breakdown = calculate_container_cost(config)

# Summary
st.markdown(f'<div class="config-section"><div class="section-title">📊 {t("configuration_summary")}</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**{t('base_container')}:**")
    st.write(f"• {t('type')}: {container_type_display}")
    st.write(f"• {t('use_case')}: {main_purpose_display}")
    st.write(f"• {t('environment')}: {environment_display}")

    st.markdown(f"**{t('key_modifications')}:**")
    st.write(f"• {t('finish_level')}: {finish_level_display}")
    st.write(f"• {t('flooring')}: {flooring_display}")
    st.write(f"• {t('windows')}: {number_of_windows}")
    if additional_doors:
        st.write(f"• {t('additional_doors_included')}")

with col2:
    st.markdown(f"**{t('cost_breakdown')}:**")
    st.write(f"• {t('base_cost')}: €{cost_breakdown['base_cost']:,.2f}")
    st.write(f"• {t('modifications')}: €{cost_breakdown['modifications_cost']:,.2f}")
    st.write(f"• {t('delivery_cost')}: €{cost_breakdown['delivery_cost']:,.2f}")
    st.write(f"• {t('multiplier')}: {cost_breakdown['multiplier']:.1f}x")
    st.markdown(f"**{t('total_cost')}: €{cost_breakdown['total_cost']:,.2f}**")

st.markdown('</div>', unsafe_allow_html=True)

# Save configuration and AI analysis buttons
col1, col2 = st.columns(2)

with col1:
    if st.button(t("save_configuration"), use_container_width=True, type="primary"):
        st.session_state.container_config = config
        st.session_state.cost_breakdown = cost_breakdown
        st.success(t("configuration_saved"))
        st.balloons()

with col2:
    if st.button(f"🤖 {t('get_ai_analysis')}", use_container_width=True, type="secondary"):
        # Save configuration first
        st.session_state.container_config = config
        st.session_state.cost_breakdown = cost_breakdown
        # Navigate to AI Cost Estimator
        st.switch_page("pages/2_AI_Cost_Estimator.py")