"""
The code is modified to use CDN flag images for language buttons.
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
    """Set current language and clear cache"""
    st.session_state.language = lang_code
    # Clear the translation cache to force reload
    load_translations.clear()
    # Force reload of translations
    global TRANSLATIONS
    TRANSLATIONS = load_translations()

def t(key, language=None):
    """Translate text key using nested key access (e.g., 'ui.back_to_home')"""
    if language is None:
        language = get_current_language()

    # Refresh translations to ensure we have the latest
    translations = get_translations()
    
    # Get translation data for language - try exact match first
    translation_data = translations.get(language)
    
    # If no exact match, try fallback chain: requested -> en -> pl
    if not translation_data:
        print(f"No translation data found for language: {language}, trying fallbacks")
        translation_data = translations.get('en', translations.get('pl', {}))

    if not translation_data:
        print(f"No translation data found for any language")
        return key

    # Handle nested keys like 'ui.back_to_home'
    keys = key.split('.')
    result = translation_data

    try:
        for k in keys:
            if isinstance(result, dict) and k in result:
                result = result[k]
            else:
                # Try fallback languages for missing keys
                for fallback_lang in ['en', 'pl']:
                    if fallback_lang != language and fallback_lang in translations:
                        fallback_data = translations[fallback_lang]
                        fallback_result = fallback_data
                        try:
                            for fk in keys:
                                if isinstance(fallback_result, dict) and fk in fallback_result:
                                    fallback_result = fallback_result[fk]
                                else:
                                    fallback_result = None
                                    break
                            if fallback_result and isinstance(fallback_result, str):
                                print(f"Translation key {key} not found in {language}, using {fallback_lang}: {fallback_result}")
                                return fallback_result
                        except:
                            continue
                print(f"Translation key not found: {key} (missing: {k}) in any language")
                return key

        return result if isinstance(result, str) else key
    except (KeyError, TypeError, AttributeError) as e:
        print(f"Translation error for key {key}: {e}")
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
    """Language selector is now handled in main app navigation - this function kept for compatibility"""
    pass