# generate_response.py
import requests
import json

# API endpoint
url = "http://localhost:8000/generate/response"

# Request payload
payload = {
    "prompt": "Tell me a short story",
    "vendor": "google",  # Optional, defaults to "openai"
    "model": "gemini-2.0-flash"     # Optional, defaults to "gpt-4"
}

# Headers
headers = {
    "Content-Type": "application/json"
}

try:
    # Send POST request
    response = requests.post(url, params=payload, headers=headers)

    # Check status code
    response.raise_for_status()  # Raises an exception for 4xx/5xx errors

    # Parse and print the response
    result = response.json()
    print("Response:", json.dumps(result, indent=2))

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    if hasattr(e.response, "text"):
        print(f"Response text: {e.response.text}")