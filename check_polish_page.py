import trafilatura
import requests

def check_polish_translations():
    """Check what text is still in English on the Polish configurator page"""
    
    try:
        # Get the Polish version of the Container Configurator page
        url = "http://0.0.0.0:5000/Container_Configurator?language=pl"
        
        # Fetch the page content
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        
        if text:
            print("=== TEXT CONTENT FROM POLISH CONFIGURATOR PAGE ===")
            print(text)
            print("\n=== SEARCHING FOR ENGLISH TERMS ===")
            
            # Look for specific English terms that should be translated
            english_terms = [
                "Construction Material", "window_types", "plumbing_system", 
                "hvac_system", "electrical_system", "lighting", "Interior layout",
                "Fire systems", "Safety systems", "accessibility", "Exterior Cladding",
                "Paint Finish", "Additional Openings", "Type of transport", 
                "Office Equipment", "Appliances", "choose an option", "Choose an option",
                "Delivery zone", "Installation"
            ]
            
            found_english = []
            for term in english_terms:
                if term in text:
                    found_english.append(term)
            
            if found_english:
                print("ENGLISH TERMS FOUND:")
                for term in found_english:
                    print(f"- {term}")
            else:
                print("No obvious English terms found in the search list")
                
        else:
            print("Could not extract text from the page")
            
    except Exception as e:
        print(f"Error checking page: {e}")

if __name__ == "__main__":
    check_polish_translations()