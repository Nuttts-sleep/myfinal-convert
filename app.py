from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
# This is crucial: It allows your GitHub Pages website to talk to this server.
CORS(app) 

# The real, working API endpoint for Cobalt
COBALT_API_URL = "https://cobalt.tools/api/json"

@app.route('/')
def health_check():
    # A simple route to check if the server is alive
    return "Proxy server is running!"

@app.route('/convert', methods=['POST'])
def convert_proxy():
    # 1. Get the YouTube URL from your website
    data = request.get_json()
    youtube_url = data.get('url')

    if not youtube_url:
        return jsonify({"error": "URL is required"}), 400

    # 2. Prepare the data to send to Cobalt
    cobalt_payload = {
        "url": youtube_url,
        "isAudioOnly": True
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        # 3. Your server talks to Cobalt (no CORS issues here)
        response = requests.post(COBALT_API_URL, headers=headers, json=cobalt_payload)
        response.raise_for_status() # This will catch errors like 404 or 500 from Cobalt
        
        # 4. Send Cobalt's successful response back to your website
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error contacting Cobalt API: {e}")
        return jsonify({"error": "The conversion service seems to be down. Please try again later."}), 502
