
import json
import os
from typing import Dict, List, Tuple, Set
import re

class TranslationQualityAnalyzer:
    """Comprehensive translation quality analyzer with formatted output"""
    
    def __init__(self):
        self.locales_dir = "locales"
        self.base_language = "pl"  # Using Polish as base reference
        
    def load_translation_file(self, language: str) -> Dict:
        """Load a specific translation file"""
        filepath = os.path.join(self.locales_dir, f"{language}.json")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading {filepath}: {e}")
            return {}
    
    def get_all_keys_flat(self, data: Dict, prefix: str = "") -> Dict[str, str]:
        """Get all keys from nested dict as flat key-value pairs"""
        result = {}
        
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                result.update(self.get_all_keys_flat(value, full_key))
            elif isinstance(value, str):
                result[full_key] = value
        
        return result
    
    def analyze_language_quality(self, language: str, base_translations: Dict[str, str]) -> Dict:
        """Analyze translation quality for a specific language"""
        lang_data = self.load_translation_file(language)
        if not lang_data:
            return {"error": f"Could not load {language} translations"}
        
        lang_translations = self.get_all_keys_flat(lang_data)
        
        # Categorize translations
        good_translations = []
        auto_placeholder = []
        identical_to_base = []
        suspicious = []
        missing = []
        
        for key, base_value in base_translations.items():
            lang_value = lang_translations.get(key)
            
            if lang_value is None:
                missing.append(key)
            elif self.is_auto_placeholder(lang_value):
                auto_placeholder.append((key, lang_value))
            elif lang_value == base_value and language != self.base_language:
                identical_to_base.append((key, lang_value))
            elif self.is_suspicious_translation(base_value, lang_value, language):
                suspicious.append((key, lang_value))
            else:
                good_translations.append((key, lang_value))
        
        total_keys = len(base_translations)
        quality_score = len(good_translations) / total_keys * 100 if total_keys > 0 else 0
        
        return {
            "good_translations": good_translations,
            "auto_placeholder": auto_placeholder,
            "identical_to_base": identical_to_base,
            "suspicious": suspicious,
            "missing": missing,
            "quality_score": quality_score,
            "total_keys": total_keys
        }
    
    def is_auto_placeholder(self, text: str) -> bool:
        """Check if text is an auto/placeholder translation"""
        if not text:
            return False
        
        # Check for [AUTO] prefix
        if text.startswith("[AUTO]"):
            return True
        
        # Check for [TRANSLATE] prefix
        if text.startswith("[TRANSLATE]"):
            return True
        
        return False
    
    def is_suspicious_translation(self, base_text: str, translated_text: str, target_lang: str) -> bool:
        """Check if translation seems suspicious"""
        if not base_text or not translated_text:
            return False
        
        # Check if translation is just English with different casing
        if base_text.lower() == translated_text.lower() and base_text != translated_text:
            return True
        
        # Check for obvious English words that should be translated
        english_words = [
            'container', 'basic', 'standard', 'premium', 'system', 'analysis',
            'configuration', 'installation', 'professional', 'advanced',
            'delivery', 'transport', 'office', 'equipment', 'security'
        ]
        
        translated_lower = translated_text.lower()
        for word in english_words:
            if word in translated_lower and len(translated_text) > len(word) + 2:
                return True
        
        return False
    
    def get_quality_indicator(self, quality_score: float) -> str:
        """Get quality indicator emoji based on score"""
        if quality_score >= 95:
            return "🟢"
        elif quality_score >= 80:
            return "🟡"
        else:
            return "🔴"
    
    def format_language_analysis(self, language: str, analysis: Dict) -> str:
        """Format analysis results for a single language"""
        if "error" in analysis:
            return f"❌ {language.upper()}: {analysis['error']}"
        
        total = analysis["total_keys"]
        good = len(analysis["good_translations"])
        auto = len(analysis["auto_placeholder"])
        identical = len(analysis["identical_to_base"])
        suspicious = len(analysis["suspicious"])
        missing = len(analysis["missing"])
        quality = analysis["quality_score"]
        
        result = f"Checking {language.upper()} translations...\n"
        result += f"   📊 {language.upper()} Translation Analysis:\n"
        result += f"      ✅ Good translations: {good} ({good/total*100:.1f}%)\n"
        result += f"      🤖 Auto/placeholder: {auto} ({auto/total*100:.1f}%)\n"
        result += f"      🔄 Identical to base: {identical} ({identical/total*100:.1f}%)\n"
        result += f"      ⚠️  Suspicious: {suspicious} ({suspicious/total*100:.1f}%)\n"
        result += f"      ❌ Missing: {missing} ({missing/total*100:.1f}%)\n"
        result += f"      🎯 Quality Score: {quality:.1f}%\n"
        
        # Show sample auto translations
        if auto > 0:
            result += "   🤖 Sample auto translations:\n"
            for key, value in analysis["auto_placeholder"][:3]:
                result += f"      {key}: '{value}'\n"
        
        # Show sample suspicious translations
        if suspicious > 0:
            result += "   ⚠️  Sample suspicious translations:\n"
            for key, value in analysis["suspicious"][:3]:
                result += f"      {key}: '{value}'\n"
        
        # Show missing keys
        if missing > 0:
            result += "   ❌ Missing keys:\n"
            for key in analysis["missing"][:3]:
                result += f"      {key}\n"
        
        return result
    
    def run_comprehensive_analysis(self) -> str:
        """Run comprehensive analysis for all languages"""
        # Load base language
        base_data = self.load_translation_file(self.base_language)
        if not base_data:
            return f"❌ Could not load base language ({self.base_language})"
        
        base_translations = self.get_all_keys_flat(base_data)
        
        # Get all available languages
        available_languages = []
        for filename in os.listdir(self.locales_dir):
            if filename.endswith('.json'):
                lang = filename[:-5]  # Remove .json extension
                if lang != self.base_language:
                    available_languages.append(lang)
        
        available_languages.sort()
        
        # Analyze each language
        results = []
        summary_data = []
        
        for language in available_languages:
            analysis = self.analyze_language_quality(language, base_translations)
            if "error" not in analysis:
                formatted = self.format_language_analysis(language, analysis)
                results.append(formatted)
                
                summary_data.append({
                    'language': language,
                    'quality': analysis['quality_score'],
                    'missing': len(analysis['missing']),
                    'auto': len(analysis['auto_placeholder']),
                    'suspicious': len(analysis['suspicious'])
                })
        
        # Create summary
        summary_data.sort(key=lambda x: x['quality'], reverse=True)
        
        summary = "\n" + "="*60 + "\n"
        summary += "📋 OVERALL TRANSLATION QUALITY SUMMARY\n"
        summary += "="*60 + "\n"
        summary += f"{'Language':<10} {'Quality':<8} {'Missing':<8} {'Auto':<8} {'Suspicious':<12}\n"
        summary += "-"*60 + "\n"
        
        high_priority = []
        medium_priority = []
        
        for item in summary_data:
            lang = item['language'].upper()
            quality = item['quality']
            missing = item['missing']
            auto = item['auto']
            suspicious = item['suspicious']
            indicator = self.get_quality_indicator(quality)
            
            summary += f"{lang:<10} {quality:>6.1f}%    {missing:<8} {auto:<8} {suspicious:<12} {indicator}\n"
            
            if quality < 80:
                high_priority.append(lang)
            elif quality < 95:
                medium_priority.append(lang)
        
        summary += "\n🎯 PRIORITY ACTIONS:\n"
        if high_priority:
            summary += f"🔴 High Priority (fix immediately): {', '.join(high_priority)}\n"
        if medium_priority:
            summary += f"🟡 Medium Priority (review and improve): {', '.join(medium_priority)}\n"
        
        summary += "\n" + "="*70 + "\n"
        summary += "✅ Translation quality check completed!\n"
        summary += "💡 Review the results above and run fixes as needed.\n"
        
        # Combine all results
        full_result = "\n".join(results) + summary
        return full_result

# CLI interface
def main():
    analyzer = TranslationQualityAnalyzer()
    results = analyzer.run_comprehensive_analysis()
    print(results)

if __name__ == "__main__":
    main()
