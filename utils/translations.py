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
    # Clear the translation cache to force reload
    load_translations.clear()
    # Force reload of translations
    global TRANSLATIONS
    TRANSLATIONS = load_translations()
    print(f"Available languages after reload: {list(TRANSLATIONS.keys())}")
    
    # Verify the language data is loaded
    if lang_code in TRANSLATIONS:
        print(f"Successfully loaded {lang_code} translations")
    else:
        print(f"Warning: {lang_code} translations not found!")

def t(key, language=None):
    """Translate text key using nested key access (e.g., 'ui.back_to_home')"""
    if language is None:
        language = get_current_language()

    # Refresh translations to ensure we have the latest
    translations = get_translations()
    
    # Debug: Print available languages
    print(f"Available languages: {list(translations.keys())}")
    print(f"Requested language: {language}")
    
    # Get translation data for requested language
    translation_data = translations.get(language)
    
    if not translation_data:
        print(f"No translation data found for language: {language}")
        # Only fallback if the requested language truly doesn't exist
        translation_data = translations.get('en', translations.get('pl', {}))
        if not translation_data:
            print(f"No fallback translation data found")
            return key

    # Handle nested keys like 'ui.back_to_home'
    keys = key.split('.')
    result = translation_data

    # First try to get the key from the requested language
    try:
        for k in keys:
            if isinstance(result, dict) and k in result:
                result = result[k]
            else:
                # Key not found in requested language, try fallbacks
                print(f"Key '{k}' not found in {language} for path: {key}")
                
                # Try fallback languages only for missing specific keys
                for fallback_lang in ['en', 'pl']:
                    if fallback_lang != language and fallback_lang in translations:
                        fallback_data = translations[fallback_lang]
                        fallback_result = fallback_data
                        
                        # Navigate to the same key path in fallback language
                        key_found = True
                        for fk in keys:
                            if isinstance(fallback_result, dict) and fk in fallback_result:
                                fallback_result = fallback_result[fk]
                            else:
                                key_found = False
                                break
                        
                        if key_found and isinstance(fallback_result, str):
                            print(f"Using fallback {fallback_lang} for key: {key}")
                            return fallback_result
                
                print(f"Translation key not found: {key} in any language")
                return key

        # Return the result if it's a string
        if isinstance(result, str):
            print(f"Found translation for {key} in {language}: {result[:50]}...")
            return result
        else:
            print(f"Translation result is not a string for key: {key}")
            return key
            
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