"""
MediScreen - 24/7 Voice & Speech AI Patient Pre-Screener
Main Flask application integrating Twilio, ElevenLabs, and AI voice agent
"""

import os
import json
import logging
from flask import Flask, request, Response, jsonify
from twilio_client import TwilioClient
from elevenlabs_client import ElevenLabsClient
from voice_agent import ClinicalTrialVoiceAgent
from typing import Dict, Any
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize clients
twilio_client = TwilioClient()
elevenlabs_client = ElevenLabsClient()

# Store active conversations
active_conversations = {}

@app.route('/handle_call', methods=['POST'])
def handle_incoming_call():
    """Handle incoming calls from potential trial participants"""
    try:
        call_sid = request.form.get('CallSid')
        from_number = request.form.get('From')
        
        logger.info(f"Incoming call from {from_number}, Call SID: {call_sid}")
        
        # Initialize voice agent for this call
        voice_agent = ClinicalTrialVoiceAgent()
        active_conversations[call_sid] = {
            'voice_agent': voice_agent,
            'from_number': from_number,
            'start_time': time.time()
        }
        
        # Get greeting from voice agent
        greeting = voice_agent.process_incoming_call()
        
        # Create TwiML response
        twiml_response = twilio_client.create_incoming_call_response(greeting)
        
        return Response(twiml_response, mimetype='text/xml')
        
    except Exception as e:
        logger.error(f"Error handling incoming call: {e}")
        error_response = twilio_client.create_speech_response(
            "I apologize, but I'm experiencing technical difficulties. Please try calling back later.",
            continue_conversation=False
        )
        return Response(error_response, mimetype='text/xml')

@app.route('/process_speech', methods=['POST'])
def process_speech():
    """Process patient speech input and generate AI response"""
    try:
        call_sid = request.form.get('CallSid')
        speech_result = request.form.get('SpeechResult', '')
        
        logger.info(f"Processing speech for call {call_sid}: {speech_result}")
        
        if call_sid not in active_conversations:
            logger.error(f"No active conversation found for call {call_sid}")
            error_response = twilio_client.create_speech_response(
                "I apologize, but I'm having trouble with this call. Please try calling back.",
                continue_conversation=False
            )
            return Response(error_response, mimetype='text/xml')
        
        # Get voice agent for this conversation
        voice_agent = active_conversations[call_sid]['voice_agent']
        
        # Process patient response
        ai_response = voice_agent.process_patient_response(speech_result)
        
        # Check if conversation should continue
        continue_conversation = voice_agent.conversation_stage != "conclusion"
        
        # Create TwiML response
        twiml_response = twilio_client.create_speech_response(
            ai_response, 
            continue_conversation=continue_conversation
        )
        
        # If conversation is ending, log the summary
        if not continue_conversation:
            _log_conversation_summary(call_sid, voice_agent)
            del active_conversations[call_sid]
        
        return Response(twiml_response, mimetype='text/xml')
        
    except Exception as e:
        logger.error(f"Error processing speech: {e}")
        error_response = twilio_client.create_speech_response(
            "I apologize, but I'm having trouble processing your response. Could you please repeat that?",
            continue_conversation=True
        )
        return Response(error_response, mimetype='text/xml')

@app.route('/call_status', methods=['POST'])
def handle_call_status():
    """Handle call status updates from Twilio"""
    call_sid = request.form.get('CallSid')
    call_status = request.form.get('CallStatus')
    logger.info(f"Call {call_sid} status: {call_status}")
    return '', 200

@app.route('/create_number', methods=['POST'])
def create_phone_number():
    """Create a new phone number for trial recruitment"""
    try:
        area_code = request.json.get('area_code', '800')
        phone_number = twilio_client.create_trial_phone_number(area_code)
        
        if phone_number:
            return jsonify({
                'success': True, 
                'phone_number': phone_number,
                'message': f'Phone number {phone_number} created successfully'
            })
        else:
            return jsonify({
                'success': False, 
                'error': 'Failed to create phone number. Check Twilio credentials.'
            }), 500
            
    except Exception as e:
        logger.error(f"Error creating phone number: {e}")
        return jsonify({
            'success': False, 
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'MediScreen Voice Agent',
        'version': '1.0.0',
        'active_conversations': len(active_conversations),
        'components': {
            'twilio': twilio_client.client is not None,
            'elevenlabs': elevenlabs_client.api_key is not None
        }
    })

@app.route('/conversations/<call_sid>', methods=['GET'])
def get_conversation(call_sid):
    """Get conversation data for a specific call"""
    if call_sid in active_conversations:
        voice_agent = active_conversations[call_sid]['voice_agent']
        return jsonify(voice_agent.get_conversation_summary())
    else:
        return jsonify({'error': 'Conversation not found'}), 404

def _log_conversation_summary(call_sid: str, voice_agent: ClinicalTrialVoiceAgent):
    """Log conversation summary for follow-up"""
    try:
        summary = voice_agent.get_conversation_summary()
        conversation_data = active_conversations.get(call_sid, {})
        
        log_data = {
            'call_sid': call_sid,
            'from_number': conversation_data.get('from_number'),
            'start_time': conversation_data.get('start_time'),
            'duration': time.time() - conversation_data.get('start_time', time.time()),
            'summary': summary,
            'timestamp': time.time()
        }
        
        # Log to file (in production, this would go to a database)
        os.makedirs('conversations', exist_ok=True)
        with open(f'conversations/{call_sid}.json', 'w') as f:
            json.dump(log_data, f, indent=2)
        
        logger.info(f"Conversation logged for call {call_sid}")
        
        # Send follow-up SMS if patient is eligible
        if summary.get('eligible') and conversation_data.get('from_number'):
            _send_follow_up_sms(conversation_data['from_number'], summary)
            
    except Exception as e:
        logger.error(f"Error logging conversation: {e}")

def _send_follow_up_sms(phone_number: str, summary: Dict[str, Any]):
    """Send follow-up SMS to eligible patients"""
    try:
        message = f"""
        Thank you for your interest in our clinical trial! 
        You may be eligible for our study. 
        Please check your email for next steps and scheduling information.
        If you have any questions, please call us back.
        """
        
        twilio_client.send_sms(phone_number, message)
        logger.info(f"Follow-up SMS sent to {phone_number}")
        
    except Exception as e:
        logger.error(f"Error sending follow-up SMS: {e}")

if __name__ == '__main__':
    print("🏥 MediScreen Voice Agent Starting...")
    print("=" * 50)
    print("📞 Twilio Integration: Ready")
    print("🎤 ElevenLabs Voice: Ready") 
    print("🤖 AI Voice Agent: Ready")
    print("🌐 Flask Server: Starting on port 5000")
    print("=" * 50)
    
    # Create conversations directory
    os.makedirs('conversations', exist_ok=True)
    
    # Start the Flask app
    app.run(debug=True, port=5000, host='0.0.0.0')
