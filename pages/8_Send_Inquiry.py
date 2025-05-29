
"""
Customer Inquiry Form - Available for all users
Allows customers to send inquiries after getting estimates
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.translations import t, render_language_selector
from utils.simple_storage import SimpleStorageManager

st.set_page_config(page_title="Send Inquiry", page_icon="📧", layout="wide")

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Language selector
render_language_selector()

st.title(f"📧 {t('nav.send_inquiry')}")
st.markdown(f"*{t('send_inquiry.description')}*")

# Important disclaimer
st.warning(f"""
⚠️ **{t('send_inquiry.disclaimer_title')}**

{t('send_inquiry.disclaimer_text')}
""")

# Check if there's a saved configuration or estimate
has_config = 'container_config' in st.session_state and st.session_state.container_config
has_estimate = 'ai_estimate' in st.session_state
has_inquiry_data = 'inquiry_config' in st.session_state

# Use inquiry data if available (from AI estimator or other sources)
config_to_use = st.session_state.get('inquiry_config', st.session_state.get('container_config', {}))
estimate_to_use = st.session_state.get('inquiry_estimate', st.session_state.get('ai_estimate', ''))

if has_config or has_estimate or has_inquiry_data:
    st.success(f"✅ {t('send_inquiry.config_detected')}")
    
    # Show summary of current configuration
    with st.expander(f"📋 {t('send_inquiry.current_config')}", expanded=True):
        if config_to_use:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**{t('form.labels.container_type')}:** {config_to_use.get('container_type', 'N/A')}")
                st.write(f"**{t('form.labels.main_purpose')}:** {config_to_use.get('main_purpose', 'N/A')}")
                st.write(f"**{t('form.labels.environment')}:** {config_to_use.get('environment', 'N/A')}")
            
            with col2:
                st.write(f"**{t('form.labels.finish_level')}:** {config_to_use.get('finish_level', 'N/A')}")
                st.write(f"**{t('form.labels.delivery_zone')}:** {config_to_use.get('delivery_zone', 'N/A')}")
                
                if 'cost_breakdown' in st.session_state:
                    total_cost = st.session_state.cost_breakdown.get('total_cost', 0)
                    st.write(f"**{t('total_cost')}:** €{total_cost:,.2f}")
        
        # Show AI estimate if available
        if estimate_to_use:
            st.markdown("**AI Cost Estimate:**")
            with st.container():
                st.markdown(estimate_to_use[:300] + "..." if len(estimate_to_use) > 300 else estimate_to_use)

# Customer information form
st.subheader(f"👤 {t('send_inquiry.customer_info')}")

col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input(f"*{t('send_inquiry.full_name')}", placeholder="Jan Kowalski")
    customer_company = st.text_input(t('send_inquiry.company_name'), placeholder="Nazwa firmy (opcjonalnie)")
    customer_email = st.text_input(f"*{t('send_inquiry.email')}", placeholder="jan@example.com")

with col2:
    customer_phone = st.text_input(f"*{t('send_inquiry.phone')}", placeholder="+48 123 456 789")
    customer_city = st.text_input(f"*{t('send_inquiry.city')}", placeholder="Warszawa")
    customer_country = st.selectbox(
        f"*{t('send_inquiry.country')}",
        ["Polska", "Niemcy", "Czechy", "Słowacja", "Austria", "Holandia", "Belgia", "Inne"]
    )

# Project details
st.subheader(f"🏗️ {t('send_inquiry.project_details')}")

project_name = st.text_input(t('send_inquiry.project_name'), placeholder="Nazwa projektu")
project_location = st.text_input(f"*{t('send_inquiry.project_location')}", placeholder="Miasto, województwo")

# Timeline and budget
col1, col2 = st.columns(2)

with col1:
    expected_timeline = st.selectbox(
        f"*{t('send_inquiry.expected_timeline')}",
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
        t('send_inquiry.budget_range'),
        [
            t('send_inquiry.budget.not_specified'),
            "€20,000 - €50,000",
            "€50,000 - €100,000", 
            "€100,000 - €200,000",
            "€200,000+"
        ]
    )

# Additional requirements
st.subheader(f"📝 {t('send_inquiry.additional_requirements')}")

inquiry_type = st.selectbox(
    f"*{t('send_inquiry.inquiry_type')}",
    [
        t('send_inquiry.types.detailed_quote'),
        t('send_inquiry.types.technical_consultation'),
        t('send_inquiry.types.site_visit'),
        t('send_inquiry.types.drawing_analysis'),
        t('send_inquiry.types.general_info')
    ]
)

special_requirements = st.text_area(
    t('send_inquiry.special_requirements'),
    placeholder=t('send_inquiry.special_requirements_placeholder'),
    height=100
)

additional_message = st.text_area(
    t('send_inquiry.additional_message'),
    placeholder=t('send_inquiry.additional_message_placeholder'),
    height=120
)

# File attachments
st.subheader(f"📎 {t('send_inquiry.attachments')}")

uploaded_files = st.file_uploader(
    t('send_inquiry.upload_files'),
    type=['pdf', 'dwg', 'jpg', 'png', 'doc', 'docx'],
    accept_multiple_files=True,
    help=t('send_inquiry.file_formats_help')
)

# File size validation
files_valid = True
total_size = 0
max_total_size = 15 * 1024 * 1024  # 15MB in bytes

if uploaded_files:
    for file in uploaded_files:
        total_size += file.size
    
    if total_size > max_total_size:
        st.error(f"❌ Total file size ({total_size / (1024*1024):.1f} MB) exceeds 15MB limit. Please reduce file sizes or remove some files.")
        files_valid = False
    else:
        st.success(f"✅ {t('send_inquiry.files_attached')}: {len(uploaded_files)} files ({total_size / (1024*1024):.1f} MB / 15 MB)")
        for file in uploaded_files:
            st.write(f"📄 {file.name} ({file.size / (1024*1024):.1f} MB)")

# Contact preferences
st.subheader(f"📞 {t('send_inquiry.contact_preferences')}")

col1, col2 = st.columns(2)

with col1:
    preferred_contact = st.selectbox(
        t('send_inquiry.preferred_contact'),
        [
            t('send_inquiry.contact.email'),
            t('send_inquiry.contact.phone'),
            t('send_inquiry.contact.both')
        ]
    )

with col2:
    best_time = st.selectbox(
        t('send_inquiry.best_time'),
        [
            t('send_inquiry.time.morning'),
            t('send_inquiry.time.afternoon'),
            t('send_inquiry.time.evening'),
            t('send_inquiry.time.anytime')
        ]
    )

# Privacy consent
st.divider()

privacy_consent = st.checkbox(f"*{t('send_inquiry.privacy_consent')}")
marketing_consent = st.checkbox(t('send_inquiry.marketing_consent'))

# Submit button
st.divider()

# Validation
required_fields = [customer_name, customer_email, customer_phone, customer_city, project_location, expected_timeline, inquiry_type]
all_required_filled = all(field.strip() for field in required_fields) and privacy_consent and files_valid

if not all_required_filled:
    if not files_valid:
        st.warning(f"⚠️ Please fix file size issues before submitting.")
    else:
        st.warning(f"⚠️ {t('send_inquiry.fill_required_fields')}")

if st.button(f"📧 {t('send_inquiry.submit_inquiry')}", use_container_width=True, type="primary", disabled=not all_required_filled):
    # Prepare inquiry data
    inquiry_data = {
        'timestamp': datetime.now().isoformat(),
        'customer': {
            'name': customer_name,
            'company': customer_company,
            'email': customer_email,
            'phone': customer_phone,
            'city': customer_city,
            'country': customer_country
        },
        'project': {
            'name': project_name,
            'location': project_location,
            'timeline': expected_timeline,
            'budget_range': budget_range
        },
        'inquiry': {
            'type': inquiry_type,
            'special_requirements': special_requirements,
            'additional_message': additional_message,
            'files_count': len(uploaded_files) if uploaded_files else 0
        },
        'contact_preferences': {
            'preferred_method': preferred_contact,
            'best_time': best_time
        },
        'consents': {
            'privacy': privacy_consent,
            'marketing': marketing_consent
        }
    }
    
    # Add configuration data if available
    if config_to_use:
        inquiry_data['container_config'] = config_to_use
        
    if estimate_to_use:
        inquiry_data['ai_estimate'] = estimate_to_use
        
    if 'cost_breakdown' in st.session_state:
        inquiry_data['cost_breakdown'] = st.session_state.cost_breakdown
        
    # Add source information
    if 'inquiry_source' in st.session_state:
        inquiry_data['source'] = st.session_state.inquiry_source
    
    # Save inquiry (in real app, this would be sent via email/API)
    try:
        storage = SimpleStorageManager()
        storage.save_user_project(
            user_id=st.session_state.get('user_id', 'guest'),
            project_name=f"Inquiry: {customer_name} - {datetime.now().strftime('%Y-%m-%d')}",
            config=inquiry_data
        )
        
        st.success(f"""
        ✅ **{t('send_inquiry.success_title')}**
        
        {t('send_inquiry.success_message')}
        
        **{t('send_inquiry.next_steps')}:**
        1. {t('send_inquiry.step_1')}
        2. {t('send_inquiry.step_2')}
        3. {t('send_inquiry.step_3')}
        
        **{t('send_inquiry.contact_info')}:**
        📞 +48 XXX XXX XXX
        ✉️ biuro@kan-bud.pl
        🌐 www.kan-bud.pl
        """)
        
        st.balloons()
        
        # Clear inquiry transfer data
        if 'inquiry_source' in st.session_state:
            del st.session_state.inquiry_source
        if 'inquiry_config' in st.session_state:
            del st.session_state.inquiry_config
        if 'inquiry_estimate' in st.session_state:
            del st.session_state.inquiry_estimate
        
        # Option to create new inquiry
        if st.button(f"📝 {t('send_inquiry.new_inquiry')}", use_container_width=True):
            st.rerun()
            
    except Exception as e:
        st.error(f"{t('send_inquiry.error')}: {str(e)}")

# Additional information
st.divider()

st.info(f"""
📋 **{t('send_inquiry.why_detailed_inquiry')}**

{t('send_inquiry.detailed_inquiry_benefits')}

💡 **{t('send_inquiry.tips')}:**
• {t('send_inquiry.tip_1')}
• {t('send_inquiry.tip_2')}
• {t('send_inquiry.tip_3')}
""")
