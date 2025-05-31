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

def get_available_languages():
    """Get available languages with complete translations only"""
    # Only show languages with complete translation coverage (220+ keys)
    return {
        'cs': '🇨🇿 Čeština',
        'de': '🇩🇪 Deutsch', 
        'en': '🇬🇧 English',
        'hu': '🇭🇺 Magyar',
        'nl': '🇳🇱 Nederlands',
        'pl': '🇵🇱 Polski'
    }

def render_language_selector():
    """Render language selector dropdown with full visibility and alphabetical order"""
    current_lang = get_current_language()
    language_options = get_available_languages()

    # Custom CSS to make selectbox show all language options without scrolling
    st.markdown("""
    <style>
    /* Force language dropdown to show all 6 language options */
    div[data-baseweb="select"] > div[role="listbox"] {
        max-height: 400px !important;
        height: auto !important;
    }
    div[data-baseweb="popover"] {
        max-height: 450px !important;
    }
    div[data-baseweb="popover"] > div {
        max-height: 400px !important;
    }
    div[data-baseweb="popover"] > div > div {
        max-height: 400px !important;
        overflow-y: visible !important;
    }
    /* Target all selectbox dropdowns */
    .stSelectbox [data-baseweb="popover"] {
        max-height: 450px !important;
    }
    .stSelectbox [data-baseweb="popover"] > div {
        max-height: 400px !important;
    }
    /* Ensure enough space for all 6 languages */
    div[role="listbox"] {
        max-height: 400px !important;
        min-height: 250px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create a unique key for each page
    import time
    key = f"lang_selector_{int(time.time()) % 10000}"

    col1, col2, col3 = st.columns([4, 1.5, 0.5])

    with col2:
        # Ensure current language is in available options
        if current_lang not in language_options:
            current_lang = 'en'  # Default to English if current language not available
            set_language(current_lang)
        
        selected_language = st.selectbox(
            "🌐 Language",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(current_lang),
            key=key,
            label_visibility="collapsed"
        )

        if selected_language != current_lang:
            set_language(selected_language)
            st.rerun()

def render_language_buttons():
    """Legacy function kept for compatibility"""
    pass

def get_nested_translation(translation_data, key):
    """
    Get a translation from nested dictionary

    Args:
        translation_data: Translation dictionary
        key: Translation key, e.g. 'form.labels.container_type'
    """
    keys = key.split('.')
    result = translation_data

    for k in keys:
        if isinstance(result, dict) and k in result:
            result = result[k]
        else:
            return None
    return result if isinstance(result, str) else ""

@st.cache_data
def get_cached_translations():
    """Cache translations to avoid repeated loading"""
    return load_translations()

def t(key: str, fallback: str = None, **kwargs) -> str:
    """
    Get translation for given key in current language
    Supports nested keys like 'form.labels.container_type'
    Includes automatic fallback to English if key missing in current language

    Args:
        key: Translation key
        fallback: Fallback text if translation is missing
        **kwargs: Format parameters
    """
    lang = st.session_state.get('language', 'pl')

    try:
        # Use cached translations
        translations = get_cached_translations()
        
        # Get translation value from current language
        if lang in translations:
            translation = get_nested_translation(translations[lang], key)
            if translation:
                # Format with kwargs if provided
                if kwargs and translation:
                    return translation.format(**kwargs)
                return translation
        
        # Fallback to English if key not found in current language
        if lang != 'en' and 'en' in translations:
            english_translation = get_nested_translation(translations['en'], key)
            if english_translation:
                if kwargs and english_translation:
                    return english_translation.format(**kwargs)
                return english_translation

        # Use provided fallback
        if fallback:
            return fallback
            
        # Last resort: return the key itself
        print(f"Translation key '{key}' not found in language '{lang}' or English fallback")
        return key

    except Exception as e:
        print(f"Translation error for key '{key}': {e}")
        return fallback if fallback else key