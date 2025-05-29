"""
Drawing Analysis Page for KAN-BUD Container Calculator
Analyzes customer drawings (PDF/DWG) to extract pricing elements
"""

import streamlit as st
import pandas as pd
from utils.document_analyzer import DocumentAnalyzer
from utils.translations import t, get_available_languages
from utils.simple_storage import SimpleStorageManager
import json

st.set_page_config(page_title="Drawing Analysis", page_icon="📐", layout="wide")

# Employee access control
if 'employee_logged_in' not in st.session_state:
    st.session_state.employee_logged_in = False

# Get current language
lang = st.session_state.get('language', 'en')

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Language selector
from utils.translations import t, render_language_selector
render_language_selector()

if not st.session_state.employee_logged_in:
    st.title("🔒 " + t('ui.access_denied'))
    st.error(t('drawing_analysis.employee_only'))
    st.info(t('drawing_analysis.login_info'))
    st.markdown(f"**{t('drawing_analysis.employee_password')}:** kan-bud-employee-2024")
    st.stop()

st.title(f"📐 {t('nav.drawing_analysis')}")
st.markdown(f"*{t('drawing_analysis.description')}*")

# Initialize services
document_analyzer = DocumentAnalyzer()
storage = SimpleStorageManager()

# Project context form
st.subheader(f"🏗️ {t('drawing_analysis.project_context')}")

col1, col2 = st.columns(2)

with col1:
    container_type = st.selectbox(
        t('form.labels.container_type'),
        [t('container.types.20ft_standard'), t('container.types.40ft_standard'), 
         t('container.types.40ft_high_cube'), "45ft Standard", "Custom"]
    )
    
    use_case = st.selectbox(
        t('form.labels.main_purpose'),
        [t('container.use_cases.office_space'), t('container.use_cases.residential'), 
         t('container.use_cases.workshop'), t('container.use_cases.storage'), 
         t('container.use_cases.retail'), t('container.use_cases.restaurant'), t('drawing_analysis.other')]
    )

with col2:
    location = st.text_input(t('drawing_analysis.project_location'), value="Polska")
    
    project_name = st.text_input(t('drawing_analysis.project_name'), placeholder=t('drawing_analysis.project_name_placeholder'))

# File upload section
st.subheader(f"📤 {t('drawing_analysis.file_upload')}")

uploaded_files = st.file_uploader(
    t('drawing_analysis.upload_drawings'),
    type=['pdf', 'dwg', 'jpg', 'png'],
    accept_multiple_files=True,
    help=t('drawing_analysis.file_formats_help')
)

if uploaded_files:
    st.info(f"Przesłano {len(uploaded_files)} plik(ów)")
    
    # Show uploaded files
    for file in uploaded_files:
        st.write(f"📄 {file.name} ({file.size} bytes)")

# Analysis section
if uploaded_files and st.button("🔍 Analizuj Rysunki", type="primary"):
    
    project_context = {
        'container_type': container_type,
        'use_case': use_case,
        'location': location,
        'project_name': project_name
    }
    
    with st.spinner("Analizuję rysunki za pomocą AI..."):
        
        analysis_results = []
        
        for uploaded_file in uploaded_files:
            st.subheader(f"📋 Analiza: {uploaded_file.name}")
            
            try:
                if uploaded_file.name.lower().endswith('.pdf'):
                    # PDF analysis with AI
                    result = document_analyzer.analyze_pdf_drawing(uploaded_file, project_context)
                    analysis_results.append(result)
                    
                    # Display results
                    if result.get('status') != 'failed':
                        st.success(f"✅ Analiza zakończona pomyślnie (Model: {result.get('ai_model_used', 'AI')})")
                        
                        # Structural elements
                        st.subheader("🏗️ Elementy Strukturalne")
                        
                        structural = result.get('structural_elements', {})
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            windows = structural.get('windows', {})
                            st.metric("Okna", windows.get('count', 0))
                            if windows.get('types'):
                                st.write("Typy:", ", ".join(windows.get('types', [])))
                        
                        with col2:
                            doors = structural.get('doors', {})
                            st.metric("Drzwi", doors.get('count', 0))
                            if doors.get('types'):
                                st.write("Typy:", ", ".join(doors.get('types', [])))
                        
                        with col3:
                            openings = structural.get('openings', {})
                            st.metric("Inne otwory", openings.get('count', 0))
                        
                        # Installations
                        st.subheader("⚡ Instalacje")
                        
                        installations = result.get('installations', {})
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            electrical = installations.get('electrical', {})
                            complexity = electrical.get('complexity', 'basic')
                            color = {"basic": "blue", "standard": "orange", "advanced": "red"}.get(complexity, "blue")
                            st.markdown(f"**Elektryczna:** :{color}[{complexity.title()}]")
                            if electrical.get('elements'):
                                for element in electrical.get('elements', []):
                                    st.write(f"• {element}")
                        
                        with col2:
                            plumbing = installations.get('plumbing', {})
                            complexity = plumbing.get('complexity', 'basic')
                            color = {"basic": "blue", "standard": "orange", "advanced": "red"}.get(complexity, "blue")
                            st.markdown(f"**Hydrauliczna:** :{color}[{complexity.title()}]")
                            if plumbing.get('elements'):
                                for element in plumbing.get('elements', []):
                                    st.write(f"• {element}")
                        
                        with col3:
                            hvac = installations.get('hvac', {})
                            complexity = hvac.get('complexity', 'basic')
                            color = {"basic": "blue", "standard": "orange", "advanced": "red"}.get(complexity, "blue")
                            st.markdown(f"**HVAC:** :{color}[{complexity.title()}]")
                            if hvac.get('elements'):
                                for element in hvac.get('elements', []):
                                    st.write(f"• {element}")
                        
                        # Cost impact
                        st.subheader("💰 Wpływ na Koszty")
                        
                        cost_summary = result.get('cost_impact_summary', {})
                        
                        complexity = cost_summary.get('estimated_complexity', 'medium')
                        complexity_color = {"low": "green", "medium": "orange", "high": "red"}.get(complexity, "orange")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Złożoność projektu:** :{complexity_color}[{complexity.title()}]")
                            
                            additional_cost = cost_summary.get('estimated_additional_cost_percentage', 0)
                            if additional_cost > 0:
                                st.metric("Szacunkowa korekta kosztów", f"+{additional_cost}%")
                        
                        with col2:
                            cost_drivers = cost_summary.get('major_cost_drivers', [])
                            if cost_drivers:
                                st.write("**Główne czynniki kosztowe:**")
                                for driver in cost_drivers:
                                    st.write(f"• {driver}")
                        
                        # Recommendations
                        recommendations = result.get('recommendations', [])
                        if recommendations:
                            st.subheader("💡 Zalecenia")
                            for rec in recommendations:
                                st.info(f"• {rec}")
                        
                        # Calculate cost adjustments if base estimate is available
                        if 'base_estimate' in st.session_state:
                            base_estimate = st.session_state.base_estimate
                            cost_adjustments = document_analyzer.calculate_cost_adjustments(result, base_estimate)
                            
                            st.subheader("📊 Szczegółowa Analiza Kosztów")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.metric("Wstępna wycena", f"€{base_estimate:,.2f}")
                                st.metric("Korekta na podstawie rysunku", f"€{cost_adjustments.get('total_adjustment', 0):,.2f}")
                            
                            with col2:
                                st.metric("Skorygowana wycena", f"€{cost_adjustments.get('adjusted_estimate', 0):,.2f}")
                                st.metric("Procentowa korekta", f"+{cost_adjustments.get('adjustment_percentage', 0):.1f}%")
                            
                            # Detailed breakdown
                            adjustments = cost_adjustments.get('cost_adjustments', {})
                            if adjustments:
                                st.write("**Szczegółowy podział korekt:**")
                                for category, amount in adjustments.items():
                                    if amount > 0:
                                        category_name = {
                                            'structural_additions': 'Elementy strukturalne',
                                            'installation_complexity': 'Złożoność instalacji',
                                            'material_upgrades': 'Ulepszenia materiałowe',
                                            'special_requirements': 'Wymagania specjalne'
                                        }.get(category, category)
                                        st.write(f"• {category_name}: €{amount:,.2f}")
                        
                    else:
                        st.error("❌ Nie udało się przeanalizować pliku")
                        st.write("Zalecenia:")
                        for rec in result.get('recommendations', []):
                            st.write(f"• {rec}")
                
                elif uploaded_file.name.lower().endswith('.dwg'):
                    # DWG analysis (limited)
                    result = document_analyzer.analyze_dwg_metadata(uploaded_file)
                    
                    st.info("📝 Analiza pliku DWG (ograniczona)")
                    st.write("**Informacje o pliku:**")
                    file_info = result.get('file_info', {})
                    st.write(f"• Nazwa: {file_info.get('filename', 'N/A')}")
                    st.write(f"• Rozmiar: {file_info.get('size_bytes', 0)/1024:.1f} KB")
                    
                    st.warning("💡 **Wskazówka:** Prześlij rysunek w formacie PDF dla pełnej analizy AI")
                    
                    recommendations = result.get('recommendations', [])
                    for rec in recommendations:
                        st.write(f"• {rec}")
                
                else:
                    # Image analysis
                    st.info("🖼️ Analizuję obraz...")
                    # For JPG/PNG, we can still use AI vision
                    result = document_analyzer.analyze_pdf_drawing(uploaded_file, project_context)
                    
                    if result.get('status') != 'failed':
                        st.success("✅ Analiza obrazu zakończona")
                        # Display similar results as PDF
                    else:
                        st.error("❌ Nie udało się przeanalizować obrazu")
                
            except Exception as e:
                st.error(f"❌ Błąd podczas analizy pliku {uploaded_file.name}: {str(e)}")
                st.write("Spróbuj ponownie lub skontaktuj się z działem technicznym.")
        
        # Save analysis results
        if analysis_results and project_name:
            try:
                analysis_data = {
                    'project_name': project_name,
                    'project_context': project_context,
                    'analysis_results': analysis_results,
                    'analysis_date': pd.Timestamp.now().isoformat(),
                    'files_analyzed': [f.name for f in uploaded_files]
                }
                
                # Save to storage
                storage.save_user_project(
                    user_id=st.session_state.get('user_id', 'guest'),
                    project_name=f"Drawing Analysis: {project_name}",
                    config=analysis_data
                )
                
                st.success("✅ Analiza została zapisana w projekcie")
                
            except Exception as e:
                st.warning(f"Nie udało się zapisać analizy: {str(e)}")

# Tips section
st.divider()

st.subheader("💡 Wskazówki dla najlepszych wyników")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Format plików:**
    • PDF - najlepsze wyniki analizy AI
    • DWG - analiza metadanych
    • JPG/PNG - analiza obrazów
    
    **Jakość rysunków:**
    • Wysoką rozdzielczość (min. 300 DPI)
    • Czytelne wymiary i opisy
    • Wszystkie warstwy widoczne
    """)

with col2:
    st.markdown("""
    **Zawartość rysunków:**
    • Plany architektoniczne
    • Przekroje techniczne
    • Specyfikacje materiałów
    • Detale konstrukcyjne
    
    **Dodatkowe informacje:**
    • Tabele z wymiarami
    • Legendy symboli
    • Notatki projektowe
    """)

# Recent analyses
st.divider()

st.subheader("📁 Ostatnie Analizy")

try:
    user_projects = storage.get_user_projects(st.session_state.get('user_id', 'guest'))
    drawing_projects = [p for p in user_projects if 'Drawing Analysis' in p.get('project_name', '')]
    
    if drawing_projects:
        for project in drawing_projects[:5]:  # Show last 5
            with st.expander(f"📐 {project.get('project_name', 'Unnamed')} - {project.get('created_at', 'Unknown date')}"):
                config = project.get('container_config', {})
                context = config.get('project_context', {})
                
                st.write(f"**Typ kontenera:** {context.get('container_type', 'N/A')}")
                st.write(f"**Przeznaczenie:** {context.get('use_case', 'N/A')}")
                st.write(f"**Lokalizacja:** {context.get('location', 'N/A')}")
                
                files_analyzed = config.get('files_analyzed', [])
                if files_analyzed:
                    st.write(f"**Przeanalizowane pliki:** {', '.join(files_analyzed)}")
    else:
        st.info("Brak zapisanych analiz rysunków")

except Exception as e:
    st.warning("Nie udało się załadować historii analiz")

# Contact information
st.divider()

st.info("""
**Potrzebujesz pomocy z analizą rysunków?**

Skontaktuj się z naszym działem technicznym:
📞 +48 XXX XXX XXX  
✉️ tech@kan-bud.pl

Oferujemy również ręczną weryfikację złożonych projektów.
""")