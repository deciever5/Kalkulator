
import json
import os

def show_auto_translation_examples():
    """Show specific examples of auto-translations for manual review"""
    
    print("=== AUTO-TRANSLATION EXAMPLES FOR MANUAL REVIEW ===\n")
    
    # Load one language file to show examples
    try:
        with open('locales/de.json', 'r', encoding='utf-8') as f:
            de_data = json.load(f)
    except:
        print("Could not load German translations")
        return
    
    # Find auto-translations in various categories
    categories = {
        'ui': 'User Interface Elements',
        'nav': 'Navigation',
        'form': 'Form Labels', 
        'container': 'Container Types',
        'send_inquiry': 'Inquiry Form'
    }
    
    for category, description in categories.items():
        if category in de_data:
            print(f"📂 {description} ({category}):")
            
            auto_found = False
            for key, value in de_data[category].items():
                if isinstance(value, str) and value.startswith("[AUTO]"):
                    clean_value = value.replace("[AUTO] ", "")
                    print(f"   {key}: '{clean_value}'")
                    auto_found = True
                elif isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, str) and subvalue.startswith("[AUTO]"):
                            clean_subvalue = subvalue.replace("[AUTO] ", "")
                            print(f"   {key}.{subkey}: '{clean_subvalue}'")
                            auto_found = True
            
            if not auto_found:
                print("   ✅ No auto-translations found in this category")
            print()
    
    # Check top-level auto-translations
    print("📂 Top-level translations:")
    auto_found = False
    for key, value in de_data.items():
        if isinstance(value, str) and value.startswith("[AUTO]"):
            clean_value = value.replace("[AUTO] ", "")
            print(f"   {key}: '{clean_value}'")
            auto_found = True
    
    if not auto_found:
        print("   ✅ No top-level auto-translations found")

if __name__ == "__main__":
    show_auto_translation_examples()
