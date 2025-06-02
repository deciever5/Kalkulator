#!/usr/bin/env python3
"""
Language Purity Scanner
Checks if translation files contain only the target language 
(excluding worldwide technical terms)
"""

import json
import os
import re
from typing import Dict, List, Set, Tuple

class LanguagePurityScanner:
    def __init__(self, locales_dir: str = "locales"):
        self.locales_dir = locales_dir

        # Common technical terms that are acceptable in any language
        self.worldwide_terms = {
            # Technical standards
            'hvac', 'pdf', 'dwg', 'jpg', 'png', 'doc', 'docx', 'gdpr', 'ada', 'atex', 'knx',
            'ups', 'ip', 'cctv', 'vrf', 'vrv', 'hpl', 'lvt', 'ral', 'ac4', 'ac5', 'pvc',
            'wc', 'led', 'ir', 'usb', 'wi-fi', 'wifi', 'it', 'api', 'ai', 'gpt', 'openai',

            # Measurements and units
            'mm', 'cm', 'm', 'ft', 'kw', '25a', '40a', '63a', 't18', 't35', 't55',
            '20ft', '40ft', '45ft', '10ft', '18mm', '21mm', '1-3kw',

            # Brand names and proper nouns
            'kan-bud', 'claude', 'anthropic', 'replit', 'streamlit', 'poland', 'polski',
            'europe', 'europa', 'scandinavian', 'mediterranean', 'atlantic', 'baltic',
            'alpine', 'continental',

            # File formats and technical codes
            'json', 'xml', 'html', 'css', 'js', 'py', 'csv', 'zip', 'tar', 'gz',
            'http', 'https', 'url', 'ssl', 'tls', 'smtp', 'pop3', 'imap',

            # Common abbreviations
            'etc', 'e.g', 'i.e', 'vs', 'ex', 'max', 'min', 'std', 'opt', 'auto',
            'pro', 'plus', 'lite', 'basic', 'premium', 'standard',

            # Technical components
            'jacuzzi', 'bidet', 'email', 'e-mail', 'online', 'offline', 'backup',
            'server', 'client', 'admin', 'user', 'login', 'logout', 'password',

            # Container specific terms
            'container', 'kontener', 'conteneur', 'contenitore', 'behälter',
            'dd', 'hc', 'iso', 'teu', 'feu'
        }

        # Language-specific patterns to detect foreign language content
        self.language_patterns = {
            'en': {
                'articles': ['the', 'a', 'an'],
                'common_words': ['and', 'or', 'of', 'to', 'for', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during'],
                'indicators': ['ing$', 'tion$', 'sion$', 'ness$', 'ment$', 'able$', 'ible$']
            },
            'de': {
                'articles': ['der', 'die', 'das', 'den', 'dem', 'des', 'ein', 'eine', 'einen', 'einem', 'einer'],
                'common_words': ['und', 'oder', 'mit', 'für', 'von', 'zu', 'auf', 'in', 'an', 'bei', 'nach'],
                'indicators': ['ung$', 'keit$', 'heit$', 'schaft$', 'lich$', 'bar$', 'sam$']
            },
            'fr': {
                'articles': ['le', 'la', 'les', 'un', 'une', 'des', 'du', 'de'],
                'common_words': ['et', 'ou', 'avec', 'pour', 'de', 'à', 'sur', 'dans', 'par', 'sans'],
                'indicators': ['tion$', 'sion$', 'ment$', 'eur$', 'euse$', 'able$', 'ible$']
            },
            'es': {
                'articles': ['el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas'],
                'common_words': ['y', 'o', 'con', 'para', 'de', 'a', 'en', 'por', 'sin', 'sobre'],
                'indicators': ['ción$', 'sión$', 'miento$', 'ador$', 'adora$', 'able$', 'ible$']
            },
            'it': {
                'articles': ['il', 'la', 'lo', 'gli', 'le', 'un', 'una', 'uno'],
                'common_words': ['e', 'o', 'con', 'per', 'di', 'a', 'in', 'da', 'su', 'tra'],
                'indicators': ['zione$', 'sione$', 'mento$', 'atore$', 'atrice$', 'abile$', 'ibile$']
            },
            'pl': {
                'articles': [],  # Polish doesn't have articles
                'common_words': ['i', 'lub', 'z', 'dla', 'do', 'w', 'na', 'o', 'od', 'za', 'przez'],
                'indicators': ['acja$', 'enie$', 'ość$', 'nik$', 'owy$', 'owa$', 'owe$']
            },
            'cs': {
                'articles': [],  # Czech doesn't have articles
                'common_words': ['a', 'nebo', 's', 'pro', 'do', 'v', 'na', 'o', 'od', 'za', 'přes'],
                'indicators': ['ace$', 'ení$', 'ost$', 'ník$', 'ový$', 'ová$', 'ové$']
            },
            'hu': {
                'articles': ['a', 'az'],
                'common_words': ['és', 'vagy', 'vagy', 'számára', 'től', 'ban', 'ben', 'on', 'en', 'ön'],
                'indicators': ['ság$', 'ség$', 'ás$', 'és$', 'ó$', 'ő$', 'i$']
            },
            'nl': {
                'articles': ['de', 'het', 'een'],
                'common_words': ['en', 'of', 'met', 'voor', 'van', 'naar', 'in', 'op', 'bij', 'door'],
                'indicators': ['ing$', 'heid$', 'lijk$', 'baar$', 'isch$', 'tie$', 'sie$']
            },
            'sv': {
                'articles': ['en', 'ett', 'den', 'det'],
                'common_words': ['och', 'eller', 'med', 'för', 'av', 'till', 'i', 'på', 'vid', 'genom'],
                'indicators': ['ning$', 'het$', 'lig$', 'bar$', 'isk$', 'tion$', 'sion$']
            },
            'fi': {
                'articles': [],  # Finnish doesn't have articles
                'common_words': ['ja', 'tai', 'kanssa', 'varten', 'sisään', 'päälle', 'kautta', 'aikana'],
                'indicators': ['inen$', 'nen$', 'us$', 'ys$', 'la$', 'lä$', 'ssa$', 'ssä$']
            },
            'sk': {
                'articles': [],  # Slovak doesn't have articles
                'common_words': ['a', 'alebo', 's', 'pre', 'do', 'v', 'na', 'o', 'od', 'za', 'cez'],
                'indicators': ['ácia$', 'enie$', 'osť$', 'ník$', 'ový$', 'ová$', 'ové$']
            },
            'uk': {
                'articles': [],  # Ukrainian doesn't have articles
                'common_words': ['і', 'або', 'з', 'для', 'до', 'в', 'на', 'про', 'від', 'за', 'через'],
                'indicators': ['ація$', 'ення$', 'ість$', 'ник$', 'овий$', 'ова$', 'ове$']
            }
        }

    def is_worldwide_term(self, word: str) -> bool:
        """Check if a word is a worldwide technical term"""
        word_lower = word.lower().strip('.,!?:;()[]{}"\'-')
        return word_lower in self.worldwide_terms

    def is_low_severity_word(self, word: str) -> bool:
        """Check if a word should be considered low severity (single letters, short common words)"""
        # Single letters
        if len(word) == 1:
            return True

        # Very short words that are common across languages
        low_severity_words = {
            'a', 'an', 'i', 'o', 'u', 'e', 'de', 'da', 'do', 'la', 'le', 'il', 'el', 
            'un', 'en', 'et', 'ou', 'si', 'no', 'ne', 'on', 'is', 'as', 'at', 'be',
            'my', 'we', 'he', 'me', 'it', 'up', 'go', 'so', 'to', 'of', 'or', 'us',
            'am', 'if', 'in', 'ad', 'ab', 'ex', 'id', 'ok', 'tv', 'pc', 'cd', 'dvd',
            'na', 'con', 'des'
        }

        return word.lower() in low_severity_words

    def contains_foreign_language(self, text: str, target_lang: str) -> Tuple[bool, List[str]]:
        """Check if text contains words from foreign languages"""
        if not text or target_lang not in self.language_patterns:
            return False, []

        # Skip if it's clearly a technical string
        if any(tech in text.lower() for tech in ['€', '$', '%', 'http', 'www', '@', '.com', '.org']):
            return False, []

        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        foreign_words = []

        # Check for English words in non-English languages
        if target_lang != 'en':
            english_patterns = self.language_patterns['en']
            for word in words:
                if self.is_worldwide_term(word) or self.is_low_severity_word(word):
                    continue

                # Check for English articles and common words
                if word in english_patterns['articles'] or word in english_patterns['common_words']:
                    foreign_words.append(f"EN:{word}")

                # Check for English word endings
                for pattern in english_patterns['indicators']:
                    if re.search(pattern, word) and len(word) > 4:
                        if not any(re.search(target_pattern, word) for target_pattern in self.language_patterns[target_lang]['indicators']):
                            foreign_words.append(f"EN:{word}")

        # Check for other foreign languages
        for lang_code, patterns in self.language_patterns.items():
            if lang_code == target_lang or lang_code == 'en':
                continue

            for word in words:
                if self.is_worldwide_term(word) or self.is_low_severity_word(word):
                    continue

                if word in patterns['articles'] or word in patterns['common_words']:
                    foreign_words.append(f"{lang_code.upper()}:{word}")

        return len(foreign_words) > 0, foreign_words

    def scan_translation_object(self, obj, target_lang: str, path: str = "") -> List[Dict]:
        """Recursively scan translation object for foreign language content"""
        issues = []

        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                issues.extend(self.scan_translation_object(value, target_lang, new_path))

        elif isinstance(obj, str):
            has_foreign, foreign_words = self.contains_foreign_language(obj, target_lang)
            if has_foreign:
                # Determine severity based on word types
                non_low_severity_words = [w for w in foreign_words if not self.is_low_severity_word(w.split(':')[-1])]

                if len(non_low_severity_words) > 2:
                    severity = 'high'
                elif len(non_low_severity_words) > 0:
                    severity = 'medium'
                else:
                    severity = 'low'

                issues.append({
                    'path': path,
                    'text': obj,
                    'foreign_words': foreign_words,
                    'severity': severity
                })

        return issues

    def scan_language_file(self, lang_code: str) -> Dict:
        """Scan a single language file for purity"""
        filepath = os.path.join(self.locales_dir, f"{lang_code}.json")

        if not os.path.exists(filepath):
            return {'error': f"File not found: {filepath}"}

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return {'error': f"Error loading {filepath}: {e}"}

        issues = self.scan_translation_object(data, lang_code)

        return {
            'language': lang_code,
            'total_issues': len(issues),
            'high_severity': len([i for i in issues if i['severity'] == 'high']),
            'medium_severity': len([i for i in issues if i['severity'] == 'medium']),
            'low_severity': len([i for i in issues if i['severity'] == 'low']),
            'issues': issues,
            'significant_issues': [i for i in issues if i['severity'] in ['high', 'medium']]
        }

    def scan_all_languages(self) -> Dict:
        """Scan all language files"""
        if not os.path.exists(self.locales_dir):
            return {'error': f"Locales directory not found: {self.locales_dir}"}

        results = {}
        total_issues = 0
        significant_issues = 0

        for filename in sorted(os.listdir(self.locales_dir)):
            if filename.endswith('.json') and not filename.endswith('.backup'):
                lang_code = filename[:-5]
                if lang_code in ['en', 'pl']:  # Skip English and Polish as they are working fine
                    continue

                result = self.scan_language_file(lang_code)
                results[lang_code] = result

                if 'total_issues' in result:
                    total_issues += result['total_issues']
                    significant_issues += len(result.get('significant_issues', []))

        return {
            'summary': {
                'total_languages_scanned': len(results),
                'total_issues_found': total_issues,
                'significant_issues_found': significant_issues,
                'languages_with_issues': len([r for r in results.values() if r.get('total_issues', 0) > 0])
            },
            'results': results
        }

    def print_report(self, results: Dict):
        """Print a formatted report"""
        print("🔍 LANGUAGE PURITY SCANNER REPORT")
        print("=" * 60)

        if 'error' in results:
            print(f"❌ Error: {results['error']}")
            return

        summary = results['summary']
        print(f"📊 SUMMARY:")
        print(f"   Languages scanned: {summary['total_languages_scanned']}")
        print(f"   Total issues found: {summary['total_issues_found']}")
        print(f"   Significant issues: {summary['significant_issues_found']}")
        print(f"   Languages with issues: {summary['languages_with_issues']}")

        if summary['significant_issues_found'] == 0:
            if summary['total_issues_found'] > 0:
                print(f"\n✅ All languages are clean! {summary['total_issues_found']} low-severity issues (single letters/short words) were ignored.")
            else:
                print("\n✅ All languages are pure! No foreign language content detected.")
            return

        print(f"\n🔍 DETAILED RESULTS (High & Medium Severity Only):")
        print("-" * 50)

        for lang_code, result in results['results'].items():
            if 'error' in result:
                print(f"\n❌ {lang_code.upper()}: {result['error']}")
                continue

            significant_count = len(result['significant_issues'])

            if significant_count == 0:
                if result['total_issues'] > 0:
                    print(f"\n✅ {lang_code.upper()}: Clean ({result['total_issues']} low-severity issues ignored)")
                else:
                    print(f"\n✅ {lang_code.upper()}: Clean (no foreign content)")
                continue

            print(f"\n⚠️  {lang_code.upper()}: {significant_count} significant issues")
            print(f"   High severity: {result['high_severity']}")
            print(f"   Medium severity: {result['medium_severity']}")
            if result['low_severity'] > 0:
                print(f"   Low severity (ignored): {result['low_severity']}")

            # Show examples of significant issues only
            for i, issue in enumerate(result['significant_issues'][:5]):  # Show first 5 significant issues
                print(f"\n   📍 {issue['path']}")
                print(f"      Text: '{issue['text'][:80]}{'...' if len(issue['text']) > 80 else ''}'")
                print(f"      Foreign words: {', '.join(issue['foreign_words'])}")

            if len(result['significant_issues']) > 5:
                print(f"   ... and {len(result['significant_issues']) - 5} more significant issues")

        print(f"\n💡 RECOMMENDATIONS:")
        print("   • Review flagged translations for accuracy")
        print("   • Replace foreign language content with proper target language")
        print("   • Technical terms (HVAC, PDF, etc.) are acceptable")
        print("   • Single letters and short common words are now treated as low-severity")
        print("   • Focus on high and medium severity issues for translation quality")
        print("   • Consider professional translation review for high-severity issues")

def main():
    scanner = LanguagePurityScanner()
    results = scanner.scan_all_languages()
    scanner.print_report(results)

if __name__ == "__main__":
    main()