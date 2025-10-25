"""
Configuration file for MediScreen Voice Agent
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ElevenLabs Configuration
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '4afb19f7ade23680cba6bb6ccf99b074e7216fb25fb2a907b6c3175ee163ac58')

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'AC76dd9ed7af5468dd51a8eb0cd2a341f1')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'cd42ffd8b85ae77dec29e23e3bff9870')

# Application Configuration
WEBHOOK_BASE_URL = os.getenv('WEBHOOK_BASE_URL', 'https://intemerately-flagless-nu.ngrok-free.dev')

# Phone Number
REGISTERED_PHONE_NUMBER = "6692909608"

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
