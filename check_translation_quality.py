
#!/usr/bin/env python3
"""
Translation Quality Analysis Script
Provides comprehensive analysis of translation completeness and quality
"""

from utils.translation_quality_analyzer import TranslationQualityAnalyzer

def main():
    print("🔍 Starting comprehensive translation quality analysis...\n")
    
    analyzer = TranslationQualityAnalyzer()
    results = analyzer.run_comprehensive_analysis()
    print(results)

if __name__ == "__main__":
    main()
