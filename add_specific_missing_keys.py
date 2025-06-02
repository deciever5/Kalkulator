#!/usr/bin/env python3
"""
Add Specific Missing Translation Keys
Adds the specific missing keys that are causing the translation errors
"""

import json

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

def add_missing_keys_to_language(lang_code):
    """Add the specific missing keys to a language file"""
    print(f"Adding missing keys to {lang_code}...")
    
    filepath = f'locales/{lang_code}.json'
    data = load_json_file(filepath)
    if not data:
        return False
    
    # Add missing ventilation keys
    if 'ventilation' not in data:
        data['ventilation'] = {}
    
    ventilation_keys = {
        'none': f'[{lang_code.upper()}_PLACEHOLDER] No ventilation',
        'gravity': f'[{lang_code.upper()}_PLACEHOLDER] Gravity vents',
        'wall_fans': f'[{lang_code.upper()}_PLACEHOLDER] Wall fans', 
        'mechanical': f'[{lang_code.upper()}_PLACEHOLDER] Mechanical ventilation',
        'heat_recovery': f'[{lang_code.upper()}_PLACEHOLDER] Heat recovery ventilation',
        'split_ac': f'[{lang_code.upper()}_PLACEHOLDER] Split AC',
        'central_ac': f'[{lang_code.upper()}_PLACEHOLDER] Central AC',
        'industrial': f'[{lang_code.upper()}_PLACEHOLDER] Industrial ventilation'
    }
    
    for key, value in ventilation_keys.items():
        if key not in data['ventilation']:
            data['ventilation'][key] = value
    
    # Add missing roof_modifications keys
    if 'roof_modifications' not in data:
        data['roof_modifications'] = {}
    
    roof_keys = {
        'none': f'[{lang_code.upper()}_PLACEHOLDER] No modifications',
        'insulation': f'[{lang_code.upper()}_PLACEHOLDER] Additional insulation',
        'skylight': f'[{lang_code.upper()}_PLACEHOLDER] Skylights',
        'fans': f'[{lang_code.upper()}_PLACEHOLDER] Roof fans',
        'solar': f'[{lang_code.upper()}_PLACEHOLDER] Solar panels',
        'antennas': f'[{lang_code.upper()}_PLACEHOLDER] Antennas',
        'sloped': f'[{lang_code.upper()}_PLACEHOLDER] Sloped roof',
        'terrace': f'[{lang_code.upper()}_PLACEHOLDER] Roof terrace',
        'snow_removal': f'[{lang_code.upper()}_PLACEHOLDER] Snow removal system'
    }
    
    for key, value in roof_keys.items():
        if key not in data['roof_modifications']:
            data['roof_modifications'][key] = value
    
    # Add missing insulation keys
    if 'insulation' not in data:
        data['insulation'] = {}
    
    insulation_keys = {
        'basic': f'[{lang_code.upper()}_PLACEHOLDER] Basic (50mm)',
        'standard': f'[{lang_code.upper()}_PLACEHOLDER] Standard (100mm)',
        'premium': f'[{lang_code.upper()}_PLACEHOLDER] Premium (150mm)',
        'extreme': f'[{lang_code.upper()}_PLACEHOLDER] Extreme (200mm)'
    }
    
    for key, value in insulation_keys.items():
        if key not in data['insulation']:
            data['insulation'][key] = value
    
    # Add missing windows keys
    if 'windows' not in data:
        data['windows'] = {}
    
    windows_keys = {
        'none': f'[{lang_code.upper()}_PLACEHOLDER] No windows',
        'one': f'[{lang_code.upper()}_PLACEHOLDER] 1 window',
        'two': f'[{lang_code.upper()}_PLACEHOLDER] 2 windows',
        'three': f'[{lang_code.upper()}_PLACEHOLDER] 3 windows',
        'four': f'[{lang_code.upper()}_PLACEHOLDER] 4 windows',
        'five_plus': f'[{lang_code.upper()}_PLACEHOLDER] 5+ windows'
    }
    
    for key, value in windows_keys.items():
        if key not in data['windows']:
            data['windows'][key] = value
    
    # Ensure lighting keys exist
    if 'lighting' not in data:
        data['lighting'] = {}
    
    lighting_missing = {
        'none': f'[{lang_code.upper()}_PLACEHOLDER] No lighting',
        'basic_led': f'[{lang_code.upper()}_PLACEHOLDER] Basic LED lighting',
        'energy_efficient': f'[{lang_code.upper()}_PLACEHOLDER] Energy efficient LED',
        'exterior': f'[{lang_code.upper()}_PLACEHOLDER] Exterior lighting',
        'emergency': f'[{lang_code.upper()}_PLACEHOLDER] Emergency lighting',
        'smart': f'[{lang_code.upper()}_PLACEHOLDER] Smart lighting'
    }
    
    for key, value in lighting_missing.items():
        if key not in data['lighting']:
            data['lighting'][key] = value
    
    if save_json_file(filepath, data):
        print(f"  ✓ Successfully added missing keys to {lang_code}")
        return True
    else:
        print(f"  ✗ Failed to update {lang_code}")
        return False

def main():
    """Main function"""
    print("Adding specific missing translation keys to all languages...")
    
    languages = ['en', 'de', 'fr', 'es', 'it', 'nl', 'cs', 'sk', 'hu', 'sv', 'fi', 'uk']
    
    for lang in languages:
        add_missing_keys_to_language(lang)
    
    print("Missing keys addition complete!")

if __name__ == "__main__":
    main()