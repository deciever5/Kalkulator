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
        
        # Send inquiry and services
        'send_inquiry': 'Wyślij zapytanie',
        'send_inquiry_service': 'Usługa zapytań',
        'get_detailed_quote_text': 'Otrzymaj szczegółową ofertę dostosowaną do Twoich potrzeb',
        'analyze_drawings': 'Analizuj rysunki',
        'drawing_analysis_service': 'Analiza rysunków',
        'upload_drawings_estimate': 'Prześlij swoje rysunki techniczne, aby uzyskać dokładne wyceny',
        
        # Additional UI elements
        'configure_container': 'Skonfiguruj kontener',
        'simple_process_2_steps': 'Prosty proces w 2 krokach',
        'step_1_configuration': 'Krok 1: Konfiguracja',
        'choose_container_type': 'Wybierz typ kontenera i specyfikacje',
        'step_2_ai_quote': 'Krok 2: Oferta AI',
        'get_instant_quote': 'Otrzymaj natychmiastową wycenę dzięki AI',
        'start_configuration': 'Rozpocznij konfigurację',
        'get_quote': 'Otrzymaj ofertę',
        'additional_services': 'Dodatkowe usługi',
        'why_kan_bud': 'Dlaczego KAN-BUD',
        'precise_quotes': 'Precyzyjne wyceny',
        'fast_realization': 'Szybka realizacja',
        'full_service': 'Pełna obsługa',
        'ai_historical_data': 'AI + dane historyczne',
        'european_climate_standards': 'Europejskie standardy klimatyczne',
        'transparent_calculations': 'Przejrzyste kalkulacje',
        'hundreds_of_projects': 'Setki zrealizowanych projektów',
        'own_machinery': 'Własny park maszynowy',
        'poland_center': 'Centralna lokalizacja w Polsce',
        'design_execution': 'Projekt i wykonanie',
        'transport_assembly': 'Transport i montaż',
        'after_sales_support': 'Wsparcie posprzedażowe',
        
        # AI and cost estimation
        'no_configuration_found': 'Nie znaleziono konfiguracji',
        'current_configuration': 'Aktualna konfiguracja',
        'generate_ai_estimate': 'Wygeneruj szacunek AI',
        'ai.messages.generating': 'Generowanie szacunku...',
        'ai.messages.estimate_generated': 'Szacunek został wygenerowany',
        'ai_cost_estimate': 'Szacunek kosztów AI',
        'estimate_disclaimer_title': 'Ważne zastrzeżenie prawne',
        'estimate_disclaimer_text': 'Ten szacunek ma charakter orientacyjny i nie stanowi oferty handlowej. Ostateczna cena może się różnić od przedstawionego szacunku.',
        'get_precise_quote': 'Otrzymaj precyzyjną ofertę',
        'contact_for_quote': 'Skontaktuj się z nami, aby otrzymać szczegółową ofertę handlową dostosowaną do Twoich potrzeb.',
        'save_estimate': 'Zapisz szacunek',
        'estimate_saved': 'Szacunek został zapisany',
        'failed_generate_estimate': 'Nie udało się wygenerować szacunku',
        'error_generating_estimate': 'Błąd podczas generowania szacunku',
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
        
        # Send inquiry and services
        'send_inquiry': 'Send Inquiry',
        'send_inquiry_service': 'Inquiry Service',
        'get_detailed_quote_text': 'Get a detailed quote tailored to your project needs',
        'analyze_drawings': 'Analyze Drawings',
        'drawing_analysis_service': 'Drawing Analysis Service',
        'upload_drawings_estimate': 'Upload your technical drawings for accurate estimates',
        
        # Additional UI elements
        'configure_container': 'Configure Container',
        'simple_process_2_steps': 'Simple 2-step process',
        'step_1_configuration': 'Step 1: Configuration',
        'choose_container_type': 'Choose container type and specifications',
        'step_2_ai_quote': 'Step 2: AI Quote',
        'get_instant_quote': 'Get instant quote with AI',
        'start_configuration': 'Start Configuration',
        'get_quote': 'Get Quote',
        'additional_services': 'Additional Services',
        'why_kan_bud': 'Why KAN-BUD',
        'precise_quotes': 'Precise Quotes',
        'fast_realization': 'Fast Realization',
        'full_service': 'Full Service',
        'ai_historical_data': 'AI + Historical Data',
        'european_climate_standards': 'European Climate Standards',
        'transparent_calculations': 'Transparent Calculations',
        'hundreds_of_projects': 'Hundreds of Completed Projects',
        'own_machinery': 'Own Machine Fleet',
        'poland_center': 'Central Location in Poland',
        'design_execution': 'Design and Execution',
        'transport_assembly': 'Transport and Assembly',
        'after_sales_support': 'After-sales Support',
        
        # AI and cost estimation
        'no_configuration_found': 'No configuration found',
        'current_configuration': 'Current Configuration',
        'generate_ai_estimate': 'Generate AI Estimate',
        'ai.messages.generating': 'Generating estimate...',
        'ai.messages.estimate_generated': 'Estimate generated successfully',
        'ai_cost_estimate': 'AI Cost Estimate',
        'estimate_disclaimer_title': 'Important Legal Disclaimer',
        'estimate_disclaimer_text': 'This estimate is indicative and does not constitute a commercial offer. Final price may differ from the presented estimate.',
        'get_precise_quote': 'Get Precise Quote',
        'contact_for_quote': 'Contact us to receive a detailed commercial quote tailored to your needs.',
        'save_estimate': 'Save Estimate',
        'estimate_saved': 'Estimate saved',
        'failed_generate_estimate': 'Failed to generate estimate',
        'error_generating_estimate': 'Error generating estimate',
        
        # UI elements
        'ui.open': 'Open',
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