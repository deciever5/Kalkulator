"""
Sidebar Navigation Manager
Manages sidebar visibility and removes redundant items
"""

import streamlit as st
from utils.translations import t

def hide_sidebar():
    """Hide sidebar completely for cleaner interface"""
    st.markdown("""
        <style>
        .css-1d391kg {display: none;}
        .css-1y4p8pa {max-width: 100%;}
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stSidebarNav"] {display: none;}
        .css-17eq0hr {display: none;}
        </style>
    """, unsafe_allow_html=True)

def show_minimal_sidebar():
    """Show minimal sidebar with only essential customer features"""
    
    # Check if user is logged in as employee
    is_employee = st.session_state.get('employee_logged_in', False)
    
    # Customer-accessible pages (always visible)
    customer_pages = [
        ("🏗️", "Container Configurator", "pages/1_Container_Configurator.py"),
        ("🤖", "AI Cost Estimator", "pages/2_AI_Cost_Estimator.py"),
        ("📊", "Bulk Pricing", "pages/10_Bulk_Pricing.py"),
        ("📐", "Drawing Analysis", "pages/9_Customer_Drawing_Analysis.py"),
        ("📝", "Send Inquiry", "pages/8_Send_Inquiry.py")
    ]
    
    # Employee-only pages (only visible after login)
    employee_pages = [
        ("🔧", "Technical Analysis", "pages/3_Technical_Analysis.py"),
        ("📋", "Quote Generator", "pages/4_Quote_Generator.py"),
        ("⚖️", "Comparison Tool", "pages/5_Comparison_Tool.py"),
        ("📐", "Advanced Drawing Analysis", "pages/6_Drawing_Analysis.py"),
        ("🎬", "Loading Demo", "pages/11_Loading_Demo.py"),
        ("👤", "Admin Panel", "pages/12_Admin_Panel.py")
    ]
    
    # Display navigation in sidebar
    st.sidebar.markdown("### 🏗️ KAN-BUD Navigation")
    
    # Customer pages
    st.sidebar.markdown("**Customer Tools**")
    for icon, name, path in customer_pages:
        if st.sidebar.button(f"{icon} {name}", key=f"nav_{name}", use_container_width=True):
            st.switch_page(path)
    
    # Employee pages (only if logged in)
    if is_employee:
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Professional Tools**")
        for icon, name, path in employee_pages:
            if st.sidebar.button(f"{icon} {name}", key=f"nav_employee_{name}", use_container_width=True):
                st.switch_page(path)
        
        # Logout button
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout", key="logout_btn", use_container_width=True):
            st.session_state.employee_logged_in = False
            st.rerun()
    
    # Return to home
    st.sidebar.markdown("---")
    if st.sidebar.button("🏠 Home", key="nav_home", use_container_width=True):
        st.switch_page("app.py")

def configure_clean_navigation():
    """Configure clean navigation without redundant sidebar items"""
    
    # Hide default Streamlit navigation
    st.markdown("""
        <style>
        /* Hide default sidebar navigation */
        .css-17eq0hr {display: none;}
        .css-1y4p8pa {max-width: 100%;}
        
        /* Clean up page header */
        .css-1rs6os {display: none;}
        .css-17ziqus {display: none;}
        
        /* Style sidebar buttons */
        .stButton button {
            width: 100%;
            text-align: left;
            border: none;
            background: transparent;
            color: #262730;
            padding: 8px 12px;
            margin: 2px 0;
            border-radius: 5px;
        }
        
        .stButton button:hover {
            background-color: #f0f2f6;
            color: #ff6b6b;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #fafafa;
            border-right: 1px solid #e0e0e0;
        }
        
        /* Hide redundant elements */
        [data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)