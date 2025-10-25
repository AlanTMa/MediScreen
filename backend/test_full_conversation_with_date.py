#!/usr/bin/env python3
"""
Test the full conversation flow with the new date question
"""

from voice_agent import ClinicalTrialVoiceAgent

def test_full_conversation_with_date():
    print("Testing full conversation flow with date question:")
    print("=" * 60)
    
    agent = ClinicalTrialVoiceAgent()
    
    print(f"Total questions: {len(agent.screening_questions)}")
    print("\nAll questions:")
    for i, question in enumerate(agent.screening_questions):
        print(f"{i+1}. {question['question']}")
        print(f"   Field: {question['field']}")
    
    print("\n" + "="*60)
    print("Testing full conversation flow:")
    print("="*60)
    
    # Start conversation
    greeting = agent.process_incoming_call()
    print(f"1. Greeting: {greeting}")
    
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
        "four five six seven", # Last 4 digits
        "October sixteenth"    # Availability date
    ]
    
    for i, response in enumerate(responses):
        print(f"\n{i+2}. Patient says: '{response}'")
        ai_response = agent.process_patient_response(response)
        print(f"   AI responds: {ai_response}")
        
        # Check phone number parts after phone questions start
        if i >= 6:
            print(f"   Phone parts:")
            print(f"     - Area code: {agent.patient_info.phone_area_code}")
            print(f"     - Middle: {agent.patient_info.phone_middle}")
            print(f"     - Last four: {agent.patient_info.phone_last_four}")
            print(f"     - Full contact: {agent.patient_info.contact_info}")
        
        # Check availability date
        if i >= 9:
            print(f"   Availability date: {agent.patient_info.availability_date}")
    
    # Get final summary
    print(f"\nFinal conversation summary:")
    summary = agent.get_conversation_summary()
    print(f"   Contact info: {summary['patient_info']['contact_info']}")
    print(f"   Availability date: {summary['patient_info']['availability_date']}")
    print(f"   Eligible: {summary['eligible']}")

if __name__ == "__main__":
    test_full_conversation_with_date()
