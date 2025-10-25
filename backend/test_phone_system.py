#!/usr/bin/env python3
"""
Test the 3-part phone number system
"""

from voice_agent import ClinicalTrialVoiceAgent

def test_phone_system():
    print("Testing 3-part phone number system:")
    print("=" * 50)
    
    agent = ClinicalTrialVoiceAgent()
    
    print(f"Total questions: {len(agent.screening_questions)}")
    print("\nPhone number questions:")
    
    for i, question in enumerate(agent.screening_questions):
        if 'phone' in question['field']:
            print(f"{i+1}. {question['question']}")
            print(f"   Field: {question['field']}")
    
    print("\nTesting phone number extraction:")
    
    # Test area code
    print("\n1. Testing area code extraction:")
    test_text = "five five five"
    print(f"Input: '{test_text}'")
    digits = agent._extract_digits_from_speech(test_text)
    if len(digits) >= 3:
        area_code = ''.join(digits[:3])
        print(f"Extracted: {area_code}")
    else:
        print("No digits found")
    
    # Test middle digits
    print("\n2. Testing middle digits extraction:")
    test_text = "one two three"
    print(f"Input: '{test_text}'")
    digits = agent._extract_digits_from_speech(test_text)
    if len(digits) >= 3:
        middle = ''.join(digits[:3])
        print(f"Extracted: {middle}")
    else:
        print("No digits found")
    
    # Test last four
    print("\n3. Testing last four extraction:")
    test_text = "four five six seven"
    print(f"Input: '{test_text}'")
    digits = agent._extract_digits_from_speech(test_text)
    if len(digits) >= 4:
        last_four = ''.join(digits[:4])
        print(f"Extracted: {last_four}")
    else:
        print("No digits found")
    
    # Test with actual digits
    print("\n4. Testing with actual digits:")
    test_text = "555 123 4567"
    print(f"Input: '{test_text}'")
    digits = agent._extract_digits_from_speech(test_text)
    print(f"All digits found: {digits}")
    if len(digits) >= 10:
        full_phone = f"{''.join(digits[:3])}-{''.join(digits[3:6])}-{''.join(digits[6:10])}"
        print(f"Full phone: {full_phone}")
    
    print("\n" + "=" * 50)
    print("Phone number system ready!")

if __name__ == "__main__":
    test_phone_system()
