import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
from utils.quote_generator import QuoteGenerator
from utils.calculations import StructuralCalculations
from utils.translations import t, render_language_selector

st.set_page_config(page_title="Quote Generator", page_icon="📄", layout="wide")

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Language selector
render_language_selector()

# Employee access control
if 'employee_logged_in' not in st.session_state:
    st.session_state.employee_logged_in = False

if not st.session_state.employee_logged_in:
    st.title("🔒 " + t('ui.access_denied'))
    st.error(t('quote_generator.employee_only'))
    st.info(t('quote_generator.login_info'))
    st.markdown(f"**{t('quote_generator.employee_password')}:** kan-bud-employee-2024")
    st.stop()

# Initialize services
if 'quote_generator' not in st.session_state:
    st.session_state.quote_generator = QuoteGenerator()

if 'calculations' not in st.session_state:
    st.session_state.calculations = StructuralCalculations()

st.title(f"📄 {t('nav.quote_generator')}")
st.markdown(f"*{t('quote_generator.description')}*")

# Check if configuration and estimates exist
if 'container_config' not in st.session_state or not st.session_state.container_config:
    st.warning(f"⚠️ {t('quote_generator.no_config')}")
    if st.button(t('quote_generator.go_to_configurator')):
        st.switch_page("pages/1_Container_Configurator.py")
    st.stop()

# Quote configuration
st.subheader(f"📋 {t('quote_generator.quote_information')}")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**{t('quote_generator.customer_information')}**")
    customer_name = st.text_input(t('quote_generator.customer_name'))
    customer_company = st.text_input(t('quote_generator.company_name'))
    customer_email = st.text_input(t('quote_generator.email_address'))
    customer_phone = st.text_input(t('quote_generator.phone_number'))

with col2:
    st.markdown(f"**{t('quote_generator.project_information')}**")
    project_name = st.text_input(t('quote_generator.project_name'))
    project_location = st.text_input(t('quote_generator.project_location'))
    delivery_address = st.text_area(t('quote_generator.delivery_address'), height=100)

# Quote parameters
st.subheader("💼 Quote Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    quote_type = st.selectbox(
        "Quote Type",
        ["Preliminary Estimate", "Detailed Quote", "Formal Proposal", "Contract Proposal"]
    )

with col2:
    validity_period = st.selectbox(
        "Quote Validity",
        ["30 days", "60 days", "90 days", "Custom"]
    )

    if validity_period == "Custom":
        custom_validity = st.number_input("Validity Days", min_value=1, max_value=365, value=30)

with col3:
    payment_terms = st.selectbox(
        "Payment Terms",
        ["50% deposit, 50% completion", "30% deposit, 70% completion", "Net 30", "Net 60", "Custom"]
    )

# Pricing options
st.subheader("💰 Pricing Configuration")

col1, col2 = st.columns(2)

with col1:
    profit_margin = st.slider("Profit Margin (%)", min_value=10, max_value=50, value=25)

    contingency = st.slider("Contingency (%)", min_value=5, max_value=20, value=10)

with col2:
    discount_offered = st.slider("Discount (%)", min_value=0, max_value=25, value=0)

    include_warranty = st.checkbox("Include Warranty", value=True)
    warranty_period = "1 year"
    if include_warranty:
        warranty_period = st.selectbox("Warranty Period", ["1 year", "2 years", "5 years"])

# Additional options
st.subheader("📦 Additional Services")

col1, col2 = st.columns(2)

with col1:
    include_delivery = st.checkbox("Include Delivery", value=True)
    delivery_distance = 0
    if include_delivery:
        delivery_distance = st.number_input("Delivery Distance (km)", min_value=0, max_value=1600, value=80)

    include_installation = st.checkbox("Include Installation", value=True)
    include_permits = st.checkbox("Include Permit Assistance", value=False)

with col2:
    include_site_prep = st.checkbox("Include Site Preparation", value=False)
    include_utilities = st.checkbox("Include Utility Connections", value=False)
    include_maintenance = st.checkbox("Include Maintenance Package", value=False)

# Special terms and conditions
special_terms = st.text_area(
    "Special Terms & Conditions",
    placeholder="Enter any special terms, conditions, or notes for this quote...",
    height=100
)

# Generate quote button
if st.button("📄 Generate Professional Quote", type="primary", use_container_width=True):

    # Validate required fields
    required_fields = [customer_name, customer_email, project_name, project_location]
    if not all(required_fields):
        st.error("❌ Please fill in all required fields marked with *")
    else:
        with st.spinner("📄 Generating professional quote..."):

            # Prepare quote data
            quote_data = {
                "customer": {
                    "name": customer_name,
                    "company": customer_company,
                    "email": customer_email,
                    "phone": customer_phone
                },
                "project": {
                    "name": project_name,
                    "location": project_location,
                    "delivery_address": delivery_address
                },
                "quote_params": {
                    "type": quote_type,
                    "validity_period": validity_period,
                    "payment_terms": payment_terms,
                    "profit_margin": profit_margin / 100,
                    "contingency": contingency / 100,
                    "discount": discount_offered / 100
                },
                "services": {
                    "delivery": include_delivery,
                    "delivery_distance": delivery_distance,
                    "installation": include_installation,
                    "permits": include_permits,
                    "site_prep": include_site_prep,
                    "utilities": include_utilities,
                    "maintenance": include_maintenance,
                    "warranty": include_warranty,
                    "warranty_period": warranty_period if include_warranty else None
                },
                "special_terms": special_terms,
                "container_config": st.session_state.container_config
            }

            # Get cost estimates
            if 'ai_estimate' in st.session_state:
                quote_data["cost_estimate"] = st.session_state.ai_estimate

            if 'technical_analysis' in st.session_state:
                quote_data["technical_analysis"] = st.session_state.technical_analysis

            try:
                # Generate quote
                quote = st.session_state.quote_generator.generate_quote(quote_data)
                st.session_state.generated_quote = quote

                st.success("✅ Quote generated successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error generating quote: {str(e)}")

# Display generated quote
if 'generated_quote' in st.session_state:
    quote = st.session_state.generated_quote

    st.divider()
    st.subheader("📄 Generated Quote")

    # Quote header
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"### Quote #{quote.get('quote_number', 'N/A')}")
        st.write(f"**Date:** {quote.get('date', datetime.now().strftime('%Y-%m-%d'))}")
        st.write(f"**Valid Until:** {quote.get('valid_until', 'N/A')}")

    with col2:
        total_cost = quote.get('total_cost', 0)
        st.metric("Total Quote Amount", f"€{total_cost:,.2f}")

    # Customer and project info
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Customer Information:**")
        customer = quote.get('customer', {})
        st.write(f"**Name:** {customer.get('name', 'N/A')}")
        if customer.get('company'):
            st.write(f"**Company:** {customer.get('company')}")
        st.write(f"**Email:** {customer.get('email', 'N/A')}")
        if customer.get('phone'):
            st.write(f"**Phone:** {customer.get('phone')}")

    with col2:
        st.markdown("**Project Information:**")
        project = quote.get('project', {})
        st.write(f"**Project:** {project.get('name', 'N/A')}")
        st.write(f"**Location:** {project.get('location', 'N/A')}")
        if project.get('delivery_address'):
            st.write(f"**Delivery:** {project.get('delivery_address')}")

    # Container specifications
    st.subheader("📦 Container Specifications")

    config = quote.get('container_config', {})
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Base Type:** {config.get('base_type', 'N/A')}")
        st.write(f"**Use Case:** {config.get('use_case', 'N/A')}")
        st.write(f"**Occupancy:** {config.get('occupancy', 'N/A')} people")

    with col2:
        st.write(f"**Environment:** {config.get('environment', 'N/A')}")
        mods = config.get('modifications', {})
        mod_count = sum(1 for v in mods.values() if (isinstance(v, bool) and v) or (isinstance(v, int) and v > 0))
        st.write(f"**Modifications:** {mod_count} items")

    # Cost breakdown
    st.subheader("💰 Cost Breakdown")

    if 'cost_breakdown' in quote:
        breakdown = quote['cost_breakdown']

        # Create breakdown table
        breakdown_data = []
        for category, details in breakdown.items():
            if isinstance(details, dict):
                breakdown_data.append({
                    "Category": category.replace('_', ' ').title(),
                    "Description": details.get('description', ''),
                    "Quantity": details.get('quantity', 1),
                    "Unit Cost": f"€{details.get('unit_cost', 0):,.2f}",
                    "Total": f"€{details.get('total', 0):,.2f}"
                })
            else:
                breakdown_data.append({
                    "Category": category.replace('_', ' ').title(),
                    "Description": "",
                    "Quantity": 1,
                    "Unit Cost": f"€{details:,.2f}",
                    "Total": f"€{details:,.2f}"
                })

        breakdown_df = pd.DataFrame(breakdown_data)
        st.dataframe(breakdown_df, use_container_width=True)

    # Summary costs
    col1, col2, col3 = st.columns(3)

    with col1:
        subtotal = quote.get('subtotal', 0)
        st.metric("Subtotal", f"€{subtotal:,.2f}")

    with col2:
        tax = quote.get('tax', 0)
        st.metric("Tax", f"€{tax:,.2f}")

    with col3:
        total = quote.get('total_cost', 0)
        st.metric("Total", f"€{total:,.2f}")

    # Terms and conditions
    if quote.get('terms_conditions'):
        st.subheader("📋 Terms & Conditions")
        terms = quote['terms_conditions']
        for term in terms:
            st.write(f"• {term}")

    # Project timeline
    if quote.get('timeline'):
        st.subheader("📅 Project Timeline")
        timeline = quote['timeline']

        timeline_df = pd.DataFrame([
            {
                "Phase": phase,
                "Duration": details.get('duration', ''),
                "Description": details.get('description', '')
            }
            for phase, details in timeline.items()
        ])

        st.dataframe(timeline_df, use_container_width=True)

# Action buttons
if 'generated_quote' in st.session_state:
    st.divider()
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📧 Email Quote", use_container_width=True):
            st.success("✅ Quote email functionality would be implemented here")

    with col2:
        if st.button("📱 Download PDF", use_container_width=True):
            # PDF generation would be implemented here
            st.success("✅ PDF download functionality would be implemented here")

    with col3:
        if st.button("🔄 Create New Quote", use_container_width=True):
            if 'generated_quote' in st.session_state:
                del st.session_state.generated_quote
            st.rerun()

    with col4:
        if st.button("⚖️ Compare Quotes", use_container_width=True):
            st.switch_page("pages/5_Comparison_Tool.py")

# Quote templates and history
with st.expander("📝 Quote Templates & History"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Available Templates:**")
        templates = ["Standard Container", "Residential Unit", "Office Space", "Workshop", "Custom"]
        selected_template = st.selectbox("Load Template", templates)
        if st.button("Load Template"):
            st.info(f"Template '{selected_template}' loaded")

    with col2:
        st.markdown("**Recent Quotes:**")
        st.write("• Quote #2024-001 - ABC Company")
        st.write("• Quote #2024-002 - XYZ Industries")
        st.write("• Quote #2024-003 - Local Government")