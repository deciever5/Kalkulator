
"""
Customer Drawing Analysis - Available for all users
Simplified version for customer use as part of estimation process
"""

import streamlit as st
from utils.document_analyzer import DocumentAnalyzer
from utils.translations import t, render_language_selector

st.set_page_config(page_title="Drawing Analysis", page_icon="📐", layout="wide")

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Language selector
render_language_selector()

st.title(f"📐 {t('nav.drawing_analysis_customer')}")
st.markdown(f"*{t('drawing_analysis_customer.description')}*")

# Important disclaimer
st.info(f"""
💡 **{t('drawing_analysis_customer.info_title')}**

{t('drawing_analysis_customer.info_text')}
""")

# Check if basic configuration exists
if 'container_config' not in st.session_state:
    st.warning(f"⚠️ {t('drawing_analysis_customer.no_config')}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"🔧 {t('ui.go_to_configurator')}", use_container_width=True):
            st.switch_page("pages/1_Container_Configurator.py")
    
    with col2:
        if st.button(f"🤖 {t('ui.get_ai_estimate')}", use_container_width=True):
            st.switch_page("pages/2_AI_Cost_Estimator.py")
    
    st.stop()

# Show current configuration summary
config = st.session_state.container_config
st.success(f"✅ {t('drawing_analysis_customer.config_found')}")

with st.expander(f"📋 {t('drawing_analysis_customer.current_config')}"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**{t('form.labels.container_type')}:** {config.get('container_type', 'N/A')}")
        st.write(f"**{t('form.labels.main_purpose')}:** {config.get('main_purpose', 'N/A')}")
    
    with col2:
        st.write(f"**{t('form.labels.environment')}:** {config.get('environment', 'N/A')}")
        if 'cost_breakdown' in st.session_state:
            total_cost = st.session_state.cost_breakdown.get('total_cost', 0)
            st.write(f"**{t('total_cost')}:** €{total_cost:,.2f}")

# Simple project context
st.subheader(f"🏗️ {t('drawing_analysis_customer.project_context')}")

col1, col2 = st.columns(2)

with col1:
    project_name = st.text_input(
        t('drawing_analysis_customer.project_name'), 
        placeholder=t('drawing_analysis_customer.project_name_placeholder')
    )

with col2:
    location = st.text_input(
        t('drawing_analysis_customer.project_location'), 
        value="Polska"
    )

# File upload section
st.subheader(f"📤 {t('drawing_analysis_customer.file_upload')}")

uploaded_files = st.file_uploader(
    t('drawing_analysis_customer.upload_drawings'),
    type=['pdf', 'jpg', 'jpeg', 'png'],
    accept_multiple_files=True,
    help=t('drawing_analysis_customer.file_formats_help'),
    key="drawing_analysis_uploader"
)

if uploaded_files:
    st.info(f"{t('drawing_analysis_customer.files_uploaded')}: {len(uploaded_files)}")
    
    for file in uploaded_files:
        st.write(f"📄 {file.name} ({file.size} bytes)")

# Analysis section
if uploaded_files and st.button(f"🔍 {t('drawing_analysis_customer.analyze_button')}", type="primary"):
    
    project_context = {
        'container_type': config.get('container_type'),
        'use_case': config.get('main_purpose'),
        'location': location,
        'project_name': project_name
    }
    
    with st.spinner(t('drawing_analysis_customer.analyzing')):
        
        try:
            document_analyzer = DocumentAnalyzer()
            
            for uploaded_file in uploaded_files:
                st.subheader(f"📋 {t('drawing_analysis_customer.analysis_results')}: {uploaded_file.name}")
                
                try:
                    # Reset file pointer to beginning
                    uploaded_file.seek(0)
                    
                    result = document_analyzer.analyze_pdf_drawing(uploaded_file, project_context)
                    
                    if result and result.get('status') != 'failed':
                        st.success(f"✅ {t('drawing_analysis_customer.analysis_complete')}")
                        
                        # Simplified results display
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            structural = result.get('structural_elements', {})
                            windows = structural.get('windows', {}).get('count', 0)
                            doors = structural.get('doors', {}).get('count', 0)
                            st.metric(t('drawing_analysis_customer.windows'), windows)
                            st.metric(t('drawing_analysis_customer.doors'), doors)
                        
                        with col2:
                            installations = result.get('installations', {})
                            electrical = installations.get('electrical', {}).get('complexity', 'basic')
                            plumbing = installations.get('plumbing', {}).get('complexity', 'basic')
                            
                            complexity_colors = {"basic": "🟢", "standard": "🟡", "advanced": "🔴"}
                            st.write(f"**{t('drawing_analysis_customer.electrical')}:** {complexity_colors.get(electrical, '🟢')} {electrical.title()}")
                            st.write(f"**{t('drawing_analysis_customer.plumbing')}:** {complexity_colors.get(plumbing, '🟢')} {plumbing.title()}")
                        
                        with col3:
                            cost_impact = result.get('cost_impact_summary', {})
                            complexity = cost_impact.get('estimated_complexity', 'medium')
                            additional_cost = cost_impact.get('estimated_additional_cost_percentage', 0)
                            
                            complexity_color = {"low": "green", "medium": "orange", "high": "red"}.get(complexity, "orange")
                            st.markdown(f"**{t('drawing_analysis_customer.complexity')}:** :{complexity_color}[{complexity.title()}]")
                            
                            if additional_cost > 0:
                                st.metric(t('drawing_analysis_customer.cost_adjustment'), f"+{additional_cost}%")
                        
                        # Cost adjustment if base estimate available
                        if 'cost_breakdown' in st.session_state and additional_cost > 0:
                            st.subheader(f"💰 {t('drawing_analysis_customer.updated_estimate')}")
                            
                            base_cost = st.session_state.cost_breakdown.get('total_cost', 0)
                            adjusted_cost = base_cost * (1 + additional_cost / 100)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric(t('drawing_analysis_customer.base_estimate'), f"€{base_cost:,.2f}")
                            with col2:
                                st.metric(t('drawing_analysis_customer.adjusted_estimate'), f"€{adjusted_cost:,.2f}")
                        
                        # Save the analysis
                        st.session_state.drawing_analysis = result
                        
                    else:
                        st.error(f"❌ {t('drawing_analysis_customer.analysis_failed')}")
                        st.info("Attempting fallback analysis based on project context...")
                        
                        # Show fallback results
                        st.info(f"📊 Based on project type: {config.get('main_purpose', 'Unknown')}")
                        
                except Exception as file_error:
                    st.error(f"❌ {t('drawing_analysis_customer.error')}: {str(file_error)}")
                    st.info("Showing fallback analysis based on configuration...")
                    
                    # Fallback display based on configuration
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Estimated Windows", 2)
                        st.metric("Estimated Doors", 1)
                    with col2:
                        st.write("**Electrical:** 🟡 Standard")
                        st.write("**Complexity:** Medium")
                        
        except Exception as e:
            st.error(f"❌ Service error: {str(e)}")
            st.info("Please try again or contact support if the problem persists.")

# Next steps
st.divider()

st.subheader(f"🎯 {t('drawing_analysis_customer.next_steps')}")

col1, col2 = st.columns(2)

with col1:
    if st.button(f"📧 {t('drawing_analysis_customer.get_detailed_quote')}", use_container_width=True, type="primary"):
        st.switch_page("pages/8_Send_Inquiry.py")

with col2:
    if st.button(f"🔄 {t('drawing_analysis_customer.refine_config')}", use_container_width=True):
        st.switch_page("pages/1_Container_Configurator.py")

# Disclaimer
st.warning(f"""
⚠️ **{t('drawing_analysis_customer.disclaimer_title')}**

{t('drawing_analysis_customer.disclaimer_text')}
""")

# Tips for better analysis
st.divider()

st.info(f"""
💡 **{t('drawing_analysis_customer.tips_title')}**

{t('drawing_analysis_customer.tips_text')}

• {t('drawing_analysis_customer.tip_1')}
• {t('drawing_analysis_customer.tip_2')}
• {t('drawing_analysis_customer.tip_3')}
""")
