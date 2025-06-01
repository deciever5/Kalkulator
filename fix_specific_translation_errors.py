
#!/usr/bin/env python3
"""
Fix Specific Translation Errors
Addresses the issues identified in the translation analysis
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
        return {}

def save_json_file(filepath, data):
    """Save JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def fix_english_translations():
    """Fix specific English translation errors"""
    
    print("🔧 Fixing specific English translation errors...")
    
    en_file = 'locales/en.json'
    en_data = load_json_file(en_file)
    
    if not en_data:
        print("❌ Could not load English translations")
        return False
    
    fixes = {
        # Fix machine translation errors
        "nav.custom_sizing": "Custom\nSizing",
        "nav.bulk_pricing": "Bulk\nPricing", 
        
        # Fix capitalization issues
        "delivery.zones.international": "International (Outside Europe)",
        
        # Fix inconsistent descriptions
        "construction_material_composite": "Composite Material",
        "exterior_cladding_composite": "Composite Material (Specialist Use)",
        
        # Fix language selector
        "ui.language_selector": "Language",
        
        # Standardize security systems
        "security_systems_advanced": "Advanced Security Systems",
        "security_systems_basic": "Basic Security Systems",
        
        # Fix technical analysis
        "technical_analysis": "Technical\nAnalysis",
        "quote_generator": "Quote\nGenerator",
        
        # Fix flooring consistency (add missing entries)
        "container.flooring.none": "No Flooring",
        "container.flooring.polished_concrete": "Polished Concrete"
    }
    
    def set_nested_value(data, key_path, value):
        """Set nested value using dot notation"""
        keys = key_path.split('.')
        current = data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    fixes_applied = 0
    
    for key_path, new_value in fixes.items():
        try:
            set_nested_value(en_data, key_path, new_value)
            fixes_applied += 1
            print(f"   ✅ Fixed: {key_path} = '{new_value}'")
        except Exception as e:
            print(f"   ❌ Failed to fix {key_path}: {e}")
    
    # Save fixes
    if save_json_file(en_file, en_data):
        print(f"✅ Applied {fixes_applied} fixes to English translations")
        return True
    else:
        print("❌ Failed to save English translation fixes")
        return False

def check_missing_keys():
    """Check for missing keys between Polish and English"""
    
    print("\n🔍 Checking for missing keys...")
    
    pl_data = load_json_file('locales/pl.json')
    en_data = load_json_file('locales/en.json')
    
    if not pl_data or not en_data:
        print("❌ Could not load translation files")
        return
    
    def get_all_keys(data, prefix=""):
        """Get all keys from nested dict"""
        keys = set()
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            keys.add(full_key)
            if isinstance(value, dict):
                keys.update(get_all_keys(value, full_key))
        return keys
    
    pl_keys = get_all_keys(pl_data)
    en_keys = get_all_keys(en_data)
    
    missing_in_english = pl_keys - en_keys
    missing_in_polish = en_keys - pl_keys
    
    if missing_in_english:
        print(f"❌ Missing in English ({len(missing_in_english)} keys):")
        for key in sorted(missing_in_english)[:10]:  # Show first 10
            print(f"   - {key}")
        if len(missing_in_english) > 10:
            print(f"   ... and {len(missing_in_english) - 10} more")
    
    if missing_in_polish:
        print(f"⚠️  Missing in Polish ({len(missing_in_polish)} keys):")
        for key in sorted(missing_in_polish)[:10]:  # Show first 10
            print(f"   - {key}")
        if len(missing_in_polish) > 10:
            print(f"   ... and {len(missing_in_polish) - 10} more")
    
    if not missing_in_english and not missing_in_polish:
        print("✅ All keys are present in both languages")

def standardize_capitalization():
    """Standardize capitalization in English translations"""
    
    print("\n🎨 Standardizing capitalization...")
    
    en_file = 'locales/en.json'
    en_data = load_json_file(en_file)
    
    if not en_data:
        return False
    
    def title_case_fixes(data):
        """Apply title case fixes recursively"""
        fixes_count = 0
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    fixes_count += title_case_fixes(value)
                elif isinstance(value, str):
                    # Apply title case to certain patterns
                    if key.endswith('_label') or key.endswith('_title'):
                        new_value = value.title()
                        if new_value != value:
                            data[key] = new_value
                            fixes_count += 1
        
        return fixes_count
    
    fixes_applied = title_case_fixes(en_data)
    
    if fixes_applied > 0:
        if save_json_file(en_file, en_data):
            print(f"✅ Applied {fixes_applied} capitalization fixes")
        else:
            print("❌ Failed to save capitalization fixes")
    else:
        print("✅ No capitalization fixes needed")

def main():
    """Main function"""
    print("🚀 FIXING SPECIFIC TRANSLATION ERRORS")
    print("="*50)
    
    # Fix specific errors
    fix_english_translations()
    
    # Check for missing keys
    check_missing_keys()
    
    # Standardize capitalization
    standardize_capitalization()
    
    print("\n🎉 Translation error fixes completed!")
    print("📝 Recommendations:")
    print("   1. Review translations with native English speakers")
    print("   2. Run comprehensive translation checker")
    print("   3. Test the application with English language selected")

if __name__ == "__main__":
    main()
