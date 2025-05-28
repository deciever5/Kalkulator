"""
Multi-language Support for KAN-BUD Container Sales Calculator
Supports Polish, English, Dutch, and German
"""

TRANSLATIONS = {
    'en': {
        # Main navigation
        'title': 'KAN-BUD Container Sales Calculator',
        'subtitle': 'AI-Powered Cost Estimation for Container Modifications',
        'nav_configurator': 'Container Configurator',
        'nav_estimator': 'AI Cost Estimator',
        'nav_analysis': 'Technical Analysis',
        'nav_quotes': 'Quote Generator',
        'nav_comparison': 'Comparison Tool',
        
        # Common terms
        'container_type': 'Container Type',
        'use_case': 'Use Case',
        'modifications': 'Modifications',
        'cost': 'Cost',
        'total_cost': 'Total Cost',
        'estimate': 'Estimate',
        'generate': 'Generate',
        'save': 'Save',
        'export': 'Export',
        'configuration': 'Configuration',
        'analysis': 'Analysis',
        'quote': 'Quote',
        'customer': 'Customer',
        'project': 'Project',
        
        # Container types and use cases
        'office_space': 'Office Space',
        'residential_living': 'Residential Living',
        'workshop_manufacturing': 'Workshop/Manufacturing',
        'storage_warehouse': 'Storage/Warehouse',
        'retail_commercial': 'Retail/Commercial',
        
        # Measurements
        'length': 'Length',
        'width': 'Width',
        'height': 'Height',
        'weight': 'Weight',
        'meters': 'm',
        'kilograms': 'kg',
        'kilometers': 'km',
        
        # Buttons and actions
        'new_project': 'New Container Project',
        'get_estimate': 'Get AI Cost Estimate',
        'technical_analysis': 'Technical Analysis',
        'generate_quote': 'Generate Quote',
        'compare_options': 'Compare Options',
        'save_configuration': 'Save Configuration',
        
        # Messages
        'success_saved': 'Configuration saved successfully!',
        'error_complete_config': 'Please complete the configuration before saving.',
        'no_config_found': 'No container configuration found. Please configure your container first.',
        'estimate_generated': 'AI cost estimate generated successfully!',
        'quote_generated': 'Quote generated successfully!',
        
        # Company info
        'company_name': 'KAN-BUD',
        'company_address': 'Kąkolewo, Poland',
        'company_phone': '+48 123 456 789',
        'company_email': 'office@kan-bud.pl'
    },
    
    'pl': {
        # Main navigation
        'title': 'KAN-BUD Kalkulator Sprzedaży Kontenerów',
        'subtitle': 'Szacowanie Kosztów z AI dla Modyfikacji Kontenerów',
        'nav_configurator': 'Konfigurator Kontenerów',
        'nav_estimator': 'Szacowanie Kosztów AI',
        'nav_analysis': 'Analiza Techniczna',
        'nav_quotes': 'Generator Ofert',
        'nav_comparison': 'Narzędzie Porównań',
        
        # Common terms
        'container_type': 'Typ Kontenera',
        'use_case': 'Zastosowanie',
        'modifications': 'Modyfikacje',
        'cost': 'Koszt',
        'total_cost': 'Koszt Całkowity',
        'estimate': 'Szacunek',
        'generate': 'Generuj',
        'save': 'Zapisz',
        'export': 'Eksportuj',
        'configuration': 'Konfiguracja',
        'analysis': 'Analiza',
        'quote': 'Oferta',
        'customer': 'Klient',
        'project': 'Projekt',
        
        # Container types and use cases
        'office_space': 'Przestrzeń Biurowa',
        'residential_living': 'Mieszkanie',
        'workshop_manufacturing': 'Warsztat/Produkcja',
        'storage_warehouse': 'Magazyn',
        'retail_commercial': 'Handel/Komercja',
        
        # Measurements
        'length': 'Długość',
        'width': 'Szerokość',
        'height': 'Wysokość',
        'weight': 'Waga',
        'meters': 'm',
        'kilograms': 'kg',
        'kilometers': 'km',
        
        # Buttons and actions
        'new_project': 'Nowy Projekt Kontenera',
        'get_estimate': 'Uzyskaj Szacunek AI',
        'technical_analysis': 'Analiza Techniczna',
        'generate_quote': 'Generuj Ofertę',
        'compare_options': 'Porównaj Opcje',
        'save_configuration': 'Zapisz Konfigurację',
        
        # Messages
        'success_saved': 'Konfiguracja zapisana pomyślnie!',
        'error_complete_config': 'Proszę uzupełnić konfigurację przed zapisaniem.',
        'no_config_found': 'Nie znaleziono konfiguracji kontenera. Proszę najpierw skonfigurować kontener.',
        'estimate_generated': 'Szacunek kosztów AI wygenerowany pomyślnie!',
        'quote_generated': 'Oferta wygenerowana pomyślnie!',
        
        # Company info
        'company_name': 'KAN-BUD',
        'company_address': 'Kąkolewo, Polska',
        'company_phone': '+48 123 456 789',
        'company_email': 'biuro@kan-bud.pl'
    },
    
    'de': {
        # Main navigation
        'title': 'KAN-BUD Container Verkaufsrechner',
        'subtitle': 'KI-gestützte Kostenschätzung für Container-Modifikationen',
        'nav_configurator': 'Container Konfigurator',
        'nav_estimator': 'KI Kostenschätzer',
        'nav_analysis': 'Technische Analyse',
        'nav_quotes': 'Angebotsgenerator',
        'nav_comparison': 'Vergleichstool',
        
        # Common terms
        'container_type': 'Container Typ',
        'use_case': 'Anwendungsfall',
        'modifications': 'Modifikationen',
        'cost': 'Kosten',
        'total_cost': 'Gesamtkosten',
        'estimate': 'Schätzung',
        'generate': 'Generieren',
        'save': 'Speichern',
        'export': 'Exportieren',
        'configuration': 'Konfiguration',
        'analysis': 'Analyse',
        'quote': 'Angebot',
        'customer': 'Kunde',
        'project': 'Projekt',
        
        # Container types and use cases
        'office_space': 'Büroraum',
        'residential_living': 'Wohnraum',
        'workshop_manufacturing': 'Werkstatt/Fertigung',
        'storage_warehouse': 'Lager',
        'retail_commercial': 'Einzelhandel/Gewerbe',
        
        # Measurements
        'length': 'Länge',
        'width': 'Breite',
        'height': 'Höhe',
        'weight': 'Gewicht',
        'meters': 'm',
        'kilograms': 'kg',
        'kilometers': 'km',
        
        # Buttons and actions
        'new_project': 'Neues Container Projekt',
        'get_estimate': 'KI Kostenschätzung',
        'technical_analysis': 'Technische Analyse',
        'generate_quote': 'Angebot Erstellen',
        'compare_options': 'Optionen Vergleichen',
        'save_configuration': 'Konfiguration Speichern',
        
        # Messages
        'success_saved': 'Konfiguration erfolgreich gespeichert!',
        'error_complete_config': 'Bitte vervollständigen Sie die Konfiguration vor dem Speichern.',
        'no_config_found': 'Keine Container-Konfiguration gefunden. Bitte konfigurieren Sie zuerst Ihren Container.',
        'estimate_generated': 'KI-Kostenschätzung erfolgreich generiert!',
        'quote_generated': 'Angebot erfolgreich erstellt!',
        
        # Company info
        'company_name': 'KAN-BUD',
        'company_address': 'Kąkolewo, Polen',
        'company_phone': '+48 123 456 789',
        'company_email': 'buero@kan-bud.pl'
    },
    
    'nl': {
        # Main navigation
        'title': 'KAN-BUD Container Verkoop Calculator',
        'subtitle': 'AI-gestuurde Kostenschatting voor Container Modificaties',
        'nav_configurator': 'Container Configurator',
        'nav_estimator': 'AI Kostenschatter',
        'nav_analysis': 'Technische Analyse',
        'nav_quotes': 'Offerte Generator',
        'nav_comparison': 'Vergelijktool',
        
        # Common terms
        'container_type': 'Container Type',
        'use_case': 'Gebruiksdoel',
        'modifications': 'Modificaties',
        'cost': 'Kosten',
        'total_cost': 'Totale Kosten',
        'estimate': 'Schatting',
        'generate': 'Genereren',
        'save': 'Opslaan',
        'export': 'Exporteren',
        'configuration': 'Configuratie',
        'analysis': 'Analyse',
        'quote': 'Offerte',
        'customer': 'Klant',
        'project': 'Project',
        
        # Container types and use cases
        'office_space': 'Kantoorruimte',
        'residential_living': 'Woonruimte',
        'workshop_manufacturing': 'Werkplaats/Productie',
        'storage_warehouse': 'Opslag/Magazijn',
        'retail_commercial': 'Detailhandel/Commercieel',
        
        # Measurements
        'length': 'Lengte',
        'width': 'Breedte',
        'height': 'Hoogte',
        'weight': 'Gewicht',
        'meters': 'm',
        'kilograms': 'kg',
        'kilometers': 'km',
        
        # Buttons and actions
        'new_project': 'Nieuw Container Project',
        'get_estimate': 'AI Kostenschatting',
        'technical_analysis': 'Technische Analyse',
        'generate_quote': 'Offerte Genereren',
        'compare_options': 'Opties Vergelijken',
        'save_configuration': 'Configuratie Opslaan',
        
        # Messages
        'success_saved': 'Configuratie succesvol opgeslagen!',
        'error_complete_config': 'Voltooi de configuratie voordat u opslaat.',
        'no_config_found': 'Geen container configuratie gevonden. Configureer eerst uw container.',
        'estimate_generated': 'AI kostenschatting succesvol gegenereerd!',
        'quote_generated': 'Offerte succesvol gegenereerd!',
        
        # Company info
        'company_name': 'KAN-BUD',
        'company_address': 'Kąkolewo, Polen',
        'company_phone': '+48 123 456 789',
        'company_email': 'kantoor@kan-bud.pl'
    }
}

def get_text(key: str, language: str = 'en') -> str:
    """Get translated text for a given key and language"""
    return TRANSLATIONS.get(language, TRANSLATIONS['en']).get(key, key)

def get_available_languages() -> dict:
    """Get available languages with their display names"""
    return {
        'en': '🇬🇧 English',
        'pl': '🇵🇱 Polski',
        'de': '🇩🇪 Deutsch', 
        'nl': '🇳🇱 Nederlands'
    }