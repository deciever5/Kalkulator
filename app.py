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
from utils.translations import t, get_current_language, set_language

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

    # Force reload translations when language changes
    if 'prev_language' not in st.session_state:
        st.session_state.prev_language = st.session_state.language
except Exception as e:
    st.error(f"Initialization error: {e}")
    st.stop()

# Modern header with enhanced styling and top navigation
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
.main .block-container {margin-left: 0 !important; max-width: 100% !important; padding-top: 0 !important;}
.stApp > header {display: none !important;}
.stApp [data-testid="stHeader"] {display: none !important;}

/* Remove all top padding and margins */
.block-container {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
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
    margin-top: 0rem;
    margin-bottom: 1rem;
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
</style>
""", unsafe_allow_html=True)

# Top navigation bar with language selector and login in top-right corner
col_spacer, col_lang, col_login = st.columns([4, 1.5, 0.5])

with col_lang:
    # Language selector in top-right area
    current_lang = get_current_language()
    language_options = {
        'pl': '🇵🇱 Polski',
        'en': '🇬🇧 English',
        'de': '🇩🇪 Deutsch',
        'nl': '🇳🇱 Nederlands',
        'hu': '🇭🇺 Magyar',
        'cs': '🇨🇿 Čeština'
    }

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

# Header without separator line
st.markdown(f"""
<div class="main-header">
    <div class="company-name">🏗️ KAN-BUD</div>
    <div class="company-subtitle">{t('app.subtitle')}</div>
</div>
""", unsafe_allow_html=True)

# Services are now initialized lazily when needed

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
            # Create clickable card using button with increased size
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <button onclick="window.parent.postMessage({{type: 'streamlit:click', target: '{key}_card'}}, '*')" 
                        style="width: 100%; 
                               height: 180px; 
                               background: white; 
                               border: 2px solid #e8f4f8; 
                               border-radius: 15px; 
                               cursor: pointer; 
                               transition: all 0.3s ease;
                               box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                               font-size: 16px;
                               color: #333;
                               padding: 1.5rem;"
                        onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.12)'; this.style.borderColor='#2E86AB';"
                        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.08)'; this.style.borderColor='#e8f4f8';">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">{icon}</div>
                    <div style="font-weight: bold; margin-bottom: 0.5rem; color: #1e3c72;">{title}</div>
                    <div style="color: #666; font-size: 14px;">{desc}</div>
                </button>
            </div>
            """, unsafe_allow_html=True)

            # Hidden Streamlit button for functionality
            if st.button(f"hidden_{key}", key=f"{key}_card", disabled=False):
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
            # Create clickable card using button with increased size
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <button onclick="window.parent.postMessage({{type: 'streamlit:click', target: '{key}_card'}}, '*')" 
                        style="width: 100%; 
                               height: 160px; 
                               background: white; 
                               border: 2px solid #e8f4f8; 
                               border-radius: 15px; 
                               cursor: pointer; 
                               transition: all 0.3s ease;
                               box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                               font-size: 15px;
                               color: #333;
                               padding: 1.5rem;"
                        onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.12)'; this.style.borderColor='#2E86AB';"
                        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.08)'; this.style.borderColor='#e8f4f8';">
                    <div style="font-size: 2.2rem; margin-bottom: 0.8rem;">{icon}</div>
                    <div style="font-weight: bold; margin-bottom: 0.5rem; color: #1e3c72;">{title}</div>
                    <div style="color: #666; font-size: 13px;">{desc}</div>
                </button>
            </div>
            """, unsafe_allow_html=True)

            # Hidden Streamlit button for functionality
            if st.button(f"hidden_{key}", key=f"{key}_card", disabled=False):
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
        # Create clickable card using custom HTML button
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <button onclick="window.parent.postMessage({{type: 'streamlit:click', target: 'client_config_card'}}, '*')" 
                    style="width: 100%; 
                           height: 200px; 
                           background: linear-gradient(135deg, #2E86AB 0%, #1e3c72 100%); 
                           border: none; 
                           border-radius: 15px; 
                           cursor: pointer; 
                           transition: all 0.3s ease;
                           box-shadow: 0 6px 20px rgba(46,134,171,0.3);
                           color: white;
                           font-size: 17px;
                           padding: 1.5rem;"
                    onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 10px 30px rgba(46,134,171,0.4)';"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(46,134,171,0.3)';">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📦</div>
                <div style="font-weight: bold; margin-bottom: 0.8rem; font-size: 18px;">{t('step_1_configuration')}</div>
                <div style="opacity: 0.9; font-size: 15px;">{t('choose_container_type')}</div>
            </button>
        </div>
        """, unsafe_allow_html=True)

        # Hidden Streamlit button for functionality
        if st.button("hidden_config", key="client_config_card"):
            st.switch_page("pages/1_Container_Configurator.py")

    with col2:
        # Create clickable card using custom HTML button
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <button onclick="window.parent.postMessage({{type: 'streamlit:click', target: 'client_ai_card'}}, '*')" 
                    style="width: 100%; 
                           height: 200px; 
                           background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           border: none; 
                           border-radius: 15px; 
                           cursor: pointer; 
                           transition: all 0.3s ease;
                           box-shadow: 0 6px 20px rgba(102,126,234,0.3);
                           color: white;
                           font-size: 17px;
                           padding: 1.5rem;"
                    onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 10px 30px rgba(102,126,234,0.4)';"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(102,126,234,0.3)';">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <div style="font-weight: bold; margin-bottom: 0.8rem; font-size: 18px;">{t('step_2_ai_quote')}</div>
                <div style="opacity: 0.9; font-size: 15px;">{t('get_instant_quote')}</div>
            </button>
        </div>
        """, unsafe_allow_html=True)

        # Hidden Streamlit button for functionality
        if st.button("hidden_ai", key="client_ai_card"):
            st.switch_page("pages/2_AI_Cost_Estimator.py")

# Customer services section - moved here after configuration/AI sections
if not st.session_state.employee_logged_in:
    st.markdown(f"""
    <div style="margin: 3rem 0;">
        <h2 style="text-align: center; color: #1e3c72; margin-bottom: 2rem;">
            🛠️ {t('additional_services')}
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Create clickable card using custom HTML button
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <button onclick="window.parent.postMessage({{type: 'streamlit:click', target: 'customer_drawing_analysis_card'}}, '*')" 
                    style="width: 100%; 
                           height: 180px; 
                           background: white; 
                           border: 2px solid #e8f4f8; 
                           border-radius: 15px; 
                           cursor: pointer; 
                           transition: all 0.3s ease;
                           box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                           font-size: 16px;
                           color: #333;
                           padding: 1.5rem;"
                    onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.12)'; this.style.borderColor='#2E86AB';"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.08)'; this.style.borderColor='#e8f4f8';">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📐</div>
                <div style="font-weight: bold; margin-bottom: 0.5rem; color: #1e3c72;">{t('drawing_analysis_service')}</div>
                <div style="color: #666; font-size: 14px;">{t('upload_drawings_estimate')}</div>
            </button>
        </div>
        """, unsafe_allow_html=True)

        # Hidden Streamlit button for functionality
        if st.button("hidden_drawing", key="customer_drawing_analysis_card"):
            st.switch_page("pages/9_Customer_Drawing_Analysis.py")

    with col2:
        # Create clickable card using custom HTML button
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <button onclick="window.parent.postMessage({{type: 'streamlit:click', target: 'customer_inquiry_card'}}, '*')" 
                    style="width: 100%; 
                           height: 180px; 
                           background: white; 
                           border: 2px solid #e8f4f8; 
                           border-radius: 15px; 
                           cursor: pointer; 
                           transition: all 0.3s ease;
                           box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                           font-size: 16px;
                           color: #333;
                           padding: 1.5rem;"
                    onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.12)'; this.style.borderColor='#2E86AB';"
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.08)'; this.style.borderColor='#e8f4f8';">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📧</div>
                <div style="font-weight: bold; margin-bottom: 0.5rem; color: #1e3c72;">{t('send_inquiry_service')}</div>
                <div style="color: #666; font-size: 14px;">{t('get_detailed_quote_text')}</div>
            </button>
        </div>
        """, unsafe_allow_html=True)

        # Hidden Streamlit button for functionality
        if st.button("hidden_inquiry", key="customer_inquiry_card"):
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