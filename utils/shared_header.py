
import streamlit as st
from utils.translations import t, get_current_language, set_language

def render_shared_header():
    """Render the shared header with language selector and login button"""
    
    # Custom CSS for the header
    st.markdown("""
    <style>
    .shared-header {
        position: fixed;
        top: 0;
        right: 0;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.95);
        padding: 0.5rem 1rem;
        border-radius: 0 0 0 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    .main-content {
        margin-top: 4rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header container
    st.markdown('<div class="shared-header">', unsafe_allow_html=True)
    
    # Create columns for language selector and login
    col_lang, col_login = st.columns([2, 1])
    
    with col_lang:
        # Language selector
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
            key="header_language_selector",
            label_visibility="collapsed"
        )
        
        if selected_language != current_lang:
            set_language(selected_language)
            st.rerun()
    
    with col_login:
        # Employee login button
        if not st.session_state.get('employee_logged_in', False):
            if st.button("👤", key="header_login_btn", help=t('ui.employee_login'), use_container_width=True):
                st.session_state.show_login = True
                st.rerun()
        else:
            if st.button("🚪", key="header_logout", help=t('ui.logout'), use_container_width=True):
                st.session_state.employee_logged_in = False
                st.session_state.show_login = False
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Employee login form
    if st.session_state.get('show_login', False) and not st.session_state.get('employee_logged_in', False):
        col_a, col_b, col_c = st.columns([2, 2, 2])
        with col_b:
            st.markdown('<div class="main-content">', unsafe_allow_html=True)
            employee_password = st.text_input(t('ui.password'), type="password", key="header_emp_pwd")
            col_x, col_y = st.columns(2)
            with col_x:
                if st.button(t('ui.login'), key="header_emp_login", use_container_width=True):
                    if employee_password == "kan-bud-employee-2024":
                        st.session_state.employee_logged_in = True
                        st.session_state.show_login = False
                        st.success(t('ui.logged_in'))
                        st.rerun()
                    else:
                        st.error(t('ui.wrong_password'))
            with col_y:
                if st.button(t('ui.cancel'), key="header_cancel_login", use_container_width=True):
                    st.session_state.show_login = False
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="main-content">', unsafe_allow_html=True)

def render_back_to_home():
    """Render back to home button"""
    if st.button(f"🏠 {t('ui.back_to_home')}", key="back_to_home_btn"):
        st.switch_page("app.py")
