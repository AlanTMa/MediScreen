#!/usr/bin/env python3
"""
Start MediScreen Voice Agent System
"""

import os
import sys
import subprocess
import time
import webbrowser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment configuration...")
    
    # Check required components
    components = {
        'ElevenLabs API Key': os.getenv('ELEVENLABS_API_KEY', '4afb19f7ade23680cba6bb6ccf99b074e7216fb25fb2a907b6c3175ee163ac58'),
        'Twilio Account SID': os.getenv('TWILIO_ACCOUNT_SID', 'AC76dd9ed7af5468dd51a8eb0cd2a341f1'),
        'Twilio Auth Token': os.getenv('TWILIO_AUTH_TOKEN', 'cd42ffd8b85ae77dec29e23e3bff9870')
    }
    
    all_good = True
    for component, value in components.items():
        if value and not value.startswith('your_'):
            print(f"✅ {component}: {value[:20]}...")
        else:
            print(f"❌ {component}: Not configured")
            all_good = False
    
    return all_good

def start_flask_app():
    """Start the Flask app"""
    print("\n🚀 Starting MediScreen Voice Agent...")
    print("=" * 50)
    print("📞 Twilio Integration: Ready")
    print("🎤 ElevenLabs Voice: Ready") 
    print("🤖 AI Voice Agent: Ready")
    print("🌐 Flask Server: Starting on port 5000")
    print("=" * 50)
    print("\n📱 Your phone number: +1 (877) 281-1957")
    print("🔗 Health check: http://localhost:5000/health")
    print("\n   Press Ctrl+C to stop the app")
    print("=" * 50)
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n✅ MediScreen Voice Agent stopped")

def show_ngrok_instructions():
    """Show ngrok setup instructions"""
    print("\n🌐 ngrok Setup Instructions:")
    print("=" * 30)
    print("1. Open a NEW terminal window")
    print("2. Run: ngrok http 5000")
    print("3. Copy the https URL (e.g., https://abc123.ngrok.io)")
    print("4. Update WEBHOOK_BASE_URL in config.py with the ngrok URL")
    print("5. Restart this script")
    
    print("\n💡 Pro tip: Keep both terminals open:")
    print("   - Terminal 1: Flask app (this script)")
    print("   - Terminal 2: ngrok tunnel")

def main():
    """Main function"""
    print("🏥 MediScreen Voice Agent System")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment not properly configured")
        print("   Please check your configuration and try again")
        return
    
    # Check if ngrok URL is configured
    webhook_url = os.getenv('WEBHOOK_BASE_URL', 'https://your-ngrok-url.ngrok.io')
    if 'ngrok.io' not in webhook_url:
        show_ngrok_instructions()
        print(f"\n⚠️  Current webhook URL: {webhook_url}")
        print("   This should be an ngrok URL for local testing")
        
        response = input("\nDo you want to start the Flask app anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Start Flask app
    start_flask_app()

if __name__ == "__main__":
    main()
