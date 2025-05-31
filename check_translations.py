
#!/usr/bin/env python3
"""
Translation Checker Script
Checks for missing translations and optionally fixes them using AI
"""

import sys
from utils.ai_translation_service import AITranslationService

def main():
    service = AITranslationService()
    
    if len(sys.argv) > 1 and sys.argv[1] == "fix":
        print("🔧 Fixing missing translations...")
        service.translate_all_languages()
    else:
        print("🔍 Checking translation completeness...")
        service.check_translation_quality()
        print("\nTo fix missing translations, run: python check_translations.py fix")

if __name__ == "__main__":
    main()
