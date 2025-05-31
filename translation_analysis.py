#!/usr/bin/env python3
"""
Translation Analysis Report Generator
Analyzes all translation files for completeness, consistency, and quality
"""

import json
import os
from typing import Dict, List, Set, Any

def load_json_file(filepath: str) -> Dict[str, Any]:
    """Load JSON translation file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def get_all_keys(data: Dict[str, Any], prefix: str = "") -> Set[str]:
    """Recursively get all keys from nested dictionary"""
    keys = set()
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        keys.add(full_key)
        if isinstance(value, dict):
            keys.update(get_all_keys(value, full_key))
    return keys

def get_nested_value(data: Dict[str, Any], key_path: str) -> str:
    """Get value from nested dictionary using dot notation"""
    keys = key_path.split('.')
    current = data
    try:
        for key in keys:
            current = current[key]
        return str(current) if current is not None else ""
    except (KeyError, TypeError):
        return ""

def detect_auto_translations(value: str) -> bool:
    """Detect if a translation appears to be auto-generated or placeholder"""
    auto_indicators = [
        'auto_', 'placeholder_', 'temp_', 'TODO:', 'FIXME:',
        'lorem ipsum', 'sample text', 'example text',
        'translation needed', 'add translation',
        '[TRANSLATE]', '[TODO]', 'XXX', 'YYY'
    ]
    value_lower = value.lower()
    return any(indicator in value_lower for indicator in auto_indicators)

def analyze_translations():
    """Analyze all translation files"""
    print("=== TRANSLATION ANALYSIS REPORT ===\n")
    
    # Language files to analyze
    locales_dir = "locales"
    if not os.path.exists(locales_dir):
        print("Error: locales directory not found")
        return
    
    # Load all translation files
    translations = {}
    file_stats = {}
    
    for filename in os.listdir(locales_dir):
        if not filename.endswith('.json'):
            continue
            
        lang_code = filename[:-5]
        filepath = os.path.join(locales_dir, filename)
        
        print(f"Loading {lang_code}...")
        translations[lang_code] = load_json_file(filepath)
        
        if translations[lang_code]:
            all_keys = get_all_keys(translations[lang_code])
            file_stats[lang_code] = {
                'total_keys': len(all_keys),
                'top_level_keys': len(translations[lang_code]),
                'file_size': os.path.getsize(filepath),
                'all_keys': all_keys
            }
    
    if not translations:
        print("No translation files found")
        return
    
    print(f"\n=== FILE STATISTICS ===")
    print(f"{'Language':<12} {'Top-Level':<12} {'Total Keys':<12} {'File Size':<12}")
    print("-" * 50)
    
    for lang, stats in sorted(file_stats.items()):
        print(f"{lang:<12} {stats['top_level_keys']:<12} {stats['total_keys']:<12} {stats['file_size']:<12}")
    
    # Find the most complete language (master reference)
    master_lang = max(file_stats.keys(), key=lambda x: file_stats[x]['total_keys'])
    master_keys = file_stats[master_lang]['all_keys']
    
    print(f"\nMaster reference language: {master_lang} ({len(master_keys)} keys)")
    
    # Compare completeness
    print(f"\n=== TRANSLATION COMPLETENESS ===")
    print(f"{'Language':<12} {'Missing Keys':<15} {'Extra Keys':<15} {'Completeness':<15}")
    print("-" * 60)
    
    completeness_report = {}
    
    for lang, stats in sorted(file_stats.items()):
        lang_keys = stats['all_keys']
        missing_keys = master_keys - lang_keys
        extra_keys = lang_keys - master_keys
        completeness = (len(lang_keys) / len(master_keys)) * 100 if master_keys else 0
        
        completeness_report[lang] = {
            'missing_keys': missing_keys,
            'extra_keys': extra_keys,
            'completeness': completeness
        }
        
        print(f"{lang:<12} {len(missing_keys):<15} {len(extra_keys):<15} {completeness:<14.1f}%")
    
    # Check for auto-generated translations
    print(f"\n=== AUTO-GENERATED TRANSLATION DETECTION ===")
    auto_translation_issues = {}
    
    for lang, data in translations.items():
        auto_count = 0
        auto_examples = []
        
        def check_values(obj, path=""):
            nonlocal auto_count, auto_examples
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    check_values(value, new_path)
            elif isinstance(obj, str):
                if detect_auto_translations(obj):
                    auto_count += 1
                    if len(auto_examples) < 5:  # Limit examples
                        auto_examples.append(f"{path}: {obj[:50]}...")
        
        check_values(data)
        
        if auto_count > 0:
            auto_translation_issues[lang] = {
                'count': auto_count,
                'examples': auto_examples
            }
    
    if auto_translation_issues:
        for lang, issues in auto_translation_issues.items():
            print(f"\n{lang}: {issues['count']} potential auto-generated translations")
            for example in issues['examples']:
                print(f"  - {example}")
    else:
        print("No obvious auto-generated translations detected")
    
    # Key consistency analysis
    print(f"\n=== KEY CONSISTENCY ANALYSIS ===")
    
    # Find keys that exist in some languages but not others
    all_possible_keys = set()
    for stats in file_stats.values():
        all_possible_keys.update(stats['all_keys'])
    
    inconsistent_keys = []
    for key in all_possible_keys:
        languages_with_key = []
        for lang, stats in file_stats.items():
            if key in stats['all_keys']:
                languages_with_key.append(lang)
        
        if len(languages_with_key) < len(file_stats) and len(languages_with_key) > 1:
            inconsistent_keys.append((key, languages_with_key))
    
    if inconsistent_keys:
        print(f"Found {len(inconsistent_keys)} keys with inconsistent coverage:")
        for key, langs in inconsistent_keys[:10]:  # Show first 10
            print(f"  {key}: present in {', '.join(langs)}")
        if len(inconsistent_keys) > 10:
            print(f"  ... and {len(inconsistent_keys) - 10} more")
    else:
        print("All keys have consistent coverage across languages")
    
    # Missing keys details for incomplete languages
    print(f"\n=== MISSING KEYS DETAILS ===")
    for lang in sorted(completeness_report.keys()):
        report = completeness_report[lang]
        if report['missing_keys'] and lang != master_lang:
            print(f"\n{lang} missing {len(report['missing_keys'])} keys:")
            missing_list = sorted(list(report['missing_keys']))
            for key in missing_list[:15]:  # Show first 15
                print(f"  - {key}")
            if len(missing_list) > 15:
                print(f"  ... and {len(missing_list) - 15} more")
    
    # Quality assessment
    print(f"\n=== QUALITY ASSESSMENT ===")
    
    complete_languages = []
    partial_languages = []
    incomplete_languages = []
    
    for lang, report in completeness_report.items():
        if report['completeness'] >= 95:
            complete_languages.append(lang)
        elif report['completeness'] >= 80:
            partial_languages.append(lang)
        else:
            incomplete_languages.append(lang)
    
    print(f"Complete languages (95%+): {', '.join(complete_languages) if complete_languages else 'None'}")
    print(f"Partial languages (80-95%): {', '.join(partial_languages) if partial_languages else 'None'}")
    print(f"Incomplete languages (<80%): {', '.join(incomplete_languages) if incomplete_languages else 'None'}")
    
    # Recommendations
    print(f"\n=== RECOMMENDATIONS ===")
    if incomplete_languages:
        print(f"1. Complete translations for: {', '.join(incomplete_languages)}")
    if auto_translation_issues:
        print(f"2. Review auto-generated translations in: {', '.join(auto_translation_issues.keys())}")
    if inconsistent_keys:
        print(f"3. Resolve {len(inconsistent_keys)} keys with inconsistent coverage")
    
    print(f"\n=== SUMMARY ===")
    print(f"Total languages analyzed: {len(translations)}")
    print(f"Master language: {master_lang}")
    print(f"Total unique keys: {len(all_possible_keys)}")
    print(f"Languages ready for production: {', '.join(complete_languages) if complete_languages else 'None'}")

if __name__ == "__main__":
    analyze_translations()