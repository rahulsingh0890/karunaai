import os
from dotenv import load_dotenv
from vapi import Vapi

# Load environment variables from .env
load_dotenv()

def test_api_connection():
    """
    Test the connection to Vapi API by making a simple request.
    """
    api_key = os.getenv("VAPI_API_KEY")
    
    if not api_key:
        print("❌ VAPI_API_KEY is not set in your .env file")
        return
    
    print("🔑 Using API Key:", api_key[:8] + "..." + api_key[-4:])
    
    try:
        # Initialize the client
        client = Vapi(token=api_key)
        
        # Try to list phone numbers (a simple API call)
        response = client.phone_numbers.list()
        print("✅ Successfully connected to Vapi API!")
        print("📱 Found", len(response), "phone numbers")
        
    except Exception as e:
        print("❌ Failed to connect to Vapi API:")
        print("Error:", str(e))

if __name__ == "__main__":
    test_api_connection() 