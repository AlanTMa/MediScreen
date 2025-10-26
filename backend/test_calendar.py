#!/usr/bin/env python3
"""
Test script to demonstrate the MediScreen Calendar UI
"""

import os
import json
import webbrowser
import time
from flask import Flask, render_template, jsonify
from threading import Thread

# Create a simple Flask app for testing
app = Flask(__name__)

@app.route('/')
def calendar():
    """Serve the calendar UI"""
    return render_template('calendar.html')

@app.route('/api/appointments')
def get_appointments():
    """API endpoint to get all appointments"""
    appointments = []
    
    # Read all conversation files
    conversations_dir = 'conversations'
    if os.path.exists(conversations_dir):
        for filename in os.listdir(conversations_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(conversations_dir, filename), 'r') as f:
                        data = json.load(f)
                        
                        patient_info = data['summary']['patient_info']
                        
                        # Only include patients with availability dates
                        if patient_info.get('availability_date') and patient_info.get('contact_info'):
                            appointment = {
                                'id': filename.replace('.json', ''),
                                'phone': patient_info['contact_info'],
                                'age': patient_info['age'],
                                'availability_date': patient_info['availability_date'],
                                'medical_conditions': patient_info.get('medical_conditions', []),
                                'medications': patient_info.get('medications', []),
                                'eligible': data['summary']['eligible'],
                                'created_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['timestamp']))
                            }
                            appointments.append(appointment)
                except Exception as e:
                    print(f"Error reading conversation file {filename}: {e}")
    
    return jsonify(appointments)

@app.route('/api/export')
def export_appointments():
    """Export appointments to various formats"""
    try:
        # Run the export script
        import subprocess
        result = subprocess.run(['python', 'export_appointments.py'], 
                              capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            return jsonify({'success': True, 'message': 'Appointments exported successfully'})
        else:
            return jsonify({'success': False, 'message': result.stderr})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

def run_calendar_server():
    """Run the calendar server"""
    print("🏥 MediScreen Calendar Server Starting...")
    print("=" * 50)
    print("📅 Calendar UI: http://localhost:5001")
    print("📊 API Endpoint: http://localhost:5001/api/appointments")
    print("📥 Export API: http://localhost:5001/api/export")
    print("=" * 50)
    
    # Open browser automatically
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:5001')
    
    Thread(target=open_browser).start()
    
    app.run(debug=False, port=5001, host='0.0.0.0')

if __name__ == "__main__":
    run_calendar_server()
