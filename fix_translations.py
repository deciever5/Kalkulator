"""
Translation Coverage Fix Script
Ensures all language files have complete key coverage based on the most complete reference file
"""

import json
import os
from typing import Dict, Set, Any

def load_json_file(filepath: str) -> Dict[str, Any]:
    """Load JSON translation file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def get_all_keys(data: Dict[str, Any], prefix: str = "") -> Set[str]:
    """Recursively get all keys from nested dictionary"""
    keys = set()
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        keys.add(full_key)
        if isinstance(value, dict):
            keys.update(get_all_keys(value, full_key))
    return keys

def set_nested_value(data: Dict[str, Any], key_path: str, value: str):
    """Set value in nested dictionary using dot notation"""
    keys = key_path.split('.')
    current = data
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value

def get_nested_value(data: Dict[str, Any], key_path: str) -> str:
    """Get value from nested dictionary using dot notation"""
    keys = key_path.split('.')
    current = data
    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return ""

def fix_translation_coverage():
    """Fix translation coverage across all language files"""
    
    # Language files to process
    languages = ['en', 'de', 'nl', 'cs', 'hu', 'pl']
    
    # Load all translation files
    translations = {}
    for lang in languages:
        filepath = f'locales/{lang}.json'
        translations[lang] = load_json_file(filepath)
    
    # Find the most complete set of keys (usually Polish has the most)
    all_keys_by_lang = {}
    for lang in languages:
        all_keys_by_lang[lang] = get_all_keys(translations[lang])
    
    # Get union of all keys to ensure complete coverage
    master_keys = set()
    for keys in all_keys_by_lang.values():
        master_keys.update(keys)
    
    print(f"Total unique keys found: {len(master_keys)}")
    
    # Key mappings for comprehensive configuration (based on Polish file)
    additional_keys = {
        # Basic Configuration
        "construction_material": "Construction Material",
        "construction_material_steel": "Steel",
        "construction_material_aluminum": "Aluminum", 
        "construction_material_composite": "Composite",
        
        "insulation": "Insulation",
        "insulation_basic": "Basic (50mm)",
        "insulation_standard": "Standard (100mm)",
        "insulation_premium": "Premium (150mm)",
        "insulation_none": "None",
        
        # Systems & Installations
        "lighting": "Lighting",
        "lighting_basic": "Basic LED",
        "lighting_professional": "Professional",
        "lighting_none": "None",
        
        "ventilation": "Ventilation",
        "ventilation_natural": "Natural",
        "ventilation_forced": "Forced Air",
        "ventilation_hvac": "Full HVAC",
        
        "roof_modifications": "Roof Modifications",
        "roof_modifications_none": "None",
        "roof_modifications_skylight": "Skylight",
        "roof_modifications_solar": "Solar Panels",
        
        # Advanced Modifications
        "interior_layout": "Interior Layout",
        "interior_layout_open": "Open Space",
        "interior_layout_partitioned": "Partitioned",
        "interior_layout_custom": "Custom Layout",
        
        "security_systems": "Security Systems",
        "security_systems_basic": "Basic",
        "security_systems_advanced": "Advanced",
        "security_systems_none": "None",
        
        "exterior_cladding": "Exterior Cladding",
        "exterior_cladding_none": "None",
        "exterior_cladding_wood": "Wood",
        "exterior_cladding_composite": "Composite",
        
        "additional_openings": "Additional Openings",
        "additional_openings_none": "None",
        "additional_openings_door": "Additional Door",
        "additional_openings_emergency": "Emergency Exit",
        
        "fire_systems": "Fire Safety Systems",
        "fire_systems_none": "None",
        "fire_systems_basic": "Basic",
        "fire_systems_full": "Full System",
        
        "accessibility": "Accessibility",
        "accessibility_none": "Standard",
        "accessibility_ramp": "Wheelchair Ramp",
        "accessibility_full": "Full Accessibility",
        
        # Transport & Logistics
        "delivery_zone": "Delivery Zone",
        "delivery_zone_local": "Local (50km)",
        "delivery_zone_regional": "Regional (200km)",
        "delivery_zone_national": "National",
        "delivery_zone_international": "International",
        
        "transport_type": "Transport Type",
        "transport_type_standard": "Standard",
        "transport_type_crane": "With Crane",
        "transport_type_special": "Special Transport",
        
        "installation": "Installation",
        "installation_none": "Self Installation",
        "installation_basic": "Basic Setup",
        "installation_full": "Full Installation",
        
        # Equipment & Extras
        "office_equipment": "Office Equipment",
        "office_equipment_none": "None",
        "office_equipment_basic": "Basic Furniture",
        "office_equipment_full": "Complete Office",
        
        "appliances": "Appliances",
        "appliances_none": "None",
        "appliances_kitchen": "Kitchen Equipment",
        "appliances_laundry": "Laundry Equipment",
        
        "it_systems": "IT Systems",
        "it_systems_none": "None",
        "it_systems_basic": "Basic Network",
        "it_systems_advanced": "Advanced IT",
        
        # Comments
        "system_comments": "System Requirements Comments",
        "advanced_comments": "Advanced Modifications Comments",
        "general_comments": "General Comments",
        
        # Window types
        "window_types": "Window Types",
        "window_types_standard": "Standard",
        "window_types_double": "Double Glazed",
        "window_types_security": "Security Windows",
        
        # Paint finish
        "paint_finish": "Paint Finish",
        "paint_finish_standard": "Standard",
        "paint_finish_premium": "Premium",
        "paint_finish_custom": "Custom Color"
    }
    
    # Add missing keys to master set
    master_keys.update(additional_keys.keys())
    
    # Fix each language file
    for lang in languages:
        current_keys = all_keys_by_lang[lang]
        missing_keys = master_keys - current_keys
        
        if missing_keys:
            print(f"\n{lang.upper()}: Adding {len(missing_keys)} missing keys")
            
            # Add missing keys with appropriate translations
            for key in missing_keys:
                if key in additional_keys:
                    # Use the English version as base
                    value = additional_keys[key]
                    
                    # Apply basic language-specific translations
                    if lang == 'de':
                        value = translate_to_german(key, value)
                    elif lang == 'nl':
                        value = translate_to_dutch(key, value)
                    elif lang == 'cs':
                        value = translate_to_czech(key, value)
                    elif lang == 'hu':
                        value = translate_to_hungarian(key, value)
                    elif lang == 'pl':
                        value = translate_to_polish(key, value)
                    
                    set_nested_value(translations[lang], key, value)
                else:
                    # Try to find the value from the most complete language file
                    found_value = None
                    for check_lang in ['pl', 'en', 'de']:  # Priority order
                        if check_lang in translations:
                            found_value = get_nested_value(translations[check_lang], key)
                            if found_value:
                                break
                    
                    if found_value:
                        set_nested_value(translations[lang], key, found_value)
                    else:
                        # Default fallback
                        set_nested_value(translations[lang], key, key.split('.')[-1].replace('_', ' ').title())
        else:
            print(f"{lang.upper()}: Complete (no missing keys)")
    
    # Save updated translation files
    for lang in languages:
        filepath = f'locales/{lang}.json'
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(translations[lang], f, ensure_ascii=False, indent=2)
            print(f"Updated {filepath}")
        except Exception as e:
            print(f"Error saving {filepath}: {e}")

def translate_to_german(key: str, english_value: str) -> str:
    """Basic German translations for key terms"""
    basic_translations = {
        "Construction Material": "Konstruktionsmaterial",
        "Steel": "Stahl", 
        "Aluminum": "Aluminium",
        "Composite": "Verbundwerkstoff",
        "Insulation": "Isolierung",
        "Basic": "Grundlegend",
        "Standard": "Standard",
        "Premium": "Premium",
        "None": "Keine",
        "Lighting": "Beleuchtung",
        "Professional": "Professionell",
        "Ventilation": "Belüftung",
        "Natural": "Natürlich",
        "Security Systems": "Sicherheitssysteme",
        "Advanced": "Erweitert"
    }
    return basic_translations.get(english_value, english_value)

def translate_to_dutch(key: str, english_value: str) -> str:
    """Basic Dutch translations for key terms"""
    basic_translations = {
        "Construction Material": "Constructiemateriaal",
        "Steel": "Staal",
        "Aluminum": "Aluminium", 
        "Composite": "Composiet",
        "Insulation": "Isolatie",
        "Basic": "Basis",
        "Standard": "Standaard",
        "Premium": "Premium", 
        "None": "Geen",
        "Lighting": "Verlichting",
        "Professional": "Professioneel",
        "Ventilation": "Ventilatie",
        "Natural": "Natuurlijk",
        "Security Systems": "Beveiligingssystemen",
        "Advanced": "Geavanceerd"
    }
    return basic_translations.get(english_value, english_value)

def translate_to_czech(key: str, english_value: str) -> str:
    """Basic Czech translations for key terms"""
    basic_translations = {
        "Construction Material": "Konstrukční materiál",
        "Steel": "Ocel",
        "Aluminum": "Hliník",
        "Composite": "Kompozit", 
        "Insulation": "Izolace",
        "Basic": "Základní",
        "Standard": "Standardní",
        "Premium": "Prémiový",
        "None": "Žádný",
        "Lighting": "Osvětlení",
        "Professional": "Profesionální",
        "Ventilation": "Ventilace",
        "Natural": "Přirozená",
        "Security Systems": "Bezpečnostní systémy",
        "Advanced": "Pokročilý"
    }
    return basic_translations.get(english_value, english_value)

def translate_to_hungarian(key: str, english_value: str) -> str:
    """Basic Hungarian translations for key terms"""
    basic_translations = {
        "Construction Material": "Építőanyag",
        "Steel": "Acél",
        "Aluminum": "Alumínium",
        "Composite": "Kompozit",
        "Insulation": "Szigetelés", 
        "Basic": "Alapvető",
        "Standard": "Szabványos",
        "Premium": "Prémium",
        "None": "Nincs",
        "Lighting": "Világítás",
        "Professional": "Professzionális",
        "Ventilation": "Szellőzés", 
        "Natural": "Természetes",
        "Security Systems": "Biztonsági rendszerek",
        "Advanced": "Fejlett"
    }
    return basic_translations.get(english_value, english_value)

def translate_to_polish(key: str, english_value: str) -> str:
    """Basic Polish translations for key terms"""
    basic_translations = {
        "Construction Material": "Materiał konstrukcyjny",
        "Steel": "Stal",
        "Aluminum": "Aluminium", 
        "Composite": "Kompozyt",
        "Insulation": "Izolacja",
        "Basic": "Podstawowa",
        "Standard": "Standardowa",
        "Premium": "Premium",
        "None": "Brak",
        "Lighting": "Oświetlenie",
        "Professional": "Profesjonalne",
        "Ventilation": "Wentylacja",
        "Natural": "Naturalna",
        "Security Systems": "Systemy bezpieczeństwa", 
        "Advanced": "Zaawansowane"
    }
    return basic_translations.get(english_value, english_value)

if __name__ == "__main__":
    fix_translation_coverage()
    print("\nTranslation coverage fix completed!")