import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.container_database import ContainerDatabase
from utils.calculations import StructuralCalculations
from utils.database import DatabaseManager
from utils.simple_storage import SimpleStorageManager
from utils.historical_data_service import HistoricalDataService
from utils.translations import get_text, get_available_languages
from utils.ai_services import OpenAIService, AnthropicService

# Page configuration
st.set_page_config(
    page_title="KAN-BUD Professional Container Solutions",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize services
@st.cache_resource
def initialize_services():
    """Initialize all services with caching"""
    # Try PostgreSQL first, fallback to simple storage
    try:
        db = DatabaseManager()
        if not db.engine:
            storage = SimpleStorageManager()
        else:
            storage = db
    except:
        storage = SimpleStorageManager()
    
    container_db = ContainerDatabase()
    calc = StructuralCalculations()
    historical_service = HistoricalDataService()
    
    # Initialize AI services
    try:
        openai_service = OpenAIService()
        anthropic_service = AnthropicService()
    except:
        openai_service = None
        anthropic_service = None
    
    return storage, container_db, calc, historical_service, openai_service, anthropic_service

# Language selection
available_languages = get_available_languages()
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Employee authentication
if 'employee_logged_in' not in st.session_state:
    st.session_state.employee_logged_in = False

# Modern client-focused header
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("# 🏗️ KAN-BUD")
    st.markdown("### " + get_text('subtitle', st.session_state.get('language', 'en')))

with col2:
    # Language selector
    st.markdown("**🌐 Język / Language**")
    selected_language = st.selectbox(
        "",
        options=list(available_languages.keys()),
        format_func=lambda x: available_languages[x],
        index=list(available_languages.keys()).index(st.session_state.language),
        label_visibility="collapsed"
    )
    
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()

with col3:
    # Discrete employee login in header
    if not st.session_state.employee_logged_in:
        with st.expander("👤 Pracownicy", expanded=False):
            employee_password = st.text_input("Hasło:", type="password", key="emp_pwd")
            if st.button("Zaloguj", key="emp_login"):
                if employee_password == "kan-bud-employee-2024":
                    st.session_state.employee_logged_in = True
                    st.success("Zalogowano!")
                    st.rerun()
                else:
                    st.error("Błędne hasło")
    else:
        st.success("✅ Pracownik")
        if st.button("Wyloguj", key="emp_logout"):
            st.session_state.employee_logged_in = False
            st.rerun()

# Initialize session state
if 'container_db' not in st.session_state:
    st.session_state.container_db = ContainerDatabase()

if 'calculations' not in st.session_state:
    st.session_state.calculations = StructuralCalculations()

if 'historical_service' not in st.session_state:
    st.session_state.historical_service = HistoricalDataService()

# Get current language
lang = st.session_state.get('language', 'en')

# Initialize services
storage, container_db, calc, historical_service_init, openai_service, anthropic_service = initialize_services()

st.markdown("---")

# Modern client-focused main dashboard
if st.session_state.employee_logged_in:
    # Employee view - show all tools
    st.markdown("## 🔧 Narzędzia dla Pracowników")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📦 Konfigurator\nKontenerów", key="emp_config", use_container_width=True, type="primary"):
            st.switch_page("pages/1_Container_Configurator.py")
    
    with col2:
        if st.button("🤖 Szacowanie\nKosztów AI", key="emp_ai", use_container_width=True):
            st.switch_page("pages/2_AI_Cost_Estimator.py")
    
    with col3:
        if st.button("🔧 Analiza\nTechniczna", key="emp_tech", use_container_width=True):
            st.switch_page("pages/3_Technical_Analysis.py")
    
    with col4:
        if st.button("📋 Generator\nOfert", key="emp_quote", use_container_width=True):
            st.switch_page("pages/4_Quote_Generator.py")
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        if st.button("⚖️ Narzędzie\nPorównań", key="emp_compare", use_container_width=True):
            st.switch_page("pages/5_Comparison_Tool.py")
    
    with col6:
        if st.button("📐 Analiza\nRysunków", key="emp_draw", use_container_width=True):
            st.switch_page("pages/6_Drawing_Analysis.py")
    
    with col7:
        if st.button("🔐 Panel\nAdministracyjny", key="emp_admin", use_container_width=True):
            st.switch_page("pages/Admin_Panel.py")

else:
    # Client view - modern, attractive layout
    st.markdown("## 💼 " + get_text('configure_container', lang))
    st.markdown("*" + get_text('simple_process_2_steps', lang) + "*")
    
    # Large client action cards
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown(f"""
        <div style="
            border: 2px solid #1f77b4; 
            border-radius: 15px; 
            padding: 30px; 
            text-align: center; 
            background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        ">
            <h2 style="color: #1f77b4; margin-bottom: 15px;">
                📦 {get_text('step_1_configuration', lang)}
            </h2>
            <p style="font-size: 18px; color: #333; margin-bottom: 20px;">
                {get_text('choose_container_type', lang)}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 " + get_text('start_configuration', lang), key="client_config", use_container_width=True, type="primary"):
            st.switch_page("pages/1_Container_Configurator.py")
    
    with col2:
        st.markdown(f"""
        <div style="
            border: 2px solid #ff7f0e; 
            border-radius: 15px; 
            padding: 30px; 
            text-align: center; 
            background: linear-gradient(135deg, #fff8f0 0%, #ffe6cc 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        ">
            <h2 style="color: #ff7f0e; margin-bottom: 15px;">
                🤖 {get_text('step_2_ai_quote', lang)}
            </h2>
            <p style="font-size: 18px; color: #333; margin-bottom: 20px;">
                {get_text('get_instant_quote', lang)}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💰 " + get_text('get_quote', lang), key="client_ai", use_container_width=True, type="secondary"):
            st.switch_page("pages/2_AI_Cost_Estimator.py")

# Client benefits section
if not st.session_state.employee_logged_in:
    st.markdown("---")
    st.markdown("## ✨ Dlaczego KAN-BUD?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 Precyzyjne Wyceny
        - Wykorzystanie AI i danych historycznych
        - Uwzględnienie europejskich norm klimatycznych
        - Transparentne kalkulacje kosztów
        """)
    
    with col2:
        st.markdown("""
        ### ⚡ Szybka Realizacja
        - Doświadczenie z setkami projektów
        - Własny park maszynowy
        - Lokalizacja w centrum Polski
        """)
    
    with col3:
        st.markdown("""
        ### 🔧 Pełen Serwis
        - Projekt i wykonanie
        - Transport i montaż
        - Wsparcie posprzedażowe
        """)
    
    # Contact information for clients
    st.markdown("---")
    st.markdown("## 📞 Kontakt")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📍 Adres**\nKąkolewo, Polska")
    with col2:
        st.markdown("**📞 Telefon**\n+48 XXX XXX XXX")
    with col3:
        st.markdown("**✉️ Email**\ninfo@kan-bud.pl")