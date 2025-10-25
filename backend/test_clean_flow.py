#!/usr/bin/env python3
"""
Test the clean flow: greeting -> first question -> normal flow
"""

from voice_agent import ClinicalTrialVoiceAgent

def test_clean_flow():
    print("Testing clean conversation flow:")
    print("=" * 60)
    
    agent = ClinicalTrialVoiceAgent()
    
    # Start conversation
    greeting = agent.process_incoming_call()
    print(f"1. Greeting: {greeting}")
    print(f"   Current stage: {agent.conversation_stage}")
    print(f"   Current index: {agent.current_question_index}")
    
    # Simulate patient responses
    responses = [
        "Yes, I'm ready",      # Response to greeting
        "I am 35 years old",   # First question
        "I have diabetes", 
        "I take metformin",
        "No, I am not pregnant",
        "No, I don't have severe conditions",
        "five five five",      # Area code
        "one two three",       # Middle digits
        "four five six seven"  # Last 4 digits
    ]
    
    for i, response in enumerate(responses):
        print(f"\n{i+2}. Patient says: '{response}'")
        print(f"   BEFORE - Stage: {agent.conversation_stage}, Index: {agent.current_question_index}")
        
        ai_response = agent.process_patient_response(response)
        
        print(f"   AFTER - Stage: {agent.conversation_stage}, Index: {agent.current_question_index}")
        print(f"   AI responds: {ai_response}")
        
        # Check phone number parts after phone questions start
        if i >= 6:
            print(f"   Phone parts:")
            print(f"     - Area code: {agent.patient_info.phone_area_code}")
            print(f"     - Middle: {agent.patient_info.phone_middle}")
            print(f"     - Last four: {agent.patient_info.phone_last_four}")
            print(f"     - Full contact: {agent.patient_info.contact_info}")

if __name__ == "__main__":
    test_clean_flow()
