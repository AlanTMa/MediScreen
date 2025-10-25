#!/usr/bin/env python3
"""
Test to see what exception is being thrown on the last question
"""

from voice_agent import ClinicalTrialVoiceAgent

def test_exception_debug():
    print("Testing for exceptions on the last question:")
    print("=" * 60)
    
    agent = ClinicalTrialVoiceAgent()
    
    # Start conversation
    greeting = agent.process_incoming_call()
    print(f"1. Greeting: {greeting[:50]}...")
    
    # Simulate responses up to the last question
    responses = [
        "I am 35 years old",
        "I have diabetes", 
        "I take metformin",
        "No, I am not pregnant",
        "No, I don't have severe conditions",
        "five five five",      # Area code
        "one two three",       # Middle digits
    ]
    
    for i, response in enumerate(responses):
        print(f"\n{i+2}. Patient says: '{response}'")
        ai_response = agent.process_patient_response(response)
        print(f"   AI responds: {ai_response}")
    
    print(f"\n" + "="*60)
    print("NOW TESTING THE LAST QUESTION:")
    print("="*60)
    
    # Now test the last question with various inputs
    test_inputs = [
        "four five six seven",
        "4 5 6 7",
        "4567",
        "four five six seven eight"
    ]
    
    for test_input in test_inputs:
        print(f"\nTesting input: '{test_input}'")
        try:
            ai_response = agent.process_patient_response(test_input)
            print(f"   AI responds: {ai_response}")
            print(f"   Phone number: {agent.patient_info.contact_info}")
        except Exception as e:
            print(f"   EXCEPTION: {e}")
            print(f"   Exception type: {type(e)}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_exception_debug()
