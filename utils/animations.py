"""
Micro-interactions and Loading Animations for KAN-BUD Container Solutions
Provides smooth, engaging visual feedback for user interactions
"""

import streamlit as st
import time
import random

def show_loading_animation(text="Processing...", duration=2):
    """Display a smooth loading animation with progress"""
    
    # Container for the loading animation
    loading_container = st.empty()
    
    # CSS for smooth animations
    st.markdown("""
    <style>
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #3b82f6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 10px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .progress-bar {
        width: 100%;
        height: 6px;
        background-color: #e5e7eb;
        border-radius: 3px;
        overflow: hidden;
        margin-top: 10px;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        border-radius: 3px;
        transition: width 0.3s ease;
    }
    
    .loading-text {
        animation: pulse 1.5s ease-in-out infinite;
        color: #6b7280;
        font-weight: 500;
    }
    
    .loading-dots::after {
        content: '';
        animation: dots 1.5s steps(5, end) infinite;
    }
    
    @keyframes dots {
        0%, 20% { content: ''; }
        40% { content: '.'; }
        60% { content: '..'; }
        80%, 100% { content: '...'; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Progress simulation
    for i in range(0, 101, 5):
        progress_html = f"""
        <div style="text-align: center; padding: 20px;">
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                <div class="loading-spinner"></div>
                <span class="loading-text">{text}<span class="loading-dots"></span></span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {i}%;"></div>
            </div>
            <div style="margin-top: 10px; font-size: 14px; color: #9ca3af;">
                {i}% Complete
            </div>
        </div>
        """
        
        loading_container.markdown(progress_html, unsafe_allow_html=True)
        time.sleep(duration / 20)  # Divide duration by number of steps
    
    loading_container.empty()

def add_hover_animations():
    """Add hover animations and micro-interactions to UI elements"""
    
    st.markdown("""
    <style>
    /* Button hover animations */
    .stButton > button {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.2) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
        transition: all 0.1s ease !important;
    }
    
    /* Ripple effect for buttons */
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:active::before {
        width: 300px;
        height: 300px;
    }
    
    /* Input field animations */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        transition: all 0.3s ease !important;
        border: 2px solid transparent !important;
    }
    
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        transform: scale(1.02) !important;
    }
    
    /* Card hover animations */
    .stContainer > div {
        transition: all 0.3s ease !important;
    }
    
    /* Metric card animations */
    .stMetric {
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    .stMetric:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Checkbox animations */
    .stCheckbox > label {
        transition: all 0.2s ease !important;
    }
    
    .stCheckbox > label:hover {
        transform: scale(1.05) !important;
    }
    
    /* Success/Error message animations */
    .stSuccess, .stError, .stWarning, .stInfo {
        animation: slideIn 0.5s ease-out !important;
        transition: all 0.3s ease !important;
    }
    
    /* Table row hover */
    .stDataFrame tbody tr {
        transition: background-color 0.2s ease !important;
    }
    
    .stDataFrame tbody tr:hover {
        background-color: rgba(59, 130, 246, 0.05) !important;
    }
    
    /* Sidebar animations (if used) */
    .css-1d391kg {
        transition: all 0.3s ease !important;
    }
    
    /* Loading state for elements */
    .loading-pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite !important;
    }
    
    /* Smooth scroll behavior */
    html {
        scroll-behavior: smooth !important;
    }
    
    /* Fade in animation for content */
    .fade-in {
        animation: fadeIn 0.6s ease-in !important;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Scale animation for icons */
    .scale-hover {
        transition: transform 0.2s ease !important;
    }
    
    .scale-hover:hover {
        transform: scale(1.1) !important;
    }
    
    /* Floating animation for special elements */
    .float {
        animation: float 3s ease-in-out infinite !important;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    </style>
    """, unsafe_allow_html=True)

def show_success_animation(message="Success!", duration=2):
    """Display animated success message"""
    
    success_container = st.empty()
    
    success_html = f"""
    <div style="text-align: center; padding: 20px; animation: bounce 0.6s ease;">
        <div style="font-size: 48px; color: #10b981; margin-bottom: 10px;">
            ✓
        </div>
        <div style="font-size: 18px; font-weight: 600; color: #065f46;">
            {message}
        </div>
    </div>
    """
    
    success_container.markdown(success_html, unsafe_allow_html=True)
    time.sleep(duration)
    success_container.empty()

def show_calculation_steps(steps, delay=0.8):
    """Show animated calculation steps"""
    
    st.markdown("""
    <style>
    .calc-step {
        padding: 12px 16px;
        margin: 8px 0;
        background: #f8fafc;
        border-left: 4px solid #3b82f6;
        border-radius: 6px;
        animation: slideIn 0.5s ease-out;
        transition: all 0.3s ease;
    }
    
    .calc-step:hover {
        background: #f1f5f9;
        transform: translateX(5px);
    }
    
    .calc-step.active {
        background: #dbeafe;
        border-left-color: #1d4ed8;
    }
    
    .step-number {
        background: #3b82f6;
        color: white;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 600;
        margin-right: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    step_container = st.empty()
    
    for i, step in enumerate(steps):
        # Show steps progressively
        steps_html = ""
        for j, s in enumerate(steps[:i+1]):
            active_class = "active" if j == i else ""
            steps_html += f"""
            <div class="calc-step {active_class}">
                <span class="step-number">{j+1}</span>
                {s}
            </div>
            """
        
        step_container.markdown(steps_html, unsafe_allow_html=True)
        time.sleep(delay)

def show_typing_animation(text, container, speed=0.05):
    """Simulate typing effect for text"""
    
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f"<div style='font-family: monospace;'>{displayed_text}<span style='animation: blink 1s infinite;'>|</span></div>", 
                          unsafe_allow_html=True)
        time.sleep(speed)
    
    # Final text without cursor
    container.markdown(f"<div>{text}</div>", unsafe_allow_html=True)

def add_page_transition():
    """Add smooth page transition effects"""
    
    st.markdown("""
    <style>
    .stApp {
        animation: pageLoad 0.5s ease-in-out !important;
    }
    
    @keyframes pageLoad {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    </style>
    """, unsafe_allow_html=True)

def create_animated_counter(target_value, label, prefix="€", suffix="", duration=2):
    """Create animated counter for displaying values"""
    
    container = st.empty()
    steps = 30
    step_value = target_value / steps
    
    for i in range(steps + 1):
        current_value = int(step_value * i)
        
        counter_html = f"""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 36px; font-weight: 700; color: #1f2937; margin-bottom: 8px;">
                {prefix}{current_value:,}{suffix}
            </div>
            <div style="font-size: 16px; color: #6b7280; font-weight: 500;">
                {label}
            </div>
        </div>
        """
        
        container.markdown(counter_html, unsafe_allow_html=True)
        time.sleep(duration / steps)

def show_calculation_animation(calculation_data):
    """Show animated calculation process with steps"""
    
    st.markdown("### 🔄 Calculating Your Quote...")
    
    calculation_steps = [
        "📦 Analyzing container specifications...",
        "🔧 Processing modifications and features...", 
        "💰 Calculating material and labor costs...",
        "🚛 Computing delivery and logistics...",
        "🎯 Applying discounts and optimizations...",
        "✅ Finalizing your custom quote..."
    ]
    
    # Show loading animation
    show_loading_animation("Calculating comprehensive quote", 3)
    
    # Show calculation steps
    show_calculation_steps(calculation_steps, 0.6)
    
    # Show success
    show_success_animation("Quote Generated Successfully!", 1.5)