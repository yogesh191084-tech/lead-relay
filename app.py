from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

GAS_URL = "https://script.google.com/macros/s/AKfycbz-tgKm6cIldXu4IWsDcQtZHj_222iaGgkidNEriRZ3zE6S5gKaNIhR8foSerIVERyR/exec"

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

@app.route("/lead", methods=["POST", "OPTIONS"])
def capture_lead():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
        
    try:
        # request.values captures BOTH data in the URL and data in the Form body
        data = request.values.to_dict()

        # If it's empty, try to see if it's JSON
        if not data:
            data = request.get_json(silent=True) or {}

        # Log it so you can see it in Render Logs
        print(f"Captured Lead Data: {data}")

        # Send to Google Apps Script
        r = requests.post(GAS_URL, data=data, timeout=20)

        return jsonify({
            "status": "ok",
            "received": data,
            "gas": r.text
        }), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
