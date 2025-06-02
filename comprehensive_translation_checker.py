#!/usr/bin/env python3
"""
Comprehensive Translation Checker
Uses Polish as base language to find all missing and wrong translations
"""

import json
import os
from typing import Dict, List, Tuple, Set
import re

class ComprehensiveTranslationChecker:
    """Advanced translation checker using Polish as base reference"""

    def __init__(self):
        self.locales_dir = "locales"
        self.base_language = "pl"  # Polish as base
        self.target_languages = ['cs', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'nl', 'sk', 'sv', 'uk']

    def load_json_file(self, filepath: str) -> Dict:
        """Load JSON translation file"""
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

    def is_placeholder_text(self, text: str) -> bool:
        """Check if text is a placeholder that needs translation"""
        if not text:
            return False

        placeholder_indicators = [
            '[AUTO]', '[TRANSLATE]', '[TODO]', '[FIXME]',
            'placeholder_', 'temp_', 'auto_', 'TODO:', 'FIXME:',
            'lorem ipsum', 'sample text', 'example text',
            'translation needed', 'add translation'
        ]

        text_lower = text.lower()
        return any(indicator.lower() in text_lower for indicator in placeholder_indicators)

    def is_likely_english(self, text: str) -> bool:
        """Check if text is likely English and should be translated"""
        if not text or len(text) < 3:
            return False

        # Common English words that should be translated in technical contexts
        english_indicators = [
            'container', 'basic', 'standard', 'premium', 'advanced',
            'configuration', 'installation', 'delivery', 'transport',
            'office', 'equipment', 'security', 'system', 'analysis',
            'professional', 'custom', 'layout', 'interior', 'exterior',
            'window', 'door', 'insulation', 'heating', 'cooling',
            'electrical', 'plumbing', 'flooring', 'ceiling', 'wall',
            'partition', 'storage', 'workspace', 'meeting', 'reception'
        ]

        text_lower = text.lower()
        english_word_count = sum(1 for word in english_indicators if word in text_lower)

        # If text contains multiple English technical terms, it's likely English
        return english_word_count >= 2 or (english_word_count >= 1 and len(text.split()) <= 3)

    def is_identical_but_should_differ(self, polish_text: str, target_text: str, target_lang: str) -> bool:
        """Check if text is identical to Polish but should be different"""
        if polish_text != target_text:
            return False

        # These terms can remain the same across languages
        keep_identical = [
            'KAN-BUD', 'OpenAI', 'GPT', 'API', 'PDF', 'DWG', 'HVAC', 'ADA',
            'GDPR', 'ISO', 'EN', 'DIN', 'mm', 'cm', 'm', 'kg', 'EUR', 'PLN', 'USD',
            'HTML', 'CSS', 'JavaScript', 'Python', 'C2', 'C3'
        ]

        # Numbers and short codes can be identical
        if len(polish_text) <= 3 or polish_text.isdigit():
            return False

        # Check if it's a term that should remain identical
        for term in keep_identical:
            if term.lower() in polish_text.lower():
                return False

        # If it contains Polish-specific characters or words, it should be translated
        polish_chars = 'ąćęłńóśźż'
        polish_words = [
            'kontener', 'konfiguracja', 'dostawa', 'transport', 'biuro',
            'wyposażenie', 'bezpieczeństwo', 'system', 'analiza',
            'profesjonalny', 'niestandardowy', 'układ', 'wnętrze',
            'zewnętrzny', 'okno', 'drzwi', 'izolacja', 'ogrzewanie',
            'chłodzenie', 'elektryczny', 'instalacja', 'podłoga'
        ]

        has_polish_chars = any(char in polish_text.lower() for char in polish_chars)
        has_polish_words = any(word in polish_text.lower() for word in polish_words)

        return has_polish_chars or has_polish_words

    def analyze_language(self, language: str, base_translations: Dict[str, str]) -> Dict:
        """Analyze translation quality for a specific language"""
        lang_file = os.path.join(self.locales_dir, f"{language}.json")
        lang_data = self.load_json_file(lang_file)

        if not lang_data:
            return {"error": f"Could not load {language} translations"}

        lang_translations = self.get_all_keys_flat(lang_data)

        # Categorize issues
        missing_keys = []
        placeholder_translations = []
        english_translations = []
        identical_translations = []
        good_translations = []

        for key, polish_value in base_translations.items():
            target_value = lang_translations.get(key)

            if target_value is None:
                missing_keys.append(key)
            elif self.is_placeholder_text(target_value):
                placeholder_translations.append((key, target_value))
            elif self.is_likely_english(target_value):
                english_translations.append((key, target_value))
            elif self.is_identical_but_should_differ(polish_value, target_value, language):
                identical_translations.append((key, target_value))
            else:
                good_translations.append((key, target_value))

        total_keys = len(base_translations)
        quality_score = len(good_translations) / total_keys * 100 if total_keys > 0 else 0

        return {
            "missing_keys": missing_keys,
            "placeholder_translations": placeholder_translations,
            "english_translations": english_translations,
            "identical_translations": identical_translations,
            "good_translations": good_translations,
            "quality_score": quality_score,
            "total_keys": total_keys
        }

    def format_language_report(self, language: str, analysis: Dict) -> str:
        """Format detailed report for a language"""
        if "error" in analysis:
            return f"❌ {language.upper()}: {analysis['error']}\n"

        total = analysis["total_keys"]
        missing = len(analysis["missing_keys"])
        placeholders = len(analysis["placeholder_translations"])
        english = len(analysis["english_translations"])
        identical = len(analysis["identical_translations"])
        good = len(analysis["good_translations"])
        quality = analysis["quality_score"]

        # Determine status emoji
        if quality >= 95:
            status = "🟢"
        elif quality >= 80:
            status = "🟡"
        else:
            status = "🔴"

        report = f"{status} {language.upper()} Translation Analysis\n"
        report += f"{'='*50}\n"
        report += f"📊 Overall Quality: {quality:.1f}% ({good}/{total} good translations)\n"
        report += f"❌ Missing keys: {missing} ({missing/total*100:.1f}%)\n"
        report += f"🏷️  Placeholder text: {placeholders} ({placeholders/total*100:.1f}%)\n"
        report += f"🔤 English text: {english} ({english/total*100:.1f}%)\n"
        report += f"🔄 Identical to Polish: {identical} ({identical/total*100:.1f}%)\n"

        # Show examples of issues
        if missing:
            report += f"\n📋 Missing keys (first 5):\n"
            for key in analysis["missing_keys"][:5]:
                report += f"   • {key}\n"

        if placeholders:
            report += f"\n🏷️  Placeholder translations (first 3):\n"
            for key, value in analysis["placeholder_translations"][:3]:
                report += f"   • {key}: '{value}'\n"

        if english:
            report += f"\n🔤 English translations (first 3):\n"
            for key, value in analysis["english_translations"][:3]:
                report += f"   • {key}: '{value}'\n"

        if identical:
            report += f"\n🔄 Identical to Polish (first 3):\n"
            for key, value in analysis["identical_translations"][:3]:
                report += f"   • {key}: '{value}'\n"

        return report + "\n"

    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive translation report"""
        print("🔍 Loading Polish base translations...")

        # Load Polish as base
        base_file = os.path.join(self.locales_dir, f"{self.base_language}.json")
        base_data = self.load_json_file(base_file)

        if not base_data:
            return f"❌ Could not load base language ({self.base_language})"

        base_translations = self.get_all_keys_flat(base_data)
        print(f"✅ Loaded {len(base_translations)} keys from Polish base")

        # Analyze each target language
        all_analyses = {}
        summary_data = []

        print(f"\n🔍 Analyzing {len(self.target_languages)} target languages...")

        for language in self.target_languages:
            print(f"   Checking {language.upper()}...")
            analysis = self.analyze_language(language, base_translations)

            if "error" not in analysis:
                all_analyses[language] = analysis
                summary_data.append({
                    'language': language,
                    'quality': analysis['quality_score'],
                    'missing': len(analysis['missing_keys']),
                    'placeholders': len(analysis['placeholder_translations']),
                    'english': len(analysis['english_translations']),
                    'identical': len(analysis['identical_translations'])
                })

        # Generate detailed reports
        detailed_reports = []
        for language in sorted(self.target_languages):
            if language in all_analyses:
                detailed_reports.append(self.format_language_report(language, all_analyses[language]))

        # Create summary table
        summary_data.sort(key=lambda x: x['quality'], reverse=True)

        summary = "\n" + "="*80 + "\n"
        summary += "📋 COMPREHENSIVE TRANSLATION SUMMARY (Polish Base)\n"
        summary += "="*80 + "\n"
        summary += f"{'Lang':<6} {'Quality':<8} {'Missing':<8} {'Placeh.':<8} {'English':<8} {'Identical':<10} {'Status'}\n"
        summary += "-"*80 + "\n"

        critical_languages = []
        needs_attention = []
        good_languages = []

        for item in summary_data:
            lang = item['language'].upper()
            quality = item['quality']
            missing = item['missing']
            placeholders = item['placeholders']
            english = item['english']
            identical = item['identical']

            if quality >= 95:
                status = "🟢 Excellent"
                good_languages.append(lang)
            elif quality >= 80:
                status = "🟡 Good"
                needs_attention.append(lang)
            else:
                status = "🔴 Critical"
                critical_languages.append(lang)

            summary += f"{lang:<6} {quality:>6.1f}%  {missing:<8} {placeholders:<8} {english:<8} {identical:<10} {status}\n"

        # Priority recommendations
        summary += "\n🎯 PRIORITY ACTIONS:\n"
        if critical_languages:
            summary += f"🔴 CRITICAL (Quality < 80%): {', '.join(critical_languages)}\n"
            summary += "   → Immediate translation work needed\n"

        if needs_attention:
            summary += f"🟡 NEEDS ATTENTION (80-95%): {', '.join(needs_attention)}\n"
            summary += "   → Review and improve translations\n"

        if good_languages:
            summary += f"🟢 EXCELLENT (95%+): {', '.join(good_languages)}\n"
            summary += "   → Ready for production\n"

        # Overall statistics
        total_issues = sum(item['missing'] + item['placeholders'] + item['english'] + item['identical'] 
                          for item in summary_data)

        summary += f"\n📊 OVERALL STATISTICS:\n"
        summary += f"   Total translation issues found: {total_issues}\n"
        summary += f"   Languages analyzed: {len(summary_data)}\n"
        summary += f"   Average quality score: {sum(item['quality'] for item in summary_data) / len(summary_data):.1f}%\n"

        summary += "\n" + "="*80 + "\n"
        summary += "✅ Comprehensive translation analysis complete!\n"
        summary += "💡 Use the detailed reports above to prioritize translation work.\n"
        summary += "🔧 Run 'python fix_translations.py' to automatically fix issues.\n"

        # Combine all reports
        full_report = "\n".join(detailed_reports) + summary
        return full_report

    def export_missing_keys(self, output_file: str = "missing_translations.json"):
        """Export all missing keys for translation work"""
        base_file = os.path.join(self.locales_dir, f"{self.base_language}.json")
        base_data = self.load_json_file(base_file)
        base_translations = self.get_all_keys_flat(base_data)

        missing_by_language = {}

        for language in self.target_languages:
            analysis = self.analyze_language(language, base_translations)
            if "error" not in analysis and analysis["missing_keys"]:
                missing_by_language[language] = {
                    key: base_translations[key] for key in analysis["missing_keys"]
                }

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(missing_by_language, f, ensure_ascii=False, indent=2)
            print(f"📄 Missing translations exported to {output_file}")
        except Exception as e:
            print(f"❌ Error exporting missing translations: {e}")

def main():
    """Main function to run comprehensive translation check"""
    checker = ComprehensiveTranslationChecker()

    print("🚀 COMPREHENSIVE TRANSLATION CHECKER")
    print("Using Polish as base language reference")
    print("="*60)

    # Generate and display report
    report = checker.generate_comprehensive_report()
    print(report)

    # Export missing keys for translator reference
    checker.export_missing_keys()

if __name__ == "__main__":
    main()