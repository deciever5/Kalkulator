import streamlit as st
import os
from utils.translations import t, get_current_language, set_language, get_available_languages, init_language

def render_shared_header(show_login=False, current_page="Home"):
    """Render shared header with consistent top navigation matching main page"""

    # Initialize language system
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

    # Top navigation bar with language selector and optional login (same as main page)
    if show_login:
        col_spacer, col_lang, col_login = st.columns([4, 1.5, 0.5])
    else:
        col_spacer, col_lang = st.columns([5, 1])

    with col_lang:
        # Language selector in top-right area (matching main page)
        current_lang = get_current_language()
        language_options = get_available_languages()

        # Create unique key for this page's language selector
        key = f"lang_selector_{current_page}"

        selected_language = st.selectbox(
            "🌐",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(current_lang),
            key=key,
            label_visibility="collapsed"
        )

        if selected_language != current_lang:
            set_language(selected_language)
            st.rerun()

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

        # Create a unique key for each page
        import time
        key = f"shared_lang_selector_{current_page}_{int(time.time()) % 10000}"

        # Ensure current language is in available options
        if current_lang not in language_options:
            current_lang = 'en'  # Default to English if current language not available
            set_language(current_lang)

    if show_login:
        with col_login:
            # Employee login button
            if st.session_state.get('employee_logged_in', False):
                if st.button("🚪", key=f"logout_btn_{current_page}", help=t('ui.logout'), use_container_width=True):
                    st.session_state.employee_logged_in = False
                    if 'show_login' in st.session_state:
                        del st.session_state.show_login
                    st.rerun()
            else:
                if st.button("👤", key=f"login_btn_{current_page}", help=t('ui.employee_login'), use_container_width=True):
                    st.session_state.show_login = not st.session_state.get('show_login', False)
                    st.rerun()

    # Employee login form (if requested and not logged in)
    if show_login and st.session_state.get('show_login', False) and not st.session_state.get('employee_logged_in', False):
        col_a, col_b, col_c = st.columns([2, 2, 2])
        with col_b:
            employee_password = st.text_input(t('ui.password'), type="password", key=f"emp_pwd_{current_page}")
            col_x, col_y = st.columns(2)
            with col_x:
                if st.button(t('ui.login'), key=f"emp_login_{current_page}", use_container_width=True):
                    if employee_password == "kan-bud-employee-2024":
                        st.session_state.employee_logged_in = True
                        st.session_state.show_login = False
                        st.success(t('ui.logged_in'))
                        st.rerun()
                    else:
                        st.error(t('ui.wrong_password'))
            with col_y:
                if st.button(t('ui.cancel'), key=f"cancel_login_{current_page}", use_container_width=True):
                    st.session_state.show_login = False
                    st.rerun()t.rerun()

    # Professional navigation header
    st.markdown("""
    <div style="background: white; border-bottom: 1px solid #e5e7eb; padding: 16px 0; margin-bottom: 24px;">
        <div style="max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 24px;">
            <div style="display: flex; align-items: center; gap: 24px;">
                <h1 style="margin: 0; font-size: 24px; font-weight: 700; color: #3b82f6;">KAN-BUD</h1>
                <div style="font-size: 14px; color: #6b7280;">
                    <span>Container Solutions</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Skip breadcrumb for pages that have their own gradient headers
    pages_with_gradient_headers = ["Container_Configurator", "AI_Cost_Estimator", "Technical_Analysis"]

    if current_page not in pages_with_gradient_headers:
        # Breadcrumb navigation for other pages
        breadcrumb_map = {
            "Home": "🏠 Home",
            "Quote_Generator": "📋 Quote Generator",
            "Comparison_Tool": "⚖️ Comparison Tool",
            "Drawing_Analysis": "📐 Drawing Analysis",
            "3D_Visualization": "🎯 3D Visualization",
            "Send_Inquiry": "📧 Send Inquiry",
            "Customer_Drawing_Analysis": "📄 Customer Analysis",
            "Bulk_Pricing": "📦 Bulk Pricing",
            "Custom_Sizing": "📐 Custom Sizing",
            "Admin_Panel": "⚙️ Admin Panel"
        }

        breadcrumb_text = breadcrumb_map.get(current_page, current_page)
        st.markdown(f"""
        <div style="margin-bottom: 16px; padding: 8px 16px; background: #f9fafb; border-radius: 8px; border-left: 4px solid #3b82f6;">
            <span style="font-size: 14px; color: #6b7280; font-weight: 500;">{breadcrumb_text}</span>
        </div>
        """, unsafe_allow_html=True)

    if show_login:
        with col_login:
            # Employee login button
            if st.session_state.get('employee_logged_in', False):
                if st.button(t('ui.logout'), key="logout_btn"):
                    st.session_state.employee_logged_in = False
                    st.session_state.show_login = False
                    st.rerun()
            else:
                if st.button(t('ui.employee_login'), key="login_btn"):
                    st.session_state.show_login = not st.session_state.get('show_login', False)
                    st.rerun()

        # Login form (if shown)
    if st.session_state.get('show_login', False) and not st.session_state.get('employee_logged_in', False):
        col_a, col_b, col_c = st.columns([2, 2, 2])
        with col_b:
            employee_password = st.text_input(t('ui.password'), type="password", key="shared_emp_pwd")
            col_x, col_y = st.columns(2)
            with col_x:
                if st.button(t('ui.login'), key="shared_emp_login", use_container_width=True):
                    if employee_password == "kan-bud-employee-2024":
                        st.session_state.employee_logged_in = True
                        st.session_state.show_login = False
                        st.success(t('ui.logged_in'))
                        st.rerun()
                    else:
                        st.error(t('ui.wrong_password'))
            with col_y:
                if st.button(t('ui.cancel'), key="shared_cancel_login", use_container_width=True):
                    st.session_state.show_login = False
                    st.rerun()

def render_back_to_home():
    """Render back to home button"""
    if st.button(t('ui.back_to_home')):
        st.switch_page("app.py")