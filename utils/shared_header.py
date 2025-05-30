import streamlit as st
from utils.translations import t, get_current_language, set_language

def render_shared_header():
    """Render shared header with language selector and login"""

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
            key=f"language_selector_{st.session_state.get('page_key', 'default')}",
            label_visibility="collapsed"
        )

        if selected_language != current_lang:
            print(f"Language change detected: {current_lang} -> {selected_language}")
            set_language(selected_language)
            st.rerun()

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
                        if password == "kan-bud-2024":
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