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
        data = request.form.to_dict()

        gas_url = "https://script.google.com/macros/s/AKfycbxtR-4ur944ZAFyxMHu0fDgtRcjUjZyez64BMD2QZjMAvLzJ4r_lv7McEqwNFPBQnNd/exec"

        r = requests.post(gas_url, data=data, timeout=15)

        return jsonify({
            "status": "success",
            "gas_status": r.status_code
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# IMPORTANT: Render port binding
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
