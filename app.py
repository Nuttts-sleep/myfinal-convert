from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app) 

# --- THE ONLY CHANGE IS THIS LINE ---
API_URL = "https://yt-dlx-api.vercel.app/api/json"

@app.route('/')
def health_check():
    return jsonify({"status": "ok", "message": "Proxy server is running."})

@app.route('/convert-proxy', methods=['POST'])
def convert_proxy():
    data = request.get_json()
    youtube_url = data.get('url')

    if not youtube_url:
        return jsonify({"error": "URL is required"}), 400

    # This new API has a slightly different format
    payload = {
        "url": youtube_url,
        "isAudioOnly": True
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        # Your server talks to the new API
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status() 
        
        data = response.json()
        
        # Check for errors from the new API
        if data.get('status') == 'error':
             raise Exception(data.get('message', 'Failed to process video.'))

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error talking to API: {e}")
        return jsonify({"error": "The conversion service is currently unavailable."}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
