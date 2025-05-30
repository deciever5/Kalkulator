
"""
The code is modified to use CDN flag images for language buttons.
"""
import streamlit as st
import json
import os

def load_translations():
    """Load all translation files without caching"""
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
                    print(f"Loaded {lang_code} translations with {len(translations[lang_code])} top-level keys")
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Error loading {filename}: {e}")
            continue

    print(f"Total languages loaded: {list(translations.keys())}")
    return translations

def get_translations():
    """Get translations - always load fresh"""
    return load_translations()

def init_language():
    """Initialize language system"""
    if 'language' not in st.session_state:
        st.session_state.language = 'pl'

def get_current_language():
    """Get current language"""
    return st.session_state.get('language', 'pl')

def set_language(lang_code):
    """Set current language"""
    print(f"Setting language to: {lang_code}")
    st.session_state.language = lang_code
    
    # Verify the language change was successful
    current = get_current_language()
    print(f"Language successfully set to: {current}")

def t(key, language=None):
    """Translate text key using nested key access (e.g., 'ui.back_to_home')"""
    if language is None:
        language = get_current_language()

    # Always get fresh translations
    translations = get_translations()
    
    print(f"Translating '{key}' for language '{language}'")
    print(f"Available languages: {list(translations.keys())}")
    
    # Get translation data for requested language
    translation_data = translations.get(language)
    
    if not translation_data:
        print(f"ERROR: Language '{language}' not found in translations!")
        # Use English as fallback, then Polish
        translation_data = translations.get('en', translations.get('pl', {}))
        if not translation_data:
            print(f"ERROR: No fallback translations found!")
            return key

    # Handle nested keys like 'ui.back_to_home'
    keys = key.split('.')
    result = translation_data

    # Navigate through the nested structure
    for i, k in enumerate(keys):
        if isinstance(result, dict) and k in result:
            result = result[k]
        else:
            print(f"Key '{k}' not found at level {i} in {language} translations")
            print(f"Available keys at this level: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            
            # Try fallback languages
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
                        print(f"Using fallback {fallback_lang} for '{key}': {fallback_result}")
                        return fallback_result
            
            # If no fallback found, return the key itself
            print(f"Translation key not found: {key}")
            return key

    # Return the result if it's a string
    final_result = result if isinstance(result, str) else key
    print(f"Translation result for '{key}': {final_result}")
    return final_result

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
