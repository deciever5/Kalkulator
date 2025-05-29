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
                        content = f.read()
                        if content.strip():  # Check if file is not empty
                            translations[lang_code] = json.loads(content)
                        else:
                            print(f"Warning: {filename} is empty")
                except json.JSONDecodeError as e:
                    print(f"JSON decode error in {filename}: {e}")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    return translations

# Load translations once
TRANSLATIONS = load_translations()

# Debug: Print what was loaded
if TRANSLATIONS:
    print(f"Loaded translations for languages: {list(TRANSLATIONS.keys())}")
    for lang, data in TRANSLATIONS.items():
        if isinstance(data, dict) and 'app' in data:
            print(f"Language {lang} has 'app' section with keys: {list(data['app'].keys())}")
else:
    print("WARNING: No translations were loaded!")

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

    # Debug: Check what we have loaded
    if not TRANSLATIONS:
        print(f"No translations loaded! Returning key: {key}")
        return key

    # Get translation data for language
    translation_data = TRANSLATIONS.get(language, TRANSLATIONS.get('pl', {}))
    
    if not translation_data:
        print(f"No translation data for language: {language}, returning key: {key}")
        return key

    # Handle nested keys like 'ui.back_to_home'
    keys = key.split('.')
    result = translation_data

    try:
        for k in keys:
            if isinstance(result, dict) and k in result:
                result = result[k]
            else:
                # Debug output
                print(f"Key '{k}' not found in result: {result}")
                print(f"Available keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                return key

        return result if isinstance(result, str) else key
    except (KeyError, TypeError, AttributeError) as e:
        # Debug output
        print(f"Error in translation for key '{key}': {e}")
        print(f"Language: {language}")
        print(f"Translation data keys: {list(translation_data.keys()) if isinstance(translation_data, dict) else 'Not a dict'}")
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