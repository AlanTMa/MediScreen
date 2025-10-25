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
                "question": "What is the best phone number to reach you for follow-up? Please say the number clearly, including the area code.",
                "field": "contact_info",
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
            # Log the patient's response
            self.conversation_log.append({
                "stage": self.conversation_stage,
                "patient_response": speech_text
            })
            
            # Extract information from response
            self._extract_patient_info(speech_text)
            
            # Determine next step
            if self.current_question_index < len(self.screening_questions):
                return self._ask_next_question()
            else:
                return self._generate_screening_conclusion()
                
        except Exception as e:
            logger.error(f"Error processing patient response: {e}")
            return "I apologize, but I'm having trouble processing your response. Could you please repeat that?"
    
    def _extract_patient_info(self, speech_text: str):
        """Extract structured information from patient's speech"""
        text_lower = speech_text.lower()
        
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
        
        # Extract contact info
        elif "contact_info" in self.screening_questions[self.current_question_index]["field"]:
            import re
            
            # Try multiple phone number patterns
            phone_number = self._extract_phone_number(speech_text)
            if phone_number:
                self.patient_info.contact_info = phone_number
                # Add confirmation to conversation log
                self.conversation_log.append({
                    "stage": "screening",
                    "extracted_phone": phone_number,
                    "original_response": speech_text
                })
    
    def _extract_phone_number(self, speech_text: str) -> Optional[str]:
        """Extract phone number from speech text using multiple patterns"""
        import re
        
        # Clean the text
        text = speech_text.lower().strip()
        
        # Pattern 1: Standard format (555-123-4567, 555.123.4567, 5551234567)
        pattern1 = r'\b(\d{3}[-.]?\d{3}[-.]?\d{4})\b'
        match = re.search(pattern1, speech_text)
        if match:
            return match.group(1)
        
        # Pattern 2: Spoken numbers (five five five, one two three, four five six seven)
        spoken_digits = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
            'oh': '0'  # 'oh' is often used for zero
        }
        
        # Look for sequences of spoken digits
        words = text.split()
        digits = []
        
        for word in words:
            if word in spoken_digits:
                digits.append(spoken_digits[word])
            elif word.isdigit():
                digits.append(word)
        
        # If we found 10 digits, format as phone number
        if len(digits) == 10:
            return f"{''.join(digits[:3])}-{''.join(digits[3:6])}-{''.join(digits[6:])}"
        
        # Pattern 3: Look for "area code" followed by number
        area_code_pattern = r'area code\s*(\d{3})[,\s]*(\d{3})[,\s-]*(\d{4})'
        match = re.search(area_code_pattern, text)
        if match:
            return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
        
        # Pattern 4: Look for any sequence of 10 consecutive digits
        digits_only = re.findall(r'\d', speech_text)
        if len(digits_only) >= 10:
            # Take the first 10 digits
            phone_digits = ''.join(digits_only[:10])
            return f"{phone_digits[:3]}-{phone_digits[3:6]}-{phone_digits[6:]}"
        
        # Pattern 5: Look for phone number with parentheses (555) 123-4567
        paren_pattern = r'\((\d{3})\)\s*(\d{3})[-\s]*(\d{4})'
        match = re.search(paren_pattern, speech_text)
        if match:
            return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
        
        return None
    
    def _ask_next_question(self) -> str:
        """Ask the next screening question"""
        if self.current_question_index < len(self.screening_questions):
            question_data = self.screening_questions[self.current_question_index]
            question = question_data["question"]
            
            self.current_question_index += 1
            self.conversation_stage = "screening"
            
            self.conversation_log.append({
                "stage": "screening",
                "question": question,
                "question_index": self.current_question_index - 1
            })
            
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
                "contact_info": self.patient_info.contact_info
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
