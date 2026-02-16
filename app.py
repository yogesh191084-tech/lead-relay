from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "HEAD"])
def home():
    return "Lead relay running", 200


@app.route("/lead", methods=["POST", "OPTIONS"])
def capture_lead():
    try:
        # Chatling may send data as form OR query params → handle both
        data = request.form.to_dict()
        if not data:
            data = request.args.to_dict()

        gas_url = "https://script.google.com/macros/s/AKfycbxtR-4ur944ZAFyxMHu0fDgtRcjUjZyez64BMD2QZjMAvLzJ4r_lv7McEqwNFPBQnNd/exec"

        r = requests.post(gas_url, data=data, timeout=15)

        return jsonify({
            "status": "success",
            "gas_status": r.status_code,
            "received": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# Render port binding (for local + Render compatibility)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
