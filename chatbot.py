import openai
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# OpenAI API Key (Use Free Trial or a Local Model)
OPENAI_API_KEY = "your_openai_api_key"

# Your API Details
API_URL = "https://stg-api.superjetom.com/getProducts"
BEARER_TOKEN = "your_bearer_token"

# Function to Chat with GPT
def chat_with_gpt(user_message):
    openai.api_key = OPENAI_API_KEY
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Change to "gpt-4" if available
        messages=[{"role": "system", "content": "You are a helpful travel assistant."},
                  {"role": "user", "content": user_message}]
    )
    
    return response["choices"][0]["message"]["content"]

# Function to Fetch Products from Your API
def get_products():
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "token": "your_api_token"
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}

# Flask Route for Chat
@app.route("/chat", methods=["POST"])
def chatbot():
    data = request.json
    user_message = data.get("message")

    # Check if user is asking about insurance
    if "insurance" in user_message.lower():
        api_data = get_products()
        return jsonify(api_data)

    # Otherwise, use GPT for response
    bot_reply = chat_with_gpt(user_message)
    return jsonify({"response": bot_reply})

# Run Flask Server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
