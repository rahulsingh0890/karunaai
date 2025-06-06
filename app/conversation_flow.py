import os
from dotenv import load_dotenv
from vapi import Vapi

# Load environment variables from .env
load_dotenv()

def initiate_call(user: dict):
    """
    Initiate a call using the Vapi assistant to handle the conversation.
    The assistant will manage the entire conversation flow based on its configuration.
    """
    api_key     = os.getenv("VAPI_API_KEY")
    from_number = os.getenv("VAPI_FROM_NUMBER")
    to_number   = user["client_phone_number"]

    if not api_key or not from_number:
        print("ERROR: VAPI_API_KEY or VAPI_FROM_NUMBER is not set in .env")
        return

    assistant_id = os.getenv("VAPI_ASSISTANT_ID")
    if not assistant_id:
        print("ERROR: VAPI_ASSISTANT_ID is not set in .env")
        return

    client = Vapi(token=api_key)

    print(f"Calling {user['client_name']} at {to_number}…")
    try:
        call_response = client.calls.create(
            assistant_id=assistant_id,
            phone_number_id=from_number,
            customer={"number": to_number}
        )
        print("Call initiated:", call_response)
    except Exception as e:
        print("ERROR initiating call:", e)
        return

if __name__ == "__main__":
    import json
    with open("config/users.json", "r") as f:
        users = json.load(f)
    print("Users loaded:", users)  # Debugging line
    if not users:
        print("No users in config/users.json")
    else:
        # Use the first user in the list
        initiate_call(users['users'][0]) 