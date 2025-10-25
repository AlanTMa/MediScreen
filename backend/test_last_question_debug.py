#!/usr/bin/env python3
"""
Debug the last question specifically
"""

from voice_agent import ClinicalTrialVoiceAgent

def test_last_question_debug():
    print("Debugging the last question specifically:")
    print("=" * 60)
    
    agent = ClinicalTrialVoiceAgent()
    
    print(f"Total questions: {len(agent.screening_questions)}")
    print(f"Last question index: {len(agent.screening_questions) - 1}")
    print(f"Last question: {agent.screening_questions[-1]['question']}")
    print(f"Last question field: {agent.screening_questions[-1]['field']}")
    
    print("\n" + "="*60)
    print("Simulating conversation up to last question:")
    print("="*60)
    
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
        print(f"   BEFORE - Question index: {agent.current_question_index}")
        ai_response = agent.process_patient_response(response)
        print(f"   AFTER - Question index: {agent.current_question_index}")
        print(f"   AI responds: {ai_response}")
        
        # Check if we're at the last question
        if agent.current_question_index == len(agent.screening_questions) - 1:
            print(f"   *** WE ARE NOW AT THE LAST QUESTION (index {agent.current_question_index}) ***")
            print(f"   Last question: {agent.screening_questions[agent.current_question_index]['question']}")
            print(f"   Last question field: {agent.screening_questions[agent.current_question_index]['field']}")
    
    print(f"\n" + "="*60)
    print("NOW TESTING THE LAST QUESTION:")
    print("="*60)
    
    # Now test the last question
    last_response = "four five six seven"
    print(f"\nFinal response: '{last_response}'")
    print(f"BEFORE - Question index: {agent.current_question_index}")
    print(f"BEFORE - Total questions: {len(agent.screening_questions)}")
    print(f"BEFORE - Index < Total: {agent.current_question_index < len(agent.screening_questions)}")
    
    final_response = agent.process_patient_response(last_response)
    
    print(f"AFTER - Question index: {agent.current_question_index}")
    print(f"AFTER - Total questions: {len(agent.screening_questions)}")
    print(f"AFTER - Index < Total: {agent.current_question_index < len(agent.screening_questions)}")
    print(f"Final AI response: {final_response}")
    
    print(f"\nFinal phone number: {agent.patient_info.contact_info}")
    print(f"Area code: {agent.patient_info.phone_area_code}")
    print(f"Middle: {agent.patient_info.phone_middle}")
    print(f"Last four: {agent.patient_info.phone_last_four}")

if __name__ == "__main__":
    test_last_question_debug()
