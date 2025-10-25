#!/usr/bin/env python3
"""
Deploy MediScreen Voice Agent to mediscreen.tech domain
"""

import os
import sys

def show_domain_setup():
    """Show how to set up mediscreen.tech domain"""
    
    print("🌐 MediScreen.tech Domain Setup")
    print("=" * 50)
    
    print("📋 Domain Configuration Options:")
    print("\n1. 🚀 Professional Setup (Recommended)")
    print("   - Deploy to a cloud server (AWS, DigitalOcean, Railway)")
    print("   - Point api.mediscreen.tech to your server")
    print("   - Use HTTPS with SSL certificate")
    
    print("\n2. 🏠 Home Server Setup")
    print("   - Run Flask app on your home computer")
    print("   - Use dynamic DNS service (DuckDNS, No-IP)")
    print("   - Point api.mediscreen.tech to your home IP")
    
    print("\n3. 🔧 Quick Setup with ngrok")
    print("   - Use ngrok for immediate testing")
    print("   - Update DNS later when ready to deploy")
    
    print("\n" + "=" * 50)
    print("🎯 Recommended: Professional Setup")
    print("=" * 50)
    
    print("\n📱 Your Current Setup:")
    print("   Phone Number: +1 (877) 281-1957")
    print("   Domain: mediscreen.tech")
    print("   Webhook URL: https://api.mediscreen.tech")
    
    print("\n🚀 Quick Deploy Options:")
    print("\nA. Railway (Easiest)")
    print("   1. Go to railway.app")
    print("   2. Connect your GitHub repo")
    print("   3. Deploy your Flask app")
    print("   4. Get Railway URL")
    print("   5. Point api.mediscreen.tech to Railway URL")
    
    print("\nB. Render (Free)")
    print("   1. Go to render.com")
    print("   2. Create new Web Service")
    print("   3. Connect GitHub repo")
    print("   4. Deploy Flask app")
    print("   5. Point api.mediscreen.tech to Render URL")
    
    print("\nC. DigitalOcean (Professional)")
    print("   1. Create Droplet (Ubuntu)")
    print("   2. Install Python, Flask, etc.")
    print("   3. Deploy your app")
    print("   4. Point api.mediscreen.tech to Droplet IP")
    
    print("\n" + "=" * 50)
    print("🔧 DNS Configuration")
    print("=" * 50)
    
    print("\nIn your domain registrar (where you bought mediscreen.tech):")
    print("Add these DNS records:")
    print("\nType: A Record")
    print("Name: api")
    print("Value: YOUR_SERVER_IP")
    print("TTL: 300")
    
    print("\nType: CNAME")
    print("Name: www")
    print("Value: mediscreen.tech")
    print("TTL: 300")
    
    print("\n" + "=" * 50)
    print("🧪 Testing Your Domain")
    print("=" * 50)
    
    print("\nOnce deployed, test these URLs:")
    print("   Health: https://api.mediscreen.tech/health")
    print("   Create Number: https://api.mediscreen.tech/create_number")
    print("   Handle Call: https://api.mediscreen.tech/handle_call")
    
    print("\n📞 Your phone number will then use:")
    print("   Webhook URL: https://api.mediscreen.tech/handle_call")
    print("   Status Callback: https://api.mediscreen.tech/call_status")

def show_ngrok_fallback():
    """Show ngrok setup as fallback"""
    
    print("\n" + "=" * 50)
    print("🔧 Quick Testing with ngrok")
    print("=" * 50)
    
    print("\nFor immediate testing while setting up domain:")
    print("1. Start Flask app: python app.py")
    print("2. Start ngrok: ngrok http 5000")
    print("3. Copy ngrok URL (e.g., https://abc123.ngrok.io)")
    print("4. Update config.py: WEBHOOK_BASE_URL = 'https://abc123.ngrok.io'")
    print("5. Test your phone number: +1 (877) 281-1957")
    
    print("\n💡 Pro tip: Use ngrok for testing, domain for production!")

if __name__ == "__main__":
    show_domain_setup()
    show_ngrok_fallback()
    
    print("\n" + "=" * 50)
    print("🎉 Ready to Deploy!")
    print("=" * 50)
    print("Your MediScreen Voice Agent is ready for deployment!")
    print("Choose your preferred deployment method above.")
