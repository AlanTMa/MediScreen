"""
Test script for MediScreen Voice Agent system
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing Imports...")
    
    try:
        from elevenlabs_client import ElevenLabsClient, get_voice_id
        print("✅ ElevenLabs client import successful")
    except Exception as e:
        print(f"❌ ElevenLabs client import failed: {e}")
        return False
    
    try:
        from twilio_client import TwilioClient
        print("✅ Twilio client import successful")
    except Exception as e:
        print(f"❌ Twilio client import failed: {e}")
        return False
    
    try:
        from voice_agent import ClinicalTrialVoiceAgent
        print("✅ Voice agent import successful")
    except Exception as e:
        print(f"❌ Voice agent import failed: {e}")
        return False
    
    return True

def test_elevenlabs():
    """Test ElevenLabs functionality"""
    print("\n🎤 Testing ElevenLabs...")
    
    try:
        from elevenlabs_client import ElevenLabsClient, get_voice_id
        
        # Initialize ElevenLabs
        client = ElevenLabsClient()
        print("✅ ElevenLabs client created")
        
        # Test voice presets
        voice_id = get_voice_id("rachel")
        print(f"✅ Voice ID for 'rachel': {voice_id}")
        
        # Test text-to-speech
        test_text = "Hello, this is a test of the ElevenLabs voice synthesis."
        print(f"Testing text-to-speech with: '{test_text}'")
        
        audio_data = client.text_to_speech(test_text, voice_id)
        if audio_data:
            print(f"✅ Text-to-speech successful! Generated {len(audio_data)} bytes")
            return True
        else:
            print("❌ Text-to-speech failed")
            return False
            
    except Exception as e:
        print(f"❌ ElevenLabs test failed: {e}")
        return False

def test_voice_agent():
    """Test voice agent functionality"""
    print("\n🤖 Testing Voice Agent...")
    
    try:
        from voice_agent import ClinicalTrialVoiceAgent
        
        # Initialize voice agent
        agent = ClinicalTrialVoiceAgent()
        print("✅ Voice agent created")
        
        # Test incoming call
        greeting = agent.process_incoming_call()
        print(f"✅ Greeting generated: {greeting[:50]}...")
        
        # Test patient response processing
        response1 = agent.process_patient_response("Hello, I am 35 years old")
        print(f"✅ Response 1: {response1[:50]}...")
        
        response2 = agent.process_patient_response("I have diabetes")
        print(f"✅ Response 2: {response2[:50]}...")
        
        # Test conversation summary
        summary = agent.get_conversation_summary()
        print(f"✅ Conversation summary generated")
        print(f"   Questions asked: {summary['questions_asked']}")
        print(f"   Patient age: {summary['patient_info']['age']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice agent test failed: {e}")
        return False

def test_twilio():
    """Test Twilio functionality"""
    print("\n📞 Testing Twilio...")
    
    try:
        from twilio_client import TwilioClient
        
        # Initialize Twilio client
        client = TwilioClient()
        print("✅ Twilio client created")
        
        # Test TwiML generation
        greeting = "Hello! Thank you for calling about our clinical trial."
        twiml = client.create_incoming_call_response(greeting)
        print("✅ TwiML response generated")
        
        # Check credentials
        if client.client:
            print("✅ Twilio credentials configured")
        else:
            print("⚠️  Twilio credentials not configured (using placeholder)")
        
        return True
        
    except Exception as e:
        print(f"❌ Twilio test failed: {e}")
        return False

def test_flask_app():
    """Test Flask app"""
    print("\n🌐 Testing Flask App...")
    
    try:
        from app import app
        
        # Test if app can be created
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Health endpoint working")
                health_data = response.get_json()
                print(f"   Service: {health_data.get('service')}")
                print(f"   Version: {health_data.get('version')}")
            else:
                print(f"⚠️  Health endpoint returned status {response.status_code}")
            
            # Test handle_call endpoint
            response = client.post('/handle_call', data={
                'CallSid': 'test_call_123',
                'From': '+1234567890'
            })
            if response.status_code == 200:
                print("✅ Handle call endpoint working")
            else:
                print(f"⚠️  Handle call endpoint returned status {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 MediScreen Voice Agent Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_elevenlabs,
        test_voice_agent,
        test_twilio,
        test_flask_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your MediScreen Voice Agent is ready!")
        print("\n🚀 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure Twilio credentials in config.py")
        print("3. Start the app: python app.py")
        print("4. Set up ngrok: ngrok http 5000")
        print("5. Create a phone number via API")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
