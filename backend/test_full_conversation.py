#!/usr/bin/env python3
"""
Test full conversation flow with phone number collection
"""

from voice_agent import ClinicalTrialVoiceAgent

def test_full_conversation():
    print("Testing full conversation flow:")
    print("=" * 50)
    
    agent = ClinicalTrialVoiceAgent()
    
    # Start conversation
    print("1. Initial greeting:")
    greeting = agent.process_incoming_call()
    print(f"   {greeting}")
    
    # Simulate patient responses
    responses = [
        "I am 35 years old",
        "I have diabetes",
        "I take metformin",
        "No, I am not pregnant",
        "No, I don't have severe conditions",
        "five five five",  # Area code
        "one two three",   # Middle digits
        "four five six seven"  # Last four
    ]
    
    for i, response in enumerate(responses):
        print(f"\n{i+2}. Patient says: '{response}'")
        ai_response = agent.process_patient_response(response)
        print(f"   AI responds: {ai_response}")
        
        # Check phone number parts after each response
        if i >= 5:  # After phone number questions start
            print(f"   Phone area code: {agent.patient_info.phone_area_code}")
            print(f"   Phone middle: {agent.patient_info.phone_middle}")
            print(f"   Phone last four: {agent.patient_info.phone_last_four}")
            print(f"   Full contact info: {agent.patient_info.contact_info}")
    
    # Get final summary
    print(f"\nFinal conversation summary:")
    summary = agent.get_conversation_summary()
    print(f"   Contact info: {summary['patient_info']['contact_info']}")
    print(f"   Phone parts: {summary['patient_info']['phone_area_code']}-{summary['patient_info']['phone_middle']}-{summary['patient_info']['phone_last_four']}")

if __name__ == "__main__":
    test_full_conversation()
