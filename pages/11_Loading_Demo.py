# Page configuration - MUST BE FIRST
import streamlit as st
st.set_page_config(
    page_title="Container Loading Demo - KAN-BUD",
    page_icon="🎬",
    layout="wide"
)

from utils.translations import t, init_language
from utils.shared_header import render_shared_header
from utils.container_loading_spinner import ContainerLoadingSpinner, show_loading_with_container_theme
import time

# Initialize language system
init_language()

# Render shared header
render_shared_header(show_login=False, current_page="Loading_Demo")

st.title("🎬 Container Loading Animations Demo")
st.markdown("### Demonstracja animacji ładowania o tematyce kontenerowej")

# Initialize the loading spinner
loader = ContainerLoadingSpinner()

# Create tabs for different animation types
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Progress Bar", 
    "Spinning Container", 
    "Crane Animation", 
    "Assembly Process", 
    "Interactive Demo"
])

with tab1:
    st.header("📦 Container Progress Bar")
    st.markdown("Pasek postępu z motywem kontenerowym")
    
    if st.button("Show Progress Animation", key="progress_btn"):
        placeholder = st.empty()
        
        messages = [
            "Inicjalizacja projektu...",
            "Ładowanie specyfikacji...",
            "Analizowanie wymagań...", 
            "Kalkulacja kosztów...",
            "Finalizacja oszacowania..."
        ]
        
        for i in range(21):
            progress = i / 20
            message_idx = min(int(progress * len(messages)), len(messages) - 1)
            current_message = messages[message_idx] if progress > 0 else "Rozpoczynanie..."
            
            progress_html = loader.container_progress_bar(progress, current_message)
            placeholder.markdown(progress_html, unsafe_allow_html=True)
            time.sleep(0.2)
        
        loader.success_animation("Oszacowanie kosztów zostało wygenerowane!")

with tab2:
    st.header("🌀 Spinning Container")
    st.markdown("Obracający się kontener z dźwigiem")
    
    if st.button("Show Spinning Animation", key="spin_btn"):
        duration = st.slider("Animation Duration (seconds)", 1, 10, 3)
        
        placeholder = st.empty()
        loader.show_spinning_container("Przetwarzanie danych kontenerowych...")
        time.sleep(duration)
        placeholder.empty()
        loader.success_animation()

with tab3:
    st.header("🏗️ Crane Loading")
    st.markdown("Animacja dźwigu przemieszczającego kontener")
    
    if st.button("Show Crane Animation", key="crane_btn"):
        duration = st.slider("Crane Duration (seconds)", 2, 8, 4, key="crane_duration")
        loader.show_crane_loading(duration)
        loader.success_animation("Kontener został pomyślnie załadowany!")

with tab4:
    st.header("🔧 Container Assembly")
    st.markdown("Krok po kroku montaż kontenera")
    
    if st.button("Show Assembly Process", key="assembly_btn"):
        custom_steps = [
            "🏗️ Przygotowanie fundamentu...",
            "📦 Ustawienie konstrukcji stalowej...",
            "🔧 Montaż ścian i drzwi...",
            "⚡ Instalacja systemów elektrycznych...",
            "🎨 Wykańczanie wnętrza...",
            "✅ Kontrola jakości i odbiór..."
        ]
        
        loader.show_container_assembly(custom_steps)
        loader.success_animation("Kontener został w pełni zmontowany!")

with tab5:
    st.header("🎮 Interactive Loading Demo")
    st.markdown("Interaktywne demo wszystkich animacji")
    
    col1, col2 = st.columns(2)
    
    with col1:
        animation_type = st.selectbox(
            "Choose Animation Type",
            ["progress", "crane", "assembly", "spinner"],
            format_func=lambda x: {
                "progress": "📊 Progress Bar",
                "crane": "🏗️ Crane Loading", 
                "assembly": "🔧 Assembly Process",
                "spinner": "🌀 Spinning Container"
            }[x]
        )
        
        duration = st.slider("Duration (seconds)", 1, 8, 3, key="interactive_duration")
        custom_message = st.text_input("Custom Message", "Przetwarzanie projektu...")
    
    with col2:
        if st.button("🚀 Start Interactive Demo", key="interactive_btn"):
            if animation_type == "progress":
                show_loading_with_container_theme(duration, "progress", custom_message)
            elif animation_type == "crane":
                show_loading_with_container_theme(duration, "crane", custom_message)
            elif animation_type == "assembly":
                show_loading_with_container_theme(duration, "assembly", custom_message)
            elif animation_type == "spinner":
                show_loading_with_container_theme(duration, "spinner", custom_message)

# Usage examples section
st.markdown("---")
st.header("💡 Integration Examples")
st.markdown("Przykłady integracji w aplikacji")

with st.expander("How to use in your code"):
    st.code('''
# Import the loading spinner
from utils.container_loading_spinner import ContainerLoadingSpinner

# Initialize
loader = ContainerLoadingSpinner()

# Show progress during processing
loader.show_interactive_progress(
    total_steps=5, 
    current_step=2, 
    message="Processing your request..."
)

# Show spinning animation
loader.show_spinning_container("Loading data...")

# Show success when complete
loader.success_animation("Process completed!")
    ''', language='python')

st.markdown("### 🎯 Perfect for:")
st.markdown("""
- **AI Cost Estimation**: Podczas generowania oszacowań kosztów
- **3D Model Loading**: Ładowanie modeli 3D kontenerów  
- **Data Processing**: Przetwarzanie dużych zestawów danych
- **File Uploads**: Przesyłanie plików i dokumentów
- **Database Operations**: Operacje na bazie danych
- **Report Generation**: Generowanie raportów PDF
""")