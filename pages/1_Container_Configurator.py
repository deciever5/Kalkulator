import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.container_database import ContainerDatabase
from utils.calculations import StructuralCalculations
from utils.global_language import init_language, get_current_language, render_language_selector, t, translate_list
from utils.advanced_3d_visualizer import Advanced3DVisualizer

st.set_page_config(page_title="Container Configurator", page_icon="📦", layout="wide", initial_sidebar_state="collapsed")

# Initialize language
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Initialize services
if 'container_db' not in st.session_state:
    st.session_state.container_db = ContainerDatabase()

if 'calculations' not in st.session_state:
    st.session_state.calculations = StructuralCalculations()

if 'visualizer_3d' not in st.session_state:
    st.session_state.visualizer_3d = Advanced3DVisualizer()

# Enhanced navigation header
st.markdown("""
<style>
.nav-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    color: white;
}
.config-section {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    margin-bottom: 1.5rem;
    border: 1px solid #e8f4f8;
}
.metric-card {
    background: linear-gradient(135deg, #f8fbff 0%, #e8f4f8 100%);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    border: 1px solid #ddd;
}
.action-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 1rem 2rem;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.3s ease;
}
.action-button:hover {
    transform: translateY(-2px);
}
</style>

<div class="nav-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h2 style="margin: 0; color: white;">📦 Konfigurator Kontenerów</h2>
            <p style="margin: 0; opacity: 0.9;">Projektuj swój idealny kontener krok po kroku</p>
        </div>
        <div style="display: flex; gap: 1rem;">
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button(get_translation('back_to_home', st.session_state.language), key="home_nav", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button(get_translation('go_to_ai_estimate', st.session_state.language), key="ai_nav", use_container_width=True):
        st.switch_page("pages/2_AI_Cost_Estimator.py")

st.markdown("</div></div></div>", unsafe_allow_html=True)

# Initialize session state for configuration
if 'container_config' not in st.session_state:
    st.session_state.container_config = {}

# Main configuration interface
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="config-section">
        <h3 style="color: #1e3c72; margin-bottom: 1.5rem;">🏗️ Specyfikacja Bazowa Kontenera</h3>
    """, unsafe_allow_html=True)
    
    # Container type selection
    container_types = st.session_state.container_db.get_container_types()
    selected_type = st.selectbox(
        "Typ Kontenera",
        options=list(container_types.keys()),
        help="Wybierz bazowy typ kontenera do modyfikacji"
    )
    
    if selected_type:
        container_specs = container_types[selected_type]
        st.session_state.container_config['base_type'] = selected_type
        
        st.markdown("<br>", unsafe_allow_html=True)
        # Display base specifications with enhanced styling
        spec_col1, spec_col2 = st.columns(2)
        with spec_col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin: 0; color: #1e3c72;">Długość</h4>
                <h2 style="margin: 0.5rem 0; color: #667eea;">{container_specs['length'] * 0.3048:.1f} m</h2>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin: 0; color: #1e3c72;">Szerokość</h4>
                <h2 style="margin: 0.5rem 0; color: #667eea;">{container_specs['width'] * 0.3048:.1f} m</h2>
            </div>
            """, unsafe_allow_html=True)
        with spec_col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin: 0; color: #1e3c72;">Wysokość</h4>
                <h2 style="margin: 0.5rem 0; color: #667eea;">{container_specs['height'] * 0.3048:.1f} m</h2>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="metric-card">
                <h4 style="margin: 0; color: #1e3c72;">Waga</h4>
                <h2 style="margin: 0.5rem 0; color: #667eea;">{container_specs['weight'] * 0.453592:.0f} kg</h2>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Use case selection with enhanced styling
    st.markdown("""
    <div class="config-section">
        <h3 style="color: #1e3c72; margin-bottom: 1.5rem;">🎯 Przeznaczenie</h3>
    """, unsafe_allow_html=True)
    
    use_cases = [
        "Office Space",
        "Residential Living", 
        "Workshop/Manufacturing",
        "Storage/Warehouse",
        "Retail/Commercial",
        "Medical/Healthcare",
        "Educational",
        "Restaurant/Kitchen",
        "Data Center",
        "Custom Industrial"
    ]
    
    selected_use_case = st.selectbox("Główne Przeznaczenie", use_cases)
    st.session_state.container_config['use_case'] = selected_use_case
    
    st.markdown("<br>", unsafe_allow_html=True)
    # Occupancy and environment
    col_occ1, col_occ2 = st.columns(2)
    with col_occ1:
        occupancy = st.number_input("Przewidywana Obsada", min_value=1, max_value=50, value=4)
    with col_occ2:
        environment = st.selectbox("Środowisko", ["Indoor", "Outdoor", "Marine", "Industrial"])
    
    st.session_state.container_config.update({
        'occupancy': occupancy,
        'environment': environment
    })
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="config-section">
        <h3 style="color: #1e3c72; margin-bottom: 1.5rem;">🔧 Wymagania Modyfikacji</h3>
    """, unsafe_allow_html=True)
    
    modifications = {}
    
    # Structural modifications
    st.markdown("##### 🏗️ Modyfikacje Strukturalne")
    col_mod1, col_mod2 = st.columns(2)
    with col_mod1:
        modifications['windows'] = st.number_input("Liczba Okien", min_value=0, max_value=20, value=0)
        modifications['doors'] = st.number_input("Liczba Drzwi", min_value=1, max_value=10, value=1)
    with col_mod2:
        modifications['skylights'] = st.number_input("Świetliki", min_value=0, max_value=10, value=0)
        modifications['vents'] = st.number_input("Otwory Wentylacyjne", min_value=0, max_value=20, value=2)
    
    st.markdown("<br>", unsafe_allow_html=True)
    # Structural reinforcements
    st.markdown("##### 🔨 Wzmocnienia Konstrukcyjne")
    col_reinf1, col_reinf2 = st.columns(2)
    with col_reinf1:
        modifications['reinforcement_walls'] = st.checkbox("Wzmocnienie Ścian")
        modifications['reinforcement_roof'] = st.checkbox("Wzmocnienie Dachu")
    with col_reinf2:
        modifications['reinforcement_floor'] = st.checkbox("Wzmocnienie Podłogi")
        modifications['additional_support'] = st.checkbox("Dodatkowe Podpory")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="config-section">
        <h4 style="color: #1e3c72; margin-bottom: 1rem;">⚡ Systemy i Instalacje</h4>
    """, unsafe_allow_html=True)
    
    col_sys1, col_sys2 = st.columns(2)
    with col_sys1:
        modifications['electrical'] = st.checkbox("System Elektryczny")
        modifications['plumbing'] = st.checkbox("System Hydrauliczny")
    with col_sys2:
        modifications['hvac'] = st.checkbox("System HVAC")
        modifications['insulation'] = st.checkbox("Pakiet Izolacyjny")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Interior finishes
    st.markdown("""
    <div class="config-section">
        <h4 style="color: #1e3c72; margin-bottom: 1rem;">🎨 Wykończenia Wnętrza</h4>
    """, unsafe_allow_html=True)
    
    finish_level = st.selectbox("Poziom Wykończenia", ["Basic", "Standard", "Premium", "Luxury"])
    modifications['finish_level'] = finish_level
    
    flooring_type = st.selectbox("Podłogi", ["Plywood", "Vinyl", "Carpet", "Hardwood", "Polished Concrete"])
    modifications['flooring'] = flooring_type
    
    st.session_state.container_config['modifications'] = modifications
    
    st.markdown("</div>", unsafe_allow_html=True)

# Configuration summary and visualization
st.divider()
st.subheader("📋 Configuration Summary")

col1, col2 = st.columns([1, 1])

with col1:
    if 'base_type' in st.session_state.container_config:
        st.markdown("**Base Container:**")
        st.write(f"Type: {st.session_state.container_config['base_type']}")
        st.write(f"Use Case: {st.session_state.container_config['use_case']}")
        st.write(f"Occupancy: {st.session_state.container_config['occupancy']} people")
        st.write(f"Environment: {st.session_state.container_config['environment']}")
        
        st.markdown("**Key Modifications:**")
        mods = st.session_state.container_config.get('modifications', {})
        mod_list = []
        
        if mods.get('windows', 0) > 0:
            mod_list.append(f"Windows: {mods['windows']}")
        if mods.get('doors', 0) > 1:
            mod_list.append(f"Additional Doors: {mods['doors'] - 1}")
        if mods.get('electrical'):
            mod_list.append("Electrical System")
        if mods.get('plumbing'):
            mod_list.append("Plumbing System")
        if mods.get('hvac'):
            mod_list.append("HVAC System")
        if mods.get('insulation'):
            mod_list.append("Insulation Package")
        
        for mod in mod_list:
            st.write(f"• {mod}")

with col2:
    # Advanced 3D visualization with all modifications
    st.markdown("**🏗️ Advanced 3D Container Model**")
    
    if 'base_type' in st.session_state.container_config:
        # Create advanced 3D model with all modifications
        fig_3d = st.session_state.visualizer_3d.create_3d_model(st.session_state.container_config)
        
        # Display the advanced 3D model
        st.plotly_chart(fig_3d, use_container_width=True)
        
        # Add visualization controls
        st.markdown("**🎛️ Visualization Controls**")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            show_interior = st.checkbox("Show Interior Layout", value=True)
            show_systems = st.checkbox("Show Systems (Electrical/Plumbing)", value=True)
        
        with col_b:
            show_modifications = st.checkbox("Show Modifications", value=True)
            show_structure = st.checkbox("Show Structural Frame", value=True)
        
        # Update visualization based on controls
        if not show_interior or not show_systems or not show_modifications or not show_structure:
            # Create filtered configuration
            filtered_config = st.session_state.container_config.copy()
            
            if not show_systems:
                mods = filtered_config.get('modifications', {})
                mods.pop('electrical', None)
                mods.pop('plumbing', None)
                mods.pop('hvac', None)
            
            if not show_modifications:
                filtered_config['modifications'] = {}
            
            # Recreate visualization with filters
            fig_filtered = st.session_state.visualizer_3d.create_3d_model(filtered_config)
            st.plotly_chart(fig_filtered, use_container_width=True, key="filtered_view")

# Enhanced action buttons
st.markdown("""
<div style="background: linear-gradient(135deg, #f8fbff 0%, #e8f4f8 100%); 
           padding: 2rem; border-radius: 15px; margin: 2rem 0;">
    <h3 style="text-align: center; color: #1e3c72; margin-bottom: 1.5rem;">
        🚀 Następne Kroki
    </h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4, gap="large")

# Show only client-facing options for non-employees
if st.session_state.get('employee_logged_in', False):
    action_buttons = [
        ("💰", "Wycena AI", "Uzyskaj automatyczną wycenę", "pages/2_AI_Cost_Estimator.py"),
        ("🔧", "Analiza Techniczna", "Sprawdź parametry konstrukcyjne", "pages/3_Technical_Analysis.py"),
        ("📄", "Generuj Ofertę", "Stwórz profesjonalną ofertę", "pages/4_Quote_Generator.py"),
        ("⚖️", "Porównaj Opcje", "Porównaj z innymi konfiguracjami", "pages/5_Comparison_Tool.py")
    ]
else:
    # Client area - only basic functions
    action_buttons = [
        ("💰", "Wycena AI", "Uzyskaj automatyczną wycenę", "pages/2_AI_Cost_Estimator.py")
    ]

for i, (icon, title, desc, page) in enumerate(action_buttons):
    with [col1, col2, col3, col4][i]:
        st.markdown(f"""
        <div style="background: white; border-radius: 10px; padding: 1.5rem; 
                   box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08); text-align: center;
                   border: 1px solid #e8f4f8; margin-bottom: 1rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
            <h4 style="color: #1e3c72; margin-bottom: 0.5rem;">{title}</h4>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Otwórz {title}", key=f"action_{i}", use_container_width=True, type="primary"):
            st.switch_page(page)

# Enhanced save configuration
st.markdown("<br>", unsafe_allow_html=True)
col_save1, col_save2, col_save3 = st.columns([1, 2, 1])
with col_save2:
    if st.button("💾 Zapisz Konfigurację", use_container_width=True, type="secondary"):
        if 'container_config' in st.session_state and st.session_state.container_config:
            st.success("✅ Konfiguracja została pomyślnie zapisana!")
            with st.expander("Podgląd zapisanej konfiguracji"):
                st.json(st.session_state.container_config)
        else:
            st.error("❌ Proszę uzupełnić konfigurację przed zapisaniem.")
