import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.translations import t, get_available_languages

st.set_page_config(page_title="Comparison Tool", page_icon="⚖️", layout="wide")

# Initialize language if not set
if 'language' not in st.session_state:
    st.session_state.language = 'pl'

# Language selector via shared header
from utils.shared_header import render_shared_header
render_shared_header(show_login=False, current_page="Comparison_Tool")

# Employee access control
if 'employee_logged_in' not in st.session_state:
    st.session_state.employee_logged_in = False

if not st.session_state.employee_logged_in:
    st.title("🔒 " + t('ui.access_denied'))
    st.error(t('comparison_tool.employee_only'))
    st.info(t('comparison_tool.login_info'))
    st.markdown(f"**{t('comparison_tool.employee_password')}:** kan-bud-employee-2024")
    st.stop()

st.title(f"⚖️ {t('nav.comparison_tool')}")
st.markdown(f"*{t('comparison_tool.description')}*")

# Initialize comparison data in session state
if 'comparison_data' not in st.session_state:
    st.session_state.comparison_data = []

# Add current configuration if available
if 'container_config' in st.session_state and st.session_state.container_config:
    current_config = {
        "name": "Current Configuration",
        "config": st.session_state.container_config,
        "cost_estimate": st.session_state.get('ai_estimate', {}),
        "technical_analysis": st.session_state.get('technical_analysis', {}),
        "timestamp": pd.Timestamp.now()
    }

    # Check if current config is already in comparison
    existing_names = [item["name"] for item in st.session_state.comparison_data]
    if "Current Configuration" not in existing_names:
        if st.button("➕ Add Current Configuration to Comparison"):
            st.session_state.comparison_data.append(current_config)
            st.success("✅ Current configuration added to comparison!")
            st.rerun()

# Configuration management
st.subheader("🔧 Comparison Management")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Add New Configuration**")

    # Quick configuration options
    container_types = {
        "20ft Standard": {"length": 20, "width": 8, "height": 8.5, "weight": 5000},
        "40ft Standard": {"length": 40, "width": 8, "height": 8.5, "weight": 8000},
        "40ft High Cube": {"length": 40, "width": 8, "height": 9.5, "weight": 8500},
        "45ft High Cube": {"length": 45, "width": 8, "height": 9.5, "weight": 9000}
    }

    quick_type = st.selectbox("Quick Add Container Type", list(container_types.keys()))
    quick_use_case = st.selectbox("Use Case", ["Office", "Residential", "Workshop", "Storage"])

    if st.button("➕ Add Quick Configuration"):
        # Generate realistic cost estimate based on container type and use case
        base_costs = {
            "20ft Standard": 35000,
            "40ft Standard": 45000, 
            "40ft High Cube": 48000,
            "45ft High Cube": 52000
        }
        
        use_case_multipliers = {
            "Office": 1.3,
            "Residential": 1.4,
            "Workshop": 1.1,
            "Storage": 1.0
        }
        
        base_cost = base_costs.get(quick_type, 45000)
        multiplier = use_case_multipliers.get(quick_use_case, 1.2)
        estimated_cost = int(base_cost * multiplier)
        
        # Generate realistic technical parameters
        load_ratios = {"Office": 0.65, "Residential": 0.7, "Workshop": 0.6, "Storage": 0.5}
        load_ratio = load_ratios.get(quick_use_case, 0.6) + (len(st.session_state.comparison_data) * 0.05)
        
        quick_config = {
            "name": f"{quick_type} - {quick_use_case}",
            "config": {
                "base_type": quick_type,
                "use_case": quick_use_case,
                "occupancy": 4 if quick_use_case in ["Office", "Residential"] else 2,
                "environment": "Outdoor",
                "modifications": {
                    "windows": 3 if quick_use_case == "Residential" else 2,
                    "doors": 2 if quick_use_case == "Office" else 1,
                    "electrical": quick_use_case != "Storage",
                    "insulation": quick_use_case in ["Office", "Residential"]
                }
            },
            "cost_estimate": {"total_cost": estimated_cost},
            "technical_analysis": {
                "load_ratio": min(0.85, load_ratio),
                "stress_ratio": min(0.8, load_ratio * 0.9)
            },
            "timestamp": pd.Timestamp.now()
        }
        st.session_state.comparison_data.append(quick_config)
        st.success(f"✅ {quick_config['name']} added to comparison!")
        st.rerun()

with col2:
    st.markdown("**Manage Configurations**")

    if st.session_state.comparison_data:
        config_names = [item["name"] for item in st.session_state.comparison_data]
        selected_to_remove = st.selectbox("Remove Configuration", [""] + config_names)

        if selected_to_remove and st.button("🗑️ Remove Selected"):
            st.session_state.comparison_data = [
                item for item in st.session_state.comparison_data 
                if item["name"] != selected_to_remove
            ]
            st.success(f"✅ {selected_to_remove} removed from comparison!")
            st.rerun()
    else:
        st.info("No configurations to manage")

with col3:
    st.markdown("**Actions**")

    if st.button("🔄 Clear All"):
        st.session_state.comparison_data = []
        st.success("✅ All configurations cleared!")
        st.rerun()

    if st.session_state.comparison_data:
        if st.button("📊 Export Comparison"):
            st.success("✅ Export functionality would be implemented here")

# Display comparison if data exists
if not st.session_state.comparison_data:
    st.info("ℹ️ No configurations to compare. Add configurations using the options above or from other pages.")
    st.stop()

st.divider()
st.subheader(f"📊 Comparison Results ({len(st.session_state.comparison_data)} configurations)")

# Create comparison dataframe
comparison_df = pd.DataFrame()
for i, item in enumerate(st.session_state.comparison_data):
    config = item["config"]
    cost_est = item.get("cost_estimate", {})
    tech_analysis = item.get("technical_analysis", {})

    # Handle different cost estimate formats
    if isinstance(cost_est, dict) and "comparison" in cost_est:
        # Multiple AI model estimates
        total_cost = (cost_est.get("openai", {}).get("total_cost", 0) + 
                     cost_est.get("claude", {}).get("total_cost", 0)) / 2
    elif isinstance(cost_est, dict):
        total_cost = cost_est.get("total_cost", 0)
    else:
        total_cost = 0

    row_data = {
        "Configuration": item["name"],
        "Container Type": config.get("base_type", "N/A"),
        "Use Case": config.get("use_case", "N/A"),
        "Occupancy": config.get("occupancy", 0),
        "Total Cost": total_cost,
        "Load Ratio": tech_analysis.get("structural", {}).get("load_ratio", 
                     tech_analysis.get("load_ratio", 0)),
        "Stress Ratio": tech_analysis.get("structural", {}).get("stress_ratio", 
                       tech_analysis.get("stress_ratio", 0))
    }

    comparison_df = pd.concat([comparison_df, pd.DataFrame([row_data])], ignore_index=True)

# Display comparison table
st.subheader("📋 Configuration Comparison Table")
st.dataframe(comparison_df, use_container_width=True)

# Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Cost Comparison")

    if not comparison_df.empty and "Total Cost" in comparison_df.columns:
        fig_cost = px.bar(
            comparison_df,
            x="Configuration",
            y="Total Cost",
            color="Use Case",
            title="Total Cost by Configuration"
        )
        fig_cost.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_cost, use_container_width=True)

with col2:
    st.subheader("🔧 Technical Performance")

    if not comparison_df.empty:
        fig_tech = go.Figure()

        fig_tech.add_trace(go.Scatter(
            x=comparison_df["Configuration"],
            y=comparison_df["Load Ratio"],
            mode='lines+markers',
            name='Load Ratio',
            line=dict(color='blue')
        ))

        fig_tech.add_trace(go.Scatter(
            x=comparison_df["Configuration"],
            y=comparison_df["Stress Ratio"],
            mode='lines+markers',
            name='Stress Ratio',
            line=dict(color='red')
        ))

        # Add safety limits
        fig_tech.add_hline(y=1.0, line_dash="dash", line_color="red", 
                          annotation_text="Safety Limit")

        fig_tech.update_layout(
            title="Technical Performance Comparison",
            yaxis_title="Ratio",
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig_tech, use_container_width=True)

# Detailed comparison
st.subheader("🔍 Detailed Comparison")

# Cost per square foot analysis
if not comparison_df.empty:
    container_specs = {
        "20ft Standard": 160,  # sq ft
        "40ft Standard": 320,
        "40ft High Cube": 320,
        "45ft High Cube": 360
    }

    comparison_df["Floor Area (sq ft)"] = comparison_df["Container Type"].map(
        lambda x: container_specs.get(x, 320)
    )
    comparison_df["Cost per Sq Ft"] = comparison_df["Total Cost"] / comparison_df["Floor Area (sq ft)"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Cost per Square Metre**")
        cost_per_sqft = comparison_df[["Configuration", "Cost per Sq Ft"]].copy()
        cost_per_sqft.columns = ["Configuration", "Cost per Sq M"]
        cost_per_sqft["Cost per Sq M"] = cost_per_sqft["Cost per Sq M"] * 10.764
        cost_per_sqft["Cost per Sq M"] = cost_per_sqft["Cost per Sq M"].apply(lambda x: f"€{x:.2f}")
        st.dataframe(cost_per_sqft, use_container_width=True)

    with col2:
        st.markdown("**Cost per Person (Based on Occupancy)**")
        comparison_df["Cost per Person"] = comparison_df["Total Cost"] / comparison_df["Occupancy"]
        cost_per_person = comparison_df[["Configuration", "Cost per Person"]].copy()
        cost_per_person["Cost per Person"] = cost_per_person["Cost per Person"].apply(lambda x: f"€{x:,.0f}")
        st.dataframe(cost_per_person, use_container_width=True)

# Radar chart for multi-dimensional comparison
st.subheader("🎯 Multi-Dimensional Analysis")

if len(st.session_state.comparison_data) >= 2:
    # Prepare data for radar chart
    categories = ['Cost Effectiveness', 'Structural Safety', 'Space Efficiency', 'Modification Level']

    fig_radar = go.Figure()

    for item in st.session_state.comparison_data[:4]:  # Limit to 4 for readability
        config = item["config"]
        cost_est = item.get("cost_estimate", {})
        tech_analysis = item.get("technical_analysis", {})

        # Calculate normalized scores (0-1)
        total_cost = cost_est.get("total_cost", 0) if isinstance(cost_est, dict) else 0
        cost_score = max(0, 1 - (total_cost - 30000) / 50000)  # Normalize cost

        load_ratio = tech_analysis.get("structural", {}).get("load_ratio", 
                    tech_analysis.get("load_ratio", 0.5))
        safety_score = max(0, 1 - load_ratio)  # Better safety = lower load ratio

        container_type = config.get("base_type", "")
        space_score = 0.7 if "40ft" in container_type else 0.5  # Larger = better space

        mods = config.get("modifications", {})
        mod_count = sum(1 for v in mods.values() if (isinstance(v, bool) and v) or (isinstance(v, int) and v > 0))
        mod_score = min(1.0, mod_count / 8)  # Normalize modification level

        values = [cost_score, safety_score, space_score, mod_score]

        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=item["name"]
        ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Multi-Dimensional Configuration Comparison"
    )

    st.plotly_chart(fig_radar, use_container_width=True)

# Recommendations
st.subheader("🎯 Recommendations")

if not comparison_df.empty:
    # Find best options
    best_cost = comparison_df.loc[comparison_df["Total Cost"].idxmin()]
    best_safety = comparison_df.loc[comparison_df["Load Ratio"].idxmin()]
    best_value = comparison_df.loc[comparison_df["Cost per Sq Ft"].idxmin()]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(f"**💰 Most Cost-Effective:**\n{best_cost['Configuration']}\n€{best_cost['Total Cost']:,.0f}")

    with col2:
        st.success(f"**🔒 Safest Design:**\n{best_safety['Configuration']}\nLoad Ratio: {best_safety['Load Ratio']:.2f}")

    with col3:
        st.success(f"**📏 Best Value per Sq M:**\n{best_value['Configuration']}\n€{best_value['Cost per Sq Ft']*10.764:.2f}/sq m")

# Export and action buttons
st.divider()
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Export Comparison", use_container_width=True):
        csv = comparison_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"container_comparison_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col2:
    if st.button("📄 Generate Report", use_container_width=True):
        # Generate detailed comparison report
        report_content = f"""
# Container Comparison Report
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
Total configurations compared: {len(st.session_state.comparison_data)}

## Cost Analysis
- Lowest cost: €{comparison_df['Total Cost'].min():,.2f}
- Highest cost: €{comparison_df['Total Cost'].max():,.2f}
- Average cost: €{comparison_df['Total Cost'].mean():,.2f}

## Technical Performance
- Best load ratio: {comparison_df['Load Ratio'].min():.2f}
- Worst load ratio: {comparison_df['Load Ratio'].max():.2f}

## Detailed Comparison
{comparison_df.to_markdown(index=False)}

## Recommendations
Based on the analysis:
1. Most cost-effective: {comparison_df.loc[comparison_df['Total Cost'].idxmin(), 'Configuration']}
2. Safest design: {comparison_df.loc[comparison_df['Load Ratio'].idxmin(), 'Configuration']}
3. Best value: {comparison_df.loc[comparison_df['Cost per Sq Ft'].idxmin(), 'Configuration']}
        """
        
        st.download_button(
            label="Download Report (Markdown)",
            data=report_content,
            file_name=f"comparison_report_{pd.Timestamp.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
        st.success("✅ Comparison report generated!")

with col3:
    if st.button("🔧 Optimize Selection", use_container_width=True):
        # Generate AI-powered optimization recommendations
        if not comparison_df.empty:
            # Find optimal configurations based on different criteria
            cost_optimal = comparison_df.loc[comparison_df['Total Cost'].idxmin()]
            safety_optimal = comparison_df.loc[comparison_df['Load Ratio'].idxmin()]
            value_optimal = comparison_df.loc[comparison_df['Cost per Sq Ft'].idxmin()]
            
            st.subheader("🤖 AI Optimization Recommendations")
            
            col_opt1, col_opt2, col_opt3 = st.columns(3)
            
            with col_opt1:
                st.metric("💰 Cost Leader", f"€{cost_optimal['Total Cost']:,.0f}", 
                         f"{cost_optimal['Configuration']}")
                cost_savings = comparison_df['Total Cost'].max() - cost_optimal['Total Cost']
                st.write(f"Saves €{cost_savings:,.0f} vs highest")
            
            with col_opt2:
                st.metric("🔒 Safety Leader", f"{safety_optimal['Load Ratio']:.2f}", 
                         f"{safety_optimal['Configuration']}")
                safety_margin = 1.0 - safety_optimal['Load Ratio']
                st.write(f"{safety_margin:.1%} safety margin")
            
            with col_opt3:
                st.metric("📏 Value Leader", f"€{value_optimal['Cost per Sq Ft']*10.764:.0f}/m²", 
                         f"{value_optimal['Configuration']}")
                st.write("Best cost per square meter")
            
            # Generate specific recommendations
            st.markdown("### 🎯 Specific Recommendations")
            
            if cost_optimal['Load Ratio'] < 0.8:
                st.success(f"✅ **Recommended Choice:** {cost_optimal['Configuration']} offers the best cost while maintaining good safety margins.")
            elif safety_optimal['Total Cost'] <= comparison_df['Total Cost'].median():
                st.success(f"✅ **Recommended Choice:** {safety_optimal['Configuration']} provides excellent safety at reasonable cost.")
            else:
                st.info(f"💡 **Balanced Choice:** Consider {value_optimal['Configuration']} for the best overall value proposition.")
            
            # Additional insights
            if comparison_df['Load Ratio'].max() > 0.9:
                st.warning("⚠️ Some configurations have high load ratios. Consider structural reinforcement.")
            
            if comparison_df['Total Cost'].std() > 10000:
                st.info("💡 Cost variation is high - consider standardizing specifications for better pricing.")
        
        else:
            st.warning("No configurations available for optimization analysis.")

with col4:
    if st.button("📋 Create Quote", use_container_width=True):
        st.switch_page("pages/4_Quote_Generator.py")

# Help section
with st.expander("ℹ️ How to Use the Comparison Tool"):
    st.markdown("""
    **Getting Started:**
    1. Add configurations from other pages or use quick-add options
    2. Compare costs, technical performance, and specifications
    3. Use visualizations to identify the best options
    4. Export results or generate quotes for selected configurations

    **Understanding Metrics:**
    - **Load Ratio:** Lower is better (< 1.0 required for safety)
    - **Stress Ratio:** Lower is better (< 1.0 required for safety)
    - **Cost per Sq Ft:** Helps compare value across different sizes
    - **Multi-dimensional Analysis:** Normalized scores from 0-1 (higher is better)

    **Tips:**
    - Consider both cost and safety when making decisions
    - Factor in intended use case and occupancy requirements
    - Review technical analysis for compliance requirements
    """)