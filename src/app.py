from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

#app = Flask(__name__)
app = Flask(__name__, template_folder='../templates')
DATA_FILE = "data/conversations.json"

# Asegurar que existe el archivo de datos
os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    
    # Lógica simple del chatbot
    responses = {
        "hola": "¡Hola! ¿Cómo estás?",
        "adios": "¡Hasta luego!",
        "hora": f"Son las {datetime.now().strftime('%H:%M')}"
    }
    
    bot_response = responses.get(user_msg.lower(), f"Recibido: {user_msg}")
    
    # Guardar conversación
    conversations = load_data()
    conversations.append({
        "timestamp": datetime.now().isoformat(),
        "user": user_msg,
        "bot": bot_response
    })
    save_data(conversations)
    
    return jsonify({"response": bot_response})

@app.route("/api/history", methods=["GET"])
def history():
    return jsonify(load_data())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
