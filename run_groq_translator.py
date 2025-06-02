
#!/usr/bin/env python3
"""
Run Groq Translator with Reserve API Key Support
This script uses the enhanced GroqService with failover API keys for translation
"""

import os
import sys
import asyncio
from utils.groq_service import GroqService, TranslationQualityChecker

def main():
    print("🤖 Starting Groq Translator with Reserve API Support...")
    
    # Check for API keys
    primary_key = os.environ.get('GROQ_API_KEY')
    reserve_key = os.environ.get('GROQ_RESERVE_API_KEY')
    reserve_key_2 = os.environ.get('GROQ_RESERVE_API_KEY_2')
    
    print(f"Primary API Key: {'✅ Available' if primary_key else '❌ Missing'}")
    print(f"Reserve API Key: {'✅ Available' if reserve_key else '❌ Missing'}")
    print(f"Reserve API Key 2: {'✅ Available' if reserve_key_2 else '❌ Missing'}")
    
    # Initialize Groq service
    groq_service = GroqService()
    
    if not groq_service.api_keys:
        print("❌ No API keys found! Please set your environment variables:")
        print("   - GROQ_API_KEY (primary)")
        print("   - GROQ_RESERVE_API_KEY (backup)")
        print("   - GROQ_RESERVE_API_KEY_2 (additional backup)")
        return
    
    print(f"📡 Initialized with {len(groq_service.api_keys)} API keys")
    
    # Test translation functionality
    test_translations()
    
    # Run translation quality checker
    run_translation_quality_check(groq_service)

def test_translations():
    """Test basic translation functionality"""
    print("\n🔄 Testing basic translation functionality...")
    
    try:
        from utils.ai_translation_service import AITranslationService
        
        service = AITranslationService()
        
        # Test translation for a few languages
        test_languages = ['en', 'de', 'fr', 'es']
        
        for lang in test_languages:
            print(f"Testing {lang.upper()}...")
            success = service.translate_missing_keys(lang, 'pl')
            if success:
                print(f"✅ {lang.upper()}: Translation completed")
            else:
                print(f"❌ {lang.upper()}: Translation failed")
                
    except Exception as e:
        print(f"❌ Translation test failed: {e}")

def run_translation_quality_check(groq_service):
    """Run translation quality check using Groq"""
    print("\n🔍 Running translation quality check...")
    
    try:
        checker = TranslationQualityChecker(groq_service)
        
        # Test with a sample text
        test_text = "Witamy w systemie konfiguracji kontenerów KAN-BUD"
        
        async def check_quality():
            results = await checker.check_translation_quality(test_text)
            
            print("\n📊 Translation Quality Results:")
            for lang, result in results.items():
                if 'error' in result:
                    print(f"❌ {lang.upper()}: {result['error']}")
                else:
                    quality_score = result.get('quality_score', 0)
                    print(f"📈 {lang.upper()}: Quality Score {quality_score:.2f}")
                    if 'translation' in result:
                        print(f"   Translation: {result['translation'][:50]}...")
        
        # Run async quality check
        asyncio.run(check_quality())
        
    except Exception as e:
        print(f"❌ Quality check failed: {e}")

def show_usage():
    """Show usage information"""
    print("""
🚀 Groq Translator Usage:

1. Basic translation of missing keys:
   python run_groq_translator.py

2. Check translation quality:
   python run_groq_translator.py --check-quality

3. Translate all languages:
   python run_groq_translator.py --translate-all

Environment Variables Required:
- GROQ_API_KEY (primary)
- GROQ_RESERVE_API_KEY (backup)
- GROQ_RESERVE_API_KEY_2 (additional backup)
    """)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            show_usage()
        elif sys.argv[1] == "--check-quality":
            groq_service = GroqService()
            run_translation_quality_check(groq_service)
        elif sys.argv[1] == "--translate-all":
            from utils.ai_translation_service import AITranslationService
            service = AITranslationService()
            service.translate_all_languages()
        else:
            print("Unknown option. Use --help for usage information.")
    else:
        main()
