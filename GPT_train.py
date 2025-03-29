import requests

url = "http://127.0.0.1:5000/chat"

messages = [
    "I'm feeling really stressed today.",
    "How can I sleep better?",
    "Give me some mental wellness tips.",
    "I'm feeling lonely. What should I do?"
]



for msg in messages:
    response = requests.post(url, json={"message": msg})
    print(f"User: {msg}")
    print(f"Bot: {response.json().get('response', 'No response')}\n")