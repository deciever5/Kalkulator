
"""
Customer Inquiry Form - Available for all users
Allows customers to send inquiries after getting estimates
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.translations import t, render_language_selector
from utils.global_language import get_current_language, set_language
from utils.simple_storage import SimpleStorageManager

st.set_page_config(page_title="Send Inquiry", page_icon="📧", layout="wide")

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Language selector - using the same dropdown style as other pages
render_language_selector()

st.title(f"📧 {t('send_inquiry')}")
st.markdown(f"*{t('get_detailed_quote_text')}*")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button(t('back_to_home', 'Powrót do strony głównej'), key="home_nav", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button(t('go_to_configurator', 'Przejdź do konfiguratora'), key="config_nav", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")

# Important disclaimer
st.warning(f"""
⚠️ **{t('send_inquiry_form.disclaimer_title', 'Ważne informacje / Important Information')}**

{t('send_inquiry_form.disclaimer_text', 'Ten formularz służy do wysyłania zapytań o szczegółowe oferty. Szacunki z naszego kalkulatora nie stanowią ofert handlowych w rozumieniu prawa.')}
""")

# Check if there's a saved configuration or estimate
has_config = 'container_config' in st.session_state and st.session_state.container_config
has_estimate = 'ai_estimate' in st.session_state

if has_config or has_estimate:
    st.success(f"✅ {t('send_inquiry_form.config_detected', 'Wykryto konfigurację z kalkulatora')}")
    
    with st.expander(f"📋 {t('send_inquiry_form.current_config', 'Aktualna konfiguracja')}", expanded=False):
        if has_config:
            config = st.session_state.container_config
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**{t('form.labels.container_type', 'Typ kontenera')}:** {config.get('container_type', 'N/A')}")
                st.write(f"**{t('form.labels.main_purpose', 'Przeznaczenie')}:** {config.get('main_purpose', 'N/A')}")
                st.write(f"**{t('form.labels.environment', 'Środowisko')}:** {config.get('environment', 'N/A')}")
            
            with col2:
                st.write(f"**{t('form.labels.finish_level', 'Poziom wykończenia')}:** {config.get('finish_level', 'N/A')}")
                st.write(f"**{t('form.labels.climate_zone', 'Strefa klimatyczna')}:** {config.get('climate_zone', 'N/A')}")
                st.write(f"**{t('form.labels.number_of_windows', 'Okna')}:** {config.get('number_of_windows', 'N/A')}")
        
        if has_estimate:
            st.markdown(f"### {t('saved_ai_estimate', 'Szacunek AI')}:")
            st.write(st.session_state.ai_estimate)

st.markdown("---")

# Customer Information Form
st.markdown(f"### 👤 {t('send_inquiry_form.customer_info', 'Informacje o kliencie')}")

col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input(f"{t('send_inquiry_form.full_name', 'Imię i nazwisko')} *", key="cust_name")
    company_name = st.text_input(t('send_inquiry_form.company_name', 'Nazwa firmy'), key="comp_name")
    email = st.text_input(f"{t('send_inquiry_form.email', 'Email')} *", key="cust_email")

with col2:
    phone = st.text_input(f"{t('send_inquiry_form.phone', 'Telefon')} *", key="cust_phone")
    address = st.text_input(t('form.labels.address', 'Adres'), key="cust_address")
    city = st.text_input(t('send_inquiry_form.city', 'Miasto'), key="cust_city")

# Project Information
st.markdown(f"### 🏗️ {t('send_inquiry_form.project_details', 'Informacje o projekcie')}")

project_name = st.text_input(t('send_inquiry_form.project_name', 'Nazwa projektu'))
project_description = st.text_area(f"{t('form.labels.project_description', 'Opis projektu')} *", height=100)
additional_requirements = st.text_area(t('send_inquiry_form.special_requirements', 'Dodatkowe wymagania'), height=80)

# Timeline and Budget
col1, col2 = st.columns(2)
with col1:
    timeline = st.selectbox(
        t('send_inquiry_form.expected_timeline', 'Planowany termin realizacji'),
        [
            t('send_inquiry_form.timeline.asap', 'Jak najszybciej'),
            t('send_inquiry_form.timeline.within_month', '1-2 miesiące'),
            t('send_inquiry_form.timeline.within_quarter', '3-6 miesięcy'), 
            t('send_inquiry_form.timeline.within_half_year', 'Powyżej 6 miesięcy')
        ]
    )

with col2:
    budget_range = st.selectbox(
        f"{t('send_inquiry_form.budget_Range', 'Przybliżony budżet')} (EUR)",
        [
            t('send_inquiry_form.budget.not_specified', '< 10,000'),
            t('send_inquiry_form.budget.up_to_50k', '10,000 - 25,000'),
            t('send_inquiry_form.budget.50k_100k', '25,000 - 50,000'),
            t('send_inquiry_form.budget.100k_200k', '50,000 - 100,000'),
            t('send_inquiry_form.budget.over_200k', '> 100,000')
        ]
    )

# File Upload
st.markdown(f"### 📎 {t('send_inquiry_form.attachments', 'Załączniki')}")
uploaded_files = st.file_uploader(
    t('send_inquiry_form.upload_files', 'Prześlij dokumenty (PDF, DWG, JPG, PNG)'),
    accept_multiple_files=True,
    type=['pdf', 'dwg', 'jpg', 'jpeg', 'png'],
    help=t('send_inquiry_form.file_formats_help', 'Obsługiwane formaty: PDF, DWG, JPG, PNG, DOC, DOCX')
)

# Contact preferences
st.markdown(f"### 📞 {t('send_inquiry_form.contact_preferences', 'Preferencje kontaktu')}")
col1, col2 = st.columns(2)

with col1:
    contact_method = st.selectbox(
        t('send_inquiry_form.preferred_contact', 'Preferowana metoda kontaktu'),
        [
            t('send_inquiry_form.contact.email', 'Email'),
            t('send_inquiry_form.contact.phone', 'Telefon'),
            t('send_inquiry_form.contact.both', 'Obie')
        ]
    )

with col2:
    contact_time = st.selectbox(
        t('send_inquiry_form.best_time', 'Preferowany czas kontaktu'),
        [
            t('send_inquiry_form.time.morning', 'Rano (8-12)'),
            t('send_inquiry_form.time.afternoon', 'Popołudnie (12-17)'),
            t('send_inquiry_form.time.anytime', 'Dowolny')
        ]
    )

# RODO/GDPR Consent
st.markdown(f"### 🔒 {t('send_inquiry_form.privacy_section', 'Zgody')}")
gdpr_consent = st.checkbox(
    f"{t('send_inquiry_form.privacy_consent', 'Wyrażam zgodę na przetwarzanie moich danych osobowych')} *",
    key="gdpr_consent"
)

marketing_consent = st.checkbox(
    t('send_inquiry_form.marketing_consent', 'Wyrażam zgodę na otrzymywanie informacji marketingowych'),
    key="marketing_consent"
)

# Submit button
st.markdown("---")

if st.button(f"📧 {t('send_inquiry_form.submit_inquiry', 'Wyślij zapytanie')}", type="primary", use_container_width=True):
    # Validation
    if not customer_name or not email or not phone or not project_description or not gdpr_consent:
        st.error(t('send_inquiry_form.fill_required_fields', 'Proszę wypełnić wszystkie wymagane pola i wyrazić zgodę na przetwarzanie danych'))
    else:
        # Prepare inquiry data
        inquiry_data = {
            'timestamp': datetime.now().isoformat(),
            'customer_name': customer_name,
            'company_name': company_name,
            'email': email,
            'phone': phone,
            'address': address,
            'city': city,
            'project_name': project_name,
            'project_description': project_description,
            'additional_requirements': additional_requirements,
            'timeline': timeline,
            'budget_range': budget_range,
            'contact_method': contact_method,
            'contact_time': contact_time,
            'gdpr_consent': gdpr_consent,
            'marketing_consent': marketing_consent,
            'container_config': st.session_state.get('container_config', {}),
            'ai_estimate': st.session_state.get('ai_estimate', ''),
            'files_uploaded': len(uploaded_files) if uploaded_files else 0
        }
        
        # Save to storage
        try:
            storage = SimpleStorageManager()
            storage.save_inquiry(inquiry_data)
            
            st.success(f"""
            ✅ **{t('send_inquiry_form.success_title', 'Zapytanie zostało wysłane!')}**
            
            {t('send_inquiry_form.success_message', 'Dziękujemy za przesłanie zapytania. Skontaktujemy się z Państwem w ciągu 24 godzin.')}
            """)
            
            # Clear the form
            for key in st.session_state.keys():
                if key.startswith(('cust_', 'comp_', 'gdpr_', 'marketing_')):
                    del st.session_state[key]
            
        except Exception as e:
            st.error(f"{t('send_inquiry_form.error', 'Błąd podczas wysyłania zapytania')}: {str(e)}")

# Contact information
st.markdown("---")
st.markdown(f"### 📞 {t('contact_us', 'Kontakt')}")
st.markdown(f"""
**KAN-BUD**  
📍 Kąkolewo, Polska  
📞 +48 XXX XXX XXX  
✉️ info@kan-bud.pl  
🕒 {t('mon_fri', 'Pon-Pt')}: 8:00-17:00
""")
