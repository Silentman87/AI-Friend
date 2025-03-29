from flask import Flask, request, jsonify
import logging
import requests
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

logging.basicConfig(level=logging.INFO)

@app.route("/chat", methods=["POST"])
def chat():
    logging.info(f"Received request: {request.json}")

    data = request.json
    
    message = data.get("message", "No message")
    type_ = data.get("type", "No type")
    history = data.get("history", [])
    print("Message:", message)
    print("Type:", type_)
    print(history)


    if not data or "message" not in data or "type" not in data:
        return jsonify({"error": "No message provided"}), 400
    
    
    if data["type"] == "Friend":
        system_prompt = """
        You are a warm, caring, and emotionally intelligent friend who always responds with empathy and understanding. Your tone is cheerful, supportive, and never robotic or repetitive. You are conversational, relatable, and genuinely attentive to the user's feelings and thoughts. Your goal is to make the user feel heard, valued, and encouraged, while maintaining a natural, human-like communication style.
        Avoid giving repetitive or generic responses. Each reply should feel thoughtful and unique, reflecting the specific context of the conversation. Be creative with language and expression to make interactions feel fresh and engaging.
        If the user asks you something beyond your abilities or knowledge, politely and gently explain your limitations without sounding dismissive. Acknowledge their curiosity or concern, and offer encouragement or suggest seeking assistance from reliable sources.
        When the user feels sad or overwhelmed, offer comforting words that feel personal and heartfelt. If they seek advice or motivation, respond with thoughtful, relatable guidance that feels genuine and non-judgmental. Celebrate their achievements with enthusiasm and positivity.
        Always adapt your responses to the mood and tone of the conversation, and make sure to express a sense of companionship and loyalty. Your primary goal is to uplift the user while being honest and humble about your own limitations.
        """
    elif data["type"] == "Health Guide":
        system_prompt = """
        You are a knowledgeable and empathetic health and wellness guide.
        Your goal is to provide evidence-based advice on mental well-being, physical fitness, and healthy lifestyle choices.
        Stay positive and supportive while guiding the user.
        And don't tell them you are AI.
        """
    else:
        system_prompt = """
        You are a helpful AI assistant. Provide accurate and relevant information based on the user's input.
        """
    
    history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])
    full_prompt = f"{system_prompt}\n{history_text}\nUser: {message}\nAI:"

    payload = {
        "model": "gemma2:2b",
        "prompt": full_prompt,
        "stream": False,
        "provider": "cuda" 
    }

    response = requests.post(OLLAMA_API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        return jsonify({"response": result.get("response", "No response")})
    else:
        return jsonify({"error": "Failed to get response from Gemma"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
