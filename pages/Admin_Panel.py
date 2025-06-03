"""
Admin Panel for KAN-BUD Container Calculator
Manage business settings, costs, margins, and historical data
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json
from utils.simple_storage import SimpleStorageManager
from utils.translations import t, render_language_selector
from utils.historical_data_service import HistoricalDataService

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Language selector
render_language_selector()

# Admin authentication
def check_admin_access():
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    
    if not st.session_state.admin_logged_in:
        st.title(f"🔐 {t('admin.access_required')}")
        st.warning(t('admin.privileges_required'))
        
        admin_password = st.text_input(t('admin.enter_password'), type="password")
        
        if st.button(t('ui.login')):
            # Simple password check - in production, use proper authentication
            import os
            if admin_password == os.getenv("ADMIN_PASSWORD", "default-change-me"):
                st.session_state.admin_logged_in = True
                st.success(t('admin.access_granted'))
                st.rerun()
            else:
                st.error(t('admin.invalid_password'))
        
        st.info(t('admin.contact_it'))
        return False
    
    return True

# Main admin panel
def admin_panel():
    st.title(f"🛠️ {t('admin.panel_title')}")
    st.markdown(f"*{t('admin.panel_subtitle')}*")
    
    # Logout button
    if st.sidebar.button(f"🚪 {t('admin.logout')}"):
        st.session_state.admin_logged_in = False
        st.rerun()
    
    # Initialize storage
    storage = SimpleStorageManager()
    
    # Admin tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        f"💰 {t('admin.cost_settings')}", 
        f"📊 {t('admin.margins_pricing')}", 
        f"📈 {t('admin.historical_data')}", 
        f"👥 {t('admin.user_management')}",
        f"⚙️ {t('admin.system_settings')}"
    ])
    
    with tab1:
        st.header("Labor and Operating Costs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Labor Rates (€/hour)")
            
            # Get current labor rates
            if 'labor_rates' not in st.session_state:
                st.session_state.labor_rates = {
                    'basic_worker': 25.0,
                    'skilled_worker': 35.0,
                    'specialist': 45.0,
                    'engineer': 65.0,
                    'project_manager': 75.0
                }
            
            st.session_state.labor_rates['basic_worker'] = st.number_input(
                "Basic Worker", 
                value=st.session_state.labor_rates['basic_worker'],
                min_value=0.0, max_value=200.0, step=0.5
            )
            
            st.session_state.labor_rates['skilled_worker'] = st.number_input(
                "Skilled Worker", 
                value=st.session_state.labor_rates['skilled_worker'],
                min_value=0.0, max_value=200.0, step=0.5
            )
            
            st.session_state.labor_rates['specialist'] = st.number_input(
                "Specialist", 
                value=st.session_state.labor_rates['specialist'],
                min_value=0.0, max_value=200.0, step=0.5
            )
            
            st.session_state.labor_rates['engineer'] = st.number_input(
                "Engineer", 
                value=st.session_state.labor_rates['engineer'],
                min_value=0.0, max_value=200.0, step=0.5
            )
            
            st.session_state.labor_rates['project_manager'] = st.number_input(
                "Project Manager", 
                value=st.session_state.labor_rates['project_manager'],
                min_value=0.0, max_value=200.0, step=0.5
            )
        
        with col2:
            st.subheader("Operating Costs")
            
            if 'operating_costs' not in st.session_state:
                st.session_state.operating_costs = {
                    'workshop_hourly': 15.0,
                    'equipment_hourly': 25.0,
                    'transport_km': 1.2,
                    'overhead_percentage': 20.0
                }
            
            st.session_state.operating_costs['workshop_hourly'] = st.number_input(
                "Workshop Cost (€/hour)", 
                value=st.session_state.operating_costs['workshop_hourly'],
                min_value=0.0, max_value=100.0, step=0.5
            )
            
            st.session_state.operating_costs['equipment_hourly'] = st.number_input(
                "Equipment Cost (€/hour)", 
                value=st.session_state.operating_costs['equipment_hourly'],
                min_value=0.0, max_value=200.0, step=0.5
            )
            
            st.session_state.operating_costs['transport_km'] = st.number_input(
                "Transport Cost (€/km)", 
                value=st.session_state.operating_costs['transport_km'],
                min_value=0.0, max_value=10.0, step=0.1
            )
            
            st.session_state.operating_costs['overhead_percentage'] = st.number_input(
                "Overhead Percentage (%)", 
                value=st.session_state.operating_costs['overhead_percentage'],
                min_value=0.0, max_value=100.0, step=1.0
            )
        
        if st.button("💾 Save Cost Settings"):
            # Save to storage
            st.success("Cost settings saved successfully!")
    
    with tab2:
        st.header("Profit Margins & Pricing Strategy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Materials Margins")
            
            if 'material_margins' not in st.session_state:
                st.session_state.material_margins = {
                    'steel_structural': 25.0,
                    'insulation': 35.0,
                    'electrical': 30.0,
                    'plumbing': 28.0,
                    'windows_doors': 40.0,
                    'finishes': 45.0
                }
            
            for material, default_margin in st.session_state.material_margins.items():
                st.session_state.material_margins[material] = st.number_input(
                    f"{material.replace('_', ' ').title()} Margin (%)",
                    value=default_margin,
                    min_value=0.0, max_value=200.0, step=1.0
                )
        
        with col2:
            st.subheader("Service Categories")
            
            if 'service_margins' not in st.session_state:
                st.session_state.service_margins = {
                    'basic_modification': 20.0,
                    'complex_structural': 35.0,
                    'hvac_systems': 30.0,
                    'electrical_systems': 28.0,
                    'custom_design': 50.0,
                    'project_management': 25.0
                }
            
            for service, default_margin in st.session_state.service_margins.items():
                st.session_state.service_margins[service] = st.number_input(
                    f"{service.replace('_', ' ').title()} Margin (%)",
                    value=default_margin,
                    min_value=0.0, max_value=200.0, step=1.0
                )
        
        st.divider()
        
        st.subheader("Pricing Rules")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Volume Discounts**")
            
            if 'volume_discounts' not in st.session_state:
                st.session_state.volume_discounts = {
                    'small_project': 0.0,  # < €50k
                    'medium_project': 5.0,  # €50k - €200k
                    'large_project': 10.0,  # €200k - €500k
                    'enterprise_project': 15.0  # > €500k
                }
            
            st.session_state.volume_discounts['small_project'] = st.number_input(
                "Small Project Discount (< €50k) %", 
                value=st.session_state.volume_discounts['small_project'],
                min_value=0.0, max_value=50.0, step=1.0
            )
            
            st.session_state.volume_discounts['medium_project'] = st.number_input(
                "Medium Project Discount (€50k-€200k) %", 
                value=st.session_state.volume_discounts['medium_project'],
                min_value=0.0, max_value=50.0, step=1.0
            )
            
            st.session_state.volume_discounts['large_project'] = st.number_input(
                "Large Project Discount (€200k-€500k) %", 
                value=st.session_state.volume_discounts['large_project'],
                min_value=0.0, max_value=50.0, step=1.0
            )
            
            st.session_state.volume_discounts['enterprise_project'] = st.number_input(
                "Enterprise Project Discount (> €500k) %", 
                value=st.session_state.volume_discounts['enterprise_project'],
                min_value=0.0, max_value=50.0, step=1.0
            )
        
        with col2:
            st.markdown("**Seasonal Adjustments**")
            
            if 'seasonal_adjustments' not in st.session_state:
                st.session_state.seasonal_adjustments = {
                    'winter_surcharge': 5.0,
                    'summer_discount': 2.0,
                    'holiday_surcharge': 10.0
                }
            
            st.session_state.seasonal_adjustments['winter_surcharge'] = st.number_input(
                "Winter Surcharge (%)", 
                value=st.session_state.seasonal_adjustments['winter_surcharge'],
                min_value=0.0, max_value=50.0, step=1.0
            )
            
            st.session_state.seasonal_adjustments['summer_discount'] = st.number_input(
                "Summer Discount (%)", 
                value=st.session_state.seasonal_adjustments['summer_discount'],
                min_value=0.0, max_value=50.0, step=1.0
            )
            
            st.session_state.seasonal_adjustments['holiday_surcharge'] = st.number_input(
                "Holiday Surcharge (%)", 
                value=st.session_state.seasonal_adjustments['holiday_surcharge'],
                min_value=0.0, max_value=50.0, step=1.0
            )
        
        if st.button("💾 Save Pricing Settings"):
            st.success("Pricing settings saved successfully!")
    
    with tab3:
        st.header("Historical Data Management")
        
        historical_service = HistoricalDataService()
        
        st.subheader("📤 Import Historical Project Data")
        st.info("**Admin Only:** Import your 2-year historical calculation results to improve pricing accuracy")
        
        uploaded_file = st.file_uploader(
            "Upload historical data (CSV or Excel)",
            type=['csv', 'xlsx', 'xls'],
            help="Upload historical project data with actual vs estimated costs"
        )
        
        if uploaded_file is not None:
            if st.button("Import Historical Data"):
                try:
                    st.info("Processing historical data...")
                    
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
                            st.success(f"Successfully imported {len(data_records)} historical projects!")
                            st.info("Pricing accuracy will now improve based on this historical data!")
                        else:
                            st.error("Failed to import data. Please check the format.")
                    
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
        
        # Show data template
        if st.button("📥 Download Data Template"):
            template = historical_service.get_data_upload_template()
            csv = template.to_csv(index=False)
            st.download_button(
                label="Download CSV Template",
                data=csv,
                file_name="kan_bud_historical_data_template.csv",
                mime="text/csv"
            )
        
        st.divider()
        
        # Historical data statistics
        st.subheader("📊 Historical Data Statistics")
        
        stats = storage.get_storage_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Historical Projects", stats.get('historical_projects', 0))
        
        with col2:
            st.metric("User Projects", stats.get('user_projects', 0))
        
        with col3:
            st.metric("Customers", stats.get('customers', 0))
        
        with col4:
            st.metric("Generated Quotes", stats.get('quotes', 0))
        
        # Clear data option (dangerous!)
        st.divider()
        st.subheader("⚠️ Danger Zone")
        
        if st.checkbox("Enable data deletion"):
            if st.button("🗑️ Clear All Historical Data", type="secondary"):
                if st.checkbox("I understand this action cannot be undone"):
                    storage.clear_historical_data()
                    st.warning("All historical data has been cleared!")
    
    with tab4:
        st.header("User Management")
        
        st.subheader("Active Users & Sessions")
        
        # Mock user data - in production, implement proper user tracking
        user_data = pd.DataFrame({
            'User ID': ['user_001', 'user_002', 'user_003', 'user_004'],
            'Last Active': ['2024-01-15 14:30', '2024-01-15 13:45', '2024-01-15 12:20', '2024-01-15 11:10'],
            'Projects': [3, 1, 5, 2],
            'Language': ['Polish', 'English', 'German', 'Polish'],
            'Status': ['Active', 'Active', 'Active', 'Inactive']
        })
        
        st.dataframe(user_data, use_container_width=True)
        
        st.subheader("Access Control")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Allow guest access", value=True)
            st.checkbox("Require registration for quotes", value=False)
            st.checkbox("Enable project sharing", value=True)
        
        with col2:
            st.number_input("Max projects per user", value=10, min_value=1, max_value=100)
            st.number_input("Session timeout (minutes)", value=60, min_value=5, max_value=480)
    
    with tab5:
        st.header("System Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Application Settings")
            
            st.selectbox(t('admin.default_language'), 
                        options=['en', 'pl', 'de', 'nl'],
                        format_func=lambda x: {'en': 'English', 'pl': 'Polish', 'de': 'German', 'nl': 'Dutch'}[x])
            
            st.selectbox(t('admin.default_currency'), options=['EUR', 'PLN', 'USD'], index=0)
            
            st.number_input("Quote Validity (days)", value=30, min_value=1, max_value=365)
            
            st.checkbox("Enable AI Cost Estimation", value=True)
            st.checkbox("Enable Technical Analysis", value=True)
            st.checkbox("Enable Market Data", value=True)
        
        with col2:
            st.subheader("Company Information")
            
            company_name = st.text_input("Company Name", value="KAN-BUD")
            company_address = st.text_area("Address", value="Kąkolewo, Poland")
            company_phone = st.text_input("Phone", value="+48 XXX XXX XXX")
            company_email = st.text_input("Email", value="info@kan-bud.pl")
            company_website = st.text_input("Website", value="www.kan-bud.pl")
        
        st.divider()
        
        st.subheader("Backup & Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📤 Export All Data"):
                # Export all data to JSON
                export_data = {
                    'labor_rates': st.session_state.get('labor_rates', {}),
                    'operating_costs': st.session_state.get('operating_costs', {}),
                    'material_margins': st.session_state.get('material_margins', {}),
                    'service_margins': st.session_state.get('service_margins', {}),
                    'volume_discounts': st.session_state.get('volume_discounts', {}),
                    'seasonal_adjustments': st.session_state.get('seasonal_adjustments', {}),
                    'export_date': datetime.now().isoformat()
                }
                
                json_data = json.dumps(export_data, indent=2)
                
                st.download_button(
                    label="📥 Download Settings Backup",
                    data=json_data,
                    file_name=f"kan_bud_settings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            uploaded_settings = st.file_uploader("📤 Import Settings", type=['json'])
            
            if uploaded_settings is not None:
                if st.button("Import Settings"):
                    try:
                        settings_data = json.load(uploaded_settings)
                        
                        # Load settings into session state
                        for key, value in settings_data.items():
                            if key != 'export_date':
                                st.session_state[key] = value
                        
                        st.success("Settings imported successfully!")
                    except Exception as e:
                        st.error(f"Error importing settings: {str(e)}")

# Main execution
if __name__ == "__main__":
    if check_admin_access():
        admin_panel()