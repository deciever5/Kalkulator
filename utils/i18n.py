
"""
Proper Internationalization (i18n) System for Streamlit
Based on industry-standard i18n patterns
"""

import streamlit as st
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class I18nManager:
    """
    Industry-standard i18n manager for Streamlit applications
    """
    
    def __init__(self, default_locale: str = 'pl', translations_dir: str = 'locales'):
        self.default_locale = default_locale
        self.translations_dir = Path(translations_dir)
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.current_locale = default_locale
        self._load_translations()
        
    def _load_translations(self):
        """Load all translation files from the locales directory"""
        if not self.translations_dir.exists():
            self.translations_dir.mkdir(exist_ok=True)
            
        for locale_file in self.translations_dir.glob('*.json'):
            locale = locale_file.stem
            try:
                with open(locale_file, 'r', encoding='utf-8') as f:
                    self.translations[locale] = json.load(f)
            except Exception as e:
                st.error(f"Error loading translations for {locale}: {e}")
                
    def set_locale(self, locale: str):
        """Set the current locale"""
        if locale in self.translations:
            self.current_locale = locale
            st.session_state.i18n_locale = locale
        else:
            st.warning(f"Locale {locale} not found, using {self.default_locale}")
            
    def get_locale(self) -> str:
        """Get current locale from session state or default"""
        return st.session_state.get('i18n_locale', self.default_locale)
        
    def t(self, key: str, locale: Optional[str] = None, **kwargs) -> str:
        """
        Translate a key to the current or specified locale
        Supports nested keys with dot notation (e.g., 'nav.home')
        Supports interpolation with kwargs
        """
        if locale is None:
            locale = self.get_locale()
            
        # Get translation dict for locale
        translation_dict = self.translations.get(locale, {})
        
        # Handle nested keys
        keys = key.split('.')
        value = translation_dict
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                # Fallback to default locale
                value = self.translations.get(self.default_locale, {})
                for k in keys:
                    if isinstance(value, dict) and k in value:
                        value = value[k]
                    else:
                        return key  # Return key if not found
                break
                
        # If value is string, perform interpolation
        if isinstance(value, str) and kwargs:
            try:
                value = value.format(**kwargs)
            except KeyError:
                pass  # Ignore missing interpolation keys
                
        return str(value)
        
    def get_available_locales(self) -> Dict[str, str]:
        """Get available locales with their display names"""
        locale_names = {
            'en': 'English',
            'pl': 'Polski',
            'de': 'Deutsch',
            'nl': 'Nederlands'
        }
        return {k: locale_names.get(k, k) for k in self.translations.keys()}

# Global i18n instance
i18n = I18nManager()

def init_i18n():
    """Initialize i18n system"""
    if 'i18n_locale' not in st.session_state:
        st.session_state.i18n_locale = i18n.default_locale

def t(key: str, locale: Optional[str] = None, **kwargs) -> str:
    """Shorthand translation function"""
    return i18n.t(key, locale, **kwargs)

def set_locale(locale: str):
    """Set current locale"""
    i18n.set_locale(locale)

def get_locale() -> str:
    """Get current locale"""
    return i18n.get_locale()

def render_language_selector(key_suffix: str = ""):
    """Render a language selector component"""
    init_i18n()
    
    available_locales = i18n.get_available_locales()
    current_locale = get_locale()
    
    selected_locale = st.selectbox(
        t('ui.language_selector'),
        options=list(available_locales.keys()),
        format_func=lambda x: available_locales[x],
        index=list(available_locales.keys()).index(current_locale) if current_locale in available_locales else 0,
        key=f"language_selector_{key_suffix}"
    )
    
    if selected_locale != current_locale:
        set_locale(selected_locale)
        st.rerun()
