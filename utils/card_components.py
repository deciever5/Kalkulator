"""
Professional Card Components for KAN-BUD Container Solutions
Implements styled card layouts for better visual presentation
"""

import streamlit as st
import base64

def load_card_css():
    """Load the professional card CSS styling"""
    try:
        with open('styles/professional_cards.css', 'r') as f:
            css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def render_configuration_card(container_type, title, description, specs, is_selected=False):
    """Render a professional configuration card for container types"""
    
    container_class = f"container-{container_type.lower().replace(' ', '-').replace('(', '').replace(')', '')}"
    selected_class = "selected" if is_selected else ""
    
    card_html = f"""
    <div class="config-card {container_class} {selected_class} fade-in">
        <h3 style="margin: 0 0 12px 0; color: #2d3748; font-size: 20px; font-weight: 600;">{title}</h3>
        <p style="margin: 0 0 16px 0; color: #718096; font-size: 14px;">{description}</p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px;">
            {specs}
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def render_cost_breakdown_card(cost_item, amount, percentage, icon, category):
    """Render a professional cost breakdown card"""
    
    icon_class = f"icon-{category.lower()}"
    progress_width = min(percentage, 100)
    
    card_html = f"""
    <div class="cost-card slide-up">
        <div class="cost-card-header">
            <div class="cost-card-icon {icon_class}">
                {icon}
            </div>
            <div style="flex: 1;">
                <h4 style="margin: 0; color: #2d3748; font-size: 16px; font-weight: 600;">{cost_item}</h4>
                <div class="cost-card-amount">€{amount:,.0f}</div>
            </div>
            <div style="text-align: right; color: #718096; font-size: 14px;">
                {percentage:.1f}%
            </div>
        </div>
        <div class="cost-progress-bar">
            <div class="cost-progress-fill" style="width: {progress_width}%;"></div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def render_feature_card(title, subtitle, current_value, upgrade_options, before_preview, after_preview):
    """Render an expandable feature modification card"""
    
    card_html = f"""
    <div class="feature-card">
        <div class="feature-card-title">{title}</div>
        <div class="feature-card-subtitle">{subtitle}</div>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #4a5568; font-weight: 500;">Current: {current_value}</span>
            <span style="color: #667eea; font-size: 12px;">Hover to see options</span>
        </div>
        <div class="feature-card-expanded">
            <div style="margin: 16px 0;">
                <strong style="color: #2d3748;">Available Upgrades:</strong>
                <ul style="margin: 8px 0; padding-left: 20px; color: #4a5568;">
                    {upgrade_options}
                </ul>
            </div>
            <div class="before-after-preview">
                <div class="preview-item">
                    <div style="font-size: 12px; font-weight: 600; color: #718096; margin-bottom: 8px;">BEFORE</div>
                    <div style="color: #4a5568;">{before_preview}</div>
                </div>
                <div class="preview-item">
                    <div style="font-size: 12px; font-weight: 600; color: #718096; margin-bottom: 8px;">AFTER</div>
                    <div style="color: #4a5568;">{after_preview}</div>
                </div>
            </div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def render_quote_summary_card(total_cost, project_duration, confidence_rating, container_type, modifications_count):
    """Render the executive quote summary card"""
    
    confidence_percentage = int(confidence_rating * 100)
    
    card_html = f"""
    <div class="quote-summary-card slide-up">
        <div class="quote-summary-title">Professional Quote Summary</div>
        <div class="quote-summary-subtitle">Complete container modification solution for {container_type}</div>
        
        <div class="quote-metrics">
            <div class="quote-metric">
                <div class="quote-metric-value">€{total_cost:,.0f}</div>
                <div class="quote-metric-label">Total Project Cost</div>
            </div>
            <div class="quote-metric">
                <div class="quote-metric-value">{project_duration}</div>
                <div class="quote-metric-label">Estimated Timeline</div>
            </div>
            <div class="quote-metric">
                <div class="quote-metric-value">{confidence_percentage}%</div>
                <div class="quote-metric-label">Accuracy Confidence</div>
            </div>
            <div class="quote-metric">
                <div class="quote-metric-value">{modifications_count}</div>
                <div class="quote-metric-label">Modifications</div>
            </div>
        </div>
        
        <div style="margin-top: 24px; padding: 16px; background: rgba(255, 255, 255, 0.1); border-radius: 12px; text-align: center;">
            <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">Ready for Professional Review</div>
            <div style="font-size: 12px; opacity: 0.8;">Quote valid for 30 days • Professional engineering included</div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def create_specs_grid(specs_dict):
    """Create a specifications grid for configuration cards"""
    specs_html = ""
    for label, value in specs_dict.items():
        specs_html += f"""
        <div style="text-align: center; padding: 8px; background: #f7fafc; border-radius: 6px;">
            <div style="font-size: 12px; color: #718096; margin-bottom: 4px;">{label}</div>
            <div style="font-size: 14px; font-weight: 600; color: #2d3748;">{value}</div>
        </div>
        """
    return specs_html

def create_upgrade_list(upgrades):
    """Create HTML list for upgrade options"""
    list_items = ""
    for upgrade in upgrades:
        list_items += f"<li>{upgrade}</li>"
    return list_items

# Icon constants for different categories
COST_ICONS = {
    'container': '📦',
    'structural': '🏗️',
    'electrical': '⚡',
    'plumbing': '🔧',
    'interior': '🏠',
    'delivery': '🚛'
}

def get_cost_icon(category):
    """Get appropriate icon for cost category"""
    return COST_ICONS.get(category.lower(), '💼')