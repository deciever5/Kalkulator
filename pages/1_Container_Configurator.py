# Page configuration - MUST BE FIRST
import streamlit as st
st.set_page_config(
    page_title="Container Configurator - KAN-BUD",
    page_icon="📦",
    layout="wide"
)

import pandas as pd
from utils.container_database import ContainerDatabase
from utils.calculations import calculate_container_cost
from utils.translations import t, init_language, get_current_language, set_language
from utils.shared_header import render_shared_header

init_language()

# Initialize session state for login
if 'employee_logged_in' not in st.session_state:
    st.session_state.employee_logged_in = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# Load animations
from utils.animations import add_hover_animations, show_loading_animation, create_animated_counter
add_hover_animations()

# Render shared header without login button
render_shared_header(show_login=False, current_page="Container_Configurator")

st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
.header-title {
    color: white;
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}
.header-subtitle {
    color: #e8f4f8;
    font-size: 1.2rem;
    text-align: center;
}
.section-header {
    background: linear-gradient(90deg, #f8fafc 0%, #e2e8f0 100%);
    border-left: 5px solid #3b82f6;
    padding: 1rem 1.5rem;
    margin: 1.5rem 0 1rem 0;
    border-radius: 0 10px 10px 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.section-title {
    color: #1e40af;
    font-size: 1.3rem;
    font-weight: 600;
    margin: 0;
}
.config-section {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    border: 1px solid #e8f4f8;
    margin-bottom: 1rem;
}
.cost-summary {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin-top: 2rem;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
}
.cost-breakdown {
    background: rgba(255, 255, 255, 0.1);
    padding: 1rem;
    border-radius: 10px;
    margin-top: 1rem;
}
.special-notes {
    background: #fffbeb;
    border: 1px solid #f59e0b;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="main-header">
    <div class="header-title">📦 {t('nav.container_configurator')}</div>
    <div class="header-subtitle">{t('container_configurator_desc')}</div>
</div>
""", unsafe_allow_html=True)

# Initialize configuration
if 'container_config' not in st.session_state:
    st.session_state.container_config = {}

# Configuration form
with st.form("container_configuration_form"):

    # SECTION 1: BASIC CONFIGURATION
    st.markdown(f"""
    <div class="section-header">
        <div class="section-title">🏗️ {t('basic_configuration', 'PODSTAWOWA KONFIGURACJA')}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Container Type
        container_type_options = [
            t('container.types.10ft_compact', '10ft Compact (3m x 2.4m)'),
            t('container.types.20ft_standard', '20ft Standard (6m x 2.4m)'), 
            t('container.types.20ft_high_cube', '20ft High Cube (6m x 2.7m)'),
            t('container.types.40ft_standard', '40ft Standard (12m x 2.4m)'),
            t('container.types.40ft_hc', '40ft High Cube (12m x 2.7m)'),
            t('container.types.multi_unit', 'Multi-unit Container'),
            t('container.types.custom_size', 'Custom Size Container'),
            t('container.types.refurbished', 'Refurbished Container')
        ]
        container_type = st.selectbox(
            t('container_type', 'Container Type'),
            options=container_type_options,
            index=3
        )

        # Construction Material
        construction_material_options = [
            t('materials.steel_standard', 'Steel (standard construction)'),
            t('materials.aluminum_light', 'Aluminum (lightweight construction)'), 
            t('materials.composite_specialist', 'Composite material (specialist)')
        ]
        construction_material = st.selectbox(
            t('construction_material', 'Construction Material'),
            options=construction_material_options
        )

        # Insulation
        insulation_options = [
            t('insulation.none', 'No insulation'),
            t('insulation.basic', 'Basic (PUR foam 5-8cm)'),
            t('insulation.advanced', 'Advanced (mineral wool 10-15cm)'),
            t('insulation.premium', 'Premium (sandwich panels 15-20cm)')
        ]
        insulation = st.selectbox(
            t('insulation', 'Insulation'),
            options=insulation_options,
            index=1
        )

        # Main Purpose
        main_purpose_options = [
            t('purposes.office_space', 'Office Space'),
            t('purposes.sanitary_containers', 'Sanitary Containers'), 
            t('purposes.residential_containers', 'Residential Containers'),
            t('purposes.commercial_containers', 'Commercial Containers'),
            t('purposes.storage_containers', 'Storage Containers'),
            t('purposes.technical_containers', 'Technical Containers'),
            t('purposes.changing_rooms', 'Changing Rooms'),
            t('purposes.guard_booths', 'Guard Booths')
        ]
        main_purpose = st.selectbox(
            t('main_purpose', 'Main Purpose'),
            options=main_purpose_options
        )

    with col2:
        # Usage Environment
        environment_options = [
            t('environments.indoor', 'Indoor (halls, warehouses)'),
            t('environments.outdoor_standard', 'Outdoor standard (temperate climate)'),
            t('environments.outdoor_extreme', 'Outdoor extreme (coastal, mountains)'),
            t('environments.industrial', 'Industrial (plants, refineries, mines)'),
            t('environments.construction', 'Construction (building sites, infrastructure)'),
            t('environments.agricultural', 'Agricultural (farms, facilities)'),
            t('environments.marine', 'Marine/shipyard (corrosive environment)')
        ]
        environment = st.selectbox(
            t('usage_environment', 'Usage Environment'),
            options=environment_options,
            index=1
        )

        # Finish Level
        finish_level = st.selectbox(
            t('finish_level', 'Poziom Wykończenia'),
            options=[
                "Bez wykończenia (kontener techniczny, szkielet)",
                "Shell (izolacja + płyta OSB)",
                "Podstawowy (izolacja + wykończenie techniczne)",
                "Standardowy (pełna izolacja + wykończenie użytkowe)",
                "Komfortowy (izolacja premium + wykończenie biurowe)",
                "Luksusowy (najwyższa klasa + wykończenie hotelowe)",
                "Specjalistyczny (normy medyczne/laboratoryjne)"
            ],
            index=3
        )

        # Flooring
        flooring = st.selectbox(
            t('flooring', 'Podłogi'),
            options=[
                "Bez podłogi (blacha falistowana)",
                "Sklejka wodoodporna 18mm (standard)",
                "Sklejka antypoślizgowa 21mm",
                "Panele laminowane AC4/AC5",
                "Panele winylowe (LVT) wodoodporne",
                "Wykładzina PVC 2-4mm",
                "Płytki ceramiczne antypoślizgowe",
                "Posadzka epoksydowa przemysłowa",
                "Parkiet 3-warstwowy",
                "Gres techniczny R11/R12",
                "Podłoga podwyższona (serwerownie)"
            ],
            index=1
        )

        # Climate Zone
        climate_zone = st.selectbox(
            t('climate_zone', 'Strefa Klimatyczna'),
            options=[
                "Europa Północna (Skandynawia, -30°C do +25°C)",
                "Europa Środkowa (Polska, Niemcy, -20°C do +35°C)",
                "Europa Południowa (Hiszpania, Włochy, -5°C do +45°C)",
                "Klimat kontynentalny (ekstremalne wahania)",
                "Klimat morski (wysoka wilgotność)",
                "Klimat górski (wysokie UV, śnieg)",
                "Klimat tropikalny (wysokie temperatury, wilgotność)"
            ],
            index=1
        )

    # SECTION 2: SYSTEMS AND INSTALLATIONS
    st.markdown(f"""
    <div class="section-header">
        <div class="section-title">⚙️ {t('systems_installations', 'SYSTEMY I INSTALACJE')}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        # Windows
        num_windows = st.selectbox(
            t('number_of_windows', 'Liczba Okien'),
            options=[
                "Bez okien (kontener zamknięty)",
                "1 okno",
                "2 okna", 
                "3 okna",
                "4 okna",
                "5+ okien (konfiguracja custom)"
            ]
        )

        window_types = st.multiselect(
            t('window_types', 'Typ Okien'),
            options=[
                "Standardowe (100x80cm)",
                "Panoramiczne (150x120cm)",
                "Przesuwne",
                "Uchylne",
                "Antywłamaniowe (klasa P4-P8)",
                "Energooszczędne (3-szybowe)",
                "Świetliki dachowe (dodatkowo)"
            ]
        )

        # Lighting
        lighting = st.selectbox(
            t('lighting', 'Oświetlenie'),
            options=[
                "Brak oświetlenia",
                "Standardowe LED (podstawowe)",
                "Energooszczędne LED z czujnikami",
                "Oświetlenie zewnętrzne (reflektory)",
                "Oświetlenie awaryjne (akumulatorowe)",
                "System inteligentny (smart lighting)"
            ],
            index=1
        )

    with col2:
        # Ventilation
        ventilation = st.selectbox(
            "Nawiewy i Wentylacja",
            options=[
                "Bez nawiewów (naturalnych i mechanicznych)",
                "Nawiewy grawitacyjne (2-4 szt., regulowane)",
                "Wentylatory ściennie (wyciąg 100-150mm)",
                "Wentylacja mechaniczna (nawiew + wyciąg)",
                "Rekuperacja (odzysk ciepła 80-95%)",
                "Klimatyzacja split (1-3 jednostki)",
                "Klimatyzacja centralna (VRV/VRF)",
                "Wentylacja przemysłowa (ATEX, chemoodporna)"
            ],
            index=1
        )

        # Roof Modifications
        roof_modifications = st.selectbox(
            "Modyfikacje Dachu",
            options=[
                "Bez modyfikacji (dach standardowy płaski)",
                "Izolacja dachu dodatkowo (10-20cm)",
                "Świetlik dachowy (60x60, 90x90, 120x120cm)",
                "Wentylatory dachowe (przemysłowe, ciche)",
                "Instalacja fotowoltaiczna (2-10kW)",
                "Anteny/maszty (GSM, radio, satelitarne)",
                "Dach skośny (jednostronny, dwuspadowy)",
                "Taras dachowy (z balustradą)",
                "Systemy odśnieżania (grzałki, rynny)"
            ]
        )

        # Electrical System
        electrical_system = st.selectbox(
            "System Elektryczny",
            options=[
                "Bez instalacji elektrycznej",
                "Przygotowanie elektryczne (tylko przepusty)",
                "Podstawowy (15A, LED, 4 gniazdka)",
                "Standardowy (25A, oświetlenie, 8 gniazdków)",
                "Rozszerzony (40A, siła, UPS, emergency)",
                "Przemysłowy (63A, 3-fazowy, rozdzielnica)",
                "IT/Serwerownia (UPS, stabilizatory, monitoring)",
                "Inteligentny (smart home, KNX, automatyka)"
            ],
            index=3
        )

    with col3:
        # Plumbing System
        plumbing_system = st.selectbox(
            "System Hydrauliczny",
            options=[
                "Bez instalacji wodnej",
                "Przygotowanie hydrauliczne (tylko przepusty)",
                "Instalacja zimna woda (umywalka)",
                "Zimna + ciepła woda (umywalka, zlewozmywak)",
                "Podstawowy węzeł sanitarny (WC + umywalka)",
                "Standardowy węzeł (WC + umywalka + prysznic)",
                "Komfortowy węzeł (WC + umywalka + kabina)",
                "Premium węzeł (jacuzzi, bidé, 2 umywalki)",
                "Instalacja przemysłowa (ciśnieniowa, filtracja)"
            ]
        )

        # HVAC System
        hvac_system = st.selectbox(
            "System HVAC (Ogrzewanie/Chłodzenie)",
            options=[
                "Bez HVAC (bez ogrzewania i chłodzenia)",
                "Grzejniki elektryczne (1-3kW, konwektory)",
                "Ogrzewanie elektryczne (promienniki IR)",
                "Pompa ciepła (split, wydajność 2-12kW)",
                "Ogrzewanie gazowe (piec kondensacyjny)",
                "Klimatyzacja split (chłodzenie + grzanie)",
                "System VRV/VRF (multi-split, sterowanie strefowe)",
                "Ogrzewanie podłogowe (elektryczne/wodne)",
                "Centrala klimatyzacyjna (z filtracją, nawilżaniem)"
            ],
            index=5
        )

    # Special Comments for Systems
    st.markdown("### Uwagi Specjalne - Systemy")
    system_comments = st.text_area(
        "Opisz dodatkowe wymagania dotyczące systemów...",
        placeholder="np. Specjalne wymagania dla wentylacji, dodatkowe gniazdka, specjalistyczne instalacje",
        key="system_comments"
    )

    # SECTION 3: ADVANCED MODIFICATIONS
    st.markdown(f"""
    <div class="section-header">
        <div class="section-title">🔧 {t('advanced_modifications', 'ZAAWANSOWANE MODYFIKACJE')}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Interior Layout
        interior_layout = st.selectbox(
            "Układ Wewnętrzny",
            options=[
                "Przestrzeń otwarta (bez podziałów)",
                "Z przegrodami (1-3 pomieszczenia)",
                "Meble wbudowane (zabudowa na wymiar)",
                "Układ niestandardowy (projekt custom)",
                "Antresola/piętro (zwiększenie powierzchni)"
            ]
        )

        # Security Systems
        security_systems = st.selectbox(
            "Zabezpieczenia i Systemy Alarmowe",
            options=[
                "Bez dodatkowych zabezpieczeń (zamki standardowe)",
                "Podstawowe (wzmocnione zamki, kraty okienne)",
                "Standardowe (alarm, czujniki, syrena)",
                "Rozszerzone (monitoring, czujniki ruchu/wibracji)",
                "Wysokie (CCTV IP, kontrola dostępu, domofon)",
                "Maksymalne (sejf, biometria, central monitoring)",
                "Przemysłowe (ATEX, systemy gazowe, panic room)"
            ],
            index=1
        )

        # Exterior Cladding
        exterior_cladding = st.selectbox(
            "Okładzina Zewnętrzna",
            options=[
                "Bez okładziny (blacha kontenerowa standardowa)",
                "Blacha trapezoidalna (T18, T35, T55)",
                "Blacha kasetowa (płaska, przetłaczana)",
                "Siding winylowy (imitacja drewna, nowoczesny)",
                "Tynk strukturalny (silikonowy, akrylowy)",
                "Okładzina drewniana (termo, egzotyczna)",
                "Płyty kompozytowe (HPL, dibond)",
                "Cegła klinkierowa (lica, elewacyjna)",
                "Kamień naturalny/sztuczny"
            ]
        )

        # Additional Openings
        additional_openings = st.selectbox(
            "Dodatkowe Otwory i Modyfikacje",
            options=[
                "Bez dodatkowych otworów (standardowe drzwi)",
                "Drzwi dodatkowe pojedyncze (80-90cm)",
                "Drzwi dwuskrzydłowe (160-180cm)",
                "Drzwi przesuwne (do 300cm)",
                "Bramy segmentowe (240-360cm)",
                "Bramy rolowane (do 400cm)",
                "Okna dodatkowe (różne wymiary)",
                "Otwory techniczne (wentylacja, kable)",
                "Rampa załadunkowa (hydrauliczna, mechaniczna)"
            ]
        )

    with col2:
        # Fire Safety Systems
        fire_systems = st.selectbox(
            "Systemy Przeciwpożarowe",
            options=[
                "Bez systemów przeciwpożarowych",
                "Podstawowe (gaśnica 6kg, czujka dymu)",
                "Rozszerzone (gaśnice CO2, czujki temp.)",
                "Automatyczne (tryskacze, centrala pożarowa)",
                "Specjalistyczne (FM200, inergen, pianowe)",
                "Przemysłowe (deluge, monitor, oddymianie)",
                "Certyfikowane (zgodne z normami krajowymi)"
            ]
        )

        # Accessibility
        accessibility = st.selectbox(
            "Dostępność i Ergonomia",
            options=[
                "Dostęp standardowy (próg 15-20cm)",
                "Podjazd/rampa (dla wózków, niepełnosprawnych)",
                "Winda/podnośnik (osobowa, towarowa)",
                "Drzwi automatyczne (fotokomorka, przycisk)",
                "Oświetlenie awaryjne (LED, akumulatorowe)",
                "Systemy ostrzegawcze (dla niedosłyszących)",
                "Ergonomia pracy (wysokość blatów, oświetlenie)"
            ]
        )

        # Paint and Finish
        paint_finish = st.selectbox(
            "Malowanie i Wykończenie Zewnętrzne",
            options=[
                "Bez malowania (blacha surowa, cynkowana)",
                "Primer antykorozyjny (zabezpieczenie podstawowe)",
                "Powłoka standardowa C2 (RAL 7035 - szary jasny)",
                "Powłoka ulepszona C3 (kolory RAL, satynowa)",
                "Powłoka premium C4 (kolory specjalne, metalic)",
                "Powłoka antykorozyjna C5-M (środowiska agresywne)",
                "Wykończenie teksturowane (struktura, efekty)",
                "Graffiti protection (powłoki antywandalizm)"
            ],
            index=2
        )

    # Special Comments for Advanced Modifications
    st.markdown("### Uwagi Specjalne - Modyfikacje")
    advanced_comments = st.text_area(
        "Opisz dodatkowe wymagania dotyczące modyfikacji...",
        placeholder="np. Specjalne kolory RAL, nietypowe rozmiary otworów, dodatkowe wzmocnienia konstrukcyjne",
        key="advanced_comments"
    )

    # TRANSPORT AND LOGISTICS
    st.markdown(f"""
    <div class="section-header">
        <div class="section-title">🚛 TRANSPORT I LOGISTYKA</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        delivery_zone = st.selectbox(
            "Strefa Dostawy",
            options=[
                "Lokalny (do 50km od producenta)",
                "Regionalny (50-200km)",
                "Krajowy (200-800km)",
                "Międzynarodowy EU (Europa)",
                "Intercontinental (transport morski/lotniczy)",
                "Transport własny klienta (odbiór z fabryki)"
            ],
            index=1
        )

    with col2:
        transport_type = st.selectbox(
            "Rodzaj Transportu",
            options=[
                "Transport standardowy (naczep 13.6m)",
                "Transport niskopodwoziowy (gabaryty specjalne)",
                "Transport kontenerowy (40ft HC, morski)",
                "Transport kolejowy (wagon platform)",
                "Transport morski (kontenerowiec)",
                "Transport lotniczy (cargo, części)",
                "Transport multimodalny (kombinowany)"
            ]
        )

    with col3:
        installation = st.selectbox(
            "Montaż i Instalacja",
            options=[
                "Bez montażu (tylko transport i rozładunek)",
                "Dostawa + pozycjonowanie (dźwig/wózek)",
                "Montaż podstawowy (ustawienie, poziomowanie)",
                "Montaż standardowy (podłączenia, testy)",
                "Montaż kompleksowy (pod klucz, odbiory)",
                "Instalacja modułowa (łączenie kontenerów)",
                "Serwis pełny (konserwacja, części)"
            ],
            index=3
        )

    # EQUIPMENT AND EXTRAS
    st.markdown(f"""
    <div class="section-header">
        <div class="section-title">📋 WYPOSAŻENIE I DODATKI</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        office_equipment = st.selectbox(
            "Wyposażenie Biurowe/Wnętrzarskie",
            options=[
                "Bez wyposażenia (pusty kontener)",
                "Meble podstawowe (biurko, 2 krzesła)",
                "Meble standardowe (+ szafy, półki, stolik)",
                "Wyposażenie biurowe (+ komputer, drukarka)",
                "Wyposażenie komfortowe (+ lodówka, ekspres)",
                "Wyposażenie premium (designerskie, smart)",
                "Wyposażenie specjalistyczne (medical/lab)"
            ]
        )

    with col2:
        appliances = st.selectbox(
            "Sprzęt AGD (dla kontenerów mieszkalnych)",
            options=[
                "Bez sprzętu AGD",
                "Podstawowy (lodówka, kuchenka 2-palnikowa)",
                "Standardowy (+ pralka, mikrofala, czajnik)",
                "Komfortowy (+ zmywarka, piekarnik, wyciąg)",
                "Premium (sprzęt w zabudowie, indukcja)",
                "Smart AGD (WiFi, aplikacje, programowanie)"
            ]
        )

    with col3:
        it_systems = st.selectbox(
            "Systemy IT i Multimedia",
            options=[
                "Bez systemów IT",
                "Podstawowe (router WiFi, gniazda RJ45)",
                "Standardowe (+ monitoring, domofon)",
                "Zaawansowane (serwer, UPS, backup)",
                "Smart Building (KNX, IoT, automatyka)",
                "Multimedia (TV, audio, prezentacje)"
            ]
        )

    # Final Comments
    st.markdown("### Uwagi Specjalne - Ogólne")
    general_comments = st.text_area(
        "Opisz wszelkie dodatkowe wymagania, specyfikacje lub ograniczenia projektu...",
        placeholder="np. Specjalne terminy realizacji, wymogi certyfikacyjne, ograniczenia budżetowe, nietypowe zastosowania",
        key="general_comments",
        height=100
    )

    # Submit button
    submitted = st.form_submit_button("💾 Zapisz Konfigurację", use_container_width=True, type="primary")

    if submitted:
        # Calculate pricing
        config = {
            'container_type': container_type,
            'construction_material': construction_material,
            'insulation': insulation,
            'main_purpose': main_purpose,
            'environment': environment,
            'finish_level': finish_level,
            'flooring': flooring,
            'climate_zone': climate_zone,
            'num_windows': num_windows,
            'window_types': window_types,
            'lighting': lighting,
            'ventilation': ventilation,
            'roof_modifications': roof_modifications,
            'electrical_system': electrical_system,
            'plumbing_system': plumbing_system,
            'hvac_system': hvac_system,
            'interior_layout': interior_layout,
            'security_systems': security_systems,
            'exterior_cladding': exterior_cladding,
            'additional_openings': additional_openings,
            'fire_systems': fire_systems,
            'accessibility': accessibility,
            'paint_finish': paint_finish,
            'delivery_zone': delivery_zone,
            'transport_type': transport_type,
            'installation': installation,
            'office_equipment': office_equipment,
            'appliances': appliances,
            'it_systems': it_systems,
            'system_comments': system_comments,
            'advanced_comments': advanced_comments,
            'general_comments': general_comments
        }

        # Save configuration
        st.session_state.container_config = config

        # Calculate rough pricing (simplified)
        base_price = 15000  # Base container price

        # Calculate modifications cost
        modifications_cost = 0

        # Add costs based on selections
        if 'Premium' in insulation:
            modifications_cost += 3000
        elif 'Zaawansowana' in insulation:
            modifications_cost += 2000
        elif 'Podstawowa' in insulation:
            modifications_cost += 1000

        if 'Standardowy' in electrical_system or 'Rozszerzony' in electrical_system:
            modifications_cost += 2500
        elif 'Przemysłowy' in electrical_system:
            modifications_cost += 5000

        if 'Standard' in plumbing_system or 'Komfort' in plumbing_system:
            modifications_cost += 3000
        elif 'Premium' in plumbing_system:
            modifications_cost += 8000

        if 'split' in hvac_system.lower():
            modifications_cost += 3500
        elif 'VRV' in hvac_system or 'centrala' in hvac_system.lower():
            modifications_cost += 8000

        if len(window_types) > 0:
            modifications_cost += len(window_types) * 500

        # Finish level multiplier
        if 'Luksusowy' in finish_level:
            base_price *= 1.8
        elif 'Komfortowy' in finish_level:
            base_price *= 1.5
        elif 'Standardowy' in finish_level:
            base_price *= 1.2

        total_cost = base_price + modifications_cost

        # Display cost summary
        st.markdown(f"""
        <div class="cost-summary">
            <h2 style="margin-top: 0;">💰 Szacunkowa Wycena Projektu</h2>
            <div class="cost-breakdown">
                <h3>Podział Kosztów:</h3>
                <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                    <span>Kontener bazowy:</span>
                    <span><strong>€{base_price:,.2f}</strong></span>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                    <span>Modyfikacje i wyposażenie:</span>
                    <span><strong>€{modifications_cost:,.2f}</strong></span>
                </div>
                <hr style="border-color: rgba(255,255,255,0.3);">
                <div style="display: flex; justify-content: space-between; margin: 1rem 0; font-size: 1.2rem;">
                    <span><strong>CAŁKOWITY KOSZT:</strong></span>
                    <span><strong>€{total_cost:,.2f}</strong></span>
                </div>
            </div>
            <div class="special-notes">
                <strong>⚠️ Ważne:</strong> To wstępne szacowanie. Ostateczna cena zależy od szczegółowych specyfikacji, 
                aktualnych cen materiałów i dostępności. Dla dokładnej wyceny skontaktuj się z naszym zespołem.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.success("✅ Konfiguracja zapisana pomyślnie!")

# Navigation buttons (outside form, only show if configuration exists)
if 'container_config' in st.session_state and st.session_state.container_config:
    st.markdown("### Następne kroki")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤖 Przejdź do Wyceny AI", use_container_width=True, key="nav_ai"):
            st.switch_page("pages/2_AI_Cost_Estimator.py")
    with col2:
        if st.button("📧 Wyślij Zapytanie", use_container_width=True, key="nav_inquiry"):
            st.switch_page("pages/8_Send_Inquiry.py")

# Initialize configuration
if 'container_config' not in st.session_state:
    st.session_state.container_config = {}