import google.generativeai as genai

# PASTE YOUR ACTUAL KEY HERE JUST FOR THIS TEST
API_KEY = "AQ.Ab8RN6IzV1fFLQpTv4oK6rydMyrQfJ3ckoWvQrdWZOQeUZPxYA"

print("Booting diagnostic test...")

try:
    genai.configure(api_key=API_KEY)
    
    # Using the standard 1.5 flash model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    print("Sending test ping to Google servers...")
    
    # A simple, non-chat request to test raw connectivity
    response = model.generate_content("Respond with exactly one word: 'Online'.")
    
    print(f"\n[SERVER RESPONSE]: {response.text.strip()}")
    print("[RESULT]: Test SUCCESSFUL! The API is working perfectly.")

except Exception as e:
    print(f"\n[RESULT]: Test FAILED. Here is the exact error:")
    print(f"--> {e}")