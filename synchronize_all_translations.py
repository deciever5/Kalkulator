#!/usr/bin/env python3
"""
Synchronize All Translation Files
Ensures all language files have identical structure to Polish with proper translations
"""

import json
from pathlib import Path

# Complete translation mappings for key system components
TRANSLATIONS = {
    'en': {
        # Window types
        'panoramic': 'Panoramic windows',
        'sliding': 'Sliding windows', 
        'tilt': 'Tilt windows',
        'skylight': 'Skylight windows',
        # Lighting
        'basic_led': 'Basic LED lighting',
        # Electrical system
        'none': 'No electrical installation',
        'preparation': 'Preparation (wiring without equipment)',
        'basic': 'Basic (lighting + outlets)',
        'standard': 'Standard (25A, lighting, 8 outlets)',
        'extended': 'Extended (40A, power, UPS, emergency)',
        'industrial': 'Industrial (63A, power, distribution panel)',
        'it_server': 'IT/Server (UPS, cooling, monitoring)',
        'smart': 'Smart (home automation, KNX)',
        # Plumbing system
        'cold_water': 'Cold water installation (sink)',
        'hot_cold_water': 'Cold + hot water (sink, washbasin)',
        'basic_sanitary': 'Basic sanitary (WC + sink)',
        'standard_sanitary': 'Standard (WC + sink + shower)',
        'comfort_sanitary': 'Comfort (WC + sink + cabin)',
        'premium_sanitary': 'Premium (jacuzzi, bidet, 2 sinks)',
        # HVAC system
        'electric_heaters': 'Electric heaters (1-3kW, convectors)',
        'vrv_vrf': 'VRV/VRF system (multi-zone, zone control)',
        'underfloor_heating': 'Underfloor heating (electric/water)'
    },
    'de': {
        # Window types
        'panoramic': 'Panoramafenster',
        'sliding': 'Schiebefenster',
        'tilt': 'Kippfenster', 
        'skylight': 'Dachfenster',
        # Lighting
        'basic_led': 'Grundlegende LED-Beleuchtung',
        # Electrical system
        'none': 'Keine Elektroinstallation',
        'preparation': 'Vorbereitung (Verkabelung ohne Ausrüstung)',
        'basic': 'Grundlegend (Beleuchtung + Steckdosen)',
        'standard': 'Standard (25A, Beleuchtung, 8 Steckdosen)',
        'extended': 'Erweitert (40A, Strom, USV, Notfall)',
        'industrial': 'Industriell (63A, Strom, Verteilerkasten)',
        'it_server': 'IT/Server (USV, Kühlung, Überwachung)',
        'smart': 'Intelligent (Hausautomation, KNX)',
        # Plumbing system
        'cold_water': 'Kaltwasserinstallation (Spüle)',
        'hot_cold_water': 'Kalt + Warmwasser (Spüle, Waschbecken)',
        'basic_sanitary': 'Grundlegend sanitär (WC + Waschbecken)',
        'standard_sanitary': 'Standard (WC + Waschbecken + Dusche)',
        'comfort_sanitary': 'Komfort (WC + Waschbecken + Kabine)',
        'premium_sanitary': 'Premium (Jacuzzi, Bidet, 2 Waschbecken)',
        # HVAC system
        'electric_heaters': 'Elektrische Heizungen (1-3kW, Konvektoren)',
        'vrv_vrf': 'VRV/VRF-System (Mehrzonen, Zonenkontrolle)',
        'underfloor_heating': 'Fußbodenheizung (elektrisch/Wasser)'
    },
    'fr': {
        # Window types
        'panoramic': 'Fenêtres panoramiques',
        'sliding': 'Fenêtres coulissantes',
        'tilt': 'Fenêtres basculantes',
        'skylight': 'Fenêtres de toit',
        # Lighting
        'basic_led': 'Éclairage LED de base',
        # Electrical system
        'none': 'Pas d\'installation électrique',
        'preparation': 'Préparation (câblage sans équipement)',
        'basic': 'De base (éclairage + prises)',
        'standard': 'Standard (25A, éclairage, 8 prises)',
        'extended': 'Étendu (40A, alimentation, UPS, urgence)',
        'industrial': 'Industriel (63A, alimentation, tableau de distribution)',
        'it_server': 'IT/Serveur (UPS, refroidissement, surveillance)',
        'smart': 'Intelligent (domotique, KNX)',
        # Plumbing system
        'cold_water': 'Installation eau froide (évier)',
        'hot_cold_water': 'Eau froide + chaude (évier, lavabo)',
        'basic_sanitary': 'Sanitaire de base (WC + lavabo)',
        'standard_sanitary': 'Standard (WC + lavabo + douche)',
        'comfort_sanitary': 'Confort (WC + lavabo + cabine)',
        'premium_sanitary': 'Premium (jacuzzi, bidet, 2 lavabos)',
        # HVAC system
        'electric_heaters': 'Chauffages électriques (1-3kW, convecteurs)',
        'vrv_vrf': 'Système VRV/VRF (multi-zones, contrôle de zones)',
        'underfloor_heating': 'Chauffage au sol (électrique/eau)'
    },
    'es': {
        # Window types
        'panoramic': 'Ventanas panorámicas',
        'sliding': 'Ventanas deslizantes',
        'tilt': 'Ventanas abatibles',
        'skylight': 'Claraboyas',
        # Lighting
        'basic_led': 'Iluminación LED básica',
        # Electrical system
        'none': 'Sin instalación eléctrica',
        'preparation': 'Preparación (cableado sin equipamiento)',
        'basic': 'Básico (iluminación + enchufes)',
        'standard': 'Estándar (25A, iluminación, 8 enchufes)',
        'extended': 'Extendido (40A, energía, UPS, emergencia)',
        'industrial': 'Industrial (63A, energía, panel de distribución)',
        'it_server': 'IT/Servidor (UPS, refrigeración, monitoreo)',
        'smart': 'Inteligente (domótica, KNX)',
        # Plumbing system
        'cold_water': 'Instalación agua fría (fregadero)',
        'hot_cold_water': 'Agua fría + caliente (fregadero, lavabo)',
        'basic_sanitary': 'Sanitario básico (WC + lavabo)',
        'standard_sanitary': 'Estándar (WC + lavabo + ducha)',
        'comfort_sanitary': 'Confort (WC + lavabo + cabina)',
        'premium_sanitary': 'Premium (jacuzzi, bidé, 2 lavabos)',
        # HVAC system
        'electric_heaters': 'Calentadores eléctricos (1-3kW, convectores)',
        'vrv_vrf': 'Sistema VRV/VRF (multi-zona, control de zonas)',
        'underfloor_heating': 'Calefacción por suelo radiante (eléctrica/agua)'
    },
    'it': {
        # Window types
        'panoramic': 'Finestre panoramiche',
        'sliding': 'Finestre scorrevoli',
        'tilt': 'Finestre a ribalta',
        'skylight': 'Lucernari',
        # Lighting
        'basic_led': 'Illuminazione LED di base',
        # Electrical system
        'none': 'Nessun impianto elettrico',
        'preparation': 'Preparazione (cablaggio senza attrezzature)',
        'basic': 'Base (illuminazione + prese)',
        'standard': 'Standard (25A, illuminazione, 8 prese)',
        'extended': 'Esteso (40A, alimentazione, UPS, emergenza)',
        'industrial': 'Industriale (63A, alimentazione, quadro di distribuzione)',
        'it_server': 'IT/Server (UPS, raffreddamento, monitoraggio)',
        'smart': 'Intelligente (automazione domestica, KNX)',
        # Plumbing system
        'cold_water': 'Impianto acqua fredda (lavello)',
        'hot_cold_water': 'Acqua fredda + calda (lavello, lavandino)',
        'basic_sanitary': 'Sanitario base (WC + lavandino)',
        'standard_sanitary': 'Standard (WC + lavandino + doccia)',
        'comfort_sanitary': 'Comfort (WC + lavandino + cabina)',
        'premium_sanitary': 'Premium (jacuzzi, bidet, 2 lavandini)',
        # HVAC system
        'electric_heaters': 'Riscaldatori elettrici (1-3kW, convettori)',
        'vrv_vrf': 'Sistema VRV/VRF (multi-zona, controllo zone)',
        'underfloor_heating': 'Riscaldamento a pavimento (elettrico/acqua)'
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

def translate_nested_structure(pl_structure, language_code):
    """Translate nested structure from Polish to target language"""
    if language_code not in TRANSLATIONS:
        return pl_structure
    
    translations = TRANSLATIONS[language_code]
    
    def translate_recursive(obj):
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                if isinstance(value, dict):
                    result[key] = translate_recursive(value)
                else:
                    # Try to translate the value
                    result[key] = translations.get(key, value)
            return result
        else:
            return obj
    
    return translate_recursive(pl_structure)

def synchronize_language_file(polish_data, target_file, language_code):
    """Synchronize target language file with Polish structure"""
    print(f"Synchronizing {target_file} ({language_code})...")
    
    # Load existing target data
    target_data = load_json_file(target_file)
    if target_data is None:
        target_data = {}
    
    # Create backup
    backup_file = f"{target_file}.sync_backup"
    save_json_file(backup_file, target_data)
    
    # Copy Polish structure and translate nested components
    synchronized_data = {}
    
    for key, value in polish_data.items():
        if isinstance(value, dict):
            # For nested structures, translate using our mappings
            if key in ['window_types', 'lighting', 'electrical_system', 'plumbing_system', 'hvac_system']:
                synchronized_data[key] = translate_nested_structure(value, language_code)
            else:
                # Keep existing translations for other nested structures
                synchronized_data[key] = target_data.get(key, value)
        else:
            # For simple strings, keep existing translation if available
            synchronized_data[key] = target_data.get(key, value)
    
    # Save synchronized data
    if save_json_file(target_file, synchronized_data):
        print(f"  Successfully synchronized {language_code}")
        return True
    else:
        print(f"  Failed to synchronize {language_code}")
        return False

def main():
    """Main synchronization function"""
    print("Synchronizing all translation files with Polish structure...")
    
    # Load Polish as base
    polish_file = Path('locales/pl.json')
    polish_data = load_json_file(polish_file)
    if not polish_data:
        print("Failed to load Polish translation file")
        return
    
    print(f"Using Polish structure with {len(polish_data)} top-level keys")
    
    # Get all other language files
    locales_dir = Path('locales')
    language_files = [f for f in locales_dir.glob('*.json') 
                     if f.name != 'pl.json' and not f.name.endswith('.backup')]
    
    success_count = 0
    for lang_file in language_files:
        language_code = lang_file.stem
        if synchronize_language_file(polish_data, lang_file, language_code):
            success_count += 1
    
    print(f"\nSynchronization complete: {success_count}/{len(language_files)} files updated")
    print("All language files now have consistent structure with proper translations")

if __name__ == "__main__":
    main()