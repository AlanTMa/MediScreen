#!/usr/bin/env python3
"""
Test Twilio integration with real credentials
"""

def test_twilio_connection():
    """Test Twilio connection with real credentials"""
    print("📞 Testing Twilio Connection...")
    
    try:
        from twilio_client import TwilioClient
        
        # Initialize Twilio client
        client = TwilioClient()
        print("✅ Twilio client initialized")
        print(f"Account SID: {client.account_sid[:10]}...")
        
        if client.client:
            print("✅ Twilio client connected successfully!")
            
            # Test account info
            try:
                account = client.client.api.accounts(client.account_sid).fetch()
                print(f"✅ Account verified: {account.friendly_name}")
                print(f"   Status: {account.status}")
                print(f"   Type: {account.type}")
                
                return True
            except Exception as e:
                print(f"❌ Account verification failed: {e}")
                return False
        else:
            print("❌ Twilio client not connected")
            return False
            
    except Exception as e:
        print(f"❌ Twilio test failed: {e}")
        return False

def test_phone_number_creation():
    """Test creating a phone number"""
    print("\n📱 Testing Phone Number Creation...")
    
    try:
        from twilio_client import TwilioClient
        
        client = TwilioClient()
        
        if not client.client:
            print("❌ Twilio client not available")
            return False
        
        # Try to create a phone number
        phone_number = client.create_trial_phone_number('800')
        
        if phone_number:
            print(f"✅ Phone number created: {phone_number}")
            return True
        else:
            print("❌ Failed to create phone number")
            return False
            
    except Exception as e:
        print(f"❌ Phone number creation test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Twilio Integration Test")
    print("=" * 40)
    
    # Test connection
    connection_ok = test_twilio_connection()
    
    if connection_ok:
        # Test phone number creation
        phone_ok = test_phone_number_creation()
        
        if phone_ok:
            print("\n🎉 Twilio integration is working perfectly!")
        else:
            print("\n⚠️  Connection works but phone number creation failed")
    else:
        print("\n❌ Twilio integration failed")
        print("   Check your credentials and try again")
