"""
Global Language Management System
Ensures consistent language settings across all pages
"""

import streamlit as st
from utils.complete_translations import get_translation, translate_options

def init_language():
    """Initialize language settings globally"""
    if 'language' not in st.session_state:
        st.session_state.language = 'pl'  # Default to Polish

def get_current_language():
    """Get current language with fallback"""
    return st.session_state.get('language', 'pl')

def set_language(language_code):
    """Set language globally"""
    st.session_state.language = language_code

def render_language_selector():
    """Render language selector that works on all pages"""
    init_language()
    
    language_options = {
        'en': 'English',
        'pl': 'Polski', 
        'de': 'Deutsch',
        'nl': 'Nederlands'
    }
    
    current_lang = get_current_language()
    
    col_lang, col_spacer = st.columns([2, 4])
    
    with col_lang:
        selected_language = st.selectbox(
            "Language / Język:",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(current_lang),
            key=f"language_selector_{st.session_state.get('page_key', 'main')}"
        )
        
        if selected_language != current_lang:
            set_language(selected_language)
            st.rerun()

def t(key, language=None):
    """Shorthand translation function"""
    if language is None:
        language = get_current_language()
    return get_translation(key, language)

def translate_list(items, language=None):
    """Translate a list of items"""
    if language is None:
        language = get_current_language()
    return translate_options(items, language)