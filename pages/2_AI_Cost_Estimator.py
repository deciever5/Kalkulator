import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.groq_service import GroqService
from utils.global_language import init_language, get_current_language, render_language_selector, t, translate_list
from utils.calculations import StructuralCalculations
from utils.container_database import ContainerDatabase

st.set_page_config(page_title="AI Cost Estimator", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

# Initialize services
if 'container_db' not in st.session_state:
    st.session_state.container_db = ContainerDatabase()

if 'calculations' not in st.session_state:
    st.session_state.calculations = StructuralCalculations()

# Initialize language
init_language()

# Initialize Groq service
if 'groq_service' not in st.session_state:
    st.session_state.groq_service = GroqService()

# Language selector
render_language_selector()

# Navigation header
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button(t('back_to_home'), key="config_nav"):
        st.switch_page("pages/1_Container_Configurator.py")

with col2:
    st.markdown(f"### 🤖 {t('ai_cost_estimation')}")

with col3:
    if st.button(t('back_to_home'), key="home_nav"):
        st.switch_page("app.py")

st.markdown("---")

# Check if configuration exists
if 'container_config' not in st.session_state or not st.session_state.container_config:
    st.warning("⚠️ No container configuration found. Please configure your container first.")
    if st.button("Go to Container Configurator"):
        st.switch_page("pages/1_Container_Configurator.py")
    st.stop()

# Display current configuration summary
with st.expander("📋 Current Configuration", expanded=False):
    config = st.session_state.container_config
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Base Type:** {config.get('base_type', 'Not set')}")
        st.write(f"**Use Case:** {config.get('use_case', 'Not set')}")
        st.write(f"**Occupancy:** {config.get('occupancy', 'Not set')} people")

    with col2:
        st.write(f"**Environment:** {config.get('environment', 'Not set')}")
        mods = config.get('modifications', {})
        mod_count = sum(1 for v in mods.values() if (isinstance(v, bool) and v) or (isinstance(v, int) and v > 0))
        st.write(f"**Modifications:** {mod_count} items")

# AI Model Selection
st.subheader("🧠 AI Model Selection")
col1, col2 = st.columns(2)

with col1:
    ai_model = st.selectbox(
        "Select AI Model",
        ["Groq Llama (Free)", "OpenAI GPT-4o", "Anthropic Claude", "All Models (Comparison)"],
        help="Choose which AI model to use for cost estimation. Groq is completely free!"
    )

with col2:
    estimation_depth = st.selectbox(
        "Estimation Depth",
        ["Quick Estimate", "Detailed Analysis", "Comprehensive Report"],
        help="Choose the level of detail for the cost analysis"
    )

# Cost estimation parameters
st.subheader("⚙️ Estimation Parameters")
col1, col2, col3 = st.columns(3)

with col1:
    project_location = st.selectbox(
        "Project Location",
        ["United States - General", "US - West Coast", "US - East Coast", "US - Midwest", "US - South", "Canada", "International"],
        help="Location affects material and labor costs"
    )

with col2:
    project_timeline = st.selectbox(
        "Project Timeline",
        ["Rush (2-4 weeks)", "Standard (6-8 weeks)", "Extended (10-12 weeks)", "Flexible"],
        help="Timeline affects labor costs and material availability"
    )

with col3:
    quality_level = st.selectbox(
        "Quality Level",
        ["Economy", "Standard", "Premium", "Luxury"],
        help="Quality level affects material selection and finishes"
    )

# Additional considerations
st.subheader("📝 Additional Requirements")
additional_notes = st.text_area(
    "Special Requirements or Notes",
    placeholder="Enter any special requirements, constraints, or additional information that might affect the cost estimate...",
    height=100
)

# Generate estimate button
if st.button("🚀 Generate AI Cost Estimate", type="primary", use_container_width=True):
    with st.spinner("🤖 AI is analyzing your configuration and generating cost estimates..."):

        # Prepare data for AI analysis
        estimation_data = {
            "container_config": st.session_state.container_config,
            "project_location": project_location,
            "project_timeline": project_timeline,
            "quality_level": quality_level,
            "additional_notes": additional_notes,
            "estimation_depth": estimation_depth
        }

        # Calculate base costs using traditional methods
        base_costs = st.session_state.calculations.calculate_base_costs(
            st.session_state.container_config
        )

        try:
            if ai_model == "OpenAI GPT-4o":
                try:
                    estimate = st.session_state.openai_service.generate_cost_estimate(estimation_data, base_costs)
                    st.session_state.ai_estimate = estimate
                except Exception as openai_error:
                    if "quota" in str(openai_error) or "insufficient_quota" in str(openai_error):
                        st.warning("⚠️ OpenAI quota exceeded. Using Anthropic Claude instead.")
                        estimate = st.session_state.anthropic_service.generate_cost_estimate(estimation_data, base_costs)
                        st.session_state.ai_estimate = estimate
                    else:
                        raise openai_error

            elif ai_model == "Anthropic Claude":
                estimate = st.session_state.anthropic_service.generate_cost_estimate(estimation_data, base_costs)
                st.session_state.ai_estimate = estimate
            
            elif ai_model == "Groq Llama (Free)":
                 estimate = st.session_state.groq_service.generate_cost_estimate(estimation_data, base_costs)
                 st.session_state.ai_estimate = estimate

            else:  # Both models
                try:
                    openai_estimate = st.session_state.openai_service.generate_cost_estimate(estimation_data, base_costs)
                except Exception as openai_error:
                    if "quota" in str(openai_error) or "insufficient_quota" in str(openai_error):
                        st.warning("⚠️ OpenAI quota exceeded. Using Anthropic Claude only.")
                        estimate = st.session_state.anthropic_service.generate_cost_estimate(estimation_data, base_costs)
                        st.session_state.ai_estimate = estimate
                    else:
                        raise openai_error
                else:
                    claude_estimate = st.session_state.anthropic_service.generate_cost_estimate(estimation_data, base_costs)

                    # Store both estimates for comparison
                    st.session_state.ai_estimate = {
                        "openai": openai_estimate,
                        "claude": claude_estimate,
                        "comparison": True
                    }

            st.success("✅ AI cost estimate generated successfully!")
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error generating AI estimate: {str(e)}")
            st.info("💡 Please check your API keys and try again. You can also use the traditional calculation method.")

# Display results if available
if 'ai_estimate' in st.session_state and st.session_state.ai_estimate:
    st.divider()

    estimate = st.session_state.ai_estimate

    if isinstance(estimate, dict) and estimate.get("comparison"):
        # Display comparison between models
        st.subheader("🔄 AI Model Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🤖 OpenAI GPT-4o Estimate")
            openai_est = estimate["openai"]
            if isinstance(openai_est, dict):
                st.metric("Total Cost", f"€{openai_est.get('total_cost', 0):,.2f}")
                st.metric("Confidence", f"{openai_est.get('confidence', 0):.1%}")

                if 'breakdown' in openai_est:
                    with st.expander("Cost Breakdown"):
                        for category, cost in openai_est['breakdown'].items():
                            st.write(f"**{category.replace('_', ' ').title()}:** €{cost:,.2f}")

        with col2:
            st.markdown("### 🧠 Anthropic Claude Estimate")
            claude_est = estimate["claude"]
            if isinstance(claude_est, dict):
                st.metric("Total Cost", f"€{claude_est.get('total_cost', 0):,.2f}")
                st.metric("Confidence", f"{claude_est.get('confidence', 0):.1%}")

                if 'breakdown' in claude_est:
                    with st.expander("Cost Breakdown"):
                        for category, cost in claude_est['breakdown'].items():
                            st.write(f"**{category.replace('_', ' ').title()}:** €{cost:,.2f}")

        # Comparison analysis
        if isinstance(openai_est, dict) and isinstance(claude_est, dict):
            openai_total = openai_est.get('total_cost', 0)
            claude_total = claude_est.get('total_cost', 0)

            st.subheader("📊 Comparison Analysis")

            col1, col2, col3 = st.columns(3)
            with col1:
                avg_estimate = (openai_total + claude_total) / 2
                st.metric("Average Estimate", f"€{avg_estimate:,.2f}")

            with col2:
                difference = abs(openai_total - claude_total)
                variance_pct = (difference / avg_estimate) * 100 if avg_estimate > 0 else 0
                st.metric("Variance", f"{variance_pct:.1f}%")

            with col3:
                recommended = "OpenAI" if openai_est.get('confidence', 0) > claude_est.get('confidence', 0) else "Claude"
                st.metric("Recommended", recommended)

    else:
        # Display single model estimate
        st.subheader("💰 AI Cost Estimate Results")

        if isinstance(estimate, dict):
            col1, col2, col3 = st.columns(3)

            with col1:
                total_cost = estimate.get('total_cost', 0)
                st.metric(
                    "Total Estimated Cost",
                    f"€{total_cost:,.2f}",
                    help="Total project cost including materials, labor, and modifications"
                )

            with col2:
                confidence = estimate.get('confidence', 0)
                st.metric(
                    "AI Confidence",
                    f"{confidence:.1%}",
                    help="AI model's confidence in the estimate accuracy"
                )

            with col3:
                timeline = estimate.get('estimated_timeline', 'Not specified')
                st.metric(
                    "Estimated Timeline",
                    timeline,
                    help="Projected completion time for the project"
                )

            # Cost breakdown visualization
            if 'breakdown' in estimate:
                st.subheader("📊 Cost Breakdown")

                breakdown = estimate['breakdown']
                categories = list(breakdown.keys())
                values = list(breakdown.values())

                col1, col2 = st.columns([1, 1])

                with col1:
                    # Pie chart
                    fig_pie = px.pie(
                        values=values,
                        names=[cat.replace('_', ' ').title() for cat in categories],
                        title="Cost Distribution"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

                with col2:
                    # Bar chart
                    fig_bar = px.bar(
                        x=values,
                        y=[cat.replace('_', ' ').title() for cat in categories],
                        orientation='h',
                        title="Cost by Category"
                    )
                    fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig_bar, use_container_width=True)

            # Detailed analysis
            if 'analysis' in estimate:
                st.subheader("🔍 AI Analysis & Recommendations")
                analysis = estimate['analysis']

                if 'recommendations' in analysis:
                    st.markdown("**💡 AI Recommendations:**")
                    for rec in analysis['recommendations']:
                        st.write(f"• {rec}")

                if 'risk_factors' in analysis:
                    st.markdown("**⚠️ Risk Factors:**")
                    for risk in analysis['risk_factors']:
                        st.warning(f"• {risk}")

                if 'cost_optimization' in analysis:
                    st.markdown("**💰 Cost Optimization Opportunities:**")
                    for opt in analysis['cost_optimization']:
                        st.info(f"• {opt}")

# Action buttons
if 'ai_estimate' in st.session_state and st.session_state.ai_estimate:
    st.divider()
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔧 Technical Analysis", use_container_width=True):
            st.switch_page("pages/3_Technical_Analysis.py")

    with col2:
        if st.button("📄 Generate Quote", use_container_width=True):
            st.switch_page("pages/4_Quote_Generator.py")

    with col3:
        if st.button("⚖️ Compare Options", use_container_width=True):
            st.switch_page("pages/5_Comparison_Tool.py")

    with col4:
        if st.button("🔄 New Estimate", use_container_width=True):
            if 'ai_estimate' in st.session_state:
                del st.session_state.ai_estimate
            st.rerun()