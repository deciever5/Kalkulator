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

        # Return the full response structure for comprehensive display
        if isinstance(response, dict) and len(response) > 5:
            # This appears to be a comprehensive response, return as-is
            return response

        # Fallback processing for simple responses
        processed = {
            "cost_analysis": {
                "total_cost": response.get("total_cost", response.get("total_project_cost", 0)),
                "confidence": min(1.0, max(0.0, response.get("confidence", response.get("confidence_level", 0.8)))),
                "estimated_timeline": response.get("estimated_timeline", response.get("project_duration", "8-12 weeks")),
                "breakdown": response.get("breakdown", response.get("detailed_breakdown", {})),
                "market_insights": response.get("market_insights", response.get("market_intelligence", {}))
            },
            "technical_assessment": response.get("technical_assessment", {}),
            "project_management": response.get("project_management", response.get("project_execution", {})),
            "risk_analysis": response.get("risk_analysis", response.get("risk_assessment", {})),
            "recommendations": response.get("recommendations", response.get("strategic_recommendations", {})),
            "sustainability": response.get("sustainability", response.get("sustainability_analysis", {})),
            "regulatory_compliance": response.get("regulatory_compliance", {})
        }

        return processed

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

        # Ensure required fields exist
        processed = {
            "total_cost": response.get("total_cost", 0),
            "confidence": min(1.0, max(0.0, response.get("confidence", 0.8))),
            "estimated_timeline": response.get("estimated_timeline", "8-12 weeks"),
            "breakdown": response.get("breakdown", {}),
            "analysis": response.get("analysis", {})
        }

        # Validate breakdown adds up to total
        breakdown_total = sum(processed["breakdown"].values())
        if abs(breakdown_total - processed["total_cost"]) > 100:  # Allow small rounding differences
            # Adjust total to match breakdown
            processed["total_cost"] = breakdown_total

        return processed

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
                "structural_engineering": ["[requirement in {language}]", "[requirement in {language}]"],
                "building_compliance": ["[code requirement in {language}]", "[code requirement in {language}]"],
                "technical_challenges": ["[challenge in {language}]", "[challenge in {language}]"],
                "quality_specifications": ["[specification in {language}]", "[specification in {language}]"]
            }},
            "project_execution": {{
                "critical_path_analysis": ["[phase in {language}]", "[phase in {language}]", "[phase in {language}]"],
                "resource_planning": {{
                    "specialized_equipment": "[equipment needs in {language}]",
                    "skilled_trades": "[labor requirements in {language}]",
                    "material_sourcing": "[procurement strategy in {language}]"
                }},
                "delivery_milestones": ["[milestone in {language}]", "[milestone in {language}]"]
            }},
            "risk_assessment": {{
                "technical_risks": ["[risk in {language}]", "[risk in {language}]"],
                "financial_risks": ["[risk in {language}]", "[risk in {language}]"],
                "schedule_risks": ["[risk in {language}]", "[risk in {language}]"],
                "mitigation_strategies": ["[strategy in {language}]", "[strategy in {language}]"]
            }},
            "sustainability_analysis": {{
                "environmental_impact": "[impact assessment in {language}]",
                "energy_performance": "[efficiency rating in {language}]",
                "material_sustainability": [recyclable percentage],
                "lifecycle_considerations": "[long-term analysis in {language}]"
            }},
            "strategic_recommendations": {{
                "priority_actions": ["[action in {language}]", "[action in {language}]"],
                "cost_optimization": ["[optimization in {language}]", "[optimization in {language}]"],
                "value_additions": ["[value proposition in {language}]", "[value proposition in {language}]"],
                "alternative_approaches": ["[alternative in {language}]", "[alternative in {language}]"]
            }}
        }}

        Base analysis on current European construction market conditions, regulatory requirements, and industry best practices. Provide actionable, specific recommendations with practical implementation guidance.
        """

        return prompt

    def _process_cost_estimate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate cost estimate response"""

        # Return the full response structure for comprehensive display
        if isinstance(response, dict) and len(response) > 5:
            # This appears to be a comprehensive response, return as-is
            return response

        # Fallback processing for simple responses
        processed = {
            "cost_analysis": {
                "total_cost": response.get("total_cost", response.get("total_project_cost", 0)),
                "confidence": min(1.0, max(0.0, response.get("confidence", response.get("confidence_level", 0.8)))),
                "estimated_timeline": response.get("estimated_timeline", response.get("project_duration", "8-12 weeks")),
                "breakdown": response.get("breakdown", response.get("detailed_breakdown", {})),
                "market_insights": response.get("market_insights", response.get("market_intelligence", {}))
            },
            "technical_assessment": response.get("technical_assessment", {}),
            "project_management": response.get("project_management", response.get("project_execution", {})),
            "risk_analysis": response.get("risk_analysis", response.get("risk_assessment", {})),
            "recommendations": response.get("recommendations", response.get("strategic_recommendations", {})),
            "sustainability": response.get("sustainability", response.get("sustainability_analysis", {})),
            "regulatory_compliance": response.get("regulatory_compliance", {})
        }

        return processed

    def generate_technical_analysis(self, config: Dict[str, Any], analysis_params: Dict[str, Any], 
                                  structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate technical analysis using Groq"""

        if self.api_key == "demo_mode":
            return self._generate_demo_technical_analysis(config, analysis_params, structural_analysis)

        prompt = self._build_technical_analysis_prompt(config, analysis_params, structural_analysis)

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
                        "content": "You are a structural engineer specializing in container modifications. Provide technical analysis and recommendations in JSON format."
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
                start = result_text.find('{')
                end = result_text.rfind('}') + 1
                json_content = result_text[start:end]

                result = json.loads(json_content)
                return result
            else:
                raise Exception(f"Groq API error: {response.status_code}")

        except Exception as e:
            print(f"Groq technical analysis error, using fallback: {str(e)}")
            return self._generate_demo_technical_analysis(config, analysis_params, structural_analysis)

    def _generate_demo_technical_analysis(self, config: Dict[str, Any], 
                                        analysis_params: Dict[str, Any], 
                                        structural_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate demo technical analysis"""

        return {
            "structural_recommendations": [
                "Add corner reinforcement for improved load distribution",
                "Consider additional floor support for heavy loads",
                "Implement proper drainage system for roof modifications"
            ],
            "modification_suggestions": [
                "Use structural-grade steel for all reinforcements",
                "Plan electrical routing to avoid structural members",
                "Consider modular approach for future modifications"
            ],
            "risk_mitigation": [
                "Conduct soil bearing capacity analysis",
                "Plan for thermal expansion in structural connections",
                "Implement proper ventilation to prevent condensation"
            ],
            "code_compliance_notes": [
                "Ensure compliance with local building codes",
                "Verify fire safety requirements for intended use",
                "Plan for ADA accessibility if required"
            ],
            "cost_impact": {
                "structural_reinforcement": "Additional $2,000-4,000 for enhanced structural integrity",
                "system_upgrades": "Professional installation recommended for safety compliance",
                "code_compliance": "Permit costs and inspections may add $1,000-2,500"
            }
        }

    def _build_technical_analysis_prompt(self, config: Dict[str, Any], 
                                       analysis_params: Dict[str, Any], 
                                       structural_analysis: Dict[str, Any]) -> str:
        """Build prompt for technical analysis"""

        prompt = f"""
        As a structural engineer, analyze this container modification project and provide technical recommendations.

        Container Configuration: {json.dumps(config, indent=2)}
        Analysis Parameters: {json.dumps(analysis_params, indent=2)}
        Structural Analysis: {json.dumps(structural_analysis, indent=2)}

        Provide analysis in this JSON format:
        {{
            "structural_recommendations": ["rec1", "rec2", "rec3"],
            "modification_suggestions": ["sug1", "sug2", "sug3"],
            "risk_mitigation": ["risk1", "risk2", "risk3"],
            "code_compliance_notes": ["note1", "note2", "note3"],
            "cost_impact": {{
                "structural_reinforcement": "impact description",
                "system_upgrades": "impact description",
                "code_compliance": "impact description"
            }}
        }}
        """

        return prompt

def estimate_cost_with_ai(config: Dict[str, Any], ai_model: str = "Auto-Select Best") -> str:
    """
    Generate AI cost estimate using specified model

    Args:
        config: Container configuration dictionary
        ai_model: Selected AI model name

    Returns:
        Formatted cost estimate as string
    """

    # Import translations here to avoid circular imports
    try:
        from utils.translations import get_current_language, t
        current_language = get_current_language()
    except ImportError:
        current_language = 'en'

    # Map the configuration format from the UI to the AI service format
    mapped_config = {
        'container_type': config.get('container_type', '20ft Standard'),
        'base_type': config.get('container_type', '20ft Standard'),
        'use_case': config.get('main_purpose', 'Office Space'),
        'environment': config.get('environment', 'Indoor'),
        'finish_level': config.get('finish_level', 'Basic'),
        'climate_zone': config.get('climate_zone', 'Central European'),
        'occupancy': 1,
        'modifications': {
            'flooring': config.get('flooring', 'Plywood'),
            'windows': config.get('number_of_windows', 0),
            'additional_doors': config.get('additional_doors', False),
            'electrical_system': config.get('finish_level') in ['Premium', 'Luxury'],
            'plumbing_system': config.get('main_purpose') in ['Office Space', 'Living Space'],
            'hvac_system': config.get('climate_zone') in ['Continental', 'Northern European'],
            'insulation_package': config.get('environment') == 'Outdoor'
        }
    }

    # Prepare estimation data
    estimation_data = {
        "container_config": mapped_config,
        "project_location": "Central Europe",
        "project_timeline": "Standard",
        "quality_level": "Standard",
        "additional_notes": "Standard container modification project",
        "response_language": current_language
    }

    # Calculate base costs from config
    base_costs = {
        "container_base": 8000 if config.get('container_type') == '20ft Standard' else 12000,
        "structural_modifications": 2000 if config.get('additional_doors') else 1000,
        "electrical": 1500 if config.get('finish_level') in ['Premium', 'Luxury'] else 800,
        "plumbing": 1200 if config.get('main_purpose') in ['Office Space', 'Living Space'] else 0,
        "hvac": 2000 if config.get('climate_zone') in ['Continental', 'Northern European'] else 1000,
        "finishes": 3000 if config.get('finish_level') == 'Luxury' else 1500,
        "windows": config.get('number_of_windows', 0) * 300
    }

    try:
        # Try Groq service first (free and fast)
        if "Groq" in ai_model or ai_model == "Auto-Select Best":
            try:
                groq_service = GroqService()
                result = groq_service.generate_cost_estimate(estimation_data, base_costs)
                return format_cost_estimate(result, "Groq AI")
            except Exception as e:
                print(f"Groq service failed: {e}")

        # Fallback to OpenAI if available
        if "OpenAI" in ai_model or ai_model == "Auto-Select Best":
            try:
                openai_service = OpenAIService()
                result = openai_service.generate_cost_estimate(estimation_data, base_costs)
                return format_cost_estimate(result, "OpenAI GPT-4o")
            except Exception as e:
                print(f"OpenAI service failed: {e}")

        # Fallback to Anthropic if available
        if "Anthropic" in ai_model or ai_model == "Auto-Select Best":
            try:
                anthropic_service = AnthropicService()
                result = anthropic_service.generate_cost_estimate(estimation_data, base_costs)
                return format_cost_estimate(result, "Anthropic Claude")
            except Exception as e:
                print(f"Anthropic service failed: {e}")

        # Final fallback - generate basic estimate
        return generate_fallback_estimate(config, base_costs, current_language)

    except Exception as e:
        return f"Error generating AI estimate: {str(e)}"

def format_cost_estimate(result: Dict[str, Any], ai_model: str) -> str:
    """Format enhanced AI cost estimate result into comprehensive readable format"""
    
    # Check if this is a raw JSON response that needs parsing
    if isinstance(result, str):
        try:
            import json
            result = json.loads(result)
        except:
            return result  # Return as-is if not parseable JSON
    
    # Handle both old and new response formats
    cost_analysis = result.get('cost_analysis', result)
    total_cost = cost_analysis.get('total_project_cost', cost_analysis.get('total_cost', 0))
    confidence = cost_analysis.get('confidence_rating', cost_analysis.get('confidence_level', cost_analysis.get('confidence', 0.85)))
    timeline = cost_analysis.get('project_duration', cost_analysis.get('estimated_timeline', '8-12 weeks'))
    
    # Cost breakdown - handle both formats
    breakdown = cost_analysis.get('detailed_breakdown', cost_analysis.get('breakdown', {}))
    
    estimate_text = f"""
## 🤖 Enhanced AI Cost Analysis (Generated by {ai_model})

### 💰 **Total Project Investment: €{total_cost:,.2f}**
*Confidence Level: {confidence*100:.0f}%*
*Project Timeline: {timeline}*

---

### 📊 **Detailed Cost Breakdown:**
"""
    
    # Enhanced breakdown display with more flexible mapping
    cost_items = [
        ('container_acquisition', 'container_base', 'Container Acquisition'),
        ('structural_modifications', 'structural_modifications', 'Structural Modifications'),
        ('building_systems', 'systems_installation', 'Building Systems'),
        ('interior_finishes', 'finishes_interior', 'Interior Finishes'),
        ('professional_services', 'permits_fees', 'Professional Services'),
        ('labor_execution', 'labor_costs', 'Labor & Execution'),
        ('logistics_delivery', 'delivery_logistics', 'Logistics & Delivery'),
        ('project_contingency', 'contingency', 'Project Contingency')
    ]
    
    for new_key, old_key, label in cost_items:
        cost = breakdown.get(new_key, breakdown.get(old_key, 0))
        if cost > 0:
            estimate_text += f"- **{label}:** €{cost:,.2f}\n"

    # Market intelligence with enhanced display
    market_insights = cost_analysis.get('market_intelligence', cost_analysis.get('market_insights', {}))
    if market_insights:
        estimate_text += "\n### 📈 **Market Intelligence:**\n"
        for key, value in market_insights.items():
            if value and str(value).strip():
                label = key.replace('_', ' ').title()
                estimate_text += f"- **{label}:** {value}\n"

    # Technical assessment with enhanced categories
    technical = result.get('technical_assessment', {})
    if technical:
        estimate_text += "\n### 🔧 **Technical Assessment:**\n"
        for category, items in technical.items():
            if items:
                category_label = category.replace('_', ' ').title()
                estimate_text += f"\n**{category_label}:**\n"
                if isinstance(items, list):
                    for i, item in enumerate(items[:4], 1):  # Show up to 4 items
                        estimate_text += f"{i}. {item}\n"
                else:
                    estimate_text += f"- {items}\n"

    # Project execution details
    project_execution = result.get('project_execution', result.get('project_management', {}))
    if project_execution:
        estimate_text += "\n### 📋 **Project Execution Plan:**\n"
        
        # Critical path
        critical_path = project_execution.get('critical_path_analysis', project_execution.get('critical_path', []))
        if critical_path:
            estimate_text += "\n**Critical Path:**\n"
            for i, phase in enumerate(critical_path[:5], 1):
                estimate_text += f"{i}. {phase}\n"
        
        # Resource requirements
        resources = project_execution.get('resource_planning', project_execution.get('resource_requirements', {}))
        if resources:
            estimate_text += "\n**Resource Requirements:**\n"
            for key, value in resources.items():
                if value:
                    label = key.replace('_', ' ').title()
                    estimate_text += f"- **{label}:** {value}\n"

    # Risk analysis with comprehensive display
    risk_analysis = result.get('risk_assessment', result.get('risk_analysis', {}))
    if risk_analysis:
        estimate_text += "\n### ⚠️ **Risk Analysis & Mitigation:**\n"
        
        # Display all risk categories
        risk_categories = ['technical_risks', 'financial_risks', 'schedule_risks', 'operational_risks']
        for risk_type in risk_categories:
            risks = risk_analysis.get(risk_type, [])
            if risks and isinstance(risks, list):
                category_label = risk_type.replace('_', ' ').title()
                estimate_text += f"\n**{category_label}:**\n"
                for i, risk in enumerate(risks[:3], 1):
                    estimate_text += f"{i}. {risk}\n"
        
        # Mitigation strategies
        mitigation = risk_analysis.get('mitigation_strategies', [])
        if mitigation:
            estimate_text += f"\n**Mitigation Strategies:**\n"
            for i, strategy in enumerate(mitigation[:4], 1):
                estimate_text += f"{i}. {strategy}\n"

    # Strategic recommendations with expanded display
    recommendations = result.get('strategic_recommendations', result.get('recommendations', {}))
    if recommendations:
        estimate_text += "\n### 💡 **Strategic Recommendations:**\n"
        
        # Handle both old and new format
        if isinstance(recommendations, dict):
            rec_categories = ['priority_actions', 'immediate_actions', 'cost_optimization', 'value_additions', 'alternative_approaches']
            for category in rec_categories:
                items = recommendations.get(category, [])
                if items and isinstance(items, list):
                    category_label = category.replace('_', ' ').title()
                    estimate_text += f"\n**{category_label}:**\n"
                    for i, item in enumerate(items[:4], 1):
                        estimate_text += f"{i}. {item}\n"
        else:
            # Old format compatibility
            analysis = result.get('analysis', {})
            old_recommendations = analysis.get('recommendations', [])
            for i, rec in enumerate(old_recommendations[:5], 1):
                estimate_text += f"{i}. {rec}\n"

    # Sustainability analysis with detailed metrics
    sustainability = result.get('sustainability_analysis', result.get('sustainability', {}))
    if sustainability:
        estimate_text += "\n### 🌱 **Sustainability Analysis:**\n"
        for key, value in sustainability.items():
            if value and str(value).strip():
                label = key.replace('_', ' ').title()
                if isinstance(value, (int, float)):
                    if 'percentage' in key.lower():
                        estimate_text += f"- **{label}:** {value}%\n"
                    elif 'rating' in key.lower():
                        estimate_text += f"- **{label}:** {value}/10\n"
                    else:
                        estimate_text += f"- **{label}:** {value}\n"
                else:
                    estimate_text += f"- **{label}:** {value}\n"

    # Regulatory compliance information
    regulatory = result.get('regulatory_compliance', {})
    if regulatory:
        estimate_text += "\n### 📋 **Regulatory Compliance:**\n"
        for category, items in regulatory.items():
            if items:
                category_label = category.replace('_', ' ').title()
                estimate_text += f"\n**{category_label}:**\n"
                if isinstance(items, list):
                    for i, item in enumerate(items[:3], 1):
                        estimate_text += f"{i}. {item}\n"
                else:
                    estimate_text += f"- {items}\n"

    # Add debugging info for development
    if len(estimate_text.split('\n')) < 20:  # If response seems too short
        estimate_text += f"\n\n---\n**Debug Info:** Response keys: {list(result.keys())}\n"
        estimate_text += f"**Total sections processed:** {len([k for k in result.keys() if result[k]])}\n"

    return estimate_text

def generate_fallback_estimate(config: Dict[str, Any], base_costs: Dict[str, Any], language: str = 'en') -> str:
    """Generate comprehensive fallback cost estimate when AI services are unavailable"""

    # Import translations here to avoid circular imports
    try:
        from utils.translations import t
    except ImportError:
        # Fallback if translations not available
        def t(key, lang=None):
            return key

    # Calculate total cost
    total_cost = sum(base_costs.values())
    
    # Calculate component costs
    materials_base = base_costs.get('container_base', 0) + base_costs.get('structural_modifications', 0) + base_costs.get('finishes', 0)
    labor_cost = total_cost * 0.4
    permits_fees = total_cost * 0.1
    delivery_cost = base_costs.get('delivery_cost', 800)
    contingency = total_cost * 0.1

    # Generate comprehensive fallback estimate using translations
    estimate = f"""
## 🤖 {t('fallback_cost_estimate', language)}

### 💰 **{t('total_project_cost', language)}: €{total_cost:,.2f}**
*{t('basic_calculation_ai_unavailable', language)}*

---

### 📊 **{t('cost_breakdown', language)}:**
- **{t('materials_base_cost', language)}:** €{materials_base:,.2f}
- **{t('labor_costs_40', language)}:** €{labor_cost:,.2f}
- **{t('contingency_10', language)}:** €{contingency:,.2f}
- **{t('delivery_cost', language)}:** €{delivery_cost:,.2f}

---

### 💡 **{t('standard_recommendations', language)}:**
1. {t('plan_standard_delivery', language)}
2. {t('consider_building_codes', language)}
3. {t('budget_site_preparation', language)}
4. {t('review_electrical_plumbing', language)}

### ⚠️ **{t('standard_risk_factors', language)}:**
1. {t('weather_delays', language)}
2. {t('permit_timeline_variations', language)}
3. {t('site_access_limitations', language)}
4. {t('material_price_fluctuations', language)}

---

*{t('basic_estimate_note', language)}*
"""

    return estimate

class ContainerCostEstimator:
    """
    A class for estimating the cost of container modifications using AI services.
    """

    def __init__(self, openai_api_key: Optional[str] = None, anthropic_api_key: Optional[str] = None):
        """
        Initializes the ContainerCostEstimator with optional OpenAI and Anthropic API keys.

        Args:
            openai_api_key (Optional[str]): The OpenAI API key. If None, OpenAI service will not be used.
            anthropic_api_key (Optional[str]): The Anthropic API key. If None, Anthropic service will not be used.
        """
        self.openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None
        self.anthropic_client = Anthropic(api_key=anthropic_api_key) if anthropic_api_key else None

    def _get_system_message(self, language: str) -> str:
        """Get system message in the appropriate language"""
        messages = {
            'en': "You are a professional container modification cost estimator with expertise in European construction standards and container conversions. Provide detailed cost estimates in English.",
            'pl': "Jesteś profesjonalnym rzeczoznawcą kosztów modyfikacji kontenerów z wiedzą na temat europejskich standardów budowlanych i przebudowy kontenerów. Przedstaw szczegółowe kosztorysy w języku polskim.",
            'de': "Sie sind ein professioneller Kostenschätzer für Containermodifikationen mit Expertise in europäischen Baustandards und Containerumbauten. Stellen Sie detaillierte Kostenschätzungen auf Deutsch bereit.",
            'nl': "Je bent een professionele kostenspecialist voor containermodificaties met expertise in Europese bouwstandaarden en containerconversies. Geef gedetailleerde kostenramingen in het Nederlands.",
            'hu': "Ön egy professzionális konténer-módosítási költségbecslő szakértő, aki jártas az európai építési szabványokban és konténer-átalakításokban. Adjon részletes költségbecsléseket magyar nyelven.",
            'cs': "Jste profesionální odhadce nákladů na úpravy kontejnerů s odborností v evropských stavebních standardech a přestavbách kontejnerů. Poskytněte podrobné odhady nákladů v češtině."
        }
        return messages.get(language, messages['en'])

    def _create_cost_estimation_prompt(self, config_data: Dict[str, Any], language: str = 'en') -> str:
        """Create detailed prompt for cost estimation in the specified language"""

        container_type = config_data.get('container_type', '20ft_standard')
        use_case = config_data.get('use_case', 'office_space')
        environment = config_data.get('environment', 'indoor')
        finish_level = config_data.get('finish_level', 'basic')

        if language == 'pl':
            prompt = f"""
Proszę o szczegółowy kosztorys dla następującego projektu modyfikacji kontenera:

SPECYFIKACJA KONTENERA:
- Typ: {container_type.replace('_', ' ').title()}
- Przeznaczenie: {use_case.replace('_', ' ').title()}
- Środowisko: {environment.title()}
- Poziom wykończenia: {finish_level.title()}

ŻĄDANE MODYFIKACJE:
- Podłoga: {config_data.get('flooring', 'standard').title()}
- Okna: {config_data.get('windows', 0)} sztuk
- Dodatkowe drzwi: {'Tak' if config_data.get('additional_doors') else 'Nie'}
- Strefa klimatyczna: {config_data.get('climate_zone', 'temperate').replace('_', ' ').title()}

SYSTEMY (jeśli wybrane):
- System elektryczny: {'Tak' if config_data.get('electrical_system') else 'Nie'}
- System hydrauliczny: {'Tak' if config_data.get('plumbing_system') else 'Nie'}
- System HVAC: {'Tak' if config_data.get('hvac_system') else 'Nie'}
- Pakiet izolacyjny: {'Tak' if config_data.get('insulation_package') else 'Nie'}

Proszę o podanie:
1. Szczegółowy podział kosztów
2. Szacowanie kosztów robocizny
3. Szacowanie kosztów materiałów
4. Całkowity koszt projektu w EUR
5. Szacowanie czasu realizacji
6. Dodatkowe uwagi lub rekomendacje

Oprzeć szacunki na aktualnych cenach rynkowych w Europie, włączając koszty dostawy/transportu.
Sformatować odpowiedź czytelnie z nagłówkami i punktami dla łatwego czytania.
"""
        elif language == 'de':
            prompt = f"""
Bitte erstellen Sie eine detaillierte Kostenschätzung für das folgende Containermodifikationsprojekt:

CONTAINER-SPEZIFIKATIONEN:
- Typ: {container_type.replace('_', ' ').title()}
- Verwendungszweck: {use_case.replace('_', ' ').title()}
- Umgebung: {environment.title()}
- Ausstattungsniveau: {finish_level.title()}

GEWÜNSCHTE MODIFIKATIONEN:
- Bodenbelag: {config_data.get('flooring', 'standard').title()}
- Fenster: {config_data.get('windows', 0)} Stück
- Zusätzliche Türen: {'Ja' if config_data.get('additional_doors') else 'Nein'}
- Klimazone: {config_data.get('climate_zone', 'temperate').replace('_', ' ').title()}

SYSTEME (falls ausgewählt):
- Elektrisches System: {'Ja' if config_data.get('electrical_system') else 'Nein'}
- Sanitärsystem: {'Ja' if config_data.get('plumbing_system') else 'Nein'}
- HVAC-System: {'Ja' if config_data.get('hvac_system') else 'Nein'}
- Isolationspaket: {'Ja' if config_data.get('insulation_package') else 'Nein'}

Bitte geben Sie an:
1. Aufgeschlüsselte Kostenübersicht
2. Arbeitskostenschätzung
3. Materialkostenschätzung
4. Gesamtprojektkosten in EUR
5. Zeitschätzung
6. Zusätzliche Überlegungen oder Empfehlungen

Basieren Sie Ihre Schätzungen auf aktuellen europäischen Marktpreisen und schließen Sie Liefer-/Transportkosten ein.
Formatieren Sie die Antwort klar mit Überschriften und Aufzählungspunkten für einfaches Lesen.
"""
        elif language == 'nl':
            prompt = f"""
Gelieve een gedetailleerde kostenraming te verstrekken voor het volgende containermodificatieproject:

CONTAINER SPECIFICATIES:
- Type: {container_type.replace('_', ' ').title()}
- Beoogd gebruik: {use_case.replace('_', ' ').title()}
- Omgeving: {environment.title()}
- Afwerkingsniveau: {finish_level.title()}

GEVRAAGDE WIJZIGINGEN:
- Vloerbedekking: {config_data.get('flooring', 'standard').title()}
- Ramen: {config_data.get('windows', 0)} stuks
- Extra deuren: {'Ja' if config_data.get('additional_doors') else 'Nee'}
- Klimaatzone: {config_data.get('climate_zone', 'temperate').replace('_', ' ').title()}

SYSTEMEN (indien geselecteerd):
- Elektrisch systeem: {'Ja' if config_data.get('electrical_system') else 'Nee'}
- Leidingsysteem: {'Ja' if config_data.get('plumbing_system') else 'Nee'}
- HVAC-systeem: {'Ja' if config_data.get('hvac_system') else 'Nee'}
- Isolatiepakket: {'Ja' if config_data.get('insulation_package') else 'Nee'}

Gelieve te verstrekken:
1. Gespecificeerde kostenverdeling
2. Arbeidskosten schatting
3. Materiaalkosten schatting
4. Totale projectkosten in EUR
5. Tijdsinschatting
6. Aanvullende overwegingen of aanbevelingen

Baseer uw schattingen op huidige Europese marktprijzen en voeg leverings-/transportkosten toe.
Formatteer het antwoord duidelijk met kopjes en opsommingstekens voor gemakkelijk lezen.
"""
        elif language == 'hu':
            prompt = f"""
Kérem, készítsen részletes költségbecslést a következő konténer-módosítási projekthez:

KONTÉNER SPECIFIKÁCIÓK:
- Típus: {container_type.replace('_', ' ').title()}
- Rendeltetés: {use_case.replace('_', ' ').title()}
- Környezet: {environment.title()}
- Befejezési szint: {finish_level.title()}

KÉRT MÓDOSÍTÁSOK:
- Padló: {config_data.get('flooring', 'standard').title()}
- Ablakok: {config_data.get('windows', 0)} darab
- További ajtók: {'Igen' if config_data.get('additional_doors') else 'Nem'}
- Klímaövezet: {config_data.get('climate_zone', 'temperate').replace('_', ' ').title()}

RENDSZEREK (ha kiválasztott):
- Elektromos rendszer: {'Igen' if config_data.get('electrical_system') else 'Nem'}
- Vízvezeték rendszer: {'Igen' if config_data.get('plumbing_system') else 'Nem'}
- HVAC rendszer: {'Igen' if config_data.get('hvac_system') else 'Nem'}
- Szigetelési csomag: {'Igen' if config_data.get('insulation_package') else 'Nem'}

Kérem, adja meg:
1. Részletes költségbontást
2. Munkaerőköltség becslést
3. Anyagköltség becslést
4. Teljes projektköltséget EUR-ban
5. Időbecslést
6. További megfontolásokat vagy ajánlásokat

Alapozza becsléseit a jelenlegi európai piaci árakra, és vegye figyelembe a szállítási/fuvarozási költségeket.
Formázza a választ világosan címekkel és felsorolásokkal a könnyű olvashatóság érdekében.
"""
        elif language == 'cs':
            prompt = f"""
Prosím o podrobný odhad nákladů na následující projekt úprav kontejneru:

SPECIFIKACE KONTEJNERU:
- Typ: {container_type.replace('_', ' ').title()}
- Zamýšlené použití: {use_case.replace('_', ' ').title()}
- Prostředí: {environment.title()}
- Úroveň dokončení: {finish_level.title()}

POŽADOVANÉ ÚPRAVY:
- Podlaha: {config_data.get('flooring', 'standard').title()}
- Okna: {config_data.get('windows', 0)} kusů
- Další dveře: {'Ano' if config_data.get('additional_doors') else 'Ne'}
- Klimatická zóna: {config_data.get('climate_zone', 'temperate').replace('_', ' ').title()}

SYSTÉMY (pokud vybráno):
- Elektrický systém: {'Ano' if config_data.get('electrical_system') else 'Ne'}
- Instalatérský systém: {'Ano' if config_data.get('plumbing_system') else 'Ne'}
- HVAC systém: {'Ano' if config_data.get('hvac_system') else 'Ne'}
- Izolační balíček: {'Ano' if config_data.get('insulation_package') else 'Ne'}

Prosím poskytněte:
1. Položkový rozpis nákladů
2. Odhad nákladů na práci
3. Odhad nákladů na materiál
4. Celkové náklady projektu v EUR
5. Odhad času
6. Dodatečné úvahy nebo doporučení

Založte své odhady na současných evropských tržních cenách a zahrňte náklady na dopravu/přepravu.
Naformátujte odpověď jasně s nadpisy a odrážkami pro snadné čtení.
"""
        else:  # English default
            prompt = f"""
Please provide a detailed cost estimate for the following container modification project:

CONTAINER SPECIFICATIONS:
- Type: {container_type.replace('_', ' ').title()}
- Intended Use: {use_case.replace('_', ' ').title()}
- Environment: {environment.title()}
- Finish Level: {finish_level.title()}

MODIFICATIONS REQUESTED:
- Flooring: {config_data.get('flooring', 'standard').title()}
- Windows: {config_data.get('windows', 0)} units
- Additional Doors: {'Yes' if config_data.get('additional_doors') else 'No'}
- Climate Zone: {config_data.get('climate_zone', 'temperate').replace('_', ' ').title()}

SYSTEMS (if selected):
- Electrical System: {'Yes' if config_data.get('electrical_system') else 'No'}
- Plumbing System: {'Yes' if config_data.get('plumbing_system') else 'No'}
- HVAC System: {'Yes' if config_data.get('hvac_system') else 'No'}
- Insulation Package: {'Yes' if config_data.get('insulation_package') else 'No'}

Please provide:
1. Itemized cost breakdown
2. Labor costs estimation
3. Material costs estimation
4. Total project cost in EUR
5. Timeline estimation
6. Any additional considerations or recommendations

Base your estimates on current European market prices and include delivery/transport costs.
Format the response clearly with headers and bullet points for easy reading.
"""

        return prompt

    def _validate_cost_response(self, response: str) -> bool:
        """Simple validation to ensure the response contains cost-related information."""
        return "EUR" in response or "€" in response or "cost" in response.lower()

    def generate_fallback_estimate(self, config_data: Dict[str, Any], language: str = 'en') -> str:
        """Generate a fallback estimate using predefined logic when AI services fail"""
        try:
            from utils.translations import t

            # Base costs (in EUR)
            base_costs = {
                '20ft_standard': 8000,
                '20ft_high_cube': 9000,
                '40ft_standard': 12000,
                '40ft_high_cube': 13500
            }

            # Get base cost
            container_type = config_data.get('container_type', '20ft_standard')
            base_cost = base_costs.get(container_type, 8000)

            # Calculate modifications cost
            modifications_cost = 0

            # Finish level multiplier
            finish_levels = {'basic': 1.0, 'standard': 1.3, 'premium': 1.8, 'luxury': 2.5}
            finish_level = config_data.get('finish_level', 'basic')
            finish_multiplier = finish_levels.get(finish_level, 1.0)

            # Add costs for specific modifications
            if config_data.get('windows', 0) > 0:
                modifications_cost += config_data['windows'] * 500

            if config_data.get('additional_doors', False):
                modifications_cost += 800

            # Flooring costs
            flooring_costs = {'plywood': 800, 'laminate': 1200, 'vinyl': 1000, 'concrete': 600}
            flooring = config_data.get('flooring', 'plywood')
            modifications_cost += flooring_costs.get(flooring, 800)

            # HVAC, electrical, etc.
            if config_data.get('hvac_system'):
                modifications_cost += 2500
            if config_data.get('electrical_system'):
                modifications_cost += 1500
            if config_data.get('plumbing_system'):
                modifications_cost += 2000

            # Apply finish level multiplier
            modifications_cost = int(modifications_cost * finish_multiplier)

            # Delivery cost
            delivery_cost = 800

            # Environment multiplier
            environment_multipliers = {'indoor': 1.0, 'outdoor': 1.3, 'marine': 1.6}
            environment = config_data.get('environment', 'indoor')
            env_multiplier = environment_multipliers.get(environment, 1.0)

            # Calculate total
            subtotal = (base_cost + modifications_cost + delivery_cost)
            total_cost = int(subtotal * env_multiplier)

            # Generate response using translations
            response = f"""
# {t('configuration_summary', language)}

**{t('base_container', language)}:**

• {t('type', language)}: {t(f'container.types.{container_type}', language)}

• {t('use_case', language)}: {t(f'container.use_cases.{config_data.get("use_case", "office_space")}', language)}

• {t('environment', language)}: {t(f'container.environment.{environment}', language)}

**{t('key_modifications', language)}:**

• {t('finish_level', language)}: {t(f'container.finish_levels.{finish_level}', language)}

• {t('flooring', language)}: {t(f'container.flooring.{flooring}', language)}

• {t('windows', language)}: {config_data.get('windows', 0)}

**{t('cost_breakdown', language)}:**

• {t('base_cost', language)}: €{base_cost:,.2f}

• {t('modifications', language)}: €{modifications_cost:,.2f}

• {t('delivery_cost', language)}: €{delivery_cost:,.2f}

• {t('multiplier', language)}: {env_multiplier}x

**{t('total_cost', language)}: €{total_cost:,.2f}**

*{t('preliminary_estimate_note', language)}*
"""

            return response.strip()

        except Exception as e:
            print(f"Error in fallback estimate generation: {e}")
            return f"Error generating estimate: {str(e)}"

    def estimate_container_cost(self, config_data: Dict[str, Any], language: str = 'en') -> str:
        """
        Generate container cost estimate using AI services
        Falls back to local estimation if AI services fail
        """
        try:
            # Create comprehensive prompt for cost estimation in the selected language
            prompt = self._create_cost_estimation_prompt(config_data, language)

            # Try OpenAI first
            if self.openai_client:
                try:
                    system_message = self._get_system_message(language)
                    response = self.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=1000,
                        temperature=0.7
                    )

                    ai_response = response.choices[0].message.content

                    # Validate the response contains cost information
                    if self._validate_cost_response(ai_response):
                        return ai_response
                    else:
                        print("OpenAI response validation failed, trying Anthropic...")

                except Exception as e:
                    print(f"OpenAI API error: {e}")

            # Try Anthropic if OpenAI fails
            if self.anthropic_client:
                try:
                    response = self.anthropic_client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=1000,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )

                    ai_response = response.content[0].text

                    # Validate the response contains cost information
                    if self._validate_cost_response(ai_response):
                        return ai_response
                    else:
                        print("Anthropic response validation failed, using fallback...")

                except Exception as e:
                    print(f"Anthropic API error: {e}")

            # If both AI services fail, use fallback estimation
            print("All AI services failed, using fallback estimation...")
            return self.generate_fallback_estimate(config_data, language)

        except Exception as e:
            print(f"Error in estimate_container_cost: {e}")
            return self.generate_fallback_estimate(config_data, language)