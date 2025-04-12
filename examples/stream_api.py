import requests
import json

# API endpoint
url = "http://localhost:8000/stream/response"

# Request payload
payload = {
    "prompt": "Write a poem about the sea",
    "vendor": "google",  # Optional
    "model": "gemini-2.0-flash"  # Optional
}

# Headers
headers = {
    "Content-Type": "application/json",
    "Accept": "text/event-stream"  # Optional, but can be application/json for JSON streaming
}

try:
    # Send POST request with streaming enabled
    with requests.post(url, params=payload, headers=headers, stream=True) as response:
        response.raise_for_status()  # Check for initial errors

        # Process the stream
        print("Streaming response:")
        for line in response.iter_lines(decode_unicode=True):
            if line:  # Filter out keep-alive lines
                try:
                    data = json.loads(line)
                    if "response" in data:
                        print(data["response"], end="", flush=True)
                    elif "error" in data:
                        print(f"\nError in stream: {data['error']}")
                        break
                except json.JSONDecodeError:
                    print(f"Raw chunk: {line}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    if hasattr(e.response, "text"):
        print(f"Response text: {e.response.text}")