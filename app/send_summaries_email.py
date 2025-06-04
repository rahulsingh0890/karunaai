import os
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Filenames
CALL_SUMMARIES_DIR = "call_summaries"
USERS_FILE = "config/users.json"
SENT_LOG_FILE = "sent_summaries.jsonl"  # append‐only log of sent summaries

def get_latest_summary_file():
    """Get the latest summary file from the call_summaries directory."""
    if not os.path.exists(CALL_SUMMARIES_DIR):
        print(f"ERROR: {CALL_SUMMARIES_DIR} directory not found.")
        return None
    files = [os.path.join(CALL_SUMMARIES_DIR, f) for f in os.listdir(CALL_SUMMARIES_DIR) if f.endswith('.json')]
    if not files:
        print(f"ERROR: No summary files found in {CALL_SUMMARIES_DIR}.")
        return None
    return max(files, key=os.path.getmtime)

def send_summaries_email():
    """
    Send the latest call summary via email, then append the sent summary to a log file.
    """
    # 1) Load the latest summary file
    latest_file = get_latest_summary_file()
    if not latest_file:
        return
    try:
        with open(latest_file, "r") as f:
            summary = json.load(f)
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON in {latest_file}")
        return

    # 2) Load user‐caregiver mapping
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {USERS_FILE} not found.")
        return
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON in {USERS_FILE}")
        return

    # 3) Email credentials
    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    if not sender_email or not sender_password:
        print("ERROR: Email configuration (EMAIL_SENDER or EMAIL_PASSWORD) not set in .env")
        return

    # 4) Send email for the latest summary
    client_name = summary.get("client_name") or summary.get("id")
    caregiver_email = None
    caregiver_name = None

    # Find caregiver email and name for this client
    for user in users.get("users", []):
        if user.get("client_name") == client_name:
            caregiver_email = user.get("caregiver_email")
            caregiver_name = user.get("caregiver_name")
            break

    if not caregiver_email:
        print(f"No caregiver email found for client '{client_name}'. Skipping.")
        return

    # Build email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = caregiver_email
    msg["Subject"] = f"Karunā Caregiver Update for {client_name} ❤️✨"

    # Construct email body
    caregiver_summary = summary.get('caregiver_summary', {})
    summary_text = caregiver_summary.get("today_summary", 'No summary available.')
    body_lines = [
        f"Hello {caregiver_name if caregiver_name else ''},",
        "",
        f"Here's today's check-in summary for {client_name}:",
        "",
        f"📝 Summary: {summary_text}",
    ]
    # Include mood if present
    if caregiver_summary.get('mood'):
        body_lines.append(f"\n😊 Mood: {caregiver_summary['mood'].capitalize()}")
    # Include observations if present
    if caregiver_summary.get('notable_observations'):
        observations = caregiver_summary['notable_observations']
        if isinstance(observations, list):
            obs_str = "\n  - " + "\n  - ".join(observations)
        else:
            obs_str = str(observations)
        body_lines.append(f"\n🔍 Observations:{obs_str}")
    # Include action items if present
    if caregiver_summary.get('action_items'):
        body_lines.append(f"\n📋 Suggested Action Items: {caregiver_summary['action_items']}")

    body_lines.extend([
        "",
        "Thank you for trusting Karunā to check-in with your family! 💛",
        "",
        "With love,",
        "Your Karunā Care Team",
        "https://tinyurl.com/karuna2025"
    ])
    body = "\n".join(body_lines)

    msg.attach(MIMEText(body, "plain"))

    # Send email via SMTP
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {caregiver_email}!")
    except Exception as e:
        print(f"ERROR sending email to {caregiver_email}: {e}")
        return  # Skip appending to log if sending failed

    # 5) Append the sent summary to a JSONL log file
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "client_name": client_name,
        "caregiver_email": caregiver_email,
        "summary": caregiver_summary.get("today_summary"),
        "mood": caregiver_summary.get("mood"),
        "observations": caregiver_summary.get("notable_observations"),
        "action_items": caregiver_summary.get("action_items")
    }
    try:
        with open(SENT_LOG_FILE, "a") as log_f:
            log_f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"WARNING: Could not append to {SENT_LOG_FILE}: {e}")

if __name__ == "__main__":
    send_summaries_email()
