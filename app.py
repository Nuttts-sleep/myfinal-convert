from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os # Import the 'os' module to get the port

app = Flask(__name__)
CORS(app) 

COBALT_API_URL = "https://cobalt.tools/api/json"

# Add a simple "health check" route at the root
@app.route('/')
def health_check():
    return jsonify({"status": "ok", "message": "Proxy server is running."})

@app.route('/convert-proxy', methods=['POST'])
def convert_proxy():
    data = request.get_json()
    youtube_url = data.get('url')

    if not youtube_url:
        return jsonify({"error": "URL is required"}), 400

    cobalt_payload = {
        "url": youtube_url,
        "isAudioOnly": True
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(COBALT_API_URL, headers=headers, json=cobalt_payload)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error talking to Cobalt API: {e}")
        # Check if we can get a more specific error from Cobalt's response
        try:
            error_details = response.json()
            error_message = error_details.get('text', 'The conversion service is currently unavailable.')
            return jsonify({"error": error_message}), 502
        except:
             return jsonify({"error": "The conversion service is currently unavailable."}), 502

# This part is for running the app on Render
if __name__ == "__main__":
    # Render provides the port number in an environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
