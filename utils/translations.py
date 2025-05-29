"""
Clean i18n Translation System for KAN-BUD Container Calculator
Uses JSON files in locales/ directory for translations
"""

import streamlit as st
import json
import os

def load_translations():
    """Load all translation files"""
    translations = {}
    locales_dir = "locales"

    if os.path.exists(locales_dir):
        for filename in os.listdir(locales_dir):
            if filename.endswith('.json'):
                lang_code = filename[:-5]  # Remove .json extension
                try:
                    with open(os.path.join(locales_dir, filename), 'r', encoding='utf-8') as f:
                        translations[lang_code] = json.load(f)
                except Exception as e:
                    st.error(f"Error loading {filename}: {e}")

    return translations

# Load translations once
TRANSLATIONS = load_translations()

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
                # Return key if translation not found
                return key

        return result if isinstance(result, str) else key
    except (KeyError, TypeError, AttributeError):
        # Return the key if any error occurs during translation
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
    """Render language selector with flags"""
    init_language()

    language_options = get_available_languages()
    current_lang = get_current_language()

    # Create columns for language selector
    col1, col2 = st.columns([2, 4])
    with col1:
        selected = st.selectbox(
            t('ui.language_selector'),
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(current_lang),
            key="lang_selector"
        )

        if selected != current_lang:
            set_language(selected)
            st.rerun()