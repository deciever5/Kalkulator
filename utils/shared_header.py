import streamlit as st
import os
from utils.translations import t, get_current_language, set_language

def render_shared_header(show_login=False, current_page="Home"):
    """Render shared header with improved navigation and breadcrumbs"""
    
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
    
    # Breadcrumb navigation
    breadcrumb_map = {
        "Home": "🏠 Home",
        "Container_Configurator": "📦 Container Configurator", 
        "AI_Cost_Estimator": "🤖 AI Cost Estimator",
        "Technical_Analysis": "🔧 Technical Analysis",
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

    # Top navigation bar with language selector and optional login
    if show_login:
        col_spacer, col_lang, col_login = st.columns([4, 1.5, 0.5])
    else:
        col_spacer, col_lang = st.columns([5, 1])

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
            key=f"language_selector_{st.session_state.get('page_key', 'default')}",
            label_visibility="collapsed"
        )

        if selected_language != current_lang:
            print(f"Language change detected: {current_lang} -> {selected_language}")
            set_language(selected_language)
            st.rerun()

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
            with st.container():
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"### {t('ui.employee_login')}")
                    password = st.text_input(t('ui.password'), type="password", key="employee_password")

                    col_login, col_cancel = st.columns(2)
                    with col_login:
                        if st.button(t('ui.login'), use_container_width=True):
                            # Get password from environment variable for security
                            admin_password = os.getenv('ADMIN_PASSWORD', 'kan-bud-2024')
                            if password == admin_password:
                                st.session_state.employee_logged_in = True
                                st.session_state.show_login = False
                                st.success(t('ui.logged_in'))
                                st.rerun()
                            else:
                                st.error(t('ui.wrong_password'))

                    with col_cancel:
                        if st.button(t('ui.cancel'), use_container_width=True):
                            st.session_state.show_login = False
                            st.rerun()

def render_back_to_home():
    """Render back to home button"""
    if st.button(t('ui.back_to_home')):
        st.switch_page("app.py")