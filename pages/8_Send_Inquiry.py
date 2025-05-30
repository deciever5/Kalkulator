
"""
Customer Inquiry Form - Enhanced template for professional inquiries
Includes contact data, project details, file uploads, and RODO compliance
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.complete_translations_fixed import get_translation
from utils.global_language import get_current_language, set_language
from utils.simple_storage import SimpleStorageManager

def t(key):
    return get_translation(key, get_current_language())

def render_language_selector():
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("🇵🇱 PL", key="lang_pl_inquiry", help="Polski", use_container_width=True):
            set_language('pl')
            st.rerun()
    with col2:
        if st.button("🇬🇧 EN", key="lang_en_inquiry", help="English", use_container_width=True):
            set_language('en')
            st.rerun()
    with col3:
        if st.button("🇩🇪 DE", key="lang_de_inquiry", help="Deutsch", use_container_width=True):
            set_language('de')
            st.rerun()
    with col4:
        if st.button("🇳🇱 NL", key="lang_nl_inquiry", help="Nederlands", use_container_width=True):
            set_language('nl')
            st.rerun()

st.set_page_config(page_title="Send Inquiry", page_icon="📧", layout="wide")

st.title(f"📧 {t('send_inquiry.title', 'Inquiry Form')}")
st.markdown(f"*{t('send_inquiry.description', 'Get a detailed quote tailored to your container project needs')}*")

# Important disclaimer
st.warning(f"""
⚠️ **{t('send_inquiry.disclaimer_title', 'Important Information')}**

{t('send_inquiry.disclaimer_text', 'This form is for sending inquiry requests for detailed quotes. Estimates from our calculator are not commercial offers under applicable law.')}
""")

# Check if there's a saved configuration or estimate
has_config = 'container_config' in st.session_state and st.session_state.container_config
has_estimate = 'ai_estimate' in st.session_state
has_inquiry_data = 'inquiry_config' in st.session_state

config_to_use = st.session_state.get('inquiry_config', st.session_state.get('container_config', {}))
estimate_to_use = st.session_state.get('inquiry_estimate', st.session_state.get('ai_estimate', ''))

if has_config or has_estimate or has_inquiry_data:
    st.success(f"✅ {t('send_inquiry.config_detected', 'Configuration detected from calculator')}")
    
    with st.expander(f"📋 {t('send_inquiry.current_config', 'Current Configuration')}", expanded=False):
        if config_to_use:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**{t('form.labels.container_type', 'Container Type')}:** {config_to_use.get('container_type', 'N/A')}")
                st.write(f"**{t('form.labels.main_purpose', 'Main Purpose')}:** {config_to_use.get('main_purpose', 'N/A')}")
                st.write(f"**{t('form.labels.environment', 'Environment')}:** {config_to_use.get('environment', 'N/A')}")
            
            with col2:
                st.write(f"**{t('form.labels.finish_level', 'Finish Level')}:** {config_to_use.get('finish_level', 'N/A')}")
                st.write(f"**{t('form.labels.delivery_zone', 'Delivery Zone')}:** {config_to_use.get('delivery_zone', 'N/A')}")
                
                if 'cost_breakdown' in st.session_state:
                    total_cost = st.session_state.cost_breakdown.get('total_cost', 0)
                    st.write(f"**{t('total_cost', 'Total Cost')}:** €{total_cost:,.2f}")

# SECTION 1: Customer Contact Information
st.header(f"👤 {t('send_inquiry.customer_info', 'Customer Contact Information')}")

col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input(
        f"*{t('send_inquiry.full_name', 'Full Name')}",
        placeholder="Jan Kowalski",
        help="Required field"
    )
    
    customer_company = st.text_input(
        t('send_inquiry.company_name', 'Company Name'),
        placeholder="Company Ltd. (optional)"
    )
    
    customer_email = st.text_input(
        f"*{t('send_inquiry.email', 'Email Address')}",
        placeholder="jan@company.com",
        help="Required for communication"
    )

with col2:
    customer_phone = st.text_input(
        f"*{t('send_inquiry.phone', 'Phone Number')}",
        placeholder="+48 123 456 789",
        help="Required for quick contact"
    )
    
    customer_city = st.text_input(
        f"*{t('send_inquiry.city', 'City')}",
        placeholder="Warsaw"
    )
    
    customer_country = st.selectbox(
        f"*{t('send_inquiry.country', 'Country')}",
        ["Poland", "Germany", "Czech Republic", "Slovakia", "Austria", "Netherlands", "Belgium", "Other"],
        help="Select your country"
    )

# SECTION 2: Project Details
st.header(f"🏗️ {t('send_inquiry.project_details', 'Project Information')}")

col1, col2 = st.columns(2)

with col1:
    project_name = st.text_input(
        t('send_inquiry.project_name', 'Project Name'),
        placeholder="Container Office Complex"
    )
    
    project_location = st.text_input(
        f"*{t('send_inquiry.project_location', 'Project Location')}",
        placeholder="City, Region, Country"
    )

with col2:
    expected_timeline = st.selectbox(
        f"*{t('send_inquiry.expected_timeline', 'Expected Timeline')}",
        [
            t('send_inquiry.timeline.asap', 'As soon as possible'),
            t('send_inquiry.timeline.within_month', 'Within 1 month'),
            t('send_inquiry.timeline.within_quarter', 'Within 3 months'),
            t('send_inquiry.timeline.within_half_year', 'Within 6 months'),
            t('send_inquiry.timeline.planning_phase', 'Planning phase only')
        ]
    )
    
    budget_range = st.selectbox(
        t('send_inquiry.budget_range', 'Budget Range (Optional)'),
        [
            t('send_inquiry.budget.not_specified', 'Not specified'),
            "€20,000 - €50,000",
            "€50,000 - €100,000",
            "€100,000 - €200,000",
            "€200,000 - €500,000",
            "€500,000+"
        ]
    )

# SECTION 3: Project Requirements
st.header(f"📝 {t('send_inquiry.project_requirements', 'Project Requirements')}")

inquiry_type = st.selectbox(
    f"*{t('send_inquiry.inquiry_type', 'Type of Inquiry')}",
    [
        t('send_inquiry.types.detailed_quote', 'Detailed price quote'),
        t('send_inquiry.types.technical_consultation', 'Technical consultation'),
        t('send_inquiry.types.site_visit', 'Site visit request'),
        t('send_inquiry.types.drawing_analysis', 'Drawing analysis service'),
        t('send_inquiry.types.general_info', 'General information')
    ]
)

col1, col2 = st.columns(2)

with col1:
    special_requirements = st.text_area(
        t('send_inquiry.special_requirements', 'Special Requirements'),
        placeholder=t('send_inquiry.special_requirements_placeholder', 'Describe specific technical requirements, certifications, special installations...'),
        height=120,
        help="Include any special technical specifications or requirements"
    )

with col2:
    additional_message = st.text_area(
        t('send_inquiry.additional_message', 'Additional Information'),
        placeholder=t('send_inquiry.additional_message_placeholder', 'Any additional information that will help us prepare a better quote...'),
        height=120,
        help="Any other details about your project"
    )

# SECTION 4: File Attachments & Documentation
st.header(f"📎 {t('send_inquiry.attachments', 'Project Documentation')}")

st.info(f"""
📋 **{t('send_inquiry.recommended_files', 'Recommended Documents')}:**
• Technical drawings (PDF, DWG)
• Site plans and layout drawings
• Project specifications
• Reference photos or sketches
• Building permits or requirements
• Any relevant documentation
""")

uploaded_files = st.file_uploader(
    t('send_inquiry.upload_files', 'Upload Project Files'),
    type=['pdf', 'dwg', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'xlsx', 'txt'],
    accept_multiple_files=True,
    help=t('send_inquiry.file_formats_help', 'Supported formats: PDF, DWG, JPG, PNG, DOC, DOCX, XLSX, TXT. Max total size: 25MB')
)

# File validation
files_valid = True
total_size = 0
max_total_size = 25 * 1024 * 1024  # 25MB

if uploaded_files:
    for file in uploaded_files:
        total_size += file.size
    
    if total_size > max_total_size:
        st.error(f"❌ Total file size ({total_size / (1024*1024):.1f} MB) exceeds 25MB limit. Please reduce file sizes or remove some files.")
        files_valid = False
    else:
        st.success(f"✅ {len(uploaded_files)} files uploaded ({total_size / (1024*1024):.1f} MB / 25 MB)")
        
        with st.expander("📄 Uploaded Files", expanded=False):
            for file in uploaded_files:
                file_size_mb = file.size / (1024*1024)
                st.write(f"📄 **{file.name}** ({file_size_mb:.1f} MB)")

# SECTION 5: Contact Preferences
st.header(f"📞 {t('send_inquiry.contact_preferences', 'Contact Preferences')}")

col1, col2 = st.columns(2)

with col1:
    preferred_contact = st.selectbox(
        t('send_inquiry.preferred_contact', 'Preferred Contact Method'),
        [
            t('send_inquiry.contact.email', 'Email'),
            t('send_inquiry.contact.phone', 'Phone call'),
            t('send_inquiry.contact.both', 'Email and phone')
        ]
    )

with col2:
    best_time = st.selectbox(
        t('send_inquiry.best_time', 'Best Time to Contact'),
        [
            t('send_inquiry.time.morning', 'Morning (8:00-12:00)'),
            t('send_inquiry.time.afternoon', 'Afternoon (12:00-17:00)'),
            t('send_inquiry.time.evening', 'Evening (17:00-20:00)'),
            t('send_inquiry.time.anytime', 'Any time')
        ]
    )

# SECTION 6: RODO/GDPR Compliance
st.header(f"🔒 {t('send_inquiry.privacy_section', 'Privacy & Data Protection (RODO/GDPR)')}")

st.info(f"""
🛡️ **{t('send_inquiry.data_protection_info', 'Data Protection Information')}:**

• Your personal data will be processed by KAN-BUD Sp. z o.o. for the purpose of handling your inquiry
• Data will be stored for the duration necessary to process your request (typically 2 years)
• You have the right to access, rectify, delete, or port your data
• You can withdraw consent at any time by contacting us at privacy@kan-bud.pl
• Full privacy policy available at: www.kan-bud.pl/privacy-policy
""")

# Required privacy consent
privacy_consent = st.checkbox(
    f"*{t('send_inquiry.privacy_consent', 'I consent to the processing of my personal data by KAN-BUD Sp. z o.o. for the purpose of handling this inquiry, in accordance with RODO/GDPR regulations')}",
    help="This consent is required to process your inquiry"
)

# Optional marketing consent
marketing_consent = st.checkbox(
    t('send_inquiry.marketing_consent', 'I consent to receiving marketing information about KAN-BUD services and products (optional)'),
    help="You can unsubscribe at any time"
)

# Data retention notice
st.caption(f"""
📅 **{t('send_inquiry.data_retention', 'Data Retention')}:** Your data will be retained for up to 2 years or until you withdraw consent. 
Contact privacy@kan-bud.pl for data deletion requests.
""")

# SECTION 7: Submit Inquiry
st.divider()

# Validation
required_fields = [customer_name, customer_email, customer_phone, customer_city, project_location, expected_timeline, inquiry_type]
all_required_filled = all(field.strip() if isinstance(field, str) else field for field in required_fields) and privacy_consent and files_valid

if not all_required_filled:
    if not files_valid:
        st.warning("⚠️ Please fix file size issues before submitting.")
    elif not privacy_consent:
        st.warning("⚠️ Privacy consent is required to submit the inquiry.")
    else:
        st.warning(f"⚠️ {t('send_inquiry.fill_required_fields', 'Please fill in all required fields marked with *')}")

# Submit button
submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])

with submit_col2:
    if st.button(
        f"📧 {t('send_inquiry.submit_inquiry', 'Submit Professional Inquiry')}",
        use_container_width=True,
        type="primary",
        disabled=not all_required_filled
    ):
        # Prepare comprehensive inquiry data
        inquiry_data = {
            'inquiry_id': f"INQ-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
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
                'budget_range': budget_range,
                'special_requirements': special_requirements,
                'additional_message': additional_message
            },
            'inquiry': {
                'type': inquiry_type,
                'files_count': len(uploaded_files) if uploaded_files else 0,
                'total_file_size_mb': round(total_size / (1024*1024), 2) if uploaded_files else 0
            },
            'contact_preferences': {
                'preferred_method': preferred_contact,
                'best_time': best_time
            },
            'consents': {
                'privacy': privacy_consent,
                'marketing': marketing_consent,
                'consent_timestamp': datetime.now().isoformat()
            }
        }
        
        # Add configuration data if available
        if config_to_use:
            inquiry_data['container_config'] = config_to_use
            
        if estimate_to_use:
            inquiry_data['ai_estimate'] = estimate_to_use
            
        if 'cost_breakdown' in st.session_state:
            inquiry_data['cost_breakdown'] = st.session_state.cost_breakdown
        
        # Save inquiry
        try:
            storage = SimpleStorageManager()
            storage.save_user_project(
                user_id=st.session_state.get('user_id', 'guest'),
                project_name=f"Inquiry: {customer_name} - {datetime.now().strftime('%Y-%m-%d')}",
                config=inquiry_data
            )
            
            st.success(f"""
            ✅ **{t('send_inquiry.success_title', 'Inquiry Submitted Successfully!')}**
            
            **Inquiry ID:** {inquiry_data['inquiry_id']}
            
            {t('send_inquiry.success_message', 'Thank you for your inquiry. Our team will contact you within 24 hours with a detailed response.')}
            """)
            
            # Show next steps
            st.info(f"""
            **{t('send_inquiry.next_steps', 'What Happens Next')}:**
            
            1. 📋 **Analysis** - Our experts will review your requirements and uploaded files
            2. 📞 **Contact** - We'll reach out within 24 hours for any clarifications
            3. 💰 **Quote** - You'll receive a detailed, professional quote tailored to your needs
            4. 🤝 **Follow-up** - We'll schedule a consultation to discuss your project
            
            **{t('send_inquiry.contact_info', 'Emergency Contact')}:**
            📞 +48 XXX XXX XXX | ✉️ office@kan-bud.pl
            """)
            
            st.balloons()
            
            # Clear inquiry transfer data
            for key in ['inquiry_source', 'inquiry_config', 'inquiry_estimate']:
                if key in st.session_state:
                    del st.session_state[key]
            
            # Option to create new inquiry
            if st.button(f"📝 {t('send_inquiry.new_inquiry', 'Submit Another Inquiry')}", use_container_width=True):
                st.rerun()
                
        except Exception as e:
            st.error(f"{t('send_inquiry.error', 'Error submitting inquiry')}: {str(e)}")

# Additional information section
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.info(f"""
    📋 **{t('send_inquiry.why_professional_inquiry', 'Why Submit a Professional Inquiry?')}**
    
    • Get accurate pricing based on your specific requirements
    • Receive expert technical consultation
    • Access to our full range of services and options
    • Professional project management support
    • Compliance with local building codes and regulations
    """)

with col2:
    st.success(f"""
    💡 **{t('send_inquiry.preparation_tips', 'Tips for Best Results')}**
    
    • Include detailed project drawings or sketches
    • Specify all technical requirements clearly
    • Mention any special certifications needed
    • Provide accurate timeline and budget information
    • Include site access and logistics considerations
    """)

# Contact information footer
st.divider()

st.markdown(f"""
### 📞 {t('contact_us', 'Contact Information')}

**KAN-BUD Sp. z o.o.**  
📍 **{t('address', 'Address')}:** [Company Address]  
📞 **{t('phone', 'Phone')}:** +48 XXX XXX XXX  
✉️ **{t('email', 'Email')}:** office@kan-bud.pl  
🌐 **Website:** www.kan-bud.pl  
🕒 **{t('working_hours', 'Working Hours')}:** {t('mon_fri', 'Mon-Fri 8:00-17:00')}  
""")
