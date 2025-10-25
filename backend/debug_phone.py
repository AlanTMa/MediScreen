#!/usr/bin/env python3
"""
Debug phone number extraction
"""

from voice_agent import ClinicalTrialVoiceAgent

def debug_phone_extraction():
    print("Debugging phone number extraction:")
    print("=" * 50)
    
    agent = ClinicalTrialVoiceAgent()
    
    # Test cases
    test_cases = [
        "four five six seven",
        "four five six seven eight",
        "4 5 6 7",
        "4567",
        "four five six",
        "one two three four"
    ]
    
    for test_input in test_cases:
        print(f"\nInput: '{test_input}'")
        digits = agent._extract_digits_from_speech(test_input)
        print(f"Extracted digits: {digits}")
        print(f"Length: {len(digits)}")
        
        if len(digits) >= 4:
            last_four = ''.join(digits[:4])
            print(f"Last 4 digits: {last_four}")
        else:
            print("Not enough digits for last 4")
        
        if len(digits) >= 3:
            first_three = ''.join(digits[:3])
            print(f"First 3 digits: {first_three}")
        else:
            print("Not enough digits for first 3")

if __name__ == "__main__":
    debug_phone_extraction()
