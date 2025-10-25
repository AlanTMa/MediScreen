#!/usr/bin/env python3
"""
Update ngrok URL in configuration
"""

def update_ngrok_url():
    """Update the webhook URL with ngrok URL"""
    
    print("🌐 Update ngrok URL in Configuration")
    print("=" * 50)
    
    print("📋 Steps:")
    print("1. Copy your ngrok URL (e.g., https://abc123.ngrok.io)")
    print("2. Run this script with your URL")
    print("3. Your Twilio webhooks will use the ngrok URL")
    
    print("\n🔧 Manual Update:")
    print("Edit config.py and change:")
    print("WEBHOOK_BASE_URL = 'https://abc123.ngrok.io'")
    
    print("\n🧪 Test Your Setup:")
    print("1. Health check: https://abc123.ngrok.io/health")
    print("2. Call your phone: +1 (877) 281-1957")
    print("3. Twilio will send webhooks to your ngrok URL")

if __name__ == "__main__":
    update_ngrok_url()
