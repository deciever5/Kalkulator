
"""
Customer Inquiry Form - Available for all users
Allows customers to send inquiries after getting estimates
"""

import streamlit as st
from datetime import datetime
from utils.translations import t, render_language_selector
from utils.global_language import get_current_language
from utils.simple_storage import SimpleStorageManager

st.set_page_config(page_title="Send Inquiry", page_icon="📧", layout="wide")

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Language selector - using the same dropdown style as other pages
render_language_selector()

st.title(f"📧 {t('send_inquiry.title')}")
st.markdown(f"*{t('send_inquiry.description')}*")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button(t('ui.back_to_home'), key="home_nav", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button(t('ui.go_to_configurator'), key="config_nav", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")

# Important disclaimer
st.warning(f"""
⚠️ **{t('send_inquiry.disclaimer_title')}**

{t('send_inquiry.disclaimer_text')}
""")

# Check if there's a saved configuration or estimate
has_config = 'container_config' in st.session_state and st.session_state.container_config
has_estimate = 'ai_estimate' in st.session_state

if has_config or has_estimate:
    st.success(f"✅ {t('send_inquiry.config_detected')}")
    
    with st.expander(f"📋 {t('send_inquiry.current_config')}", expanded=False):
        if has_config:
            config = st.session_state.container_config
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**{t('form.labels.container_type')}:** {config.get('container_type', 'N/A')}")
                st.write(f"**{t('form.labels.main_purpose')}:** {config.get('main_purpose', 'N/A')}")
                st.write(f"**{t('form.labels.environment')}:** {config.get('environment', 'N/A')}")
            
            with col2:
                st.write(f"**{t('form.labels.finish_level')}:** {config.get('finish_level', 'N/A')}")
                st.write(f"**{t('form.labels.climate_zone')}:** {config.get('climate_zone', 'N/A')}")
                st.write(f"**{t('form.labels.number_of_windows')}:** {config.get('num_windows', 'N/A')}")
        
        if has_estimate:
            st.markdown(f"### {t('saved_ai_estimate')}:")
            st.write(st.session_state.ai_estimate)

st.markdown("---")

# Customer Information Form
st.markdown(f"### 👤 {t('send_inquiry.customer_info')}")

col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input(f"{t('send_inquiry.full_name')} *", key="cust_name")
    company_name = st.text_input(t('send_inquiry.company_name'), key="comp_name")
    email = st.text_input(f"{t('send_inquiry.email')} *", key="cust_email")

with col2:
    phone = st.text_input(f"{t('send_inquiry.phone')} *", key="cust_phone")
    city = st.text_input(t('send_inquiry.city'), key="cust_city")
    country = st.text_input(t('send_inquiry.country'), key="cust_country", value="Polska")

# Project Information
st.markdown(f"### 🏗️ {t('send_inquiry.project_details')}")

project_name = st.text_input(t('send_inquiry.project_name'))
project_location = st.text_input(t('send_inquiry.project_location'))
project_description = st.text_area(f"{t('send_inquiry.additional_message')} *", height=100)

# Timeline and Budget
col1, col2 = st.columns(2)
with col1:
    timeline = st.selectbox(
        t('send_inquiry.expected_timeline'),
        [
            t('send_inquiry.timeline.asap'),
            t('send_inquiry.timeline.within_month'),
            t('send_inquiry.timeline.within_quarter'), 
            t('send_inquiry.timeline.within_half_year'),
            t('send_inquiry.timeline.planning_phase')
        ]
    )

with col2:
    budget_range = st.selectbox(
        f"{t('send_inquiry.budget_range')} (EUR)",
        [
            t('send_inquiry.budget.not_specified'),
            t('send_inquiry.budget.up_to_50k'),
            t('send_inquiry.budget.50k_100k'),
            t('send_inquiry.budget.100k_200k'),
            t('send_inquiry.budget.over_200k')
        ]
    )

# Inquiry Type
st.markdown(f"### 📋 {t('send_inquiry.additional_requirements')}")

inquiry_type = st.selectbox(
    t('send_inquiry.inquiry_type'),
    [
        t('send_inquiry.types.detailed_quote'),
        t('send_inquiry.types.technical_consultation'),
        t('send_inquiry.types.site_visit'),
        t('send_inquiry.types.drawing_analysis'),
        t('send_inquiry.types.general_info')
    ]
)

additional_requirements = st.text_area(
    t('send_inquiry.special_requirements'), 
    placeholder=t('send_inquiry.special_requirements_placeholder'),
    height=80
)

additional_message = st.text_area(
    t('send_inquiry.additional_message'), 
    placeholder=t('send_inquiry.additional_message_placeholder'),
    height=80
)

# File Upload
st.markdown(f"### 📎 {t('send_inquiry.attachments')}")
uploaded_files = st.file_uploader(
    t('send_inquiry.upload_files'),
    accept_multiple_files=True,
    type=['pdf', 'dwg', 'jpg', 'jpeg', 'png', 'doc', 'docx'],
    help=t('send_inquiry.file_formats_help')
)

if uploaded_files:
    st.info(f"{t('send_inquiry.files_attached')}: {len(uploaded_files)}")

# Contact preferences
st.markdown(f"### 📞 {t('send_inquiry.contact_preferences')}")
col1, col2 = st.columns(2)

with col1:
    contact_method = st.selectbox(
        t('send_inquiry.preferred_contact'),
        [
            t('send_inquiry.contact.email'),
            t('send_inquiry.contact.phone'),
            t('send_inquiry.contact.both')
        ]
    )

with col2:
    contact_time = st.selectbox(
        t('send_inquiry.best_time'),
        [
            t('send_inquiry.time.morning'),
            t('send_inquiry.time.afternoon'),
            t('send_inquiry.time.evening'),
            t('send_inquiry.time.anytime')
        ]
    )

# RODO/GDPR Consent
st.markdown(f"### 🔒 {t('send_inquiry.privacy_section')}")

with st.expander(t('send_inquiry.data_protection_info')):
    st.markdown(f"""
    **{t('send_inquiry.data_retention')}**
    
    {t('send_inquiry.why_professional_inquiry')}
    
    {t('send_inquiry.preparation_tips')}
    """)

gdpr_consent = st.checkbox(
    f"{t('send_inquiry.privacy_consent')} *",
    key="gdpr_consent"
)

marketing_consent = st.checkbox(
    t('send_inquiry.marketing_consent'),
    key="marketing_consent"
)

# Submit button
st.markdown("---")

if st.button(f"📧 {t('send_inquiry.submit_inquiry')}", type="primary", use_container_width=True):
    # Validation
    if not customer_name or not email or not phone or not project_description or not gdpr_consent:
        st.error(t('send_inquiry.fill_required_fields'))
    else:
        # Prepare inquiry data
        inquiry_data = {
            'timestamp': datetime.now().isoformat(),
            'customer_name': customer_name,
            'company_name': company_name,
            'email': email,
            'phone': phone,
            'city': city,
            'country': country,
            'project_name': project_name,
            'project_location': project_location,
            'project_description': project_description,
            'inquiry_type': inquiry_type,
            'additional_requirements': additional_requirements,
            'additional_message': additional_message,
            'timeline': timeline,
            'budget_range': budget_range,
            'contact_method': contact_method,
            'contact_time': contact_time,
            'gdpr_consent': gdpr_consent,
            'marketing_consent': marketing_consent,
            'container_config': st.session_state.get('container_config', {}),
            'ai_estimate': st.session_state.get('ai_estimate', ''),
            'files_uploaded': len(uploaded_files) if uploaded_files else 0,
            'language': get_current_language()
        }
        
        # Save to storage
        try:
            storage = SimpleStorageManager()
            storage.save_inquiry(inquiry_data)
            
            st.success(f"""
            ✅ **{t('send_inquiry.success_title')}**
            
            {t('send_inquiry.success_message')}
            
            ### {t('send_inquiry.next_steps')}
            1. {t('send_inquiry.step_1')}
            2. {t('send_inquiry.step_2')}
            3. {t('send_inquiry.step_3')}
            """)
            
            # Clear the form
            for key in st.session_state.keys():
                if key.startswith(('cust_', 'comp_', 'gdpr_', 'marketing_')):
                    del st.session_state[key]
            
            if st.button(t('send_inquiry.new_inquiry')):
                st.rerun()
            
        except Exception as e:
            st.error(f"{t('send_inquiry.error')}: {str(e)}")

# Contact information
st.markdown("---")
st.markdown(f"### 📞 {t('send_inquiry.contact_info')}")
st.markdown(f"""
**KAN-BUD**  
📍 {t('address')}: Kąkolewo, Polska  
📞 {t('phone')}: +48 XXX XXX XXX  
✉️ {t('email')}: info@kan-bud.pl  
🕒 {t('working_hours')}: {t('mon_fri')}
""")

# Tips section
st.markdown("---")
st.info(f"""
💡 **{t('send_inquiry.why_professional_inquiry')}**

• {t('ai_historical_data')}
• {t('european_climate_standards')}
• {t('transparent_calculations')}
• {t('after_sales_support')}
""")
