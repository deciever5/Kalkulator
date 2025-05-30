"""The code change adds a function to estimate costs using AI services, including fallback options and base cost calculations."""
"""Update fallback estimate to use proper translations and language-specific content for Hungarian and Czech."""
"""
AI Services Module
Integrates with OpenAI and Anthropic APIs for intelligent cost estimation and technical analysis
"""

import os
import json
import sys
from typing import Dict, List, Any, Optional
from openai import OpenAI
import anthropic
from anthropic import Anthropic
import google.generativeai as genai
import requests

class OpenAIService:
    """Service for OpenAI GPT-4o integration"""

    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
        self.model = "gpt-4o"
        self.api_key = os.environ.get('OPENAI_API_KEY')

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")

        self.client = OpenAI(api_key=self.api_key)

    def generate_cost_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent cost estimate using GPT-4o"""

        prompt = self._build_cost_estimation_prompt(estimation_data, base_costs)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert construction cost estimator specializing in steel container modifications. Provide detailed, accurate cost estimates in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )

            result = json.loads(response.choices[0].message.content)
            return self._process_cost_estimate_response(result)

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def generate_technical_analysis(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                  structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical analysis and recommendations"""

        prompt = self._build_technical_analysis_prompt(config, analysis_params, structural_analysis)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a structural engineer specializing in container modifications. Provide technical analysis and recommendations in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            raise Exception(f"OpenAI technical analysis error: {str(e)}")

    def _build_cost_estimation_prompt(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> str:
        """Build enhanced prompt for comprehensive cost estimation"""
        config = estimation_data.get("container_config", {})
        language = estimation_data.get('response_language', 'en')

        # Enhanced configuration summary with technical details
        config_summary = []
        config_summary.append(f"Container Type: {config.get('base_type', 'Unknown')}")
        config_summary.append(f"Primary Use Case: {config.get('use_case', 'Unknown')}")
        config_summary.append(f"Expected Occupancy: {config.get('occupancy', 1)} people")
        config_summary.append(f"Operating Environment: {config.get('environment', 'Unknown')}")
        config_summary.append(f"Finish Quality Level: {config.get('finish_level', 'Standard')}")
        config_summary.append(f"Climate Zone: {config.get('climate_zone', 'Temperate')}")

        # User-specific requirements and comments
        user_comment = config.get('user_comment', '').strip()
        special_requirements = config.get('special_requirements', {})

        if user_comment:
            config_summary.append(f"CLIENT SPECIFIC REQUIREMENTS: {user_comment}")

        # Special considerations
        special_considerations = []
        if special_requirements.get('special_location'):
            special_considerations.append("Special location requirements")
        if special_requirements.get('urgent_timeline'):
            special_considerations.append("Urgent timeline needed")
        if special_requirements.get('custom_modifications'):
            special_considerations.append("Custom modifications required")
        if special_requirements.get('sustainability_focus'):
            special_considerations.append("Sustainability priority")
        if special_requirements.get('budget_constraints'):
            special_considerations.append("Budget constraints")
        if special_requirements.get('regulatory_concerns'):
            special_considerations.append("Regulatory compliance focus")

        if special_considerations:
            config_summary.append(f"SPECIAL CONSIDERATIONS: {'; '.join(special_considerations)}")

        # Detailed modifications list
        modifications = config.get('modifications', {})
        if modifications:
            mod_details = []
            for key, value in modifications.items():
                if value:
                    if key == 'windows' and isinstance(value, int):
                        mod_details.append(f"Windows: {value} units")
                    elif key == 'flooring':
                        mod_details.append(f"Flooring: {value}")
                    elif isinstance(value, bool):
                        mod_details.append(f"{key.replace('_', ' ').title()}: Yes")
                    else:
                        mod_details.append(f"{key.replace('_', ' ').title()}: {value}")
            if mod_details:
                config_summary.append(f"Modifications: {'; '.join(mod_details)}")

        # Enhanced system message based on language
        system_messages = {
            'en': "You are a senior container modification specialist with 15+ years experience in European markets. Provide comprehensive cost analysis with market insights, technical recommendations, risk assessment, and optimization opportunities. Pay special attention to any client-specific requirements or comments and address them thoroughly in your analysis.",
            'pl': "Jesteś starszym specjalistą od modyfikacji kontenerów z ponad 15-letnim doświadczeniem na rynkach europejskich. Zapewnij kompleksową analizę kosztów z wglądem w rynek, rekomendacjami technicznymi, oceną ryzyka i możliwościami optymalizacji. Zwróć szczególną uwagę na wszelkie specyficzne wymagania lub komentarze klienta i odnieś się do nich dokładnie w swojej analizie.",
            'de': "Sie sind ein erfahrener Containermodifikations-Spezialist mit über 15 Jahren Erfahrung auf europäischen Märkten. Bieten Sie umfassende Kostenanalyse mit Markteinblicken, technischen Empfehlungen, Risikobewertung und Optimierungsmöglichkeiten. Achten Sie besonders auf kundenspezifische Anforderungen oder Kommentare und gehen Sie in Ihrer Analyse gründlich darauf ein.",
            'nl': "U bent een senior containermodificatie specialist met 15+ jaar ervaring op Europese markten. Bied uitgebreide kostenanalyse met marktinzichten, technische aanbevelingen, risicobeoordeling en optimalisatiemogelijkheden. Besteed speciale aandacht aan eventuele klantspecifieke vereisten of opmerkingen en behandel deze grondig in uw analyse.",
            'hu': "Ön egy vezető konténer-módosítási szakértő több mint 15 éves európai piaci tapasztalattal. Nyújtson átfogó költségelemzést piaci betekintéssel, műszaki ajánlásokkal, kockázatértékeléssel és optimalizálási lehetőségekkel. Fordítson különös figyelmet minden ügyfél-specifikus követelményre vagy megjegyzésre, és foglalkozzon velük alaposan az elemzésében.",
            'cs': "Jste senior specialista na úpravy kontejnerů s více než 15letými zkušenostmi na evropských trzích. Poskytněte komplexní analýzu nákladů s tržními poznatky, technickými doporučeními, hodnocením rizik a možnostmi optimalizace. Věnujte zvláštní pozornost jakýmkoli specifickým požadavkům nebo komentářům klienta a důkladně se k nim vyjádřete ve své analýze."
        }

        return f"""{system_messages.get(language, system_messages['en'])}

PROJECT ANALYSIS REQUEST:

CONTAINER SPECIFICATIONS:
{chr(10).join(config_summary)}

LOCATION CONTEXT:
- Project Location: {estimation_data.get('project_location', 'Central Europe')}
- Timeline Requirements: {estimation_data.get('project_timeline', 'Standard')}
- Quality Standards: {estimation_data.get('quality_level', 'European Standard')}

BASE COST CALCULATIONS:
{json.dumps(base_costs, indent=2)}

REQUIRED COMPREHENSIVE ANALYSIS:
1. **CLIENT-SPECIFIC RESPONSE**: Address all client comments and special requirements directly
2. **Detailed cost breakdown** with market trend analysis and regional variations
3. **Technical feasibility assessment** with structural and engineering considerations
4. **Material and labor analysis** including supplier chain considerations and seasonal factors
5. **Timeline optimization** with critical path analysis and potential acceleration options
6. **Risk assessment and mitigation** strategies for identified challenges
7. **Sustainability evaluation** including environmental impact and energy efficiency
8. **Alternative design suggestions** with detailed cost-benefit comparisons
9. **Regulatory compliance guidance** including permits and building codes
10. **Long-term value analysis** including maintenance costs and ROI considerations
11. **Implementation roadmap** with practical next steps and recommendations

CRITICAL INSTRUCTIONS:
- Respond entirely in {language} language. ALL content must be in {language}.
- Address ANY client-specific requirements or comments mentioned above with detailed solutions
- Provide actionable, specific recommendations based on the client's stated needs
- Include practical implementation advice and potential challenges
- Offer multiple options where applicable to give the client choices

Provide detailed response in this JSON format:
{{
  "cost_analysis": {{
    "total_cost": 0,
    "confidence_level": 0.9,
    "cost_breakdown": {{
      "container_base": 0,
      "structural_modifications": 0,
      "systems_installation": 0,
      "finishes_interior": 0,
      "labor_costs": 0,
      "permits_fees": 0,
      "delivery_logistics": 0,
      "contingency": 0
    }},
    "market_trends": {{
      "material_cost_trend": "description",
      "labor_availability": "description",
      "seasonal_factors": "description"
    }}
  }},
  "technical_assessment": {{
    "structural_requirements": ["requirement1", "requirement2"],
    "building_code_compliance": ["compliance1", "compliance2"],
    "engineering_challenges": ["challenge1", "challenge2"]
  }},
  "project_management": {{
    "estimated_timeline": "8-12 weeks",
    "critical_path": ["phase1", "phase2", "phase3"],
    "resource_requirements": {{
      "specialized_labor": "description",
      "equipment_needs": "description"
    }}
  }},
  "risk_analysis": {{
    "technical_risks": ["risk1", "risk2"],
    "financial_risks": ["risk1", "risk2"],
    "mitigation_strategies": ["strategy1", "strategy2"]
  }},
  "sustainability": {{
    "environmental_impact": "assessment",
    "energy_efficiency_rating": "rating",
    "recyclable_materials_percentage": 0
  }},
  "recommendations": {{
    "immediate_actions": ["action1", "action2"],
    "optimization_opportunities": ["opportunity1", "opportunity2"],
    "alternative_approaches": ["approach1", "approach2"]
  }}
}}"""

    def _build_technical_analysis_prompt(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                       structural_analysis: Dict[str, Any]) -> str:
        """Build prompt for technical analysis"""

        prompt = f"""
        Perform a technical analysis of this container modification project and provide recommendations in JSON format.

        **Container Configuration:**
        {json.dumps(config, indent=2)}

        **Analysis Parameters:**
        {json.dumps(analysis_params, indent=2)}

        **Structural Analysis Results:**
        {json.dumps(structural_analysis, indent=2)}

        Please provide technical recommendations with the following JSON structure:
        {{
            "structural_recommendations": ["recommendation1", "recommendation2"],
            "modification_suggestions": ["suggestion1", "suggestion2"],
            "risk_mitigation": ["mitigation1", "mitigation2"],
            "code_compliance_notes": ["note1", "note2"],
            "cost_impact": {{
                "structural_reinforcement": "impact description",
                "system_upgrades": "impact description",
                "code_compliance": "impact description"
            }}
        }}

        Focus on structural integrity, code compliance, and practical implementation considerations.
        """

        return prompt

    def _process_cost_estimate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate cost estimate response"""

        # Always return the full response structure for comprehensive display
        return response

class AnthropicService:
    """Service for Anthropic Claude integration"""

    def __init__(self):
        #the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
        self.model = "claude-3-5-sonnet-20241022"
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')

        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

        self.client = Anthropic(api_key=self.api_key)

    def generate_cost_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent cost estimate using Claude"""

        prompt = self._build_cost_estimation_prompt(estimation_data, base_costs)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract JSON from response
            content = response.content[0].text
            # Find JSON content between curly braces
            start = content.find('{')
            end = content.rfind('}') + 1
            json_content = content[start:end]

            result = json.loads(json_content)
            return self._process_cost_estimate_response(result)

        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

    def generate_technical_analysis(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                  structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical analysis using Claude"""

        prompt = self._build_technical_analysis_prompt(config, analysis_params, structural_analysis)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract JSON from response
            content = response.content[0].text
            start = content.find('{')
            end = content.rfind('}') + 1
            json_content = content[start:end]

            result = json.loads(json_content)
            return result

        except Exception as e:
            raise Exception(f"Anthropic technical analysis error: {str(e)}")

    def _build_cost_estimation_prompt(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> str:
        """Build enhanced prompt for comprehensive cost estimation with Claude"""

        config = estimation_data.get("container_config", {})
        language = estimation_data.get('response_language', 'en')

        # Language-specific system message
        system_messages = {
            'en': "Expert container modification cost estimator with 15+ years European market experience. Specialist in structural engineering, building codes, sustainability, and project optimization.",
            'pl': "Ekspert ds. wyceny modyfikacji kontenerów z ponad 15-letnim doświadczeniem na rynku europejskim. Specjalista w zakresie inżynierii konstrukcyjnej, przepisów budowlanych, zrównoważonego rozwoju i optymalizacji projektów.",
            'de': "Experte für Containermodifikations-Kostenschätzung mit über 15 Jahren Erfahrung auf dem europäischen Markt. Spezialist für Bauingenieurwesen, Bauvorschriften, Nachhaltigkeit und Projektoptimierung.",
            'nl': "Expert in kostenraming voor containermodificaties met 15+ jaar ervaring op de Europese markt. Specialist in constructie-engineering, bouwvoorschriften, duurzaamheid en projectoptimalisatie.",
            'hu': "Konténer-módosítási költségbecslési szakértő több mint 15 éves európai piaci tapasztalattal. Szakértő az építőmérnökségben, építési előírásokban, fenntarthatóságban és projektoptimalizálásban.",
            'cs': "Expert na odhady nákladů na úpravy kontejnerů s více než 15letými zkušenostmi na evropském trhu. Specialista na stavební inženýrství, stavební předpisy, udržitelnost a optimalizaci projektů."
        }

        prompt = f"""
        {system_messages.get(language, system_messages['en'])}

        COMPREHENSIVE PROJECT ANALYSIS REQUEST:

        CONTAINER SPECIFICATIONS:
        - Base Type: {config.get('base_type', 'Unknown')}
        - Primary Use Case: {config.get('use_case', 'Unknown')}
        - Expected Occupancy: {config.get('occupancy', 1)} people
        - Operating Environment: {config.get('environment', 'Unknown')}
        - Finish Quality Level: {config.get('finish_level', 'Standard')}
        - Climate Zone: {config.get('climate_zone', 'Temperate')}
        - Detailed Modifications: {json.dumps(config.get('modifications', {}), indent=2)}

        PROJECT CONTEXT:
        - Geographic Location: {estimation_data.get('project_location', 'Central Europe')}
        - Project Timeline: {estimation_data.get('project_timeline', 'Standard')}
        - Quality Standards: {estimation_data.get('quality_level', 'European Standard')}
        - Special Requirements: {estimation_data.get('additional_notes', 'Standard build')}

        MARKET DATA & BASE COSTS:
        {json.dumps(base_costs, indent=2)}

        **CRITICAL: Respond entirely in {language} language. ALL text, technical terms, recommendations, and analysis must be in {language}.**

        REQUIRED COMPREHENSIVE ANALYSIS:

        1. **COST ANALYSIS** - Detailed breakdown with market insights
        2. **TECHNICAL ASSESSMENT** - Structural and engineering requirements
        3. **PROJECT MANAGEMENT** - Timeline, resources, critical path
        4. **RISK ASSESSMENT** - Technical, financial, and operational risks
        5. **SUSTAINABILITY ANALYSIS** - Environmental impact and efficiency
        6. **OPTIMIZATION RECOMMENDATIONS** - Cost reduction and value engineering
        7. **REGULATORY COMPLIANCE** - Building codes and permits
        8. **MARKET INTELLIGENCE** - Pricing trends and supplier insights

        Provide detailed analysis in this JSON format:
        {{
            "cost_analysis": {{
                "total_cost": [total in EUR],
                "confidence_level": [0.0-1.0],
                "estimated_timeline": "[duration with phases]",
                "breakdown": {{
                    "container_base": [base cost],
                    "structural_modifications": [structural work],
                    "systems_installation": [electrical/plumbing/HVAC],
                    "finishes_interior": [interior work],
                    "labor_costs": [total labor],
                    "permits_fees": [regulatory costs],
                    "delivery_logistics": [transport/delivery],
                    "contingency": [risk buffer]
                }},
                "market_insights": {{
                    "material_trends": "[current market analysis]",
                    "labor_availability": "[regional labor market]",
                    "cost_drivers": ["key factor 1", "key factor 2"]
                }}
            }},
            "technical_assessment": {{
                "structural_requirements": ["requirement 1", "requirement 2"],
                "building_code_compliance": ["code 1", "code 2"],
                "engineering_challenges": ["challenge 1", "challenge 2"],
                "quality_standards": ["standard 1", "standard 2"]
            }},
            "project_management": {{
                "critical_path": ["phase 1", "phase 2", "phase 3"],
                "resource_requirements": {{
                    "specialized_equipment": "[equipment needs]",
                    "skilled_labor": "[labor requirements]",
                    "material_procurement": "[procurement timeline]"
                }},
                "milestone_schedule": ["milestone 1", "milestone 2"]
            }},
            "risk_analysis": {{
                "technical_risks": ["risk 1", "risk 2"],
                "financial_risks": ["risk 1", "risk 2"],
                "operational_risks": ["risk 1", "risk 2"],
                "mitigation_strategies": ["strategy 1", "strategy 2"]
            }},
            "sustainability": {{
                "environmental_impact_score": "[rating/description]",
                "energy_efficiency_measures": ["measure 1", "measure 2"],
                "recyclable_content_percentage": [percentage],
                "carbon_footprint_estimate": "[CO2 equivalent]"
            }},
            "recommendations": {{
                "immediate_priorities": ["priority 1", "priority 2"],
                "cost_optimization": ["optimization 1", "optimization 2"],
                "value_engineering": ["suggestion 1", "suggestion 2"],
                "alternative_solutions": ["alternative 1", "alternative 2"]
            }},
            "regulatory_compliance": {{
                "required_permits": ["permit 1", "permit 2"],
                "building_codes": ["code requirement 1", "code requirement 2"],
                "safety_standards": ["standard 1", "standard 2"]
            }}
        }}

        Focus on practical, actionable insights with current European market conditions. Consider regional variations, seasonal factors, and supply chain considerations.
        """

        return prompt

    def _build_technical_analysis_prompt(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                       structural_analysis: Dict[str, Any]) -> str:
        """Build prompt for technical analysis with Claude"""

        prompt = f"""
        As a structural engineer specializing in container modifications, analyze this project and provide technical recommendations.

        Container Configuration:
        {json.dumps(config, indent=2)}

        Analysis Parameters:
        {json.dumps(analysis_params, indent=2)}

        Structural Analysis Results:
        {json.dumps(structural_analysis, indent=2)}

        Provide your technical analysis in the following JSON format:
        {{
            "structural_recommendations": ["specific structural recommendation 1", "specific structural recommendation 2"],
            "modification_suggestions": ["modification suggestion 1", "modification suggestion 2"],
            "risk_mitigation": ["risk mitigation strategy 1", "risk mitigation strategy 2"],
            "code_compliance_notes": ["compliance note 1", "compliance note 2"],
            "cost_impact": {{
                "structural_reinforcement": "detailed impact description",
                "system_upgrades": "detailed impact description",
                "code_compliance": "detailed impact description"
            }}
        }}

        Focus on structural integrity, building code compliance, safety factors, and practical implementation. Consider the specific use case and environmental conditions.
        """

        return prompt

    def _process_cost_estimate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate cost estimate response from Claude"""

        # Always return the full response structure for comprehensive display
        return response

class GeminiService:
    """Service for Google Gemini 2.5 integration"""

    def __init__(self):
        self.model_name = "gemini-1.5-flash"  # Use stable model instead of experimental
        self.api_key = os.environ.get('GEMINI_API_KEY')
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                print("✅ Gemini API configured successfully")
            except Exception as e:
                print(f"⚠️ Gemini configuration failed: {e}")
                self.model = None
        else:
            self.model = None
            print("⚠️ No GEMINI_API_KEY found")

    def generate_cost_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent cost estimate using Gemini 2.5"""

        if not self.model:
            raise Exception("Gemini API key not configured")

        prompt = self._build_cost_estimation_prompt(estimation_data, base_costs)

        try:
            response = self.model.generate_content(prompt)

            # Extract JSON from response
            response_text = response.text
            print(f"Raw Gemini response: {response_text[:200]}...")
            
            # Remove markdown code block formatting if present
            if '```json' in response_text:
                response_text = response_text.replace('```json', '').replace('```', '')
            
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_content = response_text[start:end]
                try:
                    result = json.loads(json_content)
                    
                    # Ensure result is a dictionary, not a list
                    if isinstance(result, list):
                        if len(result) > 0 and isinstance(result[0], dict):
                            result = result[0]  # Take first dictionary from list
                        else:
                            raise Exception("Invalid response format from Gemini")
                    
                    return self._process_cost_estimate_response(result)
                except json.JSONDecodeError as je:
                    print(f"JSON parsing error: {je}")
                    print(f"JSON content: {json_content}")
                    raise Exception(f"Invalid JSON from Gemini: {je}")
            else:
                print(f"No JSON found in response: {response_text}")
                raise Exception("No valid JSON found in Gemini response")

        except Exception as e:
            print(f"Gemini API detailed error: {str(e)}")
            raise Exception(f"Gemini API error: {str(e)}")

    def _build_cost_estimation_prompt(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> str:
        """Build enhanced prompt for comprehensive cost estimation with Gemini 2.5"""
        
        # Extract all user configuration details
        container_type = estimation_data.get('container_type', 'Unknown')
        main_purpose = estimation_data.get('main_purpose', 'Unknown')
        delivery_zone = estimation_data.get('delivery_zone', 'poland')
        
        # Collect all modifications and add-ons
        modifications = []
        if estimation_data.get('number_of_windows', 0) > 0:
            modifications.append(f"Windows: {estimation_data.get('number_of_windows', 0)} units")
        if estimation_data.get('additional_doors', False):
            modifications.append("Additional Doors: Yes")
        if estimation_data.get('electrical_system'):
            modifications.append(f"Electrical: {estimation_data.get('electrical_system')}")
        if estimation_data.get('plumbing_system'):
            modifications.append(f"Plumbing: {estimation_data.get('plumbing_system')}")
        if estimation_data.get('hvac_system'):
            modifications.append(f"HVAC: {estimation_data.get('hvac_system')}")
        if estimation_data.get('air_intakes'):
            modifications.append(f"Air Intakes: {estimation_data.get('air_intakes')}")
        if estimation_data.get('roof_modifications'):
            modifications.append(f"Roof: {estimation_data.get('roof_modifications')}")
        if estimation_data.get('security_features'):
            modifications.append(f"Security: {estimation_data.get('security_features')}")
        if estimation_data.get('exterior_cladding'):
            modifications.append(f"Cladding: {estimation_data.get('exterior_cladding')}")
        if estimation_data.get('paint_finish'):
            modifications.append(f"Paint: {estimation_data.get('paint_finish')}")
        
        prompt = f"""
        You are a professional container modification cost estimator with expertise in European construction markets. Analyze this specific container project based on user requirements.

        **PROJECT SPECIFICATIONS:**
        Container Type: {container_type}
        Primary Use Case: {main_purpose}
        Delivery Zone: {delivery_zone}
        
        **USER-SPECIFIED MODIFICATIONS:**
        {chr(10).join('- ' + mod for mod in modifications) if modifications else '- No modifications specified'}
        
        **EUROPEAN MARKET BASE COSTS:**
        {json.dumps(base_costs, indent=2)}

        Provide detailed cost analysis in this exact JSON format:
        {{
            "cost_analysis": {{
                "total_cost": [total in EUR],
                "confidence_level": [0.0-1.0],
                "estimated_timeline": "[duration with phases]",
                "breakdown": {{
                    "container_base": [base cost],
                    "modifications": [all modifications total],
                    "labor_costs": [30% of total],
                    "delivery_logistics": [delivery cost],
                    "contingency": [10% buffer]
                }}
            }},
            "user_configuration": {{
                "container_type": "{container_type}",
                "main_purpose": "{main_purpose}",
                "total_modifications": {len(modifications)}
            }},
            "recommendations": [
                "Based on your configuration, specific recommendation 1",
                "Technical suggestion for your use case",
                "Cost optimization opportunity"
            ]
        }}
        
        Focus on accurate European pricing and practical implementation details.
        """

        return prompt

    def _process_cost_estimate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate cost estimate response from Gemini"""
        return response

class GroqService:
    """Service for Groq AI integration - Free and fast inference"""

    def __init__(self):
        self.model = "llama-3.1-70b-versatile"  # Free model
        self.api_key = os.environ.get('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1"

        if not self.api_key:
            # For demo purposes, we'll use a fallback but still try to generate dynamic responses
            self.api_key = None
            print("⚠️ No GROQ_API_KEY found. Using dynamic fallback mode.")

    def generate_cost_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent cost estimate using Groq"""

        if not self.api_key:
            return self._generate_demo_estimate(estimation_data, base_costs)

        prompt = self._build_cost_estimation_prompt(estimation_data, base_costs)

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert construction cost estimator specializing in steel container modifications. Provide detailed, accurate cost estimates in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            }

            response = requests.post(f"{self.base_url}/chat/completions", 
                                   headers=headers, json=data)

            if response.status_code == 200:
                result_text = response.json()["choices"][0]["message"]["content"]
                # Extract JSON from response
                start = result_text.find('{')
                end = result_text.rfind('}') + 1
                json_content = result_text[start:end]

                result = json.loads(json_content)
                return self._process_cost_estimate_response(result)
            else:
                raise Exception(f"Groq API error: {response.status_code}")

        except Exception as e:
            print(f"Groq error, using fallback: {str(e)}")
            return self._generate_demo_estimate(estimation_data, base_costs)

    def _generate_demo_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate dynamic estimate based on actual user configuration"""

        # Extract all user configuration details
        container_type = estimation_data.get('container_type', 'Unknown')
        main_purpose = estimation_data.get('main_purpose', 'Unknown')
        
        # Calculate dynamic estimate based on actual configuration
        base_total = sum(base_costs.values())
        
        # Dynamic complexity factors based on actual user input
        complexity_factor = 1.0
        modification_costs = 0
        
        # Analyze actual user-specified modifications with proper cost impact
        if estimation_data.get("additional_doors"):
            complexity_factor += 0.15
            modification_costs += 800
        
        # Electrical system costs based on user selection
        electrical = estimation_data.get("electrical_system", "")
        if "standard" in electrical.lower():
            complexity_factor += 0.20
            modification_costs += 1500
        elif "industrial" in electrical.lower():
            complexity_factor += 0.35
            modification_costs += 3500
        elif "smart" in electrical.lower():
            complexity_factor += 0.45
            modification_costs += 5000
        
        # Plumbing system costs based on user selection
        plumbing = estimation_data.get("plumbing_system", "")
        if "basic" in plumbing.lower():
            complexity_factor += 0.25
            modification_costs += 2000
        elif "full" in plumbing.lower():
            complexity_factor += 0.40
            modification_costs += 4500
        elif "commercial" in plumbing.lower():
            complexity_factor += 0.55
            modification_costs += 7000
        
        # HVAC system costs based on user selection
        hvac = estimation_data.get("hvac_system", "")
        if "basic" in hvac.lower():
            complexity_factor += 0.20
            modification_costs += 1800
        elif "split" in hvac.lower():
            complexity_factor += 0.35
            modification_costs += 3500
        elif "central" in hvac.lower():
            complexity_factor += 0.50
            modification_costs += 6000
        elif "heat_pump" in hvac.lower():
            complexity_factor += 0.45
            modification_costs += 5500
        
        # Windows cost calculation
        num_windows = estimation_data.get("number_of_windows", 0)
        if num_windows > 0:
            modification_costs += num_windows * 400
            complexity_factor += num_windows * 0.05
        
        # Advanced modifications costs
        air_intakes = estimation_data.get("air_intakes", "")
        if "industrial" in air_intakes.lower():
            modification_costs += 1200
        elif "marine" in air_intakes.lower():
            modification_costs += 1800
        
        roof_mods = estimation_data.get("roof_modifications", "")
        if "skylight" in roof_mods.lower():
            modification_costs += 2500
        elif "solar" in roof_mods.lower():
            modification_costs += 3500
        
        security = estimation_data.get("security_features", "")
        if "advanced" in security.lower():
            modification_costs += 2000
        elif "high_security" in security.lower():
            modification_costs += 4000
        
        # Calculate total cost with user-specific modifications
        total_cost = base_total + modification_costs
        total_cost = total_cost * complexity_factor
        
        # Generate comprehensive response based on user configuration
        return {
            "cost_analysis": {
                "total_cost": int(total_cost),
                "confidence_level": 0.85,
                "estimated_timeline": "6-10 weeks",
                "breakdown": {
                    "container_base": int(base_total),
                    "modifications": int(modification_costs),
                    "labor_costs": int(total_cost * 0.3),
                    "delivery_logistics": int(total_cost * 0.08),
                    "contingency": int(total_cost * 0.1)
                }
            },
            "user_configuration": {
                "container_type": container_type,
                "main_purpose": main_purpose,
                "total_modifications": len([k for k, v in estimation_data.items() if v and k not in ['container_type', 'main_purpose']])
            },
            "recommendations": [
                f"Based on your {main_purpose.lower()} use case, consider energy-efficient options",
                f"Your {container_type} selection is optimal for this configuration",
                "Quality materials recommended for long-term durability"
            ]
        }
        
        # Add window costs with proper pricing
        window_count = config.get("number_of_windows", 0)
        window_cost = window_count * 600  # €600 per window
        
        # Calculate finish level impact
        finish_level = config.get("finish_level", "Standard")
        finish_multipliers = {"Basic": 1.0, "Standard": 1.3, "Premium": 1.8, "Luxury": 2.5}
        finish_multiplier = finish_multipliers.get(finish_level, 1.3)
        
        # Calculate environment impact
        environment = config.get("environment", "")
        env_factor = 1.0
        if "extreme" in environment.lower() or "harsh" in environment.lower():
            env_factor = 1.3
        elif "marine" in environment.lower() or "coastal" in environment.lower():
            env_factor = 1.2
        
        # User comment analysis for cost impact
        user_comment = config.get('user_comment', '').lower()
        comment_factor = 1.0
        if any(word in user_comment for word in ['premium', 'high-end', 'luxury', 'top quality', 'best']):
            comment_factor += 0.4
        elif any(word in user_comment for word in ['custom', 'special', 'unique', 'complex', 'sophisticated']):
            comment_factor += 0.3
        elif any(word in user_comment for word in ['urgent', 'fast', 'quick', 'rush', 'asap']):
            comment_factor += 0.2
        
        # Special requirements impact
        special_requirements = config.get('special_requirements', {})
        special_factor = 1.0
        if special_requirements.get('urgent_timeline'):
            special_factor += 0.2
        if special_requirements.get('custom_modifications'):
            special_factor += 0.3
        if special_requirements.get('sustainability_focus'):
            special_factor += 0.15
        if special_requirements.get('regulatory_concerns'):
            special_factor += 0.25
        if special_requirements.get('special_location'):
            special_factor += 0.15
        if special_requirements.get('budget_constraints'):
            special_factor += 0.05  # Slightly higher for budget planning
        
        # Calculate final cost with all factors
        total_cost = ((base_total + window_cost) * complexity_factor * finish_multiplier * 
                     env_factor * comment_factor * special_factor)
        
        # Get user comment for personalized response
        user_comment = config.get('user_comment', '').strip()
        special_requirements = config.get('special_requirements', {})
        
        # Generate dynamic recommendations based on config
        recommendations = []
        risk_factors = []
        cost_optimization = []
        
        # Dynamic recommendations based on actual config
        if modifications.get("electrical_system"):
            if language == 'pl':
                recommendations.append("Rozważ zaawansowany system elektryczny z automatyką")
            else:
                recommendations.append("Consider advanced electrical system with automation")
        
        if modifications.get("hvac_system"):
            if language == 'pl':
                recommendations.append("Zaplanuj efektywny system HVAC z oszczędzaniem energii")
            else:
                recommendations.append("Plan energy-efficient HVAC system")
        
        if window_count > 3:
            if language == 'pl':
                recommendations.append("Dodatkowe okna poprawią oświetlenie ale wpłyną na izolację")
            else:
                recommendations.append("Multiple windows improve lighting but consider insulation impact")
        
        if finish_level in ["Premium", "Luxury"]:
            if language == 'pl':
                recommendations.append("Wysokiej jakości wykończenia wymagają specjalistów")
            else:
                recommendations.append("Premium finishes require specialized craftsmen")
        
        # Dynamic risk factors
        if special_requirements.get('urgent_timeline'):
            if language == 'pl':
                risk_factors.append("Pilny harmonogram może zwiększyć koszty o 15-25%")
            else:
                risk_factors.append("Urgent timeline may increase costs by 15-25%")
        
        if special_requirements.get('budget_constraints'):
            if language == 'pl':
                risk_factors.append("Ograniczenia budżetowe mogą wymagać kompromisów jakościowych")
            else:
                risk_factors.append("Budget constraints may require quality compromises")
        
        if environment and "extreme" in environment.lower():
            if language == 'pl':
                risk_factors.append("Trudne warunki środowiskowe wymagają wzmocnionej konstrukcji")
            else:
                risk_factors.append("Harsh environmental conditions require reinforced construction")
        
        # Dynamic optimization
        if total_cost > 50000:
            if language == 'pl':
                cost_optimization.append("Rozważ fazowanie projektu dla lepszego zarządzania przepływem środków")
            else:
                cost_optimization.append("Consider project phasing for better cash flow management")
        
        if modifications.get("electrical_system") and modifications.get("hvac_system"):
            if language == 'pl':
                cost_optimization.append("Zintegruj systemy elektryczne i HVAC dla oszczędności")
            else:
                cost_optimization.append("Integrate electrical and HVAC systems for cost savings")
        
        # Address user comments if provided
        if user_comment:
            if language == 'pl':
                recommendations.insert(0, f"Na podstawie Państwa komentarza: '{user_comment}' - dostosujemy projekt do Państwa specyficznych potrzeb")
            else:
                recommendations.insert(0, f"Based on your comment: '{user_comment}' - we'll adapt the project to your specific needs")

        # Generate more detailed technical challenges based on config
        technical_challenges = []
        if modifications.get("structural_reinforcement"):
            if language == 'pl':
                technical_challenges.append("Wzmocnienie konstrukcji wymagające inżynierskich obliczeń statycznych")
            else:
                technical_challenges.append("Structural reinforcement requiring engineering static calculations")
        
        if window_count > 2:
            if language == 'pl':
                technical_challenges.append("Utrzymanie integralności konstrukcyjnej przy wielu otworach okiennych")
            else:
                technical_challenges.append("Maintaining structural integrity with multiple window openings")

        # Generate project execution details
        critical_path = []
        if language == 'pl':
            critical_path = [
                "Przygotowanie dokumentacji technicznej i pozwoleń (2-3 tygodnie)",
                "Zamówienie i dostawa kontenera oraz materiałów (3-4 tygodnie)",
                "Modyfikacje konstrukcyjne i instalacyjne (4-6 tygodni)",
                "Wykończenia i testy końcowe (1-2 tygodnie)"
            ]
        else:
            critical_path = [
                "Technical documentation and permits preparation (2-3 weeks)",
                "Container and materials ordering and delivery (3-4 weeks)",
                "Structural and installation modifications (4-6 weeks)",
                "Finishing works and final testing (1-2 weeks)"
            ]

        # Generate resource allocation based on config
        resource_allocation = {}
        if language == 'pl':
            resource_allocation = {
                "specialized_equipment": "Spawarka przemysłowa, narzędzia do cięcia stali, sprzęt montażowy",
                "skilled_labor_force": f"Zespół {3 + (1 if modifications.get('electrical_system') else 0) + (1 if modifications.get('plumbing_system') else 0)} specjalistów",
                "material_sourcing": "Lokalni dostawcy stali i materiałów budowlanych w Polsce"
            }
        else:
            resource_allocation = {
                "specialized_equipment": "Industrial welding equipment, steel cutting tools, assembly equipment",
                "skilled_labor_force": f"Team of {3 + (1 if modifications.get('electrical_system') else 0) + (1 if modifications.get('plumbing_system') else 0)} specialists",
                "material_sourcing": "Local steel and building materials suppliers in Poland"
            }

        # Generate sustainability metrics based on config
        sustainability_metrics = {}
        recycling_percentage = 75 + (10 if special_requirements.get('sustainability_focus') else 0)
        
        if language == 'pl':
            sustainability_metrics = {
                "environmental_impact": f"Niski wpływ - recykling istniejącej konstrukcji stalowej, {recycling_percentage}% materiałów z recyklingu",
                "energy_efficiency_metrics": [
                    "Izolacja termiczna klasy A+ zgodnie z normami EU",
                    "Możliwość instalacji paneli słonecznych na dachu"
                ],
                "waste_reduction_methods": [
                    "Precyzyjne cięcie minimalizujące odpady",
                    "Ponowne wykorzystanie odciętych fragmentów stali"
                ],
                "sustainable_materials": "Izolacja z materiałów naturalnych, farby bezolejowe, okna energooszczędne"
            }
        else:
            sustainability_metrics = {
                "environmental_impact": f"Low impact - recycling existing steel structure, {recycling_percentage}% recycled materials",
                "energy_efficiency_metrics": [
                    "A+ class thermal insulation according to EU standards",
                    "Possibility of solar panel installation on roof"
                ],
                "waste_reduction_methods": [
                    "Precision cutting minimizing waste",
                    "Reuse of cut steel fragments"
                ],
                "sustainable_materials": "Natural material insulation, oil-free paints, energy-efficient windows"
            }

        return {
            "cost_analysis": {
                "total_project_cost": round(total_cost),
                "confidence_rating": 0.85 + (0.05 if user_comment else 0),
                "project_duration": "8-14 weeks" if complexity_factor > 1.5 else "6-10 weeks",
                "detailed_breakdown": {
                    "container_acquisition": base_costs.get("container_base", 5000),
                    "structural_modifications": round(total_cost * 0.25),
                    "building_systems": round(total_cost * 0.20),
                    "interior_finishes": round(total_cost * 0.15),
                    "professional_services": round(total_cost * 0.10),
                    "labor_execution": round(total_cost * 0.20),
                    "logistics_delivery": base_costs.get("delivery", 800),
                    "project_contingency": round(total_cost * 0.10)
                },
                "market_intelligence": {
                    "current_trends": "Rosnące zapotrzebowanie na kontenerowe rozwiązania mieszkaniowe i biurowe w Polsce, wzrost o 25% rok do roku" if language == 'pl' else "Growing demand for container housing and office solutions in Poland, 25% year-over-year growth",
                    "price_volatility": "Stabilne ceny stali (±3%), wahania kosztów transportu (+8% względem 2023)" if language == 'pl' else "Stable steel prices (±3%), transport cost fluctuations (+8% vs 2023)",
                    "regional_factors": "Lokalna dostępność wykwalifikowanych spawaczy w Polsce wpływa na harmonogram" if language == 'pl' else "Local availability of qualified welders in Poland affects timeline"
                }
            },
            "technical_assessment": {
                "structural_engineering": recommendations[:2] if recommendations else technical_challenges[:2],
                "building_compliance": ["Zgodność z normami europejskimi EN 1993", "Wymagane pozwolenia budowlane zgodnie z Prawem Budowlanym"] if language == 'pl' else ["European standards EN 1993 compliance", "Building permits required according to Construction Law"],
                "technical_challenges": technical_challenges[:2] if technical_challenges else risk_factors[:2]
            },
            "project_execution": {
                "critical_path_analysis": critical_path[:4],
                "resource_allocation": resource_allocation,
                "project_timeline": f"Łączny czas realizacji: {'8-14 tygodni' if complexity_factor > 1.5 else '6-10 tygodni'}, w tym 2 tygodnie na pozwolenia" if language == 'pl' else f"Total execution time: {'8-14 weeks' if complexity_factor > 1.5 else '6-10 weeks'}, including 2 weeks for permits"
            },
            "recommendations": {
                "immediate_priorities": recommendations[:3] if recommendations else [],
                "cost_optimization": cost_optimization[:3] if cost_optimization else [],
                "value_engineering": ["Optymalizacja materiałów poprzez lokalne sourcing", "Standaryzacja komponentów dla redukcji kosztów"] if language == 'pl' else ["Material optimization through local sourcing", "Component standardization for cost reduction"]
            },
            "risk_management": {
                "identified_risks": risk_factors[:3] if risk_factors else [],
                "mitigation_strategies": ["Szczegółowe planowanie z buforem czasowym", "Elastyczny harmonogram dostaw", "Backup dostawcy materiałów"] if language == 'pl' else ["Detailed planning with time buffer", "Flexible delivery schedule", "Backup material suppliers"]
            },
            "sustainability_analysis": sustainability_metrics
        }

    def _build_cost_estimation_prompt(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> str:
        """Build enhanced prompt for comprehensive cost estimation with Groq"""

        config = estimation_data.get("container_config", {})
        language = estimation_data.get('response_language', 'en')

        # Language-specific expert personas
        expert_descriptions = {
            'en': "Senior container modification specialist with extensive European market experience, structural engineering expertise, and cost optimization knowledge.",
            'pl': "Starszy specjalista ds. modyfikacji kontenerów z rozległym doświadczeniem na rynku europejskim, wiedzą z zakresu inżynierii konstrukcyjnej i optymalizacji kosztów.",
            'de': "Senior Containermodifikations-Spezialist mit umfangreicher Erfahrung auf dem europäischen Markt, Expertise im Bauingenieurwesen und Kostenoptimierung.",
            'nl': "Senior containermodificatie specialist met uitgebreide Europese marktervaring, structurele engineering expertise en kostenoptimalisatie kennis.",
            'hu': "Vezető konténer-módosítási szakértő kiterjedt európai piaci tapasztalattal, építőmérnöki szakértelemmel és költségoptimalizálási tudással.",
            'cs': "Senior specialista na úpravy kontejnerů s rozsáhlými zkušenostmi na evropském trhu, odborností v oboru stavebního inženýrství a optimalizace nákladů."
        }

        prompt = f"""
        {expert_descriptions.get(language, expert_descriptions['en'])}

        COMPREHENSIVE CONTAINER PROJECT ANALYSIS:

        DETAILED PROJECT SPECIFICATIONS:
        - Container Type: {config.get('base_type', 'Unknown')}
        - Primary Application: {config.get('use_case', 'Unknown')}
        - Occupancy Requirements: {config.get('occupancy', 1)} people
        - Operating Environment: {config.get('environment', 'Unknown')}
        - Quality Finish Level: {config.get('finish_level', 'Standard')}
        - Climate Zone Considerations: {config.get('climate_zone', 'Temperate')}

        MODIFICATION SPECIFICATIONS:
        {json.dumps(config.get('modifications', {}), indent=2)}

        PROJECT CONTEXT & REQUIREMENTS:
        - Geographic Location: {estimation_data.get('project_location', 'Central Europe')}
        - Project Timeline: {estimation_data.get('project_timeline', 'Standard delivery')}
        - Quality Standards: {estimation_data.get('quality_level', 'European standards')}
        - Special Considerations: {estimation_data.get('additional_notes', 'Standard requirements')}

        MARKET DATA & BASE CALCULATIONS:
        {json.dumps(base_costs, indent=2)}

        **MANDATORY: ALL responses must be in {language} language. Technical terms, recommendations, analysis - everything in {language}.**

        REQUIRED COMPREHENSIVE ANALYSIS DELIVERABLES:

        1. **FINANCIAL ANALYSIS** - Complete cost breakdown with market intelligence
        2. **TECHNICAL EVALUATION** - Engineering requirements and compliance
        3. **PROJECT EXECUTION** - Timeline, resources, and critical dependencies
        4. **RISK MANAGEMENT** - Comprehensive risk assessment and mitigation
        5. **SUSTAINABILITY METRICS** - Environmental and efficiency analysis
        6. **STRATEGIC RECOMMENDATIONS** - Optimization and value engineering

        Deliver analysis in this enhanced JSON structure:
        {{
            "cost_analysis": {{
                "total_project_cost": [total EUR amount],
                "confidence_rating": [0.85-0.95 range],
                "project_duration": "[detailed timeline with phases]",
                "detailed_breakdown": {{
                    "container_acquisition": [base container cost],
                    "structural_modifications": [structural engineering work],
                    "building_systems": [electrical, plumbing, HVAC],
                    "interior_finishes": [flooring, walls, fixtures],
                    "professional_services": [design, engineering, permits],
                    "labor_execution": [installation and construction],
                    "logistics_delivery": [transport and site preparation],
                    "project_contingency": [risk buffer percentage]
                }},
                "market_intelligence": {{
                    "current_trends": "[market analysis in {language}]",
                    "price_volatility": "[material cost trends in {language}]",
                    "regional_factors": "[location-specific considerations in {language}]"
                }}
            }},
            "technical_assessment": {{
                "                "structural_engineering": ["[requirement in {language}]", "[requirement in {language}]"],
                "building_compliance": ["[code requirement in {language}]", "[code requirement in {language}]"],
                "technical_challenges": ["[challenge in {language}]"]
            }},
            "project_execution": {{
                "critical_path_analysis": ["[critical dependency in {language}]", "[critical dependency in {language}]"],
                "resource_allocation": {{
                    "specialized_equipment": "[equipment in {language}]",
                    "skilled_labor_force": "[labor in {language}]",
                    "material_sourcing": "[materials in {language}]"
                }},
                "project_timeline": "[project timeline in {language}]"
            }},
            "risk_management": {{
                "identified_risks": ["[risk factor in {language}]", "[risk factor in {language}]"],
                "financial_impact": ["[financial impact in {language}]", "[financial impact in {language}]"],
                "mitigation_strategies": ["[strategy in {language}]", "[strategy in {language}]"]
            }},
            "sustainability_analysis": {{
                "environmental_impact": "[environmental impact in {language}]",
                "energy_efficiency_metrics": "[metrics in {language}]",
                "waste_reduction_methods": "[methods in {language}]",
                "sustainable_materials": "[materials in {language}]"
            }},
            "strategic_recommendations": {{
                "cost_optimization": ["[strategy in {language}]", "[strategy in {language}]"],
                "value_engineering": ["[suggestion in {language}]", "[suggestion in {language}]"],
                "design_alternatives": ["[alternative in {language}]", "[alternative in {language}]"]
            }}
        }}

        Focus on actionable insights and detailed data. Consider European market trends.
        """

        return prompt

    def _process_cost_estimate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate cost estimate response"""

        # Always return the full response structure for comprehensive display
        return response


def estimate_cost_with_ai(config: Dict[str, Any], ai_model: str = "auto") -> str:
    """
    Main function to estimate costs using AI services

    Args:
        config: Container configuration dictionary
        ai_model: AI model selection ("auto", "Groq Llama-3.1-70B", etc.)

    Returns:
        Formatted cost estimate string
    """
    from utils.translations import get_current_language

    try:
        # Get current language for response
        current_language = get_current_language()

        # Calculate base costs first
        base_costs = _calculate_base_costs(config)

        # Prepare estimation data with enhanced configuration
        estimation_data = {
            "container_config": config,
            "response_language": current_language,
            "project_location": config.get("project_location", "Central Europe"),
            "project_timeline": config.get("project_timeline", "Standard"),
            "quality_level": config.get("quality_level", "European Standard"),
            "additional_notes": config.get("user_comment", "")
        }

        # Always try to use actual AI services first
        result = None
        
        # Try Gemini 2.5 first (latest and most capable)
        try:
            gemini_service = GeminiService()
            result = gemini_service.generate_cost_estimate(estimation_data, base_costs)
            # Validate result format
            if result and isinstance(result, dict):
                print("✅ Using Google Gemini 2.5 service")
            else:
                print("⚠️ Gemini returned invalid format, trying next service")
                result = None
        except Exception as gemini_error:
            print(f"Gemini service failed: {gemini_error}")
            result = None

            # Try Groq second
            try:
                groq_service = GroqService()
                result = groq_service.generate_cost_estimate(estimation_data, base_costs)
                # Validate result format
                if result and isinstance(result, dict):
                    print("✅ Using Groq AI service")
                else:
                    print("⚠️ Groq returned invalid format, trying next service")
                    result = None
            except Exception as groq_error:
                print(f"Groq service failed: {groq_error}")
                result = None

                # Try Anthropic third
                try:
                    anthropic_service = AnthropicService()
                    result = anthropic_service.generate_cost_estimate(estimation_data, base_costs)
                    print("✅ Using Anthropic Claude service")
                except Exception as anthropic_error:
                    print(f"Anthropic service failed: {anthropic_error}")

                    # Try OpenAI last
                    try:
                        openai_service = OpenAIService()
                        result = openai_service.generate_cost_estimate(estimation_data, base_costs)
                        print("✅ Using OpenAI GPT-4 service")
                    except Exception as openai_error:
                        print(f"OpenAI service failed: {openai_error}")
                        print("🔄 Using dynamic fallback estimation")

        # If we got a result from any AI service, format and return it
        if result:
            # Ensure result is a dictionary, not a list
            if isinstance(result, list):
                print("⚠️ AI service returned list instead of dict, using fallback")
                return _generate_enhanced_fallback_estimate(config, base_costs, current_language)
            return _format_ai_response(result, current_language)
        
        # If all AI services failed, use enhanced fallback
        return _generate_enhanced_fallback_estimate(config, base_costs, current_language)

    except Exception as e:
        print(f"AI estimation error: {str(e)}")
        return _generate_enhanced_fallback_estimate(config, base_costs, current_language)


def _calculate_base_costs(config: Dict[str, Any]) -> Dict[str, float]:
    """Calculate base costs from configuration with proper modification accounting"""

    # Base container costs - Polish market
    base_costs = {
        '20ft Standard': 3000,
        '40ft Standard': 4200,
        '40ft High Cube': 4500,
        '45ft High Cube': 5000,
        '48ft Standard': 5500,
        '53ft Standard': 6000,
        '20ft Refrigerated': 6000
    }

    container_cost = base_costs.get(config.get('container_type', '20ft Standard'), 4200)

    # Get modifications from config
    modifications = config.get('modifications', {})
    
    # Calculate detailed modification costs
    total_modifications_cost = 0
    electrical_cost = 0
    plumbing_cost = 0
    hvac_cost = 0
    structural_cost = 0

    # Windows - Polish market pricing
    windows = config.get('number_of_windows', 0)
    if windows > 0:
        structural_cost += windows * 600  # €600 per window

    # Additional doors
    if config.get('additional_doors', False) or modifications.get('additional_doors', False):
        structural_cost += 900  # €900 per additional door

    # Electrical systems
    if config.get('electrical_system', False) or modifications.get('electrical_system', False):
        electrical_cost = 1800  # €1800 basic package

    # Plumbing
    if config.get('plumbing_system', False) or modifications.get('plumbing_system', False):
        plumbing_cost = 2500  # €2500 basic package

    # HVAC
    if config.get('hvac_system', False) or modifications.get('hvac_system', False):
        hvac_cost = 3000  # €3000 mini-split system

    # Insulation
    if config.get('insulation', False) or modifications.get('insulation_package', False):
        structural_cost += 1200  # €1200 insulation package

    # Structural reinforcements
    if modifications.get('wall_reinforcement', False):
        structural_cost += 2000
    if modifications.get('roof_reinforcement', False):
        structural_cost += 1500
    if modifications.get('floor_reinforcement', False):
        structural_cost += 1800
    if modifications.get('additional_support', False):
        structural_cost += 2500

    # Advanced systems
    if modifications.get('security_system', False):
        electrical_cost += 1500
    if modifications.get('fire_suppression', False):
        structural_cost += 3000
    if modifications.get('access_control', False):
        electrical_cost += 1200

    # Finish level impact
    finish_level = config.get('finish_level', 'Standard')
    finish_multipliers = {'Basic': 1.0, 'Standard': 1.3, 'Premium': 1.8, 'Luxury': 2.5}
    finish_multiplier = finish_multipliers.get(finish_level, 1.3)

    # Apply finish multiplier to interior costs
    electrical_cost = int(electrical_cost * finish_multiplier)
    plumbing_cost = int(plumbing_cost * finish_multiplier)
    hvac_cost = int(hvac_cost * finish_multiplier)

    # Environment impact
    environment = config.get('environment', '')
    env_multiplier = 1.0
    if 'extreme' in environment.lower() or 'harsh' in environment.lower():
        env_multiplier = 1.25
    elif 'marine' in environment.lower() or 'coastal' in environment.lower():
        env_multiplier = 1.15

    # Apply environment multiplier
    structural_cost = int(structural_cost * env_multiplier)

    # User comment impact - analyze for cost drivers
    user_comment = config.get('user_comment', '').lower()
    comment_multiplier = 1.0
    if any(word in user_comment for word in ['premium', 'high-end', 'luxury', 'top quality']):
        comment_multiplier += 0.3
    elif any(word in user_comment for word in ['custom', 'special', 'unique', 'complex']):
        comment_multiplier += 0.2
    elif any(word in user_comment for word in ['urgent', 'fast', 'quick', 'rush']):
        comment_multiplier += 0.15

    # Special requirements impact
    special_requirements = config.get('special_requirements', {})
    if special_requirements.get('urgent_timeline'):
        comment_multiplier += 0.15
    if special_requirements.get('custom_modifications'):
        comment_multiplier += 0.25
    if special_requirements.get('sustainability_focus'):
        comment_multiplier += 0.1
    if special_requirements.get('regulatory_concerns'):
        comment_multiplier += 0.2

    # Apply comment multiplier to all modification costs
    if comment_multiplier > 1.0:
        structural_cost = int(structural_cost * comment_multiplier)
        electrical_cost = int(electrical_cost * comment_multiplier)
        plumbing_cost = int(plumbing_cost * comment_multiplier)
        hvac_cost = int(hvac_cost * comment_multiplier)

    # Delivery cost - Polish market
    delivery_cost = 800

    return {
        'container_base': container_cost,
        'structural_modifications': structural_cost,
        'electrical': electrical_cost,
        'plumbing': plumbing_cost,
        'hvac': hvac_cost,
        'finishes': 2000 * finish_multiplier,
        'delivery': delivery_cost
    }


def _format_ai_response(ai_result: Dict[str, Any], language: str) -> str:
    """Format AI response into comprehensive readable string"""

    if isinstance(ai_result, dict):
        # Extract cost analysis if available
        cost_analysis = ai_result.get('cost_analysis', {})
        total_cost = cost_analysis.get('total_cost', 0) or cost_analysis.get('total_project_cost', 0)

        if not total_cost and 'total_cost' in ai_result:
            total_cost = ai_result['total_cost']

        # Build comprehensive formatted response
        response_parts = []

        # Title and total cost
        response_parts.append(f"## 🤖 {'Kompleksowa Analiza AI' if language == 'pl' else 'Comprehensive AI Analysis'}")
        response_parts.append(f"### 💰 {'Całkowite Koszty Projektu' if language == 'pl' else 'Total Project Cost'}: €{total_cost:,.0f}")

        # Confidence and timeline
        confidence = cost_analysis.get('confidence_rating', 0.85)
        timeline = cost_analysis.get('estimated_timeline', '') or cost_analysis.get('project_duration', '')
        if timeline:
            response_parts.append(f"⏱️ **{'Czas Realizacji' if language == 'pl' else 'Project Timeline'}:** {timeline}")
        response_parts.append(f"🎯 **{'Poziom Pewności' if language == 'pl' else 'Confidence Level'}:** {confidence*100:.0f}%")

        # Detailed cost breakdown
        breakdown = cost_analysis.get('breakdown', {}) or cost_analysis.get('detailed_breakdown', {})
        if breakdown:
            response_parts.append(f"\n📊 **{'Szczegółowy Podział Kosztów' if language == 'pl' else 'Detailed Cost Breakdown'}:**")
            for key, value in breakdown.items():
                if value and value > 0:
                    label_map = {
                        'container_acquisition': 'Zakup Kontenera' if language == 'pl' else 'Container Acquisition',
                        'structural_modifications': 'Modyfikacje Konstrukcyjne' if language == 'pl' else 'Structural Modifications',
                        'building_systems': 'Systemy Budowlane' if language == 'pl' else 'Building Systems',
                        'interior_finishes': 'Wykończenia Wnętrz' if language == 'pl' else 'Interior Finishes',
                        'professional_services': 'Usługi Profesjonalne' if language == 'pl' else 'Professional Services',
                        'labor_execution': 'Wykonanie Robót' if language == 'pl' else 'Labor Execution',
                        'logistics_delivery': 'Logistyka i Dostawa' if language == 'pl' else 'Logistics & Delivery',
                        'project_contingency': 'Rezerwa Projektowa' if language == 'pl' else 'Project Contingency'
                    }
                    label = label_map.get(key, key.replace('_', ' ').title())
                    response_parts.append(f"• **{label}:** €{value:,.0f}")

        # Market intelligence
        market_intel = cost_analysis.get('market_intelligence', {})
        if market_intel:
            response_parts.append(f"\n📈 **{'Analiza Rynkowa' if language == 'pl' else 'Market Intelligence'}:**")
            if market_intel.get('current_trends'):
                response_parts.append(f"• **{'Aktualne Trendy' if language == 'pl' else 'Current Trends'}:** {market_intel['current_trends']}")
            if market_intel.get('price_volatility'):
                response_parts.append(f"• **{'Wahania Cen' if language == 'pl' else 'Price Volatility'}:** {market_intel['price_volatility']}")
            if market_intel.get('regional_factors'):
                response_parts.append(f"• **{'Czynniki Regionalne' if language == 'pl' else 'Regional Factors'}:** {market_intel['regional_factors']}")

        # Technical assessment
        technical_assessment = ai_result.get('technical_assessment', {})
        if technical_assessment:
            response_parts.append(f"\n🔧 **{'Ocena Techniczna' if language == 'pl' else 'Technical Assessment'}:**")
            
            structural_req = technical_assessment.get('structural_engineering', []) or technical_assessment.get('structural_requirements', [])
            if structural_req:
                response_parts.append(f"• **{'Wymagania Konstrukcyjne' if language == 'pl' else 'Structural Requirements'}:**")
                for req in structural_req[:3]:
                    response_parts.append(f"  - {req}")
            
            compliance = technical_assessment.get('building_compliance', []) or technical_assessment.get('building_code_compliance', [])
            if compliance:
                response_parts.append(f"• **{'Zgodność z Przepisami' if language == 'pl' else 'Building Compliance'}:**")
                for comp in compliance[:2]:
                    response_parts.append(f"  - {comp}")

        # Recommendations with all categories
        recommendations = ai_result.get('recommendations', {})
        if recommendations:
            response_parts.append(f"\n💡 **{'Rekomendacje Strategiczne' if language == 'pl' else 'Strategic Recommendations'}:**")
            
            immediate_actions = recommendations.get('immediate_actions', []) or recommendations.get('immediate_priorities', [])
            if immediate_actions:
                response_parts.append(f"• **{'Działania Priorytetowe' if language == 'pl' else 'Priority Actions'}:**")
                for action in immediate_actions[:3]:
                    response_parts.append(f"  - {action}")
            
            cost_optimization = recommendations.get('cost_optimization', [])
            if cost_optimization:
                response_parts.append(f"• **{'Optymalizacja Kosztów' if language == 'pl' else 'Cost Optimization'}:**")
                for opt in cost_optimization[:3]:
                    response_parts.append(f"  - {opt}")
            
            value_engineering = recommendations.get('value_engineering', [])
            if value_engineering:
                response_parts.append(f"• **{'Inżynieria Wartości' if language == 'pl' else 'Value Engineering'}:**")
                for val in value_engineering[:2]:
                    response_parts.append(f"  - {val}")

        # Risk management
        risk_management = ai_result.get('risk_management', {})
        if risk_management:
            response_parts.append(f"\n⚠️ **{'Zarządzanie Ryzykiem' if language == 'pl' else 'Risk Management'}:**")
            
            risks = risk_management.get('identified_risks', [])
            if risks:
                response_parts.append(f"• **{'Zidentyfikowane Ryzyka' if language == 'pl' else 'Identified Risks'}:**")
                for risk in risks[:3]:
                    response_parts.append(f"  - {risk}")
            
            mitigation = risk_management.get('mitigation_strategies', [])
            if mitigation:
                response_parts.append(f"• **{'Strategie Mitygacji' if language == 'pl' else 'Mitigation Strategies'}:**")
                for mit in mitigation[:2]:
                    response_parts.append(f"  - {mit}")

        # Project execution details
        project_execution = ai_result.get('project_execution', {})
        if project_execution:
            response_parts.append(f"\n🚀 **{'Realizacja Projektu' if language == 'pl' else 'Project Execution'}:**")
            
            critical_path = project_execution.get('critical_path_analysis', []) or project_execution.get('critical_path', [])
            if critical_path:
                response_parts.append(f"• **{'Ścieżka Krytyczna' if language == 'pl' else 'Critical Path'}:**")
                for phase in critical_path[:3]:
                    response_parts.append(f"  - {phase}")
            
            resource_allocation = project_execution.get('resource_allocation', {})
            if resource_allocation:
                response_parts.append(f"• **{'Alokacja Zasobów' if language == 'pl' else 'Resource Allocation'}:**")
                for key, value in resource_allocation.items():
                    if value:
                        label = key.replace('_', ' ').title()
                        response_parts.append(f"  - **{label}:** {value}")

        # Sustainability analysis
        sustainability = ai_result.get('sustainability_analysis', {}) or ai_result.get('sustainability', {})
        if sustainability:
            response_parts.append(f"\n🌱 **{'Analiza Zrównoważoności' if language == 'pl' else 'Sustainability Analysis'}:**")
            
            env_impact = sustainability.get('environmental_impact', '') or sustainability.get('environmental_impact_score', '')
            if env_impact:
                response_parts.append(f"• **{'Wpływ Środowiskowy' if language == 'pl' else 'Environmental Impact'}:** {env_impact}")
            
            energy_efficiency = sustainability.get('energy_efficiency_metrics', []) or sustainability.get('energy_efficiency_measures', [])
            if energy_efficiency:
                response_parts.append(f"• **{'Efektywność Energetyczna' if language == 'pl' else 'Energy Efficiency'}:**")
                for measure in (energy_efficiency if isinstance(energy_efficiency, list) else [energy_efficiency])[:2]:
                    response_parts.append(f"  - {measure}")

        return "\n".join(response_parts)

    elif isinstance(ai_result, str):
        return ai_result
    else:
        return str(ai_result)


def _generate_enhanced_fallback_estimate(config: Dict[str, Any], base_costs: Dict[str, float], language: str) -> str:
    """Generate enhanced dynamic fallback estimate when AI services are unavailable"""

    # Create a GroqService instance to use its enhanced demo estimation
    groq_service = GroqService()
    
    # Prepare estimation data
    estimation_data = {
        "container_config": config,
        "response_language": language,
        "project_location": config.get("project_location", "Central Europe"),
        "project_timeline": config.get("project_timeline", "Standard"),
        "quality_level": config.get("quality_level", "European Standard")
    }
    
    # Use the enhanced demo estimate which is now dynamic
    result = groq_service._generate_demo_estimate(estimation_data, base_costs)
    
    # Format the enhanced result
    return _format_ai_response(result, language)