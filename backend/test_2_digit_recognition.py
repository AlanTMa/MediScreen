#!/usr/bin/env python3
"""
Test 2-digit recognition for the new system
"""

from voice_agent import ClinicalTrialVoiceAgent

def test_2_digit_recognition():
    print("Testing 2-digit recognition:")
    print("=" * 50)
    
    agent = ClinicalTrialVoiceAgent()
    
    # Test cases for 2 digits
    test_cases = [
        "four five",
        "4 5", 
        "45",
        "forty five",
        "um four five",
        "four five um",
        "one two",
        "1 2",
        "12",
        "six seven",
        "6 7",
        "67",
        "sixty seven"
    ]
    
    for test_input in test_cases:
        print(f"\nTesting: '{test_input}'")
        digits = agent._extract_digits_from_speech(test_input)
        print(f"  Extracted: {digits} (length: {len(digits)})")
        
        if len(digits) >= 2:
            two_digits = ''.join(digits[:2])
            print(f"  First 2: {two_digits} [OK]")
        elif len(digits) == 1:
            one_digit = ''.join(digits)
            print(f"  Only 1: {one_digit} (need 1 more)")
        else:
            print(f"  No digits found [FAILED]")

if __name__ == "__main__":
    test_2_digit_recognition()
