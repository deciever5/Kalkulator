import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.calculations import StructuralCalculations
from utils.ai_services import OpenAIService, AnthropicService, GroqService
from utils.container_database import ContainerDatabase
from utils.i18n import t, get_locale, set_locale, init_i18n

st.set_page_config(page_title="Technical Analysis", page_icon="🔧", layout="wide")

# Employee access control
if 'employee_logged_in' not in st.session_state:
    st.session_state.employee_logged_in = False

lang = st.session_state.get('language', 'en')

if not st.session_state.employee_logged_in:
    st.title("🔒 " + t('access_denied'))
    st.error(t("technical_analysis_employee_only"))
    st.info(t("login_employee_sidebar"))
    st.markdown("**" + t("employee_password") + ":** kan-bud-employee-2024")
    st.stop()

# Initialize services
if 'container_db' not in st.session_state:
    st.session_state.container_db = ContainerDatabase()

if 'calculations' not in st.session_state:
    st.session_state.calculations = StructuralCalculations()

if 'openai_service' not in st.session_state:
    st.session_state.openai_service = OpenAIService()

# Initialize i18n
init_i18n()

# Language selector with flag buttons
col_lang1, col_lang2, col_lang3, col_lang4, col_spacer = st.columns([1, 1, 1, 1, 2])

current_lang = get_locale()

with col_lang1:
    if st.button(f"🇵🇱 Polski", key="lang_pl_tech", 
                type="primary" if current_lang == 'pl' else "secondary",
                use_container_width=True):
        set_locale('pl')
        st.rerun()

with col_lang2:
    if st.button(f"🇬🇧 English", key="lang_en_tech", 
                type="primary" if current_lang == 'en' else "secondary",
                use_container_width=True):
        set_locale('en')
        st.rerun()

with col_lang3:
    if st.button(f"🇩🇪 Deutsch", key="lang_de_tech", 
                type="primary" if current_lang == 'de' else "secondary",
                use_container_width=True):
        set_locale('de')
        st.rerun()

with col_lang4:
    if st.button(f"🇳🇱 Nederlands", key="lang_nl_tech", 
                type="primary" if current_lang == 'nl' else "secondary",
                use_container_width=True):
        set_locale('nl')
        st.rerun()

st.markdown("""
""")

st.title("🔧 " + t("technical_analysis"))
st.markdown("*" + t("container_project_analysis") + "*")

# Check if configuration exists
if 'container_config' not in st.session_state or not st.session_state.container_config:
    st.warning("⚠️ " + t("no_container_config"))
    if st.button(t("go_to_configurator")):
        st.switch_page("pages/1_Container_Configurator.py")
    st.stop()

config = st.session_state.container_config

# Analysis parameters
st.subheader("⚙️ " + t("analysis_parameters"))
col1, col2, col3 = st.columns(3)

with col1:
    building_code = st.selectbox(
        t("building_code_label"),
        ["IBC (International Building Code)", "Local Building Code", "Marine Code", "Industrial Standard"],
        help=t("building_code_help")
    )

with col2:
    safety_factor = st.selectbox(
        t("safety_factor_label"),
        ["Standard (1.5)", "Conservative (2.0)", "High Risk (2.5)", "Marine/Offshore (3.0)"],
        help=t("safety_factor_help")
    )

with col3:
    analysis_depth = st.selectbox(
        t("analysis_depth_label"),
        ["Basic", "Standard", "Comprehensive", "Engineering Grade"],
        help=t("analysis_depth_help")
    )

# Environmental parameters
st.subheader("🌍 " + t("environmental_conditions"))
col1, col2, col3, col4 = st.columns(4)

with col1:
    wind_load = st.number_input(t("wind_load_label"), min_value=0, max_value=320, value=145)

with col2:
    snow_load = st.number_input(t("snow_load_label"), min_value=0.0, max_value=5.0, value=1.0, step=0.1)

with col3:
    climate_zone = st.selectbox(t("climate_zone_label"), [
        "Umiarkowana (Europa Środkowa)",
        "Subpolarna (Skandynawia)",
        "Morska (Wybrzeża)",
        "Górska (Alpy, Karpaty)",
        "Kontynentalna (Europa Wschodnia)",
        "Śródziemnomorska (Południe)"
    ])

with col4:
    environmental_conditions = st.selectbox(t("environmental_conditions_label"), [
        "Standardowe",
        "Wysokie zasolenie (morskie)",
        "Wysoka wilgotność",
        "Przemysłowe (zanieczyszczenia)",
        "Agresywne chemicznie",
        "Ekstremalne temperatury"
    ])

# Generate analysis button
if st.button("🔍 " + t("run_technical_analysis"), type="primary", use_container_width=True):
    with st.spinner("🔧 " + t("performing_analysis")):

        # Prepare analysis parameters
        analysis_params = {
            "building_code": building_code,
            "safety_factor": float(safety_factor.split("(")[1].split(")")[0]),
            "wind_load": wind_load,
            "snow_load": snow_load,
            "climate_zone": climate_zone,
            "environmental_conditions": environmental_conditions,
            "analysis_depth": analysis_depth
        }

        try:
            # Perform structural calculations
            structural_analysis = st.session_state.calculations.perform_structural_analysis(
                config, analysis_params
            )

            # Get AI technical recommendations using Anthropic (primary) 
            try:
                ai_analysis = st.session_state.anthropic_service.generate_technical_analysis(
                    config, analysis_params, structural_analysis
                )
            except Exception as e:
                # Fallback to OpenAI if available
                try:
                    ai_analysis = st.session_state.openai_service.generate_technical_analysis(
                        config, analysis_params, structural_analysis
                    )
                except Exception as e2:
                    st.warning("⚠️ " + t("ai_analysis_unavailable"))
                    ai_analysis = {}

            # Store results
            st.session_state.technical_analysis = {
                "structural": structural_analysis,
                "ai_analysis": ai_analysis,
                "parameters": analysis_params
            }

            st.success("✅ " + t("analysis_completed"))
            st.rerun()

        except Exception as e:
            st.error(f"❌ " + t("analysis_error") + f": {str(e)}")

# Display results if available
if 'technical_analysis' in st.session_state:
    results = st.session_state.technical_analysis
    structural = results["structural"]
    ai_analysis = results["ai_analysis"]

    st.divider()
    st.subheader("📊 " + t("structural_analysis_results"))

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        load_ratio = structural.get("load_ratio", 0)
        color = "normal" if load_ratio < 0.8 else "inverse" if load_ratio < 1.0 else "off"
        st.metric(
            t("load_ratio_label"),
            f"{load_ratio:.2f}",
            delta=f"{'✅ ' + t('safe') if load_ratio < 1.0 else '⚠️ ' + t('over_stressed')}",
            delta_color=color
        )

    with col2:
        deflection = structural.get("max_deflection", 0)
        deflection_limit = structural.get("deflection_limit", 1)
        deflection_ok = deflection < deflection_limit
        st.metric(
            t("max_deflection_label"),
            f"{deflection:.3f}",
            delta=f"{t('limit')}: {deflection_limit:.3f}",
            delta_color="normal" if deflection_ok else "inverse"
        )

    with col3:
        stress_ratio = structural.get("stress_ratio", 0)
        st.metric(
            t("stress_ratio_label"),
            f"{stress_ratio:.2f}",
            delta=f"{'✅ OK' if stress_ratio < 1.0 else '❌ ' + t('exceeded')}",
            delta_color="normal" if stress_ratio < 1.0 else "inverse"
        )

    with col4:
        foundation_req = structural.get("foundation_required", "Standard")
        st.metric(
            t("foundation_req_label"),
            foundation_req,
            help=t("foundation_req_help")
        )

    # Structural diagrams and visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📐 " + t("load_distribution"))

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
                title=t("load_distribution_diagram"),
                xaxis_title=t("length_m"),
                yaxis_title=t("load_kn_m"),
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🏗️ " + t("stress_analysis"))

        # Create stress visualization
        if "stress_points" in structural:
            stress_data = structural["stress_points"]

            fig = px.scatter(
                x=stress_data.get("x_coords", []),
                y=stress_data.get("y_coords", []),
                color=stress_data.get("stress_values", []),
                size=stress_data.get("stress_values", []),
                title=t("stress_distribution"),
                labels={"color": t("stress_psi")},
                color_continuous_scale="Viridis"
            )

            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    # Compliance analysis
    st.subheader("✅ " + t("compliance_analysis"))

    compliance = structural.get("compliance", {})
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**" + t("building_code_compliance") + ":**")
        for code, status in compliance.get("building_codes", {}).items():
            icon = "✅" if status == "Pass" else "❌" if status == "Fail" else "⚠️"
            st.write(f"{icon} {code}: {status}")

    with col2:
        st.markdown("**" + t("safety_requirements") + ":**")
        for req, status in compliance.get("safety", {}).items():
            icon = "✅" if status == "Pass" else "❌" if status == "Fail" else "⚠️"
            st.write(f"{icon} {req}: {status}")

    # AI Technical Recommendations
    if ai_analysis and isinstance(ai_analysis, dict):
        st.subheader("🤖 " + t("ai_technical_recommendations"))

        if "structural_recommendations" in ai_analysis:
            st.markdown("**🏗️ " + t("structural_recommendations") + ":**")
            for rec in ai_analysis["structural_recommendations"]:
                st.info(f"💡 {rec}")

        if "modification_suggestions" in ai_analysis:
            st.markdown("**🔧 " + t("modification_suggestions") + ":**")
            for suggestion in ai_analysis["modification_suggestions"]:
                st.write(f"• {suggestion}")

        if "risk_mitigation" in ai_analysis:
            st.markdown("**⚠️ " + t("risk_mitigation") + ":**")
            for risk in ai_analysis["risk_mitigation"]:
                st.warning(f"• {risk}")

        if "cost_impact" in ai_analysis:
            st.markdown("**💰 " + t("cost_impact_analysis") + ":**")
            cost_impact = ai_analysis["cost_impact"]
            if isinstance(cost_impact, dict):
                for category, impact in cost_impact.items():
                    st.write(f"**{category.replace('_', ' ').title()}:** {impact}")

    # Material specifications
    st.subheader("🛠️ " + t("material_specifications"))

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
    st.subheader("📋 " + t("engineering_requirements"))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**" + t("required_drawings") + ":**")
        drawings = structural.get("required_drawings", [])
        for drawing in drawings:
            st.write(f"• {drawing}")

    with col2:
        st.markdown("**" + t("professional_requirements") + ":**")
        requirements = structural.get("professional_requirements", [])
        for req in requirements:
            st.write(f"• {req}")

# Action buttons
if 'technical_analysis' in st.session_state:
    st.divider()
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("💰 " + t("view_cost_estimate"), use_container_width=True):
            st.switch_page("pages/2_AI_Cost_Estimator.py")

    with col2:
        if st.button("📄 " + t("generate_quote"), use_container_width=True):
            st.switch_page("pages/4_Quote_Generator.py")

    with col3:
        if st.button("⚖️ " + t("compare_options"), use_container_width=True):
            st.switch_page("pages/5_Comparison_Tool.py")

    with col4:
        if st.button("📊 " + t("export_analysis"), use_container_width=True):
            # Export functionality would be implemented here
            st.success("✅ " + t("analysis_exported"))

# Additional information
with st.expander("ℹ️ " + t("about_technical_analysis")):
    st.markdown(t("technical_analysis_includes"))

# Navigation Buttons
st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button(t('ui.back_to_home'), key="home_nav", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button(t('ui.go_to_configurator'), key="config_nav", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")