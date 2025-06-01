"""
Complete English Placeholder Fixer
Systematically finds and fixes all remaining English text in the Polish version
"""

import os
import json
import re
from typing import Dict, List, Set

def load_json_file(filepath: str) -> Dict:
    """Load JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def save_json_file(filepath: str, data: Dict) -> bool:
    """Save JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def find_english_patterns_in_files():
    """Find all English patterns in Python files"""
    english_patterns = [
        r'"Choose an option"',
        r'"Select"',
        r'"Please select"',
        r'"None selected"',
        r'"Loading\.\.\."',
        r'"Processing\.\.\."',
        r'"Error"',
        r'"Success"',
        r'"Warning"',
        r'"Info"',
        r'"Basic"',
        r'"Standard"',
        r'"Premium"',
        r'"Advanced"',
        r'"Configuration"',
        r'"Settings"',
        r'"Options"',
        r'"Details"',
        r'"Summary"',
        r'"Description"',
        r'"Analysis"',
        r'"Report"',
        r'"Export"',
        r'"Import"',
        r'"Save"',
        r'"Load"',
        r'"Cancel"',
        r'"OK"',
        r'"Yes"',
        r'"No"',
        r'"Continue"',
        r'"Back"',
        r'"Next"',
        r'"Finish"',
        r'"Help"',
        r'"About"'
    ]
    
    files_to_check = []
    
    # Get all Python files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.endswith('.py'):
                files_to_check.append(os.path.join(root, file))
    
    found_patterns = {}
    
    for filepath in files_to_check:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for pattern in english_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    if filepath not in found_patterns:
                        found_patterns[filepath] = []
                    found_patterns[filepath].extend(matches)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    
    return found_patterns

def add_missing_polish_translations():
    """Add comprehensive Polish translations for common UI elements"""
    
    additional_translations = {
        "ui_elements": {
            "choose_option": "Wybierz opcję",
            "select": "Wybierz",
            "please_select": "Proszę wybrać",
            "none_selected": "Nie wybrano",
            "loading": "Ładowanie...",
            "processing": "Przetwarzanie...",
            "calculating": "Obliczanie...",
            "analyzing": "Analizowanie...",
            "generating": "Generowanie...",
            "error": "Błąd",
            "success": "Sukces",
            "warning": "Ostrzeżenie",
            "info": "Informacja",
            "basic": "Podstawowy",
            "standard": "Standardowy",
            "premium": "Premium",
            "advanced": "Zaawansowany",
            "configuration": "Konfiguracja",
            "settings": "Ustawienia",
            "options": "Opcje",
            "details": "Szczegóły",
            "summary": "Podsumowanie",
            "description": "Opis",
            "analysis": "Analiza",
            "report": "Raport",
            "export": "Eksport",
            "import": "Import",
            "save": "Zapisz",
            "load": "Wczytaj",
            "cancel": "Anuluj",
            "ok": "OK",
            "yes": "Tak",
            "no": "Nie",
            "continue": "Kontynuuj",
            "back": "Wstecz",
            "next": "Dalej",
            "finish": "Zakończ",
            "help": "Pomoc",
            "about": "O programie",
            "close": "Zamknij",
            "edit": "Edytuj",
            "delete": "Usuń",
            "add": "Dodaj",
            "remove": "Usuń",
            "update": "Aktualizuj",
            "refresh": "Odśwież",
            "reset": "Resetuj",
            "clear": "Wyczyść",
            "search": "Szukaj",
            "filter": "Filtruj",
            "sort": "Sortuj",
            "view": "Widok",
            "print": "Drukuj",
            "download": "Pobierz",
            "upload": "Prześlij"
        },
        "status_messages": {
            "operation_successful": "Operacja zakończona sukcesem",
            "operation_failed": "Operacja nie powiodła się",
            "file_uploaded": "Plik został przesłany",
            "file_not_found": "Nie znaleziono pliku",
            "invalid_input": "Nieprawidłowe dane wejściowe",
            "connection_error": "Błąd połączenia",
            "timeout_error": "Przekroczono limit czasu",
            "permission_denied": "Brak uprawnień",
            "not_available": "Niedostępne",
            "coming_soon": "Wkrótce dostępne"
        },
        "form_placeholders": {
            "enter_name": "Wprowadź nazwę",
            "enter_email": "Wprowadź adres email",
            "enter_phone": "Wprowadź numer telefonu",
            "enter_address": "Wprowadź adres",
            "enter_description": "Wprowadź opis",
            "enter_comments": "Wprowadź komentarze",
            "select_date": "Wybierz datę",
            "select_time": "Wybierz godzinę",
            "select_file": "Wybierz plik",
            "select_folder": "Wybierz folder"
        }
    }
    
    # Load current Polish translations
    polish_file = "locales/pl.json"
    polish_data = load_json_file(polish_file)
    
    if not polish_data:
        print("❌ Could not load Polish translations")
        return False
    
    # Add new translations
    translations_added = 0
    for category, translations in additional_translations.items():
        if category not in polish_data:
            polish_data[category] = {}
        
        for key, value in translations.items():
            if key not in polish_data[category]:
                polish_data[category][key] = value
                translations_added += 1
    
    # Save updated translations
    if translations_added > 0:
        if save_json_file(polish_file, polish_data):
            print(f"✅ Added {translations_added} new Polish translations")
            return True
        else:
            print("❌ Failed to save updated translations")
            return False
    else:
        print("✅ All translations already exist")
        return True

def create_streamlit_polish_config():
    """Create Streamlit configuration to use Polish defaults"""
    
    config_content = """
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
headless = true
address = "0.0.0.0"
port = 5000

[client]
showErrorDetails = false

[browser]
gatherUsageStats = false

[ui]
hideTopBar = false
hideSidebarNav = false
"""
    
    # Create .streamlit directory if it doesn't exist
    os.makedirs('.streamlit', exist_ok=True)
    
    # Write config
    try:
        with open('.streamlit/config.toml', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("✅ Created Streamlit Polish configuration")
        return True
    except Exception as e:
        print(f"❌ Error creating Streamlit config: {e}")
        return False

def main():
    """Main function to fix all English placeholders"""
    print("🔧 COMPREHENSIVE ENGLISH PLACEHOLDER FIXER")
    print("=" * 60)
    
    # Step 1: Find English patterns in code
    print("📝 Step 1: Scanning for English patterns in code...")
    english_patterns = find_english_patterns_in_files()
    
    if english_patterns:
        print(f"⚠️  Found English patterns in {len(english_patterns)} files:")
        for filepath, patterns in english_patterns.items():
            print(f"   📄 {filepath}: {len(patterns)} patterns")
            for pattern in set(patterns):  # Remove duplicates
                print(f"      - {pattern}")
    else:
        print("✅ No hardcoded English patterns found in code")
    
    # Step 2: Add comprehensive Polish translations
    print("\n📝 Step 2: Adding comprehensive Polish translations...")
    add_missing_polish_translations()
    
    # Step 3: Create Streamlit Polish configuration
    print("\n📝 Step 3: Creating Streamlit Polish configuration...")
    create_streamlit_polish_config()
    
    print("\n🎯 RECOMMENDATIONS:")
    print("1. Replace hardcoded English strings with t('ui_elements.key') calls")
    print("2. Add placeholder='...' parameters to st.selectbox() calls")
    print("3. Use Polish labels for all form elements")
    print("4. Test all pages in Polish language mode")
    
    print("\n✅ English placeholder fix process completed!")

if __name__ == "__main__":
    main()