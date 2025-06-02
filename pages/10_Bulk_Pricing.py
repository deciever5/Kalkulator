# Page configuration - MUST BE FIRST
import streamlit as st
st.set_page_config(
    page_title="Bulk Pricing - KAN-BUD",
    page_icon="📦",
    layout="wide"
)

import pandas as pd
from utils.translations import t, init_language
from utils.shared_header import render_shared_header
from utils.calculations import calculate_container_cost

init_language()

# Initialize session state
if 'employee_logged_in' not in st.session_state:
    st.session_state.employee_logged_in = False
if 'bulk_containers' not in st.session_state:
    st.session_state.bulk_containers = []

# Render shared header
render_shared_header(show_login=False)

st.markdown("""
<style>
.bulk-header {
    background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    color: white;
    text-align: center;
}
.volume-discount {
    background: #f8f9fa;
    border-left: 4px solid #28a745;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 5px;
}
.savings-highlight {
    background: linear-gradient(135deg, #28a745, #20c997);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="bulk-header">
    <h1>📦 Bulk Container Pricing</h1>
    <p>Volume discounts for multiple container projects</p>
</div>
""", unsafe_allow_html=True)

# Volume discount information
st.markdown("## Volume Discount Structure")

discount_data = {
    "Quantity": ["2-4 containers", "5-9 containers", "10-19 containers", "20-49 containers", "50-99 containers", "100+ containers"],
    "Volume Discount": ["5%", "8%", "12%", "15%", "18%", "22%"],
    "Logistics Savings": ["3%", "6%", "10%", "12%", "15%", "18%"],
    "Total Savings": ["8%", "14%", "22%", "27%", "33%", "40%"]
}

st.table(pd.DataFrame(discount_data))

# Container configuration
st.markdown("## Add Containers to Bulk Order")

col1, col2 = st.columns(2)

with col1:
    # Container types including new options
    container_types = {
        "20ft Standard": "20ft Standard",
        "40ft Standard": "40ft Standard", 
        "40ft High Cube": "40ft High Cube",
        "20ft Double Door": "20ft Double Door",
        "40ft Double Door": "40ft Double Door",
        "40ft HC Double Door": "40ft HC Double Door"
    }

    container_type = st.selectbox(
        t('form.labels.container_type'),
        list(container_types.keys()),
        key="bulk_container_type"
    )

    main_purposes = {
        "Office Space": "Office Space",
        "Residential": "Residential",
        "Storage": "Storage",
        "Workshop": "Workshop",
        "Retail": "Retail",
        "Restaurant": "Restaurant",
        "Medical": "Medical",
        "Laboratory": "Laboratory"
    }

    main_purpose = st.selectbox(
        t('form.labels.main_purpose'),
        list(main_purposes.keys()),
        key="bulk_main_purpose"
    )

with col2:
    quantity = st.number_input(
        "Quantity of This Configuration",
        min_value=1, max_value=100, value=1,
        key="bulk_quantity"
    )

    # Modifications
    st.markdown("**Modifications:**")
    num_windows = st.number_input("Windows", min_value=0, max_value=10, value=0, key="bulk_windows")
    num_doors = st.number_input("Additional Doors", min_value=0, max_value=4, value=0, key="bulk_doors")
    electrical = st.checkbox("Electrical System", key="bulk_electrical")
    plumbing = st.checkbox("Plumbing System", key="bulk_plumbing")

# Add to bulk order
if st.button("Add to Bulk Order", type="primary"):
    from utils.animations import show_loading_animation, show_success_animation

    container_config = {
        "container_type": container_type,
        "main_purpose": main_purpose,
        "num_windows": num_windows,
        "num_doors": num_doors,
        "electrical_system": electrical,
        "plumbing_system": plumbing,
        "hvac_system": False,
        "insulation": False,
        "delivery_zone": "poland"
    }

    # Show loading animation
    show_loading_animation("Adding containers to bulk order...", 2)

    # Add multiple containers based on quantity
    for _ in range(quantity):
        st.session_state.bulk_containers.append(container_config.copy())

    # Show success animation
    show_success_animation(f"Added {quantity} containers successfully!", 1)
    st.rerun()

# Display current bulk order
if st.session_state.bulk_containers:
    st.markdown("## Current Bulk Order")

    total_quantity = len(st.session_state.bulk_containers)

    # Calculate volume discounts
    volume_discounts = {
        2: 0.05, 5: 0.08, 10: 0.12, 20: 0.15, 50: 0.18, 100: 0.22
    }

    logistics_savings = {
        2: 0.03, 5: 0.06, 10: 0.10, 20: 0.12, 50: 0.15, 100: 0.18
    }

    volume_discount_rate = 0.0
    logistics_savings_rate = 0.0

    for min_qty, disc in sorted(volume_discounts.items(), reverse=True):
        if total_quantity >= min_qty:
            volume_discount_rate = disc
            break

    for min_qty, save in sorted(logistics_savings.items(), reverse=True):
        if total_quantity >= min_qty:
            logistics_savings_rate = save
            break

    # Calculate total costs
    total_base_cost = 0
    individual_costs = []

    for i, container in enumerate(st.session_state.bulk_containers):
        try:
            cost_result = calculate_container_cost(container)
            
            # Handle dictionary return type from calculate_container_cost
            if isinstance(cost_result, dict):
                cost = cost_result.get('total_cost', 0)
            elif isinstance(cost_result, (int, float)):
                cost = cost_result
            else:
                cost = 15000  # Default estimate
                
            individual_costs.append({
                "ID": i + 1,
                "Type": container["container_type"],
                "Purpose": container["main_purpose"],
                "Cost (€)": f"{cost:,.0f}"
            })
            total_base_cost += cost
            
        except Exception as e:
            # Fallback calculation
            estimated_cost = 15000
            individual_costs.append({
                "ID": i + 1,
                "Type": container["container_type"],
                "Purpose": container["main_purpose"],
                "Cost (€)": f"{estimated_cost:,.0f} (estimated)"
            })
            total_base_cost += estimated_costtimated_cost

    # Apply discounts
    volume_discount_amount = total_base_cost * volume_discount_rate
    logistics_savings_amount = total_base_cost * logistics_savings_rate
    total_discount = volume_discount_amount + logistics_savings_amount
    final_total = total_base_cost - total_discount

    # Display summary metrics with animated counters
    from utils.animations import create_animated_counter

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Containers", total_quantity)

    with col2:
        create_animated_counter(total_base_cost, "Base Cost", "€", "")

    with col3:
        create_animated_counter(total_discount, "Total Savings", "€", "")

    with col4:
        create_animated_counter(final_total, "Final Total", "€", "")

    # Savings highlight
    if total_discount > 0:
        savings_percentage = (total_discount / total_base_cost * 100)
        st.markdown(f"""
        <div class="savings-highlight">
            <h3>💰 You Save €{total_discount:,.0f} ({savings_percentage:.1f}%)</h3>
            <p>Volume Discount: {volume_discount_rate*100:.0f}% + Logistics Savings: {logistics_savings_rate*100:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)

    # Detailed breakdown
    st.markdown("### Cost Breakdown")

    breakdown_data = {
        "Item": [
            "Base Cost (All Containers)",
            f"Volume Discount ({volume_discount_rate*100:.1f}%)",
            f"Logistics Savings ({logistics_savings_rate*100:.1f}%)",
            "Final Total"
        ],
        "Amount (€)": [
            f"{total_base_cost:,.0f}",
            f"-{volume_discount_amount:,.0f}",
            f"-{logistics_savings_amount:,.0f}",
            f"{final_total:,.0f}"
        ]
    }

    st.table(pd.DataFrame(breakdown_data))

    # Individual containers
    with st.expander("Individual Container Details"):
        st.dataframe(pd.DataFrame(individual_costs), use_container_width=True)

    # Bulk benefits
    st.markdown("### Bulk Order Benefits")

    benefits = []
    if total_quantity >= 2:
        benefits.extend(["✅ Volume pricing discounts", "✅ Reduced per-unit logistics costs"])
    if total_quantity >= 5:
        benefits.extend(["✅ Priority production scheduling", "✅ Dedicated project manager"])
    if total_quantity >= 10:
        benefits.extend(["✅ Parallel production capabilities", "✅ Batch delivery coordination"])
    if total_quantity >= 20:
        benefits.extend(["✅ Custom design consultation", "✅ On-site installation support"])

    for benefit in benefits:
        st.markdown(benefit)

    # Project timeline
    st.markdown("### Project Timeline")
    base_weeks = 8 + (total_quantity // 10) * 2
    if total_quantity >= 10:
        base_weeks *= 0.9  # Parallel processing benefits

    timeline_data = {
        "Phase": ["Design & Permits", "Material Procurement", "Production", "Quality Control", "Delivery"],
        "Duration": ["2-3 weeks", "1-2 weeks", f"{int(base_weeks - 4)} weeks", "1 week", "1-2 weeks"]
    }

    st.table(pd.DataFrame(timeline_data))

    # Action buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Clear Bulk Order", type="secondary"):
            st.session_state.bulk_containers = []
            st.rerun()

    with col2:
        if st.button("Generate Quote", type="primary"):
            st.success("Quote request submitted! Our team will contact you within 24 hours.")

else:
    st.info("Add containers to your bulk order to see pricing calculations and volume discounts.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("Custom Sizing →", use_container_width=True):
        st.switch_page("pages/11_Custom_Sizing.py")