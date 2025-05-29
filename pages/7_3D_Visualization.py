"""
Advanced 3D Visualization Page for KAN-BUD Container Calculator
Interactive 3D models with real-time modification visualization
"""

import streamlit as st
import plotly.graph_objects as go
from utils.advanced_3d_visualizer import Advanced3DVisualizer
from utils.container_database import ContainerDatabase
from utils.complete_translations import get_translation, translate_options

st.set_page_config(page_title="3D Visualization", page_icon="🏗️", layout="wide", initial_sidebar_state="collapsed")

# Initialize language
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Initialize services
if 'visualizer_3d' not in st.session_state:
    st.session_state.visualizer_3d = Advanced3DVisualizer()

if 'container_db' not in st.session_state:
    st.session_state.container_db = ContainerDatabase()

# Language selection
st.markdown("""
<div style="position: fixed; top: 10px; right: 20px; z-index: 999; background: white; padding: 10px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🇵🇱", help="Polski"):
        st.session_state.language = 'pl'
        st.rerun()
with col2:
    if st.button("🇬🇧", help="English"):
        st.session_state.language = 'en'
        st.rerun()
with col3:
    if st.button("🇩🇪", help="Deutsch"):
        st.session_state.language = 'de'
        st.rerun()
with col4:
    if st.button("🇳🇱", help="Nederlands"):
        st.session_state.language = 'nl'
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Navigation header
st.markdown("""
<div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
           padding: 2rem; margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 20px 20px;">
    <h1 style="color: white; text-align: center; margin: 0; font-size: 2.5rem;">
        🏗️ Advanced 3D Container Visualization
    </h1>
    <p style="color: #e8f4f8; text-align: center; margin: 0.5rem 0 0 0; font-size: 1.2rem;">
        Realistic 3D Models with Real-time Modifications
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button(get_translation('back_to_home', st.session_state.language), key="home_nav", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button(get_translation('go_to_configurator', st.session_state.language), key="config_nav", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")

st.markdown("---")

# Main content
st.markdown("## 🎛️ Interactive 3D Container Designer")

# Configuration section
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### ⚙️ Configuration")
    
    # Container type selection
    container_types = ['20ft Standard', '40ft Standard', '40ft High Cube', '20ft Refrigerated']
    translated_types = translate_options(container_types, st.session_state.language)
    
    selected_type_translated = st.selectbox(
        get_translation('container_type', st.session_state.language),
        translated_types,
        key="viz_container_type"
    )
    selected_type = container_types[translated_types.index(selected_type_translated)]
    
    # Use case selection
    use_cases = ['Office Space', 'Residential', 'Storage', 'Workshop', 'Retail', 'Restaurant', 'Medical', 'Laboratory']
    translated_use_cases = translate_options(use_cases, st.session_state.language)
    
    selected_use_case_translated = st.selectbox(
        get_translation('main_purpose', st.session_state.language),
        translated_use_cases,
        key="viz_use_case"
    )
    selected_use_case = use_cases[translated_use_cases.index(selected_use_case_translated)]
    
    st.markdown("### 🔧 Modifications")
    
    # Modification options
    num_windows = st.slider("Number of Windows", 0, 8, 2)
    num_doors = st.slider("Additional Doors", 0, 3, 1)
    
    # Systems
    st.markdown("**Systems Installation:**")
    electrical = st.checkbox("Electrical System", value=True)
    plumbing = st.checkbox("Plumbing System", value=False)
    hvac = st.checkbox("HVAC System", value=True)
    insulation = st.checkbox("Insulation Package", value=True)
    reinforcement = st.checkbox("Structural Reinforcement", value=False)
    
    # Build configuration
    config = {
        'base_type': selected_type,
        'use_case': selected_use_case,
        'modifications': {
            'windows': num_windows,
            'doors': num_doors + 1,  # +1 for the standard door
            'electrical': electrical,
            'plumbing': plumbing,
            'hvac': hvac,
            'insulation': insulation,
            'reinforcement': reinforcement
        }
    }

with col2:
    st.markdown("### 🏗️ 3D Model Preview")
    
    # Generate and display 3D model
    try:
        fig_3d = st.session_state.visualizer_3d.create_3d_model(config)
        st.plotly_chart(fig_3d, use_container_width=True, height=500)
    except Exception as e:
        st.error(f"Error generating 3D model: {str(e)}")
        st.info("Please check your configuration and try again.")

# Visualization controls
st.markdown("---")
st.markdown("## 🎮 Visualization Controls")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**👁️ View Options**")
    show_frame = st.checkbox("Show Frame Structure", value=True, key="show_frame")
    show_walls = st.checkbox("Show Walls", value=True, key="show_walls")

with col2:
    st.markdown("**🔧 Modifications**")
    show_openings = st.checkbox("Show Windows/Doors", value=True, key="show_openings")
    show_interior = st.checkbox("Show Interior Layout", value=True, key="show_interior")

with col3:
    st.markdown("**⚡ Systems**")
    show_electrical = st.checkbox("Show Electrical", value=True, key="show_electrical")
    show_plumbing = st.checkbox("Show Plumbing", value=True, key="show_plumbing")

with col4:
    st.markdown("**🌡️ Climate Control**")
    show_hvac = st.checkbox("Show HVAC", value=True, key="show_hvac")
    show_insulation = st.checkbox("Show Insulation", value=True, key="show_insulation")

# Comparison tool
st.markdown("---")
st.markdown("## 🔄 Before/After Comparison")

if st.button("🔍 Generate Comparison View", use_container_width=True):
    st.markdown("### 📊 Standard vs Modified Container")
    
    # Create base configuration (minimal modifications)
    base_config = {
        'base_type': selected_type,
        'use_case': 'Storage',  # Basic use case
        'modifications': {
            'windows': 0,
            'doors': 1,
            'electrical': False,
            'plumbing': False,
            'hvac': False,
            'insulation': False,
            'reinforcement': False
        }
    }
    
    try:
        # Generate comparison
        comparison_fig = st.session_state.visualizer_3d.create_modification_comparison(base_config, config)
        st.plotly_chart(comparison_fig, use_container_width=True, height=600)
        
        # Comparison summary
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📦 Standard Container**")
            st.write("• Basic storage configuration")
            st.write("• No additional windows")
            st.write("• Single entry door")
            st.write("• No systems installed")
        
        with col2:
            st.markdown("**🏗️ Modified Container**")
            st.write(f"• {selected_use_case} configuration")
            st.write(f"• {num_windows} windows installed")
            st.write(f"• {num_doors + 1} doors total")
            
            systems = []
            if electrical: systems.append("Electrical")
            if plumbing: systems.append("Plumbing") 
            if hvac: systems.append("HVAC")
            if insulation: systems.append("Insulation")
            
            if systems:
                st.write(f"• Systems: {', '.join(systems)}")
            else:
                st.write("• No additional systems")
    
    except Exception as e:
        st.error(f"Error generating comparison: {str(e)}")

# Technical specifications
st.markdown("---")
st.markdown("## 📐 Technical Specifications")

col1, col2, col3 = st.columns(3)

container_specs = st.session_state.container_db.get_container_specs(selected_type)

with col1:
    st.markdown("**📏 Dimensions**")
    st.write(f"Length: {container_specs['length']:.2f} m")
    st.write(f"Width: {container_specs['width']:.2f} m") 
    st.write(f"Height: {container_specs['height']:.2f} m")

with col2:
    st.markdown("**📊 Areas**")
    areas = st.session_state.container_db.calculate_container_area(selected_type)
    st.write(f"Floor: {areas['floor_area']:.1f} m²")
    st.write(f"Wall: {areas['wall_area']:.1f} m²")
    st.write(f"Volume: {areas['volume']:.1f} m³")

with col3:
    st.markdown("**🔧 Modifications**")
    st.write(f"Windows: {num_windows}")
    st.write(f"Doors: {num_doors + 1}")
    st.write(f"Systems: {len([s for s in [electrical, plumbing, hvac, insulation] if s])}")

# Export options
st.markdown("---")
st.markdown("## 💾 Export Options")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Export Configuration", use_container_width=True):
        config_text = f"""
Container Configuration Export
=============================

Container Type: {selected_type}
Use Case: {selected_use_case}

Modifications:
- Windows: {num_windows}
- Additional Doors: {num_doors}
- Electrical System: {'Yes' if electrical else 'No'}
- Plumbing System: {'Yes' if plumbing else 'No'}
- HVAC System: {'Yes' if hvac else 'No'}
- Insulation Package: {'Yes' if insulation else 'No'}
- Structural Reinforcement: {'Yes' if reinforcement else 'No'}

Generated by KAN-BUD Container Calculator
"""
        st.download_button(
            label="📥 Download Configuration",
            data=config_text,
            file_name=f"container_config_{selected_type.replace(' ', '_').lower()}.txt",
            mime="text/plain"
        )

with col2:
    if st.button("🖼️ Save 3D View", use_container_width=True):
        st.info("3D model view saved to session. Use browser's save function to download the visualization.")

with col3:
    if st.button("📋 Generate Quote", use_container_width=True):
        # Store configuration for quote generation
        st.session_state.container_config = config
        st.switch_page("pages/4_Quote_Generator.py")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>KAN-BUD Advanced 3D Container Visualization System</p>
    <p>Professional Container Modifications • Real-time 3D Models • Technical Analysis</p>
</div>
""", unsafe_allow_html=True)