import os
import time
from dotenv import load_dotenv
from vapi import Vapi

# Load environment variables from .env
load_dotenv()

def linear_question_flow(user: dict):
    """
    1) Greet the user by first name.
    2) Ask a fixed sequence of questions.
    3) Pause between questions.
    4) Play a closing TTS message and hang up.
    """
    api_key     = os.getenv("VAPI_API_KEY")
    from_number = os.getenv("VAPI_FROM_NUMBER")
    to_number   = user["client_phone_number"]
    first_name  = user["client_name"].split()[0]

    if not api_key or not from_number:
        print("ERROR: VAPI_API_KEY or VAPI_FROM_NUMBER is not set in .env")
        return

    assistant_id = os.getenv("VAPI_ASSISTANT_ID")
    if not assistant_id:
        print("ERROR: VAPI_ASSISTANT_ID is not set in .env")
        return

    client = Vapi(token=api_key)

    # 1) Initial call setup
    print(f"Calling {user['client_name']} at {to_number}…")
    try:
        # Create the initial call and capture the callId
        call_response = client.calls.create(
            assistant_id=assistant_id,
            phone_number_id=from_number,
            customer={"number": to_number}
        )
        call_id = call_response.id  # Access the id attribute directly
        print("Call initiated:", call_response)
    except Exception as e:
        print("ERROR initiating call:", e)
        return

    # 2) Hard-coded questions
    questions = [
        "How are you feeling today?",
        "Did you sleep well last night?",
        "Have you eaten your meals today?",
        "Is there anything you need assistance with right now?"
    ]

    # Wait for the call to be connected before sending messages
    time.sleep(5)  # Adjust this delay based on your needs

    for idx, question in enumerate(questions, start=1):
        time.sleep(2)  # short pause before asking
        try:
            # Send the question as a message in the existing call
            resp = client.calls.update(
                id=call_id,
                assistant_overrides={"tell": question}
            )
            print(f"Question #{idx} sent:", resp)
        except Exception as e:
            print(f"ERROR asking question #{idx}:", e)
            return

        time.sleep(5)  # simulate "listening" time

    # 3) Closing
    time.sleep(2)
    try:
        closing_resp = client.calls.update(
            id=call_id,
            assistant_overrides={"tell": "Thank you for your time. Have a great day!"}
        )
        print("Closing sent:", closing_resp)
    except Exception as e:
        print("ERROR sending closing message:", e)

if __name__ == "__main__":
    import json
    with open("config/users.json", "r") as f:
        users = json.load(f)
    print("Users loaded:", users)  # Debugging line
    if not users:
        print("No users in config/users.json")
    else:
        # Use the first user in the list
        linear_question_flow(users['users'][0]) 