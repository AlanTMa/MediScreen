"""
Twilio Telephony Client
Handles phone number management and call processing for clinical trial recruitment
"""

import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwilioClient:
    def __init__(self, account_sid: Optional[str] = None, auth_token: Optional[str] = None):
        from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
        self.account_sid = account_sid or TWILIO_ACCOUNT_SID
        self.auth_token = auth_token or TWILIO_AUTH_TOKEN
        self.phone_number = "6692909608"  # Your registered caller ID
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            logger.warning("Twilio credentials not configured")
    
    def create_trial_phone_number(self, area_code: str = "800") -> Optional[str]:
        """
        Create a toll-free number for clinical trial recruitment
        
        Args:
            area_code: Area code (800 for toll-free)
        
        Returns:
            Phone number if successful, None otherwise
        """
        if not self.client:
            logger.error("Twilio client not initialized")
            return None
        
        try:
            if area_code == "800":
                # Search for toll-free numbers
                available_numbers = self.client.available_phone_numbers('US').toll_free.list(
                    voice_enabled=True,
                    limit=10
                )
            else:
                # Search for local numbers
                available_numbers = self.client.available_phone_numbers('US').local.list(
                    area_code=area_code,
                    voice_enabled=True,
                    limit=10
                )
            
            if available_numbers:
                # Purchase the first available number
                phone_number = self.client.incoming_phone_numbers.create(
                    phone_number=available_numbers[0].phone_number,
                    voice_url=f"{os.getenv('WEBHOOK_BASE_URL', 'https://your-domain.com')}/handle_call",
                    voice_method='POST',
                    status_callback=f"{os.getenv('WEBHOOK_BASE_URL', 'https://your-domain.com')}/call_status",
                    status_callback_method='POST'
                )
                
                logger.info(f"Created phone number: {phone_number.phone_number}")
                return phone_number.phone_number
            else:
                logger.error(f"No available numbers found for area code {area_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating phone number: {e}")
            return None
    
    def create_incoming_call_response(self, greeting_text: str) -> str:
        """
        Create TwiML response for incoming calls
        
        Args:
            greeting_text: Text to speak to the caller
        
        Returns:
            TwiML response as string
        """
        response = VoiceResponse()
        
        # Professional greeting for clinical trial recruitment
        response.say(greeting_text, voice='alice')
        
        # Gather user input
        gather = response.gather(
            input='speech',
            action='/process_speech',
            method='POST',
            speech_timeout='auto',
            timeout=15,
            language='en-US'
        )
        
        # Fallback if no response
        response.say("I didn't hear anything. Please try again or press any key to continue.", voice='alice')
        response.redirect('/handle_call')
        
        return str(response)
    
    def create_speech_response(self, response_text: str, continue_conversation: bool = True) -> str:
        """
        Create TwiML response for speech processing
        
        Args:
            response_text: Text to speak to the caller
            continue_conversation: Whether to continue gathering input
        
        Returns:
            TwiML response as string
        """
        response = VoiceResponse()
        
        # Speak the AI response
        response.say(response_text, voice='alice')
        
        if continue_conversation:
            # Continue gathering responses
            gather = response.gather(
                input='speech',
                action='/process_speech',
                method='POST',
                speech_timeout='auto',
                timeout=15,
                language='en-US'
            )
            
            # Fallback
            response.say("I didn't catch that. Could you please repeat your answer?", voice='alice')
            response.redirect('/process_speech')
        else:
            # End conversation
            response.say("Thank you for your interest in our clinical trial. Have a wonderful day!", voice='alice')
            response.hangup()
        
        return str(response)
    
    def send_sms(self, to_number: str, message: str) -> bool:
        """
        Send SMS message
        
        Args:
            to_number: Recipient phone number
            message: Message content
        
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            logger.error("Twilio client not initialized")
            return False
        
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.phone_number,
                to=to_number
            )
            logger.info(f"SMS sent successfully: {message.sid}")
            return True
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            return False
