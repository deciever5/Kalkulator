
"""
Unified translation utility for KAN-BUD Container Calculator
"""

import streamlit as st
from utils.complete_translations_fixed import get_translation, get_available_languages

def t(key: str) -> str:
    """Get translation for current language"""
    current_language = st.session_state.get('language', 'pl')
    return get_translation(key, current_language)

def render_language_selector():
    """Render language selector buttons"""
    st.markdown("""
    <div style="position: fixed; top: 10px; right: 20px; z-index: 999; background: white; padding: 10px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🇵🇱", help="Polski"):
            st.session_state.language = 'pl'
            st.rerun()
    with col2:
        if st.button("🇬🇧", help="English"):
            st.session_state.language = 'en'
            st.rerun()
    with col3:
        if st.button("🇩🇪", help="Deutsch"):
            st.session_state.language = 'de'
            st.rerun()
    with col4:
        if st.button("🇳🇱", help="Nederlands"):
            st.session_state.language = 'nl'
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
