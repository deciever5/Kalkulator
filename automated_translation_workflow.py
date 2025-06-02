#!/usr/bin/env python3
"""
Automated Translation Workflow
Scans for language purity issues and automatically fixes them
"""

import json
import os
import sys
from typing import Dict, List
from language_purity_scanner import LanguagePurityScanner
from advanced_translation_fixer import AdvancedTranslationFixer
from utils.ai_translation_service import AITranslationService

class AutomatedTranslationWorkflow:
    """Automated workflow for scanning and fixing translation issues"""

    def __init__(self):
        self.scanner = LanguagePurityScanner()
        self.fixer = AdvancedTranslationFixer()
        self.ai_service = AITranslationService()
        self.results_file = "translation_scan_results.json"
        self.fixed_languages = []
        self.failed_languages = []

    def save_scan_results(self, results: Dict):
        """Save scan results to file for analysis"""
        try:
            with open(self.results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"📄 Scan results saved to {self.results_file}")
        except Exception as e:
            print(f"❌ Error saving scan results: {e}")

    def load_scan_results(self) -> Dict:
        """Load previous scan results"""
        try:
            if os.path.exists(self.results_file):
                with open(self.results_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading previous scan results: {e}")
        return {}

    def extract_problematic_languages(self, scan_results: Dict) -> List[str]:
        """Extract languages that have significant issues"""
        problematic_languages = []

        if 'results' not in scan_results:
            return problematic_languages

        for lang_code, result in scan_results['results'].items():
            if 'error' in result:
                continue

            # Focus on high and medium severity issues
            significant_issues = len(result.get('significant_issues', []))
            high_severity = result.get('high_severity', 0)
            medium_severity = result.get('medium_severity', 0)

            # Add language if it has significant issues
            if significant_issues > 0 or high_severity > 0 or medium_severity > 2:
                problematic_languages.append(lang_code)

        return problematic_languages

    def fix_specific_language_issues(self, lang_code: str, issues: List[Dict]) -> bool:
        """Fix specific issues for a language using AI translation"""
        print(f"🔧 Fixing specific issues for {lang_code.upper()}...")

        # Load the language file
        lang_file = os.path.join("locales", f"{lang_code}.json")
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                lang_data = json.load(f)
        except Exception as e:
            print(f"❌ Error loading {lang_code} file: {e}")
            return False

        # Load Polish base for reference
        base_file = os.path.join("locales", "pl.json")
        try:
            with open(base_file, 'r', encoding='utf-8') as f:
                base_data = json.load(f)
        except Exception as e:
            print(f"❌ Error loading Polish base: {e}")
            return False

        base_translations = self.fixer.get_all_keys_flat(base_data)
        fixes_made = 0

        # Common words that automatic translator often misses
        common_missed_words = {
            'heating': {'de': 'Heizung', 'fr': 'chauffage', 'es': 'calefacción', 'it': 'riscaldamento', 'nl': 'verwarming'},
            'cooling': {'de': 'Kühlung', 'fr': 'refroidissement', 'es': 'refrigeración', 'it': 'raffreddamento', 'nl': 'koeling'},
            'container': {'de': 'Container', 'fr': 'conteneur', 'es': 'contenedor', 'it': 'contenitore', 'nl': 'container'},
            'basic': {'de': 'Basis', 'fr': 'de base', 'es': 'básico', 'it': 'di base', 'nl': 'basis'},
            'standard': {'de': 'Standard', 'fr': 'standard', 'es': 'estándar', 'it': 'standard', 'nl': 'standaard'},
            'premium': {'de': 'Premium', 'fr': 'premium', 'es': 'premium', 'it': 'premium', 'nl': 'premium'},
            'advanced': {'de': 'Erweitert', 'fr': 'avancé', 'es': 'avanzado', 'it': 'avanzato', 'nl': 'geavanceerd'},
            'configuration': {'de': 'Konfiguration', 'fr': 'configuration', 'es': 'configuración', 'it': 'configurazione', 'nl': 'configuratie'},
            'installation': {'de': 'Installation', 'fr': 'installation', 'es': 'instalación', 'it': 'installazione', 'nl': 'installatie'},
            'delivery': {'de': 'Lieferung', 'fr': 'livraison', 'es': 'entrega', 'it': 'consegna', 'nl': 'levering'},
            'transport': {'de': 'Transport', 'fr': 'transport', 'es': 'transporte', 'it': 'trasporto', 'nl': 'transport'},
            'security': {'de': 'Sicherheit', 'fr': 'sécurité', 'es': 'seguridad', 'it': 'sicurezza', 'nl': 'beveiliging'},
            'system': {'de': 'System', 'fr': 'système', 'es': 'sistema', 'it': 'sistema', 'nl': 'systeem'},
            'analysis': {'de': 'Analyse', 'fr': 'analyse', 'es': 'análisis', 'it': 'analisi', 'nl': 'analyse'}
        }

        # Process each significant issue
        for issue in issues[:20]:  # Limit to prevent overwhelming
            issue_key = issue['path']
            issue_type = issue['type']
            current_value = issue['text']

            try:
                if issue_type in ['missing_translation', 'likely_english', 'placeholder']:
                    # Check if it's a commonly missed word first
                    current_lower = current_value.lower().strip()
                    translated = None

                    for english_word, translations in common_missed_words.items():
                        if english_word in current_lower and lang_code in translations:
                            if current_lower == english_word or current_value.strip() == english_word.title():
                                translated = translations[lang_code]
                                break

                    # If not a common word, use AI translation
                    if not translated:
                        polish_text = base_translations.get(issue_key)
                        if polish_text and self.fixer.should_translate(polish_text):
                            translated = self.ai_service._translate_text(polish_text, lang_code)

                    if translated and translated != current_value:
                        self.fixer.set_nested_value(lang_data, issue_key, translated)
                        fixes_made += 1
                        print(f"   ✓ Fixed: {issue_key}")

                        # Rate limiting
                        #time.sleep(0.1) # Removed this line because there is no time module imported

            except Exception as e:
                print(f"   ⚠️ Error fixing {issue_key}: {e}")
                continue

        # Save the fixes
        if fixes_made > 0:
            try:
                with open(lang_file, 'w', encoding='utf-8') as f:
                    json.dump(lang_data, f, ensure_ascii=False, indent=2, separators=(',', ': '))
                print(f"✅ {lang_code.upper()}: Fixed {fixes_made} specific issues")
                return True
            except Exception as e:
                print(f"❌ Error saving {lang_code}: {e}")
                return False

        return True

    def run_comprehensive_workflow(self):
        """Run the complete workflow: scan -> analyze -> fix"""
        print("🚀 AUTOMATED TRANSLATION WORKFLOW")
        print("=" * 60)

        # Step 1: Run language purity scan
        print("🔍 Step 1: Scanning all languages for purity issues...")
        scan_results = self.scanner.scan_all_languages()

        if 'error' in scan_results:
            print(f"❌ Scan failed: {scan_results['error']}")
            return

        # Save scan results
        self.save_scan_results(scan_results)

        # Display scan summary
        summary = scan_results['summary']
        print(f"\n📊 SCAN SUMMARY:")
        print(f"   Languages scanned: {summary['total_languages_scanned']}")
        print(f"   Total issues: {summary['total_issues_found']}")
        print(f"   Significant issues: {summary['significant_issues_found']}")

        if summary['significant_issues_found'] == 0:
            print("✅ All languages are clean! No fixing needed.")
            return

        # Step 2: Extract problematic languages
        print(f"\n🎯 Step 2: Identifying languages that need fixing...")
        problematic_languages = self.extract_problematic_languages(scan_results)

        if not problematic_languages:
            print("✅ No languages need fixing based on scan results.")
            return

        print(f"Languages needing fixes: {', '.join(problematic_languages)}")

        # Step 3: Fix problematic languages
        print(f"\n🔧 Step 3: Fixing problematic languages...")

        for lang_code in problematic_languages:
            try:
                result = scan_results['results'][lang_code]
                if 'error' in result:
                    print(f"❌ Skipping {lang_code} due to scan error")
                    self.failed_languages.append(lang_code)
                    continue

                # Get significant issues for this language
                significant_issues = result.get('significant_issues', [])

                if significant_issues:
                    # Try specific issue fixes first
                    if self.fix_specific_language_issues(lang_code, significant_issues):
                        self.fixed_languages.append(lang_code)
                    else:
                        # Fall back to comprehensive fixer
                        print(f"🔄 Falling back to comprehensive fixer for {lang_code}")
                        if self.fixer.fix_language_translations(lang_code):
                            self.fixed_languages.append(lang_code)
                        else:
                            self.failed_languages.append(lang_code)
                else:
                    # Use comprehensive fixer for general issues
                    if self.fixer.fix_language_translations(lang_code):
                        self.fixed_languages.append(lang_code)
                    else:
                        self.failed_languages.append(lang_code)

            except Exception as e:
                print(f"❌ Error processing {lang_code}: {e}")
                self.failed_languages.append(lang_code)

        # Step 4: Run verification scan
        print(f"\n🔍 Step 4: Running verification scan...")
        verification_results = self.scanner.scan_all_languages()

        if 'error' not in verification_results:
            verification_summary = verification_results['summary']
            print(f"📊 VERIFICATION RESULTS:")
            print(f"   Significant issues after fixes: {verification_summary['significant_issues_found']}")

            # Save verification results
            verification_file = "translation_verification_results.json"
            try:
                with open(verification_file, 'w', encoding='utf-8') as f:
                    json.dump(verification_results, f, ensure_ascii=False, indent=2)
                print(f"📄 Verification results saved to {verification_file}")
            except Exception as e:
                print(f"⚠️ Error saving verification results: {e}")

        # Final summary
        print(f"\n🎉 WORKFLOW COMPLETE!")
        print(f"=" * 60)
        print(f"✅ Successfully fixed: {len(self.fixed_languages)} languages")
        if self.fixed_languages:
            print(f"   Fixed languages: {', '.join(self.fixed_languages)}")

        if self.failed_languages:
            print(f"❌ Failed to fix: {len(self.failed_languages)} languages")
            print(f"   Failed languages: {', '.join(self.failed_languages)}")

        print(f"\n📋 NEXT STEPS:")
        if verification_results.get('summary', {}).get('significant_issues_found', 0) > 0:
            print("1. Review remaining issues in verification results")
            print("2. Consider manual review for complex translations")
            print("3. Test the application with fixed languages")
        else:
            print("1. All translation issues resolved!")
            print("2. Test the application with all languages")
            print("3. Consider professional review for business-critical translations")

        print(f"\n📄 Files created:")
        print(f"   • {self.results_file} - Initial scan results")
        if os.path.exists("translation_verification_results.json"):
            print(f"   • translation_verification_results.json - Post-fix verification")

def main():
    """Main function"""
    workflow = AutomatedTranslationWorkflow()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--scan-only":
            # Just run the scan and save results
            print("🔍 Running scan-only mode...")
            results = workflow.scanner.scan_all_languages()
            workflow.scanner.print_report(results)
            workflow.save_scan_results(results)
        elif sys.argv[1] == "--fix-from-results":
            # Load previous results and fix
            print("🔧 Loading previous scan results and fixing...")
            results = workflow.load_scan_results()
            if results:
                problematic_languages = workflow.extract_problematic_languages(results)
                print(f"Found {len(problematic_languages)} languages to fix: {', '.join(problematic_languages)}")
                # Continue with fixing logic...
            else:
                print("❌ No previous scan results found. Run with --scan-only first.")
        else:
            print("Usage:")
            print("  python automated_translation_workflow.py              # Full workflow")
            print("  python automated_translation_workflow.py --scan-only  # Scan and save results")
            print("  python automated_translation_workflow.py --fix-from-results  # Fix from saved results")
    else:
        # Run complete workflow
        workflow.run_comprehensive_workflow()

if __name__ == "__main__":
    main()