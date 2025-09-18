from flask import Flask, jsonify
from flask_cors import CORS
import os, json
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app)  # ✅ यह सभी origins से requests allow करेगा

# Firebase Admin init
cred_json = os.getenv("GOOGLE_CREDENTIALS")
cred = credentials.Certificate(json.loads(cred_json))
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/")
def home():
    return "AI Prompts Backend running 🔥"

@app.route("/prompts")
def get_prompts():
    try:
        docs = db.collection("prompts").stream()
        data = [doc.to_dict() for doc in docs]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
