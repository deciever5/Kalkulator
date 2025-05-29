"""
Complete Translation System - All text in 4 languages
Every visible text element is translated here
"""

import streamlit as st

# Complete translation dictionary - EVERY text element
TRANSLATIONS = {
    'pl': {
        # Navigation and buttons
        'back_to_home': '← Powrót do strony głównej',
        'go_to_ai_estimate': '🤖 Przejdź do Wyceny AI →',
        'ai_cost_estimation': 'Wycena AI',
        'container_configurator': 'Konfigurator Kontenerów',
        'language': 'Język',
        
        # Container Configurator - Main sections
        'base_container_spec': '🏗️ Specyfikacja Bazowa Kontenera',
        'purpose': '🎯 Przeznaczenie',
        'modification_requirements': '🔧 Wymagania Modyfikacji',
        
        # Form labels
        'container_type': 'Typ Kontenera',
        'main_purpose': 'Główne Przeznaczenie',
        'expected_occupancy': 'Przewidywana Obsada',
        'environment_label': 'Środowisko',
        'climate_zone_label': 'Strefa Klimatyczna',
        
        # Container specifications
        'length': 'Długość',
        'width': 'Szerokość',
        'height': 'Wysokość',
        'weight': 'Waga',
        
        # Help text
        'container_help': 'Wybierz bazowy typ kontenera do modyfikacji',
        'use_case_help': 'Wybierz główne przeznaczenie kontenera',
        'climate_help': 'Wybierz strefę klimatyczną dla odpowiedniej izolacji',
        
        # Container types
        '20ft Standard': '20ft Standard',
        '40ft Standard': '40ft Standard',
        '40ft High Cube': '40ft Wysokościowy',
        '20ft Refrigerated': '20ft Chłodniczy',
        
        # Use cases
        'Office Space': 'Przestrzeń Biurowa',
        'Residential Living': 'Mieszkalne',
        'Workshop/Manufacturing': 'Warsztat/Produkcja',
        'Storage/Warehouse': 'Magazyn',
        'Retail/Commercial': 'Handel',
        'Medical/Healthcare': 'Medyczne',
        'Educational': 'Edukacyjne',
        'Restaurant/Kitchen': 'Restauracja/Kuchnia',
        'Data Center': 'Centrum Danych',
        'Custom Industrial': 'Przemysł Specjalistyczny',
        
        # Environment types
        'Indoor': 'Wewnętrzne',
        'Outdoor': 'Zewnętrzne',
        'Marine': 'Morskie',
        'Industrial': 'Przemysłowe',
        
        # Climate zones
        'Central European': 'Europa Środkowa',
        'Scandinavian': 'Skandynawski',
        'Mediterranean': 'Śródziemnomorski',
        'Atlantic Maritime': 'Atlantycki Morski',
        'Continental': 'Kontynentalny',
        'Alpine': 'Alpejski',
        'Baltic': 'Bałtycki',
        'Temperate Oceanic': 'Umiarkowany Oceaniczny',
        
        # Modifications
        'structural_modifications': '🏗️ Modyfikacje Strukturalne',
        'structural_reinforcements': '🔨 Wzmocnienia Konstrukcyjne',
        'number_of_windows': 'Liczba Okien',
        'number_of_doors': 'Liczba Drzwi',
        'skylights': 'Świetliki',
        'ventilation_openings': 'Otwory Wentylacyjne',
        'wall_reinforcement': 'Wzmocnienie Ścian',
        'roof_reinforcement': 'Wzmocnienie Dachu',
        'floor_reinforcement': 'Wzmocnienie Podłogi',
        'additional_support': 'Dodatkowe Podpory',
        
        # Systems
        'electrical_system': 'System Elektryczny',
        'plumbing': 'Instalacja Wodna',
        'hvac': 'System HVAC',
        'insulation_type': 'Typ Izolacji',
        'electrical_needed': 'Czy potrzebny system elektryczny?',
        'plumbing_needed': 'Czy potrzebna instalacja wodna?',
        'hvac_needed': 'Czy potrzebny system HVAC?',
    },
    
    'en': {
        # Navigation and buttons
        'back_to_home': '← Back to Home',
        'go_to_ai_estimate': '🤖 Go to AI Estimate →',
        'ai_cost_estimation': 'AI Cost Estimation',
        'container_configurator': 'Container Configurator',
        'language': 'Language',
        
        # Container Configurator - Main sections
        'base_container_spec': '🏗️ Base Container Specification',
        'purpose': '🎯 Purpose',
        'modification_requirements': '🔧 Modification Requirements',
        
        # Form labels
        'container_type': 'Container Type',
        'main_purpose': 'Main Purpose',
        'expected_occupancy': 'Expected Occupancy',
        'environment_label': 'Environment',
        'climate_zone_label': 'Climate Zone',
        
        # Container specifications
        'length': 'Length',
        'width': 'Width',
        'height': 'Height',
        'weight': 'Weight',
        
        # Help text
        'container_help': 'Select base container type for modification',
        'use_case_help': 'Select main purpose of the container',
        'climate_help': 'Select climate zone for appropriate insulation',
        
        # Container types
        '20ft Standard': '20ft Standard',
        '40ft Standard': '40ft Standard',
        '40ft High Cube': '40ft High Cube',
        '20ft Refrigerated': '20ft Refrigerated',
        
        # Use cases
        'Office Space': 'Office Space',
        'Residential Living': 'Residential Living',
        'Workshop/Manufacturing': 'Workshop/Manufacturing',
        'Storage/Warehouse': 'Storage/Warehouse',
        'Retail/Commercial': 'Retail/Commercial',
        'Medical/Healthcare': 'Medical/Healthcare',
        'Educational': 'Educational',
        'Restaurant/Kitchen': 'Restaurant/Kitchen',
        'Data Center': 'Data Center',
        'Custom Industrial': 'Custom Industrial',
        
        # Environment types
        'Indoor': 'Indoor',
        'Outdoor': 'Outdoor',
        'Marine': 'Marine',
        'Industrial': 'Industrial',
        
        # Climate zones
        'Central European': 'Central European',
        'Scandinavian': 'Scandinavian',
        'Mediterranean': 'Mediterranean',
        'Atlantic Maritime': 'Atlantic Maritime',
        'Continental': 'Continental',
        'Alpine': 'Alpine',
        'Baltic': 'Baltic',
        'Temperate Oceanic': 'Temperate Oceanic',
        
        # Modifications
        'structural_modifications': '🏗️ Structural Modifications',
        'structural_reinforcements': '🔨 Structural Reinforcements',
        'number_of_windows': 'Number of Windows',
        'number_of_doors': 'Number of Doors',
        'skylights': 'Skylights',
        'ventilation_openings': 'Ventilation Openings',
        'wall_reinforcement': 'Wall Reinforcement',
        'roof_reinforcement': 'Roof Reinforcement',
        'floor_reinforcement': 'Floor Reinforcement',
        'additional_support': 'Additional Support',
        
        # Systems
        'electrical_system': 'Electrical System',
        'plumbing': 'Plumbing',
        'hvac': 'HVAC System',
        'insulation_type': 'Insulation Type',
        'electrical_needed': 'Electrical system needed?',
        'plumbing_needed': 'Plumbing installation needed?',
        'hvac_needed': 'HVAC system needed?',
    },
    
    'de': {
        # Navigation and buttons
        'back_to_home': '← Zurück zur Startseite',
        'go_to_ai_estimate': '🤖 Zur KI-Schätzung →',
        'ai_cost_estimation': 'KI-Kostenvoranschlag',
        'container_configurator': 'Container-Konfigurator',
        'language': 'Sprache',
        
        # Container Configurator - Main sections
        'base_container_spec': '🏗️ Container-Grundspezifikation',
        'purpose': '🎯 Zweck',
        'modification_requirements': '🔧 Änderungsanforderungen',
        
        # Form labels
        'container_type': 'Container-Typ',
        'main_purpose': 'Hauptzweck',
        'expected_occupancy': 'Erwartete Belegung',
        'environment_label': 'Umgebung',
        'climate_zone_label': 'Klimazone',
        
        # Container specifications
        'length': 'Länge',
        'width': 'Breite',
        'height': 'Höhe',
        'weight': 'Gewicht',
        
        # Help text
        'container_help': 'Basis-Container-Typ für Modifikation auswählen',
        'use_case_help': 'Hauptzweck des Containers auswählen',
        'climate_help': 'Klimazone für entsprechende Isolierung auswählen',
        
        # Container types
        '20ft Standard': '20ft Standard',
        '40ft Standard': '40ft Standard',
        '40ft High Cube': '40ft Hochcontainer',
        '20ft Refrigerated': '20ft Kühlcontainer',
        
        # Use cases
        'Office Space': 'Büroräume',
        'Residential Living': 'Wohnraum',
        'Workshop/Manufacturing': 'Werkstatt/Fertigung',
        'Storage/Warehouse': 'Lager',
        'Retail/Commercial': 'Handel',
        'Medical/Healthcare': 'Medizin/Gesundheit',
        'Educational': 'Bildung',
        'Restaurant/Kitchen': 'Restaurant/Küche',
        'Data Center': 'Rechenzentrum',
        'Custom Industrial': 'Industriell Speziell',
        
        # Environment types
        'Indoor': 'Innenbereich',
        'Outdoor': 'Außenbereich',
        'Marine': 'Marin',
        'Industrial': 'Industriell',
        
        # Climate zones
        'Central European': 'Mitteleuropäisch',
        'Scandinavian': 'Skandinavisch',
        'Mediterranean': 'Mediterran',
        'Atlantic Maritime': 'Atlantisch-maritim',
        'Continental': 'Kontinental',
        'Alpine': 'Alpin',
        'Baltic': 'Baltisch',
        'Temperate Oceanic': 'Gemäßigt-ozeanisch',
        
        # Modifications
        'structural_modifications': '🏗️ Strukturelle Änderungen',
        'structural_reinforcements': '🔨 Strukturelle Verstärkungen',
        'number_of_windows': 'Anzahl Fenster',
        'number_of_doors': 'Anzahl Türen',
        'skylights': 'Oberlichter',
        'ventilation_openings': 'Lüftungsöffnungen',
        'wall_reinforcement': 'Wandverstärkung',
        'roof_reinforcement': 'Dachverstärkung',
        'floor_reinforcement': 'Bodenverstärkung',
        'additional_support': 'Zusätzliche Stützen',
        
        # Systems
        'electrical_system': 'Elektrisches System',
        'plumbing': 'Sanitärinstallation',
        'hvac': 'Klima-/Lüftungssystem',
        'insulation_type': 'Isolierungstyp',
        'electrical_needed': 'Elektrisches System erforderlich?',
        'plumbing_needed': 'Sanitärinstallation erforderlich?',
        'hvac_needed': 'Klima-/Lüftungssystem erforderlich?',
    },
    
    'nl': {
        # Navigation and buttons
        'back_to_home': '← Terug naar start',
        'go_to_ai_estimate': '🤖 Naar AI-schatting →',
        'ai_cost_estimation': 'AI-kostenschatting',
        'container_configurator': 'Container-configurator',
        'language': 'Taal',
        
        # Container Configurator - Main sections
        'base_container_spec': '🏗️ Basis Container Specificatie',
        'purpose': '🎯 Doel',
        'modification_requirements': '🔧 Modificatie-eisen',
        
        # Form labels
        'container_type': 'Container Type',
        'main_purpose': 'Hoofddoel',
        'expected_occupancy': 'Verwachte Bezetting',
        'environment_label': 'Omgeving',
        'climate_zone_label': 'Klimaatzone',
        
        # Container specifications
        'length': 'Lengte',
        'width': 'Breedte',
        'height': 'Hoogte',
        'weight': 'Gewicht',
        
        # Help text
        'container_help': 'Selecteer basis container type voor modificatie',
        'use_case_help': 'Selecteer hoofddoel van de container',
        'climate_help': 'Selecteer klimaatzone voor juiste isolatie',
        
        # Container types
        '20ft Standard': '20ft Standaard',
        '40ft Standard': '40ft Standaard',
        '40ft High Cube': '40ft Hoog',
        '20ft Refrigerated': '20ft Gekoeld',
        
        # Use cases
        'Office Space': 'Kantoorruimte',
        'Residential Living': 'Woonruimte',
        'Workshop/Manufacturing': 'Werkplaats/Productie',
        'Storage/Warehouse': 'Opslag/Magazijn',
        'Retail/Commercial': 'Retail/Commercieel',
        'Medical/Healthcare': 'Medisch/Zorg',
        'Educational': 'Educatief',
        'Restaurant/Kitchen': 'Restaurant/Keuken',
        'Data Center': 'Datacenter',
        'Custom Industrial': 'Industrieel Speciaal',
        
        # Environment types
        'Indoor': 'Binnen',
        'Outdoor': 'Buiten',
        'Marine': 'Marien',
        'Industrial': 'Industrieel',
        
        # Climate zones
        'Central European': 'Midden-Europees',
        'Scandinavian': 'Scandinavisch',
        'Mediterranean': 'Mediterraan',
        'Atlantic Maritime': 'Atlantisch Maritiem',
        'Continental': 'Continentaal',
        'Alpine': 'Alpien',
        'Baltic': 'Baltisch',
        'Temperate Oceanic': 'Gematigd Oceanisch',
        
        # Modifications
        'structural_modifications': '🏗️ Structurele Modificaties',
        'structural_reinforcements': '🔨 Structurele Versterkingen',
        'number_of_windows': 'Aantal Ramen',
        'number_of_doors': 'Aantal Deuren',
        'skylights': 'Dakramen',
        'ventilation_openings': 'Ventilatie-openingen',
        'wall_reinforcement': 'Muurversterking',
        'roof_reinforcement': 'Dakversterking',
        'floor_reinforcement': 'Vloerversterking',
        'additional_support': 'Extra Ondersteuning',
        
        # Systems
        'electrical_system': 'Elektrisch Systeem',
        'plumbing': 'Leidingwerk',
        'hvac': 'HVAC Systeem',
        'insulation_type': 'Isolatietype',
        'electrical_needed': 'Elektrisch systeem nodig?',
        'plumbing_needed': 'Leidingwerk nodig?',
        'hvac_needed': 'HVAC systeem nodig?',
    }
}

def t(key, language=None):
    """Universal translation function - works everywhere"""
    if language is None:
        language = st.session_state.get('language', 'pl')
    
    return TRANSLATIONS.get(language, {}).get(key, key)

def translate_list(items, language=None):
    """Translate a list of items (for dropdowns)"""
    if language is None:
        language = st.session_state.get('language', 'pl')
    
    return [t(item, language) for item in items]

def render_language_selector():
    """Render language selector that updates everything"""
    language_options = {
        'pl': 'Polski 🇵🇱',
        'en': 'English 🇬🇧',
        'de': 'Deutsch 🇩🇪',
        'nl': 'Nederlands 🇳🇱'
    }
    
    current_lang = st.session_state.get('language', 'pl')
    
    col1, col2, col3 = st.columns([1, 2, 3])
    with col1:
        selected = st.selectbox(
            t('language'),
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(current_lang),
            key=f"lang_select_{id(st)}"
        )
        
        if selected != current_lang:
            st.session_state.language = selected
            st.rerun()