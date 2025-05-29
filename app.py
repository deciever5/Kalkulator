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
from utils.translations import t, render_language_selector
from utils.groq_service import GroqService

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
    try:
        db = DatabaseManager()
        if db.engine:
            storage = db
        else:
            storage = SimpleStorageManager()
    except Exception as e:
        if st.session_state.get('employee_logged_in', False):
            st.error(f"Database initialization failed: {str(e)}")
        storage = SimpleStorageManager()

    container_db = ContainerDatabase()
    calc = StructuralCalculations()

    try:
        historical_service = HistoricalDataService()
    except Exception as e:
        if st.session_state.get('employee_logged_in', False):
            st.error(f"Historical data initialization: {str(e)}")
        historical_service = None

    try:
        groq_service = GroqService()
    except Exception as e:
        if st.session_state.get('employee_logged_in', False):
            st.warning(f"Groq AI service initialization: {str(e)}")
        groq_service = None

    return storage, container_db, calc, historical_service, groq_service

# Initialize language
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Language selector
render_language_selector()

# Employee authentication
if 'employee_logged_in' not in st.session_state:
    st.session_state.employee_logged_in = False

if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# Employee login button
col_spacer, col_login = st.columns([5, 1])
with col_login:
    if not st.session_state.employee_logged_in:
        if st.button("👤", key="login_toggle_btn", help=t('ui.employee_login'), use_container_width=True):
            st.session_state.show_login = True
            st.rerun()
    else:
        if st.button("🚪", key="emp_logout", help=t('ui.logout'), use_container_width=True):
            st.session_state.employee_logged_in = False
            st.session_state.show_login = False
            st.rerun()

# Employee login form
if st.session_state.show_login and not st.session_state.employee_logged_in:
    col_a, col_b, col_c = st.columns([2, 2, 2])
    with col_b:
        employee_password = st.text_input(t('ui.password'), type="password", key="emp_pwd")
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button(t('ui.login'), key="emp_login", use_container_width=True):
                if employee_password == "kan-bud-employee-2024":
                    st.session_state.employee_logged_in = True
                    st.session_state.show_login = False
                    st.success(t('ui.logged_in'))
                    st.rerun()
                else:
                    st.error(t('ui.wrong_password'))
        with col_y:
            if st.button(t('ui.cancel'), key="cancel_login", use_container_width=True):
                st.session_state.show_login = False
                st.rerun()

# Modern header with enhanced styling
st.markdown("""
<style>
/* Hide sidebar completely */
section[data-testid="stSidebar"] {display: none !important;}
.stSidebar {display: none !important;}
button[kind="header"] {display: none !important;}
button[data-testid="collapsedControl"] {display: none !important;}
.css-1d391kg {display: none !important;}
.css-1y4p8pa {margin-left: 0 !important;}
.css-17eq0hr {display: none !important;}
.css-164nlkn {margin-left: 0 !important;}
div[data-testid="stSidebarNav"] {display: none !important;}
button[data-testid="baseButton-header"] {display: none !important;}
.css-1544g2n {display: none !important;}
.css-18e3th9 {display: none !important;}
[data-testid="stSidebarCollapseButton"] {display: none !important;}
[data-testid="stSidebarUserContent"] {display: none !important;}
[data-testid="stSidebarContent"] {display: none !important;}
button[title="Open sidebar navigation"] {display: none !important;}
button[aria-label="Open sidebar navigation"] {display: none !important;}
.css-1vq4p4l {display: none !important;}
.css-1d391kg {display: none !important;}
.css-6qob1r {margin-left: 0 !important;}
.css-1cypcdb {margin-left: 0 !important;}
.css-18e3th9 {margin-left: 0 !important;}
.css-1d391kg {margin-left: 0 !important;}
.main .block-container {margin-left: 0 !important; max-width: 100% !important;}
.stApp > header {display: none !important;}
.stApp [data-testid="stHeader"] {display: none !important;}

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
</style>
""" + f"""
<div class="main-header">
    <div class="company-name">🏗️ KAN-BUD</div>
    <div class="company-subtitle">{t('app.subtitle')}</div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'container_db' not in st.session_state:
    st.session_state.container_db = ContainerDatabase()

if 'calculations' not in st.session_state:
    st.session_state.calculations = StructuralCalculations()

if 'historical_service' not in st.session_state:
    st.session_state.historical_service = HistoricalDataService()

# Initialize services
storage, container_db, calc, historical_service_init, groq_service = initialize_services()

st.markdown("---")

# Main dashboard content
if st.session_state.employee_logged_in:
    # Employee view
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1.5rem; border-radius: 15px; margin: 2rem 0; text-align: center;">
        <h2 style="margin: 0;">🔧 Employee Tools</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Full system access and advanced features</p>
    </div>
    """, unsafe_allow_html=True)

    # Primary tools
    col1, col2, col3, col4 = st.columns(4, gap="large")

    tools = [
        ("📦", t('nav.container_configurator'), "Professional container configuration", "pages/1_Container_Configurator.py", "emp_config"),
        ("🤖", t('nav.ai_cost_estimation'), "AI cost estimation", "pages/2_AI_Cost_Estimator.py", "emp_ai"), 
        ("🔧", t('nav.technical_analysis'), "Technical analysis", "pages/3_Technical_Analysis.py", "emp_tech"),
        ("📋", t('nav.quote_generator'), "Quote generator", "pages/4_Quote_Generator.py", "emp_quote")
    ]

    for i, (icon, title, desc, page, key) in enumerate(tools):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-description">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"{t('ui.open')} {title}", key=key, use_container_width=True, type="primary"):
                st.switch_page(page)

    # Secondary tools
    col5, col6, col7 = st.columns([1, 1, 1], gap="large")

    secondary_tools = [
        ("⚖️", t('nav.comparison_tool'), t('nav.comparison_tool_desc'), "pages/5_Comparison_Tool.py", "emp_compare"),
        ("📐", t('nav.drawing_analysis'), t('nav.drawing_analysis_desc'), "pages/6_Drawing_Analysis.py", "emp_draw"),
        ("🔐", t('nav.admin_panel'), t('nav.admin_panel_desc'), "pages/Admin_Panel.py", "emp_admin")
    ]

    for i, (icon, title, desc, page, key) in enumerate(secondary_tools):
        with [col5, col6, col7][i]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-description">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"{t('ui.open')} {title}", key=key, use_container_width=True):
                st.switch_page(page)

else:
    # Client view
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="color: #1e3c72; font-size: 2.5rem; margin-bottom: 0.5rem;">
            💼 {t('configure_container')}
        </h2>
        <p style="font-size: 1.3rem; color: #666; font-style: italic;">
            {t('simple_process_2_steps')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Client action cards
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
                {t('step_1_configuration')}
            </h2>
            <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 0;">
                {t('choose_container_type')}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(t('start_configuration'), key="client_config", use_container_width=True, type="primary"):
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
                {t('step_2_ai_quote')}
            </h2>
            <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 0;">
                {t('get_instant_quote')}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(t('get_quote'), key="client_ai", use_container_width=True, type="secondary"):
            st.switch_page("pages/2_AI_Cost_Estimator.py")

# Enhanced client benefits section
if not st.session_state.employee_logged_in:
    st.markdown(f"""
    <div class="benefits-section">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 2rem; font-size: 2.2rem;">
            ✨ {t('why_kan_bud')}
        </h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    benefits = [
        ("🎯", t('precise_quotes'), [
            t('ai_historical_data'),
            t('european_climate_standards'), 
            t('transparent_calculations')
        ]),
        ("⚡", t('fast_realization'), [
            t('hundreds_of_projects'),
            t('own_machinery'),
            t('poland_center')
        ]),
        ("🔧", t('full_service'), [
            t('design_execution'),
            t('transport_assembly'),
            t('after_sales_support')
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
    st.markdown(f"""
    <div class="contact-section">
        <h2 style="margin-bottom: 2rem; font-size: 2.2rem;">📞 {t('contact_us')}</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 2rem;">
            <div>
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📍</div>
                <h4 style="margin-bottom: 0.5rem;">{t('address')}</h4>
                <p style="opacity: 0.9;">Kąkolewo, Polska</p>
            </div>
            <div>
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📞</div>
                <h4 style="margin-bottom: 0.5rem;">{t('phone')}</h4>
                <p style="opacity: 0.9;">+48 XXX XXX XXX</p>
            </div>
            <div>
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">✉️</div>
                <h4 style="margin-bottom: 0.5rem;">{t('email')}</h4>
                <p style="opacity: 0.9;">info@kan-bud.pl</p>
            </div>
            <div>
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌐</div>
                <h4 style="margin-bottom: 0.5rem;">{t('working_hours')}</h4>
                <p style="opacity: 0.9;">{t('mon_fri')}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Language selector already rendered at the top