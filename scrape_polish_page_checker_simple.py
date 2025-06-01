
import requests
import time
import json
import re
from typing import Dict, Set
from bs4 import BeautifulSoup

class SimplePolishPageChecker:
    def __init__(self):
        self.base_url = "http://0.0.0.0:5000"
        self.polish_url = f"{self.base_url}/Container_Configurator?language=pl"

    def check_app_accessibility(self):
        """Check if the Streamlit app is accessible and running"""
        try:
            print(f"🔍 Checking if Streamlit app is accessible at {self.base_url}")
            
            # Try to reach the base app
            response = requests.get(self.base_url, timeout=10)
            
            if "streamlit" in response.text.lower():
                print("✅ Streamlit app is running")
                
                # Check if it's the JavaScript loading message
                if "enable JavaScript" in response.text:
                    print("⚠️  App requires JavaScript - this is a single-page application")
                    print("💡 To properly test Polish translations, you need to:")
                    print("   1. Open the app in a browser: http://0.0.0.0:5000")
                    print("   2. Set language to Polish in the language selector")
                    print("   3. Navigate to Container Configurator")
                    print("   4. Manually check for English text")
                    return False
                else:
                    print("✅ App content is loading properly")
                    return True
            else:
                print("❌ No Streamlit app detected")
                return False
                
        except requests.RequestException as e:
            print(f"❌ Could not reach app: {e}")
            return False

    def provide_manual_testing_guide(self):
        """Provide a guide for manual testing"""
        print("\n" + "="*60)
        print("📋 MANUAL TESTING GUIDE FOR POLISH TRANSLATIONS")
        print("="*60)
        print()
        print("Since this is a JavaScript-rendered Streamlit app, here's how to test:")
        print()
        print("1. 🌐 Open in browser: http://0.0.0.0:5000")
        print("2. 🇵🇱 Change language to Polish using the language selector")
        print("3. 📦 Go to 'Container Configurator' page")
        print("4. 👀 Look for these English terms that should be in Polish:")
        print()
        
        terms_to_check = [
            "Construction Material", "window_types", "plumbing_system",
            "hvac_system", "electrical_system", "Interior layout",
            "Fire systems", "Safety systems", "Exterior Cladding", 
            "Paint Finish", "Additional Openings", "flooring",
            "lighting", "accessibility", "Choose an option",
            "Office Equipment", "Appliances", "Delivery zone"
        ]
        
        for i, term in enumerate(terms_to_check, 1):
            print(f"   {i:2d}. {term}")
        
        print()
        print("5. ✅ Check dropdown menus - they should show 'Wybierz opcję' not 'Choose an option'")
        print("6. 🔍 Look for any form labels or buttons in English")
        print()
        print("Common issues to look for:")
        print("• Dropdown placeholders showing 'Choose an option' instead of 'Wybierz opcję'")
        print("• Section headers in English (should be Polish)")
        print("• Button text in English")
        print("• Form field labels in English")
        print()
        print("💡 If you find English text, check the locales/pl.json file")
        print("   and make sure the translation key exists and is correct.")

def main():
    print("🚀 Simple Polish Page Checker")
    print("Checking if we can access the Streamlit app...")
    
    checker = SimplePolishPageChecker()
    
    # Check if app is accessible
    if not checker.check_app_accessibility():
        checker.provide_manual_testing_guide()
        return
    
    print("✅ App is accessible! You can now test manually or use browser automation.")

if __name__ == "__main__":
    main()
