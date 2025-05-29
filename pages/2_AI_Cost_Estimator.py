import streamlit as st
import pandas as pd
from utils.calculations import calculate_container_cost
from utils.ai_services import OpenAIService, AnthropicService
from utils.translations import t, get_current_language, render_language_selector

# Page configuration
st.set_page_config(
    page_title="AI Cost Estimator - KAN-BUD",
    page_icon="🤖",
    layout="wide"
)

# Language selector at the top
render_language_selector()

import streamlit as st
import json
from utils.ai_services import estimate_cost_with_ai
from utils.translations import t, get_current_language

# Page configuration
st.set_page_config(
    page_title="AI Cost Estimator - KAN-BUD",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
.header-title {
    color: white;
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}
.header-subtitle {
    color: #e8f4f8;
    font-size: 1.2rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="main-header">
    <div class="header-title">🤖 {t('nav.ai_cost_estimation')}</div>
    <div class="header-subtitle">AI-powered container modification cost estimation</div>
</div>
""", unsafe_allow_html=True)

# Navigation
col1, col2 = st.columns(2)
with col1:
    if st.button(t('ui.back_to_home'), key="home_nav", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button(t('ui.go_to_configurator'), key="config_nav", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")

# Check if configuration exists
if 'container_config' not in st.session_state:
    st.warning("No container configuration found. Please configure your container first.")
    if st.button("🔧 Go to Configurator", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")
else:
    # Display configuration
    config = st.session_state.container_config

    st.markdown("### Current Configuration:")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Container Type:** {config['container_type']}")
        st.write(f"**Purpose:** {config['main_purpose']}")
        st.write(f"**Environment:** {config['environment']}")
        st.write(f"**Finish Level:** {config['finish_level']}")

    with col2:
        st.write(f"**Flooring:** {config['flooring']}")
        st.write(f"**Climate Zone:** {config['climate_zone']}")
        st.write(f"**Windows:** {config['number_of_windows']}")
        st.write(f"**Additional Doors:** {'Yes' if config['additional_doors'] else 'No'}")

    st.markdown("---")

    # AI model selection
    st.markdown("### AI Model Selection:")
    ai_model = st.selectbox(
        "Choose AI Model:",
        [
            "Auto-Select Best",
            "Groq Llama-3.1-70B",
            "Groq Llama-3.1-8B",
            "Groq Mixtral-8x7B"
        ],
        key="ai_model_select"
    )

    # Generate estimate button
    if st.button("🚀 Generate AI Cost Estimate", use_container_width=True, type="primary"):
        with st.spinner(t('ai.messages.generating')):
            try:
                # Call AI service
                estimate = estimate_cost_with_ai(config, ai_model)

                if estimate:
                    st.session_state.ai_estimate = estimate
                    st.success(t('ai.messages.estimate_generated'))

                    # Display estimate
                    st.markdown("### 🤖 AI Cost Estimate:")
                    st.markdown(estimate)

                    # Save estimate
                    if st.button("💾 Save Estimate", key="save_estimate"):
                        st.success("Estimate saved!")
                else:
                    st.error("Failed to generate estimate. Please try again.")

            except Exception as e:
                st.error(f"Error generating estimate: {str(e)}")

    # Display saved estimate if available
    if 'ai_estimate' in st.session_state:
        st.markdown("### 📋 Saved AI Estimate:")
        st.markdown(st.session_state.ai_estimate)