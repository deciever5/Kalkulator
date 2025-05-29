"""
European Climate Standards and Environmental Conditions
Replaces US-based seismic zones with European climate considerations
"""

from typing import Dict, Any

class EuropeanClimateStandards:
    """European climate zones and environmental conditions for container analysis"""
    
    def __init__(self):
        self.climate_zones = {
            'Umiarkowana (Europa Środkowa)': {
                'snow_load_factor': 1.0,
                'temperature_factor': 1.0,
                'wind_factor': 1.0,
                'humidity_factor': 1.0,
                'description': 'Standardowe warunki europejskie',
                'typical_countries': ['Polska', 'Czechy', 'Słowacja', 'Austria']
            },
            'Subpolarna (Skandynawia)': {
                'snow_load_factor': 2.5,
                'temperature_factor': 1.5,
                'wind_factor': 1.3,
                'humidity_factor': 1.1,
                'description': 'Ekstremalne warunki zimowe, wysokie obciążenia śniegiem',
                'typical_countries': ['Szwecja', 'Norwegia', 'Finlandia', 'Północna Rosja']
            },
            'Morska (Wybrzeża)': {
                'snow_load_factor': 0.8,
                'temperature_factor': 0.9,
                'wind_factor': 1.4,
                'humidity_factor': 1.3,
                'description': 'Wysokie zasolenie, korozja, silne wiatry',
                'typical_countries': ['Holandia', 'Dania', 'Wybrzeża UK', 'Północne Niemcy']
            },
            'Górska (Alpy, Karpaty)': {
                'snow_load_factor': 3.0,
                'temperature_factor': 1.4,
                'wind_factor': 1.2,
                'humidity_factor': 0.9,
                'description': 'Ekstremalne obciążenia śniegiem, wahania temperatur',
                'typical_countries': ['Szwajcaria', 'Austria', 'Rumunia', 'Słowacja']
            },
            'Kontynentalna (Europa Wschodnia)': {
                'snow_load_factor': 1.8,
                'temperature_factor': 1.3,
                'wind_factor': 1.1,
                'humidity_factor': 0.8,
                'description': 'Suche, ekstremalne wahania temperatur',
                'typical_countries': ['Ukraina', 'Białoruś', 'Wschodnia Polska', 'Węgry']
            },
            'Śródziemnomorska (Południe)': {
                'snow_load_factor': 0.3,
                'temperature_factor': 0.7,
                'wind_factor': 1.0,
                'humidity_factor': 1.2,
                'description': 'Wysokie temperatury, minimalne obciążenia śniegiem',
                'typical_countries': ['Hiszpania', 'Włochy', 'Grecja', 'Południowa Francja']
            }
        }
        
        self.environmental_conditions = {
            'Standardowe': {
                'corrosion_factor': 1.0,
                'durability_factor': 1.0,
                'maintenance_factor': 1.0,
                'description': 'Normalne warunki środowiskowe'
            },
            'Wysokie zasolenie (morskie)': {
                'corrosion_factor': 1.5,
                'durability_factor': 0.8,
                'maintenance_factor': 1.4,
                'description': 'Przyspiesziona korozja, wymagane specjalne powłoki'
            },
            'Wysoka wilgotność': {
                'corrosion_factor': 1.2,
                'durability_factor': 0.9,
                'maintenance_factor': 1.2,
                'description': 'Zwiększone ryzyko korozji i pleśni'
            },
            'Przemysłowe (zanieczyszczenia)': {
                'corrosion_factor': 1.3,
                'durability_factor': 0.85,
                'maintenance_factor': 1.3,
                'description': 'Chemiczne zanieczyszczenia powietrza'
            },
            'Agresywne chemicznie': {
                'corrosion_factor': 1.6,
                'durability_factor': 0.7,
                'maintenance_factor': 1.5,
                'description': 'Bardzo agresywne środowisko chemiczne'
            },
            'Ekstremalne temperatury': {
                'corrosion_factor': 1.1,
                'durability_factor': 0.9,
                'maintenance_factor': 1.3,
                'description': 'Duże wahania temperatur, rozszerzalność termiczna'
            }
        }
    
    def get_climate_factors(self, climate_zone: str) -> Dict[str, float]:
        """Get climate adjustment factors for specific zone"""
        return self.climate_zones.get(climate_zone, self.climate_zones['Umiarkowana (Europa Środkowa)'])
    
    def get_environmental_factors(self, conditions: str) -> Dict[str, float]:
        """Get environmental condition factors"""
        return self.environmental_conditions.get(conditions, self.environmental_conditions['Standardowe'])
    
    def calculate_snow_load(self, base_snow_load: float, climate_zone: str) -> float:
        """Calculate adjusted snow load based on European climate zone"""
        factor = self.get_climate_factors(climate_zone)['snow_load_factor']
        return base_snow_load * factor
    
    def calculate_wind_load(self, base_wind_load: float, climate_zone: str) -> float:
        """Calculate adjusted wind load"""
        factor = self.get_climate_factors(climate_zone)['wind_factor']
        return base_wind_load * factor
    
    def get_material_recommendations(self, climate_zone: str, environmental_conditions: str) -> Dict[str, Any]:
        """Get material recommendations based on climate and environment"""
        
        climate_data = self.get_climate_factors(climate_zone)
        env_data = self.get_environmental_factors(environmental_conditions)
        
        recommendations = {
            'steel_grade': 'S355' if climate_data['temperature_factor'] > 1.2 else 'S275',
            'coating_system': self._get_coating_recommendation(env_data['corrosion_factor']),
            'insulation_thickness': self._get_insulation_recommendation(climate_data['temperature_factor']),
            'ventilation_requirements': self._get_ventilation_recommendation(climate_data['humidity_factor']),
            'special_considerations': []
        }
        
        # Add special considerations
        if climate_data['snow_load_factor'] > 2.0:
            recommendations['special_considerations'].append('Wzmocnienie dachu pod obciążenia śniegiem')
        
        if env_data['corrosion_factor'] > 1.3:
            recommendations['special_considerations'].append('Zaawansowany system antykorozyjny')
        
        if climate_data['wind_factor'] > 1.3:
            recommendations['special_considerations'].append('Dodatkowe kotwienie przeciwwiatrowe')
        
        if climate_data['temperature_factor'] > 1.3:
            recommendations['special_considerations'].append('Mostki termiczne, dylatacje')
        
        return recommendations
    
    def _get_coating_recommendation(self, corrosion_factor: float) -> str:
        """Recommend coating system based on corrosion risk"""
        if corrosion_factor >= 1.5:
            return 'System 3-warstwowy + cynkowanie ogniowe'
        elif corrosion_factor >= 1.2:
            return 'System 2-warstwowy + primer antykorozyjny'
        else:
            return 'Standardowy system malarski'
    
    def _get_insulation_recommendation(self, temperature_factor: float) -> str:
        """Recommend insulation thickness"""
        if temperature_factor >= 1.4:
            return '150-200mm (klimat subarktyczny)'
        elif temperature_factor >= 1.2:
            return '120-150mm (klimat chłodny)'
        elif temperature_factor <= 0.8:
            return '80-100mm (klimat ciepły)'
        else:
            return '100-120mm (klimat umiarkowany)'
    
    def _get_ventilation_recommendation(self, humidity_factor: float) -> str:
        """Recommend ventilation system"""
        if humidity_factor >= 1.3:
            return 'Wentylacja mechaniczna z osuszaniem'
        elif humidity_factor >= 1.1:
            return 'Wentylacja mechaniczna nawiewno-wywiewna'
        else:
            return 'Wentylacja naturalna z wywiewnikami'
    
    def get_compliance_requirements(self, climate_zone: str, use_case: str) -> Dict[str, Any]:
        """Get European compliance requirements"""
        
        base_standards = {
            'structural': ['EN 1990', 'EN 1991', 'EN 1993'],
            'thermal': ['EN ISO 6946', 'EN 12831'],
            'fire': ['EN 13501-1'],
            'accessibility': ['EN 17210'] if 'Residential' in use_case or 'Office' in use_case else []
        }
        
        # Climate-specific additions
        climate_data = self.get_climate_factors(climate_zone)
        
        if climate_data['snow_load_factor'] > 2.0:
            base_standards['structural'].append('EN 1991-1-3 (Snow loads)')
        
        if climate_data['wind_factor'] > 1.3:
            base_standards['structural'].append('EN 1991-1-4 (Wind actions)')
        
        if 'Morska' in climate_zone:
            base_standards['corrosion'] = ['EN ISO 12944', 'EN 1993-1-4']
        
        return base_standards