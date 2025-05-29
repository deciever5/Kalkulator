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

# Modern header with enhanced styling
st.markdown("""
<style>
/* Hide sidebar completely */
.css-1d391kg {display: none !important;}
.css-1y4p8pa {margin-left: 0 !important;}
.css-17eq0hr {display: none !important;}
section[data-testid="stSidebar"] {display: none !important;}
.css-164nlkn {margin-left: 0 !important;}
div[data-testid="stSidebarNav"] {display: none !important;}

.main-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
.company-name {
    color: white;
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}
.company-subtitle {
    color: #e8f4f8;
    font-size: 1.2rem;
    text-align: center;
    margin-bottom: 1rem;
}
.header-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
}
.feature-card {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid #e8f4f8;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    height: 100%;
}
.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
}
.feature-icon {
    font-size: 3rem;
    text-align: center;
    margin-bottom: 1rem;
}
.feature-title {
    font-size: 1.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1rem;
    color: #1e3c72;
}
.feature-description {
    text-align: center;
    color: #666;
    line-height: 1.6;
}
.benefits-section {
    background: linear-gradient(135deg, #f8fbff 0%, #e8f4f8 100%);
    padding: 3rem 2rem;
    border-radius: 15px;
    margin: 2rem 0;
}
.benefit-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    height: 100%;
}
.contact-section {
    background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
}
</style>

<div class="main-header">
    <div class="company-name">🏗️ KAN-BUD</div>
    <div class="company-subtitle">AI-Powered Cost Estimation for Container Modifications</div>
</div>
""", unsafe_allow_html=True)

# Header controls
col1, col2, col3 = st.columns([2, 1, 1])

with col2:
    # Language selector with improved styling
    st.markdown("##### 🌐 Język / Language")
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
    # Enhanced employee login
    if not st.session_state.employee_logged_in:
        with st.expander("👤 Panel Pracownika", expanded=False):
            st.markdown("**Dostęp dla pracowników KAN-BUD**")
            employee_password = st.text_input("Hasło:", type="password", key="emp_pwd")
            if st.button("🔐 Zaloguj", key="emp_login", use_container_width=True):
                if employee_password == "kan-bud-employee-2024":
                    st.session_state.employee_logged_in = True
                    st.success("✅ Pomyślnie zalogowano!")
                    st.rerun()
                else:
                    st.error("❌ Błędne hasło")
    else:
        st.success("✅ Zalogowany jako Pracownik")
        if st.button("🚪 Wyloguj", key="emp_logout", use_container_width=True):
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
    # Employee view - enhanced card layout
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1.5rem; border-radius: 15px; margin: 2rem 0; text-align: center;">
        <h2 style="margin: 0;">🔧 Narzędzia dla Pracowników</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Pełny dostęp do wszystkich funkcji systemu</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Primary tools
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    tools = [
        ("📦", "Konfigurator\nKontenerów", "Tworzenie konfiguracji kontenerów", "pages/1_Container_Configurator.py", "emp_config"),
        ("🤖", "Szacowanie\nKosztów AI", "Automatyczne wyceny AI", "pages/2_AI_Cost_Estimator.py", "emp_ai"),
        ("🔧", "Analiza\nTechniczna", "Obliczenia strukturalne", "pages/3_Technical_Analysis.py", "emp_tech"),
        ("📋", "Generator\nOfert", "Profesjonalne oferty", "pages/4_Quote_Generator.py", "emp_quote")
    ]
    
    for i, (icon, title, desc, page, key) in enumerate(tools):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title.replace(chr(10), ' ')}</div>
                <div class="feature-description">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Otwórz {title.replace(chr(10), ' ')}", key=key, use_container_width=True, type="primary"):
                st.switch_page(page)
    
    # Secondary tools
    col5, col6, col7 = st.columns([1, 1, 1], gap="large")
    
    secondary_tools = [
        ("⚖️", "Narzędzie\nPorównań", "Porównywanie konfiguracji", "pages/5_Comparison_Tool.py", "emp_compare"),
        ("📐", "Analiza\nRysunków", "Analiza dokumentów AI", "pages/6_Drawing_Analysis.py", "emp_draw"),
        ("🔐", "Panel\nAdministracyjny", "Zarządzanie systemem", "pages/Admin_Panel.py", "emp_admin")
    ]
    
    for i, (icon, title, desc, page, key) in enumerate(secondary_tools):
        with [col5, col6, col7][i]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title.replace(chr(10), ' ')}</div>
                <div class="feature-description">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Otwórz {title.replace(chr(10), ' ')}", key=key, use_container_width=True):
                st.switch_page(page)

else:
    # Client view - enhanced modern layout
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="color: #1e3c72; font-size: 2.5rem; margin-bottom: 0.5rem;">
            💼 {get_text('configure_container', lang)}
        </h2>
        <p style="font-size: 1.3rem; color: #666; font-style: italic;">
            {get_text('simple_process_2_steps', lang)}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced client action cards
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown(f"""
        <div class="feature-card" style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 3rem 2rem;
            transform: scale(1.02);
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📦</div>
            <h2 style="color: white; margin-bottom: 1rem; font-size: 1.8rem;">
                {get_text('step_1_configuration', lang)}
            </h2>
            <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 0;">
                {get_text('choose_container_type', lang)}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 " + get_text('start_configuration', lang), key="client_config", use_container_width=True, type="primary"):
            st.switch_page("pages/1_Container_Configurator.py")
    
    with col2:
        st.markdown(f"""
        <div class="feature-card" style="
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            text-align: center;
            padding: 3rem 2rem;
            transform: scale(1.02);
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🤖</div>
            <h2 style="color: white; margin-bottom: 1rem; font-size: 1.8rem;">
                {get_text('step_2_ai_quote', lang)}
            </h2>
            <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 0;">
                {get_text('get_instant_quote', lang)}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💰 " + get_text('get_quote', lang), key="client_ai", use_container_width=True, type="secondary"):
            st.switch_page("pages/2_AI_Cost_Estimator.py")

# Enhanced client benefits section
if not st.session_state.employee_logged_in:
    st.markdown("""
    <div class="benefits-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 2rem; font-size: 2.2rem;">
            ✨ Dlaczego KAN-BUD?
        </h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    benefits = [
        ("🎯", "Precyzyjne Wyceny", [
            "Wykorzystanie AI i danych historycznych",
            "Uwzględnienie europejskich norm klimatycznych", 
            "Transparentne kalkulacje kosztów"
        ]),
        ("⚡", "Szybka Realizacja", [
            "Doświadczenie z setkami projektów",
            "Własny park maszynowy",
            "Lokalizacja w centrum Polski"
        ]),
        ("🔧", "Pełen Serwis", [
            "Projekt i wykonanie",
            "Transport i montaż",
            "Wsparcie posprzedażowe"
        ])
    ]
    
    for i, (icon, title, features) in enumerate(benefits):
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div class="benefit-card">
                <div style="font-size: 3rem; text-align: center; margin-bottom: 1rem;">{icon}</div>
                <h3 style="color: #1e3c72; text-align: center; margin-bottom: 1rem;">{title}</h3>
                <ul style="color: #666; line-height: 1.8;">
                    {''.join(f'<li>{feature}</li>' for feature in features)}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Enhanced contact section
    st.markdown("""
    <div class="contact-section">
        <h2 style="margin-bottom: 2rem; font-size: 2.2rem;">📞 Skontaktuj się z nami</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 2rem;">
            <div>
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📍</div>
                <h4 style="margin-bottom: 0.5rem;">Adres</h4>
                <p style="opacity: 0.9;">Kąkolewo, Polska</p>
            </div>
            <div>
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📞</div>
                <h4 style="margin-bottom: 0.5rem;">Telefon</h4>
                <p style="opacity: 0.9;">+48 XXX XXX XXX</p>
            </div>
            <div>
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">✉️</div>
                <h4 style="margin-bottom: 0.5rem;">Email</h4>
                <p style="opacity: 0.9;">info@kan-bud.pl</p>
            </div>
            <div>
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌐</div>
                <h4 style="margin-bottom: 0.5rem;">Godziny pracy</h4>
                <p style="opacity: 0.9;">Pon-Pt: 8:00-17:00</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)