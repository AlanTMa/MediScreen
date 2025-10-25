"""
ElevenLabs Voice Synthesis Client
Handles natural voice generation for clinical trial conversations
"""

import requests
import os
from typing import Optional, Dict, Any

class ElevenLabsClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY', '4afb19f7ade23680cba6bb6ccf99b074e7216fb25fb2a907b6c3175ee163ac58')
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        # Voice settings optimized for medical conversations
        self.voice_settings = {
            "stability": 0.7,  # More stable for medical context
            "similarity_boost": 0.8,  # Clear pronunciation
            "style": 0.2,  # Professional tone
            "use_speaker_boost": True
        }
    
    def text_to_speech(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
        """
        Convert text to speech using ElevenLabs
        
        Args:
            text: Text to convert to speech
            voice_id: ElevenLabs voice ID (default is Rachel - professional female voice)
        
        Returns:
            Audio data as bytes
        """
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": self.voice_settings
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/text-to-speech/{voice_id}",
                json=data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error in text-to-speech: {e}")
            return b""
    
    def get_available_voices(self) -> Dict[str, Any]:
        """Get available voices from ElevenLabs"""
        try:
            response = requests.get(f"{self.base_url}/voices", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching voices: {e}")
            return {}

# Voice presets for different conversation contexts
VOICE_PRESETS = {
    "rachel": "21m00Tcm4TlvDq8ikWAM",  # Professional female - default
    "domi": "AZnzlk1XvdvUeBnXmlld",    # Warm female
    "bella": "EXAVITQu4vr4xnSDxMaL",   # Friendly female
    "antoni": "ErXwobaYiN019PkySvjV",  # Professional male
    "josh": "TxGEqnHWrfWFTfGW9XjX",    # Warm male
}

def get_voice_id(voice_name: str) -> str:
    """Get voice ID by name"""
    return VOICE_PRESETS.get(voice_name.lower(), VOICE_PRESETS["rachel"])
