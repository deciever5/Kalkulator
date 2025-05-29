"""
Complete translations system for KAN-BUD Container Calculator
Comprehensive multilingual support for all application components
"""

# Complete translation dictionary with all required keys
TRANSLATIONS = {
    'pl': {
        # Navigation and UI
        'nav.home': 'Strona główna',
        'nav.configurator': 'Konfigurator kontenerów',
        'nav.ai_cost_estimation': 'Szacowanie kosztów AI',
        'nav.technical_analysis': 'Analiza techniczna',
        'nav.quote_generator': 'Generator ofert',
        'nav.comparison_tool': 'Narzędzie porównania',
        'nav.drawing_analysis': 'Analiza rysunków',
        'nav.3d_visualization': 'Wizualizacja 3D',
        
        # Main UI elements
        'ui.language_selector': 'Wybór języka',
        'ui.employee_login': 'Logowanie pracownika',
        'ui.password': 'Hasło',
        'ui.login': 'Zaloguj',
        'ui.logout': 'Wyloguj',
        'ui.cancel': 'Anuluj',
        'ui.logged_in': 'Zalogowano pomyślnie',
        'ui.wrong_password': 'Nieprawidłowe hasło',
        'ui.back_to_home': 'Powrót do strony głównej',
        'ui.go_to_configurator': 'Przejdź do konfiguratora',
        'ui.yes': 'Tak',
        'ui.no': 'Nie',
        
        # Container types
        'container.types.20ft_standard': 'Kontener 20ft standardowy',
        'container.types.40ft_standard': 'Kontener 40ft standardowy',
        'container.types.40ft_high_cube': 'Kontener 40ft high cube',
        'container.types.20ft_refrigerated': 'Kontener 20ft chłodniczy',
        
        # Basic terms
        'container_type': 'Typ kontenera',
        'purpose': 'Przeznaczenie',
        'environment': 'Środowisko',
        'finish_level': 'Poziom wykończenia',
        'flooring': 'Podłoga',
        'climate_zone': 'Strefa klimatyczna',
        'windows': 'Okna',
        'additional_doors': 'Dodatkowe drzwi',
        'yes': 'Tak',
        'no': 'Nie',
        
        # Contact information
        'contact_us': 'Skontaktuj się z nami',
        'address': 'Adres',
        'phone': 'Telefon',
        'email': 'Email',
        'working_hours': 'Godziny pracy',
        'mon_fri': 'Poniedziałek - Piątek',
        
        # AI and technical
        'ai_model_selection': 'Wybór modelu AI',
        'choose_ai_model': 'Wybierz model AI',
        'auto_select_best': 'Automatyczny wybór najlepszego',
        'ai_powered_estimation': 'Szacowanie kosztów wspomagane przez AI',
        
        # Quote generator
        'quote_generator.no_config': 'Brak konfiguracji kontenera',
        'quote_generator.go_to_configurator': 'Przejdź do konfiguratora',
        'quote_generator.quote_information': 'Informacje o ofercie',
        'quote_generator.customer_information': 'Informacje o kliencie',
        'quote_generator.customer_name': 'Nazwa klienta',
        'quote_generator.company_name': 'Nazwa firmy',
        'quote_generator.email_address': 'Adres email',
        'quote_generator.phone_number': 'Numer telefonu',
        'quote_generator.project_information': 'Informacje o projekcie',
        'quote_generator.project_name': 'Nazwa projektu',
        'quote_generator.project_location': 'Lokalizacja projektu',
        'quote_generator.delivery_address': 'Adres dostawy',
        
        # Common navigation
        'back_to_home': 'Powrót do strony głównej',
        'go_to_configurator': 'Przejdź do konfiguratora',
        
        # Container use cases
        'container.use_cases.office': 'Biuro',
        'container.use_cases.residential': 'Mieszkalny',
        'container.use_cases.storage': 'Magazyn',
        'container.use_cases.workshop': 'Warsztat',
        'container.use_cases.retail': 'Handel',
        'container.use_cases.cafe_restaurant': 'Kawiarnia/Restauracja',
        'container.use_cases.medical': 'Medyczny',
        'container.use_cases.education': 'Edukacja',
        
        # Container environment
        'container.environment.urban': 'Miejskie',
        'container.environment.rural': 'Wiejskie',
        'container.environment.industrial': 'Przemysłowe',
        'container.environment.coastal': 'Nadmorskie',
        'container.environment.mountain': 'Górskie',
        
        # Container finish levels
        'container.finish_levels.basic': 'Podstawowy',
        'container.finish_levels.standard': 'Standardowy',
        'container.finish_levels.premium': 'Premium',
        'container.finish_levels.luxury': 'Luksusowy',
        
        # Container flooring
        'container.flooring.plywood': 'Sklejka',
        'container.flooring.vinyl': 'Winyl',
        'container.flooring.laminate': 'Laminat',
        'container.flooring.hardwood': 'Drewno twarde',
        'container.flooring.carpet': 'Wykładzina',
        'container.flooring.ceramic_tiles': 'Płytki ceramiczne',
        
        # Container climate zones
        'container.climate_zones.temperate': 'Umiarkowana',
        'container.climate_zones.continental': 'Kontynentalna',
        'container.climate_zones.mediterranean': 'Śródziemnomorska',
        'container.climate_zones.northern': 'Północna',
        'container.climate_zones.alpine': 'Alpejska',
    },
    
    'en': {
        # Navigation and UI
        'nav.home': 'Home',
        'nav.configurator': 'Container Configurator',
        'nav.ai_cost_estimation': 'AI Cost Estimation',
        'nav.technical_analysis': 'Technical Analysis',
        'nav.quote_generator': 'Quote Generator',
        'nav.comparison_tool': 'Comparison Tool',
        'nav.drawing_analysis': 'Drawing Analysis',
        'nav.3d_visualization': '3D Visualization',
        
        # Main UI elements
        'ui.language_selector': 'Language Selector',
        'ui.employee_login': 'Employee Login',
        'ui.password': 'Password',
        'ui.login': 'Login',
        'ui.logout': 'Logout',
        'ui.cancel': 'Cancel',
        'ui.logged_in': 'Successfully logged in',
        'ui.wrong_password': 'Wrong password',
        'ui.back_to_home': 'Back to Home',
        'ui.go_to_configurator': 'Go to Configurator',
        'ui.yes': 'Yes',
        'ui.no': 'No',
        
        # Container types
        'container.types.20ft_standard': '20ft Standard Container',
        'container.types.40ft_standard': '40ft Standard Container',
        'container.types.40ft_high_cube': '40ft High Cube Container',
        'container.types.20ft_refrigerated': '20ft Refrigerated Container',
        
        # Basic terms
        'container_type': 'Container Type',
        'purpose': 'Purpose',
        'environment': 'Environment',
        'finish_level': 'Finish Level',
        'flooring': 'Flooring',
        'climate_zone': 'Climate Zone',
        'windows': 'Windows',
        'additional_doors': 'Additional Doors',
        'yes': 'Yes',
        'no': 'No',
        
        # Contact information
        'contact_us': 'Contact Us',
        'address': 'Address',
        'phone': 'Phone',
        'email': 'Email',
        'working_hours': 'Working Hours',
        'mon_fri': 'Monday - Friday',
        
        # AI and technical
        'ai_model_selection': 'AI Model Selection',
        'choose_ai_model': 'Choose AI Model',
        'auto_select_best': 'Auto-select Best',
        'ai_powered_estimation': 'AI-Powered Cost Estimation',
        
        # Quote generator
        'quote_generator.no_config': 'No container configuration',
        'quote_generator.go_to_configurator': 'Go to Configurator',
        'quote_generator.quote_information': 'Quote Information',
        'quote_generator.customer_information': 'Customer Information',
        'quote_generator.customer_name': 'Customer Name',
        'quote_generator.company_name': 'Company Name',
        'quote_generator.email_address': 'Email Address',
        'quote_generator.phone_number': 'Phone Number',
        'quote_generator.project_information': 'Project Information',
        'quote_generator.project_name': 'Project Name',
        'quote_generator.project_location': 'Project Location',
        'quote_generator.delivery_address': 'Delivery Address',
        
        # Common navigation
        'back_to_home': 'Back to Home',
        'go_to_configurator': 'Go to Configurator',
        
        # Container use cases
        'container.use_cases.office': 'Office',
        'container.use_cases.residential': 'Residential',
        'container.use_cases.storage': 'Storage',
        'container.use_cases.workshop': 'Workshop',
        'container.use_cases.retail': 'Retail',
        'container.use_cases.cafe_restaurant': 'Cafe/Restaurant',
        'container.use_cases.medical': 'Medical',
        'container.use_cases.education': 'Education',
        
        # Container environment
        'container.environment.urban': 'Urban',
        'container.environment.rural': 'Rural',
        'container.environment.industrial': 'Industrial',
        'container.environment.coastal': 'Coastal',
        'container.environment.mountain': 'Mountain',
        
        # Container finish levels
        'container.finish_levels.basic': 'Basic',
        'container.finish_levels.standard': 'Standard',
        'container.finish_levels.premium': 'Premium',
        'container.finish_levels.luxury': 'Luxury',
        
        # Container flooring
        'container.flooring.plywood': 'Plywood',
        'container.flooring.vinyl': 'Vinyl',
        'container.flooring.laminate': 'Laminate',
        'container.flooring.hardwood': 'Hardwood',
        'container.flooring.carpet': 'Carpet',
        'container.flooring.ceramic_tiles': 'Ceramic Tiles',
        
        # Container climate zones
        'container.climate_zones.temperate': 'Temperate',
        'container.climate_zones.continental': 'Continental',
        'container.climate_zones.mediterranean': 'Mediterranean',
        'container.climate_zones.northern': 'Northern',
        'container.climate_zones.alpine': 'Alpine',
    },
    
    'de': {
        # Navigation and UI
        'nav.home': 'Startseite',
        'nav.configurator': 'Container-Konfigurator',
        'nav.ai_cost_estimation': 'KI-Kostenschätzung',
        'nav.technical_analysis': 'Technische Analyse',
        'nav.quote_generator': 'Angebotsgenerator',
        'nav.comparison_tool': 'Vergleichstool',
        'nav.drawing_analysis': 'Zeichnungsanalyse',
        'nav.3d_visualization': '3D-Visualisierung',
        
        # Main UI elements
        'ui.language_selector': 'Sprachauswahl',
        'ui.employee_login': 'Mitarbeiter-Login',
        'ui.password': 'Passwort',
        'ui.login': 'Anmelden',
        'ui.logout': 'Abmelden',
        'ui.cancel': 'Abbrechen',
        'ui.logged_in': 'Erfolgreich angemeldet',
        'ui.wrong_password': 'Falsches Passwort',
        'ui.back_to_home': 'Zurück zur Startseite',
        'ui.go_to_configurator': 'Zum Konfigurator',
        'ui.yes': 'Ja',
        'ui.no': 'Nein',
        
        # Container types
        'container.types.20ft_standard': '20ft Standard-Container',
        'container.types.40ft_standard': '40ft Standard-Container',
        'container.types.40ft_high_cube': '40ft High Cube Container',
        'container.types.20ft_refrigerated': '20ft Kühlcontainer',
        
        # Basic terms
        'container_type': 'Container-Typ',
        'purpose': 'Zweck',
        'environment': 'Umgebung',
        'finish_level': 'Ausbaustufe',
        'flooring': 'Bodenbelag',
        'climate_zone': 'Klimazone',
        'windows': 'Fenster',
        'additional_doors': 'Zusätzliche Türen',
        'yes': 'Ja',
        'no': 'Nein',
        
        # Contact information
        'contact_us': 'Kontakt',
        'address': 'Adresse',
        'phone': 'Telefon',
        'email': 'E-Mail',
        'working_hours': 'Arbeitszeiten',
        'mon_fri': 'Montag - Freitag',
        
        # AI and technical
        'ai_model_selection': 'KI-Modell-Auswahl',
        'choose_ai_model': 'KI-Modell wählen',
        'auto_select_best': 'Automatisch Bestes wählen',
        'ai_powered_estimation': 'KI-gestützte Kostenschätzung',
        
        # Quote generator
        'quote_generator.no_config': 'Keine Container-Konfiguration',
        'quote_generator.go_to_configurator': 'Zum Konfigurator',
        'quote_generator.quote_information': 'Angebotsinformationen',
        'quote_generator.customer_information': 'Kundeninformationen',
        'quote_generator.customer_name': 'Kundenname',
        'quote_generator.company_name': 'Firmenname',
        'quote_generator.email_address': 'E-Mail-Adresse',
        'quote_generator.phone_number': 'Telefonnummer',
        'quote_generator.project_information': 'Projektinformationen',
        'quote_generator.project_name': 'Projektname',
        'quote_generator.project_location': 'Projektstandort',
        'quote_generator.delivery_address': 'Lieferadresse',
        
        # Common navigation
        'back_to_home': 'Zurück zur Startseite',
        'go_to_configurator': 'Zum Konfigurator',
        
        # Container use cases
        'container.use_cases.office': 'Büro',
        'container.use_cases.residential': 'Wohnbereich',
        'container.use_cases.storage': 'Lager',
        'container.use_cases.workshop': 'Werkstatt',
        'container.use_cases.retail': 'Einzelhandel',
        'container.use_cases.cafe_restaurant': 'Café/Restaurant',
        'container.use_cases.medical': 'Medizinisch',
        'container.use_cases.education': 'Bildung',
        
        # Container environment
        'container.environment.urban': 'Städtisch',
        'container.environment.rural': 'Ländlich',
        'container.environment.industrial': 'Industriell',
        'container.environment.coastal': 'Küsten',
        'container.environment.mountain': 'Gebirge',
        
        # Container finish levels
        'container.finish_levels.basic': 'Basis',
        'container.finish_levels.standard': 'Standard',
        'container.finish_levels.premium': 'Premium',
        'container.finish_levels.luxury': 'Luxus',
        
        # Container flooring
        'container.flooring.plywood': 'Sperrholz',
        'container.flooring.vinyl': 'Vinyl',
        'container.flooring.laminate': 'Laminat',
        'container.flooring.hardwood': 'Hartholz',
        'container.flooring.carpet': 'Teppich',
        'container.flooring.ceramic_tiles': 'Keramikfliesen',
        
        # Container climate zones
        'container.climate_zones.temperate': 'Gemäßigt',
        'container.climate_zones.continental': 'Kontinental',
        'container.climate_zones.mediterranean': 'Mediterran',
        'container.climate_zones.northern': 'Nördlich',
        'container.climate_zones.alpine': 'Alpin',
    },
    
    'nl': {
        # Navigation and UI
        'nav.home': 'Home',
        'nav.configurator': 'Container Configurator',
        'nav.ai_cost_estimation': 'AI Kostenschatting',
        'nav.technical_analysis': 'Technische Analyse',
        'nav.quote_generator': 'Offerte Generator',
        'nav.comparison_tool': 'Vergelijkingstool',
        'nav.drawing_analysis': 'Tekening Analyse',
        'nav.3d_visualization': '3D Visualisatie',
        
        # Main UI elements
        'ui.language_selector': 'Taal Selectie',
        'ui.employee_login': 'Medewerker Login',
        'ui.password': 'Wachtwoord',
        'ui.login': 'Inloggen',
        'ui.logout': 'Uitloggen',
        'ui.cancel': 'Annuleren',
        'ui.logged_in': 'Succesvol ingelogd',
        'ui.wrong_password': 'Verkeerd wachtwoord',
        'ui.back_to_home': 'Terug naar Home',
        'ui.go_to_configurator': 'Ga naar Configurator',
        'ui.yes': 'Ja',
        'ui.no': 'Nee',
        
        # Container types
        'container.types.20ft_standard': '20ft Standaard Container',
        'container.types.40ft_standard': '40ft Standaard Container',
        'container.types.40ft_high_cube': '40ft High Cube Container',
        'container.types.20ft_refrigerated': '20ft Gekoelde Container',
        
        # Basic terms
        'container_type': 'Container Type',
        'purpose': 'Doel',
        'environment': 'Omgeving',
        'finish_level': 'Afwerkingsniveau',
        'flooring': 'Vloerbedekking',
        'climate_zone': 'Klimaatzone',
        'windows': 'Ramen',
        'additional_doors': 'Extra Deuren',
        'yes': 'Ja',
        'no': 'Nee',
        
        # Contact information
        'contact_us': 'Contact',
        'address': 'Adres',
        'phone': 'Telefoon',
        'email': 'E-mail',
        'working_hours': 'Werkuren',
        'mon_fri': 'Maandag - Vrijdag',
        
        # AI and technical
        'ai_model_selection': 'AI Model Selectie',
        'choose_ai_model': 'Kies AI Model',
        'auto_select_best': 'Automatisch Beste Kiezen',
        'ai_powered_estimation': 'AI-Gedreven Kostenschatting',
        
        # Quote generator
        'quote_generator.no_config': 'Geen container configuratie',
        'quote_generator.go_to_configurator': 'Ga naar Configurator',
        'quote_generator.quote_information': 'Offerte Informatie',
        'quote_generator.customer_information': 'Klant Informatie',
        'quote_generator.customer_name': 'Klantnaam',
        'quote_generator.company_name': 'Bedrijfsnaam',
        'quote_generator.email_address': 'E-mailadres',
        'quote_generator.phone_number': 'Telefoonnummer',
        'quote_generator.project_information': 'Project Informatie',
        'quote_generator.project_name': 'Projectnaam',
        'quote_generator.project_location': 'Projectlocatie',
        'quote_generator.delivery_address': 'Bezorgadres',
        
        # Common navigation
        'back_to_home': 'Terug naar Home',
        'go_to_configurator': 'Ga naar Configurator',
        
        # Container use cases
        'container.use_cases.office': 'Kantoor',
        'container.use_cases.residential': 'Residentieel',
        'container.use_cases.storage': 'Opslag',
        'container.use_cases.workshop': 'Werkplaats',
        'container.use_cases.retail': 'Retail',
        'container.use_cases.cafe_restaurant': 'Café/Restaurant',
        'container.use_cases.medical': 'Medisch',
        'container.use_cases.education': 'Onderwijs',
        
        # Container environment
        'container.environment.urban': 'Stedelijk',
        'container.environment.rural': 'Landelijk',
        'container.environment.industrial': 'Industrieel',
        'container.environment.coastal': 'Kust',
        'container.environment.mountain': 'Berg',
        
        # Container finish levels
        'container.finish_levels.basic': 'Basis',
        'container.finish_levels.standard': 'Standaard',
        'container.finish_levels.premium': 'Premium',
        'container.finish_levels.luxury': 'Luxe',
        
        # Container flooring
        'container.flooring.plywood': 'Multiplex',
        'container.flooring.vinyl': 'Vinyl',
        'container.flooring.laminate': 'Laminaat',
        'container.flooring.hardwood': 'Hardhout',
        'container.flooring.carpet': 'Tapijt',
        'container.flooring.ceramic_tiles': 'Keramische Tegels',
        
        # Container climate zones
        'container.climate_zones.temperate': 'Gematigd',
        'container.climate_zones.continental': 'Continentaal',
        'container.climate_zones.mediterranean': 'Mediterraan',
        'container.climate_zones.northern': 'Noordelijk',
        'container.climate_zones.alpine': 'Alpien',
    }
}

def get_translation(key: str, language: str = 'pl') -> str:
    """Get translation for a specific key and language"""
    if language not in TRANSLATIONS:
        language = 'pl'  # Default to Polish
    
    # Try to get the translation
    translation = TRANSLATIONS[language].get(key, key)
    
    # If not found, try English as fallback
    if translation == key and language != 'en':
        translation = TRANSLATIONS['en'].get(key, key)
    
    return translation

def translate_options(options: list, language: str = 'pl') -> list:
    """Translate a list of options"""
    return [get_translation(option, language) for option in options]

def get_available_languages() -> list:
    """Get list of available languages"""
    return list(TRANSLATIONS.keys())