#!/usr/bin/env python3
"""
Fix All Translation Issues
Corrects structural problems in all language files after sync
"""

import json
from pathlib import Path

# Proper English translations for key sections
ENGLISH_CORRECTIONS = {
    "electrical_system": "Electrical System",
    "plumbing_system": "Plumbing System", 
    "hvac_system": "HVAC System",
    "configure_container": "Configure Your Container",
    "simple_process_2_steps": "Simple process in 2 easy steps",
    "step_1_configuration": "Step 1: Configuration",
    "choose_container_type": "Choose container type and modifications",
    "step_2_ai_estimation": "Step 2: AI Estimation",
    "ai_analyzes_configuration": "AI analyzes your configuration and provides cost estimates",
    "send_inquiry_button": "Send Inquiry",
    "why_kan_bud": "Why KAN-BUD?",
    "precise_quotes": "Precise Quotes",
    "ai_historical_data": "AI analysis with historical data",
    "european_climate_standards": "European climate standards",
    "transparent_calculations": "Transparent calculations",
    "fast_realization": "Fast Realization",
    "hundreds_of_projects": "Hundreds of completed projects",
    "own_machinery": "Own machinery park",
    "poland_center": "Central location in Poland",
    "full_service": "Full Service",
    "design_execution": "From design to execution",
    "transport_assembly": "Transport and assembly",
    "after_sales_support": "After-sales support",
    "contact_us": "Contact us",
    "address": "Address",
    "phone": "Phone",
    "email": "Email",
    "working_hours": "Working hours",
    "mon_fri": "Mon-Fri 8:00-17:00"
}

# Basic translations for other languages
BASIC_TRANSLATIONS = {
    'de': {
        'electrical_system': 'Elektrisches System',
        'plumbing_system': 'Sanitärsystem',
        'hvac_system': 'HVAC-System',
        'configure_container': 'Container konfigurieren',
        'contact_us': 'Kontaktieren Sie uns',
        'address': 'Adresse',
        'phone': 'Telefon',
        'email': 'E-Mail'
    },
    'fr': {
        'electrical_system': 'Système électrique',
        'plumbing_system': 'Système de plomberie',
        'hvac_system': 'Système CVC',
        'configure_container': 'Configurez votre conteneur',
        'contact_us': 'Contactez-nous',
        'address': 'Adresse',
        'phone': 'Téléphone',
        'email': 'E-mail'
    },
    'es': {
        'electrical_system': 'Sistema eléctrico',
        'plumbing_system': 'Sistema de fontanería',
        'hvac_system': 'Sistema HVAC',
        'configure_container': 'Configure su contenedor',
        'contact_us': 'Contáctenos',
        'address': 'Dirección',
        'phone': 'Teléfono',
        'email': 'Correo electrónico'
    },
    'it': {
        'electrical_system': 'Sistema elettrico',
        'plumbing_system': 'Sistema idraulico',
        'hvac_system': 'Sistema HVAC',
        'configure_container': 'Configura il tuo container',
        'contact_us': 'Contattaci',
        'address': 'Indirizzo',
        'phone': 'Telefono',
        'email': 'Email'
    }
}

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

def fix_language_file(filepath, language_code):
    """Fix translation issues in a specific language file"""
    data = load_json_file(filepath)
    if not data:
        return False
    
    if language_code == 'en':
        # Apply English corrections
        for key, value in ENGLISH_CORRECTIONS.items():
            if key in data:
                data[key] = value
    elif language_code in BASIC_TRANSLATIONS:
        # Apply basic translations for other languages
        translations = BASIC_TRANSLATIONS[language_code]
        for key, value in translations.items():
            if key in data:
                data[key] = value
    
    return save_json_file(filepath, data)

def main():
    """Main function"""
    print("Fixing translation issues across all language files...")
    
    locales_dir = Path('locales')
    language_files = [f for f in locales_dir.glob('*.json') if not f.name.endswith('.backup')]
    
    success_count = 0
    for lang_file in language_files:
        language_code = lang_file.stem
        print(f"Fixing {language_code}...")
        
        if fix_language_file(lang_file, language_code):
            success_count += 1
            print(f"  Successfully fixed {language_code}")
        else:
            print(f"  Failed to fix {language_code}")
    
    print(f"\nFixed {success_count}/{len(language_files)} language files")

if __name__ == "__main__":
    main()