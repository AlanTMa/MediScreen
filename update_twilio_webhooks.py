#!/usr/bin/env python3
"""
Update Twilio phone number webhooks to point to ngrok URL
"""

import os
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, WEBHOOK_BASE_URL

def update_twilio_webhooks():
    """Update Twilio phone number webhooks"""
    
    print("Updating Twilio Webhooks")
    print("=" * 50)
    print(f"Webhook URL: {WEBHOOK_BASE_URL}")
    print(f"Account SID: {TWILIO_ACCOUNT_SID}")
    print()
    
    try:
        # Initialize Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Get all phone numbers
        phone_numbers = client.incoming_phone_numbers.list()
        
        if not phone_numbers:
            print("No phone numbers found in your Twilio account")
            print("   You may need to purchase a phone number first")
            return
        
        print(f"Found {len(phone_numbers)} phone number(s):")
        
        for number in phone_numbers:
            print(f"   - {number.phone_number}")
            
            # Update webhook URLs
            webhook_url = f"{WEBHOOK_BASE_URL}/handle_call"
            
            try:
                number.update(
                    voice_url=webhook_url,
                    voice_method='POST',
                    status_callback=f"{WEBHOOK_BASE_URL}/call_status",
                    status_callback_method='POST'
                )
                print(f"   Updated webhooks for {number.phone_number}")
                print(f"      Voice URL: {webhook_url}")
                print(f"      Status Callback: {WEBHOOK_BASE_URL}/call_status")
                
            except Exception as e:
                print(f"   Failed to update {number.phone_number}: {e}")
        
        print("\nWebhook update complete!")
        print("\nTest your phone number:")
        print("   Call +1 (877) 281-1957")
        print("   Your AI voice agent should now answer!")
        
    except Exception as e:
        print(f"Error updating webhooks: {e}")
        print("\nManual Setup Instructions:")
        print("1. Go to https://console.twilio.com/")
        print("2. Navigate to Phone Numbers > Manage > Active numbers")
        print("3. Click on your phone number")
        print("4. Set Voice webhook to:")
        print(f"   {WEBHOOK_BASE_URL}/handle_call")
        print("5. Set Status callback to:")
        print(f"   {WEBHOOK_BASE_URL}/call_status")
        print("6. Save configuration")

if __name__ == "__main__":
    update_twilio_webhooks()
