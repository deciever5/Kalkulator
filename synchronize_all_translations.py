#!/usr/bin/env python3
"""
Synchronize All Translation Structures
Ensures all language files have the same nested structure with proper translations
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

def get_missing_structures():
    """Get the missing translation structures for each language"""
    return {
        'en': {
            'ventilation': {
                'none': 'No ventilation',
                'gravity': 'Gravity ventilation',
                'wall_fans': 'Wall fans',
                'mechanical': 'Mechanical ventilation',
                'heat_recovery': 'Heat recovery',
                'split_ac': 'Split AC',
                'central_ac': 'Central AC',
                'industrial': 'Industrial ventilation'
            },
            'roof_modifications': {
                'none': 'No modifications',
                'insulation': 'Additional insulation',
                'skylight': 'Skylights',
                'fans': 'Roof fans',
                'solar': 'Solar panels',
                'antennas': 'Antennas',
                'sloped': 'Sloped roof',
                'terrace': 'Roof terrace',
                'snow_removal': 'Snow removal system'
            },
            'insulation': {
                'basic': 'Basic (50mm)',
                'standard': 'Standard (100mm)',
                'premium': 'Premium (150mm)',
                'extreme': 'Extreme (200mm)'
            },
            'windows': {
                'none': 'No windows',
                'one': '1 window',
                'two': '2 windows',
                'three': '3 windows',
                'four': '4 windows',
                'five_plus': '5+ windows'
            }
        },
        'fr': {
            'ventilation': {
                'none': 'Aucune ventilation',
                'gravity': 'Ventilation gravitaire',
                'wall_fans': 'Ventilateurs muraux',
                'mechanical': 'Ventilation mécanique',
                'heat_recovery': 'Récupération de chaleur',
                'split_ac': 'Climatisation split',
                'central_ac': 'Climatisation centrale',
                'industrial': 'Ventilation industrielle'
            },
            'roof_modifications': {
                'none': 'Aucune modification',
                'insulation': 'Isolation supplémentaire',
                'skylight': 'Lucarnes',
                'fans': 'Ventilateurs de toit',
                'solar': 'Panneaux solaires',
                'antennas': 'Antennes',
                'sloped': 'Toit en pente',
                'terrace': 'Terrasse de toit',
                'snow_removal': 'Système de déneigement'
            },
            'insulation': {
                'basic': 'Base (50mm)',
                'standard': 'Standard (100mm)',
                'premium': 'Premium (150mm)',
                'extreme': 'Extrême (200mm)'
            },
            'windows': {
                'none': 'Aucune fenêtre',
                'one': '1 fenêtre',
                'two': '2 fenêtres',
                'three': '3 fenêtres',
                'four': '4 fenêtres',
                'five_plus': '5+ fenêtres'
            }
        },
        'es': {
            'ventilation': {
                'none': 'Sin ventilación',
                'gravity': 'Ventilación por gravedad',
                'wall_fans': 'Ventiladores de pared',
                'mechanical': 'Ventilación mecánica',
                'heat_recovery': 'Recuperación de calor',
                'split_ac': 'AC split',
                'central_ac': 'AC central',
                'industrial': 'Ventilación industrial'
            },
            'roof_modifications': {
                'none': 'Sin modificaciones',
                'insulation': 'Aislamiento adicional',
                'skylight': 'Claraboyas',
                'fans': 'Ventiladores de techo',
                'solar': 'Paneles solares',
                'antennas': 'Antenas',
                'sloped': 'Techo inclinado',
                'terrace': 'Terraza en el techo',
                'snow_removal': 'Sistema de remoción de nieve'
            },
            'insulation': {
                'basic': 'Básico (50mm)',
                'standard': 'Estándar (100mm)',
                'premium': 'Premium (150mm)',
                'extreme': 'Extremo (200mm)'
            },
            'windows': {
                'none': 'Sin ventanas',
                'one': '1 ventana',
                'two': '2 ventanas',
                'three': '3 ventanas',
                'four': '4 ventanas',
                'five_plus': '5+ ventanas'
            }
        },
        'it': {
            'ventilation': {
                'none': 'Nessuna ventilazione',
                'gravity': 'Ventilazione a gravità',
                'wall_fans': 'Ventole a parete',
                'mechanical': 'Ventilazione meccanica',
                'heat_recovery': 'Recupero calore',
                'split_ac': 'AC split',
                'central_ac': 'AC centrale',
                'industrial': 'Ventilazione industriale'
            },
            'roof_modifications': {
                'none': 'Nessuna modifica',
                'insulation': 'Isolamento aggiuntivo',
                'skylight': 'Lucernari',
                'fans': 'Ventole del tetto',
                'solar': 'Pannelli solari',
                'antennas': 'Antenne',
                'sloped': 'Tetto inclinato',
                'terrace': 'Terrazza sul tetto',
                'snow_removal': 'Sistema rimozione neve'
            },
            'insulation': {
                'basic': 'Base (50mm)',
                'standard': 'Standard (100mm)',
                'premium': 'Premium (150mm)',
                'extreme': 'Estremo (200mm)'
            },
            'windows': {
                'none': 'Nessuna finestra',
                'one': '1 finestra',
                'two': '2 finestre',
                'three': '3 finestre',
                'four': '4 finestre',
                'five_plus': '5+ finestre'
            }
        }
    }

def add_missing_structures_to_language(lang_code):
    """Add missing translation structures to a language file"""
    print(f"Synchronizing {lang_code}...")
    
    filepath = f'locales/{lang_code}.json'
    data = load_json_file(filepath)
    if not data:
        return False
    
    structures = get_missing_structures()
    
    # Use English as fallback for languages not explicitly defined
    lang_structures = structures.get(lang_code, structures['en'])
    
    added_count = 0
    for structure_name, structure_data in lang_structures.items():
        if structure_name not in data:
            data[structure_name] = structure_data
            added_count += 1
            print(f"  Added {structure_name} structure")
        else:
            # Check for missing keys within the structure
            for key, value in structure_data.items():
                if key not in data[structure_name]:
                    data[structure_name][key] = value
                    print(f"  Added {structure_name}.{key}")
    
    if save_json_file(filepath, data):
        print(f"  ✓ Successfully synchronized {lang_code}")
        return True
    else:
        print(f"  ✗ Failed to update {lang_code}")
        return False

def main():
    """Main function"""
    print("Synchronizing translation structures across all languages...")
    
    # Languages that need missing structures added
    languages = ['en', 'fr', 'es', 'it', 'nl', 'cs', 'sk', 'hu', 'sv', 'fi', 'uk']
    
    for lang in languages:
        add_missing_structures_to_language(lang)
    
    print("Translation synchronization complete!")

if __name__ == "__main__":
    main()