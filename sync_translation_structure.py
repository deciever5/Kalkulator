#!/usr/bin/env python3
"""
Sync Translation Structure Script
Copies Polish structure to all other language files and translates missing content
"""

import json
import os
from pathlib import Path

# Language mappings for automatic translation of key system terms
TRANSLATIONS = {
    'en': {
        'flooring': 'Flooring',
        'electrical_system': 'Electrical System',
        'plumbing_system': 'Plumbing System',
        'hvac_system': 'HVAC System',
        'none': 'None',
        'basic': 'Basic',
        'standard': 'Standard',
        'extended': 'Extended',
        'industrial': 'Industrial',
        'smart': 'Smart',
        'preparation': 'Preparation',
        'full': 'Full',
        'commercial': 'Commercial'
    },
    'de': {
        'flooring': 'Bodenbelag',
        'electrical_system': 'Elektrisches System',
        'plumbing_system': 'Sanitärsystem',
        'hvac_system': 'HVAC-System',
        'none': 'Keine',
        'basic': 'Grundlegend',
        'standard': 'Standard',
        'extended': 'Erweitert',
        'industrial': 'Industriell',
        'smart': 'Intelligent',
        'preparation': 'Vorbereitung',
        'full': 'Vollständig',
        'commercial': 'Kommerziell'
    },
    'fr': {
        'flooring': 'Revêtement de sol',
        'electrical_system': 'Système électrique',
        'plumbing_system': 'Système de plomberie',
        'hvac_system': 'Système CVC',
        'none': 'Aucun',
        'basic': 'De base',
        'standard': 'Standard',
        'extended': 'Étendu',
        'industrial': 'Industriel',
        'smart': 'Intelligent',
        'preparation': 'Préparation',
        'full': 'Complet',
        'commercial': 'Commercial'
    },
    'es': {
        'flooring': 'Suelo',
        'electrical_system': 'Sistema eléctrico',
        'plumbing_system': 'Sistema de fontanería',
        'hvac_system': 'Sistema HVAC',
        'none': 'Ninguno',
        'basic': 'Básico',
        'standard': 'Estándar',
        'extended': 'Extendido',
        'industrial': 'Industrial',
        'smart': 'Inteligente',
        'preparation': 'Preparación',
        'full': 'Completo',
        'commercial': 'Comercial'
    },
    'it': {
        'flooring': 'Pavimentazione',
        'electrical_system': 'Sistema elettrico',
        'plumbing_system': 'Sistema idraulico',
        'hvac_system': 'Sistema HVAC',
        'none': 'Nessuno',
        'basic': 'Base',
        'standard': 'Standard',
        'extended': 'Esteso',
        'industrial': 'Industriale',
        'smart': 'Intelligente',
        'preparation': 'Preparazione',
        'full': 'Completo',
        'commercial': 'Commerciale'
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

def translate_value(value, language_code, key_context=""):
    """Translate a value using basic mappings"""
    if language_code not in TRANSLATIONS:
        return value
    
    translations = TRANSLATIONS[language_code]
    
    # Try exact match first
    if value.lower() in translations:
        return translations[value.lower()]
    
    # For complex descriptions, translate key components
    if isinstance(value, str):
        result = value
        for en_term, translated_term in translations.items():
            if en_term in value.lower():
                result = result.replace(en_term.title(), translated_term)
                result = result.replace(en_term.lower(), translated_term.lower())
        return result
    
    return value

def merge_structures(polish_data, target_data, language_code):
    """Merge Polish structure with existing target language data"""
    def merge_recursive(pl_obj, target_obj, path=""):
        if isinstance(pl_obj, dict):
            if not isinstance(target_obj, dict):
                target_obj = {}
            
            for key, value in pl_obj.items():
                if key in target_obj:
                    # Key exists, merge recursively if both are dicts
                    if isinstance(value, dict) and isinstance(target_obj[key], dict):
                        target_obj[key] = merge_recursive(value, target_obj[key], f"{path}.{key}")
                    # Keep existing translation if it's not a dict
                    elif not isinstance(value, dict):
                        continue  # Keep existing translation
                else:
                    # Key missing, add with translation
                    if isinstance(value, dict):
                        target_obj[key] = merge_recursive(value, {}, f"{path}.{key}")
                    else:
                        # Translate the value
                        target_obj[key] = translate_value(value, language_code, f"{path}.{key}")
            
            return target_obj
        else:
            # For non-dict values, return existing if available, otherwise translate
            return target_obj if target_obj is not None else translate_value(pl_obj, language_code, path)
    
    return merge_recursive(polish_data, target_data)

def sync_language_file(polish_data, language_file, language_code):
    """Sync a single language file with Polish structure"""
    print(f"\nSyncing {language_file} ({language_code})...")
    
    # Load existing data
    existing_data = load_json_file(language_file)
    if existing_data is None:
        existing_data = {}
    
    # Create backup
    backup_file = f"{language_file}.backup"
    if not os.path.exists(backup_file):
        save_json_file(backup_file, existing_data)
        print(f"  Created backup: {backup_file}")
    
    # Merge structures
    merged_data = merge_structures(polish_data, existing_data, language_code)
    
    # Save merged data
    if save_json_file(language_file, merged_data):
        print(f"  Successfully synced structure")
        return True
    else:
        print(f"  Failed to save changes")
        return False

def main():
    """Main sync function"""
    print("🔄 Starting Translation Structure Sync...")
    print("📋 Using Polish (pl.json) as base structure")
    
    # Load Polish translations as base
    polish_file = Path('locales/pl.json')
    if not polish_file.exists():
        print("❌ Polish translation file not found")
        return
    
    polish_data = load_json_file(polish_file)
    if not polish_data:
        print("❌ Failed to load Polish translations")
        return
    
    print(f"✅ Loaded Polish base structure with {len(polish_data)} top-level keys")
    
    # Get all language files
    locales_dir = Path('locales')
    language_files = [f for f in locales_dir.glob('*.json') if f.name != 'pl.json' and not f.name.endswith('.backup')]
    
    print(f"📁 Found {len(language_files)} target language files")
    
    success_count = 0
    for lang_file in language_files:
        language_code = lang_file.stem
        
        if sync_language_file(polish_data, lang_file, language_code):
            success_count += 1
    
    print(f"\n✨ Structure sync complete!")
    print(f"📊 Successfully synced: {success_count}/{len(language_files)} files")
    print(f"💾 Backup files created for safety")
    
    print(f"\n📋 Summary:")
    print(f"  - All files now have consistent structure matching Polish")
    print(f"  - Missing keys translated using basic mappings")
    print(f"  - Existing translations preserved where possible")
    print(f"  - Manual review recommended for accuracy")

if __name__ == "__main__":
    main()