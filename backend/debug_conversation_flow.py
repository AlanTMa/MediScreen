#!/usr/bin/env python3
"""
Debug the conversation flow to find why last 2 digits fail
"""

from voice_agent import ClinicalTrialVoiceAgent

def debug_conversation_flow():
    print("Debugging conversation flow:")
    print("=" * 60)
    
    agent = ClinicalTrialVoiceAgent()
    
    print(f"Total questions: {len(agent.screening_questions)}")
    print("\nAll questions:")
    for i, question in enumerate(agent.screening_questions):
        print(f"{i+1}. {question['question']}")
        print(f"   Field: {question['field']}")
    
    print("\n" + "="*60)
    print("Testing conversation flow step by step:")
    print("="*60)
    
    # Start conversation
    greeting = agent.process_incoming_call()
    print(f"1. Greeting: {greeting[:50]}...")
    print(f"   Current question index: {agent.current_question_index}")
    
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
        print(f"   BEFORE - Question index: {agent.current_question_index}")
        print(f"   BEFORE - Current field: {agent.screening_questions[agent.current_question_index]['field'] if agent.current_question_index < len(agent.screening_questions) else 'NONE'}")
        
        ai_response = agent.process_patient_response(response)
        
        print(f"   AFTER - Question index: {agent.current_question_index}")
        print(f"   AFTER - Current field: {agent.screening_questions[agent.current_question_index]['field'] if agent.current_question_index < len(agent.screening_questions) else 'NONE'}")
        print(f"   AI responds: {ai_response}")
        
        # Check phone number parts after phone questions start
        if i >= 5:
            print(f"   Area code: {agent.patient_info.phone_area_code}")
            print(f"   Middle: {agent.patient_info.phone_middle}")
            print(f"   First 2 of last 4: {getattr(agent.patient_info, 'phone_last_two_first', 'None')}")
            print(f"   Last 2: {getattr(agent.patient_info, 'phone_last_two_second', 'None')}")
            print(f"   Full contact: {agent.patient_info.contact_info}")

if __name__ == "__main__":
    debug_conversation_flow()
