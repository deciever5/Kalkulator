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
    print(f"Setting language to: {lang_code}")
    st.session_state.language = lang_code
    
    # Clear the translation cache completely
    if hasattr(load_translations, 'clear'):
        load_translations.clear()
    
    # Force complete reload of translations
    global TRANSLATIONS
    TRANSLATIONS = load_translations()
    
    print(f"Available languages after reload: {list(TRANSLATIONS.keys())}")
    
    # Verify the language data is loaded
    if lang_code in TRANSLATIONS:
        print(f"Successfully loaded {lang_code} translations with {len(TRANSLATIONS[lang_code])} top-level keys")
        # Check for a common key to verify the translation is working
        test_key = "ui.language_selector"
        test_result = t(test_key, lang_code)
        print(f"Test translation for '{test_key}': {test_result}")
    else:
        print(f"ERROR: {lang_code} translations not found!")
        print(f"Translation files should be in locales/{lang_code}.json")

def t(key, language=None):
    """Translate text key using nested key access (e.g., 'ui.back_to_home')"""
    if language is None:
        language = get_current_language()

    # Refresh translations to ensure we have the latest
    translations = get_translations()
    
    # Get translation data for requested language - must exist
    translation_data = translations.get(language)
    
    if not translation_data:
        print(f"ERROR: Language '{language}' not found in translations!")
        print(f"Available languages: {list(translations.keys())}")
        # Only fallback if the language file doesn't exist at all
        translation_data = translations.get('en', translations.get('pl', {}))
        if not translation_data:
            return key

    # Handle nested keys like 'ui.back_to_home'
    keys = key.split('.')
    result = translation_data

    # Navigate through the nested structure
    for k in keys:
        if isinstance(result, dict) and k in result:
            result = result[k]
        else:
            # Only use fallback if key is completely missing from the language file
            # This should rarely happen since translation files should be complete
            for fallback_lang in ['en', 'pl']:
                if fallback_lang != language and fallback_lang in translations:
                    fallback_data = translations[fallback_lang]
                    fallback_result = fallback_data
                    
                    # Try to find the key in fallback language
                    fallback_found = True
                    for fk in keys:
                        if isinstance(fallback_result, dict) and fk in fallback_result:
                            fallback_result = fallback_result[fk]
                        else:
                            fallback_found = False
                            break
                    
                    if fallback_found and isinstance(fallback_result, str):
                        print(f"WARNING: Key '{key}' missing from {language}, using {fallback_lang}")
                        return fallback_result
            
            # If no fallback found, return the key itself
            print(f"Translation key not found: {key}")
            return key

    # Return the result if it's a string
    return result if isinstance(result, str) else key

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