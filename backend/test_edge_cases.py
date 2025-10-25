#!/usr/bin/env python3
"""
Test edge cases for phone number recognition
"""

from voice_agent import ClinicalTrialVoiceAgent

def test_edge_cases():
    print("Testing edge cases for phone number recognition:")
    print("=" * 60)
    
    agent = ClinicalTrialVoiceAgent()
    
    # Test cases that might be problematic
    test_cases = [
        ("Area code: 'five five five'", "five five five"),
        ("Middle: 'one two three'", "one two three"),
        ("Last 4: 'four five six seven'", "four five six seven"),
        ("Last 4: '4 5 6 7'", "4 5 6 7"),
        ("Last 4: '4567'", "4567"),
        ("Last 4: 'forty five sixty seven'", "forty five sixty seven"),
        ("Last 4: 'um four five six seven'", "um four five six seven"),
        ("Last 4: 'four five six seven eight'", "four five six seven eight"),
    ]
    
    for description, test_input in test_cases:
        print(f"\n{description}")
        print(f"Input: '{test_input}'")
        digits = agent._extract_digits_from_speech(test_input)
        print(f"Extracted: {digits} (length: {len(digits)})")
        
        if len(digits) >= 4:
            result = ''.join(digits[:4])
            print(f"Result: {result} [OK]")
        elif len(digits) >= 3:
            result = ''.join(digits[:3])
            print(f"Result: {result} (3 digits) [OK]")
        else:
            print(f"Result: {''.join(digits)} (partial) [PARTIAL]")

if __name__ == "__main__":
    test_edge_cases()
