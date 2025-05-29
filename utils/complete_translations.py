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
        'ai_cost_estimation': 'AI Cost Estimation',
        'container_configurator': 'Container Configurator',
        
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
        
        # European Climate zones
        'Central European': 'Central European',
        'Scandinavian': 'Scandinavian',
        'Mediterranean': 'Mediterranean',
        'Atlantic Maritime': 'Atlantic Maritime',
        'Continental': 'Continental',
        'Alpine': 'Alpine',
        'Baltic': 'Baltic',
        'Temperate Oceanic': 'Temperate Oceanic',
        
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
        
        # Additional options
        'number_of_windows': 'Number of Windows',
        'additional_doors': 'Additional Doors',
        'electrical_system': 'Electrical System',
        'plumbing_system': 'Plumbing System',
        'hvac_system': 'HVAC System',
        'insulation_package': 'Insulation Package',
        'structural_reinforcement': 'Structural Reinforcement',
        
        # Analysis types
        'Wind Load Analysis': 'Wind Load Analysis',
        'Seismic Analysis': 'Seismic Analysis',
        'Snow Load Analysis': 'Snow Load Analysis',
        'Foundation Analysis': 'Foundation Analysis',
        'Thermal Analysis': 'Thermal Analysis',
        
        # AI Models
        'OpenAI GPT-4o': 'OpenAI GPT-4o',
        'Anthropic Claude': 'Anthropic Claude',
        'Auto-Select Best': 'Auto-Select Best',
        
        # Customer types
        'Individual': 'Individual',
        'Business': 'Business',
        'Government': 'Government',
        'Non-Profit': 'Non-Profit',
        
        # Project sizes
        'Small': 'Small',
        'Medium': 'Medium',
        'Large': 'Large',
        'Extra Large': 'Extra Large',
        
        # Quote status
        'pending': 'Pending',
        'accepted': 'Accepted',
        'rejected': 'Rejected',
        'expired': 'Expired',
    },
    
    'pl': {
        # Navigation buttons
        'back_to_home': '← Powrót do strony głównej',
        'go_to_ai_estimate': '🤖 Przejdź do Wyceny AI →',
        'go_to_configurator': '🔧 Przejdź do Konfiguratora',
        'ai_cost_estimation': 'Wycena AI',
        'container_configurator': 'Konfigurator Kontenerów',
        
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
        
        # European Climate zones
        'Central European': 'Europa Środkowa',
        'Scandinavian': 'Skandynawski',
        'Mediterranean': 'Śródziemnomorski',
        'Atlantic Maritime': 'Atlantycki Morski',
        'Continental': 'Kontynentalny',
        'Alpine': 'Alpejski',
        'Baltic': 'Bałtycki',
        'Temperate Oceanic': 'Umiarkowany Oceaniczny',
        
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
        
        # Additional options
        'number_of_windows': 'Liczba Okien',
        'additional_doors': 'Dodatkowe Drzwi',
        'electrical_system': 'System Elektryczny',
        'plumbing_system': 'System Hydrauliczny',
        'hvac_system': 'System HVAC',
        'insulation_package': 'Pakiet Izolacji',
        'structural_reinforcement': 'Wzmocnienie Konstrukcyjne',
        
        # Analysis types
        'Wind Load Analysis': 'Analiza Obciążeń Wiatrem',
        'Seismic Analysis': 'Analiza Sejsmiczna',
        'Snow Load Analysis': 'Analiza Obciążeń Śniegiem',
        'Foundation Analysis': 'Analiza Fundamentów',
        'Thermal Analysis': 'Analiza Termiczna',
        
        # AI Models
        'OpenAI GPT-4o': 'OpenAI GPT-4o',
        'Anthropic Claude': 'Anthropic Claude',
        'Auto-Select Best': 'Automatyczny Wybór',
        
        # Customer types
        'Individual': 'Osoba Fizyczna',
        'Business': 'Firma',
        'Government': 'Instytucja Rządowa',
        'Non-Profit': 'Organizacja Non-Profit',
        
        # Project sizes
        'Small': 'Mały',
        'Medium': 'Średni',
        'Large': 'Duży',
        'Extra Large': 'Bardzo Duży',
        
        # Quote status
        'pending': 'Oczekujący',
        'accepted': 'Zaakceptowany',
        'rejected': 'Odrzucony',
        'expired': 'Wygasły',
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
        
        # European Climate zones
        'Central European': 'Mitteleuropäisch',
        'Scandinavian': 'Skandinavisch',
        'Mediterranean': 'Mediterran',
        'Atlantic Maritime': 'Atlantisch-Maritim',
        'Continental': 'Kontinental',
        'Alpine': 'Alpin',
        'Baltic': 'Baltisch',
        'Temperate Oceanic': 'Gemäßigt Ozeanisch',
        
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
        
        # Additional options
        'number_of_windows': 'Anzahl Fenster',
        'additional_doors': 'Zusätzliche Türen',
        'electrical_system': 'Elektrisches System',
        'plumbing_system': 'Sanitärsystem',
        'hvac_system': 'HVAC-System',
        'insulation_package': 'Isolierungspaket',
        'structural_reinforcement': 'Strukturelle Verstärkung',
        
        # Analysis types
        'Wind Load Analysis': 'Windlastanalyse',
        'Seismic Analysis': 'Seismische Analyse',
        'Snow Load Analysis': 'Schneelastanalyse',
        'Foundation Analysis': 'Fundamentanalyse',
        'Thermal Analysis': 'Thermische Analyse',
        
        # AI Models
        'OpenAI GPT-4o': 'OpenAI GPT-4o',
        'Anthropic Claude': 'Anthropic Claude',
        'Auto-Select Best': 'Automatische Auswahl',
        
        # Customer types
        'Individual': 'Privatperson',
        'Business': 'Unternehmen',
        'Government': 'Regierung',
        'Non-Profit': 'Gemeinnützig',
        
        # Project sizes
        'Small': 'Klein',
        'Medium': 'Mittel',
        'Large': 'Groß',
        'Extra Large': 'Sehr Groß',
        
        # Quote status
        'pending': 'Ausstehend',
        'accepted': 'Angenommen',
        'rejected': 'Abgelehnt',
        'expired': 'Abgelaufen',
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
        
        # European Climate zones
        'Central European': 'Midden-Europees',
        'Scandinavian': 'Scandinavisch',
        'Mediterranean': 'Mediterraan',
        'Atlantic Maritime': 'Atlantisch Maritiem',
        'Continental': 'Continentaal',
        'Alpine': 'Alpien',
        'Baltic': 'Baltisch',
        'Temperate Oceanic': 'Gematigd Oceanisch',
        
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
        
        # Additional options
        'number_of_windows': 'Aantal Ramen',
        'additional_doors': 'Extra Deuren',
        'electrical_system': 'Elektrisch Systeem',
        'plumbing_system': 'Loodgieterswerk',
        'hvac_system': 'HVAC Systeem',
        'insulation_package': 'Isolatiepakket',
        'structural_reinforcement': 'Structurele Versterking',
        
        # Analysis types
        'Wind Load Analysis': 'Windbelasting Analyse',
        'Seismic Analysis': 'Seismische Analyse',
        'Snow Load Analysis': 'Sneeuwbelasting Analyse',
        'Foundation Analysis': 'Fundament Analyse',
        'Thermal Analysis': 'Thermische Analyse',
        
        # AI Models
        'OpenAI GPT-4o': 'OpenAI GPT-4o',
        'Anthropic Claude': 'Anthropic Claude',
        'Auto-Select Best': 'Automatische Selectie',
        
        # Customer types
        'Individual': 'Particulier',
        'Business': 'Bedrijf',
        'Government': 'Overheid',
        'Non-Profit': 'Non-Profit',
        
        # Project sizes
        'Small': 'Klein',
        'Medium': 'Gemiddeld',
        'Large': 'Groot',
        'Extra Large': 'Extra Groot',
        
        # Quote status
        'pending': 'In Behandeling',
        'accepted': 'Geaccepteerd',
        'rejected': 'Afgewezen',
        'expired': 'Verlopen',
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