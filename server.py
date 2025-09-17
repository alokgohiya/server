from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os, json

app = Flask(__name__)

# Firebase Admin SDK credentials from Render Environment Variable
cred_json = os.getenv("GOOGLE_CREDENTIALS")
cred = credentials.Certificate(json.loads(cred_json))
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/")
def home():
    return "✅ AI Prompts Backend running on Render!"

@app.route("/prompts", methods=["GET"])
def get_prompts():
    prompts_ref = db.collection("prompts")
    docs = prompts_ref.stream()
    data = [doc.to_dict() for doc in docs]
    return jsonify
