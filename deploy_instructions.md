# Deploy MediScreen Voice Agent to mediscreen.tech

## 🚀 Quick Deployment Options

### Option 1: Railway (Recommended - Easiest)

1. **Go to [railway.app](https://railway.app)**
2. **Sign up with GitHub**
3. **Create new project**
4. **Connect your GitHub repository**
5. **Deploy automatically**
6. **Get your Railway URL** (e.g., `your-app.railway.app`)

### Option 2: Render (Free)

1. **Go to [render.com](https://render.com)**
2. **Sign up with GitHub**
3. **Create new Web Service**
4. **Connect GitHub repository**
5. **Deploy automatically**
6. **Get your Render URL** (e.g., `your-app.onrender.com`)

## 🌐 DNS Configuration

### For Railway/Render (CNAME approach):
```
Type: CNAME
Name: api
Value: your-app.railway.app (or your-app.onrender.com)
TTL: 300
```

### For DigitalOcean (A record approach):
```
Type: A
Name: api
Value: YOUR_DROPLET_IP
TTL: 300
```

## 📱 Your Setup

- **Phone Number**: +1 (877) 281-1957
- **Domain**: mediscreen.tech
- **API Endpoint**: https://api.mediscreen.tech
- **Webhook URL**: https://api.mediscreen.tech/handle_call

## 🧪 Testing

After deployment and DNS setup:

1. **Test health endpoint**: https://api.mediscreen.tech/health
2. **Test phone number**: Call +1 (877) 281-1957
3. **Check webhooks**: Twilio will send calls to your domain

## 🔧 Environment Variables

Set these in your cloud service:

```
ELEVENLABS_API_KEY=4afb19f7ade23680cba6bb6ccf99b074e7216fb25fb2a907b6c3175ee163ac58
TWILIO_ACCOUNT_SID=AC76dd9ed7af5468dd51a8eb0cd2a341f1
TWILIO_AUTH_TOKEN=cd42ffd8b85ae77dec29e23e3bff9870
WEBHOOK_BASE_URL=https://api.mediscreen.tech
```

## 🎉 Ready to Go Live!

Your MediScreen Voice Agent will be accessible at:
- **API**: https://api.mediscreen.tech
- **Phone**: +1 (877) 281-1957
- **24/7 AI Voice Agent**: Ready for clinical trial recruitment
