import streamlit as st
from utils.translations import t, get_current_language, set_language

def render_shared_header():
    """Render the shared header with language selector and login button matching main page style"""

    # Custom CSS for unified header style
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
            'nl': '🇳🇱 Nederlands'
        }

        selected_language = st.selectbox(
            "🌐",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(current_lang),
            key="page_language_selector",
            label_visibility="collapsed"
        )

        if selected_language != current_lang:
            set_language(selected_language)
            st.rerun()

    with col_login:
        # Employee login button in top-right corner
        if not st.session_state.get('employee_logged_in', False):
            if st.button("👤", key="page_login_toggle_btn", help=t('ui.employee_login'), use_container_width=True):
                st.session_state.show_login = True
                st.rerun()
        else:
            if st.button("🚪", key="page_emp_logout", help=t('ui.logout'), use_container_width=True):
                st.session_state.employee_logged_in = False
                st.session_state.show_login = False
                st.rerun()

    # Employee login form
    if st.session_state.get('show_login', False) and not st.session_state.get('employee_logged_in', False):
        col_a, col_b, col_c = st.columns([2, 2, 2])
        with col_b:
            employee_password = st.text_input(t('ui.password'), type="password", key="page_emp_pwd")
            col_x, col_y = st.columns(2)
            with col_x:
                if st.button(t('ui.login'), key="page_emp_login", use_container_width=True):
                    if employee_password == "kan-bud-employee-2024":
                        st.session_state.employee_logged_in = True
                        st.session_state.show_login = False
                        st.success(t('ui.logged_in'))
                        st.rerun()
                    else:
                        st.error(t('ui.wrong_password'))
            with col_y:
                if st.button(t('ui.cancel'), key="page_cancel_login", use_container_width=True):
                    st.session_state.show_login = False
                    st.rerun()

def render_back_to_home():
    """Render back to home button"""
    if st.button(f"🏠 {t('ui.back_to_home')}", key="back_to_home_btn"):
        st.switch_page("app.py")