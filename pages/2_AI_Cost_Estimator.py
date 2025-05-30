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
render_shared_header(show_login=False, current_page="AI_Cost_Estimator")

def generate_cost_estimate(config, ai_model):
    """Generate AI-powered cost estimate with animated loading"""
    from utils.ai_services import estimate_cost_with_ai
    from utils.animations import show_calculation_animation, create_animated_counter

    # Show animated calculation process
    calculation_container = st.container()
    with calculation_container:
        show_calculation_animation(config)

    try:
        # Call the actual AI service with the configuration
        ai_estimate = estimate_cost_with_ai(config, ai_model)
        return ai_estimate
    except Exception as e:
        # Fallback to configurator pricing when AI fails
        from utils.calculations import StructuralCalculations
        calc = StructuralCalculations()

        try:
            # Use the base cost calculation method that exists
            cost_breakdown = calc.calculate_base_costs(config)
            total_cost = cost_breakdown.get('subtotal', 0)

            return f"""
## ⚠️ {t('ai_service_error')}

{t('fallback_estimate_basic')}

**{t('container_type')}:** {config.get('container_type', 'N/A')}
**{t('base_cost')}:** €{cost_breakdown.get('base_container', 0):,.2f}
**{t('modifications')}:** €{cost_breakdown.get('modifications', 0):,.2f}
**{t('labor_costs_30')}:** €{cost_breakdown.get('labor', 0):,.2f}

### **{t('total_cost').upper()}: €{total_cost:,.2f}**

*{t('ai_retry_later')}*

**{t('basic_estimate_note')}**

---

### {t('standard_recommendations')}
- {t('plan_standard_delivery')}
- {t('consider_building_codes')}
- {t('budget_site_preparation')}
- {t('review_electrical_plumbing')}

### {t('standard_risk_factors')}
- {t('weather_delays')}
- {t('permit_timeline_variations')}
- {t('site_access_limitations')}
- {t('material_price_fluctuations')}
"""
        except Exception as calc_error:
            # Ultimate fallback if even basic calculation fails
            return f"""
## ⚠️ {t('ai_service_error')}

{t('basic_calculation_ai_unavailable')}

**{t('container_type')}:** {config.get('container_type', 'N/A')}
**{t('error_details')}:** {str(e)}
**{t('error_details')} (calc):** {str(calc_error)}

{t('basic_estimate_note')}
"""

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

        # Show all advanced modifications from the enhanced configurator
        st.write(f"**{t('electrical_system')}:** {config.get('electrical_system', 'N/A')}")
        st.write(f"**{t('plumbing_system')}:** {config.get('plumbing_system', 'N/A')}")
        st.write(f"**{t('hvac_system')}:** {config.get('hvac_system', 'N/A')}")

        if config.get('air_intakes'):
            st.write(f"**{t('air_intakes_label')}:** {config.get('air_intakes', 'N/A')}")
        if config.get('roof_modifications'):
            st.write(f"**{t('roof_modifications_label')}:** {config.get('roof_modifications', 'N/A')}")
        if config.get('security_features'):
            st.write(f"**{t('security_features')}:** {config.get('security_features', 'N/A')}")
        if config.get('paint_finish'):
            st.write(f"**{t('paint_finish')}:** {config.get('paint_finish', 'N/A')}")

        # Show detailed modifications
        modifications = config.get('modifications', {})
        if modifications:
            st.markdown("**Modifications:**")
            mod_count = 0
            for key, value in modifications.items():
                if value:
                    if isinstance(value, bool):
                        st.write(f"• {key.replace('_', ' ').title()}")
                        mod_count += 1
                    elif isinstance(value, (int, float)) and value > 0:
                        st.write(f"• {key.replace('_', ' ').title()}: {value}")
                        mod_count += 1
            if mod_count == 0:
                st.write("• No additional modifications")

        # Show cost-impacting factors
        if config.get('user_comment', '').strip():
            st.markdown(f"**User Requirements:** {config['user_comment'][:100]}{'...' if len(config['user_comment']) > 100 else ''}")

        special_reqs = config.get('special_requirements', {})
        if any(special_reqs.values()):
            active_reqs = [key.replace('_', ' ').title() for key, value in special_reqs.items() if value]
            st.markdown(f"**Special Requirements:** {', '.join(active_reqs)}")

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

    # Check if user is employee to show AI model selection and pricing rates
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

        # Show pricing rates for employees
        with st.expander("💰 View Current Pricing Rates"):
            from utils.calculations import StructuralCalculations
            calc = StructuralCalculations()
            rates = calc.get_all_pricing_rates()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Labor Rates:**")
                for role, rate in rates["labor_rates"].items():
                    st.write(f"• {role.replace('_', ' ').title()}: {rate}")

                st.markdown("**Markup Rates:**")
                for rate_type, rate in rates["markup_rates"].items():
                    st.write(f"• {rate_type.replace('_', ' ').title()}: {rate}")

            with col2:
                st.markdown("**Container Base Costs:**")
                for container, cost in rates["container_base_costs"].items():
                    st.write(f"• {container.replace('_', ' ').title()}: {cost}")

                st.markdown("**Modification Costs:**")
                for mod, cost in rates["modification_costs"].items():
                    st.write(f"• {mod.replace('_', ' ').title()}: {cost}")

            st.markdown("**Tax Rate:** " + rates["tax_rate"])

            st.markdown("**Calculation Method:**")
            for step, description in rates["calculation_method"].items():
                st.write(f"{step.replace('_', ' ').title()}: {description}")
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