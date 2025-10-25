#!/usr/bin/env python3
"""
Test the new 4-part phone number system
"""

from voice_agent import ClinicalTrialVoiceAgent

def test_new_phone_system():
    print("Testing new 4-part phone number system:")
    print("=" * 60)
    
    agent = ClinicalTrialVoiceAgent()
    
    print(f"Total questions: {len(agent.screening_questions)}")
    print("\nPhone number questions:")
    
    for i, question in enumerate(agent.screening_questions):
        if 'phone' in question['field']:
            print(f"{i+1}. {question['question']}")
            print(f"   Field: {question['field']}")
    
    print("\nTesting full conversation flow:")
    print("-" * 40)
    
    # Start conversation
    greeting = agent.process_incoming_call()
    print(f"1. Greeting: {greeting[:50]}...")
    
    # Simulate patient responses
    responses = [
        "I am 35 years old",
        "I have diabetes", 
        "I take metformin",
        "No, I am not pregnant",
        "No, I don't have severe conditions",
        "five five five",      # Area code
        "one two three",       # Middle digits
        "four five",           # First 2 of last 4
        "six seven"            # Last 2 digits
    ]
    
    for i, response in enumerate(responses):
        print(f"\n{i+2}. Patient says: '{response}'")
        ai_response = agent.process_patient_response(response)
        print(f"   AI responds: {ai_response}")
        
        # Check phone number parts after phone questions start
        if i >= 5:
            print(f"   Area code: {agent.patient_info.phone_area_code}")
            print(f"   Middle: {agent.patient_info.phone_middle}")
            print(f"   First 2 of last 4: {agent.patient_info.phone_last_two_first}")
            print(f"   Last 2: {agent.patient_info.phone_last_two_second}")
            print(f"   Full contact: {agent.patient_info.contact_info}")
    
    # Get final summary
    print(f"\nFinal conversation summary:")
    summary = agent.get_conversation_summary()
    print(f"   Contact info: {summary['patient_info']['contact_info']}")
    print(f"   Phone parts: {summary['patient_info']['phone_area_code']}-{summary['patient_info']['phone_middle']}-{summary['patient_info']['phone_last_four']}")

if __name__ == "__main__":
    test_new_phone_system()
