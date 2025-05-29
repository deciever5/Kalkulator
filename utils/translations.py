"""
Unified Translation System for KAN-BUD Container Calculator
Simple, consistent translations across all pages
"""

import streamlit as st

# Complete translations for all visible text
TRANSLATIONS = {
    'pl': {
        # Navigation
        'back_to_home': '← Powrót do strony głównej',
        'go_to_ai_estimate': '🤖 Przejdź do Wyceny AI →',
        'go_to_configurator': '🔧 Przejdź do Konfiguratora',
        'language': 'Język / Language',
        'yes': 'Tak',
        'no': 'Nie',

        # Main sections
        'container_configurator': 'Konfigurator Kontenerów',
        'ai_cost_estimator': 'Wycena AI',
        'technical_analysis': 'Analiza Techniczna',

        # Form labels
        'container_type': 'Typ Kontenera',
        'main_purpose': 'Główne Przeznaczenie',
        'environment': 'Środowisko',
        'finish_level': 'Poziom Wykończenia',
        'flooring': 'Podłogi',
        'climate_zone': 'Strefa Klimatyczna',
        'number_of_windows': 'Liczba Okien',
        'additional_doors': 'Dodatkowe Drzwi',
        'electrical_system': 'System Elektryczny',
        'plumbing_system': 'System Hydrauliczny',
        'hvac_system': 'System HVAC',
        'insulation_package': 'Pakiet Izolacji',
        'structural_reinforcement': 'Wzmocnienie Konstrukcyjne',

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

        # Environment
        'Indoor': 'Wewnętrzne',
        'Outdoor': 'Zewnętrzne',
        'Marine': 'Morskie',
        'Industrial': 'Przemysłowe',

        # Finish levels
        'Basic': 'Podstawowy',
        'Standard': 'Standardowy',
        'Premium': 'Premium',
        'Luxury': 'Luksusowy',

        # Flooring
        'Plywood': 'Sklejka',
        'Vinyl': 'Winyl',
        'Carpet': 'Wykładzina',
        'Hardwood': 'Drewno',
        'Polished Concrete': 'Polerowany beton',

        # Climate zones
        'Central European': 'Europa Środkowa',
        'Scandinavian': 'Skandynawski',
        'Mediterranean': 'Śródziemnomorski',
        'Atlantic Maritime': 'Atlantycki Morski',
        'Continental': 'Kontynentalny',
        'Alpine': 'Alpejski',
        'Baltic': 'Bałtycki',
        'Temperate Oceanic': 'Umiarkowany Oceaniczny',

        # Systems
        'base_container_spec': 'Specyfikacja Podstawowa Kontenera',
        'modification_requirements': 'Wymagania Modyfikacji',
        'systems_installations': 'Systemy i Instalacje',
        'cost_breakdown': 'Rozbicie Kosztów',
        'generate_estimate': 'Generuj Wycenę',
        'configuration_summary': 'Podsumowanie Konfiguracji',
        'estimated_cost': 'Szacowany Koszt',
        'basic_cost': 'Koszt Podstawowy',
        'modifications_cost': 'Koszt Modyfikacji',
        'total_cost': 'Koszt Całkowity',

        # AI messages
        'generating_estimate': 'Generowanie wyceny AI...',
        'estimate_ready': 'Wycena gotowa!',
        'error_occurred': 'Wystąpił błąd',

        # Buttons
        'calculate': 'Oblicz',
        'reset': 'Resetuj',
        'save': 'Zapisz',
        'load': 'Wczytaj',
        'export': 'Eksportuj',
        'print': 'Drukuj',
        
        # Common
        'yes': 'Tak',
        'no': 'Nie',
        
        #yes/no
        'yes': 'Tak',
        'no': 'Nie',
    },

    'en': {
        # Navigation
        'back_to_home': '← Back to Home',
        'go_to_ai_estimate': '🤖 Go to AI Estimate →',
        'go_to_configurator': '🔧 Go to Configurator',
        'language': 'Language / Język',
        'yes': 'Yes',
        'no': 'No',

        # Main sections
        'container_configurator': 'Container Configurator',
        'ai_cost_estimator': 'AI Cost Estimator',
        'technical_analysis': 'Technical Analysis',

        # Form labels
        'container_type': 'Container Type',
        'main_purpose': 'Main Purpose',
        'environment': 'Environment',
        'finish_level': 'Finish Level',
        'flooring': 'Flooring',
        'climate_zone': 'Climate Zone',
        'number_of_windows': 'Number of Windows',
        'additional_doors': 'Additional Doors',
        'electrical_system': 'Electrical System',
        'plumbing_system': 'Plumbing System',
        'hvac_system': 'HVAC System',
        'insulation_package': 'Insulation Package',
        'structural_reinforcement': 'Structural Reinforcement',

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

        # Environment
        'Indoor': 'Indoor',
        'Outdoor': 'Outdoor',
        'Marine': 'Marine',
        'Industrial': 'Industrial',

        # Finish levels
        'Basic': 'Basic',
        'Standard': 'Standard',
        'Premium': 'Premium',
        'Luxury': 'Luxury',

        # Flooring
        'Plywood': 'Plywood',
        'Vinyl': 'Vinyl',
        'Carpet': 'Carpet',
        'Hardwood': 'Hardwood',
        'Polished Concrete': 'Polished Concrete',

        # Climate zones
        'Central European': 'Central European',
        'Scandinavian': 'Scandinavian',
        'Mediterranean': 'Mediterranean',
        'Atlantic Maritime': 'Atlantic Maritime',
        'Continental': 'Continental',
        'Alpine': 'Alpine',
        'Baltic': 'Baltic',
        'Temperate Oceanic': 'Temperate Oceanic',

        # Systems
        'base_container_spec': 'Base Container Specification',
        'modification_requirements': 'Modification Requirements',
        'systems_installations': 'Systems & Installations',
        'cost_breakdown': 'Cost Breakdown',
        'generate_estimate': 'Generate Estimate',
        'configuration_summary': 'Configuration Summary',
        'estimated_cost': 'Estimated Cost',
        'basic_cost': 'Basic Cost',
        'modifications_cost': 'Modifications Cost',
        'total_cost': 'Total Cost',

        # AI messages
        'generating_estimate': 'Generating AI estimate...',
        'estimate_ready': 'Estimate ready!',
        'error_occurred': 'An error occurred',

        # Buttons
        'calculate': 'Calculate',
        'reset': 'Reset',
        'save': 'Save',
        'load': 'Load',
        'export': 'Export',
        'print': 'Print',
        
        # Common
        'yes': 'Yes',
        'no': 'No',
        
        #yes/no
        'yes': 'Yes',
        'no': 'No',
    },

    'de': {
        # Navigation
        'back_to_home': '← Zurück zur Startseite',
        'go_to_ai_estimate': '🤖 Zur KI-Schätzung →',
        'go_to_configurator': '🔧 Zum Konfigurator',
        'language': 'Sprache / Language',
        'yes': 'Ja',
        'no': 'Nein',

        # Main sections
        'container_configurator': 'Container-Konfigurator',
        'ai_cost_estimator': 'KI-Kostenschätzer',
        'technical_analysis': 'Technische Analyse',

        # Form labels
        'container_type': 'Container-Typ',
        'main_purpose': 'Hauptzweck',
        'environment': 'Umgebung',
        'finish_level': 'Ausstattungsgrad',
        'flooring': 'Bodenbelag',
        'climate_zone': 'Klimazone',
        'number_of_windows': 'Anzahl Fenster',
        'additional_doors': 'Zusätzliche Türen',
        'electrical_system': 'Elektrisches System',
        'plumbing_system': 'Sanitärsystem',
        'hvac_system': 'HVAC-System',
        'insulation_package': 'Isolierungspaket',
        'structural_reinforcement': 'Strukturelle Verstärkung',

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

        # Environment
        'Indoor': 'Innenbereich',
        'Outdoor': 'Außenbereich',
        'Marine': 'Marin',
        'Industrial': 'Industriell',

        # Finish levels
        'Basic': 'Basis',
        'Standard': 'Standard',
        'Premium': 'Premium',
        'Luxury': 'Luxus',

        # Flooring
        'Plywood': 'Sperrholz',
        'Vinyl': 'Vinyl',
        'Carpet': 'Teppich',
        'Hardwood': 'Hartholz',
        'Polished Concrete': 'Polierter Beton',

        # Climate zones
        'Central European': 'Mitteleuropäisch',
        'Scandinavian': 'Skandinavisch',
        'Mediterranean': 'Mediterran',
        'Atlantic Maritime': 'Atlantisch-Maritim',
        'Continental': 'Kontinental',
        'Alpine': 'Alpin',
        'Baltic': 'Baltisch',
        'Temperate Oceanic': 'Gemäßigt Ozeanisch',

        # Systems
        'base_container_spec': 'Basis-Container-Spezifikation',
        'modification_requirements': 'Modifikationsanforderungen',
        'systems_installations': 'Systeme & Installationen',
        'cost_breakdown': 'Kostenaufschlüsselung',
        'generate_estimate': 'Schätzung generieren',
        'configuration_summary': 'Konfigurationszusammenfassung',
        'estimated_cost': 'Geschätzte Kosten',
        'basic_cost': 'Grundkosten',
        'modifications_cost': 'Modifikationskosten',
        'total_cost': 'Gesamtkosten',

        # AI messages
        'generating_estimate': 'KI-Schätzung wird generiert...',
        'estimate_ready': 'Schätzung bereit!',
        'error_occurred': 'Ein Fehler ist aufgetreten',

        # Buttons
        'calculate': 'Berechnen',
        'reset': 'Zurücksetzen',
        'save': 'Speichern',
        'load': 'Laden',
        'export': 'Exportieren',
        'print': 'Drucken',
        
        # Common
        'yes': 'Ja',
        'no': 'Nein',
        
        #yes/no
        'yes': 'Ja',
        'no': 'Nein',
    },

    'nl': {
        # Navigation
        'back_to_home': '← Terug naar Home',
        'go_to_ai_estimate': '🤖 Naar AI Schatting →',
        'go_to_configurator': '🔧 Naar Configurator',
        'language': 'Taal / Language',
        'yes': 'Ja',
        'no': 'Nee',

        # Main sections
        'container_configurator': 'Container Configurator',
        'ai_cost_estimator': 'AI Kostenschatter',
        'technical_analysis': 'Technische Analyse',

        # Form labels
        'container_type': 'Container Type',
        'main_purpose': 'Hoofddoel',
        'environment': 'Omgeving',
        'finish_level': 'Afwerkingsniveau',
        'flooring': 'Vloerbedekking',
        'climate_zone': 'Klimaatzone',
        'number_of_windows': 'Aantal Ramen',
        'additional_doors': 'Extra Deuren',
        'electrical_system': 'Elektrisch Systeem',
        'plumbing_system': 'Loodgieterswerk',
        'hvac_system': 'HVAC Systeem',
        'insulation_package': 'Isolatiepakket',
        'structural_reinforcement': 'Structurele Versterking',

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

        # Environment
        'Indoor': 'Binnen',
        'Outdoor': 'Buiten',
        'Marine': 'Marien',
        'Industrial': 'Industrieel',

        # Finish levels
        'Basic': 'Basis',
        'Standard': 'Standaard',
        'Premium': 'Premium',
        'Luxury': 'Luxe',

        # Flooring
        'Plywood': 'Multiplex',
        'Vinyl': 'Vinyl',
        'Carpet': 'Tapijt',
        'Hardwood': 'Hardhout',
        'Polished Concrete': 'Gepolijst Beton',

        # Climate zones
        'Central European': 'Midden-Europees',
        'Scandinavian': 'Scandinavisch',
        'Mediterranean': 'Mediterraan',
        'Atlantic Maritime': 'Atlantisch Maritiem',
        'Continental': 'Continentaal',
        'Alpine': 'Alpien',
        'Baltic': 'Baltisch',
        'Temperate Oceanic': 'Gematigd Oceanisch',

        # Systems
        'base_container_spec': 'Basis Container Specificatie',
        'modification_requirements': 'Modificatie Vereisten',
        'systems_installations': 'Systemen & Installaties',
        'cost_breakdown': 'Kostenverdeling',
        'generate_estimate': 'Genereer Schatting',
        'configuration_summary': 'Configuratie Samenvatting',
        'estimated_cost': 'Geschatte Kosten',
        'basic_cost': 'Basiskosten',
        'modifications_cost': 'Modificatiekosten',
        'total_cost': 'Totale Kosten',

        # AI messages
        'generating_estimate': 'AI schatting wordt gegenereerd...',
        'estimate_ready': 'Schatting klaar!',
        'error_occurred': 'Er is een fout opgetreden',

        # Buttons
        'calculate': 'Bereken',
        'reset': 'Reset',
        'save': 'Opslaan',
        'load': 'Laden',
        'export': 'Exporteren',
        'print': 'Afdrukken',
        
        # Common
        'yes': 'Ja',
        'no': 'Nee',
        
        #yes/no
        'yes': 'Ja',
        'no': 'Nee',
    }
}

def init_language():
    """Initialize language system"""
    if 'language' not in st.session_state:
        st.session_state.language = 'pl'

def get_current_language():
    """Get current language"""
    return st.session_state.get('language', 'pl')

def set_language(lang_code):
    """Set current language"""
    st.session_state.language = lang_code

def t(key, language=None):
    """Translate text key"""
    if language is None:
        language = get_current_language()

    return TRANSLATIONS.get(language, {}).get(key, key)

def translate_options(options, language=None):
    """Translate list of options"""
    if language is None:
        language = get_current_language()

    return [t(option, language) for option in options]

def render_language_selector():
    """Render language selector with flags"""
    init_language()

    language_options = {
        'pl': '🇵🇱 Polski',
        'en': '🇬🇧 English',
        'de': '🇩🇪 Deutsch',
        'nl': '🇳🇱 Nederlands'
    }

    current_lang = get_current_language()

    # Create columns for language selector
    col1, col2 = st.columns([2, 4])
    with col1:
        selected = st.selectbox(
            t('language'),
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(current_lang),
            key="lang_selector"
        )

        if selected != current_lang:
            set_language(selected)
            st.rerun()