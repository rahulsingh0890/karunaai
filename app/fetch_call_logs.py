import os
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
from vapi import Vapi

# Load environment variables from .env
load_dotenv()

def fetch_call_logs():
    """
    Fetches the most recent call log using the Vapi API and saves it to call_logs.json.
    """
    # Initialize Vapi client
    vapi = Vapi(token=os.getenv('VAPI_API_KEY'))
    
    # Get all calls
    calls = vapi.calls.list()
    
    # Filter calls for the specific phone number
    target_number = '+12342342345'  # Replace with your phone number
    filtered_calls = []
    
    for call in calls:
        # Check if the call has the target phone number
        if hasattr(call, 'customer') and call.customer and call.customer.number == target_number:
            artifact = getattr(call, 'artifact', None)
            recording_url = getattr(artifact, 'recording_url', None) if artifact else None
            stereo_recording_url = getattr(artifact, 'stereo_recording_url', None) if artifact else None
            transcript = getattr(artifact, 'transcript', None) if artifact else None
            # Create a dictionary with relevant call information
            call_info = {
                'id': call.id,
                'status': call.status,
                'started_at': call.started_at.isoformat() if call.started_at else None,
                'ended_at': call.ended_at.isoformat() if call.ended_at else None,
                'duration': (call.ended_at - call.started_at).total_seconds() if call.started_at and call.ended_at else None,
                'cost': call.cost,
                'transcript': transcript,
                'recording_url': recording_url,
                'stereo_recording_url': stereo_recording_url
            }
            filtered_calls.append(call_info)
    
    # Sort calls by started_at in descending order (most recent first)
    filtered_calls.sort(key=lambda x: x['started_at'] if x['started_at'] else '', reverse=True)
    
    # Take only the most recent call
    filtered_calls = filtered_calls[:1]
    
    # Save to JSON file
    with open('call_logs.json', 'w') as f:
        json.dump(filtered_calls, f, indent=2)
    
    print(f"Found latest call for {target_number}")
    print("Call log has been saved to call_logs.json")

if __name__ == "__main__":
    fetch_call_logs() 