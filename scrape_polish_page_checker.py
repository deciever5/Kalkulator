
import requests
from bs4 import BeautifulSoup
import re
import json
from typing import List, Dict, Set
import time

class PolishPageChecker:
    def __init__(self):
        self.base_url = "http://0.0.0.0:5000"
        self.polish_url = f"{self.base_url}/Container_Configurator?language=pl"
        
        # Common English words that should be translated in Polish context
        self.english_indicators = {
            # Technical terms that should be in Polish
            'construction', 'material', 'window_types', 'plumbing_system', 
            'hvac_system', 'electrical_system', 'lighting', 'interior', 'layout',
            'fire', 'systems', 'safety', 'accessibility', 'exterior', 'cladding',
            'paint', 'finish', 'additional', 'openings', 'delivery', 'zone',
            'transport', 'type', 'installation', 'office', 'equipment', 
            'appliances', 'flooring', 'insulation', 'package',
            
            # Form elements
            'choose', 'option', 'select', 'please', 'none', 'basic', 'standard',
            'premium', 'advanced', 'professional', 'industrial', 'commercial',
            
            # Common UI elements
            'submit', 'cancel', 'save', 'configuration', 'estimate', 'quote',
            'generate', 'calculate', 'analyze', 'upload', 'download',
            
            # Container specific
            'container', 'shipping', 'freight', 'cargo', 'steel', 'aluminum',
            'composite', 'residential', 'storage', 'workshop', 'retail',
            'medical', 'laboratory', 'office space', 'technical',
            
            # HVAC and technical
            'ventilation', 'heating', 'cooling', 'climate', 'temperature',
            'humidity', 'pressure', 'thermal', 'insulation', 'soundproof',
            
            # Common dropdown placeholders
            'choose an option', 'select option', 'please select'
        }
        
        # Polish words that are expected (to avoid false positives)
        self.polish_words = {
            'kontener', 'kontenery', 'biuro', 'biurowy', 'mieszkalne', 'magazyn',
            'warsztat', 'handel', 'restauracja', 'medyczne', 'laboratorium',
            'standardowy', 'podstawowy', 'premium', 'luksusowy', 'wybierz',
            'opcję', 'konfiguracja', 'wycena', 'systemy', 'instalacje',
            'elektryczny', 'hydrauliczny', 'oświetlenie', 'wentylacja',
            'ogrzewanie', 'chłodzenie', 'izolacja', 'wykończenie', 'podłogi',
            'okna', 'drzwi', 'bezpieczeństwo', 'przeciwpożarowe', 'dostępność',
            'transport', 'dostawa', 'montaż', 'wyposażenie', 'sprzęt'
        }

    def scrape_page(self) -> Dict:
        """Scrape the Polish configurator page"""
        try:
            print(f"🔍 Scraping Polish page: {self.polish_url}")
            
            # Wait a moment to ensure page is ready
            time.sleep(2)
            
            response = requests.get(self.polish_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract different types of content
            content = {
                'title': soup.find('title').get_text() if soup.find('title') else '',
                'headings': [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
                'labels': [label.get_text().strip() for label in soup.find_all('label')],
                'buttons': [btn.get_text().strip() for btn in soup.find_all('button')],
                'select_options': [],
                'input_placeholders': [],
                'all_text': soup.get_text(),
                'form_elements': []
            }
            
            # Extract select options
            for select in soup.find_all('select'):
                for option in select.find_all('option'):
                    text = option.get_text().strip()
                    if text:
                        content['select_options'].append(text)
            
            # Extract input placeholders
            for input_elem in soup.find_all('input'):
                placeholder = input_elem.get('placeholder', '')
                if placeholder:
                    content['input_placeholders'].append(placeholder)
            
            # Extract form elements with data-testid (Streamlit specific)
            for elem in soup.find_all(attrs={'data-testid': True}):
                text = elem.get_text().strip()
                if text and len(text) < 200:  # Avoid very long texts
                    content['form_elements'].append(text)
            
            return content
            
        except requests.RequestException as e:
            print(f"❌ Error scraping page: {e}")
            return {}
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return {}

    def is_english_word(self, word: str) -> bool:
        """Check if a word appears to be English"""
        word_lower = word.lower().strip()
        
        # Skip very short words (might be abbreviations)
        if len(word_lower) < 3:
            return False
        
        # Skip if it's a known Polish word
        if word_lower in self.polish_words:
            return False
        
        # Check against English indicators
        if word_lower in self.english_indicators:
            return True
        
        # Check for English patterns
        english_patterns = [
            r'ing$',  # -ing endings
            r'tion$', # -tion endings
            r'ment$', # -ment endings
            r'^choose',
            r'^select',
            r'^please',
            r'system$',
            r'type$',
            r'level$'
        ]
        
        for pattern in english_patterns:
            if re.search(pattern, word_lower):
                return True
        
        return False

    def analyze_content(self, content: Dict) -> Dict:
        """Analyze scraped content for English words"""
        findings = {
            'english_words': set(),
            'suspicious_phrases': set(),
            'section_analysis': {},
            'statistics': {}
        }
        
        # Analyze each content section
        sections = ['title', 'headings', 'labels', 'buttons', 'select_options', 'input_placeholders', 'form_elements']
        
        for section in sections:
            if section in content:
                section_english = set()
                section_items = content[section] if isinstance(content[section], list) else [content[section]]
                
                for item in section_items:
                    if not item or not isinstance(item, str):
                        continue
                    
                    # Check whole phrases first
                    item_lower = item.lower().strip()
                    
                    # Check for common English phrases
                    english_phrases = [
                        'choose an option', 'select option', 'please select',
                        'construction material', 'window types', 'electrical system',
                        'plumbing system', 'hvac system', 'fire systems',
                        'safety systems', 'interior layout', 'exterior cladding',
                        'paint finish', 'additional openings', 'delivery zone',
                        'office equipment', 'choose option'
                    ]
                    
                    for phrase in english_phrases:
                        if phrase in item_lower:
                            findings['suspicious_phrases'].add(f"{section}: '{item}'")
                    
                    # Check individual words
                    words = re.findall(r'\b\w+\b', item)
                    for word in words:
                        if self.is_english_word(word):
                            findings['english_words'].add(word)
                            section_english.add(f"'{word}' in '{item}'")
                
                if section_english:
                    findings['section_analysis'][section] = list(section_english)
        
        # Calculate statistics
        total_words = len(re.findall(r'\b\w+\b', content.get('all_text', '')))
        findings['statistics'] = {
            'total_words_found': total_words,
            'english_words_count': len(findings['english_words']),
            'suspicious_phrases_count': len(findings['suspicious_phrases']),
            'sections_with_issues': len([s for s in findings['section_analysis'] if findings['section_analysis'][s]])
        }
        
        return findings

    def generate_report(self, findings: Dict) -> str:
        """Generate a detailed report"""
        report = []
        report.append("=" * 80)
        report.append("🇵🇱 POLISH PAGE LANGUAGE VERIFICATION REPORT")
        report.append("=" * 80)
        report.append(f"📅 Checked at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"🌐 URL: {self.polish_url}")
        report.append("")
        
        # Statistics
        stats = findings['statistics']
        report.append("📊 SUMMARY STATISTICS")
        report.append("-" * 40)
        report.append(f"Total words analyzed: {stats['total_words_found']}")
        report.append(f"English words found: {stats['english_words_count']}")
        report.append(f"Suspicious phrases: {stats['suspicious_phrases_count']}")
        report.append(f"Sections with issues: {stats['sections_with_issues']}")
        report.append("")
        
        # English words found
        if findings['english_words']:
            report.append("🚨 ENGLISH WORDS DETECTED")
            report.append("-" * 40)
            for word in sorted(findings['english_words']):
                report.append(f"  • {word}")
            report.append("")
        
        # Suspicious phrases
        if findings['suspicious_phrases']:
            report.append("⚠️  SUSPICIOUS ENGLISH PHRASES")
            report.append("-" * 40)
            for phrase in sorted(findings['suspicious_phrases']):
                report.append(f"  • {phrase}")
            report.append("")
        
        # Section-by-section analysis
        if findings['section_analysis']:
            report.append("🔍 DETAILED SECTION ANALYSIS")
            report.append("-" * 40)
            for section, issues in findings['section_analysis'].items():
                if issues:
                    report.append(f"\n📍 {section.upper()}:")
                    for issue in issues[:10]:  # Limit to 10 per section
                        report.append(f"   {issue}")
                    if len(issues) > 10:
                        report.append(f"   ... and {len(issues) - 10} more")
        
        # Recommendations
        report.append("\n💡 RECOMMENDATIONS")
        report.append("-" * 40)
        if findings['english_words'] or findings['suspicious_phrases']:
            report.append("1. Check translation keys in locales/pl.json")
            report.append("2. Verify form element translations")
            report.append("3. Update missing Polish translations")
            report.append("4. Run translation validation scripts")
        else:
            report.append("✅ Page appears to be properly translated to Polish!")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)

    def save_report(self, report: str, findings: Dict):
        """Save report to files"""
        # Save text report
        with open('polish_page_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save detailed findings as JSON
        findings_serializable = {
            'english_words': list(findings['english_words']),
            'suspicious_phrases': list(findings['suspicious_phrases']),
            'section_analysis': findings['section_analysis'],
            'statistics': findings['statistics'],
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'url': self.polish_url
        }
        
        with open('polish_page_findings.json', 'w', encoding='utf-8') as f:
            json.dump(findings_serializable, f, indent=2, ensure_ascii=False)

def main():
    print("🚀 Starting Polish Page Language Checker...")
    
    checker = PolishPageChecker()
    
    # Scrape the page
    content = checker.scrape_page()
    if not content:
        print("❌ Failed to scrape page content")
        return
    
    print("✅ Page scraped successfully")
    
    # Analyze content
    print("🔍 Analyzing content for English words...")
    findings = checker.analyze_content(content)
    
    # Generate and display report
    report = checker.generate_report(findings)
    print(report)
    
    # Save reports
    checker.save_report(report, findings)
    print(f"\n💾 Reports saved:")
    print(f"   📄 Text report: polish_page_report.txt")
    print(f"   📋 JSON data: polish_page_findings.json")

if __name__ == "__main__":
    main()
