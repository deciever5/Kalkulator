"""
Auto-Translator Module for KAN-BUD Container Calculator
Automatically translates all hardcoded text strings throughout the application
"""

import streamlit as st
from utils.translations import get_text

class AutoTranslator:
    """Centralized translation system for all application texts"""
    
    def __init__(self):
        self.translations_map = {
            # Navigation buttons
            "← Powrót do strony głównej": "back_to_home",
            "🤖 Przejdź do Wyceny AI →": "go_to_ai_estimate",
            "🔧 Przejdź do Konfiguratora": "go_to_configurator",
            
            # Container Configurator
            "Typ Kontenera": "container_type",
            "Główne Przeznaczenie": "main_purpose", 
            "Środowisko": "environment",
            "Indoor": "indoor",
            "Outdoor": "outdoor", 
            "Marine": "marine",
            "Industrial": "industrial",
            "🏗️ Modyfikacje Strukturalne": "structural_modifications",
            "🔨 Wzmocnienia Konstrukcyjne": "structural_reinforcements",
            "Poziom Wykończenia": "finish_level",
            "Basic": "basic",
            "Standard": "standard", 
            "Premium": "premium",
            "Luxury": "luxury",
            "Podłogi": "flooring",
            "Plywood": "plywood",
            "Vinyl": "vinyl",
            "Carpet": "carpet",
            "Hardwood": "hardwood",
            "Polished Concrete": "polished_concrete",
            
            # Configuration Summary  
            "Configuration Summary": "configuration_summary",
            "Base Container": "base_container",
            "Type": "type",
            "Use Case": "use_case", 
            "Occupancy": "occupancy",
            "people": "people",
            "Key Modifications": "key_modifications",
            
            # Use cases
            "Office Space": "office_space",
            "Residential": "residential",
            "Storage": "storage",
            "Workshop": "workshop", 
            "Retail": "retail",
            "Restaurant": "restaurant",
            "Medical": "medical",
            "Laboratory": "laboratory",
            
            # Admin Panel
            "🔐 Admin Access Required": "admin_access_required",
            "Enter admin password:": "enter_admin_password",
            "🛠️ KAN-BUD Admin Panel": "kan_bud_admin_panel",
            "*Business Configuration & Data Management*": "business_config_data_mgmt",
            "Labor and Operating Costs": "labor_operating_costs",
            "Labor Rates (€/hour)": "labor_rates_per_hour",
            "Operating Costs": "operating_costs",
            "Profit Margins & Pricing Strategy": "profit_margins_pricing",
            "Materials Margins": "materials_margins",
            "Service Categories": "service_categories",
            "Pricing Rules": "pricing_rules",
            "**Volume Discounts**": "volume_discounts",
            "**Seasonal Adjustments**": "seasonal_adjustments",
            "Historical Data Management": "historical_data_management",
            "📤 Import Historical Project Data": "import_historical_project_data",
            "📊 Historical Data Statistics": "historical_data_statistics",
            "⚠️ Danger Zone": "danger_zone",
            "User Management": "user_management",
            "Active Users & Sessions": "active_users_sessions",
            "Access Control": "access_control",
        }
    
    def t(self, text_key_or_hardcoded: str, language: str = None) -> str:
        """
        Translate text - works with both translation keys and hardcoded text
        Args:
            text_key_or_hardcoded: Either a translation key or hardcoded text
            language: Target language (defaults to session state)
        Returns:
            Translated text
        """
        if language is None:
            language = getattr(st.session_state, 'language', 'pl')
        
        # If it's a hardcoded text, find its translation key
        if text_key_or_hardcoded in self.translations_map:
            translation_key = self.translations_map[text_key_or_hardcoded]
            return get_text(translation_key, language)
        
        # If it's already a translation key, use it directly
        return get_text(text_key_or_hardcoded, language)
    
    def apply_translations(self):
        """Apply translations to current page automatically"""
        if 'language' not in st.session_state:
            st.session_state.language = 'pl'
        
        return self.t

# Global translator instance
translator = AutoTranslator()
t = translator.t  # Short alias for easy use