from flask import Flask, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import certifi
import ssl
import os


app = Flask(__name__)
CORS(app)  # GitHub Pages frontend fetch ke liye



# -------- MongoDB setup --------
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())
db = client["promptsDB"]        # database name
collection = db["prompts"]
ads_collection = db["ads"]

# -------- Serve frontend --------
@app.route('/')
def home():
    return render_template('index.html')

# -------- API for frontend --------
@app.route("/prompts")
def get_prompts():
    prompts = []
    count=0
     # _id descending order -> latest first
    for item in collection.find().sort("_id", -1):
        if count>=3:
            break
        prompts.append({
           "title": item.get("title"),
            "description": item.get("description"),
            "photo": item.get("photo"),
            "category": item.get("category")
            # timestamp optional
            
        })
        count+=1

     
    return jsonify(prompts)

@app.route("/allprompt")
def get_allprompt():
    prompts = []
   
     # _id descending order -> latest first
    for item in collection.find().sort("_id", -1):
        
        prompts.append({
           "title": item.get("title"),
            "description": item.get("description"),
            "photo": item.get("photo"),
            "category": item.get("category")
            # timestamp optional
            
        })
      
     
    return jsonify(prompts)

@app.route("/prompts-page")
def prompts_page_html():
    return render_template("prompts.html")
@app.route("/contactus")
def contactus():
    return render_template("contactus.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/ads")
def get_ads():
    ads_list = []
    for ad in ads_collection.find():
        ads_list.append({
            "title": ad.get("title"),
            "amazon_link": ad.get("amazon_link"),
            "youtube_link": ad.get("youtube_link"),
            "image": ad.get("image")
        })
    return jsonify(ads_list)
@app.route("/privacy")
def privacy():
    return render_template("privacypolicy.html")
if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True)

