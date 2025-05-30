import streamlit as st
import json
from utils.translations import t, init_language
from utils.shared_header import render_shared_header, render_back_to_home

# Initialize language system
init_language()

# Initialize session state
if 'employee_logged_in' not in st.session_state:
    st.session_state.employee_logged_in = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# Render shared header with language selector and login
render_shared_header()

def generate_cost_estimate(config, ai_model):
    """Generate a realistic cost estimate based on configuration"""
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
    
    current_lang = get_current_language()
    
    if current_lang == 'pl':
        return f"""
## Szacunek kosztów AI

**Typ kontenera:** {config.get('container_type', 'N/A')}
**Koszt bazowy:** {container_cost:,} EUR
**Modyfikacje:** {modifications_cost:,} EUR
**Poziom wykończenia:** {config.get('finish_level', 'N/A')} (mnożnik: {finish_multiplier})

### **CAŁKOWITY SZACOWANY KOSZT: {total_cost:,.0f} EUR**

*Cena zawiera: projekt, materiały, wykonanie, transport (do 100km)*
*Nie zawiera: pozwoleń, przyłączy, fundamentów*
"""
    else:
        return f"""
## AI Cost Estimate

**Container Type:** {config.get('container_type', 'N/A')}
**Base Cost:** {container_cost:,} EUR
**Modifications:** {modifications_cost:,} EUR
**Finish Level:** {config.get('finish_level', 'N/A')} (multiplier: {finish_multiplier})

### **TOTAL ESTIMATED COST: {total_cost:,.0f} EUR**

*Price includes: design, materials, execution, transport (up to 100km)*
*Does not include: permits, utilities, foundations*
"""

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
                # Generate cost estimate
                estimate = generate_cost_estimate(config, ai_model)

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