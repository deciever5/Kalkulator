#!/usr/bin/env python3
"""
Safe Translation Cleanup Script
Removes clearly obsolete translation keys identified from the analysis
"""

import json
import os
from pathlib import Path

# Keys that are clearly obsolete based on analysis
OBSOLETE_KEYS = [
    "basic_configuration",
    "ai_cost_estimator_desc", 
    "complexity_multiplier",
    "materials_base_cost",
    "fallback_cost_estimate",
    "equipment_extras",
    "cost_breakdown",
    "ai_powered_estimation",
    "technical_analysis",
    "ai_cost_estimation",
    "advanced_modifications",
    "key_modifications"
]

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

def remove_obsolete_keys(data, keys_to_remove):
    """Remove obsolete keys from translation data"""
    removed_count = 0
    
    for key in keys_to_remove:
        if key in data:
            del data[key]
            removed_count += 1
            print(f"  Removed: {key}")
    
    return removed_count

def cleanup_language_file(language_file):
    """Clean up obsolete keys from a single language file"""
    print(f"\nCleaning up {language_file}...")
    
    data = load_json_file(language_file)
    if not data:
        return False
    
    # Create backup
    backup_file = f"{language_file}.backup"
    if not os.path.exists(backup_file):
        save_json_file(backup_file, data)
        print(f"  Created backup: {backup_file}")
    
    # Remove obsolete keys
    removed_count = remove_obsolete_keys(data, OBSOLETE_KEYS)
    
    if removed_count > 0:
        if save_json_file(language_file, data):
            print(f"  Successfully removed {removed_count} obsolete keys")
            return True
        else:
            print(f"  Failed to save changes")
            return False
    else:
        print(f"  No obsolete keys found")
        return True

def main():
    """Main cleanup function"""
    print("🧹 Starting Safe Translation Cleanup...")
    print(f"Target obsolete keys: {len(OBSOLETE_KEYS)}")
    
    locales_dir = Path('locales')
    if not locales_dir.exists():
        print("❌ No locales directory found")
        return
    
    # Get all JSON files in locales directory
    language_files = list(locales_dir.glob('*.json'))
    if not language_files:
        print("❌ No translation files found")
        return
    
    print(f"📋 Found {len(language_files)} language files to process")
    
    success_count = 0
    for lang_file in language_files:
        if lang_file.name.endswith('.backup'):
            continue
            
        if cleanup_language_file(lang_file):
            success_count += 1
    
    print(f"\n✨ Cleanup complete!")
    print(f"📊 Successfully processed: {success_count}/{len([f for f in language_files if not f.name.endswith('.backup')])} files")
    print(f"💾 Backup files created for safety")
    
    if success_count > 0:
        print(f"\n💡 Next steps:")
        print(f"  1. Test the application thoroughly")
        print(f"  2. If everything works, you can delete .backup files")
        print(f"  3. If issues occur, restore from .backup files")

if __name__ == "__main__":
    main()