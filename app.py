import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.container_database import ContainerDatabase
from utils.calculations import StructuralCalculations
from utils.database import DatabaseManager
from utils.simple_storage import SimpleStorageManager
from utils.historical_data_service import HistoricalDataService
from utils.translations import get_text, get_available_languages
from utils.ai_services import OpenAIService, AnthropicService

# Page configuration
st.set_page_config(
    page_title="KAN-BUD Professional Container Solutions",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
@st.cache_resource
def initialize_services():
    """Initialize all services with caching"""
    # Try PostgreSQL first, fallback to simple storage
    try:
        db = DatabaseManager()
        if not db.engine:
            storage = SimpleStorageManager()
        else:
            storage = db
    except:
        storage = SimpleStorageManager()
    
    container_db = ContainerDatabase()
    calc = StructuralCalculations()
    historical_service = HistoricalDataService()
    
    # Initialize AI services
    try:
        openai_service = OpenAIService()
        anthropic_service = AnthropicService()
    except:
        openai_service = None
        anthropic_service = None
    
    return storage, container_db, calc, historical_service, openai_service, anthropic_service

# Language selection in sidebar
available_languages = get_available_languages()
if 'language' not in st.session_state:
    st.session_state.language = 'en'

with st.sidebar:
    st.markdown("### 🌐 " + get_text('language_selector', st.session_state.get('language', 'en')))
    selected_language = st.selectbox(
        get_text('choose_language', st.session_state.get('language', 'en')),
        options=list(available_languages.keys()),
        format_func=lambda x: available_languages[x],
        index=list(available_languages.keys()).index(st.session_state.language)
    )
    
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()



# Initialize session state
if 'container_db' not in st.session_state:
    st.session_state.container_db = ContainerDatabase()

if 'calculations' not in st.session_state:
    st.session_state.calculations = StructuralCalculations()

if 'historical_service' not in st.session_state:
    st.session_state.historical_service = HistoricalDataService()

# Get current language
lang = st.session_state.get('language', 'en')

# Get current language
lang = st.session_state.get('language', 'en')

# Initialize services
storage, container_db, calc, historical_service_init, openai_service, anthropic_service = initialize_services()

# Create a simple historical service that works with our storage
class SimpleHistoricalService:
    def __init__(self, storage_manager):
        self.storage = storage_manager
    
    def get_data_upload_template(self):
        template_data = {
            'project_date': ['2023-01-15', '2023-02-20', '2023-03-10'],
            'container_type': ['40ft Standard', '20ft Standard', '40ft High Cube'],
            'use_case': ['Office Space', 'Workshop', 'Residential'],
            'location': ['Kąkolewo', 'Poznań', 'Warszawa'],
            'actual_cost': [45000, 25000, 55000],
            'estimated_cost': [42000, 27000, 52000],
            'materials_cost': [28000, 16000, 33000],
            'labor_cost': [12000, 7000, 15000],
            'delivery_cost': [3000, 1500, 4000],
            'modifications': ['{"windows": 4, "electrical": true}', 
                           '{"doors": 2, "hvac": true}',
                           '{"windows": 6, "electrical": true, "plumbing": true}'],
            'project_duration_days': [45, 30, 60],
            'customer_satisfaction': [5, 4, 5]
        }
        return pd.DataFrame(template_data)
    
    def import_historical_projects(self, file_path=None, data=None):
        if data:
            return self.storage.import_historical_data(data)
        return False

# Use the initialized historical service or create a simple one
if historical_service_init:
    historical_service = historical_service_init
else:
    historical_service = SimpleHistoricalService(storage)

# Main dashboard
st.title(f"🏗️ {get_text('app_title', lang)}")
st.markdown(f"*{get_text('app_subtitle', lang)}*")

# Company information in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🏢 KAN-BUD")
    company_info = get_text('company_info', lang)
    if isinstance(company_info, dict):
        st.markdown(f"📍 {company_info.get('address', 'Kąkolewo, Poland')}")
        st.markdown(f"📞 {company_info.get('phone', '+48 XXX XXX XXX')}")
        st.markdown(f"✉️ {company_info.get('email', 'info@kan-bud.pl')}")
        st.markdown(f"🌐 {company_info.get('website', 'www.kan-bud.pl')}")

# Historical Data Upload Section
if historical_service and storage:
    with st.expander(f"📊 {get_text('historical_data_import', lang)}"):
        st.markdown(get_text('improve_pricing_accuracy', lang))
        st.markdown(f"\n{get_text('upload_historical_data', lang)}")
        st.markdown(get_text('get_accurate_estimates', lang))
        st.markdown(get_text('analyze_pricing_trends', lang))
        st.markdown(get_text('identify_profitable_projects', lang))
        st.markdown(get_text('build_customer_confidence', lang))
        
        uploaded_file = st.file_uploader(
            get_text('upload_historical_file', lang),
            type=['csv', 'xlsx', 'xls'],
            help=get_text('upload_help_text', lang)
        )
        
        if uploaded_file is not None:
            if st.button(get_text('import_historical_data', lang)):
                try:
                    st.info(get_text('processing_data', lang))
                    
                    # Process the uploaded file
                    df = None
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(uploaded_file)
                    
                    if df is not None:
                        # Convert DataFrame to records and import
                        data_records = df.to_dict('records')
                        if historical_service.import_historical_projects(data=data_records):
                            st.success(get_text('successfully_imported', lang).format(count=len(data_records)))
                            st.info(get_text('pricing_accuracy_improved', lang))
                        else:
                            st.error(get_text('import_failed', lang))
                    
                except Exception as e:
                    st.error(get_text('error_processing_file', lang).format(error=str(e)))
        
        # Show data template
        if st.button(get_text('download_data_template', lang)):
            template = historical_service.get_data_upload_template()
            csv = template.to_csv(index=False)
            st.download_button(
                label=get_text('download_csv_template', lang),
                data=csv,
                file_name="kan_bud_historical_data_template.csv",
                mime="text/csv"
            )

# Sidebar navigation info
with st.sidebar:
    st.header(get_text('navigation', lang))
    st.markdown(f"""
    **{get_text('pages_available', lang)}**
    1. 📦 {get_text('container_configurator', lang)}
    2. 🤖 {get_text('ai_cost_estimator', lang)}
    3. 🔧 {get_text('technical_analysis', lang)}
    4. 📋 {get_text('quote_generator', lang)}
    5. ⚖️ {get_text('comparison_tool', lang)}
    """)
    
    st.divider()
    st.subheader(get_text('quick_stats', lang))
    
    # Display some quick statistics
    container_types = st.session_state.container_db.get_container_types()
    st.metric(get_text('available_container_types', lang), len(container_types))
    st.metric(get_text('standard_sizes', lang), "6 (20ft, 40ft, 45ft, 48ft, 53ft, Custom)")
    st.metric(get_text('modification_categories', lang), "8")

# Main dashboard content
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader(f"📊 {get_text('quick_overview', lang)}")
    st.markdown(f"""
    **{get_text('container_modification_services', lang)}**
    - {get_text('structural_reinforcements', lang)}
    - {get_text('custom_openings_windows', lang)}
    - {get_text('insulation_hvac', lang)}
    - {get_text('electrical_installations', lang)}
    - {get_text('plumbing_utilities', lang)}
    - {get_text('interior_fitouts', lang)}
    """)

with col2:
    st.subheader(f"🎯 {get_text('key_features', lang)}")
    st.markdown(f"""
    **{get_text('ai_powered_analysis', lang)}**
    - {get_text('intelligent_cost_estimation', lang)}
    - {get_text('technical_feasibility_check', lang)}
    - {get_text('material_optimization', lang)}
    - {get_text('compliance_verification', lang)}
    - {get_text('risk_assessment', lang)}
    - {get_text('timeline_prediction', lang)}
    """)

with col3:
    st.subheader(f"💼 {get_text('sales_tools', lang)}")
    st.markdown(f"""
    **{get_text('professional_outputs', lang)}**
    - {get_text('detailed_quotes', lang)}
    - {get_text('technical_specifications', lang)}
    - {get_text('visualizations_3d', lang)}
    - {get_text('cost_comparisons', lang)}
    - {get_text('project_timelines', lang)}
    - {get_text('compliance_reports', lang)}
    """)

st.divider()

# Recent activity and quick actions
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"📈 {get_text('market_insights', lang)}")
    
    # Sample market data visualization
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='ME')
    steel_prices = [2800, 2850, 2920, 3100, 3050, 2980, 3150, 3200, 3180, 3250, 3300, 3280]  # €/tonne
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, 
        y=steel_prices,
        mode='lines+markers',
        name='Steel Price (€/tonne)',
        line=dict(color='#1f77b4', width=3)
    ))
    
    fig.update_layout(
        title=get_text('steel_price_trends', lang),
        xaxis_title=get_text('month', lang),
        yaxis_title=f"{get_text('price', lang)} (€/tonne)",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader(f"🚀 {get_text('quick_actions', lang)}")
    
    if st.button(f"🆕 {get_text('new_container_project', lang)}", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")
    
    if st.button(f"💰 {get_text('get_ai_cost_estimate', lang)}", use_container_width=True):
        st.switch_page("pages/2_AI_Cost_Estimator.py")
    
    if st.button(f"🔍 {get_text('view_technical_analysis', lang)}", use_container_width=True):
        st.switch_page("pages/3_Technical_Analysis.py")
    
    if st.button(f"📄 {get_text('generate_quote', lang)}", use_container_width=True):
        st.switch_page("pages/4_Quote_Generator.py")
    
    st.divider()
    
    st.subheader(f"💡 {get_text('tips', lang)}")
    st.info(f"""
    **{get_text('best_practices', lang)}**
    - Start with Container Configurator
    - Use AI Cost Estimator for accuracy
    - Run Technical Analysis for compliance
    - Generate professional quotes
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
<p>Steel Container Sales Calculator v1.0 | Built with Streamlit & AI</p>
<p>For technical support, contact your system administrator</p>
</div>
""", unsafe_allow_html=True)
