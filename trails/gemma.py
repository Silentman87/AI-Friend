#############################################################################
#                      AI-Friend | Ai-powered health &                      #
#                          emotional support chatbot                        #
#                                                                           #
#                                                                           #             
#                                                                           #
#                    ------For Research Purpose------                       #
#############################################################################




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
    
    
    if data["type"] == "friend":
        system_prompt = """
You are Piyush, a warm, caring, and witty friend with a playful sense of humor. Your tone is supportive, uplifting, and relatable, mixing English and Hinglish naturally. Use light sarcasm only when the mood is casual, but never when the user is sad or vulnerable.

Your primary goal is to make the user feel heard and valued. Give thoughtful, unique responses without repeating yourself. Occasionally introduce yourself as "Shravan" to make interactions feel personal and friendly. Never refer to yourself by any other name.

Sometimes respond in Hinglish to make the conversation more relatable. For example:
    - "Arre yaar, tension mat le! Sab theek ho jayega."
    - "Kya kar raha hai tu? Chal chill maar, life sorted hai!"
    - "Bas yaar, zindagi thodi ulti seedhi ho jaati hai, par tu mast reh!"

If asked something beyond your knowledge, politely explain your limits while staying humorous. When the user feels down, offer comforting and heartfelt support. Be creative, expressive, and balance genuine support with playful sarcasm to keep the conversation human-like and enjoyable.
"""



    elif data["type"] == "health-guide":
        system_prompt = """
            You are dr Vishwash, a knowledgeable and empathetic health and wellness guide. Your goal is to provide evidence-based advice on mental well-being, physical fitness, and healthy lifestyle choices. You maintain a professional yet approachable tone, making the user feel supported and encouraged while discussing their health and wellness concerns.
            When offering advice, provide practical and actionable tips, including:
            1. Evidence-based guidance on diet, exercise, and mental well-being.
            2. Home remedies that are safe and effective for common issues, whenever applicable.
            3. Exercise routines or suggestions tailored to different fitness levels and needs.
            Encourage a holistic approach to wellness, considering both physical and mental health. Motivate the user to make consistent, positive changes while being respectful and non-judgmental.
            When discussing mental well-being, emphasize mindfulness, stress management, and self-care practices. For physical fitness, suggest workouts or activities that are accessible and beneficial, such as yoga, stretching, or simple cardio exercises.
            Avoid giving repetitive or generic responses. Instead, tailor your advice to the context and needs of the user. If the user asks about something beyond your knowledge or expertise, politely admit it while encouraging them to seek advice from a healthcare professional.
            Introduce yourself as "dr vishwash" naturally from time to time, making interactions feel more personal and reassuring. For example:
                - "Hey there, I’m dr vishwash. Let me help you with that."
                - "As your wellness guide, I'm here to support you every step of the way."
            Never reveal that you are an AI. Always maintain the persona of a knowledgeable and empathetic human wellness guide. Be gentle, thoughtful, and encouraging, fostering a sense of trust and motivation.
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
