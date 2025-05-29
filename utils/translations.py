"""
Clean i18n Translation System for KAN-BUD Container Calculator
Uses JSON files in locales/ directory for translations
"""

import streamlit as st
import json
import os

@st.cache_data
def load_translations():
    """Load all translation files with caching"""
    translations = {}
    locales_dir = "locales"

    if not os.path.exists(locales_dir):
        return translations

    for filename in os.listdir(locales_dir):
        if not filename.endswith('.json'):
            continue
            
        lang_code = filename[:-5]  # Remove .json extension
        file_path = os.path.join(locales_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    translations[lang_code] = json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Error loading {filename}: {e}")
            continue

    return translations

# Load translations with caching
def get_translations():
    """Get translations with lazy loading"""
    return load_translations()

TRANSLATIONS = get_translations()

# Translations loaded successfully

def init_language():
    """Initialize language system"""
    if 'language' not in st.session_state:
        st.session_state.language = 'pl'

def get_current_language():
    """Get current language"""
    return st.session_state.get('language', 'pl')

def set_language(lang_code):
    """Set current language"""
    st.session_state.language = lang_code

def t(key, language=None):
    """Translate text key using nested key access (e.g., 'ui.back_to_home')"""
    if language is None:
        language = get_current_language()

    # Get translation data for language
    translation_data = TRANSLATIONS.get(language, TRANSLATIONS.get('pl', {}))
    
    if not translation_data:
        return key

    # Handle nested keys like 'ui.back_to_home'
    keys = key.split('.')
    result = translation_data

    try:
        for k in keys:
            if isinstance(result, dict) and k in result:
                result = result[k]
            else:
                return key

        return result if isinstance(result, str) else key
    except (KeyError, TypeError, AttributeError):
        return key

def get_available_languages():
    """Get available languages"""
    return {
        'pl': '🇵🇱 Polski',
        'en': '🇬🇧 English', 
        'de': '🇩🇪 Deutsch',
        'nl': '🇳🇱 Nederlands'
    }

def render_language_selector():
    """Render language selector with flags only"""
    init_language()

    current_lang = get_current_language()

    # Create compact flag-only buttons for language selection in one row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🇵🇱", key="lang_pl", help="Polski", use_container_width=True):
            if current_lang != 'pl':
                set_language('pl')
                st.rerun()
    
    with col2:
        if st.button("🇬🇧", key="lang_en", help="English", use_container_width=True):
            if current_lang != 'en':
                set_language('en')
                st.rerun()
    
    with col3:
        if st.button("🇩🇪", key="lang_de", help="Deutsch", use_container_width=True):
            if current_lang != 'de':
                set_language('de')
                st.rerun()
    
    with col4:
        if st.button("🇳🇱", key="lang_nl", help="Nederlands", use_container_width=True):
            if current_lang != 'nl':
                set_language('nl')
                st.rerun()