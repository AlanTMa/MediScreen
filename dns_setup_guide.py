#!/usr/bin/env python3
"""
DNS Setup Guide for mediscreen.tech
Step-by-step instructions for configuring your domain
"""

def show_dns_setup():
    """Show detailed DNS setup instructions"""
    
    print("🌐 DNS Setup for mediscreen.tech")
    print("=" * 50)
    
    print("📋 Step 1: Access Your Domain Registrar")
    print("   Go to where you bought mediscreen.tech (GoDaddy, Namecheap, etc.)")
    print("   Look for 'DNS Management' or 'Domain Settings'")
    
    print("\n📋 Step 2: Add DNS Records")
    print("   Add these exact records:")
    
    print("\n   Record 1: Main API Endpoint")
    print("   Type: A")
    print("   Name: api")
    print("   Value: YOUR_SERVER_IP (we'll get this)")
    print("   TTL: 300")
    
    print("\n   Record 2: WWW Redirect")
    print("   Type: CNAME")
    print("   Name: www")
    print("   Value: mediscreen.tech")
    print("   TTL: 300")
    
    print("\n   Record 3: Root Domain (Optional)")
    print("   Type: A")
    print("   Name: @")
    print("   Value: YOUR_SERVER_IP")
    print("   TTL: 300")
    
    print("\n" + "=" * 50)
    print("🔧 Getting Your Server IP")
    print("=" * 50)
    
    print("\nOption A: Use Your Home IP (Temporary)")
    print("   1. Go to whatismyipaddress.com")
    print("   2. Copy your public IP address")
    print("   3. Use this IP in DNS records")
    print("   4. Note: This only works if your home IP is static")
    
    print("\nOption B: Use a Cloud Service (Recommended)")
    print("   1. Deploy to Railway/Render/DigitalOcean")
    print("   2. Get the server IP from the service")
    print("   3. Use this IP in DNS records")
    
    print("\n" + "=" * 50)
    print("🧪 Testing Your DNS Setup")
    print("=" * 50)
    
    print("\nAfter adding DNS records, test with:")
    print("   nslookup api.mediscreen.tech")
    print("   ping api.mediscreen.tech")
    print("   curl https://api.mediscreen.tech/health")

def show_cloud_deployment():
    """Show cloud deployment options for getting a server IP"""
    
    print("\n" + "=" * 50)
    print("☁️ Cloud Deployment Options")
    print("=" * 50)
    
    print("\n🚀 Option A: Railway (Easiest)")
    print("   1. Go to railway.app")
    print("   2. Sign up with GitHub")
    print("   3. Create new project")
    print("   4. Connect your GitHub repo")
    print("   5. Deploy your Flask app")
    print("   6. Get Railway URL (e.g., your-app.railway.app)")
    print("   7. Use Railway URL as CNAME target")
    
    print("\n🚀 Option B: Render (Free)")
    print("   1. Go to render.com")
    print("   2. Sign up with GitHub")
    print("   3. Create new Web Service")
    print("   4. Connect GitHub repo")
    print("   5. Deploy Flask app")
    print("   6. Get Render URL (e.g., your-app.onrender.com)")
    print("   7. Use Render URL as CNAME target")
    
    print("\n🚀 Option C: DigitalOcean (Professional)")
    print("   1. Go to digitalocean.com")
    print("   2. Create Droplet (Ubuntu 22.04)")
    print("   3. Get Droplet IP address")
    print("   4. SSH into Droplet")
    print("   5. Install Python, Flask, etc.")
    print("   6. Deploy your app")
    print("   7. Use Droplet IP in DNS A record")

def show_dns_record_examples():
    """Show exact DNS record examples"""
    
    print("\n" + "=" * 50)
    print("📝 Exact DNS Record Examples")
    print("=" * 50)
    
    print("\nFor Railway/Render (CNAME approach):")
    print("   Type: CNAME")
    print("   Name: api")
    print("   Value: your-app.railway.app")
    print("   TTL: 300")
    
    print("\nFor DigitalOcean (A record approach):")
    print("   Type: A")
    print("   Name: api")
    print("   Value: 157.245.123.456 (example IP)")
    print("   TTL: 300")
    
    print("\nFor Home Server (if static IP):")
    print("   Type: A")
    print("   Name: api")
    print("   Value: 192.168.1.100 (your home IP)")
    print("   TTL: 300")

def show_ssl_setup():
    """Show SSL certificate setup"""
    
    print("\n" + "=" * 50)
    print("🔒 SSL Certificate Setup")
    print("=" * 50)
    
    print("\nMost cloud services provide SSL automatically:")
    print("   ✅ Railway: Automatic HTTPS")
    print("   ✅ Render: Automatic HTTPS")
    print("   ✅ DigitalOcean: Use Let's Encrypt")
    
    print("\nFor custom servers:")
    print("   1. Install Certbot")
    print("   2. Run: certbot --nginx -d api.mediscreen.tech")
    print("   3. Automatic SSL certificate")

if __name__ == "__main__":
    show_dns_setup()
    show_cloud_deployment()
    show_dns_record_examples()
    show_ssl_setup()
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps")
    print("=" * 50)
    print("1. Choose your deployment method")
    print("2. Deploy your Flask app")
    print("3. Get server IP or URL")
    print("4. Add DNS records in your registrar")
    print("5. Test: https://api.mediscreen.tech/health")
    print("6. Update Twilio webhook URL")
    print("7. Test your phone number: +1 (877) 281-1957")
    
    print("\n🎉 Your mediscreen.tech domain will be live!")
