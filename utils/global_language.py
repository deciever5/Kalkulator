"""
Global language management for KAN-BUD Container Calculator
Handles language state across the application
"""

import streamlit as st

def get_current_language():
    """Get current language from session state"""
    if 'language' not in st.session_state:
        st.session_state.language = 'pl'  # Default to Polish
    return st.session_state.language

def set_language(language_code):
    """Set current language in session state"""
    st.session_state.language = language_code

def get_available_languages():
    """Get list of available language codes"""
    return ['pl', 'en', 'de', 'nl']