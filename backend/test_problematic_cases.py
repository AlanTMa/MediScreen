#!/usr/bin/env python3
"""
Test problematic cases for phone number recognition
"""

from voice_agent import ClinicalTrialVoiceAgent

def test_problematic_cases():
    print("Testing problematic cases for last 4 digits:")
    print("=" * 60)
    
    agent = ClinicalTrialVoiceAgent()
    
    # Test cases that might fail
    test_cases = [
        "four five six",  # Only 3 digits
        "four five",      # Only 2 digits  
        "four",           # Only 1 digit
        "four five six seven eight",  # Too many digits
        "um four five six seven",     # With filler words
        "four five six seven um",     # Filler at end
        "4 5 6 7",        # Actual digits
        "4567",           # All together
        "forty five sixty seven",     # Different pronunciation
        "four five six seven eight nine",  # Way too many
    ]
    
    for test_input in test_cases:
        print(f"\nTesting: '{test_input}'")
        digits = agent._extract_digits_from_speech(test_input)
        print(f"  Extracted: {digits} (length: {len(digits)})")
        
        if len(digits) >= 4:
            last_four = ''.join(digits[:4])
            print(f"  Last 4: {last_four} [OK]")
        elif len(digits) > 0:
            partial = ''.join(digits)
            print(f"  Partial: {partial} (need {4-len(digits)} more)")
        else:
            print(f"  No digits found [FAILED]")

if __name__ == "__main__":
    test_problematic_cases()
