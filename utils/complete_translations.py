"""
Complete Translation System for KAN-BUD Container Calculator
Handles ALL text translations including dropdown options and navigation buttons
"""

import streamlit as st

# Complete translations dictionary for all texts in the application
COMPLETE_TRANSLATIONS = {
    'en': {
        # Navigation buttons
        'back_to_home': '← Back to Home',
        'go_to_ai_estimate': '🤖 Go to AI Estimate →',
        'go_to_configurator': '🔧 Go to Configurator',
        
        # Container types
        '20ft Standard': '20ft Standard',
        '40ft Standard': '40ft Standard',
        '40ft High Cube': '40ft High Cube',
        '20ft Refrigerated': '20ft Refrigerated',
        
        # Use cases
        'Office Space': 'Office Space',
        'Residential': 'Residential',
        'Storage': 'Storage',
        'Workshop': 'Workshop',
        'Retail': 'Retail',
        'Restaurant': 'Restaurant',
        'Medical': 'Medical',
        'Laboratory': 'Laboratory',
        
        # Environment types
        'Indoor': 'Indoor',
        'Outdoor': 'Outdoor',
        'Marine': 'Marine',
        'Industrial': 'Industrial',
        
        # Climate zones (European and African)
        'Central European': 'Central European',
        'Scandinavian': 'Scandinavian',
        'Mediterranean': 'Mediterranean',
        'Atlantic Maritime': 'Atlantic Maritime',
        'Continental': 'Continental',
        'Alpine': 'Alpine',
        'North African': 'North African',
        'Sub-Saharan': 'Sub-Saharan',
        
        # Finish levels
        'Basic': 'Basic',
        'Standard': 'Standard',
        'Premium': 'Premium',
        'Luxury': 'Luxury',
        
        # Flooring types
        'Plywood': 'Plywood',
        'Vinyl': 'Vinyl',
        'Carpet': 'Carpet',
        'Hardwood': 'Hardwood',
        'Polished Concrete': 'Polished Concrete',
        
        # Form labels
        'container_type': 'Container Type',
        'main_purpose': 'Main Purpose',
        'environment': 'Environment',
        'finish_level': 'Finish Level',
        'flooring': 'Flooring',
        'climate_zone': 'Climate Zone',
    },
    
    'pl': {
        # Navigation buttons
        'back_to_home': '← Powrót do strony głównej',
        'go_to_ai_estimate': '🤖 Przejdź do Wyceny AI →',
        'go_to_configurator': '🔧 Przejdź do Konfiguratora',
        
        # Container types
        '20ft Standard': '20ft Standard',
        '40ft Standard': '40ft Standard',
        '40ft High Cube': '40ft Wysokościowy',
        '20ft Refrigerated': '20ft Chłodniczy',
        
        # Use cases
        'Office Space': 'Przestrzeń Biurowa',
        'Residential': 'Mieszkalne',
        'Storage': 'Magazyn',
        'Workshop': 'Warsztat',
        'Retail': 'Handel',
        'Restaurant': 'Restauracja',
        'Medical': 'Medyczne',
        'Laboratory': 'Laboratorium',
        
        # Environment types
        'Indoor': 'Wewnętrzne',
        'Outdoor': 'Zewnętrzne',
        'Marine': 'Morskie',
        'Industrial': 'Przemysłowe',
        
        # Climate zones (European and African)
        'Central European': 'Europa Środkowa',
        'Scandinavian': 'Skandynawski',
        'Mediterranean': 'Śródziemnomorski',
        'Atlantic Maritime': 'Atlantycki Morski',
        'Continental': 'Kontynentalny',
        'Alpine': 'Alpejski',
        'North African': 'Północnoafrykański',
        'Sub-Saharan': 'Subsaharyjski',
        
        # Finish levels
        'Basic': 'Podstawowy',
        'Standard': 'Standardowy',
        'Premium': 'Premium',
        'Luxury': 'Luksusowy',
        
        # Flooring types
        'Plywood': 'Sklejka',
        'Vinyl': 'Winyl',
        'Carpet': 'Wykładzina',
        'Hardwood': 'Drewno',
        'Polished Concrete': 'Polerowany beton',
        
        # Form labels
        'container_type': 'Typ Kontenera',
        'main_purpose': 'Główne Przeznaczenie',
        'environment': 'Środowisko',
        'finish_level': 'Poziom Wykończenia',
        'flooring': 'Podłogi',
        'climate_zone': 'Strefa Klimatyczna',
    },
    
    'de': {
        # Navigation buttons
        'back_to_home': '← Zurück zur Startseite',
        'go_to_ai_estimate': '🤖 Zur KI-Schätzung →',
        'go_to_configurator': '🔧 Zum Konfigurator',
        
        # Container types
        '20ft Standard': '20ft Standard',
        '40ft Standard': '40ft Standard',
        '40ft High Cube': '40ft Hochcontainer',
        '20ft Refrigerated': '20ft Kühlcontainer',
        
        # Use cases
        'Office Space': 'Büroraum',
        'Residential': 'Wohnbereich',
        'Storage': 'Lager',
        'Workshop': 'Werkstatt',
        'Retail': 'Einzelhandel',
        'Restaurant': 'Restaurant',
        'Medical': 'Medizinisch',
        'Laboratory': 'Labor',
        
        # Environment types
        'Indoor': 'Innenbereich',
        'Outdoor': 'Außenbereich',
        'Marine': 'Marin',
        'Industrial': 'Industriell',
        
        # Climate zones (European and African)
        'Central European': 'Mitteleuropäisch',
        'Scandinavian': 'Skandinavisch',
        'Mediterranean': 'Mediterran',
        'Atlantic Maritime': 'Atlantisch-Maritim',
        'Continental': 'Kontinental',
        'Alpine': 'Alpin',
        'North African': 'Nordafrikanisch',
        'Sub-Saharan': 'Subsahara',
        
        # Finish levels
        'Basic': 'Basis',
        'Standard': 'Standard',
        'Premium': 'Premium',
        'Luxury': 'Luxus',
        
        # Flooring types
        'Plywood': 'Sperrholz',
        'Vinyl': 'Vinyl',
        'Carpet': 'Teppich',
        'Hardwood': 'Hartholz',
        'Polished Concrete': 'Polierter Beton',
        
        # Form labels
        'container_type': 'Container-Typ',
        'main_purpose': 'Hauptzweck',
        'environment': 'Umgebung',
        'finish_level': 'Ausstattungsgrad',
        'flooring': 'Bodenbelag',
        'climate_zone': 'Klimazone',
    },
    
    'nl': {
        # Navigation buttons
        'back_to_home': '← Terug naar Home',
        'go_to_ai_estimate': '🤖 Naar AI Schatting →',
        'go_to_configurator': '🔧 Naar Configurator',
        
        # Container types
        '20ft Standard': '20ft Standaard',
        '40ft Standard': '40ft Standaard',
        '40ft High Cube': '40ft Hoge Container',
        '20ft Refrigerated': '20ft Koel Container',
        
        # Use cases
        'Office Space': 'Kantoorruimte',
        'Residential': 'Residentieel',
        'Storage': 'Opslag',
        'Workshop': 'Werkplaats',
        'Retail': 'Winkel',
        'Restaurant': 'Restaurant',
        'Medical': 'Medisch',
        'Laboratory': 'Laboratorium',
        
        # Environment types
        'Indoor': 'Binnen',
        'Outdoor': 'Buiten',
        'Marine': 'Marien',
        'Industrial': 'Industrieel',
        
        # Climate zones (European and African)
        'Central European': 'Midden-Europees',
        'Scandinavian': 'Scandinavisch',
        'Mediterranean': 'Mediterraan',
        'Atlantic Maritime': 'Atlantisch Maritiem',
        'Continental': 'Continentaal',
        'Alpine': 'Alpien',
        'North African': 'Noord-Afrikaans',
        'Sub-Saharan': 'Sub-Sahara',
        
        # Finish levels
        'Basic': 'Basis',
        'Standard': 'Standaard',
        'Premium': 'Premium',
        'Luxury': 'Luxe',
        
        # Flooring types
        'Plywood': 'Multiplex',
        'Vinyl': 'Vinyl',
        'Carpet': 'Tapijt',
        'Hardwood': 'Hardhout',
        'Polished Concrete': 'Gepolijst Beton',
        
        # Form labels
        'container_type': 'Container Type',
        'main_purpose': 'Hoofddoel',
        'environment': 'Omgeving',
        'finish_level': 'Afwerkingsniveau',
        'flooring': 'Vloerbedekking',
        'climate_zone': 'Klimaatzone',
    }
}

def get_translation(key: str, language: str = None) -> str:
    """Get translation for any text key"""
    if language is None:
        language = st.session_state.get('language', 'pl')
    
    return COMPLETE_TRANSLATIONS.get(language, {}).get(key, key)

def translate_options(options: list, language: str = None) -> list:
    """Translate a list of dropdown options"""
    return [get_translation(option, language) for option in options]