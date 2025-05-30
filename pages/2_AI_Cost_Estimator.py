# Page configuration - MUST BE FIRST
import streamlit as st
st.set_page_config(
    page_title="AI Cost Estimator - KAN-BUD",
    page_icon="🤖",
    layout="wide"
)

import json
from utils.translations import t, init_language, get_current_language
from utils.shared_header import render_shared_header, render_back_to_home

# Initialize language system
init_language()

# Initialize session state
if 'employee_logged_in' not in st.session_state:
    st.session_state.employee_logged_in = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# Render shared header without login button
render_shared_header(show_login=False)

def generate_cost_estimate(config, ai_model):
    """Generate AI-powered cost estimate using actual AI services"""
    from utils.ai_services import estimate_cost_with_ai
    
    try:
        # Call the actual AI service with the configuration
        ai_estimate = estimate_cost_with_ai(config, ai_model)
        return ai_estimate
    except Exception as e:
        # Fallback to basic estimate if AI fails
        current_lang = get_current_language()
        
        base_costs = {
            '20ft Standard': 8000,
            '40ft Standard': 12000,
            '40ft High Cube': 14000,
            '20ft Refrigerated': 15000
        }
        
        container_cost = base_costs.get(config.get('container_type', '20ft Standard'), 8000)
        
        # Add costs based on modifications
        modifications_cost = 0
        modifications_cost += config.get('number_of_windows', 0) * 300
        if config.get('additional_doors', False):
            modifications_cost += 800
        
        # Finish level multiplier
        finish_multipliers = {
            'Basic': 1.0,
            'Standard': 1.2,
            'Premium': 1.5,
            'Luxury': 2.0
        }
        finish_multiplier = finish_multipliers.get(config.get('finish_level', 'Standard'), 1.2)
        
        total_cost = (container_cost + modifications_cost) * finish_multiplier
        
        error_msg = t('ai_service_error', current_lang) if 'ai_service_error' in t.__dict__ else "AI service temporarily unavailable"
        
        return f"""
## ⚠️ {error_msg}

{t('fallback_estimate_basic', current_lang) if 'fallback_estimate_basic' in t.__dict__ else 'Basic calculation fallback:'}

**{t('container_type', current_lang)}:** {config.get('container_type', 'N/A')}
**{t('base_cost', current_lang)}:** €{container_cost:,}
**{t('modifications', current_lang)}:** €{modifications_cost:,}
**{t('finish_level', current_lang)}:** {config.get('finish_level', 'N/A')} ({t('multiplier', current_lang)}: {finish_multiplier})

### **{t('total_cost', current_lang).upper()}: €{total_cost:,.0f}**

*{t('ai_retry_later', current_lang) if 'ai_retry_later' in t.__dict__ else 'Please try again later for AI analysis'}*

**{t('error_details', current_lang) if 'error_details' in t.__dict__ else 'Error'}: {str(e)}**
"""

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
    <div class="header-title">🤖 {t('ai_cost_estimation')}</div>
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
        # Translate container type
        container_type_key = config['container_type'].lower().replace(' ', '_').replace('ft', 'ft')
        if container_type_key == '20ft_standard':
            container_type_translated = t('container.types.20ft_standard')
        elif container_type_key == '40ft_standard':
            container_type_translated = t('container.types.40ft_standard')
        elif container_type_key == '40ft_high_cube':
            container_type_translated = t('container.types.40ft_high_cube')
        elif container_type_key == '20ft_refrigerated':
            container_type_translated = t('container.types.20ft_refrigerated')
        else:
            container_type_translated = config['container_type']

        # Translate main purpose
        purpose_key = config['main_purpose'].lower().replace(' ', '_')
        purpose_translated = t(f'container.use_cases.{purpose_key}')
        if purpose_translated == f'container.use_cases.{purpose_key}':
            purpose_translated = config['main_purpose']

        # Translate environment
        env_key = config['environment'].lower()
        env_translated = t(f'container.environment.{env_key}')
        if env_translated == f'container.environment.{env_key}':
            env_translated = config['environment']

        # Translate finish level
        finish_key = config['finish_level'].lower()
        finish_translated = t(f'container.finish_levels.{finish_key}')
        if finish_translated == f'container.finish_levels.{finish_key}':
            finish_translated = config['finish_level']

        st.write(f"**{t('container_type')}:** {container_type_translated}")
        st.write(f"**{t('purpose')}:** {purpose_translated}")
        st.write(f"**{t('environment')}:** {env_translated}")
        st.write(f"**{t('finish_level')}:** {finish_translated}")

    with col2:
        # Translate flooring
        flooring_key = config['flooring'].lower().replace(' ', '_')
        flooring_translated = t(f'container.flooring.{flooring_key}')
        if flooring_translated == f'container.flooring.{flooring_key}':
            flooring_translated = config['flooring']

        # Translate climate zone
        climate_key = config['climate_zone'].lower().replace(' ', '_')
        climate_translated = t(f'container.climate_zones.{climate_key}')
        if climate_translated == f'container.climate_zones.{climate_key}':
            climate_translated = config['climate_zone']

        st.write(f"**{t('flooring')}:** {flooring_translated}")
        st.write(f"**{t('climate_zone')}:** {climate_translated}")
        st.write(f"**{t('windows')}:** {config['number_of_windows']}")
        st.write(f"**{t('additional_doors')}:** {t('yes') if config['additional_doors'] else t('no')}")

    st.markdown("---")

    # User input section for additional details
    st.markdown(f"### 💬 {t('additional_project_details')}:")
    
    user_comment = st.text_area(
        t('project_specific_requirements'),
        placeholder=t('project_comment_placeholder'),
        height=120,
        help=t('project_comment_help'),
        key="user_project_comment"
    )
    
    # Specific requirement checkboxes
    st.markdown(f"**{t('specific_considerations')}:**")
    col1, col2 = st.columns(2)
    
    with col1:
        special_location = st.checkbox(t('special_location_requirements'), key="special_location")
        urgent_timeline = st.checkbox(t('urgent_timeline_needed'), key="urgent_timeline")
        custom_modifications = st.checkbox(t('custom_modifications_needed'), key="custom_mods")
    
    with col2:
        sustainability_focus = st.checkbox(t('sustainability_priority'), key="sustainability")
        budget_constraints = st.checkbox(t('budget_constraints'), key="budget_limit")
        regulatory_concerns = st.checkbox(t('regulatory_compliance_focus'), key="regulatory")

    st.markdown("---")

    # Check if user is employee to show AI model selection
    if st.session_state.get('employee_logged_in', False):
        # AI model selection for employees only
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
    else:
        # For customers, use default AI model without showing selection
        ai_model = t('auto_select_best')

    # Generate estimate button
    if st.button(f"🚀 {t('generate_ai_estimate')}", use_container_width=True, type="primary"):
        with st.spinner(t('ai.messages.generating')):
            try:
                # Prepare enhanced config with user input
                enhanced_config = config.copy()
                enhanced_config['user_comment'] = user_comment
                enhanced_config['special_requirements'] = {
                    'special_location': special_location,
                    'urgent_timeline': urgent_timeline,
                    'custom_modifications': custom_modifications,
                    'sustainability_focus': sustainability_focus,
                    'budget_constraints': budget_constraints,
                    'regulatory_concerns': regulatory_concerns
                }
                
                # Generate cost estimate
                estimate = generate_cost_estimate(enhanced_config, ai_model)

                if estimate:
                    st.session_state.ai_estimate = estimate
                    st.success(t('ai.messages.estimate_generated'))

                    # Display estimate
                    st.markdown(f"### 🤖 {t('ai_cost_estimate')}:")
                    st.markdown(estimate)

                    # Legal disclaimer
                    st.warning(f"""
                    ⚠️ **{t('estimate_disclaimer_title')}**

                    {t('estimate_disclaimer_text')}
                    """)

                    # Call to action
                    st.info(f"""
                    📧 **{t('get_precise_quote')}**

                    {t('contact_for_quote')}
                    """)

                    if st.button(f"📧 {t('send_inquiry_cta')}", key="inquiry_cta", use_container_width=True, type="primary"):
                        # Store the current estimate and config for inquiry
                        st.session_state.inquiry_source = "ai_estimator"
                        st.session_state.inquiry_estimate = estimate
                        st.session_state.inquiry_config = config
                        st.session_state.ai_estimate = estimate  # Preserve the estimate
                        st.switch_page("pages/8_Send_Inquiry.py")

                    # Save estimate
                    if st.button(f"💾 {t('save_estimate')}", key="save_estimate"):
                        st.success(t('estimate_saved'))
                else:
                    st.error(t('failed_generate_estimate'))

            except Exception as e:
                st.error(f"{t('error_generating_estimate')}: {str(e)}")