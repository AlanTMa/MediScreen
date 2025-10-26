#!/usr/bin/env python3
"""
Simple Calendar Export - No API Required
Exports appointment data for manual calendar entry
"""

import json
import csv
from datetime import datetime
from typing import Dict, List, Any

def export_appointments_to_files():
    """Export all conversation data to calendar-friendly formats"""
    
    # Read all conversation files
    import os
    conversations_dir = "conversations"
    appointments = []
    
    for filename in os.listdir(conversations_dir):
        if filename.endswith('.json'):
            with open(os.path.join(conversations_dir, filename), 'r') as f:
                data = json.load(f)
                
                patient_info = data['summary']['patient_info']
                
                # Only include eligible patients with availability dates
                if (data['summary']['eligible'] and 
                    patient_info.get('availability_date') and 
                    patient_info.get('contact_info')):
                    
                    appointment = {
                        'call_id': filename.replace('.json', ''),
                        'phone': patient_info['contact_info'],
                        'age': patient_info['age'],
                        'availability_date': patient_info['availability_date'],
                        'medical_conditions': patient_info.get('medical_conditions', []),
                        'medications': patient_info.get('medications', []),
                        'created_at': datetime.fromtimestamp(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    }
                    appointments.append(appointment)
    
    if not appointments:
        print("No eligible appointments found")
        return
    
    # Export to CSV
    with open('appointments.csv', 'w', newline='') as csvfile:
        fieldnames = ['call_id', 'phone', 'age', 'availability_date', 'medical_conditions', 'medications', 'created_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for appointment in appointments:
            # Convert lists to strings for CSV
            appointment_copy = appointment.copy()
            appointment_copy['medical_conditions'] = ', '.join(appointment['medical_conditions']) if appointment['medical_conditions'] else 'None'
            appointment_copy['medications'] = ', '.join(appointment['medications']) if appointment['medications'] else 'None'
            writer.writerow(appointment_copy)
    
    # Export to JSON
    with open('appointments.json', 'w') as jsonfile:
        json.dump(appointments, jsonfile, indent=2)
    
    # Export to iCal format
    ical_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//MediScreen//Appointments//EN\n"
    
    for appointment in appointments:
        # Parse availability date
        date_str = appointment['availability_date']
        if '/' in date_str:
            month, day = date_str.split('/')
            current_year = datetime.now().year
            start_dt = datetime(current_year, int(month), int(day), 10, 0)  # 10 AM
            end_dt = datetime(current_year, int(month), int(day), 10, 30)  # 30 min
            
            start_ical = start_dt.strftime("%Y%m%dT%H%M%S")
            end_ical = end_dt.strftime("%Y%m%dT%H%M%S")
            
            ical_content += f"""BEGIN:VEVENT
UID:{appointment['call_id']}@mediscreen.com
DTSTART:{start_ical}
DTEND:{end_ical}
SUMMARY:MediScreen Appointment - {appointment['phone']}
DESCRIPTION:Phone: {appointment['phone']}\\nAge: {appointment['age']}\\nConditions: {', '.join(appointment['medical_conditions']) if appointment['medical_conditions'] else 'None'}
LOCATION:MediScreen Clinic
END:VEVENT
"""
    
    ical_content += "END:VCALENDAR"
    
    with open('appointments.ics', 'w') as icalfile:
        icalfile.write(ical_content)
    
    print(f"✅ Exported {len(appointments)} appointments:")
    print("   📄 appointments.csv (for Excel/Google Sheets)")
    print("   📄 appointments.json (for data processing)")
    print("   📅 appointments.ics (for calendar apps)")
    print("\n📅 You can import appointments.ics into:")
    print("   - Google Calendar")
    print("   - Apple Calendar")
    print("   - Outlook")
    print("   - Any calendar app that supports .ics files")

if __name__ == "__main__":
    export_appointments_to_files()
