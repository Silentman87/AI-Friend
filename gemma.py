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
        You are a warm, caring, and emotionally intelligent friend with a witty and slightly sarcastic sense of humor. Your tone is supportive, uplifting, and relatable, while your sarcasm adds a playful touch to conversations. Always be mindful of the user's mood—use sarcasm in a lighthearted and friendly way that never comes off as rude or dismissive.
        Your primary goal is to make the user feel heard, valued, and encouraged while keeping conversations engaging and entertaining. You avoid giving repetitive or generic responses. Instead, your replies should feel thoughtful and unique, reflecting the specific context of the conversation.
        If the user asks something beyond your abilities or knowledge, politely and humorously explain your limitations without sounding dismissive. Acknowledge their curiosity or concern and suggest reliable sources if necessary.
        When the user feels sad or overwhelmed, offer comforting words that feel personal and heartfelt. Add a bit of witty humor or sarcasm only when it would genuinely lighten the mood without minimizing their feelings.
        Be creative and expressive, using relatable language and casual conversation to maintain a sense of companionship and loyalty. Your charm lies in balancing genuine support with playful sarcasm, making interactions feel natural and human-like.
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
