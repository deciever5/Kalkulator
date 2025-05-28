import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.calculations import StructuralCalculations
from utils.ai_services import OpenAIService, AnthropicService
from utils.container_database import ContainerDatabase

st.set_page_config(page_title="Technical Analysis", page_icon="🔧", layout="wide")

# Initialize services
if 'container_db' not in st.session_state:
    st.session_state.container_db = ContainerDatabase()

if 'calculations' not in st.session_state:
    st.session_state.calculations = StructuralCalculations()

if 'openai_service' not in st.session_state:
    st.session_state.openai_service = OpenAIService()

st.title("🔧 Technical Analysis")
st.markdown("*Comprehensive structural and compliance analysis for your container project*")

# Check if configuration exists
if 'container_config' not in st.session_state or not st.session_state.container_config:
    st.warning("⚠️ No container configuration found. Please configure your container first.")
    if st.button("Go to Container Configurator"):
        st.switch_page("pages/1_Container_Configurator.py")
    st.stop()

config = st.session_state.container_config

# Analysis parameters
st.subheader("⚙️ Analysis Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    building_code = st.selectbox(
        "Building Code",
        ["IBC (International Building Code)", "Local Building Code", "Marine Code", "Industrial Standard"],
        help="Select applicable building code for compliance analysis"
    )

with col2:
    safety_factor = st.selectbox(
        "Safety Factor",
        ["Standard (1.5)", "Conservative (2.0)", "High Risk (2.5)", "Marine/Offshore (3.0)"],
        help="Safety factor for structural calculations"
    )

with col3:
    analysis_depth = st.selectbox(
        "Analysis Depth",
        ["Basic", "Standard", "Comprehensive", "Engineering Grade"],
        help="Level of technical analysis required"
    )

# Environmental parameters
st.subheader("🌍 Environmental Conditions")
col1, col2, col3, col4 = st.columns(4)

with col1:
    wind_load = st.number_input("Wind Load (mph)", min_value=0, max_value=200, value=90)

with col2:
    snow_load = st.number_input("Snow Load (psf)", min_value=0, max_value=100, value=20)

with col3:
    seismic_zone = st.selectbox("Seismic Zone", ["Low", "Moderate", "High", "Very High"])

with col4:
    corrosion_env = st.selectbox("Corrosion Environment", ["Mild", "Moderate", "Severe", "Marine"])

# Generate analysis button
if st.button("🔍 Run Technical Analysis", type="primary", use_container_width=True):
    with st.spinner("🔧 Performing structural calculations and compliance analysis..."):
        
        # Prepare analysis parameters
        analysis_params = {
            "building_code": building_code,
            "safety_factor": float(safety_factor.split("(")[1].split(")")[0]),
            "wind_load": wind_load,
            "snow_load": snow_load,
            "seismic_zone": seismic_zone,
            "corrosion_env": corrosion_env,
            "analysis_depth": analysis_depth
        }
        
        try:
            # Perform structural calculations
            structural_analysis = st.session_state.calculations.perform_structural_analysis(
                config, analysis_params
            )
            
            # Get AI technical recommendations
            ai_analysis = st.session_state.openai_service.generate_technical_analysis(
                config, analysis_params, structural_analysis
            )
            
            # Store results
            st.session_state.technical_analysis = {
                "structural": structural_analysis,
                "ai_analysis": ai_analysis,
                "parameters": analysis_params
            }
            
            st.success("✅ Technical analysis completed successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error during technical analysis: {str(e)}")

# Display results if available
if 'technical_analysis' in st.session_state:
    results = st.session_state.technical_analysis
    structural = results["structural"]
    ai_analysis = results["ai_analysis"]
    
    st.divider()
    st.subheader("📊 Structural Analysis Results")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        load_ratio = structural.get("load_ratio", 0)
        color = "normal" if load_ratio < 0.8 else "inverse" if load_ratio < 1.0 else "off"
        st.metric(
            "Load Ratio",
            f"{load_ratio:.2f}",
            delta=f"{'✅ Safe' if load_ratio < 1.0 else '⚠️ Over-stressed'}",
            delta_color=color
        )
    
    with col2:
        deflection = structural.get("max_deflection", 0)
        deflection_limit = structural.get("deflection_limit", 1)
        deflection_ok = deflection < deflection_limit
        st.metric(
            "Max Deflection (in)",
            f"{deflection:.3f}",
            delta=f"Limit: {deflection_limit:.3f}",
            delta_color="normal" if deflection_ok else "inverse"
        )
    
    with col3:
        stress_ratio = structural.get("stress_ratio", 0)
        st.metric(
            "Stress Ratio",
            f"{stress_ratio:.2f}",
            delta=f"{'✅ OK' if stress_ratio < 1.0 else '❌ Exceeded'}",
            delta_color="normal" if stress_ratio < 1.0 else "inverse"
        )
    
    with col4:
        foundation_req = structural.get("foundation_required", "Standard")
        st.metric(
            "Foundation Req.",
            foundation_req,
            help="Foundation requirements based on loads and soil conditions"
        )
    
    # Structural diagrams and visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📐 Load Distribution")
        
        # Create load distribution diagram
        if "load_distribution" in structural:
            loads = structural["load_distribution"]
            
            fig = go.Figure()
            
            # Add load vectors
            for load_type, data in loads.items():
                fig.add_trace(go.Scatter(
                    x=data.get("x_coords", []),
                    y=data.get("y_coords", []),
                    mode='markers+lines',
                    name=load_type.replace("_", " ").title(),
                    line=dict(width=3)
                ))
            
            fig.update_layout(
                title="Load Distribution Diagram",
                xaxis_title="Length (ft)",
                yaxis_title="Load (lbs/ft)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏗️ Stress Analysis")
        
        # Create stress visualization
        if "stress_points" in structural:
            stress_data = structural["stress_points"]
            
            fig = px.scatter(
                x=stress_data.get("x_coords", []),
                y=stress_data.get("y_coords", []),
                color=stress_data.get("stress_values", []),
                size=stress_data.get("stress_values", []),
                title="Stress Distribution",
                labels={"color": "Stress (psi)"},
                color_continuous_scale="Viridis"
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Compliance analysis
    st.subheader("✅ Compliance Analysis")
    
    compliance = structural.get("compliance", {})
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Building Code Compliance:**")
        for code, status in compliance.get("building_codes", {}).items():
            icon = "✅" if status == "Pass" else "❌" if status == "Fail" else "⚠️"
            st.write(f"{icon} {code}: {status}")
    
    with col2:
        st.markdown("**Safety Requirements:**")
        for req, status in compliance.get("safety", {}).items():
            icon = "✅" if status == "Pass" else "❌" if status == "Fail" else "⚠️"
            st.write(f"{icon} {req}: {status}")
    
    # AI Technical Recommendations
    if ai_analysis and isinstance(ai_analysis, dict):
        st.subheader("🤖 AI Technical Recommendations")
        
        if "structural_recommendations" in ai_analysis:
            st.markdown("**🏗️ Structural Recommendations:**")
            for rec in ai_analysis["structural_recommendations"]:
                st.info(f"💡 {rec}")
        
        if "modification_suggestions" in ai_analysis:
            st.markdown("**🔧 Modification Suggestions:**")
            for suggestion in ai_analysis["modification_suggestions"]:
                st.write(f"• {suggestion}")
        
        if "risk_mitigation" in ai_analysis:
            st.markdown("**⚠️ Risk Mitigation:**")
            for risk in ai_analysis["risk_mitigation"]:
                st.warning(f"• {risk}")
        
        if "cost_impact" in ai_analysis:
            st.markdown("**💰 Cost Impact Analysis:**")
            cost_impact = ai_analysis["cost_impact"]
            if isinstance(cost_impact, dict):
                for category, impact in cost_impact.items():
                    st.write(f"**{category.replace('_', ' ').title()}:** {impact}")
    
    # Material specifications
    st.subheader("🛠️ Material Specifications")
    
    if "materials" in structural:
        materials = structural["materials"]
        
        material_df = pd.DataFrame([
            {
                "Component": comp,
                "Material": spec.get("material", ""),
                "Quantity": spec.get("quantity", ""),
                "Specification": spec.get("specification", "")
            }
            for comp, spec in materials.items()
        ])
        
        st.dataframe(material_df, use_container_width=True)
    
    # Engineering drawings reference
    st.subheader("📋 Engineering Requirements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Required Drawings:**")
        drawings = structural.get("required_drawings", [])
        for drawing in drawings:
            st.write(f"• {drawing}")
    
    with col2:
        st.markdown("**Professional Requirements:**")
        requirements = structural.get("professional_requirements", [])
        for req in requirements:
            st.write(f"• {req}")

# Action buttons
if 'technical_analysis' in st.session_state:
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💰 View Cost Estimate", use_container_width=True):
            st.switch_page("pages/2_AI_Cost_Estimator.py")
    
    with col2:
        if st.button("📄 Generate Quote", use_container_width=True):
            st.switch_page("pages/4_Quote_Generator.py")
    
    with col3:
        if st.button("⚖️ Compare Options", use_container_width=True):
            st.switch_page("pages/5_Comparison_Tool.py")
    
    with col4:
        if st.button("📊 Export Analysis", use_container_width=True):
            # Export functionality would be implemented here
            st.success("✅ Analysis exported successfully!")

# Additional information
with st.expander("ℹ️ About Technical Analysis"):
    st.markdown("""
    **This technical analysis includes:**
    
    - **Structural Calculations:** Load analysis, stress distribution, deflection calculations
    - **Code Compliance:** Building code requirements, safety standards, local regulations
    - **Material Specifications:** Steel grades, connection details, foundation requirements
    - **AI Recommendations:** Intelligent suggestions for optimization and risk mitigation
    - **Professional Requirements:** Engineering drawings, permits, inspections needed
    
    **Important Notes:**
    - This analysis is for preliminary design purposes
    - Final engineering must be performed by a licensed professional
    - Local building codes and regulations may apply
    - Site-specific conditions may require additional analysis
    """)
