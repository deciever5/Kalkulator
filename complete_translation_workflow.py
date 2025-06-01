
#!/usr/bin/env python3
"""
Complete Translation Workflow
Check and fix all translations using Polish as base
"""

import sys
import os

def main():
    """Main workflow function"""
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
    else:
        action = "check"
    
    print("🌍 COMPLETE TRANSLATION WORKFLOW")
    print("Using Polish as base language reference")
    print("="*50)
    
    if action == "check":
        print("🔍 Running comprehensive translation check...")
        os.system("python comprehensive_translation_checker.py")
        
    elif action == "fix":
        print("🔧 Running translation fixes...")
        os.system("python advanced_translation_fixer.py")
        print("\n🔍 Re-checking after fixes...")
        os.system("python comprehensive_translation_checker.py")
        
    elif action == "full":
        print("🔍 Step 1: Initial check...")
        os.system("python comprehensive_translation_checker.py")
        
        print("\n" + "="*50)
        print("🔧 Step 2: Fixing issues...")
        os.system("python advanced_translation_fixer.py")
        
        print("\n" + "="*50)
        print("🔍 Step 3: Final verification...")
        os.system("python comprehensive_translation_checker.py")
        
    else:
        print("Usage:")
        print("  python complete_translation_workflow.py check  # Check only")
        print("  python complete_translation_workflow.py fix    # Fix and re-check")
        print("  python complete_translation_workflow.py full   # Complete workflow")

if __name__ == "__main__":
    main()
