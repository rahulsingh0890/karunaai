import os
import subprocess
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/webhook/vapi", methods=["POST"])
def vapi_webhook():
    """
    This endpoint is called by Vapi when a call ends.
    It simply invokes three existing scripts in sequence:
      1) fetch_call_logs.py
      2) summarize_call_logs.py
      3) send_summaries_email.py
    """
    # (Optionally) you can inspect data = request.json if you need fields,
    # but for now we just trigger the existing scripts.
    data = request.json

    # 1) Fetch latest call logs from Vapi into call_logs.json
    try:
        subprocess.run(["python", "fetch_call_logs.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running fetch_call_logs.py:", e)
        return jsonify({"error": "fetch_failed"}), 500

    # 2) Summarize call logs into call_summaries.json
    try:
        subprocess.run(["python", "summarize_call_logs.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running summarize_call_logs.py:", e)
        return jsonify({"error": "summarize_failed"}), 500

    # 3) Send summary emails based on call_summaries.json
    try:
        subprocess.run(["python", "send_summaries_email.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error running send_summaries_email.py:", e)
        return jsonify({"error": "email_failed"}), 500

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    # Listen on port 5000 by default
    app.run(port=5000) 