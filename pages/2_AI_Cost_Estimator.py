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
    from utils.container_loading_spinner import ContainerLoadingSpinner
    
    # Initialize container-themed loading spinner
    loader = ContainerLoadingSpinner()
    
    # Show container-themed loading animation during AI processing
    with st.container():
        st.markdown(f"### 🤖 {t('generating_ai_estimate')}")
        
        # Show progress animation while AI processes
        loader.show_interactive_progress(
            total_steps=5,
            current_step=1, 
            message=t('ai_analyzing_requirements')
        )
        
        # Brief pause for animation effect
        import time
        time.sleep(1)

    try:
        # Show progressive loading steps
        loader.show_interactive_progress(2, 1, t('ai_calculating_costs'))
        time.sleep(0.5)
        
        loader.show_interactive_progress(3, 2, t('ai_optimizing_design'))
        time.sleep(0.5)
        
        # Call the actual AI service with the configuration
        ai_estimate = estimate_cost_with_ai(config, ai_model)
        
        # Show completion
        loader.show_interactive_progress(5, 5, t('ai_finalizing_estimate'))
        time.sleep(0.3)
        loader.success_animation("Oszacowanie AI zostało wygenerowane!")
        
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
        st.write(f"**{t('container_type')}:** {config.get('container_type', 'N/A')}")
        st.write(f"**Materiał konstrukcyjny:** {config.get('construction_material', 'N/A')}")
        st.write(f"**Izolacja:** {config.get('insulation', 'N/A')}")
        st.write(f"**{t('purpose')}:** {config.get('main_purpose', 'N/A')}")
        st.write(f"**{t('environment')}:** {config.get('environment', 'N/A')}")
        st.write(f"**{t('finish_level')}:** {config.get('finish_level', 'N/A')}")
        st.write(f"**{t('flooring')}:** {config.get('flooring', 'N/A')}")
        st.write(f"**{t('climate_zone')}:** {config.get('climate_zone', 'N/A')}")

    with col2:
        st.write(f"**Okna:** {config.get('num_windows', 'N/A')}")
        if config.get('window_types'):
            st.write(f"**Typ okien:** {', '.join(config.get('window_types', []))}")
        st.write(f"**Oświetlenie:** {config.get('lighting', 'N/A')}")
        st.write(f"**Wentylacja:** {config.get('ventilation', 'N/A')}")
        st.write(f"**Modyfikacje dachu:** {config.get('roof_modifications', 'N/A')}")
        st.write(f"**{t('electrical_system')}:** {config.get('electrical_system', 'N/A')}")
        st.write(f"**{t('plumbing_system')}:** {config.get('plumbing_system', 'N/A')}")
        st.write(f"**{t('hvac_system')}:** {config.get('hvac_system', 'N/A')}")

    # Show additional systems and modifications
    st.markdown("### Dodatkowe systemy i modyfikacje:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Układ wewnętrzny:** {config.get('interior_layout', 'N/A')}")
        st.write(f"**Zabezpieczenia:** {config.get('security_systems', 'N/A')}")
        st.write(f"**Okładzina zewnętrzna:** {config.get('exterior_cladding', 'N/A')}")
        st.write(f"**Dodatkowe otwory:** {config.get('additional_openings', 'N/A')}")
        
    with col2:
        st.write(f"**Systemy przeciwpożarowe:** {config.get('fire_systems', 'N/A')}")
        st.write(f"**Dostępność:** {config.get('accessibility', 'N/A')}")
        st.write(f"**Malowanie:** {config.get('paint_finish', 'N/A')}")
        st.write(f"**Strefa dostawy:** {config.get('delivery_zone', 'N/A')}")

    # Show special comments
    if config.get('system_comments') or config.get('advanced_comments') or config.get('general_comments'):
        st.markdown("### Dodatkowe wymagania klienta:")
        if config.get('system_comments'):
            st.write(f"**Systemy:** {config.get('system_comments')}")
        if config.get('advanced_comments'):
            st.write(f"**Modyfikacje:** {config.get('advanced_comments')}")
        if config.get('general_comments'):
            st.write(f"**Ogólne:** {config.get('general_comments')}")

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
                # Prepare enhanced config with user input and comprehensive configuration
                enhanced_config = config.copy()
                enhanced_config['user_comment'] = user_comment
                
                # Add all comprehensive configuration details for AI analysis
                comprehensive_details = []
                if config.get('construction_material'):
                    comprehensive_details.append(f"Materiał konstrukcyjny: {config['construction_material']}")
                if config.get('insulation'):
                    comprehensive_details.append(f"Izolacja: {config['insulation']}")
                if config.get('lighting'):
                    comprehensive_details.append(f"Oświetlenie: {config['lighting']}")
                if config.get('ventilation'):
                    comprehensive_details.append(f"Wentylacja: {config['ventilation']}")
                if config.get('roof_modifications'):
                    comprehensive_details.append(f"Modyfikacje dachu: {config['roof_modifications']}")
                if config.get('interior_layout'):
                    comprehensive_details.append(f"Układ wewnętrzny: {config['interior_layout']}")
                if config.get('security_systems'):
                    comprehensive_details.append(f"Zabezpieczenia: {config['security_systems']}")
                if config.get('exterior_cladding'):
                    comprehensive_details.append(f"Okładzina zewnętrzna: {config['exterior_cladding']}")
                if config.get('additional_openings'):
                    comprehensive_details.append(f"Dodatkowe otwory: {config['additional_openings']}")
                if config.get('fire_systems'):
                    comprehensive_details.append(f"Systemy przeciwpożarowe: {config['fire_systems']}")
                if config.get('accessibility'):
                    comprehensive_details.append(f"Dostępność: {config['accessibility']}")
                if config.get('delivery_zone'):
                    comprehensive_details.append(f"Strefa dostawy: {config['delivery_zone']}")
                if config.get('transport_type'):
                    comprehensive_details.append(f"Transport: {config['transport_type']}")
                if config.get('installation'):
                    comprehensive_details.append(f"Montaż: {config['installation']}")
                if config.get('office_equipment'):
                    comprehensive_details.append(f"Wyposażenie biurowe: {config['office_equipment']}")
                if config.get('appliances'):
                    comprehensive_details.append(f"Sprzęt AGD: {config['appliances']}")
                if config.get('it_systems'):
                    comprehensive_details.append(f"Systemy IT: {config['it_systems']}")
                
                # Combine all comments and requirements
                all_comments = []
                if config.get('system_comments'):
                    all_comments.append(f"Wymagania systemów: {config['system_comments']}")
                if config.get('advanced_comments'):
                    all_comments.append(f"Wymagania modyfikacji: {config['advanced_comments']}")
                if config.get('general_comments'):
                    all_comments.append(f"Wymagania ogólne: {config['general_comments']}")
                if user_comment:
                    all_comments.append(f"Dodatkowe wymagania: {user_comment}")
                
                # Create detailed requirements string for AI
                enhanced_config['comprehensive_specifications'] = "; ".join(comprehensive_details)
                enhanced_config['all_requirements'] = "; ".join(all_comments)
                
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