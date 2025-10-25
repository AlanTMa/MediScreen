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
    availability_date: Optional[str] = None

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
            },
            {
                "question": "What is the next date when you would be available for a screening visit? You can say it like 'ten sixteen' for October 16th, or 'October sixteenth', or 'the sixteenth of October'.",
                "field": "availability_date",
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
            print(f"DEBUG: Conversation stage: {self.conversation_stage}")
            
            # Log the patient's response
            self.conversation_log.append({
                "stage": self.conversation_stage,
                "patient_response": speech_text
            })
            
            # If we're in greeting stage, just ask the first question
            if self.conversation_stage == "greeting":
                print(f"DEBUG: In greeting stage, asking first question")
                self.conversation_stage = "screening"
                return self._ask_next_question()
            
            # Extract information from response
            self._extract_patient_info(speech_text)
            
            # Increment question index after processing response
            self.current_question_index += 1
            
            # Determine next step - check if we've completed all questions
            if self.current_question_index >= len(self.screening_questions):
                print(f"DEBUG: Generating conclusion (no more questions)")
                return self._generate_screening_conclusion()
            else:
                print(f"DEBUG: Asking next question (index {self.current_question_index})")
                return self._ask_next_question()
                
        except Exception as e:
            logger.error(f"Error processing patient response: {e}")
            print(f"DEBUG: Exception occurred: {e}")
            print(f"DEBUG: Exception type: {type(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            return "I apologize, but I'm having trouble processing your response. Could you please repeat that?"
    
    def _extract_patient_info(self, speech_text: str):
        """Extract structured information from patient's speech"""
        text_lower = speech_text.lower()
        
        # Check if we're still in the screening phase
        if self.current_question_index >= len(self.screening_questions):
            print(f"DEBUG: Conversation already complete, skipping extraction")
            return
        
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
        
        elif "availability_date" in self.screening_questions[self.current_question_index]["field"]:
            date_text = self._extract_date_from_speech(speech_text)
            print(f"DEBUG: Availability date - Input: '{speech_text}', Extracted: '{date_text}'")
            
            if date_text:
                self.patient_info.availability_date = date_text
                self.conversation_log.append({
                    "stage": "screening",
                    "extracted_date": self.patient_info.availability_date,
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
    
    def _extract_date_from_speech(self, speech_text: str) -> str:
        """Extract date from speech text, handling various formats"""
        import re
        
        text_lower = speech_text.lower().strip()
        
        # Month names mapping
        months = {
            'january': '01', 'jan': '01',
            'february': '02', 'feb': '02',
            'march': '03', 'mar': '03',
            'april': '04', 'apr': '04',
            'may': '05',
            'june': '06', 'jun': '06',
            'july': '07', 'jul': '07',
            'august': '08', 'aug': '08',
            'september': '09', 'sep': '09', 'sept': '09',
            'october': '10', 'oct': '10',
            'november': '11', 'nov': '11',
            'december': '12', 'dec': '12'
        }
        
        # Ordinal numbers mapping
        ordinals = {
            'first': '1', 'second': '2', 'third': '3', 'fourth': '4', 'fifth': '5',
            'sixth': '6', 'seventh': '7', 'eighth': '8', 'ninth': '9', 'tenth': '10',
            'eleventh': '11', 'twelfth': '12', 'thirteenth': '13', 'fourteenth': '14',
            'fifteenth': '15', 'sixteenth': '16', 'seventeenth': '17', 'eighteenth': '18',
            'nineteenth': '19', 'twentieth': '20', 'twenty-first': '21', 'twenty-second': '22',
            'twenty-third': '23', 'twenty-fourth': '24', 'twenty-fifth': '25', 'twenty-sixth': '26',
            'twenty-seventh': '27', 'twenty-eighth': '28', 'twenty-ninth': '29', 'thirtieth': '30',
            'thirty-first': '31'
        }
        
        # Regular numbers
        numbers = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
            'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
            'eleven': '11', 'twelve': '12', 'thirteen': '13', 'fourteen': '14', 'fifteen': '15',
            'sixteen': '16', 'seventeen': '17', 'eighteen': '18', 'nineteen': '19', 'twenty': '20',
            'twenty-one': '21', 'twenty-two': '22', 'twenty-three': '23', 'twenty-four': '24',
            'twenty-five': '25', 'twenty-six': '26', 'twenty-seven': '27', 'twenty-eight': '28',
            'twenty-nine': '29', 'thirty': '30', 'thirty-one': '31'
        }
        
        # Pattern 1: "ten sixteen" -> "10/16"
        pattern1 = r'(\w+)\s+(\w+)'
        match1 = re.search(pattern1, text_lower)
        if match1:
            first_word = match1.group(1)
            second_word = match1.group(2)
            
            # Check if first word is a month and second is a day
            if first_word in months and second_word in numbers:
                month = months[first_word]
                day = numbers[second_word]
                return f"{month}/{day}"
            elif first_word in numbers and second_word in numbers:
                # Could be month/day format
                month = numbers[first_word]
                day = numbers[second_word]
                if int(month) <= 12 and int(day) <= 31:
                    return f"{month}/{day}"
        
        # Pattern 2: "October sixteenth" or "October 16" or "dec 15"
        pattern2 = r'(\w+)\s+(\w+)'
        match2 = re.search(pattern2, text_lower)
        if match2:
            first_word = match2.group(1)
            second_word = match2.group(2)
            
            if first_word in months:
                month = months[first_word]
                if second_word in ordinals:
                    day = ordinals[second_word]
                    return f"{month}/{day}"
                elif second_word in numbers:
                    day = numbers[second_word]
                    return f"{month}/{day}"
        
        # Pattern 3: "the sixteenth of October"
        pattern3 = r'the\s+(\w+)\s+of\s+(\w+)'
        match3 = re.search(pattern3, text_lower)
        if match3:
            day_word = match3.group(1)
            month_word = match3.group(2)
            
            if day_word in ordinals and month_word in months:
                day = ordinals[day_word]
                month = months[month_word]
                return f"{month}/{day}"
        
        # Pattern 4: Direct numbers like "10/16" or "10 16"
        pattern4 = r'(\d{1,2})[/\s]+(\d{1,2})'
        match4 = re.search(pattern4, speech_text)
        if match4:
            month = match4.group(1)
            day = match4.group(2)
            return f"{month}/{day}"
        
        # If no pattern matches, return the original text
        return speech_text
    
    def _ask_next_question(self) -> str:
        """Ask the next screening question"""
        print(f"DEBUG: _ask_next_question called with index {self.current_question_index}")
        print(f"DEBUG: Total questions: {len(self.screening_questions)}")
        print(f"DEBUG: Index < Total: {self.current_question_index < len(self.screening_questions)}")
        
        # Check if we have more questions to ask
        if self.current_question_index < len(self.screening_questions):
            question_data = self.screening_questions[self.current_question_index]
            question = question_data["question"]
            
            print(f"DEBUG: Asking question: {question}")
            
            self.conversation_stage = "screening"
            
            self.conversation_log.append({
                "stage": "screening",
                "question": question,
                "question_index": self.current_question_index
            })
            
            # Index is incremented in the main processing loop
            
            return question
        
        print(f"DEBUG: Going to conclusion")
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

        if self.patient_info.medications:
            return False
        
        if self.patient_info.medical_conditions:
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
                "phone_last_four": self.patient_info.phone_last_four,
                "availability_date": self.patient_info.availability_date
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
