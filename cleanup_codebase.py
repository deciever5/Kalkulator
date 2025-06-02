#!/usr/bin/env python3
"""
Codebase Cleanup Script
Removes unused imports, variables, and obsolete translation keys
"""

import os
import re
import ast
import json
from pathlib import Path

def find_unused_imports(file_path):
    """Find unused imports in a Python file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the AST
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []
    
    # Find all imports
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                for alias in node.names:
                    imports.append(f"{node.module}.{alias.name}")
    
    # Find unused imports by checking if they're referenced
    unused = []
    for imp in imports:
        if imp not in content.replace(f"import {imp}", ""):
            unused.append(imp)
    
    return unused

def find_unused_variables(file_path):
    """Find potentially unused variables"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    unused_patterns = [
        r'(\w+)_options\s*=.*\]',  # Hardcoded option lists
        r'(\w+)_list\s*=.*\]',    # Lists that might be unused
    ]
    
    potentially_unused = []
    for i, line in enumerate(lines):
        for pattern in unused_patterns:
            match = re.search(pattern, line)
            if match:
                var_name = match.group(1)
                # Check if variable is used elsewhere in the file
                file_content = ''.join(lines)
                if file_content.count(var_name) == 1:  # Only defined, never used
                    potentially_unused.append((i+1, var_name, line.strip()))
    
    return potentially_unused

def find_obsolete_translation_keys():
    """Find translation keys that are no longer referenced in code"""
    # Get all Python files
    py_files = []
    for root, dirs, files in os.walk('.'):
        # Skip cache and hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    
    # Find all t('...') calls
    used_keys = set()
    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find t('key') patterns
            matches = re.findall(r"t\(['\"]([^'\"]+)['\"]\)", content)
            used_keys.update(matches)
        except Exception:
            continue
    
    # Load translation files and find unused keys
    obsolete_keys = {}
    locales_dir = Path('locales')
    if locales_dir.exists():
        for lang_file in locales_dir.glob('*.json'):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    translations = json.load(f)
                
                # Flatten nested keys
                flat_keys = set()
                def flatten_keys(obj, prefix=''):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            full_key = f"{prefix}.{key}" if prefix else key
                            if isinstance(value, dict):
                                flatten_keys(value, full_key)
                            else:
                                flat_keys.add(full_key)
                
                flatten_keys(translations)
                
                # Find keys not used in code
                unused = flat_keys - used_keys
                if unused:
                    obsolete_keys[lang_file.name] = list(unused)
                    
            except Exception as e:
                print(f"Error processing {lang_file}: {e}")
    
    return obsolete_keys

def main():
    """Main cleanup function"""
    print("🧹 Starting codebase cleanup...")
    
    # Find Python files
    py_files = []
    for root, dirs, files in os.walk('.'):
        # Skip cache and hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for file in files:
            if file.endswith('.py') and not file.startswith('cleanup_'):
                py_files.append(os.path.join(root, file))
    
    print(f"\n📋 Analyzing {len(py_files)} Python files...")
    
    # Check for unused imports
    print("\n🔍 Checking for unused imports:")
    for py_file in py_files:
        try:
            unused = find_unused_imports(py_file)
            if unused:
                print(f"  📄 {py_file}: {', '.join(unused)}")
        except Exception as e:
            print(f"  ⚠️  Error analyzing {py_file}: {e}")
    
    # Check for unused variables
    print("\n🔍 Checking for potentially unused variables:")
    for py_file in py_files:
        try:
            unused = find_unused_variables(py_file)
            if unused:
                print(f"  📄 {py_file}:")
                for line_num, var_name, line in unused:
                    print(f"    Line {line_num}: {var_name} - {line}")
        except Exception as e:
            print(f"  ⚠️  Error analyzing {py_file}: {e}")
    
    # Check for obsolete translation keys
    print("\n🔍 Checking for obsolete translation keys:")
    obsolete = find_obsolete_translation_keys()
    if obsolete:
        for lang_file, keys in obsolete.items():
            if len(keys) > 10:  # Only show if many unused keys
                print(f"  📄 {lang_file}: {len(keys)} potentially unused keys")
            elif keys:
                print(f"  📄 {lang_file}: {', '.join(keys[:5])}{'...' if len(keys) > 5 else ''}")
    else:
        print("  ✅ No obsolete translation keys found")
    
    print("\n✨ Cleanup analysis complete!")
    print("\n💡 Recommendations:")
    print("  1. Review and remove unused imports manually")
    print("  2. Consolidate duplicate option lists into reusable functions")
    print("  3. Remove obsolete translation keys after verification")
    print("  4. Consider using a linter like flake8 for ongoing maintenance")

if __name__ == "__main__":
    main()