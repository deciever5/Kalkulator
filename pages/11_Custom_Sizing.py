# Page configuration - MUST BE FIRST
import streamlit as st
st.set_page_config(
    page_title="Custom Sizing - KAN-BUD",
    page_icon="📐",
    layout="wide"
)

import pandas as pd
from utils.translations import t, init_language
from utils.shared_header import render_shared_header
import math

init_language()

# Initialize session state
if 'employee_logged_in' not in st.session_state:
    st.session_state.employee_logged_in = False

# Render shared header
render_shared_header(show_login=False)

st.markdown("""
<style>
.custom-header {
    background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
}
.dimension-card {
    background: white;
    border: 2px solid #e9ecef;
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
    text-align: center;
}
.warning-box {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
.error-box {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="custom-header">
    <h1>📐 Custom Container Sizing</h1>
    <p>Design containers with your exact specifications</p>
</div>
""", unsafe_allow_html=True)

# Dimension limits information
st.markdown("## Dimension Limits")
limits_data = {
    "Dimension": ["Length", "Width", "Height"],
    "Minimum": ["3.0m", "2.0m", "2.0m"],
    "Maximum": ["15.0m", "4.0m", "4.0m"],
    "Special Transport Required": ["> 12.2m", "> 2.44m", "> 2.9m"]
}
st.table(pd.DataFrame(limits_data))

# Dimension inputs
st.markdown("## Container Dimensions")

col1, col2, col3 = st.columns(3)

with col1:
    length = st.number_input(
        "Length (meters)",
        min_value=3.0, max_value=15.0, value=6.0, step=0.1,
        help="Container length in meters"
    )

with col2:
    width = st.number_input(
        "Width (meters)", 
        min_value=2.0, max_value=4.0, value=2.4, step=0.1,
        help="Container width in meters"
    )

with col3:
    height = st.number_input(
        "Height (meters)",
        min_value=2.0, max_value=4.0, value=2.6, step=0.1,
        help="Container height in meters"
    )

# Validation
errors = []
warnings = []

# Check dimensions
if length < 3.0 or width < 2.0 or height < 2.0:
    errors.append("Dimensions below minimum requirements")

if length > 15.0 or width > 4.0 or height > 4.0:
    errors.append("Dimensions exceed maximum limits")

# Transportation warnings
if length > 12.2:
    warnings.append("Length > 12.2m requires special transport permits")
if width > 2.44:
    warnings.append("Width > 2.44m requires special transport permits")
if height > 2.9:
    warnings.append("Height > 2.9m requires special transport permits")

# Structural warnings
aspect_ratio = length / width if width > 0 else 0
if aspect_ratio > 6:
    warnings.append("High aspect ratio may require additional structural support")

area = length * width
if area > 35:
    warnings.append("Large floor area may require foundation engineering")

# Display errors and warnings
for error in errors:
    st.markdown(f'<div class="error-box">❌ {error}</div>', unsafe_allow_html=True)

for warning in warnings:
    st.markdown(f'<div class="warning-box">⚠️ {warning}</div>', unsafe_allow_html=True)

if not errors:
    # Calculate specifications
    floor_area = length * width
    internal_volume = length * width * height
    wall_area = 2 * (length * height + width * height)
    roof_area = length * width
    total_surface_area = wall_area + roof_area + floor_area
    
    # Weight calculations
    wall_thickness = 0.002  # 2mm
    steel_density = 7850  # kg/m³
    steel_volume = total_surface_area * wall_thickness
    estimated_weight = steel_volume * steel_density
    max_payload = min(25000, (floor_area * 1000))
    
    # Display specifications
    st.markdown("## Container Specifications")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="dimension-card">
            <h4>Floor Area</h4>
            <h2>{floor_area:.1f} m²</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="dimension-card">
            <h4>Internal Volume</h4>
            <h2>{internal_volume:.1f} m³</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="dimension-card">
            <h4>Estimated Weight</h4>
            <h2>{estimated_weight:.0f} kg</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="dimension-card">
            <h4>Max Payload</h4>
            <h2>{max_payload:.0f} kg</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="dimension-card">
            <h4>Wall Area</h4>
            <h2>{wall_area:.1f} m²</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="dimension-card">
            <h4>Surface Area</h4>
            <h2>{total_surface_area:.1f} m²</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Modifications
    st.markdown("## Modifications")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_windows = st.number_input("Number of Windows", min_value=0, max_value=10, value=0)
        num_doors = st.number_input("Additional Doors", min_value=0, max_value=4, value=0)
    
    with col2:
        electrical = st.checkbox("Electrical System")
        plumbing = st.checkbox("Plumbing System")
        hvac = st.checkbox("HVAC System")
    
    # Pricing calculation
    base_price_per_sqm = 450  # EUR per square meter
    custom_fabrication_multiplier = 1.3  # 30% premium
    steel_cost_per_kg = 2.8  # EUR per kg
    
    # Base costs
    base_cost = floor_area * base_price_per_sqm
    custom_premium = base_cost * (custom_fabrication_multiplier - 1)
    steel_cost = steel_volume * steel_density * steel_cost_per_kg
    engineering_cost = base_cost * 0.15  # 15% of base cost
    
    # Transport cost
    base_transport = 1200
    permit_cost = 800 if (length > 12.2 or width > 2.44 or height > 2.9) else 0
    oversized_multiplier = 1.5 if (length > 13 or width > 3 or height > 3) else 1.0
    transport_cost = (base_transport + permit_cost) * oversized_multiplier
    
    # Modification costs (with custom premium)
    custom_mod_multiplier = 1.2
    modification_cost = 0
    
    if num_windows > 0:
        modification_cost += num_windows * 900 * custom_mod_multiplier
    if num_doors > 0:
        modification_cost += num_doors * 1200 * custom_mod_multiplier
    if electrical:
        modification_cost += (floor_area * 180) * custom_mod_multiplier
    if plumbing:
        modification_cost += (floor_area * 220) * custom_mod_multiplier
    if hvac:
        modification_cost += (floor_area * 280) * custom_mod_multiplier
    
    total_cost = (base_cost + custom_premium + steel_cost + 
                 engineering_cost + transport_cost + modification_cost)
    
    # Display pricing
    st.markdown("## Pricing Breakdown")
    
    cost_data = {
        "Cost Item": [
            "Base Container Cost",
            "Custom Fabrication Premium",
            "Material Costs",
            "Engineering & Design",
            "Transport Costs",
            "Modifications",
            "Total Cost"
        ],
        "Amount (€)": [
            f"{base_cost:,.0f}",
            f"{custom_premium:,.0f}",
            f"{steel_cost:,.0f}",
            f"{engineering_cost:,.0f}",
            f"{transport_cost:,.0f}",
            f"{modification_cost:,.0f}",
            f"{total_cost:,.0f}"
        ]
    }
    
    df = pd.DataFrame(cost_data)
    # Highlight total row
    def highlight_total(row):
        return ['background-color: #e8f5e8' if row.name == len(df)-1 else '' for _ in row]
    
    st.dataframe(df.style.apply(highlight_total, axis=1), use_container_width=True)
    
    # Total cost highlight
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;">
        <h2>Total Cost: €{total_cost:,.0f}</h2>
        <p>Including all customizations and engineering</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Important notes
    st.markdown("## Important Notes")
    
    notes = [
        "Custom containers require 30% premium over standard pricing",
        "Engineering design and structural calculations included",
        "Special transport arrangements may be required",
        "Lead time: 12-16 weeks for custom fabrication",
        "Foundation requirements may vary based on size and local regulations",
        "Building permits required for most installations"
    ]
    
    for note in notes:
        st.info(note)

else:
    st.error("Please adjust dimensions to meet requirements before seeing specifications and pricing.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("← Back to Bulk Pricing", use_container_width=True):
        st.switch_page("pages/10_Bulk_Pricing.py")

with col2:
    if st.button("Send Inquiry →", use_container_width=True):
        st.switch_page("pages/8_Send_Inquiry.py")