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
            t('container_types.10ft_compact'),
            t('container_types.20ft_standard'),
            t('container_types.20ft_high_cube'),
            t('container_types.40ft_standard'),
            t('container_types.40ft_high_cube'),
            t('container_types.multi_unit'),
            t('container_types.custom_size'),
            t('container_types.refurbished')
        ]
        container_type = st.selectbox(
            t('container_type'),
            options=container_type_options,
            index=3
        )

        # Construction Material
        construction_material_options = [
            t('construction_material_steel'),
            t('construction_material_aluminum'),
            t('construction_material_composite')
        ]
        construction_material = st.selectbox(
            t('construction_material'),
            options=construction_material_options
        )

        # Insulation
        insulation_options = [
            t('insulation.basic'),
            t('insulation.standard'),
            t('insulation.premium'),
            t('insulation.extreme')
        ]
        insulation = st.selectbox(
            t('insulation_label'),
            options=insulation_options,
            index=1
        )

        # Main Purpose
        main_purpose_options = [
            t('purposes.office_space'),
            t('purposes.sanitary_containers'), 
            t('purposes.residential_containers'),
            t('purposes.commercial_containers'),
            t('purposes.storage_containers'),
            t('purposes.technical_containers'),
            t('purposes.changing_rooms'),
            t('purposes.guard_booths')
        ]
        main_purpose = st.selectbox(
            t('main_purpose'),
            options=main_purpose_options
        )

    with col2:
        # Usage Environment
        environment_options = [
            t('environments.indoor'),
            t('environments.outdoor_standard'),
            t('environments.outdoor_extreme'),
            t('environments.industrial'),
            t('environments.construction'),
            t('environments.agricultural'),
            t('environments.marine')
        ]
        environment = st.selectbox(
            t('environment'),
            options=environment_options,
            index=1
        )

        # Finish Level
        finish_level_options = [
            t('finish_levels.basic'),
            t('finish_levels.shell'),
            t('finish_levels.standard'),
            t('finish_levels.comfort'),
            t('finish_levels.luxury'),
            t('finish_levels.specialist')
        ]
        finish_level = st.selectbox(
            t('finish_level'),
            options=finish_level_options,
            index=2
        )

        # Flooring
        flooring_options = [
            t('flooring.none'),
            t('flooring.plywood'),
            t('flooring.anti_slip'),
            t('flooring.laminate'),
            t('flooring.vinyl'),
            t('flooring.carpet'),
            t('flooring.epoxy'),
            t('flooring.concrete')
        ]
        flooring = st.selectbox(
            t('flooring'),
            options=flooring_options,
            index=1
        )

        # Climate Zone
        climate_zone_options = [
            t('climate_zones.northern_europe'),
            t('climate_zones.central_europe'),
            t('climate_zones.southern_europe'),
            t('climate_zones.continental'),
            t('climate_zones.maritime'),
            t('climate_zones.mountain'),
            t('climate_zones.tropical')
        ]
        climate_zone = st.selectbox(
            t('climate_zone'),
            options=climate_zone_options,
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
        num_windows_options = [
            t('windows.none'),
            t('windows.one'),
            t('windows.two'), 
            t('windows.three'),
            t('windows.four'),
            t('windows.five_plus')
        ]
        num_windows = st.selectbox(
            t('number_of_windows'),
            options=num_windows_options
        )

        window_types_options = [
            t('window_types.standard'),
            t('window_types.panoramic'),
            t('window_types.sliding'),
            t('window_types.tilt'),
            t('window_types.security'),
            t('window_types.energy_efficient'),
            t('window_types.skylight')
        ]
        window_types = st.multiselect(
            t('window_types'),
            options=window_types_options
        )

        # Lighting
        lighting_options = [
            t('lighting.none'),
            t('lighting.basic_led'),
            t('lighting.energy_efficient'),
            t('lighting.exterior'),
            t('lighting.emergency'),
            t('lighting.smart')
        ]
        lighting = st.selectbox(
            t('lighting'),
            options=lighting_options,
            index=1
        )

    with col2:
        # Ventilation
        ventilation_options = [
            t('ventilation.none'),
            t('ventilation.gravity'),
            t('ventilation.wall_fans'),
            t('ventilation.mechanical'),
            t('ventilation.heat_recovery'),
            t('ventilation.split_ac'),
            t('ventilation.central_ac'),
            t('ventilation.industrial')
        ]
        ventilation = st.selectbox(
            t('air_intakes_label'),
            options=ventilation_options,
            index=1
        )

        # Roof Modifications
        roof_modifications_options = [
            t('roof_modifications.none'),
            t('roof_modifications.insulation'),
            t('roof_modifications.skylight'),
            t('roof_modifications.fans'),
            t('roof_modifications.solar'),
            t('roof_modifications.antennas'),
            t('roof_modifications.sloped'),
            t('roof_modifications.terrace'),
            t('roof_modifications.snow_removal')
        ]
        roof_modifications = st.selectbox(
            t('roof_modifications_label'),
            options=roof_modifications_options
        )

        # Electrical System
        electrical_system_options = [
            t('electrical_system.none'),
            t('electrical_system.preparation'),
            t('electrical_system.basic'),
            t('electrical_system.standard'),
            t('electrical_system.extended'),
            t('electrical_system.industrial'),
            t('electrical_system.it_server'),
            t('electrical_system.smart')
        ]
        electrical_system = st.selectbox(
            t('electrical_system'),
            options=electrical_system_options,
            index=3
        )

    with col3:
        # Plumbing System
        plumbing_system_options = [
            t('plumbing_system.none'),
            t('plumbing_system.preparation'),
            t('plumbing_system.cold_water'),
            t('plumbing_system.hot_cold_water'),
            t('plumbing_system.basic_sanitary'),
            t('plumbing_system.standard_sanitary'),
            t('plumbing_system.comfort_sanitary'),
            t('plumbing_system.premium_sanitary'),
            t('plumbing_system.industrial')
        ]
        plumbing_system = st.selectbox(
            t('plumbing_system'),
            options=plumbing_system_options
        )

        # HVAC System
        hvac_system_options = [
            t('hvac_system.none'),
            t('hvac_system.electric_heaters'),
            t('hvac_system.electric_heating'),
            t('hvac_system.heat_pump'),
            t('hvac_system.gas_heating'),
            t('hvac_system.split_ac'),
            t('hvac_system.vrv_vrf'),
            t('hvac_system.underfloor_heating'),
            t('hvac_system.central_ac')
        ]
        hvac_system = st.selectbox(
            t('hvac_system'),
            options=hvac_system_options,
            index=5
        )

    # Special Comments for Systems
    st.markdown(f"### {t('special_comments_systems')}")
    system_comments = st.text_area(
        t('system_requirements_description'),
        placeholder=t('system_requirements_placeholder'),
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
        interior_layout_options = [
            t('interior_layout.open_space'),
            t('interior_layout.partitioned'),
            t('interior_layout.built_in_furniture'),
            t('interior_layout.custom_design'),
            t('interior_layout.mezzanine')
        ]
        interior_layout = st.selectbox(
            t('interior_layout'),
            options=interior_layout_options
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