# 🏥 MediScreen

**24/7 Voice & Speech AI Patient Pre-Screener**

MediScreen is an AI-powered voice agent system that conducts automated clinical trial patient pre-screening via phone calls. It integrates Twilio for telephony, ElevenLabs for voice synthesis, and custom AI logic to collect patient information, assess eligibility, and manage appointments.

## ✨ Features

- 🤖 **AI Voice Agent**: Conversational AI that guides patients through screening questions
- 📞 **Phone Integration**: Full Twilio integration for receiving and handling calls
- 🗣️ **Natural Speech Processing**: Handles spoken numbers, dates, and responses
- 📋 **Clinical Trial Screening**: Automated eligibility assessment and data collection
- 📅 **Appointment Management**: Calendar interface to view and manage eligible patients
- 📊 **Data Export**: Export appointments to CSV, JSON, and ICS formats
- 🔔 **Follow-up SMS**: Automatic SMS notifications for eligible patients
- 📝 **Conversation Logging**: Detailed logs of all patient interactions

## 🏗️ Architecture

```
┌─────────────────┐
│   Patient Call  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Twilio Cloud   │────▶│  Flask Server   │────▶│ Voice Agent AI  │
│   Telephony     │     │   (Backend)     │     │  (Screening)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │
                                ▼
                        ┌─────────────────┐
                        │   Database/      │
                        │   JSON Files    │
                        └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Twilio account with a phone number
- ElevenLabs API key (optional, for voice synthesis)
- Letta client library (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/MediScreen.git
cd MediScreen
```

2. **Navigate to backend directory**
```bash
cd backend
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the `backend` directory:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token

# ElevenLabs Configuration (optional)
ELEVENLABS_API_KEY=your_elevenlabs_api_key

# Webhook Configuration
WEBHOOK_BASE_URL=https://your-domain.com

# Application Configuration
REGISTERED_PHONE_NUMBER=your_phone_number
LOG_LEVEL=INFO
```

5. **Start the Flask server**
```bash
python app.py
```

The application will run on `http://localhost:5000`

## 📱 Configuration

### Twilio Setup

1. Create a Twilio account at [twilio.com](https://www.twilio.com)
2. Get a phone number for your application
3. Configure webhooks in Twilio console:
   - **Voice URL**: `https://your-domain.com/handle_call`
   - **Status Callback**: `https://your-domain.com/call_status`

### Webhook Setup

Update your Twilio phone number webhooks to point to your deployment URL:

```bash
python update_twilio_webhooks.py
```

## 🔄 Usage

### Starting the System

```bash
python app.py
```

Or use the system starter:

```bash
python start_system.py
```

### Making a Test Call

1. Call your registered Twilio phone number
2. Follow the AI voice prompts
3. Answer screening questions
4. Receive eligibility assessment
5. Check calendar UI for appointment data

### Accessing the Calendar UI

Navigate to `http://localhost:5000/calendar` to view and manage eligible patients.

## 📊 API Endpoints

### Core Endpoints

- `POST /handle_call` - Handle incoming phone calls
- `POST /process_speech` - Process patient speech input
- `POST /call_status` - Handle call status updates
- `GET /health` - Health check endpoint
- `GET /conversations/<call_sid>` - Get conversation data

### Calendar Endpoints

- `GET /calendar` - Serve calendar UI
- `GET /api/appointments` - Get all appointments (JSON)
- `GET /api/export` - Export appointments to file

### Phone Management

- `POST /create_number` - Create new Twilio phone number

## 🧪 Testing

Run the test suite:

```bash
# Test full conversation flow
python test_full_conversation.py

# Test date extraction
python test_date_extraction.py

# Test phone system
python test_phone_system.py

# Test edge cases
python test_edge_cases.py
```

## 📁 Project Structure

```
MediScreen/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── voice_agent.py         # AI voice agent logic
│   ├── twilio_client.py       # Twilio integration
│   ├── elevenlabs_client.py   # ElevenLabs integration
│   ├── config.py              # Configuration management
│   ├── templates/
│   │   └── calendar.html      # Calendar UI
│   ├── conversations/         # Logged conversations (JSON)
│   ├── appointments.csv       # Exported appointments
│   ├── appointments.json      # Exported appointments
│   └── requirements.txt       # Python dependencies
├── calendar-ui/               # Additional UI components
└── README.md                  # This file
```

## 🌐 Deployment

### Railway Deployment (Recommended)

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Connect your repository
4. Deploy automatically
5. Set environment variables in Railway dashboard
6. Update DNS to point to Railway URL

### Render Deployment

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect repository
5. Deploy automatically
6. Configure environment variables

### Environment Variables for Production

```env
ELEVENLABS_API_KEY=your_key
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
WEBHOOK_BASE_URL=https://your-domain.com
REGISTERED_PHONE_NUMBER=your_phone_number
LOG_LEVEL=INFO
```

See `backend/deploy_instructions.md` for detailed deployment instructions.

## 📝 Screening Questions

The voice agent collects the following information:

1. Age
2. Medical conditions
3. Current medications
4. Pregnancy status
5. Severe medical conditions
6. Contact phone number
7. Availability date

## 🎯 Eligibility Assessment

Patients are assessed based on:
- Age range (typically 18-75)
- Pregnancy status (exclusion criteria)
- Current medications
- Medical conditions
- Severe ongoing conditions

## 📞 Features in Detail

### Voice Agent Capabilities

- **Natural Language Processing**: Extracts structured data from spoken responses
- **Date Parsing**: Handles multiple date formats ("ten sixteen", "October sixteenth", etc.)
- **Phone Number Collection**: Gathers phone numbers in parts for accuracy
- **Conversation Management**: Maintains state across multiple exchanges
- **Eligibility Logic**: Real-time assessment during screening

### Data Management

- **Conversation Logging**: All interactions saved as JSON files
- **Appointment Tracking**: Eligible patients tracked with availability dates
- **Export Capabilities**: Data exported to CSV, JSON, and ICS formats
- **Follow-up Automation**: SMS notifications to eligible patients

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🔧 Troubleshooting

### Call Not Connecting

- Check Twilio webhook configuration
- Verify webhook URL is accessible
- Check nginx configuration (if using ngrok)

### Speech Not Processing

- Verify Twilio credentials
- Check speech recognition settings
- Review conversation logs in `conversations/` directory

### Deployment Issues

- Ensure all environment variables are set
- Check deployment logs in platform dashboard
- Verify DNS configuration

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review test files for usage examples

## 🎉 Acknowledgments

- **Twilio** for telephony services
- **ElevenLabs** for voice AI capabilities
- **Letta** for conversational AI framework
- **Flask** for web framework

---

**Built with ❤️ for clinical trial recruitment**

