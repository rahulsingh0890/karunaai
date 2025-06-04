import os
import json
import requests
import shutil
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict

# Load environment variables from .env
load_dotenv()

# Ollama configuration
OLLAMA_SERVER = os.getenv("OLLAMA_SERVER", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

CALL_LOGS_FILE = "call_logs.json"
OUTPUT_SUMMARIES_FILE = "call_summaries.json"

USERS_FILE = "config/users.json"
TARGET_NUMBER = "+12342342345"  # Replace with your phone number

# --- Load users.json and map phone numbers to client names ---
def load_user_mapping():
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f).get("users", [])
            return {u["client_phone_number"]: u["client_name"] for u in users}
    except Exception as e:
        print(f"Error loading users.json: {e}")
        return {}

def load_call_logs():
    """Load the JSON array of up to 5 recent calls from call_logs.json."""
    try:
        with open(CALL_LOGS_FILE, "r") as f:
            calls = json.load(f)
            return calls if isinstance(calls, list) else []
    except FileNotFoundError:
        print(f"Error: {CALL_LOGS_FILE} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {CALL_LOGS_FILE}.")
        return []

def cleanup_old_summaries():
    """Remove all existing summary files."""
    if os.path.exists("call_summaries"):
        shutil.rmtree("call_summaries")
    os.makedirs("call_summaries", exist_ok=True)

def generate_caregiver_summary(transcript, client_name):
    """Generate a caregiver-friendly summary using Ollama's Mistral model."""
    if not transcript:
        return {
            "summary": "No transcript available for this call.",
            "mood": "Unknown",
            "notable_observations": [],
            "action_items": []
        }

    prompt = f"You are a helpful assistant that provides concise, friendly updates to caregivers.\n"
    prompt += f"The client's name is {client_name}.\n"
    prompt += "Analyze the following call transcript and provide a structured summary in JSON format with these fields:\n"
    prompt += "- \"today_summary\": A brief, warm summary of the conversation (4–5 sentences, refer to the client by name)\n"
    prompt += "- \"mood\": The person's overall mood (Positive/Neutral/Negative)\n"
    prompt += "- \"notable_observations\": A list of important observations about their well-being or any concerns they shared\n\n"
    prompt += "Keep the tone warm and conversational. Focus on how the person was feeling and any notable changes in their condition or mood.\n\n"
    prompt += f"Transcript:\n{transcript}\n\n"
    prompt += "Provide the response in valid JSON format only."

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            try:
                # Extract the JSON response from Mistral's output
                summary_text = response.json().get("response", "")
                # Find the JSON object in the response
                start_idx = summary_text.find('{')
                end_idx = summary_text.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = summary_text[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    raise ValueError("No JSON object found in response")
            except json.JSONDecodeError:
                print("Error: Could not parse JSON from Mistral response")
                return {
                    "summary": "Error generating summary.",
                    "mood": "Unknown",
                    "notable_observations": [],
                    "action_items": []
                }
        else:
            print(f"Error: Ollama API returned status code {response.status_code}")
            return {
                "summary": "Error generating summary.",
                "mood": "Unknown",
                "notable_observations": [],
                "action_items": []
            }
    except Exception as e:
        print(f"Error calling Ollama API: {e}")
        return {
            "summary": "Error generating summary.",
            "mood": "Unknown",
            "notable_observations": [],
            "action_items": []
        }

def save_call_summaries(calls, user_map):
    """Save each call's summary as a separate file named by call ID."""
    os.makedirs("call_summaries", exist_ok=True)
    
    for call in calls:
        call_id = call.get("id")
        if not call_id:
            continue
            
        # Use the phone number to get the client name
        client_name = user_map.get(TARGET_NUMBER, "the client")
        # Generate caregiver-friendly summary
        caregiver_summary = generate_caregiver_summary(call.get("transcript"), client_name)
        
        summary_data = {
            "id": call.get("id"),
            "client_name": client_name,
            "status": call.get("status"),
            "started_at": call.get("started_at"),
            "ended_at": call.get("ended_at"),
            "duration": call.get("duration"),
            "cost": call.get("cost"),
            "recording_url": call.get("recording_url"),
            "stereo_recording_url": call.get("stereo_recording_url"),
            "transcript": call.get("transcript"),
            "caregiver_summary": caregiver_summary
        }
        
        filename = f"call_summaries/{call_id}.json"
        with open(filename, 'w') as f:
            json.dump(summary_data, f, indent=2)
            
    print(f"Saved {len(calls)} call summaries to call_summaries/ directory.")

def main():
    # Clean up old summaries
    cleanup_old_summaries()
    
    # Load call logs
    user_map = load_user_mapping()
    calls = load_call_logs()
    if not calls:
        return
    
    # Save call summaries
    save_call_summaries(calls, user_map)

if __name__ == "__main__":
    main()
