import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.container_database import ContainerDatabase
from utils.calculations import StructuralCalculations

st.set_page_config(page_title="Container Configurator", page_icon="📦", layout="wide")

# Initialize services
if 'container_db' not in st.session_state:
    st.session_state.container_db = ContainerDatabase()

if 'calculations' not in st.session_state:
    st.session_state.calculations = StructuralCalculations()

st.title("📦 Container Configurator")
st.markdown("*Configure your container specifications and modifications*")

# Initialize session state for configuration
if 'container_config' not in st.session_state:
    st.session_state.container_config = {}

# Main configuration interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🏗️ Base Container Specifications")
    
    # Container type selection
    container_types = st.session_state.container_db.get_container_types()
    selected_type = st.selectbox(
        "Container Type",
        options=list(container_types.keys()),
        help="Select the base container type for modification"
    )
    
    if selected_type:
        container_specs = container_types[selected_type]
        st.session_state.container_config['base_type'] = selected_type
        
        # Display base specifications
        spec_col1, spec_col2 = st.columns(2)
        with spec_col1:
            st.metric("Length (ft)", container_specs['length'])
            st.metric("Width (ft)", container_specs['width'])
        with spec_col2:
            st.metric("Height (ft)", container_specs['height'])
            st.metric("Weight (lbs)", f"{container_specs['weight']:,}")
    
    st.divider()
    
    # Use case selection
    st.subheader("🎯 Intended Use Case")
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
    
    selected_use_case = st.selectbox("Primary Use Case", use_cases)
    st.session_state.container_config['use_case'] = selected_use_case
    
    # Occupancy and environment
    col_occ1, col_occ2 = st.columns(2)
    with col_occ1:
        occupancy = st.number_input("Expected Occupancy", min_value=1, max_value=50, value=4)
    with col_occ2:
        environment = st.selectbox("Environment", ["Indoor", "Outdoor", "Marine", "Industrial"])
    
    st.session_state.container_config.update({
        'occupancy': occupancy,
        'environment': environment
    })

with col2:
    st.subheader("🔧 Modification Requirements")
    
    # Structural modifications
    st.markdown("**Structural Modifications**")
    modifications = {}
    
    # Windows and doors
    col_mod1, col_mod2 = st.columns(2)
    with col_mod1:
        modifications['windows'] = st.number_input("Number of Windows", min_value=0, max_value=20, value=0)
        modifications['doors'] = st.number_input("Number of Doors", min_value=1, max_value=10, value=1)
    with col_mod2:
        modifications['skylights'] = st.number_input("Skylights", min_value=0, max_value=10, value=0)
        modifications['vents'] = st.number_input("Ventilation Openings", min_value=0, max_value=20, value=2)
    
    # Structural reinforcements
    st.markdown("**Structural Reinforcements**")
    modifications['reinforcement_walls'] = st.checkbox("Wall Reinforcement")
    modifications['reinforcement_roof'] = st.checkbox("Roof Reinforcement")
    modifications['reinforcement_floor'] = st.checkbox("Floor Reinforcement")
    modifications['additional_support'] = st.checkbox("Additional Support Beams")
    
    # Systems and utilities
    st.markdown("**Systems & Utilities**")
    col_sys1, col_sys2 = st.columns(2)
    with col_sys1:
        modifications['electrical'] = st.checkbox("Electrical System")
        modifications['plumbing'] = st.checkbox("Plumbing System")
    with col_sys2:
        modifications['hvac'] = st.checkbox("HVAC System")
        modifications['insulation'] = st.checkbox("Insulation Package")
    
    # Interior finishes
    st.markdown("**Interior Finishes**")
    finish_level = st.selectbox("Finish Level", ["Basic", "Standard", "Premium", "Luxury"])
    modifications['finish_level'] = finish_level
    
    flooring_type = st.selectbox("Flooring", ["Plywood", "Vinyl", "Carpet", "Hardwood", "Polished Concrete"])
    modifications['flooring'] = flooring_type
    
    st.session_state.container_config['modifications'] = modifications

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
    # Simple 3D visualization placeholder
    st.markdown("**Container Visualization**")
    
    if 'base_type' in st.session_state.container_config:
        # Create a simple 3D wireframe representation
        container_specs = container_types[st.session_state.container_config['base_type']]
        
        # Define container corners
        length = container_specs['length']
        width = container_specs['width']
        height = container_specs['height']
        
        # Create 3D box visualization
        fig = go.Figure()
        
        # Define the 8 corners of the container
        x = [0, length, length, 0, 0, length, length, 0]
        y = [0, 0, width, width, 0, 0, width, width]
        z = [0, 0, 0, 0, height, height, height, height]
        
        # Create the wireframe
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # bottom face
            [4, 5], [5, 6], [6, 7], [7, 4],  # top face
            [0, 4], [1, 5], [2, 6], [3, 7]   # vertical edges
        ]
        
        for edge in edges:
            fig.add_trace(go.Scatter3d(
                x=[x[edge[0]], x[edge[1]]],
                y=[y[edge[0]], y[edge[1]]],
                z=[z[edge[0]], z[edge[1]]],
                mode='lines',
                line=dict(color='blue', width=4),
                showlegend=False
            ))
        
        # Add modifications visualization
        mods = st.session_state.container_config.get('modifications', {})
        
        # Add windows (simple rectangles on sides)
        if mods.get('windows', 0) > 0:
            for i in range(min(mods['windows'], 4)):  # Max 4 windows for visualization
                side = i % 2  # Alternate between sides
                if side == 0:  # Front/back
                    fig.add_trace(go.Scatter3d(
                        x=[length/4 + (i//2)*length/2, 3*length/4 + (i//2)*length/2],
                        y=[0, 0] if i < 2 else [width, width],
                        z=[height/3, 2*height/3],
                        mode='lines',
                        line=dict(color='lightblue', width=6),
                        name='Windows' if i == 0 else None,
                        showlegend=i == 0
                    ))
        
        fig.update_layout(
            scene=dict(
                xaxis_title='Length (ft)',
                yaxis_title='Width (ft)',
                zaxis_title='Height (ft)',
                aspectmode='data'
            ),
            title=f"{st.session_state.container_config['base_type']} Configuration",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Action buttons
st.divider()
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💰 Get AI Cost Estimate", use_container_width=True):
        st.switch_page("pages/2_AI_Cost_Estimator.py")

with col2:
    if st.button("🔧 Technical Analysis", use_container_width=True):
        st.switch_page("pages/3_Technical_Analysis.py")

with col3:
    if st.button("📄 Generate Quote", use_container_width=True):
        st.switch_page("pages/4_Quote_Generator.py")

with col4:
    if st.button("⚖️ Compare Options", use_container_width=True):
        st.switch_page("pages/5_Comparison_Tool.py")

# Save configuration
if st.button("💾 Save Configuration", use_container_width=True):
    if 'container_config' in st.session_state and st.session_state.container_config:
        st.success("✅ Configuration saved successfully!")
        st.json(st.session_state.container_config)
    else:
        st.error("❌ Please complete the configuration before saving.")
