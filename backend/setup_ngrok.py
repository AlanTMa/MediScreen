#!/usr/bin/env python3
"""
Setup ngrok for MediScreen Voice Agent
"""

import subprocess
import sys
import os
import time

def setup_ngrok():
    """Setup ngrok for local testing"""
    
    print("🌐 Setting up ngrok for MediScreen Voice Agent")
    print("=" * 50)
    
    print("📋 Step-by-Step Setup:")
    print("1. Go to https://ngrok.com and sign up for a free account")
    print("2. Go to https://dashboard.ngrok.com/get-started/your-authtoken")
    print("3. Copy your authtoken")
    print("4. Run: ngrok config add-authtoken YOUR_AUTHTOKEN_HERE")
    print("5. Start your Flask app: python app.py")
    print("6. In another terminal, run: ngrok http 5000")
    print("7. Copy the https URL (e.g., https://abc123.ngrok.io)")
    print("8. Update WEBHOOK_BASE_URL in config.py with the ngrok URL")
    
    print("\n🔧 Quick Commands:")
    print("# Terminal 1 - Start Flask app:")
    print("python app.py")
    print("\n# Terminal 2 - Start ngrok tunnel:")
    print("ngrok http 5000")
    
    print("\n📝 Example config.py update:")
    print("WEBHOOK_BASE_URL = 'https://abc123.ngrok.io'")
    
    print("\n✅ Once ngrok is running, you'll see:")
    print("   Forwarding: https://abc123.ngrok.io -> http://localhost:5000")
    print("   Use the https URL as your webhook URL in Twilio")

def test_ngrok():
    """Test if ngrok is working"""
    try:
        # Try to run ngrok version
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ngrok is installed and working!")
            print(f"   Version: {result.stdout.strip()}")
            return True
        else:
            print("❌ ngrok is not working properly")
            return False
    except FileNotFoundError:
        print("❌ ngrok is not found in PATH")
        print("   Please restart your terminal or add ngrok to PATH manually")
        return False

def start_flask_app():
    """Start the Flask app"""
    print("\n🚀 Starting Flask app...")
    print("   App will be available at: http://localhost:5000")
    print("   Health check: http://localhost:5000/health")
    print("\n   Press Ctrl+C to stop the app")
    print("=" * 50)
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n✅ Flask app stopped")

if __name__ == "__main__":
    print("🔍 Checking ngrok installation...")
    
    if test_ngrok():
        print("\n🎉 ngrok is ready to use!")
        print("\nNext steps:")
        print("1. Configure your authtoken (see instructions above)")
        print("2. Start your Flask app")
        print("3. Run ngrok http 5000")
    else:
        setup_ngrok()
        
    print("\n" + "=" * 50)
    print("🚀 Ready to start your MediScreen Voice Agent!")
    print("   Your phone number: +1 (877) 281-1957")
    print("   Once ngrok is running, Twilio can send webhooks to your app")
