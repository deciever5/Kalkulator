#!/usr/bin/env python3
"""
Add Purposes Section to All Language Files
Adds the missing purposes section with proper translations to all language files
"""

import json
from pathlib import Path

# Purposes translations for all languages
PURPOSES_TRANSLATIONS = {
    'en': {
        "office_space": "Office Space",
        "sanitary_containers": "Sanitary Containers",
        "residential_containers": "Residential Containers",
        "commercial_containers": "Commercial Containers",
        "storage_containers": "Storage Containers",
        "technical_containers": "Technical Containers",
        "changing_rooms": "Changing Rooms",
        "guard_booths": "Guard Booths"
    },
    'de': {
        "office_space": "Büroraum",
        "sanitary_containers": "Sanitärcontainer",
        "residential_containers": "Wohncontainer",
        "commercial_containers": "Gewerbecontainer",
        "storage_containers": "Lagercontainer",
        "technical_containers": "Technische Container",
        "changing_rooms": "Umkleideräume",
        "guard_booths": "Wachhäuschen"
    },
    'fr': {
        "office_space": "Espace Bureau",
        "sanitary_containers": "Conteneurs Sanitaires",
        "residential_containers": "Conteneurs Résidentiels",
        "commercial_containers": "Conteneurs Commerciaux",
        "storage_containers": "Conteneurs de Stockage",
        "technical_containers": "Conteneurs Techniques",
        "changing_rooms": "Vestiaires",
        "guard_booths": "Guérites"
    },
    'es': {
        "office_space": "Espacio de Oficina",
        "sanitary_containers": "Contenedores Sanitarios",
        "residential_containers": "Contenedores Residenciales",
        "commercial_containers": "Contenedores Comerciales",
        "storage_containers": "Contenedores de Almacenamiento",
        "technical_containers": "Contenedores Técnicos",
        "changing_rooms": "Vestuarios",
        "guard_booths": "Casetas de Vigilancia"
    },
    'it': {
        "office_space": "Spazio Ufficio",
        "sanitary_containers": "Container Sanitari",
        "residential_containers": "Container Residenziali",
        "commercial_containers": "Container Commerciali",
        "storage_containers": "Container di Stoccaggio",
        "technical_containers": "Container Tecnici",
        "changing_rooms": "Spogliatoi",
        "guard_booths": "Cabine di Guardia"
    },
    'nl': {
        "office_space": "Kantoorruimte",
        "sanitary_containers": "Sanitaire Containers",
        "residential_containers": "Wooncontainers",
        "commercial_containers": "Commerciële Containers",
        "storage_containers": "Opslagcontainers",
        "technical_containers": "Technische Containers",
        "changing_rooms": "Kleedkamers",
        "guard_booths": "Wachthuisjes"
    },
    'cs': {
        "office_space": "Kancelářský Prostor",
        "sanitary_containers": "Sanitární Kontejnery",
        "residential_containers": "Obytné Kontejnery",
        "commercial_containers": "Komerční Kontejnery",
        "storage_containers": "Skladovací Kontejnery",
        "technical_containers": "Technické Kontejnery",
        "changing_rooms": "Šatny",
        "guard_booths": "Strážní Budky"
    },
    'hu': {
        "office_space": "Irodai Tér",
        "sanitary_containers": "Szaniter Konténerek",
        "residential_containers": "Lakókonténerek",
        "commercial_containers": "Kereskedelmi Konténerek",
        "storage_containers": "Raktározó Konténerek",
        "technical_containers": "Műszaki Konténerek",
        "changing_rooms": "Öltözők",
        "guard_booths": "Őrházak"
    },
    'sv': {
        "office_space": "Kontorsutrymme",
        "sanitary_containers": "Sanitära Containrar",
        "residential_containers": "Bostadscontainrar",
        "commercial_containers": "Kommersiella Containrar",
        "storage_containers": "Förvaringscontainrar",
        "technical_containers": "Tekniska Containrar",
        "changing_rooms": "Omklädningsrum",
        "guard_booths": "Vaktkurer"
    },
    'fi': {
        "office_space": "Toimistotila",
        "sanitary_containers": "Sanitaarikonttia",
        "residential_containers": "Asuinkonttia",
        "commercial_containers": "Kaupalliset Kontit",
        "storage_containers": "Varastokontit",
        "technical_containers": "Tekniset Kontit",
        "changing_rooms": "Pukuhuoneet",
        "guard_booths": "Vartiointikoppit"
    },
    'sk': {
        "office_space": "Kancelársky Priestor",
        "sanitary_containers": "Sanitárne Kontajnery",
        "residential_containers": "Obytné Kontajnery",
        "commercial_containers": "Komerčné Kontajnery",
        "storage_containers": "Skladovacie Kontajnery",
        "technical_containers": "Technické Kontajnery",
        "changing_rooms": "Šatne",
        "guard_booths": "Strážne Búdky"
    },
    'uk': {
        "office_space": "Офісний Простір",
        "sanitary_containers": "Санітарні Контейнери",
        "residential_containers": "Житлові Контейнери",
        "commercial_containers": "Комерційні Контейнери",
        "storage_containers": "Складські Контейнери",
        "technical_containers": "Технічні Контейнери",
        "changing_rooms": "Роздягальні",
        "guard_booths": "Сторожові Будки"
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

def add_purposes_to_language(filepath, language_code):
    """Add purposes section to a language file"""
    data = load_json_file(filepath)
    if not data:
        return False
    
    # Get the appropriate translations
    if language_code in PURPOSES_TRANSLATIONS:
        purposes = PURPOSES_TRANSLATIONS[language_code]
    else:
        # Fallback to English for unknown languages
        purposes = PURPOSES_TRANSLATIONS['en']
    
    # Add purposes section
    data["purposes"] = purposes
    
    return save_json_file(filepath, data)

def main():
    """Main function"""
    print("Adding purposes section to all language files...")
    
    locales_dir = Path('locales')
    language_files = [f for f in locales_dir.glob('*.json') 
                     if f.name != 'pl.json' and not f.name.endswith('.backup')]
    
    success_count = 0
    for lang_file in language_files:
        language_code = lang_file.stem
        print(f"Adding purposes to {language_code}...")
        
        if add_purposes_to_language(lang_file, language_code):
            success_count += 1
            print(f"  Successfully added purposes to {language_code}")
        else:
            print(f"  Failed to add purposes to {language_code}")
    
    print(f"\nCompleted: {success_count}/{len(language_files)} files updated")
    print("All language files now have the purposes section")

if __name__ == "__main__":
    main()