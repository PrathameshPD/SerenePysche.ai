# app.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with actual Nemetron API details
NEMETRON_API_URL = "https://api.nemetron.com/generate"
API_KEY = "YOUR_API_KEY_HERE"

def get_nemetron_response(user_input):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": user_input,
        "model": "nemetron-70b-instruct",
        "temperature": 0.7  # Adjust as needed for creativity
    }
    response = requests.post(NEMETRON_API_URL, headers=headers, json=data)
    return response.json().get("text", "Sorry, I couldn't process that.")

@app.route("/process", methods=["POST"])
def process():
    user_input = request.json.get("input")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    response_text = get_nemetron_response(user_input)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
