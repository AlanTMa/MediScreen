#!/usr/bin/env python3
"""
Test the date extraction functionality
"""

from voice_agent import ClinicalTrialVoiceAgent

def test_date_extraction():
    print("Testing date extraction functionality:")
    print("=" * 60)
    
    agent = ClinicalTrialVoiceAgent()
    
    # Test various date formats
    test_cases = [
        "ten sixteen",
        "October sixteen", 
        "October sixteenth",
        "the sixteenth of October",
        "the sixteenth of october",
        "10/16",
        "10 16",
        "november twenty fifth",
        "dec 15",
        "january first",
        "the first of january"
    ]
    
    for test_input in test_cases:
        print(f"\nTesting: '{test_input}'")
        extracted_date = agent._extract_date_from_speech(test_input)
        print(f"  Extracted: '{extracted_date}'")

if __name__ == "__main__":
    test_date_extraction()
