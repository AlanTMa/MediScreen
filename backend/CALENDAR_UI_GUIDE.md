# 🏥 MediScreen Calendar UI

## 🎯 **What We Built**

A beautiful, custom calendar interface for your MediScreen voice agent that displays all collected appointments in an interactive calendar view.

## 📅 **Features**

### **Visual Calendar**
- **Monthly View**: Clean, modern calendar grid
- **Appointment Display**: Shows appointments as colored blocks
- **Interactive**: Click appointments to see full details
- **Responsive**: Works on desktop and mobile

### **Real-Time Data**
- **Live Integration**: Fetches data from your voice agent conversations
- **Automatic Updates**: Shows new appointments as they're collected
- **Smart Parsing**: Handles different date formats from voice input

### **Statistics Dashboard**
- **Total Appointments**: Count of all collected appointments
- **This Month**: Appointments for current month
- **Eligible Patients**: Count of patients who passed screening

### **Export Functionality**
- **One-Click Export**: Export all appointments to multiple formats
- **Multiple Formats**: CSV, JSON, and iCal (.ics) files
- **Calendar Import**: Import .ics files into Google Calendar, Apple Calendar, Outlook

## 🚀 **How to Use**

### **Option 1: Standalone Calendar Server**
```bash
cd /Users/hugh/repos/MediScreen/backend
source venv/bin/activate
python test_calendar.py
```
- Opens automatically in your browser at `http://localhost:5001`
- Perfect for testing and demonstration

### **Option 2: Integrated with Main System**
```bash
cd /Users/hugh/repos/MediScreen/backend
source venv/bin/activate
python start_system.py
```
- Access calendar at `http://localhost:5000/calendar`
- Full integration with your voice agent system

## 📊 **API Endpoints**

### **Get Appointments**
```
GET /api/appointments
```
Returns JSON array of all appointments with patient details.

### **Export Appointments**
```
GET /api/export
```
Exports appointments to CSV, JSON, and iCal formats.

## 🎨 **Calendar Features**

### **Appointment Display**
- **Time**: Shows 10:00 AM (configurable)
- **Phone**: Patient's contact number
- **Color Coding**: Red gradient for visual appeal
- **Hover Effects**: Interactive animations

### **Appointment Details Modal**
- **Call ID**: Unique conversation identifier
- **Patient Info**: Age, phone, availability
- **Medical Data**: Conditions and medications
- **Eligibility**: Clear yes/no status
- **Timestamps**: When conversation was created

### **Navigation**
- **Month Navigation**: Previous/Next buttons
- **Current Month**: Clear month/year display
- **Today Highlighting**: Current date highlighted

## 📁 **File Structure**

```
backend/
├── templates/
│   └── calendar.html          # Calendar UI template
├── app.py                     # Main Flask app (updated with calendar routes)
├── test_calendar.py          # Standalone calendar server
├── export_appointments.py    # Export functionality
└── conversations/            # Voice agent conversation data
    └── *.json               # Individual conversation files
```

## 🔄 **Data Flow**

```
Voice Agent collects appointment data
    ↓
Stored in conversations/*.json files
    ↓
Calendar API reads conversation files
    ↓
Calendar UI displays appointments
    ↓
Export functionality creates files
    ↓
Import into external calendar apps
```

## 🎯 **Next Steps**

### **Immediate Use**
1. **Run the calendar**: `python test_calendar.py`
2. **View appointments**: Browser opens automatically
3. **Export data**: Click "Export" button
4. **Import to calendar**: Use the generated .ics file

### **Customization Options**
- **Time Slots**: Modify appointment times
- **Colors**: Change appointment colors
- **Layout**: Adjust calendar grid
- **Fields**: Add more patient information

### **Integration Options**
- **Email Notifications**: Send calendar invites
- **SMS Reminders**: Text patients about appointments
- **Database Storage**: Store in database instead of JSON
- **Calendar Sync**: Real-time sync with Google Calendar

## 🌟 **Benefits**

### **For You**
- **Visual Overview**: See all appointments at a glance
- **Easy Management**: Click to view patient details
- **Export Options**: Multiple formats for different needs
- **No External Dependencies**: Works with your existing data

### **For Patients**
- **Clear Scheduling**: Visual representation of availability
- **Easy Export**: Import into their preferred calendar app
- **Professional Look**: Clean, modern interface

## 🎉 **Success!**

Your MediScreen project now has a complete calendar system that:
- ✅ Displays all voice agent appointments
- ✅ Provides interactive patient details
- ✅ Exports to multiple formats
- ✅ Integrates with external calendar apps
- ✅ Works on all devices

The calendar information now has a beautiful, functional destination! 🏥📅✨
