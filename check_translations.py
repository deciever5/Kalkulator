
#!/usr/bin/env python3
"""
Translation Quality Checker
Uses Polish as base language to check quality of all other translations
"""

from utils.ai_translation_service import check_translation_quality_all_languages

if __name__ == "__main__":
    print("🚀 Starting comprehensive translation quality check...")
    print("📚 Using Polish (pl) as base reference language")
    print("=" * 70)
    
    results = check_translation_quality_all_languages()
    
    print("\n" + "=" * 70)
    print("✅ Translation quality check completed!")
    print("💡 Review the results above and run fixes as needed.")
