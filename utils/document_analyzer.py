"""
Document Analysis Module for KAN-BUD Container Calculator
Analyzes PDF drawings and DWG files from customers to extract pricing elements
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional
import base64
from utils.ai_services import OpenAIService, AnthropicService
import json
import re

class DocumentAnalyzer:
    """Analyzes customer drawings (PDF/DWG) to extract pricing elements"""
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.anthropic_service = AnthropicService()
    
    def analyze_pdf_drawing(self, uploaded_file, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze PDF technical drawing and extract elements for pricing
        """
        try:
            # Convert PDF to base64 for AI analysis
            file_bytes = uploaded_file.read()
            base64_file = base64.b64encode(file_bytes).decode()
            
            # Reset file pointer for potential future use
            uploaded_file.seek(0)
            
            analysis_prompt = self._build_drawing_analysis_prompt(project_context)
            
            # Try OpenAI first, fallback to Anthropic
            try:
                result = self._analyze_with_openai(base64_file, analysis_prompt)
                result['ai_model_used'] = 'OpenAI GPT-4o'
            except Exception as e:
                st.info("Używam Anthropic Claude do analizy rysunku...")
                result = self._analyze_with_anthropic(base64_file, analysis_prompt)
                result['ai_model_used'] = 'Anthropic Claude'
            
            return result
            
        except Exception as e:
            st.error(f"Błąd podczas analizy dokumentu: {str(e)}")
            return self._get_fallback_analysis()
    
    def analyze_dwg_metadata(self, uploaded_file) -> Dict[str, Any]:
        """
        Analyze DWG file metadata and extract available information
        Note: Full DWG parsing requires specialized libraries
        """
        try:
            file_info = {
                'filename': uploaded_file.name,
                'size_bytes': len(uploaded_file.read()),
                'file_type': 'DWG',
                'analysis_method': 'metadata_extraction'
            }
            
            # Reset file pointer
            uploaded_file.seek(0)
            
            # For now, we'll use AI to analyze the file context based on filename and user input
            # In production, you might want to use libraries like ezdxf for full DWG parsing
            
            return {
                'extracted_elements': [],
                'file_info': file_info,
                'recommendations': [
                    "Prześlij rysunek w formacie PDF dla pełnej analizy AI",
                    "Sprawdź czy plik zawiera warstwy z wymiarami",
                    "Upewnij się, że rysunek zawiera specyfikacje materiałów"
                ],
                'status': 'partial_analysis'
            }
            
        except Exception as e:
            st.error(f"Błąd podczas analizy pliku DWG: {str(e)}")
            return self._get_fallback_analysis()
    
    def _build_drawing_analysis_prompt(self, project_context: Dict[str, Any]) -> str:
        """Build comprehensive prompt for drawing analysis"""
        
        return f"""
        Analizujesz techniczny rysunek kontenera dla firmy KAN-BUD (Polska).
        
        KONTEKST PROJEKTU:
        - Typ kontenera: {project_context.get('container_type', 'Nie określono')}
        - Przeznaczenie: {project_context.get('use_case', 'Nie określono')}
        - Lokalizacja: {project_context.get('location', 'Polska')}
        
        ZADANIE:
        Przeanalizuj rysunek i wyekstraktuj wszystkie elementy wpływające na koszty:
        
        1. ELEMENTY STRUKTURALNE:
        - Liczba i rozmiar okien
        - Liczba i typ drzwi
        - Dodatkowe otwory (wentylacja, instalacje)
        - Wzmocnienia strukturalne
        - Zmiany w konstrukcji
        
        2. INSTALACJE:
        - System elektryczny (gniazdka, oświetlenie, rozdzielnica)
        - Instalacja hydrauliczna (rury, armatura, punkty wodne)
        - System HVAC (klimatyzacja, wentylacja, ogrzewanie)
        - Systemy specjalne (alarmy, monitoring)
        
        3. MATERIAŁY I WYKOŃCZENIA:
        - Typ izolacji i grubość
        - Materiały podłogowe
        - Materiały ścienne wewnętrzne
        - Wykończenia zewnętrzne
        
        4. WYMIARY I SPECYFIKACJE:
        - Dokładne wymiary elementów
        - Specyfikacje techniczne
        - Wymagania jakościowe
        
        ODPOWIEDŹ W FORMACIE JSON:
        {{
            "structural_elements": {{
                "windows": {{"count": 0, "types": [], "sizes": []}},
                "doors": {{"count": 0, "types": [], "sizes": []}},
                "openings": {{"count": 0, "purposes": [], "sizes": []}},
                "reinforcements": []
            }},
            "installations": {{
                "electrical": {{"complexity": "basic/standard/advanced", "elements": []}},
                "plumbing": {{"complexity": "basic/standard/advanced", "elements": []}},
                "hvac": {{"complexity": "basic/standard/advanced", "elements": []}}
            }},
            "materials": {{
                "insulation": {{"type": "", "thickness": ""}},
                "flooring": {{"type": "", "area": ""}},
                "wall_finish": {{"type": "", "area": ""}},
                "external_finish": {{"type": "", "area": ""}}
            }},
            "specifications": {{
                "dimensions": {{}},
                "quality_requirements": [],
                "special_requirements": []
            }},
            "cost_impact_summary": {{
                "estimated_complexity": "low/medium/high",
                "major_cost_drivers": [],
                "estimated_additional_cost_percentage": 0
            }},
            "recommendations": []
        }}
        
        Bądź precyzyjny i szczegółowy. Jeśli na rysunku brakuje informacji, zaznacz to w odpowiedzi.
        """
    
    def _analyze_with_openai(self, base64_file: str, prompt: str) -> Dict[str, Any]:
        """Analyze drawing using OpenAI GPT-4o with vision"""
        
        try:
            response = self.openai_service.client.chat.completions.create(
                model="gpt-4o",  # GPT-4o supports vision
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:application/pdf;base64,{base64_file}"}
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=2000
            )
            
            result = json.loads(response.choices[0].message.content)
            result['analysis_confidence'] = 'high'
            result['analysis_method'] = 'openai_vision'
            
            return result
            
        except Exception as e:
            raise Exception(f"OpenAI analysis failed: {str(e)}")
    
    def _analyze_with_anthropic(self, base64_file: str, prompt: str) -> Dict[str, Any]:
        """Analyze drawing using Anthropic Claude with vision"""
        
        try:
            response = self.anthropic_service.client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Claude 3.5 Sonnet supports vision
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "application/pdf",
                                    "data": base64_file
                                }
                            }
                        ]
                    }
                ]
            )
            
            # Parse JSON response from Claude
            response_text = response.content[0].text
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # Fallback parsing
                result = self._parse_text_response(response_text)
            
            result['analysis_confidence'] = 'high'
            result['analysis_method'] = 'anthropic_vision'
            
            return result
            
        except Exception as e:
            raise Exception(f"Anthropic analysis failed: {str(e)}")
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Parse text response when JSON parsing fails"""
        
        # Basic fallback structure
        return {
            "structural_elements": {
                "windows": {"count": 0, "types": [], "sizes": []},
                "doors": {"count": 0, "types": [], "sizes": []},
                "openings": {"count": 0, "purposes": [], "sizes": []},
                "reinforcements": []
            },
            "installations": {
                "electrical": {"complexity": "standard", "elements": []},
                "plumbing": {"complexity": "basic", "elements": []},
                "hvac": {"complexity": "basic", "elements": []}
            },
            "materials": {
                "insulation": {"type": "standard", "thickness": ""},
                "flooring": {"type": "standard", "area": ""},
                "wall_finish": {"type": "standard", "area": ""},
                "external_finish": {"type": "standard", "area": ""}
            },
            "specifications": {
                "dimensions": {},
                "quality_requirements": [],
                "special_requirements": []
            },
            "cost_impact_summary": {
                "estimated_complexity": "medium",
                "major_cost_drivers": ["Wymagana ręczna weryfikacja"],
                "estimated_additional_cost_percentage": 0
            },
            "recommendations": [
                "Rysunek wymaga ręcznej weryfikacji",
                "Skontaktuj się z zespołem technicznym KAN-BUD"
            ],
            "raw_analysis": text
        }
    
    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """Provide fallback analysis when AI fails"""
        
        return {
            "structural_elements": {
                "windows": {"count": 0, "types": [], "sizes": []},
                "doors": {"count": 0, "types": [], "sizes": []},
                "openings": {"count": 0, "purposes": [], "sizes": []},
                "reinforcements": []
            },
            "installations": {
                "electrical": {"complexity": "basic", "elements": []},
                "plumbing": {"complexity": "basic", "elements": []},
                "hvac": {"complexity": "basic", "elements": []}
            },
            "materials": {
                "insulation": {"type": "", "thickness": ""},
                "flooring": {"type": "", "area": ""},
                "wall_finish": {"type": "", "area": ""},
                "external_finish": {"type": "", "area": ""}
            },
            "specifications": {
                "dimensions": {},
                "quality_requirements": [],
                "special_requirements": []
            },
            "cost_impact_summary": {
                "estimated_complexity": "unknown",
                "major_cost_drivers": ["Analiza niedostępna"],
                "estimated_additional_cost_percentage": 0
            },
            "recommendations": [
                "Prześlij rysunek ponownie",
                "Skontaktuj się z działem technicznym",
                "Sprawdź format pliku"
            ],
            "analysis_confidence": "low",
            "analysis_method": "fallback",
            "status": "failed"
        }
    
    def calculate_cost_adjustments(self, analysis_result: Dict[str, Any], 
                                 base_estimate: float) -> Dict[str, Any]:
        """
        Calculate cost adjustments based on drawing analysis
        """
        try:
            cost_adjustments = {
                'structural_additions': 0,
                'installation_complexity': 0,
                'material_upgrades': 0,
                'special_requirements': 0
            }
            
            # Structural elements cost impact
            structural = analysis_result.get('structural_elements', {})
            
            # Windows and doors
            windows_count = structural.get('windows', {}).get('count', 0)
            doors_count = structural.get('doors', {}).get('count', 0)
            
            cost_adjustments['structural_additions'] += windows_count * 800  # €800 per window
            cost_adjustments['structural_additions'] += doors_count * 1200   # €1200 per door
            
            # Installation complexity
            installations = analysis_result.get('installations', {})
            
            electrical_complexity = installations.get('electrical', {}).get('complexity', 'basic')
            if electrical_complexity == 'advanced':
                cost_adjustments['installation_complexity'] += base_estimate * 0.15
            elif electrical_complexity == 'standard':
                cost_adjustments['installation_complexity'] += base_estimate * 0.08
            
            hvac_complexity = installations.get('hvac', {}).get('complexity', 'basic')
            if hvac_complexity == 'advanced':
                cost_adjustments['installation_complexity'] += base_estimate * 0.20
            elif hvac_complexity == 'standard':
                cost_adjustments['installation_complexity'] += base_estimate * 0.10
            
            # Total adjustment
            total_adjustment = sum(cost_adjustments.values())
            adjusted_estimate = base_estimate + total_adjustment
            
            return {
                'base_estimate': base_estimate,
                'cost_adjustments': cost_adjustments,
                'total_adjustment': total_adjustment,
                'adjusted_estimate': adjusted_estimate,
                'adjustment_percentage': (total_adjustment / base_estimate * 100) if base_estimate > 0 else 0
            }
            
        except Exception as e:
            st.error(f"Błąd podczas kalkulacji kosztów: {str(e)}")
            return {
                'base_estimate': base_estimate,
                'cost_adjustments': {},
                'total_adjustment': 0,
                'adjusted_estimate': base_estimate,
                'adjustment_percentage': 0,
                'error': str(e)
            }
    
    def generate_analysis_report(self, analysis_result: Dict[str, Any], 
                               cost_adjustments: Dict[str, Any]) -> str:
        """
        Generate detailed analysis report in Polish
        """
        
        report = f"""
        # 📋 RAPORT ANALIZY RYSUNKU TECHNICZNEGO
        
        ## Elementy Strukturalne
        - **Okna**: {analysis_result.get('structural_elements', {}).get('windows', {}).get('count', 0)} szt.
        - **Drzwi**: {analysis_result.get('structural_elements', {}).get('doors', {}).get('count', 0)} szt.
        - **Dodatkowe otwory**: {analysis_result.get('structural_elements', {}).get('openings', {}).get('count', 0)} szt.
        
        ## Instalacje
        - **Elektryczna**: {analysis_result.get('installations', {}).get('electrical', {}).get('complexity', 'podstawowa').title()}
        - **Hydrauliczna**: {analysis_result.get('installations', {}).get('plumbing', {}).get('complexity', 'podstawowa').title()}
        - **HVAC**: {analysis_result.get('installations', {}).get('hvac', {}).get('complexity', 'podstawowa').title()}
        
        ## Wpływ na Koszty
        - **Estymowana złożoność**: {analysis_result.get('cost_impact_summary', {}).get('estimated_complexity', 'średnia').title()}
        - **Korekta kosztów**: +{cost_adjustments.get('adjustment_percentage', 0):.1f}%
        - **Dodatkowe koszty**: €{cost_adjustments.get('total_adjustment', 0):,.2f}
        
        ## Zalecenia
        """
        
        recommendations = analysis_result.get('recommendations', [])
        for rec in recommendations:
            report += f"- {rec}\n"
        
        return report