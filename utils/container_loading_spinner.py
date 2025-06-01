"""
Container-Themed Loading Spinner and Animation System
Provides interactive loading animations with container construction themes
"""

import streamlit as st
import time
import random
from typing import List, Optional

class ContainerLoadingSpinner:
    """Container-themed loading spinner with various animation styles"""
    
    def __init__(self):
        self.container_stages = [
            "🏗️ Przygotowywanie fundamentów...",
            "📦 Montaż konstrukcji stalowej...", 
            "🔧 Instalacja systemów...",
            "🎨 Wykańczanie wnętrza...",
            "✅ Finalizacja projektu..."
        ]
        
        self.loading_messages = [
            "Analizujemy Twoje wymagania...",
            "Obliczamy koszty materiałów...",
            "Sprawdzamy dostępność kontenerów...",
            "Generujemy spersonalizowaną ofertę...",
            "Weryfikujemy specyfikację techniczną...",
            "Przygotowujemy dokumentację...",
            "Finalizujemy kalkulację..."
        ]
        
        self.crane_animation = [
            "🏗️     ",
            " 🏗️    ",
            "  🏗️   ",
            "   🏗️  ",
            "    🏗️ ",
            "     🏗️",
            "    🏗️ ",
            "   🏗️  ",
            "  🏗️   ",
            " 🏗️    "
        ]
        
        self.container_build_frames = [
            "[ ]     Building foundation...",
            "[■]     Installing steel frame...",
            "[■■]    Adding walls...",
            "[■■■]   Installing systems...",
            "[■■■■]  Interior finishing...",
            "[■■■■■] Project complete! ✅"
        ]

    def container_progress_bar(self, progress: float, message: str = "") -> str:
        """Create container-themed progress bar"""
        filled_blocks = int(progress * 20)
        empty_blocks = 20 - filled_blocks
        
        progress_bar = "📦" + "■" * filled_blocks + "□" * empty_blocks + "🏗️"
        percentage = f"{int(progress * 100)}%"
        
        return f"""
        <div style="
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        ">
            <h3 style="margin: 0 0 15px 0; color: #ffd700;">🏗️ KAN-BUD Container Builder</h3>
            <div style="font-size: 18px; margin: 10px 0;">
                {progress_bar}
            </div>
            <div style="font-size: 24px; font-weight: bold; color: #ffd700; margin: 10px 0;">
                {percentage}
            </div>
            <div style="font-size: 16px; color: #e8f4f8; margin-top: 10px;">
                {message}
            </div>
        </div>
        """

    def spinning_container_css(self) -> str:
        """CSS for spinning container animation"""
        return """
        <style>
        @keyframes spin-container {
            0% { transform: rotate(0deg) scale(1); }
            25% { transform: rotate(90deg) scale(1.1); }
            50% { transform: rotate(180deg) scale(1); }
            75% { transform: rotate(270deg) scale(1.1); }
            100% { transform: rotate(360deg) scale(1); }
        }
        
        @keyframes crane-move {
            0% { transform: translateX(-50px); }
            50% { transform: translateX(50px); }
            100% { transform: translateX(-50px); }
        }
        
        @keyframes container-build {
            0% { width: 0%; background: #ff6b6b; }
            25% { width: 25%; background: #ffd93d; }
            50% { width: 50%; background: #6bcf7f; }
            75% { width: 75%; background: #4ecdc4; }
            100% { width: 100%; background: #45b7d1; }
        }
        
        .spinning-container {
            animation: spin-container 3s linear infinite;
            font-size: 48px;
            display: inline-block;
        }
        
        .crane-animation {
            animation: crane-move 4s ease-in-out infinite;
            font-size: 36px;
            display: inline-block;
        }
        
        .container-progress {
            width: 100%;
            height: 30px;
            background: #f0f0f0;
            border-radius: 15px;
            overflow: hidden;
            position: relative;
        }
        
        .container-fill {
            height: 100%;
            animation: container-build 5s ease-in-out;
            border-radius: 15px;
            position: relative;
        }
        
        .loading-text {
            color: #2c3e50;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            margin: 15px 0;
        }
        </style>
        """

    def show_spinning_container(self, message: str = "Ładowanie...") -> None:
        """Display spinning container animation"""
        css = self.spinning_container_css()
        
        html_content = f"""
        {css}
        <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 20px 0;">
            <div class="spinning-container">📦</div>
            <div class="crane-animation">🏗️</div>
            <div class="loading-text" style="color: white; font-size: 20px; margin-top: 20px;">
                {message}
            </div>
        </div>
        """
        
        st.markdown(html_content, unsafe_allow_html=True)

    def show_crane_loading(self, duration: float = 3.0) -> None:
        """Show animated crane loading sequence"""
        placeholder = st.empty()
        
        frames_per_second = 10
        total_frames = int(duration * frames_per_second)
        
        for i in range(total_frames):
            frame_index = i % len(self.crane_animation)
            crane_frame = self.crane_animation[frame_index]
            
            message_index = i % len(self.loading_messages)
            current_message = self.loading_messages[message_index]
            
            html_content = f"""
            <div style="
                text-align: center; 
                padding: 30px; 
                background: linear-gradient(135deg, #ff9a56 0%, #ff6b6b 100%);
                border-radius: 15px;
                color: white;
                margin: 20px 0;
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            ">
                <div style="font-size: 48px; margin-bottom: 20px;">
                    {crane_frame}
                </div>
                <div style="font-size: 18px; font-weight: bold;">
                    {current_message}
                </div>
            </div>
            """
            
            placeholder.markdown(html_content, unsafe_allow_html=True)
            time.sleep(1.0 / frames_per_second)

    def show_container_assembly(self, steps: Optional[List[str]] = None) -> None:
        """Show step-by-step container assembly animation"""
        if steps is None:
            steps = self.container_stages
            
        placeholder = st.empty()
        
        for i, step in enumerate(steps):
            progress = (i + 1) / len(steps)
            
            # Create visual representation of container being built
            filled_sections = "■" * (i + 1)
            empty_sections = "□" * (len(steps) - i - 1)
            container_visual = f"[{filled_sections}{empty_sections}]"
            
            html_content = f"""
            <div style="
                text-align: center;
                padding: 25px;
                background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
                border-radius: 15px;
                color: white;
                margin: 20px 0;
                box-shadow: 0 6px 20px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 32px; margin-bottom: 15px; font-family: 'Courier New', monospace;">
                    📦 {container_visual} 🏗️
                </div>
                <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px;">
                    Etap {i + 1} z {len(steps)}
                </div>
                <div style="font-size: 16px; margin-bottom: 15px;">
                    {step}
                </div>
                <div style="
                    width: 100%;
                    height: 8px;
                    background: rgba(255,255,255,0.3);
                    border-radius: 4px;
                    overflow: hidden;
                ">
                    <div style="
                        width: {progress * 100}%;
                        height: 100%;
                        background: #ffd700;
                        border-radius: 4px;
                        transition: width 0.5s ease;
                    "></div>
                </div>
                <div style="margin-top: 10px; font-size: 14px;">
                    {int(progress * 100)}% ukończone
                </div>
            </div>
            """
            
            placeholder.markdown(html_content, unsafe_allow_html=True)
            time.sleep(1.5)

    def show_interactive_progress(self, total_steps: int, current_step: int, message: str) -> None:
        """Show interactive progress with container theme"""
        progress = current_step / total_steps if total_steps > 0 else 0
        
        progress_html = self.container_progress_bar(progress, message)
        st.markdown(progress_html, unsafe_allow_html=True)

    def success_animation(self, message: str = "Projekt kontenerowy gotowy!") -> None:
        """Show success animation when loading completes"""
        success_html = f"""
        <div style="
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
            border-radius: 15px;
            color: white;
            margin: 20px 0;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            animation: pulse 2s ease-in-out;
        ">
            <div style="font-size: 64px; margin-bottom: 20px;">
                ✅ 📦 🎉
            </div>
            <div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">
                Sukces!
            </div>
            <div style="font-size: 18px;">
                {message}
            </div>
        </div>
        
        <style>
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        </style>
        """
        
        st.markdown(success_html, unsafe_allow_html=True)

def show_loading_with_container_theme(
    duration: float = 3.0,
    animation_type: str = "progress",
    message: str = "Przetwarzanie..."
) -> None:
    """
    Main function to show container-themed loading animation
    
    Args:
        duration: How long to show the animation
        animation_type: Type of animation ('progress', 'crane', 'assembly', 'spinner')
        message: Custom message to display
    """
    loader = ContainerLoadingSpinner()
    
    if animation_type == "progress":
        placeholder = st.empty()
        steps = 20
        for i in range(steps + 1):
            progress = i / steps
            progress_html = loader.container_progress_bar(progress, message)
            placeholder.markdown(progress_html, unsafe_allow_html=True)
            time.sleep(duration / steps)
            
    elif animation_type == "crane":
        loader.show_crane_loading(duration)
        
    elif animation_type == "assembly":
        loader.show_container_assembly()
        
    elif animation_type == "spinner":
        placeholder = st.empty()
        start_time = time.time()
        while time.time() - start_time < duration:
            placeholder.empty()
            loader.show_spinning_container(message)
            time.sleep(0.1)
    
    # Show success animation at the end
    loader.success_animation()