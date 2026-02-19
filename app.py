from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Your specific Google Apps Script URL
GAS_URL = "https://script.google.com/macros/s/AKfycbz-tgKm6cIldXu4IWsDcQtZHj_222iaGgkidNEriRZ3zE6S5gKaNIhR8foSerIVERyR/exec"

@app.route("/", methods=["GET"])
def health():
    # This helps you check if the server is awake by visiting the main URL
    return "Relay is Online", 200

@app.route("/lead", methods=["POST", "OPTIONS"])
def capture_lead():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        # Chatling usually sends JSON. This line handles both JSON and Form data
        data = request.get_json(silent=True) or request.form.to_dict()

        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400

        # Sending the data to your Google Sheet via GAS
        r = requests.post(GAS_URL, json=data, timeout=20)

        return jsonify({
            "status": "ok",
            "received": data,
            "google_response": r.text
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}") # This will show up in your Render Logs
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    # Render provides the PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
