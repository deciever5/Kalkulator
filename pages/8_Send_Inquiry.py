"""
Customer Inquiry Form - Available for all users
Allows customers to send inquiries after getting estimates
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.translations import t
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

# Language selector
render_language_selector()

st.title(f"📧 {t('send_inquiry')}")
st.markdown(f"*{t('get_detailed_quote_text')}*")

# Navigation buttons
col1, col2 = st.columns(2)
with col1:
    if st.button(t('back_to_home'), key="home_nav", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button(t('go_to_configurator'), key="config_nav", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")

# Important disclaimer
st.warning("""
⚠️ **Ważne informacje / Important Information**

PL: Ten formularz służy do wysyłania zapytań o szczegółowe oferty. Szacunki z naszego kalkulatora nie stanowią ofert handlowych w rozumieniu prawa.

EN: This form is for sending inquiry requests for detailed quotes. Estimates from our calculator are not commercial offers under applicable law.
""")

# Check if there's a saved configuration or estimate
has_config = 'container_config' in st.session_state and st.session_state.container_config
has_estimate = 'ai_estimate' in st.session_state

if has_config or has_estimate:
    st.success("✅ Wykryto konfigurację z kalkulatora / Configuration detected from calculator")
    
    with st.expander("📋 Aktualna konfiguracja / Current Configuration", expanded=False):
        if has_config:
            config = st.session_state.container_config
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Typ kontenera / Container Type:** {config.get('container_type', 'N/A')}")
                st.write(f"**Przeznaczenie / Purpose:** {config.get('main_purpose', 'N/A')}")
                st.write(f"**Środowisko / Environment:** {config.get('environment', 'N/A')}")
            
            with col2:
                st.write(f"**Poziom wykończenia / Finish Level:** {config.get('finish_level', 'N/A')}")
                st.write(f"**Strefa klimatyczna / Climate Zone:** {config.get('climate_zone', 'N/A')}")
                st.write(f"**Okna / Windows:** {config.get('number_of_windows', 'N/A')}")
        
        if has_estimate:
            st.markdown("### Szacunek AI / AI Estimate:")
            st.write(st.session_state.ai_estimate)

st.markdown("---")

# Customer Information Form
st.markdown("### 👤 Informacje o kliencie / Customer Information")

col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input("Imię i nazwisko / Full Name *", key="cust_name")
    company_name = st.text_input("Nazwa firmy / Company Name", key="comp_name")
    email = st.text_input("Email *", key="cust_email")

with col2:
    phone = st.text_input("Telefon / Phone *", key="cust_phone")
    address = st.text_input("Adres / Address", key="cust_address")
    city = st.text_input("Miasto / City", key="cust_city")

# Project Information
st.markdown("### 🏗️ Informacje o projekcie / Project Information")

project_name = st.text_input("Nazwa projektu / Project Name")
project_description = st.text_area("Opis projektu / Project Description *", height=100)
additional_requirements = st.text_area("Dodatkowe wymagania / Additional Requirements", height=80)

# Timeline and Budget
col1, col2 = st.columns(2)
with col1:
    timeline = st.selectbox(
        "Planowany termin realizacji / Timeline",
        ["Jak najszybciej / ASAP", "1-2 miesiące / 1-2 months", "3-6 miesięcy / 3-6 months", "Powyżej 6 miesięcy / 6+ months"]
    )

with col2:
    budget_range = st.selectbox(
        "Przybliżony budżet / Budget Range (EUR)",
        ["< 10,000", "10,000 - 25,000", "25,000 - 50,000", "50,000 - 100,000", "> 100,000"]
    )

# File Upload
st.markdown("### 📎 Załączniki / Attachments")
uploaded_files = st.file_uploader(
    "Prześlij dokumenty (PDF, DWG, JPG, PNG) / Upload documents",
    accept_multiple_files=True,
    type=['pdf', 'dwg', 'jpg', 'jpeg', 'png']
)

# Contact preferences
st.markdown("### 📞 Preferencje kontaktu / Contact Preferences")
col1, col2 = st.columns(2)

with col1:
    contact_method = st.selectbox(
        "Preferowana metoda kontaktu / Preferred contact method",
        ["Email", "Telefon / Phone", "Obie / Both"]
    )

with col2:
    contact_time = st.selectbox(
        "Preferowany czas kontaktu / Preferred contact time",
        ["Rano (8-12) / Morning", "Popołudnie (12-17) / Afternoon", "Dowolny / Any time"]
    )

# RODO/GDPR Consent
st.markdown("### 🔒 Zgody / Consent")
gdpr_consent = st.checkbox(
    "Wyrażam zgodę na przetwarzanie moich danych osobowych zgodnie z RODO / I consent to processing of my personal data according to GDPR *",
    key="gdpr_consent"
)

marketing_consent = st.checkbox(
    "Wyrażam zgodę na otrzymywanie informacji marketingowych / I consent to receiving marketing information",
    key="marketing_consent"
)

# Submit button
st.markdown("---")

if st.button("📧 Wyślij zapytanie / Send Inquiry", type="primary", use_container_width=True):
    # Validation
    if not customer_name or not email or not phone or not project_description or not gdpr_consent:
        st.error("Proszę wypełnić wszystkie wymagane pola i wyrazić zgodę na przetwarzanie danych / Please fill all required fields and give consent for data processing")
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
            
            st.success("""
            ✅ **Zapytanie zostało wysłane! / Inquiry sent successfully!**
            
            PL: Dziękujemy za przesłanie zapytania. Skontaktujemy się z Państwem w ciągu 24 godzin.
            
            EN: Thank you for your inquiry. We will contact you within 24 hours.
            """)
            
            # Clear the form
            for key in st.session_state.keys():
                if key.startswith(('cust_', 'comp_', 'gdpr_', 'marketing_')):
                    del st.session_state[key]
            
        except Exception as e:
            st.error(f"Błąd podczas wysyłania zapytania / Error sending inquiry: {str(e)}")

# Contact information
st.markdown("---")
st.markdown("### 📞 Kontakt / Contact")
st.markdown("""
**KAN-BUD**  
📍 Kąkolewo, Polska  
📞 +48 XXX XXX XXX  
✉️ info@kan-bud.pl  
🕒 Pon-Pt / Mon-Fri: 8:00-17:00
""")