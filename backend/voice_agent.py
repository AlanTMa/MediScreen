"""
AI Voice Agent for Clinical Trial Pre-Screening
Manages conversation flow and screening logic
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PatientInfo:
    """Patient information collected during screening"""
    age: Optional[int] = None
    medical_conditions: List[str] = None
    medications: List[str] = None
    pregnant: Optional[bool] = None
    severe_conditions: Optional[bool] = None
    contact_info: Optional[str] = None
    phone_area_code: Optional[str] = None
    phone_middle: Optional[str] = None
    phone_last_four: Optional[str] = None
    phone_last_two_first: Optional[str] = None
    phone_last_two_second: Optional[str] = None

class ClinicalTrialVoiceAgent:
    """
    AI Voice Agent specialized for clinical trial patient pre-screening
    """
    
    def __init__(self):
        self.conversation_stage = "greeting"
        self.patient_info = PatientInfo()
        self.screening_questions = self._initialize_screening_questions()
        self.current_question_index = 0
        self.conversation_log = []
        
        # Clinical trial context
        self.trial_name = "Clinical Research Study"
        self.trial_description = "A research study to evaluate a new treatment for medical conditions"
        
    def _initialize_screening_questions(self) -> List[Dict[str, str]]:
        """Initialize screening questions for clinical trial"""
        return [
            {
                "question": "What is your age?",
                "field": "age",
                "type": "number"
            },
            {
                "question": "Have you been diagnosed with any medical conditions?",
                "field": "medical_conditions",
                "type": "list"
            },
            {
                "question": "Are you currently taking any medications?",
                "field": "medications",
                "type": "list"
            },
            {
                "question": "Are you currently pregnant or nursing?",
                "field": "pregnant",
                "type": "boolean"
            },
            {
                "question": "Do you have any severe medical conditions that require ongoing treatment?",
                "field": "severe_conditions",
                "type": "boolean"
            },
            {
                "question": "What is the best phone number to reach you for follow-up? Please say the first 3 digits of your area code.",
                "field": "phone_area_code",
                "type": "text"
            },
            {
                "question": "Now please say the next 3 digits of your phone number.",
                "field": "phone_middle",
                "type": "text"
            },
            {
                "question": "Finally, please say the last 4 digits of your phone number.",
                "field": "phone_last_four",
                "type": "text"
            }
        ]
    
    def process_incoming_call(self) -> str:
        """Handle initial incoming call"""
        self.conversation_stage = "greeting"
        
        greeting = f"""
        Hello! Thank you for calling about our {self.trial_name}. 
        I'm here to help you learn more about this study and see if you might be a good fit. 
        This will take about 5 minutes. Are you ready to begin?
        """
        
        self.conversation_log.append({"stage": "greeting", "response": greeting})
        return greeting.strip()
    
    def process_patient_response(self, speech_text: str) -> str:
        """
        Process patient's spoken response and generate next question or conclusion
        
        Args:
            speech_text: Patient's spoken response
        
        Returns:
            AI response text
        """
        try:
            print(f"DEBUG: Processing response '{speech_text}'")
            print(f"DEBUG: Current question index: {self.current_question_index}")
            print(f"DEBUG: Total questions: {len(self.screening_questions)}")
            
            # Log the patient's response
            self.conversation_log.append({
                "stage": self.conversation_stage,
                "patient_response": speech_text
            })
            
            # Extract information from response
            self._extract_patient_info(speech_text)
            
            # Determine next step
            if self.current_question_index < len(self.screening_questions):
                print(f"DEBUG: Asking next question (index {self.current_question_index})")
                return self._ask_next_question()
            else:
                print(f"DEBUG: Generating conclusion (no more questions)")
                return self._generate_screening_conclusion()
                
        except Exception as e:
            logger.error(f"Error processing patient response: {e}")
            return "I apologize, but I'm having trouble processing your response. Could you please repeat that?"
    
    def _extract_patient_info(self, speech_text: str):
        """Extract structured information from patient's speech"""
        text_lower = speech_text.lower()
        
        print(f"DEBUG: Extracting info for field: {self.screening_questions[self.current_question_index]['field']}")
        
        # Extract age
        if "age" in self.screening_questions[self.current_question_index]["field"]:
            import re
            age_match = re.search(r'\b(\d{1,2})\b', speech_text)
            if age_match:
                self.patient_info.age = int(age_match.group(1))
        
        # Extract medical conditions
        elif "medical_conditions" in self.screening_questions[self.current_question_index]["field"]:
            if any(word in text_lower for word in ["diabetes", "diabetic"]):
                self.patient_info.medical_conditions = self.patient_info.medical_conditions or []
                self.patient_info.medical_conditions.append("diabetes")
            if any(word in text_lower for word in ["hypertension", "high blood pressure"]):
                self.patient_info.medical_conditions = self.patient_info.medical_conditions or []
                self.patient_info.medical_conditions.append("hypertension")
        
        # Extract pregnancy status
        elif "pregnant" in self.screening_questions[self.current_question_index]["field"]:
            if any(word in text_lower for word in ["yes", "pregnant", "nursing", "breastfeeding"]):
                self.patient_info.pregnant = True
            elif any(word in text_lower for word in ["no", "not pregnant", "not nursing"]):
                self.patient_info.pregnant = False
        
        # Extract severe conditions
        elif "severe_conditions" in self.screening_questions[self.current_question_index]["field"]:
            if any(word in text_lower for word in ["yes", "severe", "serious", "ongoing treatment"]):
                self.patient_info.severe_conditions = True
            elif any(word in text_lower for word in ["no", "not severe", "mild"]):
                self.patient_info.severe_conditions = False
        
        # Extract phone number parts
        elif "phone_area_code" in self.screening_questions[self.current_question_index]["field"]:
            digits = self._extract_digits_from_speech(speech_text)
            if len(digits) >= 3:
                self.patient_info.phone_area_code = ''.join(digits[:3])
                self.conversation_log.append({
                    "stage": "screening",
                    "extracted_area_code": self.patient_info.phone_area_code,
                    "original_response": speech_text
                })
        
        elif "phone_middle" in self.screening_questions[self.current_question_index]["field"]:
            digits = self._extract_digits_from_speech(speech_text)
            if len(digits) >= 3:
                self.patient_info.phone_middle = ''.join(digits[:3])
                self.conversation_log.append({
                    "stage": "screening",
                    "extracted_middle": self.patient_info.phone_middle,
                    "original_response": speech_text
                })
        
        elif "phone_last_four" in self.screening_questions[self.current_question_index]["field"]:
            digits = self._extract_digits_from_speech(speech_text)
            print(f"DEBUG: Last four digits - Input: '{speech_text}', Found digits: {digits}, Length: {len(digits)}")
            
            if len(digits) >= 4:
                self.patient_info.phone_last_four = ''.join(digits[:4])
                # Combine all phone number parts
                if self.patient_info.phone_area_code and self.patient_info.phone_middle:
                    full_phone = f"{self.patient_info.phone_area_code}-{self.patient_info.phone_middle}-{self.patient_info.phone_last_four}"
                    self.patient_info.contact_info = full_phone
                    self.conversation_log.append({
                        "stage": "screening",
                        "extracted_last_four": self.patient_info.phone_last_four,
                        "full_phone": full_phone,
                        "original_response": speech_text
                    })
    
    def _extract_digits_from_speech(self, speech_text: str) -> List[str]:
        """Extract digits from speech text, handling both spoken numbers and digits"""
        import re
        
        # Dictionary for spoken numbers (expanded)
        spoken_digits = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
            'oh': '0', 'o': '0',  # 'oh' and 'o' are often used for zero
            'to': '2', 'too': '2', 'for': '4', 'ate': '8',  # Common mispronunciations
            'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13',
            'fourteen': '14', 'fifteen': '15', 'sixteen': '16', 'seventeen': '17',
            'eighteen': '18', 'nineteen': '19', 'twenty': '20', 'thirty': '30',
            'forty': '40', 'fifty': '50', 'sixty': '60', 'seventy': '70',
            'eighty': '80', 'ninety': '90'
        }
        
        # Clean the text and remove common filler words
        text = speech_text.lower().strip()
        # Remove common filler words that might interfere
        filler_words = ['um', 'uh', 'like', 'the', 'and', 'or', 'is', 'are']
        for filler in filler_words:
            text = text.replace(f' {filler} ', ' ')
        
        words = text.split()
        digits = []
        
        # Look for spoken digits
        for word in words:
            if word in spoken_digits:
                digit_value = spoken_digits[word]
                # Handle multi-digit numbers by splitting them
                if len(digit_value) > 1:
                    for char in digit_value:
                        digits.append(char)
                else:
                    digits.append(digit_value)
        
        # If no spoken digits found, look for actual digits
        if not digits:
            digits = re.findall(r'\d', speech_text)
        
        # Debug logging
        print(f"DEBUG: Input='{speech_text}' -> Words={words} -> Digits={digits}")
        
        return digits
    
    def _ask_next_question(self) -> str:
        """Ask the next screening question"""
        if self.current_question_index < len(self.screening_questions):
            question_data = self.screening_questions[self.current_question_index]
            question = question_data["question"]
            
            self.conversation_stage = "screening"
            
            self.conversation_log.append({
                "stage": "screening",
                "question": question,
                "question_index": self.current_question_index
            })
            
            # Increment AFTER processing the current question
            self.current_question_index += 1
            
            return question
        
        return self._generate_screening_conclusion()
    
    def _generate_screening_conclusion(self) -> str:
        """Generate screening conclusion and next steps"""
        self.conversation_stage = "conclusion"
        
        # Simple eligibility assessment
        is_eligible = self._assess_eligibility()
        
        if is_eligible:
            conclusion = f"""
            Thank you for answering all the questions. Based on your responses, 
            you appear to be a potential candidate for our {self.trial_name}. 
            We will contact you within 24 hours to schedule a screening visit 
            and provide more details about the study. 
            Have a great day!
            """
        else:
            conclusion = f"""
            Thank you for your interest in our {self.trial_name}. 
            Based on your responses, you may not be eligible for this particular study, 
            but we will keep your information for future research opportunities. 
            Thank you for your time.
            """
        
        self.conversation_log.append({
            "stage": "conclusion",
            "eligible": is_eligible,
            "conclusion": conclusion
        })
        
        return conclusion.strip()
    
    def _assess_eligibility(self) -> bool:
        """Assess patient eligibility based on collected information"""
        # Simple eligibility criteria
        if self.patient_info.age and (self.patient_info.age < 18 or self.patient_info.age > 75):
            return False
        
        if self.patient_info.pregnant:
            return False
        
        if self.patient_info.severe_conditions:
            return False
        
        # If we have basic info and no exclusions, consider eligible
        return self.patient_info.age is not None
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation"""
        return {
            "trial_name": self.trial_name,
            "conversation_stage": self.conversation_stage,
            "questions_asked": self.current_question_index,
            "patient_info": {
                "age": self.patient_info.age,
                "medical_conditions": self.patient_info.medical_conditions,
                "medications": self.patient_info.medications,
                "pregnant": self.patient_info.pregnant,
                "severe_conditions": self.patient_info.severe_conditions,
                "contact_info": self.patient_info.contact_info,
                "phone_area_code": self.patient_info.phone_area_code,
                "phone_middle": self.patient_info.phone_middle,
                "phone_last_four": self.patient_info.phone_last_four
            },
            "eligible": self._assess_eligibility(),
            "conversation_log": self.conversation_log
        }
    
    def reset_conversation(self):
        """Reset conversation for a new patient"""
        self.conversation_stage = "greeting"
        self.patient_info = PatientInfo()
        self.current_question_index = 0
        self.conversation_log = []
