#!/usr/bin/env python3
"""
Test the reverted 3-part phone number system
"""

from voice_agent import ClinicalTrialVoiceAgent

def test_reverted_system():
    print("Testing reverted 3-part phone number system:")
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
        "four five six seven"  # Last 4 digits
    ]
    
    for i, response in enumerate(responses):
        print(f"\n{i+2}. Patient says: '{response}'")
        ai_response = agent.process_patient_response(response)
        print(f"   AI responds: {ai_response}")
        
        # Check phone number parts after phone questions start
        if i >= 5:
            print(f"   Area code: {agent.patient_info.phone_area_code}")
            print(f"   Middle: {agent.patient_info.phone_middle}")
            print(f"   Last four: {agent.patient_info.phone_last_four}")
            print(f"   Full contact: {agent.patient_info.contact_info}")
    
    # Get final summary
    print(f"\nFinal conversation summary:")
    summary = agent.get_conversation_summary()
    print(f"   Contact info: {summary['patient_info']['contact_info']}")
    print(f"   Phone parts: {summary['patient_info']['phone_area_code']}-{summary['patient_info']['phone_middle']}-{summary['patient_info']['phone_last_four']}")

if __name__ == "__main__":
    test_reverted_system()
