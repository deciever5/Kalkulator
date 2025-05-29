import streamlit as st
import json
from utils.ai_services import estimate_cost_with_ai
from utils.translations import t, render_language_selector

# Page configuration
st.set_page_config(
    page_title="AI Cost Estimator - KAN-BUD",
    page_icon="🤖",
    layout="wide"
)

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Language selector
render_language_selector()

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
    <div class="header-subtitle">{t('ai_powered_estimation')}</div>
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
    st.warning(t('no_configuration_found'))
    if st.button(f"🔧 {t('ui.go_to_configurator')}", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")
else:
    # Display configuration
    config = st.session_state.container_config

    st.markdown(f"### {t('current_configuration')}:")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**{t('container_type')}:** {config['container_type']}")
        st.write(f"**{t('purpose')}:** {config['main_purpose']}")
        st.write(f"**{t('environment')}:** {config['environment']}")
        st.write(f"**{t('finish_level')}:** {config['finish_level']}")

    with col2:
        st.write(f"**{t('flooring')}:** {config['flooring']}")
        st.write(f"**{t('climate_zone')}:** {config['climate_zone']}")
        st.write(f"**{t('windows')}:** {config['number_of_windows']}")
        st.write(f"**{t('additional_doors')}:** {t('yes') if config['additional_doors'] else t('no')}")

    st.markdown("---")

    # AI model selection
    st.markdown(f"### {t('ai_model_selection')}:")
    ai_model = st.selectbox(
        t('choose_ai_model'),
        [
            t('auto_select_best'),
            "Groq Llama-3.1-70B",
            "Groq Llama-3.1-8B", 
            "Groq Mixtral-8x7B"
        ],
        key="ai_model_select"
    )

    # Generate estimate button
    if st.button(f"🚀 {t('generate_ai_estimate')}", use_container_width=True, type="primary"):
        with st.spinner(t('ai.messages.generating')):
            try:
                # Call AI service
                estimate = estimate_cost_with_ai(config, ai_model)

                if estimate:
                    st.session_state.ai_estimate = estimate
                    st.success(t('ai.messages.estimate_generated'))

                    # Display estimate
                    st.markdown(f"### 🤖 {t('ai_cost_estimate')}:")
                    st.markdown(estimate)

                    # Save estimate
                    if st.button(f"💾 {t('save_estimate')}", key="save_estimate"):
                        st.success(t('estimate_saved'))
                else:
                    st.error(t('failed_generate_estimate'))

            except Exception as e:
                st.error(f"{t('error_generating_estimate')}: {str(e)}")

    # Display saved estimate if available
    if 'ai_estimate' in st.session_state:
        st.markdown(f"### 📋 {t('saved_ai_estimate')}:")
        st.markdown(st.session_state.ai_estimate)