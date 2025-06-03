import streamlit as st

# Set page config first - before any other Streamlit commands
st.set_page_config(
    page_title="KAN-BUD Professional Container Solutions",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import after page config
from utils.container_database import ContainerDatabase
from utils.calculations import StructuralCalculations
from utils.database import DatabaseManager
from utils.simple_storage import SimpleStorageManager
from utils.translations import t, init_language, get_current_language, set_language
from utils.groq_service import GroqService

# Initialize services with lazy loading
@st.cache_resource
def get_storage_service():
    """Initialize storage service only when needed"""
    try:
        db = DatabaseManager()
        return db if db.engine else SimpleStorageManager()
    except Exception:
        return SimpleStorageManager()

@st.cache_resource
def get_container_db():
    """Initialize container database only when needed"""
    return ContainerDatabase()

@st.cache_resource
def get_calculations_service():
    """Initialize calculations service only when needed"""
    return StructuralCalculations()

@st.cache_resource
def get_historical_service():
    """Initialize historical service only when needed"""
    try:
        from utils.historical_data_service import HistoricalDataService
        return HistoricalDataService()
    except Exception:
        return None

@st.cache_resource
def get_groq_service():
    """Initialize Groq service only when needed"""
    try:
        return GroqService()
    except Exception:
        return None

# Initialize session state efficiently
def init_session_state():
    """Initialize session state with default values"""
    defaults = {
        'language': 'pl',
        'employee_logged_in': False,
        'show_login': False,
        'services_initialized': False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

try:
    init_session_state()
    
    # Load animations and micro-interactions
    from utils.animations import add_hover_animations, add_page_transition
    add_hover_animations()
    add_page_transition()

    # Force reload translations when language changes
    if 'prev_language' not in st.session_state:
        st.session_state.prev_language = st.session_state.language
except Exception as e:
    st.error(f"Initialization error: {e}")
    st.stop()

# Professional UX Design System
st.markdown("""
<style>
/* KAN-BUD Design System - Professional UX Standards */
:root {
  --font-primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 20px;
  --text-2xl: 24px;
  --text-3xl: 32px;
  --space-1: 8px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;
  --space-6: 48px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
  --primary-500: #3b82f6;
  --primary-600: #2563eb;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-700: #374151;
  --gray-900: #111827;
}

/* Hide sidebar completely */
section[data-testid="stSidebar"] {display: none !important;}
.stSidebar {display: none !important;}
button[kind="header"] {display: none !important;}
button[data-testid="collapsedControl"] {display: none !important;}
.main .block-container {margin-left: 0 !important; max-width: 100% !important; padding-top: 0 !important;}
.stApp > header {display: none !important;}
.stApp [data-testid="stHeader"] {display: none !important;}

/* Base Typography Improvements */
.stApp {
    font-family: var(--font-primary) !important;
    font-size: var(--text-base) !important;
    line-height: 1.6 !important;
}

/* Heading Hierarchy */
h1, .stMarkdown h1 {
    font-size: var(--text-3xl) !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;
    margin-bottom: var(--space-3) !important;
    color: var(--gray-900) !important;
}

h2, .stMarkdown h2 {
    font-size: var(--text-2xl) !important;
    font-weight: 600 !important;
    line-height: 1.3 !important;
    margin-bottom: var(--space-2) !important;
    color: var(--gray-900) !important;
}

h3, .stMarkdown h3 {
    font-size: var(--text-lg) !important;
    font-weight: 600 !important;
    line-height: 1.4 !important;
    margin-bottom: var(--space-2) !important;
    color: var(--gray-700) !important;
}

/* Button System Improvements */
.stButton > button {
    min-height: 44px !important;
    padding: var(--space-2) var(--space-3) !important;
    border-radius: var(--radius-md) !important;
    font-size: var(--text-base) !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    border: 1px solid transparent !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--primary-500), var(--primary-600)) !important;
    color: white !important;
    box-shadow: var(--shadow-sm) !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-md) !important;
}

.stButton > button[kind="secondary"] {
    background: white !important;
    border: 1px solid var(--gray-200) !important;
    color: var(--gray-700) !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: var(--primary-500) !important;
    color: var(--primary-600) !important;
    transform: translateY(-1px) !important;
}

/* Form Input Improvements */
.stSelectbox > div > div {
    min-height: 44px !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--gray-200) !important;
    font-size: var(--text-base) !important;
}

.stNumberInput > div > div > input {
    min-height: 44px !important;
    border-radius: var(--radius-md) !important;
    font-size: var(--text-base) !important;
}

.stCheckbox {
    margin: var(--space-2) 0 !important;
}

/* Metric Cards */
.stMetric {
    background: var(--gray-50) !important;
    padding: var(--space-3) !important;
    border-radius: var(--radius-lg) !important;
    border: 1px solid var(--gray-200) !important;
    text-align: center !important;
    min-height: 100px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

.stMetric > div {
    margin: 0 !important;
}

.stMetric [data-testid="metric-value"] {
    font-size: var(--text-xl) !important;
    font-weight: 700 !important;
    color: var(--gray-900) !important;
}

.stMetric [data-testid="metric-label"] {
    font-size: var(--text-base) !important;
    color: var(--gray-700) !important;
    font-weight: 500 !important;
}

/* Table Improvements */
.stDataFrame {
    border: 1px solid var(--gray-200) !important;
    border-radius: var(--radius-lg) !important;
    overflow: hidden !important;
}

.stDataFrame table {
    font-size: var(--text-base) !important;
}

.stDataFrame th {
    background: var(--gray-50) !important;
    font-weight: 600 !important;
    padding: var(--space-2) !important;
}

.stDataFrame td {
    padding: var(--space-2) !important;
}

/* Column Layout Improvements */
.stColumns {
    gap: var(--space-3) !important;
}

/* Spacing System */
.stMarkdown {
    margin-bottom: var(--space-2) !important;
}

.section-spacing {
    margin-bottom: var(--space-6) !important;
}

/* Remove all top padding and margins */
.block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
    max-width: 1200px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: var(--space-3) !important;
    padding-right: var(--space-3) !important;
}

/* Ensure main content respects max width */
.stApp > .main {
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* Limit button widths on wide screens */
.stButton > button {
    max-width: 800px !important;
    margin: 0 auto !important;
}

/* Center navigation cards */
.main .block-container > div {
    max-width: 1200px !important;
    margin: 0 auto !important;
}

.top-nav {
    position: absolute;
    top: 1rem;
    right: 1rem;
    z-index: 1000;
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

.main-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 2rem;
    border-radius: 15px;
    margin: 0rem auto 1rem auto;
    max-width: 1200px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    position: relative;
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
    margin-bottom: 0rem;
}
.feature-card {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid #e8f4f8;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    height: 100%;
    cursor: pointer;
    margin-bottom: 1rem;
}
.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    border-color: #2E86AB;
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

/* Navigation card improvements */
.nav-card {
    background: white;
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-lg);
    padding: var(--space-3);
    margin: var(--space-2) 0;
    transition: all 0.3s ease;
    cursor: pointer;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
}

.nav-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
    border-color: var(--primary-500);
}

/* Custom button styling */
.stButton > button {
    min-height: 44px !important;
    white-space: pre-line !important;
    font-size: var(--text-base) !important;
    border: 1px solid var(--gray-200) !important;
    border-radius: var(--radius-lg) !important;
    background: white !important;
    color: #333 !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.12) !important;
    border-color: #2E86AB !important;
}

/* Special styling for primary action buttons */
div[data-testid="column"]:nth-child(1) .stButton > button,
div[data-testid="column"]:nth-child(2) .stButton > button {
    height: 2080px !important;
    color: white !important;
    font-weight: bold !important;
}

/* First column button (config) */
div[data-testid="column"]:nth-child(1) .stButton > button {
    background: linear-gradient(135deg, #2E86AB 0%, #1e3c72 100%) !important;
    border: none !important;
    box-shadow: 0 6px 20px rgba(46,134,171,0.3) !important;
}

div[data-testid="column"]:nth-child(1) .stButton > button:hover {
    box-shadow: 0 10px 30px rgba(46,134,171,0.4) !important;
}

/* Second column button (AI) */
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    box-shadow: 0 6px 20px rgba(102,126,234,0.3) !important;
}

div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    box-shadow: 0 10px 30px rgba(102,126,234,0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# Top navigation bar with language selector and login in top-right corner
col_spacer, col_lang, col_login = st.columns([4, 1.5, 0.5])

with col_lang:
    # Language selector in top-right area
    current_lang = get_current_language()
    # Language options in alphabetical order by country name
    language_options = {
        'cs': '🇨🇿 Čeština',
        'de': '🇩🇪 Deutsch', 
        'en': '🇬🇧 English',
        'es': '🇪🇸 Español',
        'fi': '🇫🇮 Suomi',
        'fr': '🇫🇷 Français',
        'hu': '🇭🇺 Magyar',
        'it': '🇮🇹 Italiano',
        'nl': '🇳🇱 Nederlands',
        'pl': '🇵🇱 Polski',
        'sk': '🇸🇰 Slovenčina',
        'sv': '🇸🇪 Svenska',
        'uk': '🇺🇦 Українська'
    }

    # Initialize language system first
    init_language()
    
    # Custom CSS to make selectbox show all options without scrolling
    st.markdown("""
    <style>
    /* Force language dropdown to show all 13 options */
    div[data-baseweb="select"] > div[role="listbox"] {
        max-height: 650px !important;
        height: auto !important;
    }
    div[data-baseweb="popover"] {
        max-height: 700px !important;
    }
    div[data-baseweb="popover"] > div {
        max-height: 650px !important;
    }
    div[data-baseweb="popover"] > div > div {
        max-height: 650px !important;
        overflow-y: visible !important;
    }
    /* Target all selectbox dropdowns */
    .stSelectbox [data-baseweb="popover"] {
        max-height: 700px !important;
    }
    .stSelectbox [data-baseweb="popover"] > div {
        max-height: 650px !important;
    }
    /* Ensure enough space for all 13 languages */
    div[role="listbox"] {
        max-height: 650px !important;
        min-height: 400px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    selected_language = st.selectbox(
        "🌐",
        options=list(language_options.keys()),
        format_func=lambda x: language_options[x],
        index=list(language_options.keys()).index(current_lang),
        key="top_language_selector",
        label_visibility="collapsed"
    )

    if selected_language != current_lang:
        set_language(selected_language)
        st.session_state.prev_language = selected_language
        st.rerun()

# Check if language changed and force refresh translations
if st.session_state.get('prev_language') != get_current_language():
    st.session_state.prev_language = get_current_language()
    st.rerun()

# Check if it's the main page before rendering the login button
import os
current_file = os.path.basename(__file__)
is_main_page = current_file == "app.py"

with col_login:
    # Employee login button in top-right corner, only on main page
    if is_main_page:
        if not st.session_state.employee_logged_in:
            if st.button("👤", key="login_toggle_btn", help=t('ui.employee_login'), use_container_width=True):
                st.session_state.show_login = not st.session_state.get('show_login', False)
                st.rerun()
        else:
            if st.button("🚪", key="emp_logout", help=t('ui.logout'), use_container_width=True):
                st.session_state.employee_logged_in = False
                if 'show_login' in st.session_state:
                    del st.session_state.show_login
                st.rerun()

# Employee login form
if st.session_state.show_login and not st.session_state.employee_logged_in:
    col_a, col_b, col_c = st.columns([2, 2, 2])
    with col_b:
        employee_password = st.text_input(t('ui.password'), type="password", key="emp_pwd")
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button(t('ui.login'), key="emp_login", use_container_width=True):
                import os
                if employee_password == os.getenv("EMPLOYEE_PASSWORD", "default-change-me"):
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

# Header without separator line
st.markdown(f"""
<div class="main-header">
    <div class="company-name">🏗️ KAN-BUD</div>
    <div class="company-subtitle">{t('app.subtitle')}</div>
</div>
""", unsafe_allow_html=True)

# Services are now initialized lazily when needed

# Interactive navigation cards with gradient styling
st.markdown("""
<style>


/* Enhanced button styling for navigation cards */
.stButton > button {
    background: white !important;
    border: 2px solid #e8f4f8 !important;
    color: #333 !important;
    padding: 2rem !important;
    text-align: center !important;
    border-radius: 15px !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08) !important;
    transition: all 0.3s ease !important;
    min-height: 150px !important;
}

/* Gradient styling for specific navigation buttons */
div[data-testid="column"]:nth-child(1) .stButton > button {
    background: linear-gradient(135deg, #2E86AB 0%, #1e3c72 100%) !important;
    color: white !important;
    border: none !important;
}

div[data-testid="column"]:nth-child(2) .stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
}

/* Customer service buttons */
div[data-testid="column"]:nth-child(3) .stButton > button {
    background: linear-gradient(135deg, #A23B72 0%, #2E86AB 100%) !important;
    color: white !important;
    border: none !important;
}

div[data-testid="column"]:nth-child(4) .stButton > button {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    color: white !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

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
            # Create clickable card using Streamlit button
            if st.button(
                f"{icon}\n\n**{title}**\n\n{desc}",
                key=f"{key}_card",
                use_container_width=True,
                help=f"Click to open {title}"
            ):
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
            # Create clickable card using Streamlit button
            if st.button(
                f"{icon}\n\n**{title}**\n\n{desc}",
                key=f"{key}_card",
                use_container_width=True,
                help=f"Click to open {title}"
            ):
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

    # Main navigation grid with working buttons
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        if st.button(f"📦 {t('step_1_configuration')}\n\n{t('choose_container_type')}", key="config_nav", use_container_width=True):
            st.switch_page("pages/1_Container_Configurator.py")
    
    with col2:
        if st.button(f"🤖 {t('step_2_ai_quote')}\n\n{t('get_instant_quote')}", key="ai_nav", use_container_width=True):
            st.switch_page("pages/2_AI_Cost_Estimator.py")

# Customer services section with working buttons
if not st.session_state.employee_logged_in:
    col3, col4 = st.columns(2, gap="large")
    
    with col3:
        if st.button(f"📐 {t('drawing_analysis_service')}\n\n{t('upload_drawings_estimate')}", key="drawing_nav", use_container_width=True):
            st.switch_page("pages/9_Customer_Drawing_Analysis.py")
    
    with col4:
        if st.button(f"📧 {t('send_inquiry_service')}\n\n{t('get_detailed_quote_text')}", key="inquiry_nav", use_container_width=True):
            st.switch_page("pages/8_Send_Inquiry.py")

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



# Employee tools section
if st.session_state.employee_logged_in:
    pass

# Language selector already rendered at the top