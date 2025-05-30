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

class GroqService:
    """Service for Groq AI integration - Free and fast inference"""

    def __init__(self):
        self.model = "llama-3.1-70b-versatile"  # Free model
        self.api_key = os.environ.get('GROQ_API_KEY')
        self.base_url = "https://api.groq.com/openai/v1"

        if not self.api_key:
            # For demo purposes, we'll use a fallback
            self.api_key = "demo_mode"
            print("⚠️ No GROQ_API_KEY found. Using demo mode.")

    def generate_cost_estimate(self, estimation_data: Dict[str, Any], base_costs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent cost estimate using Groq"""

        if self.api_key == "demo_mode":
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
        """Generate demo estimate when API is not available"""

        config = estimation_data.get("container_config", {})

        # Calculate basic estimate
        base_total = sum(base_costs.values())

        # Add complexity factors
        complexity_factor = 1.2
        if config.get("modifications", {}).get("reinforcement_walls"):
            complexity_factor += 0.1
        if config.get("modifications", {}).get("electrical"):
            complexity_factor += 0.15
        if config.get("modifications", {}).get("plumbing"):
            complexity_factor += 0.2

        total_cost = base_total * complexity_factor

        return {
            "total_cost": round(total_cost),
            "confidence": 0.85,
            "estimated_timeline": "8-12 weeks",
            "breakdown": {
                "container_base": base_costs.get("container_base", 5000),
                "structural_modifications": base_costs.get("structural_modifications", 0),
                "systems_installation": (base_costs.get("electrical", 0) + 
                                       base_costs.get("plumbing", 0) + 
                                       base_costs.get("hvac", 0)),
                "finishes_interior": base_costs.get("finishes", 1500),
                "labor_costs": total_cost * 0.4,
                "permits_fees": 1200,
                "delivery_logistics": 800,
                "contingency": total_cost * 0.1
            },
            "analysis": {
                "recommendations": [
                    "Consider standard electrical package for cost efficiency",
                    "Plan delivery route for oversized transport requirements",
                    "Schedule structural inspections early in process"
                ],
                "risk_factors": [
                    "Weather delays during construction phase",
                    "Permit approval timeline variations",
                    "Site access limitations for delivery"
                ],
                "cost_optimization": [
                    "Bundle multiple modifications for labor efficiency",
                    "Source materials locally to reduce shipping costs",
                    "Consider phased construction approach"
                ]
            }
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