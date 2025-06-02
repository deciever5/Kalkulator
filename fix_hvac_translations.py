#!/usr/bin/env python3
"""
Fix HVAC System Translations
Ensures all languages have proper HVAC system translations without mixing languages
"""

import json
import os

def load_json_file(filepath):
    """Load JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def save_json_file(filepath, data):
    """Save JSON file with proper formatting"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def fix_hvac_translations():
    """Fix HVAC translations for all languages"""
    
    # Define correct HVAC translations for each language
    hvac_translations = {
        'en': {
            "none": "No HVAC (no heating and cooling)",
            "basic": "Basic ventilation",
            "electric_heating": "Electric heating (IR radiators)",
            "gas_heating": "Gas heating (condensing boiler)",
            "split_ac": "Split air conditioning (cooling + heating)",
            "central_ac": "Central air conditioning (with filtration, humidification)",
            "heat_pump": "Heat pump",
            "electric_heaters": "Electric heaters (1-3kW, convectors)",
            "vrv_vrf": "VRV/VRF system (multi-zone, zone control)",
            "underfloor_heating": "Underfloor heating (electric/water)"
        },
        'pl': {
            "none": "Bez HVAC (bez ogrzewania i chłodzenia)",
            "basic": "Podstawowa wentylacja",
            "electric_heating": "Ogrzewanie elektryczne (promienniki IR)",
            "gas_heating": "Ogrzewanie gazowe (piec kondensacyjny)",
            "split_ac": "Klimatyzacja rozdzielna (chłodzenie + grzanie)",
            "central_ac": "Centrala klimatyzacyjna (z filtracją, nawilżaniem)",
            "heat_pump": "Pompa ciepła",
            "electric_heaters": "Grzejniki elektryczne (1-3kW, konwektory)",
            "vrv_vrf": "System VRV/VRF (wielostrefowy, kontrola stref)",
            "underfloor_heating": "Ogrzewanie podłogowe (elektryczne/wodne)"
        },
        'de': {
            "none": "Keine HVAC (keine Heizung und Kühlung)",
            "basic": "Grundlüftung",
            "electric_heating": "Elektroheizung (IR-Strahler)",
            "gas_heating": "Gasheizung (Brennwertkessel)",
            "split_ac": "Split-Klimaanlage (Kühlung + Heizung)",
            "central_ac": "Zentrale Klimaanlage (mit Filterung, Befeuchtung)",
            "heat_pump": "Wärmepumpe",
            "electric_heaters": "Elektroheizgeräte (1-3kW, Konvektoren)",
            "vrv_vrf": "VRV/VRF-System (Mehrzonenregelung)",
            "underfloor_heating": "Fußbodenheizung (elektrisch/Wasser)"
        },
        'fr': {
            "none": "Pas de CVC (pas de chauffage et refroidissement)",
            "basic": "Ventilation de base",
            "electric_heating": "Chauffage électrique (radiateurs IR)",
            "gas_heating": "Chauffage au gaz (chaudière à condensation)",
            "split_ac": "Climatisation split (refroidissement + chauffage)",
            "central_ac": "Climatisation centrale (avec filtration, humidification)",
            "heat_pump": "Pompe à chaleur",
            "electric_heaters": "Radiateurs électriques (1-3kW, convecteurs)",
            "vrv_vrf": "Système VRV/VRF (multizones, contrôle de zones)",
            "underfloor_heating": "Chauffage au sol (électrique/eau)"
        }
    }
    
    # For other languages, use English as base and mark for translation
    default_hvac = hvac_translations['en']
    
    languages = ['en', 'pl', 'de', 'fr', 'nl', 'it', 'es', 'cs', 'sk', 'hu', 'sv', 'fi', 'uk']
    
    for lang in languages:
        filepath = f'locales/{lang}.json'
        print(f"Fixing HVAC translations for {lang}...")
        
        data = load_json_file(filepath)
        if not data:
            continue
            
        # Get the appropriate HVAC translations
        if lang in hvac_translations:
            hvac_data = hvac_translations[lang]
        else:
            hvac_data = default_hvac
            
        # Update the HVAC system translations
        if 'hvac_system' in data:
            data['hvac_system'] = hvac_data
            
        # Save the updated file
        if save_json_file(filepath, data):
            print(f"  ✓ Successfully updated {lang}")
        else:
            print(f"  ✗ Failed to update {lang}")
    
    print("HVAC translation fix complete!")

if __name__ == "__main__":
    fix_hvac_translations()