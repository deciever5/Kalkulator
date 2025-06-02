#!/usr/bin/env python3
"""
Advanced Translation Key Analyzer
Combines static code analysis with runtime tracking to identify truly unused translation keys
"""

import os
import re
import json
import ast
from pathlib import Path
from typing import Dict, Set, List, Tuple

class TranslationKeyAnalyzer:
    def __init__(self):
        self.used_keys = set()
        self.dynamic_patterns = set()
        self.all_translation_keys = {}
        self.runtime_used_keys = set()
        
    def scan_python_files_for_translation_keys(self) -> Set[str]:
        """Scan all Python files for t('key') patterns"""
        used_keys = set()
        dynamic_patterns = set()
        
        # Get all Python files
        py_files = []
        for root, dirs, files in os.walk('.'):
            # Skip cache and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            for file in files:
                if file.endswith('.py'):
                    py_files.append(os.path.join(root, file))
        
        print(f"Scanning {len(py_files)} Python files for translation key usage...")
        
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Pattern 1: Direct t('key') calls
                direct_matches = re.findall(r"t\(['\"]([^'\"]+)['\"]\)", content)
                used_keys.update(direct_matches)
                
                # Pattern 2: Dynamic key construction t(f'{variable}.something')
                dynamic_matches = re.findall(r"t\(f['\"][^'\"]*\{[^}]+\}[^'\"]*['\"]\)", content)
                dynamic_patterns.update(dynamic_matches)
                
                # Pattern 3: Variable-based keys t(some_variable)
                var_matches = re.findall(r"t\(([a-zA-Z_][a-zA-Z0-9_]*)\)", content)
                for var in var_matches:
                    if not var.startswith(("'", '"')):
                        dynamic_patterns.add(f"VARIABLE: {var} in {py_file}")
                
                # Pattern 4: Keys built with + concatenation
                concat_matches = re.findall(r"t\(['\"]([^'\"]+)['\"][\s]*\+", content)
                for match in concat_matches:
                    dynamic_patterns.add(f"CONCAT_BASE: {match}")
                
            except Exception as e:
                print(f"Error scanning {py_file}: {e}")
        
        self.used_keys = used_keys
        self.dynamic_patterns = dynamic_patterns
        return used_keys
    
    def load_all_translation_files(self) -> Dict[str, Set[str]]:
        """Load all translation files and extract their keys"""
        all_keys = {}
        locales_dir = Path('locales')
        
        if not locales_dir.exists():
            print("No locales directory found")
            return {}
        
        for lang_file in locales_dir.glob('*.json'):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    translations = json.load(f)
                
                # Flatten nested keys
                flat_keys = set()
                self._flatten_keys(translations, flat_keys)
                all_keys[lang_file.stem] = flat_keys
                
            except Exception as e:
                print(f"Error loading {lang_file}: {e}")
        
        self.all_translation_keys = all_keys
        return all_keys
    
    def _flatten_keys(self, obj, flat_keys, prefix=''):
        """Recursively flatten nested dictionary keys"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                full_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    self._flatten_keys(value, flat_keys, full_key)
                else:
                    flat_keys.add(full_key)
    
    def analyze_unused_keys(self) -> Dict[str, List[str]]:
        """Find potentially unused keys in each language"""
        unused_by_language = {}
        
        for language, all_keys in self.all_translation_keys.items():
            # Find keys that aren't directly used
            potentially_unused = all_keys - self.used_keys
            
            # Filter out keys that might be used dynamically
            truly_unused = []
            for key in potentially_unused:
                is_likely_used = False
                
                # Check if key matches dynamic patterns
                for pattern in self.dynamic_patterns:
                    if "CONCAT_BASE:" in pattern:
                        base = pattern.replace("CONCAT_BASE: ", "")
                        if key.startswith(base):
                            is_likely_used = True
                            break
                
                # Check for common dynamic usage patterns
                key_parts = key.split('.')
                for part in key_parts:
                    # Check if any part of the key is used in dynamic contexts
                    if any(part in str(p) for p in self.dynamic_patterns):
                        is_likely_used = True
                        break
                
                if not is_likely_used:
                    truly_unused.append(key)
            
            unused_by_language[language] = truly_unused
        
        return unused_by_language
    
    def generate_runtime_tracker_code(self) -> str:
        """Generate code to add to translations.py for runtime tracking"""
        tracker_code = '''
# Add this to your translations.py file to track runtime key usage

import json
from pathlib import Path

_RUNTIME_USED_KEYS = set()

def track_translation_usage(key: str):
    """Track which translation keys are actually used at runtime"""
    _RUNTIME_USED_KEYS.add(key)
    
    # Save to file periodically (every 100 new keys)
    if len(_RUNTIME_USED_KEYS) % 100 == 0:
        save_runtime_usage()

def save_runtime_usage():
    """Save runtime usage data to file"""
    try:
        with open('runtime_translation_usage.json', 'w') as f:
            json.dump(list(_RUNTIME_USED_KEYS), f, indent=2)
    except Exception:
        pass  # Fail silently to not break the app

# Modify your existing t() function to include tracking:
# def t(key, default=None, **kwargs):
#     track_translation_usage(key)  # Add this line
#     # ... rest of your existing t() function code
'''
        return tracker_code
    
    def create_detailed_report(self) -> str:
        """Create a comprehensive analysis report"""
        report = []
        report.append("🔍 TRANSLATION KEY ANALYSIS REPORT")
        report.append("=" * 50)
        
        # Summary
        total_used = len(self.used_keys)
        total_dynamic = len(self.dynamic_patterns)
        report.append(f"\n📊 SUMMARY:")
        report.append(f"  Direct translation calls found: {total_used}")
        report.append(f"  Dynamic patterns detected: {total_dynamic}")
        
        # Used keys sample
        report.append(f"\n✅ DIRECTLY USED KEYS (sample of {min(20, len(self.used_keys))}):")
        for key in sorted(list(self.used_keys))[:20]:
            report.append(f"  - {key}")
        if len(self.used_keys) > 20:
            report.append(f"  ... and {len(self.used_keys) - 20} more")
        
        # Dynamic patterns
        if self.dynamic_patterns:
            report.append(f"\n🔄 DYNAMIC USAGE PATTERNS:")
            for pattern in sorted(self.dynamic_patterns):
                report.append(f"  - {pattern}")
        
        # Unused keys by language
        unused_by_lang = self.analyze_unused_keys()
        report.append(f"\n❌ POTENTIALLY UNUSED KEYS BY LANGUAGE:")
        for language, unused_keys in unused_by_lang.items():
            report.append(f"\n  {language.upper()}: {len(unused_keys)} potentially unused keys")
            if len(unused_keys) <= 10:
                for key in unused_keys:
                    report.append(f"    - {key}")
            else:
                for key in unused_keys[:5]:
                    report.append(f"    - {key}")
                report.append(f"    ... and {len(unused_keys) - 5} more")
        
        # Recommendations
        report.append(f"\n💡 RECOMMENDATIONS:")
        report.append(f"  1. Review dynamic patterns - some unused keys might be accessed dynamically")
        report.append(f"  2. Add runtime tracking to translations.py to get accurate usage data")
        report.append(f"  3. Test thoroughly before removing any keys")
        report.append(f"  4. Start by removing keys that are clearly obsolete (old feature names, etc.)")
        
        return "\n".join(report)
    
    def export_unused_keys_for_review(self, output_file: str = "unused_translation_keys.json"):
        """Export unused keys for manual review"""
        unused_by_lang = self.analyze_unused_keys()
        
        review_data = {
            "analysis_summary": {
                "total_used_keys": len(self.used_keys),
                "dynamic_patterns_found": len(self.dynamic_patterns),
                "languages_analyzed": list(self.all_translation_keys.keys())
            },
            "unused_keys_by_language": unused_by_lang,
            "dynamic_patterns": list(self.dynamic_patterns),
            "sample_used_keys": list(sorted(self.used_keys))[:50]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(review_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Unused keys analysis exported to: {output_file}")

def main():
    """Run the complete translation key analysis"""
    print("🔍 Starting Advanced Translation Key Analysis...")
    
    analyzer = TranslationKeyAnalyzer()
    
    # Step 1: Scan code for used keys
    used_keys = analyzer.scan_python_files_for_translation_keys()
    print(f"✅ Found {len(used_keys)} directly used translation keys")
    
    # Step 2: Load all translation files
    all_keys = analyzer.load_all_translation_files()
    total_keys = sum(len(keys) for keys in all_keys.values())
    print(f"✅ Loaded {total_keys} total translation keys from {len(all_keys)} languages")
    
    # Step 3: Generate detailed report
    report = analyzer.create_detailed_report()
    print("\n" + report)
    
    # Step 4: Export for manual review
    analyzer.export_unused_keys_for_review()
    
    # Step 5: Generate runtime tracker code
    print(f"\n🔧 RUNTIME TRACKING CODE:")
    print("To get more accurate data, add runtime tracking to your translations.py:")
    print(analyzer.generate_runtime_tracker_code())

if __name__ == "__main__":
    main()