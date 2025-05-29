"""
Quick translation fix for dropdown lists and navigation
"""

import streamlit as st

# Simple translation dictionaries
TRANSLATIONS = {
    'pl': {
        # Container types
        '20ft Standard': '20ft Standard',
        '40ft Standard': '40ft Standard', 
        '40ft High Cube': '40ft Wysokościowy',
        '20ft Refrigerated': '20ft Chłodniczy',
        
        # Use cases
        'Office Space': 'Przestrzeń Biurowa',
        'Residential': 'Mieszkalne',
        'Storage': 'Magazyn',
        'Workshop': 'Warsztat',
        'Retail': 'Handel',
        'Restaurant': 'Restauracja',
        'Medical': 'Medyczne',
        'Laboratory': 'Laboratorium',
        
        # Climate zones
        'Central European': 'Europa Środkowa',
        'Scandinavian': 'Skandynawski',
        'Mediterranean': 'Śródziemnomorski',
        'Atlantic Maritime': 'Atlantycki Morski',
        'Continental': 'Kontynentalny',
        'Alpine': 'Alpejski',
        'Baltic': 'Bałtycki',
        'Temperate Oceanic': 'Umiarkowany Oceaniczny',
        
        # Environment types
        'Indoor': 'Wewnętrzne',
        'Outdoor': 'Zewnętrzne',
        'Marine': 'Morskie',
        'Industrial': 'Przemysłowe',
        
        # Navigation
        'back_to_home': '← Powrót do strony głównej',
        'ai_cost_estimation': 'Wycena AI',
        'container_configurator': 'Konfigurator Kontenerów',
        
        # Labels
        'container_type': 'Typ Kontenera',
        'main_purpose': 'Główne Przeznaczenie',
        'environment': 'Środowisko',
        'climate_zone': 'Strefa Klimatyczna',
        'language': 'Język'
    },
    'en': {
        # Keep English as default
        'back_to_home': '← Back to Home',
        'ai_cost_estimation': 'AI Cost Estimation',
        'container_configurator': 'Container Configurator',
        'container_type': 'Container Type',
        'main_purpose': 'Main Purpose',
        'environment': 'Environment',
        'climate_zone': 'Climate Zone',
        'language': 'Language'
    }
}

def quick_translate(text, language=None):
    """Quick translation function"""
    if language is None:
        language = st.session_state.get('language', 'pl')
    
    # Return translation if exists, otherwise return original text
    return TRANSLATIONS.get(language, {}).get(text, text)

def translate_dropdown_options(options, language=None):
    """Translate dropdown options"""
    if language is None:
        language = st.session_state.get('language', 'pl')
    
    return [quick_translate(option, language) for option in options]

def render_language_dropdown():
    """Render language dropdown that works everywhere"""
    language_options = {
        'pl': 'Polski',
        'en': 'English', 
        'de': 'Deutsch',
        'nl': 'Nederlands'
    }
    
    current_lang = st.session_state.get('language', 'pl')
    
    col1, col2 = st.columns([2, 4])
    with col1:
        selected = st.selectbox(
            quick_translate('language'),
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(current_lang),
            key=f"lang_select_{st.session_state.get('page_name', 'main')}"
        )
        
        if selected != current_lang:
            st.session_state.language = selected
            st.rerun()